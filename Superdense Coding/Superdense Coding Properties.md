# Superdense Coding 
### A valid bell state has been induced

- Precondition:

A quantum circuit with a bell pair: *qc*

A two bit binary message to encode: *M*  
- Operation:

MeasureZ( encodeMessage( *qc, M* ) ) : Res[n]

> This measurement should be performed with many shots, as to have a high probability of catching an error in bell pairs

- Output:

AssertTrue( toSet( Res[0],…,Res[10000] ) = {00,11} OR toSet(Res[0],…,Res[10000]) = {01,10} )

> toSet is a method that converts the results list, into a set containing unique values

---

### The encoding and decoding a message should return the original message 
 
 - Precondition:

A quantum circuit with a bell pair: *qc*

A two bit binary message to encode: *M*  

- Operation:

encodeMessage( *qc, M* )

- Output:

assertEqual( decodeMessage( *qc* ), *M* )