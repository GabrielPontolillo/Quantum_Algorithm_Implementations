# Quantum Key Distribution
### Measuring the encoded message circuit in the Z basis should return a message of the same length as the encoded message

- Precondition:

Random binary string to encode: M

Random binary string for bases: B

Length( M ) = Length( B )

- Operation:

encodeMessage( M, B ): encodedCircuit

- Output:

assertEqual( Length( measureZ( encodedCircuit ) ), Length( M ) )

---

### The encodedCircuit needs to be the same length as the output of measureMessage

- Precondition:

Random binary string to encode: M

Random binary string for bases: BAlice

Random binary string for bases: BBob

Length( M ) = Length( BAlice )

Length( M ) = Length( BBob )

- Operation:

encodeMessage( M, BAlice ): encodedCircuit

measureMessage( encodedCircuit, BBob ):

- Output:

assertEqual( Length( measureMessage( encodedCircuit, BBob ) ), Length( encodedCircuit ) )

---

### The measured array should be a binary array
 
- Precondition:

Random binary string to encode: M

Random binary string for bases: BAlice

Random binary string for bases: BBob

Length( M ) = Length( BAlice )

Length( M ) = Length( BBob )

- Operation:

encodeMessage( M, BAlice ): encodedCircuit

measureMessage( encodedCircuit, BBob ): measuredArray

- Output:

assertTrue( isBinaryArray( measuredArray ) )

---

### If an array is measured in the same basis it was encoded with, it should output the same - originally encoded message

- Precondition:

Random binary string to encode: M

Random binary string for bases: BAlice

Length( M ) = Length( BAlice )

- Operation:

encodeMessage( M, BAlice ): encodedCircuit

measureMessage( encodedCircuit, BAlice ): measuredArray

- Output:

assertEqual( measuredArray, M )

---

### The same message encoded with different basis should output different circuits (hence output different things when measured in Z/X basis)

- Precondition:

Random binary string to encode: M

Random binary string for bases: BAlice

Random binary string for bases: BBob

Length( M ) >= 100

Length( M ) = Length( BAlice )

Length( M ) = Length( BBob )

BAlice != BBob

- Operation:

encodeMessage( M, BAlice ): encodedCircuitAlice

encodeMessage( M, BBob ): encodedCircuitBob

- Output:

assertTrue( measureZ( encodedCircuitAlice ) != measureZ( encodedCircuitBob ) )

assertTrue( measureX( encodedCircuitAlice ) != measureX( encodedCircuitBob ) )

---

### Removing parts where different basis was used to measured should result in equally decoded keys, samples taken from the keys should also be equal

Precondition:

Random binary string to encode: M

Random binary string for bases: BAlice

Random binary string for bases: BBob

Length( M ) = Length( BAlice )

Length( M ) = Length( BBob )

BAlice != BBob

Operation:

encodeMessage( M, BAlice ): encodedCircuitAlice

measureMessage( encodedCircuitAlice, BBob ): measuredMessageBob

removeGarbage( BAlice, BBob, M ): AliceKey

removeGarbage( BAlice, BBob, measuredMessageBob ): BobKey

Generate sample length for verification: S

S < Length( AliceKey )

Generate random binary string of length S: binS

sampleBits( BobKey, binS ): bobSample

sampleBits( AliceKey, binS ) aliceSample

Output:

assertEqual( AliceKey, BobKey )

assertEqual( bobSample, AliceSample )

---
### Measuring with the wrong basis will not output the original message

- Precondition:

Random binary string to encode: M

Random binary string for bases: BAlice

Random binary string for bases: BBob

Length( M ) >= 100

Length( M ) = Length( BAlice )

Length( M ) = Length( BBob )

BAlice != BBob

- Operation:

encodeMessage( M, BAlice ): encodedCircuitAlice

- Output:

assertTrue( measureMessage( encodedCircuitAlice, BBob) != M )

---

### The same message encoded with different basis, and measured with the correct basis, should return the original/same message for both

- Precondition: 

Random binary string to encode: M

Random binary string for bases: BAlice

Random binary string for bases: BBob

Length( M ) = Length( BAlice )

Length( M ) = Length( BBob )

BAlice != BBob

- Operation:

encodeMessage( M, BAlice ): encodedCircuitAlice

encodeMessage( M, BBob ): encodedCircuitBob
 
Output:

assertTrue( measureMessage( encodedCircuitAlice, BAlice) != measureMessage ( encodedCircuitBob, BBob ) )

assertEqual( measureMessage( encodedCircuitAlice, BAlice ), M )