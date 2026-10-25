# Goal or No Goal? (100 pts)

Official title: Goal or No Goal?

### Problem

Prepare the $n$-qubit GHZ state $(|00\dots0\rangle + |11\dots1\rangle)/\sqrt{2}$ and return the $n$ observables that certify it: the global X parity $X_0 X_1 \dots X_{n-1}$ plus the $n-1$ neighbouring parities $Z_i Z_{i+1}$. The grader inspects the observables themselves, so there can be no substitutes, repeats or identity operators. The average of the $n$ expectation values is +1 only for the GHZ state.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

A Hadamard on wire 0 followed by CNOTs from wire 0 to every other wire builds the GHZ state. The checks come in two kinds because each kind alone can be fooled. The ZZ parities confirm that neighbouring qubits always agree, but a classical coin flip between $00\dots0$ and $11\dots1$ passes them too. The X parity only gives +1 when the two branches are in a coherent superposition, but the product state $|+\rangle^{\otimes n}$ also passes it. Only the GHZ state passes both, so returning the X parity first and then the $n-1$ ZZ parities, built with `qp.prod`, gives the grader exactly the set it expects.

### Result

Completed on the platform. Re-checked: the averaged score is exactly 1.0 for $n = 2, 3$ and $5$, with $n$ checks each time.
