# Playing Period (100 pts)

Official title: Playing Period

### Problem

Build the 4-qubit Quantum Fourier Transform on wires 0–3 using only `qp.Hadamard`, `qp.ControlledPhaseShift` and `qp.SWAP` (`qp.QFT` is not allowed). The grader compares the circuit's unitary with `qp.QFT`.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

This is the textbook QFT circuit. For each wire $i$, a Hadamard comes first, then controlled phase shifts from every later wire $j$, with angle $\pi/2^{j-i}$: $\pi/2$ for the next wire, $\pi/4$ for the one after, and so on. That circuit leaves the output bits in reverse order, so two SWAPs at the end (wires 0↔3 and 1↔2) put them back in the order PennyLane's `qp.QFT` uses.

### Result

Completed on the platform. Re-checked: the circuit matches `qp.QFT` with a maximum difference of 1.7e-16.
