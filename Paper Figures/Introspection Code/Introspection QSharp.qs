namespace QPE_Qsharp {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    @EntryPoint()
    operation runIntrospection() :  Unit{
        use qubits = Qubit[3];
        H(qubits[0]);
        (Controlled X)([qubits[0]],qubits[1]);
        H(qubits[2]);
        S(qubits[2]);
        DumpMachine();
        ResetAll(qubits);
    }
}
