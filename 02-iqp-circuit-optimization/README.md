# IQP circuit optimization

Official title: `[To be added]`

### Problem

On 4 qubits, build `iqp_circuit(weights, pattern, observable)` as a QNode without `qp.IQP`. `pattern[i]` is a list of qubit groups that all share the parameter `weights[i]`, and each group S applies exp(−iθ X_S / 2). `observable` is a 0/1 vector selecting which wires get a Pauli Z. Then write `optimize_iqp(pattern, observable)`, which returns weights minimising the expectation value (usually reaching −1).

### Result

The circuit check matches both public cases (0.730681… and 0.936293…), and the optimizer reaches a minimum of about −0.9999999 on both, in under a second each.
