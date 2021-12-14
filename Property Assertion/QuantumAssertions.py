import pandas as pd  
import math
import numpy as np
import scipy.stats as sci

from statsmodels.stats.proportion import proportions_ztest

from qiskit import execute
from qiskit.circuit import ClassicalRegister

def assertPhase(backend, quantumCircuit, qubits_to_assert, expected_phases, measurements_to_make, alpha):
    ## if "qubits to assert" is just a single value, convert it to a list containing the single value
    if (not isinstance(qubits_to_assert, list)):
        qubits_to_assert = [qubits_to_assert]

    ## if "expected phases" is just a single value, convert it to a list containing the single value
    if (not isinstance(expected_phases, list)):
        expected_phases = [expected_phases]

    ## needs to make at least 2 measurements, one for x axis, one for y axis
    ## realistically we need more for any statistical significance
    if (measurements_to_make < 2):
        raise ValueError("Must make at least 2 measurements")

    ## classical register must be of same length as amount of qubits to assert
    ## if there is no classical register, add one
    if (quantumCircuit.num_clbits == 0):
        quantumCircuit.add_register(ClassicalRegister(len(qubits_to_assert)))
    elif (quantumCircuit.num_clbits != len(qubits_to_assert)):
        raise ValueError("QuantumCircuit classical register length not equal to qubits to assert")

    ## divide measurements to make by 2 as we need to run measurements twice, one for x and one for y
    measurements_to_make = measurements_to_make // 2

    ## copy the circit and set measurement to y axis
    yQuantumCircuit = measure_y(quantumCircuit.copy(), qubits_to_assert)

    ## measure the x axis
    xQuantumCircuit = measure_x(quantumCircuit, qubits_to_assert)

    ## get y axis results
    yJob = execute(yQuantumCircuit, backend, shots=measurements_to_make, memory=True)
    yCounts = yJob.result().get_counts()

    ## get x axis results
    xJob = execute(xQuantumCircuit, backend, shots=measurements_to_make, memory=True)
    xCounts = xJob.result().get_counts()

    ## make a df to keep track of the predicted angles 
    resDf = pd.DataFrame(columns=['+','i','-','-i'])

    ## fill the df with the x and y results of each qubit that is being asserted
    classical_qubit_index = 1
    for qubit in qubits_to_assert:
        plus_amount, i_amount, minus_amount, minus_i_amount = 0,0,0,0
        for experiment in xCounts:
            if (experiment[len(qubits_to_assert)-classical_qubit_index] == '0'):
                plus_amount += xCounts[experiment]
            else:
                minus_amount += xCounts[experiment]
        for experiment in yCounts:
            if (experiment[len(qubits_to_assert)-classical_qubit_index] == '0'):
                i_amount += yCounts[experiment]
            else:
                minus_i_amount += yCounts[experiment]
        df = {'+':plus_amount, 'i':i_amount,
              '-':minus_amount, '-i':minus_i_amount}
        resDf = resDf.append(df, ignore_index = True)
        classical_qubit_index+=1

    ## convert the columns to a strict numerical type
    resDf['+'] = resDf['+'].astype(int)
    resDf['i'] = resDf['i'].astype(int)
    resDf['-'] = resDf['-'].astype(int)
    resDf['-i'] = resDf['-i'].astype(int)

    print(f"full df \n {resDf}")


    xAmount = resDf['-'].tolist()
    yAmount = resDf['-i'].tolist()

    # print(f"x amounts {xAmount}")
    # print(f"y amounts {yAmount}")

    ## make a dataframe that contains p values of chi square tests to analyse results
    ## if x and y counts are both 25/25/25/25, it means that we cannot calculate a phase
    ## we assume that a qubit that is in |0> or |1> position to have 50% chance to fall 
    ## either way, like a coin toss: We treat X and Y results like coin tosses 
    pValues = pd.DataFrame(columns=['X','Y'])    
    pValues['X'] = resDf.apply(lambda row: applyChiSquareX(row, measurements_to_make/2), axis=1)
    pValues['Y'] = resDf.apply(lambda row: applyChiSquareY(row, measurements_to_make/2), axis=1)

    ## check p values on chi square test, we use a low value to be sure that 
    ## we only except if we are certain there is an issue with the x, y results
    pValues = pValues > 0.00001

    ## if both pvalues are more than 0.00001, we are pretty certain that the results follow an even distribution
    ## likely that the qubit is not in the fourier basis (very likely in the |0> or |1> state)
    pValues.apply(lambda row: assertIfBothTrue(row), axis=1)

    ## this sequence of operations converts from measured results
    ## into an angle for phase: 
    ## with 0   (       0 rad) signifying the |+> state
    ## with 90  (    pi/2 rad) signifying the |i> state
    ## with 180 (      pi rad) signifying the |-> state
    ## with 270 (3 * pi/2 rad) signifying the |-i> state
    resDf = resDf / measurements_to_make
    resDf = resDf * 2
    resDf = resDf - 1
    resDf = np.arccos(resDf)
    resDf = resDf * 180
    resDf = resDf / math.pi
    
    ## to get a final result for phase on each qubit:
    ## we must get the lowest 2 values for each column
    lowestDf = pd.DataFrame(columns=['lowest','lowest-location','second-lowest','second-lowest-location','estimated-phase'])
    
    ## store the lowest value as well as what column it is from
    lowestDf['lowest'] = resDf.min(axis=1)
    lowestDf['lowest-location'] = resDf.idxmin(axis=1)

    ## remove the lowest value from the dataframe
    lowestDf = lowestDf.apply(lambda row: setLowestCellToNan(row, resDf), axis=1)

    ## store the second lowest value from the dataframe as well as the column
    lowestDf['second-lowest'] = resDf.min(axis=1)
    lowestDf['second-lowest-location'] = resDf.idxmin(axis=1)

    ## estimate the phase and put it in a new column
    lowestDf['estimated-phase'] =  lowestDf.apply(lambda row: setPhaseEstimate(row), axis=1)

    ## calculate what the expected row would be for the expected phase
    #expectedX, expectedY = expectedPhaseToRow(expected_phases[0],measurements_to_make)
    expectedX = np.zeros(len(expected_phases)).astype(int)
    expectedY = np.zeros(len(expected_phases)).astype(int)

    for idx, phase in enumerate(expected_phases):
        expectedX[idx], expectedY[idx] = expectedPhaseToRow(expected_phases[idx],measurements_to_make)

    #print(type(expectedX[0]))
    # print(f"expected x {expectedX}")
    # print(f"expected y {expectedY}")

    for i in range(len(qubits_to_assert)):
        ## set observed X values in a table
        observedXtable = [xAmount[i],measurements_to_make-xAmount[i]]
        ## set expected X values in a table
        expectedXtable = [expectedX[i],measurements_to_make-expectedX[i]]

        ## set observed Y values in a table
        observedYtable = [yAmount[i],measurements_to_make-yAmount[i]]
        ## set expected Y values in a table
        expectedYtable = [expectedY[i],measurements_to_make-expectedY[i]]

        xPvalue = sci.chisquare(f_obs=observedXtable, f_exp=expectedXtable)[1]

        yPvalue = sci.chisquare(f_obs=observedYtable, f_exp=expectedYtable)[1]

        print(observedXtable)
        print(expectedXtable)
        print(sci.chisquare(f_obs=observedXtable, f_exp=expectedXtable)[1])

        print(observedYtable)
        print(expectedYtable)
        print(sci.chisquare(f_obs=observedYtable, f_exp=expectedYtable)[1])

        if (yPvalue != np.NaN and yPvalue <= alpha):
            raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in qubit {qubits_to_assert[i]} according to significance level {alpha}"))
        if (xPvalue != np.NaN and xPvalue <= alpha):
            raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in qubit {qubits_to_assert[i]} according to significance level {alpha}"))
        

    # ## set observed X values in a table
    # observedX = [xAmount,measurements_to_make-xAmount]
    # ## set expected X values in a table
    # expectedX = [expectedX,measurements_to_make-expectedX]

    # ## set observed Y values in a table
    # observedY = [yAmount,measurements_to_make-yAmount]
    # ## set expected Y values in a table
    # expectedY = [expectedY,measurements_to_make-expectedY]

    # print(observedX)
    # print(expectedX)

    # print(observedY)
    # print(expectedY)

    # print(sci.chisquare(f_obs=observedX, f_exp=expectedX)[1])
    # xPvalue = sci.chisquare(f_obs=observedX, f_exp=expectedX)[1]

    # print(sci.chisquare(f_obs=observedY, f_exp=expectedY)[1])
    # yPvalue = sci.chisquare(f_obs=observedY, f_exp=expectedY)[1]

    # if (yPvalue != np.NaN and yPvalue <= alpha):
    #     raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))
    # if (xPvalue != np.NaN and xPvalue <= alpha):
    #     raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))
    


