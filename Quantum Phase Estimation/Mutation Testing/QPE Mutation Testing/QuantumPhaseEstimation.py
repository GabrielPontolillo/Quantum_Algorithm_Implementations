import warnings
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram, plot_bloch_multivector

warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np

pi = np.pi


def qft_dagger(qc, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-pi/float(2**(j-m)), m, j)
        qc.h(j)

def generalised_qpe(amt_estimation_qubits, angle, shots=10000):
    go = True
    while go:
        # Create and set up circuit
        qpe3 = QuantumCircuit(amt_estimation_qubits+1, amt_estimation_qubits)

        # Apply H-Gates to counting qubits:
        for qubit in range(amt_estimation_qubits):
            qpe3.h(qubit)

        # Prepare our eigenstate |psi>:
        qpe3.x(amt_estimation_qubits)

        repetitions = 1
        for counting_qubit in range(amt_estimation_qubits):
            for i in range(repetitions):
                qpe3.cp(angle, counting_qubit, amt_estimation_qubits);
            repetitions *= 2

        # Do the inverse QFT:
        qft_dagger(qpe3, amt_estimation_qubits)

        # Measure of course!
        qpe3.barrier()
        for n in range(amt_estimation_qubits):
            qpe3.measure(n,n)

        aer_sim = Aer.get_backend('aer_simulator')
        t_qpe3 = transpile(qpe3, aer_sim)
        qobj = assemble(t_qpe3, shots=shots)
        results = aer_sim.run(qobj).result()
        answer = results.get_counts()
        
        answer2 = {int(k,2)/2**amt_estimation_qubits: v for k, v in answer.items()}
        print(answer2)
    
        try:
            freq = answer.most_frequent()
            go = False
        except:
            pass
        

    #print("Most frequent '" + answer.most_frequent() + "'")
    print("Approx rotation angle by Z from the unitary in degrees '" + str(360 * int(answer.most_frequent(), 2)/2**amt_estimation_qubits) + "'")
    #print("Phase Calculation " + answer.most_frequent())

    ##return(plot_histogram(answer))
    ##comment out the return if you want to see the histogram
    return((int(answer.most_frequent(), 2)/2**amt_estimation_qubits))
