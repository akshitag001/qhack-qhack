# Diffuse and Conquer (400 pts)

Official title: Diffuse and Conquer

### Problem

One backward-Euler step of the 1D diffusion-reaction equation on 4 grid points ($h = 0.2, dt = 0.01$) gives a linear system $A\phi_{\text{new}} = b$, with $A = (1 + k \cdot dt)I - \nu \cdot dt \cdot D_2$ and $b = \phi_{\text{old}} + dt \cdot s$. Write `qsvt_diffusion(nu, k)`, which applies $A^{-1}$ to $b$ approximately with QSVT:
- build $A$
- fit a polynomial to $C/x$
- convert it to angles with `qp.poly_to_angles`
- run QSVT

The grader rescales the output using $C$ and needs fidelity above 0.99.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

QSVT can only apply polynomials to a matrix's singular values, so the inverse is replaced by an odd degree-15 polynomial fitted to $C/x$ on $[0.15, 1]$, with $C = 0.075$. `build_A` divides $A$ by its largest possible eigenvalue $\alpha$ so the singular values fall inside that range. `qp.BlockEncode` embeds the scaled $A$ in a unitary on wires 1–3, and `qp.PCPhase` projectors with the converted angles form the QSVT sequence. 

QSVT naturally produces $P(A) + iQ(A)$, but only the real part $P(A)$ approximates the inverse. So the circuit runs the $+$ angle and $-$ angle versions under a control qubit (wire 0) placed between two Hadamards. Averaging the two branches cancels the imaginary part, which is a linear combination of unitaries.

### Result

Completed on the platform. Re-checked: fidelity against the classical solution is 0.99989 for $\nu = 0.5, k = 1$ and 0.99989 for $\nu = 1, k = 2$, both above the 0.99 threshold.
