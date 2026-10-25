"""Pauli word measurement from computational-basis probabilities."""
import pennylane as qp
import pennylane.numpy as np

def prepare(angles):
    qp.RY(angles[0], wires=0)
    qp.RX(angles[1], wires=1)
    qp.RY(angles[2], wires=2)
    qp.CNOT(wires=[0, 1])
    qp.RZ(angles[3], wires=1)
    qp.CNOT(wires=[1, 2])
    qp.RX(angles[3], wires=0)

def measure_pauli_word(word, angles):
    letter_to_basis = {"I": "none", "Z": "none", "X": "H", "Y": "SH"}
    basis = [letter_to_basis[letter] for letter in word]
    dev = qp.device("default.qubit", wires=3)

    @qp.qnode(dev)
    def circuit():
        prepare(angles)
        for wire, change in enumerate(basis):
            if change == "H":
                qp.Hadamard(wires=wire)
            elif change == "SH":
                qp.adjoint(qp.S(wires=wire))
                qp.Hadamard(wires=wire)
        return qp.probs(wires=[0, 1, 2])

    probabilities = circuit()
    carried = [w for w, letter in enumerate(word) if letter != "I"]
    signs = [(-1) ** sum((b >> (2 - w)) & 1 for w in carried) for b in range(8)]
    value = float(sum(p * s for p, s in zip(probabilities, signs)))
    return basis, signs, value
