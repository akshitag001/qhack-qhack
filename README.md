# PennyLane Coding Challenges: Questions, Solutions and Notes

A structured collection of PennyLane quantum coding challenge solutions, explanatory notes, and benchmarks.

## Repository Layout

```
qhack-qhack/
├── README.md                                  # Index & overview of all challenges
├── 01-pauli-word-measurement/
│   ├── README.md                              # Problem breakdown, theory & results
│   └── solution.py                            # Tested PennyLane solution
├── 02-iqp-circuit-optimization/
│   ├── README.md
│   └── solution.py
├── 03-nmr-time-evolution/
│   ├── README.md
│   └── solution.py
├── 04-unitary-synthesis-bronze/
│   ├── README.md
│   └── solution.py
├── 05-unitary-synthesis-silver/
│   ├── README.md
│   └── solution.py
├── 06-unitary-synthesis-gold/
│   ├── README.md
│   └── notes.md                               # Analysis of Gold attempt routes
├── 07-goal-or-no-goal/
│   ├── README.md
│   └── solution.py
├── 08-playing-period/
│   ├── README.md
│   └── solution.py
├── 09-fermionic-vqe/
│   ├── README.md
│   └── solution.py
├── 10-the-draft-lottery/
│   ├── README.md
│   └── solution.py
├── 11-the-hidden-subgroup-stage/
│   ├── README.md
│   └── solution.py
├── 12-diffuse-and-conquer/
│   ├── README.md
│   └── solution.py
└── 13-grovers-little-helper/
    ├── README.md
    └── solution.py
```

---

## Challenges Index

