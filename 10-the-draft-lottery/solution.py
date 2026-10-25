"""The Draft Lottery (200 pts): reading a spectrum with QPE."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np) and the template's unitary_matrix helper.

def read_spectrum(phases, amplitudes, m):
    n_target = int(np.log2(len(phases)))
    target_wires = list(range(n_target))
    estimation_wires = list(range(n_target, n_target + m))
    dev = qp.device("default.qubit", wires=n_target + m)

    @qp.qnode(dev)
    def circuit():
        qp.StatePrep(np.array(amplitudes), wires=target_wires)
        qp.QuantumPhaseEstimation(
            qp.QubitUnitary(unitary_matrix(phases), wires=target_wires),
            estimation_wires=estimation_wires,
        )
        return qp.probs(wires=estimation_wires)

    probs = circuit()
    eigenphases = []
    weights = []
    for k, p in enumerate(probs):
        p = float(p)
        if p > 1e-9:
            eigenphases.append(k / 2 ** m)
            weights.append(p)

    faintest = min(weights)
    repetitions = int(np.ceil(np.log(0.01) / np.log(1.0 - faintest)))
    return eigenphases, weights, repetitions