## assert that 2 qubits are equal
def assertEqual(backend, quantumCircuit, qubit1, qubit2, measurements_to_make, alpha):
    ## needs to make at least 2 measurements, one for x axis, one for y axis
    ## realistically we need more for any statistical significance
    if (measurements_to_make < 2):
        raise ValueError("Must make at least 2 measurements")

    ## classical register must be of same length as amount of qubits to assert
    ## if there is no classical register, add one
    if (quantumCircuit.num_clbits == 0):
        quantumCircuit.add_register(ClassicalRegister(2))
    elif (quantumCircuit.num_clbits != 2):
        raise ValueError("QuantumCircuit classical register must be of length 2")

    ## divide measurements to make by 3 as we need to run measurements twice, one for x and one for y
    measurements_to_make = measurements_to_make // 3

    ## copy the circit and set measurement to y axis
    yQuantumCircuit = measure_y(quantumCircuit.copy(), [qubit1, qubit2])

    ## measure the x axis
    xQuantumCircuit = measure_x(quantumCircuit.copy(), [qubit1, qubit2])

    ## measure the z axis
    zQuantumCircuit = measure_z(quantumCircuit, [qubit1, qubit2])

    ## get y axis results
    yJob = execute(yQuantumCircuit, backend, shots=measurements_to_make, memory=True)
    yMemory = yJob.result().get_memory()
    yCounts = yJob.result().get_counts()

    ## get x axis results
    xJob = execute(xQuantumCircuit, backend, shots=measurements_to_make, memory=True)
    xMemory = xJob.result().get_memory()
    xCounts = xJob.result().get_counts()

    ## get z axis results
    zJob = execute(zQuantumCircuit, backend, shots=measurements_to_make, memory=True)
    zMemory = zJob.result().get_memory()
    zCounts = zJob.result().get_counts()

    # xDf = pd.DataFrame(columns=['q0', 'q1'])
    # yDf = pd.DataFrame(columns=['q0', 'q1'])
    # zDf = pd.DataFrame(columns=['q0', 'q1'])

    # for row in yMemory:
    #     yDf = yDf.append({'q0':row[0], 'q1':row[1]}, ignore_index=True)

    # for row in xMemory:
    #     xDf = xDf.append({'q0':row[0], 'q1':row[1]}, ignore_index=True)

    # for row in zMemory:
    #     zDf = zDf.append({'q0':row[0], 'q1':row[1]}, ignore_index=True)

    # yDf = yDf.astype(int)
    # xDf = xDf.astype(int)
    # zDf = zDf.astype(int)

    #yStat, yPvalue = (sci.ttest_ind(yDf['q0'], yDf['q1']))
    #xStat, xPvalue = (sci.ttest_ind(xDf['q0'], xDf['q1']))
    #zStat, zPvalue = (sci.ttest_ind(zDf['q0'], zDf['q1']))

    print(alpha)

    #print(f"Y p-value {yPvalue}")
    #print(f"X p-value {xPvalue}")
    #print(f"Z p-value {zPvalue}")

    # if (yPvalue != np.NaN and yPvalue <= alpha):
    #     raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))
    # if (xPvalue != np.NaN and xPvalue <= alpha):
    #     raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))
    # if (zPvalue != np.NaN and zPvalue <= alpha):
    #     raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))

    ## make a df to keep track of the predicted angles 
    resDf = pd.DataFrame(columns=['0','1','+','i','-','-i'])
    
    ## fill the df with the x and y results of each qubit that is being asserted
    classical_qubit_index = 1
    for qubit in [qubit1,qubit2]:
        zero_amount, one_amount, plus_amount, i_amount, minus_amount, minus_i_amount = 0,0,0,0,0,0
        for experiment in xCounts:
            if (experiment[2-classical_qubit_index] == '0'):
                plus_amount += xCounts[experiment]
            else:
                minus_amount += xCounts[experiment]
        for experiment in yCounts:
            if (experiment[2-classical_qubit_index] == '0'):
                i_amount += yCounts[experiment]
            else:
                minus_i_amount += yCounts[experiment]
        for experiment in zCounts:
            if (experiment[2-classical_qubit_index] == '0'):
                zero_amount += zCounts[experiment]
            else:
                one_amount += zCounts[experiment]
        df = {'0':zero_amount, '1':one_amount,
              '+':plus_amount, 'i':i_amount,
              '-':minus_amount,'-i':minus_i_amount}
        resDf = resDf.append(df, ignore_index = True)
        classical_qubit_index+=1

    ## convert the columns to a strict numerical type
    resDf['+'] = resDf['+'].astype(int)
    resDf['i'] = resDf['i'].astype(int)
    resDf['-'] = resDf['-'].astype(int)
    resDf['-i'] = resDf['-i'].astype(int)
    resDf['0'] = resDf['0'].astype(int)
    resDf['1'] = resDf['1'].astype(int)

    print(resDf.astype(str))

    print(resDf['1'][0].astype(int))
    print(resDf['1'][1].astype(int))

    print(resDf['-'][0].astype(int))
    print(resDf['-'][1].astype(int))

    print(resDf['-i'][0].astype(int))
    print(resDf['-i'][1].astype(int))

    zStat_z, zPvalue = proportions_ztest(count=[resDf['1'][0],resDf['1'][1]], nobs=[measurements_to_make, measurements_to_make],  alternative='two-sided')
    zStat_x, xPvalue = proportions_ztest(count=[resDf['-'][0],resDf['-'][1]], nobs=[measurements_to_make, measurements_to_make],  alternative='two-sided')
    zStat_y, yPvalue = proportions_ztest(count=[resDf['-i'][0],resDf['-i'][1]], nobs=[measurements_to_make, measurements_to_make],  alternative='two-sided')

    print(zPvalue, zStat_z)
    print(xPvalue, zStat_x)
    print(yPvalue, zStat_y)

    if (yPvalue != np.NaN and yPvalue <= alpha):
        raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))
    if (xPvalue != np.NaN and xPvalue <= alpha):
        raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))
    if (zPvalue != np.NaN and zPvalue <= alpha):
        raise(AssertionError(f"Null hypothesis rejected, there is a significant enough difference in the qubits according to significance level {alpha}"))

    # ## apply t test to see if two populations of results on qu  bits are expected to from the same population
    # resDf.apply(lambda row: applyTtest(row), axis=1)

