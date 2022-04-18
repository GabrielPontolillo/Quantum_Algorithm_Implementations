import warnings
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute, Aer, transpile
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from Quantum_Algorithm_Implementations.Property_Assertion import QuantumAssertions
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np

pi = np.pi

def flip_endian(dict):
    newdict = {}
    for key in list(dict):
        newdict[key[::-1]] = dict.pop(key)
    return newdict

def set_measure_x(circuit, n):
    for num in range(n):
        circuit.h(num)

def set_measure_y(circuit, n):
    for num in range(n):
        circuit.sdg(num)
        circuit.h(num)

def qft_rotations(circuit, n):
    #if qubit amount is 0, then do nothing and return
    if n == 0:
        #set it to measure the x axis
        set_measure_x(qc, 4)
        qc.measure_all()
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n)
    return qft_rotations(circuit, n)

backend = Aer.get_backend('aer_simulator') 
qc = QuantumCircuit(4)

qc.x(0)

qft_rotations(qc,4)#call the recursive qft method
#set it to measure the x axis
set_measure_x(qc, 4)

job = execute(qc, backend, shots=100000)#run the circuit 1000000 times
print(flip_endian(job.result().get_counts()))#return the result counts