| # | Challenge | Points / Topic | Result | Solution | Notes |
|---|---|---|---|---|---|
| 1 | [Pauli word measurement from probabilities](./01-pauli-word-measurement/) | Expectation value using only `qp.probs` | Both public tests pass | [solution.py](./01-pauli-word-measurement/solution.py) | [Notes](./01-pauli-word-measurement/README.md) |
| 2 | [IQP circuit optimization](./02-iqp-circuit-optimization/) | Minimise a Z-observable with Adam | Both public tests pass, min ≈ −1 | [solution.py](./02-iqp-circuit-optimization/solution.py) | [Notes](./02-iqp-circuit-optimization/README.md) |
| 3 | [NMR time evolution](./03-nmr-time-evolution/) | Evolve \|0⟩ under time-dependent NMR Hamiltonian | Both public tests pass | [solution.py](./03-nmr-time-evolution/solution.py) | [Notes](./03-nmr-time-evolution/README.md) |
| 4 | [Unitary synthesis, Bronze](./04-unitary-synthesis-bronze/) | Beat Shannon decomposition by 5% | 9.7% saving | [solution.py](./04-unitary-synthesis-bronze/solution.py) | [Notes](./04-unitary-synthesis-bronze/README.md) |
| 5 | [Unitary synthesis, Silver](./05-unitary-synthesis-silver/) | Beat Shannon decomposition by 20% | 21.0% saving | [solution.py](./05-unitary-synthesis-silver/solution.py) | [Notes](./05-unitary-synthesis-silver/README.md) |
| 6 | [Unitary synthesis, Gold](./06-unitary-synthesis-gold/) | Beat Shannon decomposition by 60% | Not reached; Silver code is best honest result | [notes.md](./06-unitary-synthesis-gold/notes.md) | [Notes](./06-unitary-synthesis-gold/README.md) |
| 7 | [Goal or No Goal?](./07-goal-or-no-goal/) | 100 pts • GHZ state certifying checks | Completed; score 1.0 re-checked | [solution.py](./07-goal-or-no-goal/solution.py) | [Notes](./07-goal-or-no-goal/README.md) |
| 8 | [Playing Period](./08-playing-period/) | 100 pts • 4-qubit QFT from H, C-Phase & SWAP | Completed; matches `qp.QFT` | [solution.py](./08-playing-period/solution.py) | [Notes](./08-playing-period/README.md) |
| 9 | [Fermionic VQE](./09-fermionic-vqe/) | 200 pts • Jordan–Wigner Hamiltonian & VQE | Completed; exact energies re-checked | [solution.py](./09-fermionic-vqe/solution.py) | [Notes](./09-fermionic-vqe/README.md) |
| 10 | [The Draft Lottery](./10-the-draft-lottery/) | 200 pts • Read spectrum with phase estimation | Completed; re-checked on test case | [solution.py](./10-the-draft-lottery/solution.py) | [Notes](./10-the-draft-lottery/README.md) |
| 11 | [The Hidden Subgroup Stage](./11-the-hidden-subgroup-stage/) | 200 pts • Symmetry score for labelled bit strings | Completed; worked example gives 0.9 | [solution.py](./11-the-hidden-subgroup-stage/solution.py) | [Notes](./11-the-hidden-subgroup-stage/README.md) |
| 12 | [Diffuse and Conquer](./12-diffuse-and-conquer/) | 400 pts • 1D diffusion-reaction step with QSVT | Completed; fidelity 0.9999 re-checked | [solution.py](./12-diffuse-and-conquer/solution.py) | [Notes](./12-diffuse-and-conquer/README.md) |
| 13 | [Grover's Little Helper](./13-grovers-little-helper/) | 400 pts • Grover with half states marked, 1 shot | Completed; 100% success rate | [solution.py](./13-grovers-little-helper/solution.py) | [Notes](./13-grovers-little-helper/README.md) |

---

## Challenge Summaries

### 1. [Pauli word measurement from probabilities](./01-pauli-word-measurement/)
- **Official title:** `[To be added]`
- **Problem:** Measure expectation value of a 3-qubit Pauli word (`word` from `I`, `X`, `Y`, `Z`) given a fixed state preparation, returning only `qp.probs(wires=[0, 1, 2])`.
- **Result:** Both public tests match (`"ZIZ"` gives 0.931986…, `"XYI"` gives 0.967399…).
- **Links:** 📄 [Solution Code](./01-pauli-word-measurement/solution.py) • 📖 [Explanatory Notes](./01-pauli-word-measurement/README.md)

### 2. [IQP circuit optimization](./02-iqp-circuit-optimization/)
- **Official title:** `[To be added]`
- **Problem:** Build a 4-qubit IQP circuit without `qp.IQP` and optimize parameter weights with Adam to minimize a Pauli-Z observable expectation value.
- **Result:** Both public cases match (0.730681… and 0.936293…); optimizer reaches ≈ −0.9999999.
- **Links:** 📄 [Solution Code](./02-iqp-circuit-optimization/solution.py) • 📖 [Explanatory Notes](./02-iqp-circuit-optimization/README.md)

### 3. [NMR time evolution](./03-nmr-time-evolution/)
- **Official title:** `[To be added]`
- **Problem:** Evolve a single qubit starting in \|0⟩ under the time-dependent NMR Hamiltonian $H(t) = B_0 Z + B_1 (\cos(\omega t) X - \sin(\omega t) Y)$ using `qp.evolve`.
- **Result:** Both public cases match to ~1e-6 (within 3e-2 tolerance): [0.69620…, 0.30379…] and [0.72782…, 0.27217…].
- **Links:** 📄 [Solution Code](./03-nmr-time-evolution/solution.py) • 📖 [Explanatory Notes](./03-nmr-time-evolution/README.md)

### 4. [Unitary synthesis, Bronze](./04-unitary-synthesis-bronze/)
- **Official title:** `[To be added]`
- **Problem:** Synthesize a Haar-random unitary on 2–5 qubits within 1e-8 entrywise error, beating the Shannon decomposition baseline cost by 5% at 5 qubits.
- **Result:** 9.7% saving at 5 qubits (Cost: 51,480 vs baseline 57,024). Max error ~1e-14 with 0 extra wires.
- **Links:** 📄 [Solution Code](./04-unitary-synthesis-bronze/solution.py) • 📖 [Explanatory Notes](./04-unitary-synthesis-bronze/README.md)

### 5. [Unitary synthesis, Silver](./05-unitary-synthesis-silver/)
- **Official title:** `[To be added]`
- **Problem:** Synthesize a Haar-random unitary on 2–5 qubits beating the Shannon decomposition baseline by 20% at 5 qubits (at most 1,036 rotations).
- **Result:** 21.0% saving at 5 qubits (Rotations: 1,023; Cost: 45,012 vs baseline 57,024). Max errors 1.5e-14 and 8.8e-15.
- **Links:** 📄 [Solution Code](./05-unitary-synthesis-silver/solution.py) • 📖 [Explanatory Notes](./05-unitary-synthesis-silver/README.md)

### 6. [Unitary synthesis, Gold](./06-unitary-synthesis-gold/)
- **Official title:** `[To be added]`
- **Problem:** Synthesize a Haar-random unitary on 2–5 qubits beating the Shannon decomposition baseline by 60% (cost 22,809 or less at 5 qubits).
- **Result:** Not reached. 21.0% (Silver code) is the best honest score; analysis proves rotation-based exact circuits cannot breach the 1,023 parameter floor.
- **Links:** 📄 [Analysis & Notes](./06-unitary-synthesis-gold/notes.md) • 📖 [Overview](./06-unitary-synthesis-gold/README.md)

### 7. [Goal or No Goal? (100 pts)](./07-goal-or-no-goal/)
- **Official title:** Goal or No Goal?
- **Problem:** Prepare the $n$-qubit GHZ state and return the $n$ certifying observables: global X parity $X_0 \dots X_{n-1}$ plus $n-1$ neighbouring parities $Z_i Z_{i+1}$.
- **Result:** Completed; averaged score is exactly 1.0 for $n = 2, 3, 5$.
- **Links:** 📄 [Solution Code](./07-goal-or-no-goal/solution.py) • 📖 [Explanatory Notes](./07-goal-or-no-goal/README.md)

### 8. [Playing Period (100 pts)](./08-playing-period/)
- **Official title:** Playing Period
- **Problem:** Build the 4-qubit Quantum Fourier Transform on wires 0–3 using only `qp.Hadamard`, `qp.ControlledPhaseShift` and `qp.SWAP`.
- **Result:** Completed; circuit matches `qp.QFT` with max difference 1.7e-16.
- **Links:** 📄 [Solution Code](./08-playing-period/solution.py) • 📖 [Explanatory Notes](./08-playing-period/README.md)

### 9. [Fermionic VQE (200 pts)](./09-fermionic-vqe/)
- **Official title:** Fermionic VQE
- **Problem:** Map a 6-mode fermionic Hamiltonian to qubits with Jordan–Wigner and optimize ground-state energy with a variational ansatz.
- **Result:** Completed; matches exact ground energy for [1, 2, 3] (energy 0) and [−1, 0.5, −2] (energy −3).
- **Links:** 📄 [Solution Code](./09-fermionic-vqe/solution.py) • 📖 [Explanatory Notes](./09-fermionic-vqe/README.md)

### 10. [The Draft Lottery (200 pts)](./10-the-draft-lottery/)
- **Official title:** The Draft Lottery
- **Problem:** Run Quantum Phase Estimation on a diagonal unitary with superposition input; extract eigenphases, weights, and required repetitions.
- **Result:** Completed; matches test spectrum and required confidence repetitions.
- **Links:** 📄 [Solution Code](./10-the-draft-lottery/solution.py) • 📖 [Explanatory Notes](./10-the-draft-lottery/README.md)

### 11. [The Hidden Subgroup Stage (200 pts)](./11-the-hidden-subgroup-stage/)
- **Official title:** The Hidden Subgroup Stage
- **Problem:** Given binary strings with class labels and candidate symmetry $s$, compute the closed-form symmetry score $S(s)$.
- **Result:** Completed; worked example gives 0.9.
- **Links:** 📄 [Solution Code](./11-the-hidden-subgroup-stage/solution.py) • 📖 [Explanatory Notes](./11-the-hidden-subgroup-stage/README.md)

### 12. [Diffuse and Conquer (400 pts)](./12-diffuse-and-conquer/)
- **Official title:** Diffuse and Conquer
- **Problem:** Solve a 1D diffusion-reaction backward-Euler step by applying polynomial matrix inversion with Quantum Singular Value Transformation (QSVT) and LCU.
- **Result:** Completed; fidelity against classical solution is 0.99989 (threshold 0.99).
- **Links:** 📄 [Solution Code](./12-diffuse-and-conquer/solution.py) • 📖 [Explanatory Notes](./12-diffuse-and-conquer/README.md)

### 13. [Grover's Little Helper (400 pts)](./13-grovers-little-helper/)
- **Official title:** Grover's Little Helper
- **Problem:** Single-shot Grover search on 2 qubits with 2 marked states using 1 auxiliary qubit to adjust marked subspace ratio to $1/4$.
- **Result:** Completed; single shot guaranteed to locate marked state.
- **Links:** 📄 [Solution Code](./13-grovers-little-helper/solution.py) • 📖 [Explanatory Notes](./13-grovers-little-helper/README.md)