def measure_x(circuit, qubitIndexes):
    cBitIndex = 0
    for index in qubitIndexes:
        circuit.h(index)
        circuit.measure(index, cBitIndex)
        cBitIndex+=1
    return circuit

def measure_y(circuit, qubit_indexes):
    cBitIndex = 0
    for index in qubit_indexes:
        circuit.sdg(index)
        circuit.h(index)
        circuit.measure(index, cBitIndex)
        cBitIndex+=1
    return circuit

def measure_z(circuit, qubit_indexes):
    cBitIndex = 0
    for index in qubit_indexes:
        circuit.measure(index, cBitIndex)
        cBitIndex+=1
    return circuit

def setLowestCellToNan(row, resDf):
    for col in row.index:
        resDf.iloc[row.name][row[col]] = np.nan
    return row

def setPhaseEstimate(row):
    overallPhase = 0
    if(row['lowest-location'] == '+'):
        if(row['second-lowest-location'] == 'i'):
            overallPhase = 0 + row['lowest']
        elif (row['second-lowest-location'] == '-i'):
            overallPhase = 360 - row['lowest']
            if (row['lowest'] == 0):
                overallPhase = 0
    elif(row['lowest-location'] == 'i'):
        if(row['second-lowest-location'] == '+'):
            overallPhase = 90 - row['lowest']
        elif (row['second-lowest-location'] == '-'):
            overallPhase = 90 + row['lowest']
    elif(row['lowest-location'] == '-'):
        if(row['second-lowest-location'] == 'i'):
            overallPhase = 180 - row['lowest']
        elif (row['second-lowest-location'] == '-i'):
            overallPhase = 180 + row['lowest']
    elif(row['lowest-location'] == '-i'):
        if(row['second-lowest-location'] == '+'):
            overallPhase = 270 + row['lowest']
        elif (row['second-lowest-location'] == '-'):
            overallPhase = 270 - row['lowest']
    return overallPhase

