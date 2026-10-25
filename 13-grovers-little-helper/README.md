# Grover's Little Helper (400 pts)

Official title: Grover's Little Helper

### Problem

On 2 qubits with exactly 2 of the 4 states marked, plain Grover search stalls: one iteration leaves the success probability at 50%. Using one auxiliary qubit, apply the oracle and diffuser once each and guarantee a marked state in a single shot. `circuit(generator, oracle, diffuser)` returns `qp.counts` on wires 0 and 1. The grader tries 1,000 random oracles.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

The fix is to change the fraction of marked states. The circuit puts an extra qubit (wire 2) into superposition alongside the normal 2-qubit generator, giving 8 basis states. It applies the oracle only when wire 2 is $|1\rangle$, so only 2 of the 8 states pick up the minus sign. With a marked fraction of $1/4$, a single Grover iteration rotates the state exactly onto the marked subspace ($\sin^2(3\theta) = 1$ when $\sin^2\theta = 1/4$). The diffuser then reflects about the full 3-qubit uniform state built by `generator_3`. One shot on wires 0 and 1 always returns a marked state, and the auxiliary qubit is ignored.

### Result

Completed on the platform.
