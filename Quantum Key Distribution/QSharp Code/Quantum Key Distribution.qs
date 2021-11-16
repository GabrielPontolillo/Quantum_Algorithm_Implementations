namespace Quantum_key_distribution {

    open Microsoft.Quantum.Random;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic; 
    open Microsoft.Quantum.Arrays as Array; 

    operation generateBinary(len: Int): Int[] {
        mutable binArray = new Int[0];
        for index in 0 .. (len - 1) {
            set binArray += [DrawRandomInt(0, 1)];
        }
        return binArray;
    }

    operation encodeMessage(bits: Int[], bases: Int[], messageLen: Int, qubits: Qubit[]): Unit {
        for i in 0 .. (messageLen - 1) {
            if (bases[i] == 0) { 
                if (bits[i] == 0) { 
                } else {
                    X(qubits[i]);
                }
            } else {
                if bits[i] == 0 {
                    H(qubits[i]);
                } else {
                    X(qubits[i]);
                    H(qubits[i]);
                }
            }
        }
    }

    operation measureMessage(message: Qubit[], bases: Int[], messageLen: Int): Int[] {
        mutable measurements = new Int[0];
        for q in 0 .. (messageLen - 1) {
            if (bases[q] == 0) { 
                if (M(message[q]) == One) {
                    set measurements += [1]; 
                } else {
                    set measurements += [0];
                }
            }
            if (bases[q] == 1) { 
                H(message[q]);
                if (M(message[q]) == One) {
                    set measurements += [1]; 
                } else {
                    set measurements += [0];
                }
            }
        }
        ResetAll(message);
        return measurements;
    }

    operation removeGarbage(a_bases: Int[], b_bases: Int[], bits: Int[], messageLen: Int): Int[] {
        mutable good_bits = new Int[0];
        for q in 0 .. (messageLen - 1)  {
            if (a_bases[q] == b_bases[q]) {
                set good_bits += [bits[q]];
            }
        }
        return good_bits;
    }

    operation sampleBits(bits: Int[], selection: Int[]): Int[] {
        mutable bitsArr = bits;
        mutable sample = new Int[0];
        for i in selection {
           //Message(IntAsString(i));
           //Message(IntAsString(Length(bitsArr)));
           mutable popVal = ModI(i, Length(bitsArr));
           set sample += [bitsArr[popVal]];
           set bitsArr = Array.Exclude([popVal], bitsArr);
        }
        return sample;
    }

    operation IntArrayAsString(intArray: Int[]): String {
        mutable buildString = "";
        for i in intArray {
            set buildString += IntAsString(i); 
        }
        return buildString;
    }
    

    operation runQKD() : Unit {
        let messageLen = 25;
        use qubits = Qubit[messageLen];
        // Step 1
        // Alice generates bits
        let alice_bits = generateBinary(messageLen);

        // Step 2
        // Create an array to tell us which qubits
        // are encoded in which bases
        let alice_bases = generateBinary(messageLen);
        encodeMessage(alice_bits, alice_bases, messageLen, qubits);

        // Step 3
        // Decide which basis to measure in:
        let bob_bases = generateBinary(messageLen);
        let bob_results = measureMessage(qubits, bob_bases, messageLen);

        // Step 4
        let alice_key = removeGarbage(alice_bases, bob_bases, alice_bits, messageLen);
        let bob_key = removeGarbage(alice_bases, bob_bases, bob_results, messageLen);

        // Step 5
        let sample_size = 10;
        let bit_selection = generateBinary(sample_size);

        let bob_sample = sampleBits(bob_key, bit_selection);
        let alice_sample = sampleBits(alice_key, bit_selection);
        Message("bob_sample = " + IntArrayAsString(bob_sample));
        Message("alice_sample = "+ IntArrayAsString(alice_sample));
    }
}