def expectedPhaseToRow(expected_phase, number_of_measurements):
    # print(expected_phase)
    # print(number_of_measurements)
    expected_phase_y = expected_phase - 90
    expected_phase_y = expected_phase_y * math.pi
    expected_phase_y = expected_phase_y / 180
    expected_phase_y = np.cos(expected_phase_y)
    expected_phase_y = expected_phase_y + 1
    expected_phase_y = expected_phase_y / 2
    expected_phase_y = expected_phase_y * number_of_measurements
    expected_phase = expected_phase * math.pi
    expected_phase = expected_phase / 180
    expected_phase = np.cos(expected_phase)
    expected_phase = expected_phase + 1
    expected_phase = expected_phase / 2
    expected_phase = expected_phase * number_of_measurements
    # print(f"phase + {expected_phase} ---- phase - {number_of_measurements-expected_phase}") 
    # print(f"phase i {expected_phase_y} ---- phase -i {number_of_measurements-expected_phase_y}") 
    xRes = int(round(number_of_measurements-expected_phase))
    yRes = int(round(number_of_measurements-expected_phase_y))
    return((xRes, yRes))

def applyChiSquareX(row, expected_amount):
    observed = [row['+'],row['-']]
    expected = [expected_amount,expected_amount]
    return(sci.chisquare(f_obs=observed, f_exp=expected)[1])

def applyChiSquareY(row, expected_amount):
    observed = [row['i'],row['-i']]
    expected = [expected_amount,expected_amount]
    return(sci.chisquare(f_obs=observed, f_exp=expected)[1])

def assertIfBothTrue(row):
    if row.all():
        raise AssertionError("Qubit does not appear to have a phase applied to it!")

# def assertIfExpectedDoNotFitTolerance(row, expected, tolerance):
#     deltaAngle = (row['estimated-phase'] - expected[row.name] + 180 + 360) % 360 - 180
#     print('observed: ' + str(row['estimated-phase']))
#     print('predicted: ' + str(expected[row.name]))
#     print('diff: ' + str(deltaAngle))
#     if (abs(deltaAngle) > tolerance):
#         raise AssertionError(f"The estimated angle ({row['estimated-phase']}) is off the prediction ({expected[row.name]}) +- tolerance value ({tolerance}) specified")
    