"""Playing Period (100 pts): 4-qubit QFT from elementary gates."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np).

def qft_four_qubits():
    n = 4
    for i in range(n):
        qp.Hadamard(wires=i)
        for j in range(i + 1, n):
            qp.ControlledPhaseShift(np.pi / 2 ** (j - i), wires=[j, i])

    # Reverse qubit order to match PennyLane's QFT
    for i in range(n // 2):
        qp.SWAP(wires=[i, n - 1 - i])
