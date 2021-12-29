import hypothesis.strategies as st
from hypothesis import given, settings, note
from qiskit.circuit.library import CCXGate, CXGate, CSwapGate, HGate, SwapGate, CPhaseGate

#####################################################################################
### Change the file to import from, in order to test a mutant version of the code ###
#####################################################################################
### e.g. from Add_mutant_1 import ...
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

#########################
### Running the tests ###
#########################
if __name__ == '__main__':
    test_modular_exponentiation_non_coprime_int_throws_exception()
    test_qpe_amod_15_phase_between_0_and_1()
    test_qpe_amod_15_non_coprime_int_throws_exception()
    test_find_factor_is_3_or_5()
    test_find_factor_non_coprime_int_throws_exception()