# IQP circuit optimization

Official title: `[To be added]`

### Problem

On 4 qubits, build `iqp_circuit(weights, pattern, observable)` as a QNode without `qp.IQP`. `pattern[i]` is a list of qubit groups that all share the parameter `weights[i]`, and each group S applies exp(−iθ X_S / 2). `observable` is a 0/1 vector selecting which wires get a Pauli Z. Then write `optimize_iqp(pattern, observable)`, which returns weights minimising the expectation value (usually reaching −1).

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

Each IQP term $\exp(-i\theta X_S / 2)$ is exactly `qp.PauliRot(θ, "XX…X", wires=S)`, so the circuit is a double loop over the pattern. Every generator is built only from X's, so all the gates commute and their order doesn't matter. The observable is a product of `PauliZ` on the wires marked 1, with a guard for an all-zero vector. 

For the optimizer, $\theta = 0$ is a trap: the state stays $|0000\rangle$, every Z-product equals $+1$, and the gradient is zero. So each run starts from random angles and does 200 Adam steps with step size 0.1. It keeps the best of up to 10 restarts and stops early once the cost is within $10^{-3}$ of $-1$. A fixed seed keeps the output reproducible.

### Result

The circuit check matches both public cases (0.730681… and 0.936293…), and the optimizer reaches a minimum of about −0.9999999 on both, in under a second each.
