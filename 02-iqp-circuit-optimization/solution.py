"""IQP circuit construction and optimization."""
import pennylane as qp
import pennylane.numpy as np
n_qubits = 4
dev = qp.device('default.qubit', wires=n_qubits)

@qp.qnode(dev)
def iqp_circuit(weights, pattern, observable):
    for i, group in enumerate(pattern):
        for gate in group:
            qp.PauliRot(weights[i], "X" * len(gate), wires=list(gate))
    z_ops = [qp.PauliZ(k) for k, a in enumerate(observable) if a]
    if not z_ops:
        return qp.expval(qp.Identity(0))
    obs = z_ops[0] if len(z_ops) == 1 else qp.prod(*z_ops)
    return qp.expval(obs)

def optimize_iqp(pattern, observable):
    def cost(w):
        return iqp_circuit(w, pattern, observable)
    np.random.seed(0)
    best_weights, best_cost = None, np.inf
    for _ in range(10):
        weights = np.array(np.random.uniform(0, 2 * np.pi, size=len(pattern)), requires_grad=True)
        opt = qp.AdamOptimizer(stepsize=0.1)
        for _ in range(200):
            weights = opt.step(cost, weights)
        c = float(cost(weights))
        if c < best_cost:
            best_cost, best_weights = c, weights
        if best_cost < -0.999:
            break
    return best_weights
