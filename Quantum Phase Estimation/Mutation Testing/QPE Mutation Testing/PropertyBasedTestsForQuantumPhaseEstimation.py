import unittest
import numpy as np

import hypothesis.strategies as st
from hypothesis import given, settings
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import QFT
from math import pi, degrees

# importing sys
import sys

from sympy import false
  
# adding Folder_2 to the system path
import pathlib

sys.path.insert(0, str(pathlib.Path().resolve())+f"/Property_Assertion")

from QuantumAssertions import assertPhase

#####################################################################################
### Change the file to import from, in order to test a mutant version of the code ###
#####################################################################################
### e.g. from Add_mutant_1 import remove_garbage, generate_binary, encode_message, measure_message
#####################################################################################

from QuantumPhaseEstimation import generalised_qpe

###########################################################################
## Define composite strategies to generate lists of ints in equal length ##
###########################################################################

@st.composite
def draw_a_small_and_bigger_number_theta(draw):
    small = draw(st.integers(min_value=1, max_value=5))
    big = draw(st.integers(min_value=small+1, max_value=7))
    theta = draw(st.floats(min_value=0, max_value=1, exclude_max=True))
    return(small,big, theta)

@st.composite
def draw_a_qubit_size_and_theta(draw):
    size = draw(st.integers(min_value=2, max_value=7))
    theta = draw(st.floats(min_value=0, max_value=1, exclude_max=True))
    return(size, theta)

##########################
## test generate binary ##
##########################
@given(draw_a_small_and_bigger_number_theta())
@settings(deadline=None)
def more_qubits_better_estimation(vals):
    small = vals[0]
    big = vals[1]
    theta = vals[2]

    smallEst = generalised_qpe(small, theta*2*pi, shots=10000)    
    bigEst = generalised_qpe(big, theta*2*pi, shots=10000)    

    print("---")
    print(smallEst)
    print(bigEst)
    print(theta)
    print(abs(smallEst - theta))
    print(abs(bigEst - theta))


    assert(abs(smallEst - theta) <= abs(smallEst - theta))

@given(draw_a_qubit_size_and_theta())
@settings(deadline=None)
def accurate_to_2_minus_n_radians(vals):
    size = vals[0]
    theta = vals[1]

    est = generalised_qpe(size, theta*2*pi, shots=10000)        
    if est == 0:
        if abs(1 - theta) < abs(0 - theta):
            est = 1

    print("---")
    print(f"size {size}")
    print(f"est {est}")
    print(f"theta {theta}")
    print(f"abs(est - theta) {abs(est - theta)}")
    print(2**-size)


    assert(abs(est - theta) <= 2**-size)

if __name__ == "__main__":
    more_qubits_better_estimation()
    accurate_to_2_minus_n_radians()