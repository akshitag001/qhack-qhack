# NMR time evolution

Official title: `[To be added]`

### Problem

Evolve a single qubit starting in |0⟩ under the NMR Hamiltonian

H(t) = B0·Z + B1·(cos(ωt)·X − sin(ωt)·Y)

for a time `time`, using `qp.evolve`, and return the computational-basis probabilities. The inputs are `B0`, `B1`, `omega` and `time`. The tolerance is 3e-2.

### Result

Both public cases match to about 1e-6, well inside the 3e-2 tolerance: [0.69620…, 0.30379…] and [0.72782…, 0.27217…].
