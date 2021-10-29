import unittest

import cirq
from cirq.ops import H, X, I
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

import hypothesis.strategies as st
from hypothesis import given, settings

def generate_binary(len):
    return randint(2, size=len)

def encode_message(bits, bases, messageLen):
    message = []
    for i in range(messageLen):
        qubits = cirq.LineQubit.range(1)
        qc = cirq.Circuit()
        if bases[i] == 0: # Prepare qubit in Z-basis
            if bits[i] == 0:
                qc.append(cirq.I(qubits[0]))
            else:
                qc.append(cirq.X(qubits[0]))
        else: # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.append(cirq.H(qubits[0]))
            else:
                qc.append(cirq.X(qubits[0]))
                ### mutant - remove ###
        message.append(qc)
    return message

def measure_message(message, bases, messageLen):
    measurements = []
    for q in range(messageLen):
        if bases[q] == 0: # measuring in Z-basis
            if (not message[q].has_measurements()):
                for qubit in message[q].all_qubits():
                    message[q].append(cirq.measure(qubit))
        if bases[q] == 1: # measuring in X-basis
            if (not message[q].has_measurements()):
                for qubit in message[q].all_qubits():
                    message[q].append(cirq.H(qubit))
                    message[q].append(cirq.measure(qubit))
        simulator = cirq.Simulator()
        measured_bit = simulator.run(message[q])
        measurements.append((measured_bit.data.iat[0,0]))   
    return measurements

def remove_garbage(a_bases, b_bases, bits, messageLen):
    good_bits = []
    for q in range(messageLen):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits

def sample_bits(bits, selection):
    sample = []
    for i in selection:
        # use np.mod to make sure the
        # bit we sample is always in 
        # the list range
        i = np.mod(i, len(bits))
        # pop(i) removes the element of the
        # list at index 'i'
        sample.append(bits.pop(i))
    return sample