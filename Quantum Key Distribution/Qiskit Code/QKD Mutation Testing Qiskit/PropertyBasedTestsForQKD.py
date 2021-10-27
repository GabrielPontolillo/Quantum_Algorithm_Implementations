import unittest
import numpy as np

import hypothesis.strategies as st
from hypothesis import given, settings
from qiskit.circuit.library import Barrier, HGate, XGate
from qiskit import QuantumCircuit, Aer

#####################################################################################
### Change the file to import from, in order to test a mutant version of the code ###
#####################################################################################
### e.g. from Add_mutant_1 import remove_garbage, generate_binary, encode_message, measure_message
#####################################################################################

from QKD import remove_garbage, generate_binary, encode_message, measure_message

###########################################################################
## Define composite strategies to generate lists of ints in equal length ##
###########################################################################
@st.composite
def single_list(draw):
    arrayLengths = draw(st.integers(min_value=1, max_value=100))
    fixed_length_list = st.lists(st.integers(min_value=0, max_value=1), min_size=arrayLengths, max_size=arrayLengths)
    return (draw(fixed_length_list))

@st.composite
def pair_of_lists(draw):
    arrayLengths = draw(st.integers(min_value=1, max_value=100))
    fixed_length_list = st.lists(st.integers(min_value=0, max_value=1), min_size=arrayLengths, max_size=arrayLengths)
    return (draw(fixed_length_list), draw(fixed_length_list))

@st.composite
def trio_of_lists(draw):
    arrayLengths = draw(st.integers(min_value=1, max_value=100))
    fixed_length_list = st.lists(st.integers(min_value=0, max_value=1), min_size=arrayLengths, max_size=arrayLengths)
    return (draw(fixed_length_list), draw(fixed_length_list), draw(fixed_length_list))

@st.composite
def long_trio_of_lists(draw):
    arrayLengths = draw(st.integers(min_value=100, max_value=110))
    fixed_length_list = st.lists(st.integers(min_value=0, max_value=1), min_size=arrayLengths, max_size=arrayLengths)
    return (draw(fixed_length_list), draw(fixed_length_list), draw(fixed_length_list))

##########################
## test generate binary ##
##########################
@given(testLength = st.integers(min_value=0, max_value=10000))
def test_created_message_is_binary(testLength):
    binArr = generate_binary(testLength)
    for i in binArr:
        assert (i == 1 or i == 0) 

@given(testLength = st.integers(min_value=1, max_value=10000))
def test_created_message_equal_length_to_int_passed_in(testLength):
    binArr = generate_binary(testLength)
    assert(len(binArr) == testLength) 

############################
## encoding message tests ##
############################
@given(pair_of_lists())
@settings(deadline=None)
def test_encode_message_equal_length_to_base(lists):
    alice_bits, alice_bases = lists
    circuitArr = encode_message(alice_bits, alice_bases, len(alice_bits))
    assert(len(circuitArr) ==  len(alice_bits))

@given(pair_of_lists())
@settings(deadline=None)
def test_encode_message_are_circuits(lists):
    alice_bits, alice_bases = lists
    circuitArr = encode_message(alice_bits, alice_bases, len(alice_bits))
    for i in circuitArr:
        assert(isinstance(i, QuantumCircuit))

@given(pair_of_lists())
@settings(deadline=None)
def test_encode_message_circuits_are_not_longer_than_3(lists):
    alice_bits, alice_bases = lists
    circuitArr = encode_message(alice_bits, alice_bases, len(alice_bits))
    for i in circuitArr:
        assert(not(len(i.data) > 3))

@given(pair_of_lists())
@settings(deadline=None)
def test_encode_message_circuits_use_only_H_X_Barrier(lists):
    alice_bits, alice_bases = lists
    circuitArr = encode_message(alice_bits, alice_bases, len(alice_bits))
    for i in circuitArr:
        for gate in i:
            assert(isinstance(gate[0], Barrier) 
                   or isinstance(gate[0], XGate)
                   or isinstance(gate[0], HGate)) 

