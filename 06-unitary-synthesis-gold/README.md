# Unitary synthesis, Gold

Official title: `[To be added]`

### Problem

Same as sections 4 and 5, with a 60% saving needed: a cost of 22,809 or less at 5 qubits, about 518 rotations' worth.

### Detailed Notes & Analysis
Full analysis: [`notes.md`](notes.md)

### What we did

Every rotation carries one real number, and a random 5-qubit unitary needs 1,023 of them (with the global phase free), so any exact circuit built from rotations needs at least 1,023 rotations. That costs 45,012, roughly double the Gold limit, and the Silver code already sits exactly on that floor. A circuit made of Clifford+T sequences isn't bound by that count, and on paper it could approximate a 5-qubit unitary with a few thousand T gates. But no known algorithm finds such sequences fast enough to run in seconds per sample. Every route we tested failed:

| Route | Estimated cost at 5 qubits | Why it fails |
|---|---|---|
| Merge or remove rotations in the Silver circuit | 45,012 | Zero mergeable pairs; already at the floor |
| Replace each rotation with a Clifford+T sequence | ~92,000 | Each rotation needs about 90 T gates for 1e-9 |
| Repeat-until-success circuits (arXiv:1404.5320) | ~90,000 | Needs measurement (rejected by grader) and extra qubit (×2) |
| QROM / phase-gradient synthesis | — | Needs ~170 extra qubits, against cap of 3 |
| Flag decomposition (Xanadu) | 45,012 at best | Parameter-optimal, so reaches same floor as Silver |

### Result

Not passed. 21.0% is the best honest score we found, and the Silver code is the submission to keep.
