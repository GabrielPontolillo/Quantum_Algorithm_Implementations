import hypothesis.strategies as st
from hypothesis import given, settings, note
from qiskit.circuit.library import CCXGate, CXGate, CSwapGate, HGate, SwapGate, CPhaseGate

#####################################################################################
### Change the file to import from, in order to test a mutant version of the code ###
#####################################################################################
### e.g. from Add_mutant_1 import remove_garbage, generate_binary, encode_message, measure_message
#####################################################################################

from Remove_Mutant_1 import c_amod15, qft_dagger, qpe_amod15, find_factor

#############################
### Postcondition Testing ###
#############################

@st.composite
def draw_coprime_int(draw):
    return draw(st.sampled_from([2,7,8,11,13]))

@st.composite
def draw_non_coprime_int(draw):
    return draw(st.sampled_from([1,3,4,5,6,9,10,12,14,15]))

@given(draw_coprime_int(), st.integers(min_value=0, max_value=7))
@settings(deadline=None)
def test_modular_exponentiation_uses_CSWap_CCX_CX_gates(coprime_int, power):
    note("coprime integer %i and power %i"%(coprime_int, power))
    circuit = (c_amod15(coprime_int, power).definition)
    note(circuit)
    for gate in circuit:
            note(type(gate[0]))
            assert(isinstance(gate[0], CSwapGate) 
                    or isinstance(gate[0], CCXGate)
                    or isinstance(gate[0], CXGate))

@given(draw_non_coprime_int(), st.integers(min_value=0, max_value=7))
@settings(deadline=None)
def test_modular_exponentiation_non_coprime_int_throws_exception(non_coprime_int, power):
    note("non coprime integer %i and power %i"%(non_coprime_int, power))
    # we expect an assertion to be thrown if a non coprime int is supplied
    # ussing assertRaises() is challenging in jupyter notebook so we just use a try block
    try:
        c_amod15(non_coprime_int, power)
    except ValueError:
        assert(True)
    else:
        assert(False)
        
@given(st.integers(min_value=1, max_value=25))
@settings(deadline=None)
def test_qft_dagger_uses_H_Swap_CPhase_gates(qft_dagger_length):
    note("qft dagger circuit length %i"%(qft_dagger_length))
    circuit = qft_dagger(qft_dagger_length)
    note(circuit)
    for gate in circuit:
            note(type(gate[0]))
            assert(isinstance(gate[0], HGate) 
                    or isinstance(gate[0], SwapGate)
                    or isinstance(gate[0], CPhaseGate))
            
@given(draw_coprime_int())
@settings(deadline=None)
def test_qpe_amod_15_phase_between_0_and_1(coprime_integer):
    note("coprime integer %i"%coprime_integer)
    phase = qpe_amod15(coprime_integer)
    note("phase %i"%phase)
    assert(phase >= 0 and phase <= 1)
    
    
@given(draw_non_coprime_int())
@settings(deadline=None)
def test_qpe_amod_15_non_coprime_int_throws_exception(non_coprime_int):
    note("non coprime integer %i"%(non_coprime_int))
    # we expect an assertion to be thrown if a non coprime int is supplied
    # ussing assertRaises() is challenging in jupyter notebook so we just use a try block
    try:
        qpe_amod15(non_coprime_int)
    except ValueError:
        assert(True)
    else:
        assert(False)
        
@given(draw_coprime_int())
@settings(deadline=None)
def test_find_factor_is_3_or_5(coprime_integer):
    note("coprime integer %i"%coprime_integer)
    guesses = find_factor(coprime_integer)
    note(guesses)
    assert(len(guesses)>0)
    for guess in guesses:
        note("guess %i"%guess)
        assert guess in [3,5]
        
@given(draw_non_coprime_int())
@settings(deadline=None)
def test_find_factor_non_coprime_int_throws_exception(non_coprime_int):
    note("non coprime integer %i"%(non_coprime_int))
    # we expect an assertion to be thrown if a non coprime int is supplied
    # ussing assertRaises() is challenging in jupyter notebook so we just use a try block
    try:
        find_factor(non_coprime_int)
    except ValueError:
        assert(True)
    else:
        assert(False)

