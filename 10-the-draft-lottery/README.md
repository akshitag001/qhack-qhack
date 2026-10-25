# The Draft Lottery (200 pts)

Official title: The Draft Lottery

### Problem

Run quantum phase estimation on a diagonal unitary (`unitary_matrix(phases)`, eigenvalue $e^{2\pi i \cdot \text{phases}[k]}$ on $|k\rangle$) with a superposition as input, using $m$ estimation wires. Return three things:
- the distinct eigenphases present, in ascending order (bins with probability > 1e-9)
- their weights, in matching order
- the number of repetitions $r$ needed to see the faintest phase with 99% confidence, from $(1 - w)^r \le 0.01$

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

Phase estimation is linear, so a superposition input runs every eigenvector branch at once. Measuring only the estimation register then gives phase $k/2^m$ with probability equal to its weight in the input. The code loads the amplitudes with `qp.StatePrep`, runs `qp.QuantumPhaseEstimation` with the unitary wrapped in `qp.QubitUnitary`, and reads `qp.probs` on the estimation wires. Every bin above 1e-9 becomes an eigenphase with its weight. Phases that share a bin merge automatically, because their probabilities land in the same bin. The repetition count is $\lceil \ln(0.01)/\ln(1 - w) \rceil$ for the smallest weight.

### Result

Completed on the platform. Re-checked: phases [0.25, 0.5, 0.25, 0.75] with uniform amplitudes and $m = 3$ give eigenphases [0.25, 0.5, 0.75], weights [0.5, 0.25, 0.25] (the two 0.25 phases merge) and 17 repetitions.
