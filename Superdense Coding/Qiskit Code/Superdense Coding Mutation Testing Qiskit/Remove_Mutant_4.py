from qiskit import QuantumCircuit

def create_bell_pair():
    qc = QuantumCircuit(2)
    qc.h(1)
    qc.cx(1, 0)
    return qc

def encode_message(qc, qubit, msg):
    if len(msg) != 2 or not set([0,1]).issubset({0,1}):
        raise ValueError(f"message '{msg}' is invalid")
    if msg[1] == "1":
        qc.x(qubit)
    if msg[0] == "1":
        ### removed z gate ###
        pass
    return qc

def decode_message(qc):
    ### removed cx gate ###
    qc.h(1)
    return qc