######################################
### Metamorphic Properties Testing ###
######################################

@st.composite
def draw_pair_of_ints(draw):
    drawnInt = draw(st.integers(min_value=0, max_value=6))
    randIncrease = 7 - drawnInt 
    drawnLarger = draw(st.integers(min_value=drawnInt+1, max_value=drawnInt+randIncrease))
    return(drawnInt, drawnLarger)

@st.composite
def draw_larger_pair_of_ints(draw):
    drawnInt = draw(st.integers(min_value=1, max_value=24))
    randIncrease = 25 - drawnInt 
    drawnLarger = draw(st.integers(min_value=drawnInt+1, max_value=drawnInt+randIncrease))
    return(drawnInt, drawnLarger)

@given(draw_coprime_int(), draw_pair_of_ints())
@settings(deadline=None)
def test_modular_exponentiation_circuit_longer_with_larger_power(coprime_int, powers):
    smaller, larger = powers
    note("coprime integer %i and powers %i, %i"%(coprime_int, smaller, larger))
    circuit = (c_amod15(coprime_int, smaller).definition)
    circuitLarger =  (c_amod15(coprime_int, larger).definition)
    note("smaller circuit length = %i, larger circuit length = %i"%(len(circuit.data), len(circuitLarger.data)))
    assert(len(circuit.data) < len(circuitLarger.data))
    
@given(draw_coprime_int(), st.integers(min_value=0, max_value=7))
@settings(deadline=None)
def test_modular_exponentiation_circuit_same_length_with_equal_power(coprime_int, power):
    note("coprime integer %i and power %i"%(coprime_int, power))
    circuit = (c_amod15(coprime_int, power).definition)
    circuitEqual =  (c_amod15(coprime_int, power).definition)
    note("circuit 1 length = %i, circuit 2 length = %i"%(len(circuit.data), len(circuitEqual.data)))
    assert(len(circuit.data) == len(circuitEqual.data))
    
@given(draw_larger_pair_of_ints())
@settings(deadline=None)
def test_qft_dagger_circuit_is_longer_with_higher_length_parameter(qft_lengths):
    length1, length2 = qft_lengths
    note("smaller length %i and larger length %i"%(length1, length2))
    circuit = qft_dagger(length1)
    circuitLarger =  qft_dagger(length2)
    note("smaller circuit length = %i, larger circuit length = %i"%(len(circuit.data), len(circuitLarger.data)))
    assert(len(circuit.data) < len(circuitLarger.data))
    
@given(st.integers(min_value=1, max_value=25))
@settings(deadline=None)
def test_qft_dagger_circuit_same_length_with_length_parameter(qft_length):
    note("length %i"%(qft_length))
    circuit = qft_dagger(qft_length)
    circuitEqual =  qft_dagger(qft_length)
    note("circuit 1 length = %i, circuit 2 length = %i"%(len(circuit.data), len(circuitEqual.data)))
    assert(len(circuit.data) == len(circuitEqual.data))


#########################
### Running the tests ###
#########################
if __name__ == '__main__':
    test_modular_exponentiation_uses_CSWap_CCX_CX_gates()
    test_modular_exponentiation_non_coprime_int_throws_exception()
    test_qft_dagger_uses_H_Swap_CPhase_gates()
    test_qpe_amod_15_phase_between_0_and_1()
    test_qpe_amod_15_non_coprime_int_throws_exception()
    test_find_factor_is_3_or_5()
    test_find_factor_non_coprime_int_throws_exception()
    test_modular_exponentiation_circuit_longer_with_larger_power()
    test_modular_exponentiation_circuit_same_length_with_equal_power()
    test_qft_dagger_circuit_is_longer_with_higher_length_parameter()
    test_qft_dagger_circuit_same_length_with_length_parameter()