############################
## decoding message tests ##
############################
@given(lists = trio_of_lists())
@settings(deadline=None)
def test_decode_message_length_equals_base_length(lists):
    alice_bits, alice_bases, bob_base = lists
    encoded_message = encode_message(alice_bits, alice_bases, len(bob_base))
    msmtArr = measure_message(encoded_message, bob_base, len(bob_base))
    assert len(msmtArr) == len(bob_base)

@given(lists = trio_of_lists())
@settings(deadline=None)
def test_decode_message_is_binary(lists):
    alice_bits, alice_bases, bob_base = lists
    encoded_message = encode_message(alice_bits, alice_bases, len(bob_base))
    msmtArr = measure_message(encoded_message, bob_base, len(bob_base))
    for i in msmtArr:
        assert (i == 1 or i == 0) 
        
@given(lists = pair_of_lists())
@settings(deadline=None)
def test_decode_with_same_base_returns_original_bits(lists):
    alice_bits, alice_bases = lists
    encoded_message = encode_message(alice_bits, alice_bases, len(alice_bits))
    decodeWithSameBases = measure_message(encoded_message, alice_bases, len(alice_bases))
    assert(np.array_equal(np.array(alice_bits), np.array(decodeWithSameBases)))        
        
@given(lists = pair_of_lists())
@settings(deadline=None)
def test_decode_with_same_bases_return_same_array(lists):
    alice_bits, alice_bases = lists
    encoded_message = encode_message(alice_bits, alice_bases, len(alice_bits))
    encoded_message2 = encode_message(alice_bits, alice_bases, len(alice_bits))
    decodeWithSameBases = measure_message(encoded_message, alice_bases, len(alice_bases))
    decodeWithSameBases2 = measure_message(encoded_message2, alice_bases, len(alice_bases))
    assert(np.array_equal(np.array(decodeWithSameBases), np.array(decodeWithSameBases2)))
    
    
@given(lists = long_trio_of_lists())
@settings(deadline=None)
def test_decoding_runs_likely_different(lists):
    alice_bits, alice_bases, bob_bases = lists
    encoded_message = encode_message(alice_bits, alice_bases, len(bob_bases))
    msmtArr = measure_message(encoded_message, alice_bases, len(alice_bases))
    msmtArrRun2 = measure_message(encoded_message, bob_bases, len(bob_bases))
    assert(not np.array_equal(np.array(msmtArr), np.array(msmtArrRun2)))

##############################
## remove garbage/key tests ##
##############################
@given(lists = trio_of_lists())
@settings(deadline=None)
def test_key_smaller_or_equal_len_to_original_bits(lists):
    alice_bits, alice_bases, bob_base = lists
    assert len(remove_garbage(alice_bits, alice_bases, bob_base, len(bob_base))) <= len(bob_base)

@given(lists = trio_of_lists())
@settings(deadline=None)
def test_check_keys_equal(lists):
    alice_bits, alice_bases, bob_bases = lists
    message = encode_message(alice_bits, alice_bases, len(bob_bases))
    bob_results = measure_message(message, bob_bases, len(bob_bases))
    alice_key = remove_garbage(alice_bases, bob_bases, alice_bits, len(bob_bases))
    bob_key = remove_garbage(alice_bases, bob_bases, bob_results, len(bob_bases)) 
    assert(np.array_equal(np.array(alice_key), np.array(bob_key)))

@given(lists = trio_of_lists())
@settings(deadline=None)
def test_key_is_binary(lists):
    alice_bits, alice_bases, bob_bases = lists
    alice_key = remove_garbage(alice_bases, bob_bases, alice_bits, len(bob_bases))
    for i in alice_key:
        assert (i == 1 or i == 0) 

if __name__ == "__main__":
    test_created_message_is_binary()
    test_created_message_equal_length_to_int_passed_in()
    test_encode_message_equal_length_to_base()
    test_encode_message_are_circuits()
    test_encode_message_circuits_are_not_longer_than_3()
    test_encode_message_circuits_use_only_H_X_Barrier()
    test_decode_message_length_equals_base_length()
    test_decode_message_is_binary()
    test_decode_with_same_base_returns_original_bits()
    test_decode_with_same_bases_return_same_array()
    ###########
    #test_decoding_runs_likely_different()
    ###########
    test_key_smaller_or_equal_len_to_original_bits()
    test_check_keys_equal()
    test_key_is_binary()