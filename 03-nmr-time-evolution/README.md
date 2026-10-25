# NMR time evolution

Official title: `[To be added]`

### Problem

Evolve a single qubit starting in $|0\rangle$ under the NMR Hamiltonian

$$H(t) = B_0 Z + B_1 (\cos(\omega t) X - \sin(\omega t) Y)$$

for a time `time`, using `qp.evolve`, and return the computational-basis probabilities. The inputs are `B0`, `B1`, `omega` and `time`. The tolerance is 3e-2.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

The Hamiltonian has one constant term and two terms whose coefficients change with time, which is what PennyLane's `ParametrizedHamiltonian` is for. Passing `qp.dot` a mix of plain numbers and callables `f(p, t)` builds one. `B0` stays a fixed coefficient on Z, and `f_x`, `f_y` give $B_1 \cos(\omega t)$ and $-B_1 \sin(\omega t)$. 

`qp.evolve(H)(params, t=time)` needs one parameter entry per callable, in order, so both entries are `[B1, omega]`. A single float for `t` means "evolve from 0 to `time`", and PennyLane solves the time-ordered Schrödinger equation numerically with JAX. As a sanity check for the first case: over a short time $H \approx Z + 2X$, which predicts $P(1) \approx 0.31$, close to the expected 0.304.

### Result

Both public cases match to about 1e-6, well inside the 3e-2 tolerance: [0.69620…, 0.30379…] and [0.72782…, 0.27217…].
