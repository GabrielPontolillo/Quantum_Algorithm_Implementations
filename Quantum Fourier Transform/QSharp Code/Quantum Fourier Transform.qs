namespace QuantumFourierTransform {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    operation GenerateQFT(qubits: Qubit[], num: Int) : Result[] {
        if (num == 0){
            mutable results = new Result[0];
            //tell it to measure the x axis
            measure_x(qubits);
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

    operation measure_x(qubits: Qubit[]): Unit{
        for index in 0 .. Length(qubits)-1 {
            H(qubits[index]);
        }
    }

    operation measure_y(qubits: Qubit[]): Unit{
        for index in 0 .. Length(qubits)-1 {
            R1((-PI()/2.0), qubits[index]);
            H(qubits[index]);
        }
    }

    operation runQFTGenerator() : Result[] {
        let max = 4;
        use qubits = Qubit[max];
        X(qubits[0]);
        return GenerateQFT(qubits, max);
    }
}
