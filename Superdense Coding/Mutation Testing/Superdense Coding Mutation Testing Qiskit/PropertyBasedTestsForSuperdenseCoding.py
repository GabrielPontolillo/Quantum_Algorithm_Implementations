import unittest

import hypothesis.strategies as st
from hypothesis import given, settings, note

from qiskit import QuantumCircuit
from qiskit import Aer, execute
from qiskit.circuit.library import Barrier, XGate, HGate, CXGate, ZGate, Measure

#####################################################################################
### Change the file to import from, in order to test a mutant version of the code ###
#####################################################################################
### e.g. from Add_mutant_1 import ...
#####################################################################################

from Replace_Mutant_5 import create_bell_pair, encode_message, decode_message

#############################
### Postcondition testing ###
#############################

@st.composite
def draw_message(draw):
    drawnInt = draw(st.integers(min_value=0, max_value=1))
    drawnInt2 = draw(st.integers(min_value=0, max_value=1))
    return(str(drawnInt)+str(drawnInt2))

@given(draw_message())
@settings(deadline=None)
def test_encode_message_returns_only_sets_of_bell_pair_values(message):
    qc = create_bell_pair()
    qc = encode_message(qc, 1, message)
    qc.measure_all()
    note(message)
    backend = Aer.get_backend('aer_simulator') 
    job = execute(qc, backend, shots=1000, memory=True)
    readings = job.result().get_memory()
    note(readings)
    note(not(set(readings) == set(['11','00']) and set(readings) == set(['01','10'])))
    note(set(readings) == set(['11','00']) or set(readings) == set(['01','10']))
    assert(not(set(readings) == set(['11','00']) and set(readings) == set(['01','10'])))
    assert(set(readings) == set(['11','00']) or set(readings) == set(['01','10']))
    
    
@given(draw_message())
def test_decode_message_equal_to_encode_message(message):
    note(message)
    qc = create_bell_pair()
    qc = encode_message(qc, 1, message)
    qc = decode_message(qc)
    qc.measure_all()
    backend = Aer.get_backend('aer_simulator') 
    job = execute(qc, backend, shots=1, memory=True)
    readings = job.result().get_memory()
    note(readings)
    assert(readings == [message])

if __name__ == '__main__':
    test_encode_message_returns_only_sets_of_bell_pair_values()
    test_decode_message_equal_to_encode_message()
