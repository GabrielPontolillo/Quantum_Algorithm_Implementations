namespace QPE_Qsharp {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    operation generalised_qpe_qsharp(amt_estimation_qubits: Int, angle: Double) : Result[] {
        use qubits = Qubit[amt_estimation_qubits+1];
        
        for qubit in 0..amt_estimation_qubits-1 {
            H(qubits[qubit]);
        }

        X(qubits[amt_estimation_qubits]);

        mutable repetitions = 1;
        for counting_qubit in 0..amt_estimation_qubits-1 {
            for i in 0..repetitions-1 {
                (Controlled R1)([qubits[counting_qubit]], ((angle), qubits[amt_estimation_qubits]));
            }
            set repetitions = repetitions*2;
        }

        qft_dagger_qsharp(qubits, amt_estimation_qubits);

        mutable results = new Result[0];
        for index in 0..amt_estimation_qubits-1 {
            set results += [M(qubits[index])];
        }
        ResetAll(qubits);
        return results;
    }

    operation qft_dagger_qsharp(qubits : Qubit[], n: Int) : Unit is Adj + Ctl {
        for qubit in 0..(n/2)-1 {
            SWAP(qubits[qubit],qubits[n-qubit-1]);
        }
        for j in 0..n-1 {
            for m in 0..j-1 {
                let divisor = PowD(2.0, IntAsDouble(j-m));
                (Controlled R1)([qubits[m]], ((-PI()/divisor), qubits[j]));
            }
            H(qubits[j]);
        }
    }

    @EntryPoint()
    operation runQPEGenerator() : Result[] {
        return generalised_qpe_qsharp(5,(PI()*2.0*(1.0/3.0)));
    }
}
