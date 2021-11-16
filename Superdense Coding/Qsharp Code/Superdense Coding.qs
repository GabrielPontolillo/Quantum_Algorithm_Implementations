namespace Superdense_Coding {

    open Microsoft.Quantum.Random;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    operation createBellPair(qubits: Qubit[]): Unit { 
        H(qubits[1]);
        (Controlled X)([qubits[1]],qubits[0]);        
    }
    
    operation encodeMessage(qubit: Qubit, message: Int[]): Unit { 
        for num in 0..1 {
            Message(IntAsString(message[num]));
            if (message[num] != 0 and message[num] != 1 ){
                fail("invalid message, it must be made up of 1 and 0 (int)");
            }     
        }
        if (message[1] == 1){
            X(qubit);
        }
        if (message[0] == 1){
            Z(qubit);
        }        
    }

    operation decodeMessage(qubits: Qubit[]): Unit { 
        (Controlled X)([qubits[1]],qubits[0]);  
        H(qubits[1]);        
    }

    operation runSuperdense() : Result[] {
        use qubits = Qubit[2]; 

        createBellPair(qubits); 

        let message = [1,1]; 

        encodeMessage(qubits[1], message);

        decodeMessage(qubits);

        mutable results = new Result[0];
        for index in 0..1 {
            set results += [M(qubits[index])];
        }
        ResetAll(qubits);

        return(results);
    }
}
