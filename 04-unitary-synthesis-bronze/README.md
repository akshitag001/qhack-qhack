# Unitary synthesis, Bronze

Official title: `[To be added]`

### Problem (shared by Bronze, Silver, and Gold)

Write `submission_circ(u_mat)`, which queues gates implementing a Haar-random unitary on 2, 3, 4 or 5 qubits. It must match to 1e-8 entrywise, global phase included. The circuit is decomposed into RX, RY, RZ, T, S, H, X, Y, Z, CNOT and GlobalPhase, and charged as follows:
- RX, RY and RZ cost 44 each (the T-count of one arbitrary rotation).
- T costs 1.
- Everything else costs 0.
- Every extra wire doubles the total, with at most 8 wires in all.

The target is the Shannon decomposition, which costs $44 \cdot (21/16 \cdot 4^n - 3 \cdot 2^{n-1})$, or 57,024 at 5 qubits. The saving at 5 qubits must reach the Bronze threshold (5%), and the saving must never shrink from one size to the next.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

This follows the Shannon decomposition itself: split on the top qubit with a cosine-sine decomposition, and "demultiplex" each block-diagonal half into two smaller unitaries plus an RZ multiplexor. Then recurse until only 2-qubit blocks remain. 

A general 2-qubit block costs 15 rotations, and the saving comes from not building each block in full. Every block except the last is implemented only up to a diagonal phase, which takes 13 rotations, and the leftover diagonal is handed to the next block. That works because every multiplexor in between uses the bottom two qubits as controls, so the diagonal commutes through it and merges into the next block's matrix for free. The last block absorbs everything with PennyLane's built-in 2-qubit decomposition (15 rotations). Multiplexed rotations are built recursively from CNOTs, so a multiplexor with $k$ controls costs $2^k$ rotations.

### Result

| Qubits | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Cost | 660 | 2,904 | 12,408 | 51,480 |
| Baseline | 660 | 3,168 | 13,728 | 57,024 |
| Saving | 0.0% | 8.3% | 9.6% | 9.7% |

The max error is about 1e-14, with no extra wires. Bronze passes with a 9.7% saving.
