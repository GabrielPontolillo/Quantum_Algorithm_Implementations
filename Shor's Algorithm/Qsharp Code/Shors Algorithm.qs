namespace Shors_Algorithm {

    open Microsoft.Quantum.Random;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Logical;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    operation c_amod15(a: Int, power: Int, qubits: Qubit[]): Unit is Ctl{
        mutable checkArr = [2, 7, 8, 11, 13];
        mutable isIn = false;
        for i in 0 .. Length(checkArr) - 1 {
            if (a == checkArr[i]) {
                set isIn = true;
            }
        }
        if (not isIn){
            fail "a must be 2,7,8,11 or 13";
        }
        for iteration in 0 .. power-1 {
            if (a == 2 or a == 13){
                SWAP(qubits[0],qubits[1]);
                SWAP(qubits[1],qubits[2]);
                SWAP(qubits[2],qubits[3]);
            }
            if (a == 7 or a == 8){
                SWAP(qubits[2],qubits[3]);
                SWAP(qubits[1],qubits[2]);
                SWAP(qubits[0],qubits[1]);
            }
            if (a == 11){
                SWAP(qubits[1],qubits[3]);
                SWAP(qubits[0],qubits[2]);
            }
            if (a == 7 or a == 11 or a == 13){
                X(qubits[0]);
                X(qubits[1]);
                X(qubits[2]);
                X(qubits[3]);
            }
        } 
    }

    operation qft_dagger(qubits : Qubit[], n: Int) : Unit is Adj + Ctl {
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

    operation qpe_amod15(a: Int): Result[] {
        let n_count = 8;
        use qubits = Qubit[n_count + 4];
        for q in 0 .. n_count-1 {
            H(qubits[q]);
        }
        X(qubits[3+n_count]);
        for q in 0 .. n_count-1 {
            (Controlled c_amod15)([qubits[q]], (a, PowI(2,q), [qubits[n_count],qubits[n_count+1],qubits[n_count+2],qubits[n_count+3]]));
        }
        qft_dagger(qubits[0..n_count-1], n_count);
        mutable results = new Result[0];
        for index in 0..n_count-1 {
            set results += [M(qubits[index])];
        }
        ResetAll(qubits);
        return results;
    }

    operation runShors(a: Int) : Result[] {
        return(Array.Reversed<Result>(qpe_amod15(a)));
    }
}
