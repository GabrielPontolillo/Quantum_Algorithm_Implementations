import unittest
from matplotlib.pyplot import close
import numpy as np

import hypothesis.strategies as st
from hypothesis import given, settings
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import QFT
from math import pi, degrees, sqrt, sin, cos

# importing sys
import sys

from sympy import false
  
# adding Folder_2 to the system path
import pathlib

sys.path.insert(0, str(pathlib.Path().resolve())+f"/Property_Assertion")

from QuantumAssertions import assertPhase

#####################################################################################
### Change the file to import from, in order to test a mutant version of the code ###
##################################################################################################
### e.g. from Add_mutant_1 import remove_garbage, generate_binary, encode_message, measure_message
##################################################################################################

from QuantumFourierTransform import qft_rotations, flip_endian, qft_rotations_not_inplace

###########################################################################
## Define composite strategies to generate lists of ints in equal length ##
###########################################################################

@st.composite
def size_and_value_to_input(draw):
    circuit_size = draw(st.integers(min_value=1, max_value=4))
    value = draw(st.integers(min_value=0, max_value=(2**circuit_size)-1))
    return(circuit_size,value)

##########################
## test generate binary ##
##########################
@given(size_and_value_to_input())
@settings(deadline=None)
def test_qft_then_inverse(vals):
    size = vals[0]
    value = vals[1]
     
    qc = QuantumCircuit(size)
    binValue = bin(value)[2:].zfill(size)[::-1]
    
    for i in range(size):
        if binValue[i] == "1":
            qc.x(i) 

    qft_rotations(qc, size)
    qc.append(QFT(num_qubits=size, do_swaps=false, inverse=True), [i for i in range(size)])

    qc.measure_all()

    backend = Aer.get_backend('aer_simulator') 
    job = execute(qc, backend, shots=1, memory=True)
    readings = job.result().get_memory()[0]
    assert(value == int(readings,2))

@given(size_and_value_to_input())
@settings(deadline=None)
def test_specific_phase(vals):
    size = vals[0]
    value = vals[1]
     
    qc = QuantumCircuit(size)
    binValue = bin(value)[2:].zfill(size)[::-1]
    
    for i in range(size):
        if binValue[i] == "1":
            qc.x(i) 

    qft_rotations(qc, size)
    
    backend = Aer.get_backend('aer_simulator') 

    expected_values = []
    
    print(size)
    print(value)
    
    for i in range(size):
        expected_values.append(degrees(pi*value/2**i)%360)

    
    assertPhase(backend, qc, [i for i in range(size)], expected_values, 3000000, 0.01)

@given(size_and_value_to_input())
@settings(deadline=None)
def test_superposition_inputs(vals):
    size = vals[0]
    value = vals[1]
    
    qc = QuantumCircuit(size)

    expected_values = []
    for i in range(size):
        expected_values.append(degrees(pi*value/2**i)%360)

    init_vector = calculate_tensor_product(angle_to_vector(expected_values))[0]

    #for vect in init_vector:
        #print(vect)

    qc.initialize(init_vector, [i  for i in range(size)])

    qc.append(qft_rotations_not_inplace(size).inverse(), [i for i in range(size)])

    qc.measure_all()

    backend = Aer.get_backend('aer_simulator') 

    job = execute(qc, backend, shots=10000)#run the circuit 1000000 times
    assert(len(job.result().get_counts()) == 1)
    assert(int(job.result().get_counts().most_frequent(), 2) == value)
    print(int(job.result().get_counts().most_frequent(), 2))
    print(job.result().get_counts())
    print(value)

###########################
## Define helper methods ##
###########################

def calculate_tensor_product(vectors):
    """ 
    takes in array of pairs of complex numbers
    returns statevector array
    (recursively)
    """
    if vectors == []:
        return vectors
    elif len(vectors) == 1:
        return vectors
    else:
        v1 = vectors.pop(-1)
        v2 = vectors.pop(-1)
        newvect = []
        for v1_val in v1:
            for v2_val in v2:
                newvect.append(v1_val*v2_val)
        vectors.append(newvect)
        return calculate_tensor_product(vectors)

        
    

def angle_to_vector(expected_values):
    """ 
    takes in array of angles (degrees)
    returns pairs of complex numbers
    """
    plus =  1/sqrt(2)
    minus = -1/sqrt(2)
    plus_i = complex(0,1)/sqrt(2)
    minus_i = complex(0,-1)/sqrt(2)
    
    ret_vector = []

    for angle in expected_values:
        basis_arr = [0, 90, 180, 270, 360]
        closest_basis_arr = [abs(x-angle) for x in basis_arr]
        
        closest = basis_arr[closest_basis_arr.index(min(closest_basis_arr))] 
        closest_angle = closest_basis_arr[closest_basis_arr.index(min(closest_basis_arr))]
        #print("closest " + str(closest))
        #print("closest angle " + str(closest_angle))

        basis_arr.pop(closest_basis_arr.index(min(closest_basis_arr)))
        closest_basis_arr.pop(closest_basis_arr.index(min(closest_basis_arr)))

        second_closest = basis_arr[closest_basis_arr.index(min(closest_basis_arr))] 
        second_closest_angle = closest_basis_arr[closest_basis_arr.index(min(closest_basis_arr))]
        #print("second closest " + str(second_closest))
        #print("second closest angle " + str(second_closest_angle))


        if closest == 0:
            if second_closest == 90:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * plus + sin(closest_angle * pi / 180) * plus_i])
            else:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * plus + sin(closest_angle * pi / 180) * minus_i])
        elif closest == 90:
            if second_closest == 180:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * plus_i + sin(closest_angle * pi / 180) * minus])
            else:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * plus_i + sin(closest_angle * pi / 180) * plus])
        elif closest == 180:
            if second_closest == 270:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * minus + sin(closest_angle * pi / 180) * minus_i])
            else:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * minus + sin(closest_angle * pi / 180) * plus_i])
        elif closest == 270:
            if second_closest == 360:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * minus_i + sin(closest_angle * pi / 180) * plus])
            else:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * minus_i + sin(closest_angle * pi / 180) * minus])
        elif closest == 360:
            if second_closest == 90:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * plus + sin(closest_angle * pi / 180) * plus_i])
            else:
                ret_vector.append([1/sqrt(2) , cos(closest_angle * pi / 180) * plus + sin(closest_angle * pi / 180) * minus_i])
    
    #print(ret_vector)
    return ret_vector

if __name__ == "__main__":
    #test_qft_then_inverse()
    test_specific_phase()
    #test_superposition_inputs()



