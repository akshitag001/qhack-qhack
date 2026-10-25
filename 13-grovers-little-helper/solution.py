"""Grover's Little Helper (400 pts): one-shot Grover with an auxiliary qubit."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np) and the template's dev device.

@qp.set_shots(1)
@qp.qnode(dev)
def circuit(generator, oracle, diffuser):
    @qp.prod
    def generator_3():
        qp.Hadamard(wires=0)
        qp.Hadamard(wires=1)
        qp.Hadamard(wires=2)

    # Uniform superposition over 8 states
    generator()
    qp.Hadamard(wires=2)

    # Oracle only acts when the auxiliary qubit is |1>
    qp.ctrl(oracle, control=2)()

    # Diffuser over all 3 qubits
    diffuser(generator_3)

    return qp.counts(wires=[0, 1])
