namespace QuantumFourierTransform {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    // Code from Qiskit 
    // https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html
    // Code adapted for Q#

    operation GenerateQFT(qubits: Qubit[], num: Int) : Result[] {
        if (num == 0){
            //tell it to measure the x axis
            set_measure_x(qubits);
            mutable results = [];
            for index in 0 .. Length(qubits) - 1 {
                set results += [M(qubits[index])];
            }
            return results;
        }
        mutable n = num-1;
        H(qubits[n]);
        for index in 0 .. (n - 1) {
           let divisor = PowD(2.0, IntAsDouble(n-index));
           (Controlled R1)([qubits[index]], ((PI()/divisor), qubits[n]));
        }
        return GenerateQFT(qubits,n);
    }

    operation set_measure_x(qubits: Qubit[]): Unit{
        for index in 0 .. Length(qubits)-1 {
            H(qubits[index]);
        }
    }

    operation set_measure_y(qubits: Qubit[]): Unit{
        for index in 0 .. Length(qubits)-1 {
            R1((-PI()/2.0), qubits[index]);
            H(qubits[index]);
        }
    }

    operation runQFTGenerator() : Result[] {
        use qubits = Qubit[4];
        X(qubits[0]);
        return GenerateQFT(qubits, Length(qubits));
    }
}
