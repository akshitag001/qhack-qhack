# Unitary synthesis, Bronze

Official title: `[To be added]`

### Problem

Write `submission_circ(u_mat)`, which queues gates implementing a Haar-random unitary on 2, 3, 4 or 5 qubits. It must match to 1e-8 entrywise, global phase included. The circuit is decomposed into RX, RY, RZ, T, S, H, X, Y, Z, CNOT and GlobalPhase, and charged with specific gate costs. The target is the Shannon decomposition, which costs 44·(21/16·4ⁿ − 3·2ⁿ⁻¹), or 57,024 at 5 qubits. The saving at 5 qubits must reach the Bronze threshold (5%), and the saving must never shrink from one size to the next.

### Result

| Qubits | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Cost | 660 | 2,904 | 12,408 | 51,480 |
| Baseline | 660 | 3,168 | 13,728 | 57,024 |
| Saving | 0.0% | 8.3% | 9.6% | 9.7% |

The max error is about 1e-14, with no extra wires. Bronze passes with a 9.7% saving.
