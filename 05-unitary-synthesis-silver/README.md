# Unitary synthesis, Silver

Official title: `[To be added]`

### Problem

Same as Bronze, with a 20% saving needed at 5 qubits. That means at most 1,036 rotations, against a theoretical minimum of 1,023 for any rotation-based exact circuit.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

The Bronze method wastes one multiplexor per recursion level on demultiplexing, so this version drops demultiplexing entirely. It keeps applying the cosine-sine split to the multiplexed blocks themselves, all the way down to single-qubit gates on the last wire, each controlled by every other qubit (the Möttönen et al. 2004 structure). 

The circuit then consists only of fully controlled RZ and RY multiplexors. Each leaf is written as $R_z R_y R_z$ times a phase; only the $R_z$ and $R_y$ nearest in time are built, and the rest becomes a diagonal over all $n$ qubits that is carried forward. Before each cosine-sine step on wire $k$, that diagonal is split into two parts:
- **The part that doesn't involve wire $k$:** It commutes past the RY multiplexor and merges into the next leaf for free.
- **An RZ multiplexor on wire $k$:** This is the only piece that costs rotations.

At the end, one last diagonal is built with a short chain of multiplexors, and the scalar phase goes into a `GlobalPhase` gate. Nothing in the circuit is redundant: it uses exactly $4^n - 1$ rotations, the number of real parameters in a unitary after the free global phase.

### Result

| Qubits | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Rotations | 15 | 63 | 255 | 1,023 |
| Cost | 660 | 2,772 | 11,220 | 45,012 |
| Baseline | 660 | 3,168 | 13,728 | 57,024 |
| Saving | 0.0% | 12.5% | 18.2% | 21.0% |

The platform's own run on seeds 7 and 2026 gave the same costs, with max errors of 1.5e-14 and 8.8e-15. Silver passes (21.0% saving), and the same code passes the Bronze version too.
