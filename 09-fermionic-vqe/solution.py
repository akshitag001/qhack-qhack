"""Fermionic VQE (200 pts): Jordan-Wigner Hamiltonian and VQE."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np).

w0 = qp.FermiWord({(0, 0): "-", (1, 0): "+"})
w1 = qp.FermiWord({(0, 1): "-", (1, 1): "+"})
w2 = qp.FermiWord({(0, 2): "-", (1, 2): "+"})


def build_hamiltonian(coeffs):
    fermi_h = coeffs[0] * w0 + coeffs[1] * w1 + coeffs[2] * w2
    qubit_h = qp.jordan_wigner(fermi_h)
    h_coeffs, h_ops = qubit_h.terms()
    real_coeffs = [float(np.real(c)) for c in h_coeffs]
    return qp.Hamiltonian(real_coeffs, h_ops)


dev = qp.device("default.qubit", wires=6)


@qp.qnode(dev)
def vqe_circuit(params, coeffs):
    for i in range(6):
        qp.RY(params[i], wires=i)
    return qp.expval(build_hamiltonian(coeffs))


def optimization(coeffs):
    opt = qp.AdamOptimizer(stepsize=0.1)
    params = np.random.uniform(0, 2 * np.pi, size=6, requires_grad=True)
    for _ in range(300):
        params = opt.step(lambda p: vqe_circuit(p, coeffs), params)
    return vqe_circuit(params, coeffs)
