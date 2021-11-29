import pandas as pd  
import math
import numpy as np
import scipy.stats as sci

from qiskit import execute
from qiskit.circuit import ClassicalRegister

def returnPhase(backend, quantumCircuit, qubits_to_assert, expected_phases, measurements_to_make, tolerance):
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
    lowestDf['estimated-phase'] =  lowestDf.apply(lambda row: setPhaseEstimate(row, resDf), axis=1)

    ## check that the estimated phase fits in the tolerance
    lowestDf.apply(lambda row: assertIfExpectedDoNotFitTolerance(row, expected_phases, tolerance), axis=1)

    return(lowestDf['estimated-phase'][0])
    #return(lowestDf['estimated-phase'][0])

    
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

def setLowestCellToNan(row, resDf):
    for col in row.index:
        resDf.iloc[row.name][row[col]] = np.nan
    return row

def setPhaseEstimate(row, resDf):
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
        #raise AssertionError("Qubit does not appear to have a phase applied to it!")
        pass

def assertIfExpectedDoNotFitTolerance(row, expected, tolerance):
    deltaAngle = (row['estimated-phase'] - expected[row.name] + 180 + 360) % 360 - 180
    #print('observed: ' + str(row['estimated-phase']))
    #print('predicted: ' + str(expected[row.name]))
    #print('diff: ' + str(deltaAngle))
    if (abs(deltaAngle) > tolerance):
        #raise AssertionError(f"The estimated angle ({row['estimated-phase']}) is off the prediction ({expected[row.name]}) +- tolerance value ({tolerance}) specified")
        pass
    