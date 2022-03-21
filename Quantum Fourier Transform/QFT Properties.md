# Quantum Fourier Transform
### Performing QFT on qubits, then inverse of QFT, should result in the original qubits to be returned

 - Precondition:
 
Vector of qubits, *x<sub>0</sub> … x<sub>n-1</sub>*
- Operation:

InverseQFT(QFT(*x<sub>0</sub> … x<sub>n-1</sub>*))
- Output:

assertEqual((*x<sub>0</sub>…x<sub>n-1</sub>*), (*x'<sub>0</sub>…x'<sub>n-1</sub>*)

---

### A specific phase will be induced in each qubit after QFT is applied

 - Precondition:
 
Vector of qubits, *x<sub>0</sub> … x<sub>n-1</sub>*

s.t. &emsp; *∀ i:*

*&emsp;&emsp;&emsp;0 <= i < n:*

*&emsp;&emsp;&emsp;x<sub>i</sub> = |0> or x<sub>i</sub> = |1>*

Where the binary total of *x<sub>0</sub> … x<sub>n-1</sub>* : T   

- Operation:

QFT( *x<sub>0</sub> … x<sub>n-1</sub>* )
- Output:

assertPhase( ( *x<sub>0</sub> … x<sub>n-1</sub>* ), ( ( *πT/2<sup>0</sup>* )<sup>c</sup>, ..., ( *πT/2<sup>n-1</sup>* )<sup>c</sup> ) )

---
### A multiple of a phase will be induced in each qubit after QFT is applied

 - Precondition:
 
Vector of qubits, *x<sub>0</sub> … x<sub>n-1</sub>*

s.t.&emsp; *∀ i:*

*&emsp;&emsp;&emsp;0 <= i < n:*

*&emsp;&emsp;&emsp;x<sub>i</sub> = |0> or x<sub>i</sub> = |1>*

- Operation:

QFT( *x<sub>0</sub> … x<sub>n-1</sub>* )
- Output:

assertTrue( estimatePhase( *x<sub>0</sub>* ) MOD  ( *πT/2<sup>0</sup>* )<sup>c</sup> ≈ 0 )

.

.

.

assertTrue( estimatePhase( *x<sub>0</sub>* ) MOD  ( *πT/2<sup>n-1</sup>* )<sup>c</sup> ≈ 0 )

---

### When QFT is applied to two sets of qubits of same length, the LSB qubit on the set of qubits with the higher binary total will  have a greater phase

 - Precondition:
 
 Two vectors of qubits, *x<sub>0</sub> … x<sub>n-1</sub>, &emsp; y<sub>0</sub> … y<sub>n-1</sub>*

s.t.&emsp; *∀ i:*

*&emsp;&emsp;&emsp;0 <= i < n:*

*&emsp;&emsp;&emsp;x<sub>i</sub> = |0> or x<sub>i</sub> = |1>,*

*&emsp;&emsp;&emsp;y<sub>i</sub> = |0> or y<sub>i</sub> = |1>*

Where the binary total of *x<sub>0</sub> … x<sub>n-1</sub>, > y<sub>0</sub> … y<sub>n-1</sub>*  
- Operation:

QFT( *x<sub>0</sub> … x<sub>n-1</sub>* )

QFT( *y<sub>0</sub> … y<sub>n-1</sub>* )
- Output:

assertTrue( estimatePhase( *x<sub>n-1</sub>* ) > estimatePhase( *y<sub>n-1</sub>*  ) )

---

### When QFT is applied to two sets of qubits in the |1> state of different length, the LSB qubit on the set of qubits with the higher binary total will  have a greater phase.

 - Precondition:
 
 Two vectors of qubits, *x<sub>0</sub> … x<sub>n-1</sub>, &emsp; y<sub>0</sub> … y<sub>n-1</sub>*

s.t.&emsp; *∀ i:* 

*&emsp;&emsp;&emsp;0 <= i < n:*

*&emsp;&emsp;&emsp;x<sub>i</sub> = |1>, &emsp;y<sub>i</sub> = |1>*

- Operation:

QFT( *x<sub>0</sub> … x<sub>n-1</sub>* )

QFT( *y<sub>0</sub> … y<sub>n-1</sub>* )
- Output:

assertTrue( estimatePhase( *x<sub>n-1</sub>* ) > estimatePhase( *y<sub>n-1</sub>*  ) )
