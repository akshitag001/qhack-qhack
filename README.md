# PennyLane coding challenges: questions, solutions and notes

Six challenge submissions, in the order I worked on them. Each section has a short version of the problem, the code that goes into the template, a paragraph on what the code does and why, and the result.

The titles below describe each problem. The official names on the challenge platform may differ, so each section has an `Official title` line to fill in.

Repo layout that fits this file, one folder per challenge:

```
qhack-qhack/
├── README.md
├── 01-pauli-word-measurement/solution.py
├── 02-iqp-circuit-optimization/solution.py
├── 03-nmr-time-evolution/solution.py
├── 04-unitary-synthesis-bronze/solution.py
├── 05-unitary-synthesis-silver/solution.py
└── 06-unitary-synthesis-gold/notes.md
```

| # | Challenge | What it asks for | Result |
|---|---|---|---|
| 1 | Pauli word measurement from probabilities | Expectation value of a 3-qubit Pauli word using only `qp.probs` | Both public tests pass |
| 2 | IQP circuit optimization | Build an IQP circuit and minimise a Z-observable | Both public tests pass, minimum ≈ −1 |
| 3 | NMR time evolution | Evolve \|0⟩ under a time-dependent NMR Hamiltonian | Both public tests pass |
| 4 | Unitary synthesis, Bronze | Beat the Shannon decomposition by 5% | 9.7% saving |
| 5 | Unitary synthesis, Silver | Beat it by 20% | 21.0% saving |
| 6 | Unitary synthesis, Gold | Beat it by 60% | Not reached; Silver code is the best honest result |

---

## 1. Pauli word measurement from probabilities

Official title: `[To be added]`

### Problem

A fixed `prepare(angles)` function builds a 3-qubit state. Write `measure_pauli_word(word, angles)`, where `word` is three letters from `I`, `X`, `Y`, `Z`. You may only return `qp.probs(wires=[0, 1, 2])` from the circuit; `qp.expval` and `qp.state` are blocked. Return three things:

- `basis`: the basis change per wire (`"none"`, `"H"` or `"SH"`).
- `signs`: the ±1 parity of each of the 8 outcomes, with wire 0 as the most significant bit.
- `value`: the expectation value, the sum of probability × sign.

### Solution

```python
def measure_pauli_word(word, angles):
    letter_to_basis = {"I": "none", "Z": "none", "X": "H", "Y": "SH"}
    basis = [letter_to_basis[letter] for letter in word]
    dev = qp.device("default.qubit", wires=3)

    @qp.qnode(dev)
    def circuit():
        prepare(angles)
        for wire, change in enumerate(basis):
            if change == "H":
                qp.Hadamard(wires=wire)
            elif change == "SH":
                qp.adjoint(qp.S(wires=wire))
                qp.Hadamard(wires=wire)
        return qp.probs(wires=[0, 1, 2])

    probabilities = circuit()
    carried = [w for w, letter in enumerate(word) if letter != "I"]
    signs = [(-1) ** sum((b >> (2 - w)) & 1 for w in carried) for b in range(8)]
    value = float(sum(p * s for p, s in zip(probabilities, signs)))
    return basis, signs, value
```

### What we did

A quantum computer only measures in the Z basis, so measuring X or Y means rotating that axis onto Z first. A Hadamard does it for X because HXH = Z, and S† followed by H does it for Y. After those basis changes the word is a product of Z's, and each shot's value is a parity: +1 if an even number of the participating bits are 1, −1 if odd. Two decisions are kept apart on purpose. The gate applied to a wire depends on its letter (I and Z both get none), but the parity depends only on whether the letter is I. Z wires need no gate and still count toward the sign, and that's where people usually go wrong. The expectation value is then the probability-weighted sum of the signs.

### Result

Both public tests match: `"ZIZ"` gives 0.931986…, and `"XYI"` gives 0.967399…, with the exact basis and sign lists the grader expects.

---

## 2. IQP circuit optimization

Official title: `[To be added]`

### Problem

On 4 qubits, build `iqp_circuit(weights, pattern, observable)` as a QNode without `qp.IQP`. `pattern[i]` is a list of qubit groups that all share the parameter `weights[i]`, and each group S applies exp(−iθ X_S / 2). `observable` is a 0/1 vector selecting which wires get a Pauli Z. Then write `optimize_iqp(pattern, observable)`, which returns weights minimising the expectation value (usually reaching −1).

### Solution

```python
n_qubits = 4
dev = qp.device('default.qubit', wires=n_qubits)

@qp.qnode(dev)
def iqp_circuit(weights, pattern, observable):
    for i, group in enumerate(pattern):
        for gate in group:
            qp.PauliRot(weights[i], "X" * len(gate), wires=list(gate))
    z_ops = [qp.PauliZ(k) for k, a in enumerate(observable) if a]
    if not z_ops:
        return qp.expval(qp.Identity(0))
    obs = z_ops[0] if len(z_ops) == 1 else qp.prod(*z_ops)
    return qp.expval(obs)

def optimize_iqp(pattern, observable):
    def cost(w):
        return iqp_circuit(w, pattern, observable)
    np.random.seed(0)
    best_weights, best_cost = None, np.inf
    for _ in range(10):
        weights = np.array(np.random.uniform(0, 2 * np.pi, size=len(pattern)), requires_grad=True)
        opt = qp.AdamOptimizer(stepsize=0.1)
        for _ in range(200):
            weights = opt.step(cost, weights)
        c = float(cost(weights))
        if c < best_cost:
            best_cost, best_weights = c, weights
        if best_cost < -0.999:
            break
    return best_weights
```

### What we did

Each IQP term exp(−iθ X_S / 2) is exactly `qp.PauliRot(θ, "XX…X", wires=S)`, so the circuit is a double loop over the pattern. Every generator is built only from X's, so all the gates commute and their order doesn't matter. The observable is a product of `PauliZ` on the wires marked 1, with a guard for an all-zero vector. For the optimizer, θ = 0 is a trap: the state stays |0000⟩, every Z-product equals +1, and the gradient is zero. So each run starts from random angles and does 200 Adam steps with step size 0.1. It keeps the best of up to 10 restarts and stops early once the cost is within 10⁻³ of −1. A fixed seed keeps the output reproducible.

### Result

The circuit check matches both public cases (0.730681… and 0.936293…), and the optimizer reaches a minimum of about −0.9999999 on both, in under a second each.

---

## 3. NMR time evolution

Official title: `[To be added]`

### Problem

Evolve a single qubit starting in |0⟩ under the NMR Hamiltonian

H(t) = B0·Z + B1·(cos(ωt)·X − sin(ωt)·Y)

for a time `time`, using `qp.evolve`, and return the computational-basis probabilities. The inputs are `B0`, `B1`, `omega` and `time`. The tolerance is 3e-2.

### Solution

```python
def f_x(p, t):
    return p[0] * jnp.cos(p[1] * t)

def f_y(p, t):
    return -p[0] * jnp.sin(p[1] * t)

dev = qp.device('default.qubit', wires=1)

@qp.qnode(dev)
def nmr_evolve(B0, B1, omega, time):
    H = qp.dot([B0, f_x, f_y], [qp.PauliZ(0), qp.PauliX(0), qp.PauliY(0)])
    params = [jnp.array([B1, omega]), jnp.array([B1, omega])]
    qp.evolve(H)(params, t=time)
    return qp.probs(wires=0)
```

### What we did

The Hamiltonian has one constant term and two terms whose coefficients change with time, which is what PennyLane's `ParametrizedHamiltonian` is for. Passing `qp.dot` a mix of plain numbers and callables `f(p, t)` builds one. `B0` stays a fixed coefficient on Z, and `f_x`, `f_y` give B1·cos(ωt) and −B1·sin(ωt). `qp.evolve(H)(params, t=time)` needs one parameter entry per callable, in order, so both entries are `[B1, omega]`. A single float for `t` means "evolve from 0 to `time`", and PennyLane solves the time-ordered Schrödinger equation numerically with JAX. As a sanity check for the first case: over a short time H ≈ Z + 2X, which predicts P(1) ≈ 0.31, close to the expected 0.304.

### Result

Both public cases match to about 1e-6, well inside the 3e-2 tolerance: [0.69620…, 0.30379…] and [0.72782…, 0.27217…].

---

## 4. Unitary synthesis, Bronze

Official title: `[To be added]`

### Problem (shared by the Bronze, Silver and Gold versions)

Write `submission_circ(u_mat)`, which queues gates implementing a Haar-random unitary on 2, 3, 4 or 5 qubits. It must match to 1e-8 entrywise, global phase included. The circuit is decomposed into RX, RY, RZ, T, S, H, X, Y, Z, CNOT and GlobalPhase, and charged as follows:

- RX, RY and RZ cost 44 each (the T-count of one arbitrary rotation).
- T costs 1.
- Everything else costs 0.
- Every extra wire doubles the total, with at most 8 wires in all.

The target is the Shannon decomposition, which costs 44·(21/16·4ⁿ − 3·2ⁿ⁻¹), or 57,024 at 5 qubits. The saving at 5 qubits must reach the grade threshold (Bronze 5%, Silver 20%, Gold 60%), and the saving must never shrink from one size to the next. The template provides `cs_decomposition`, `diagonalize_unitary` and `_plain`, and no extra imports are allowed.

### Solution

Replace the template's `submission_circ` with this function (keep its docstring if you like). It only uses the template's helpers.

```python
def submission_circ(u_mat):
    def zyz(m):
        phi = float(np.angle(np.linalg.det(m))) / 2
        su = m * np.exp(-1j * phi)
        a, b = su[0, 0], su[1, 0]
        beta = 2 * float(np.arctan2(abs(b), abs(a)))
        pa = float(np.angle(a)) if abs(a) > 1e-14 else 0.0
        pb = float(np.angle(b)) if abs(b) > 1e-14 else 0.0
        return phi, pb - pa, beta, -pa - pb

    def mux(rot, angles, controls, target):
        angles = [float(x) for x in angles]
        if not controls:
            rot(angles[0], wires=target)
            return
        half = len(angles) // 2
        a0, a1 = angles[:half], angles[half:]
        mux(rot, [(x + y) / 2 for x, y in zip(a0, a1)], controls[1:], target)
        qp.CNOT(wires=[controls[0], target])
        mux(rot, [(x - y) / 2 for x, y in zip(a0, a1)], controls[1:], target)
        qp.CNOT(wires=[controls[0], target])

    def demux(a0, a1):
        v_mat, lam = diagonalize_unitary(a0 @ a1.conj().T)
        w_mat = np.exp(1j * lam / 2)[:, None] * (v_mat.conj().T @ a1)
        return v_mat, lam, w_mat

    u_mat = _plain(u_mat)
    n = int(round(np.log2(len(u_mat))))
    state = {"phase": 0.0, "pending": np.ones(4, dtype=complex), "left": 4 ** (n - 2)}

    def leaf(u, wires):
        a, b = wires
        u = u * state["pending"][None, :]
        state["left"] -= 1
        if state["left"] == 0:
            qp.QubitUnitary(u, wires=[a, b])
            return
        l0, l1, theta, r0, r1 = cs_decomposition(u)
        v_mat, lam, w_mat = demux(r0, r1)
        ph, al, be, ga = zyz(w_mat)
        qp.RZ(ga, wires=b)
        qp.RY(be, wires=b)
        qp.RZ(al, wires=b)
        state["phase"] += ph
        mux(qp.RZ, -lam, [b], a)
        ph, al, be, ga = zyz(v_mat)
        qp.RZ(ga, wires=b)
        qp.RY(be, wires=b)
        delta = np.exp(1j * ph) * np.array([np.exp(-0.5j * al), np.exp(0.5j * al)])
        mux(qp.RY, 2 * theta, [b], a)
        p0, a0, b0, g0 = zyz(l0 * delta[None, :])
        p1, a1, b1, g1 = zyz(l1 * delta[None, :])
        mux(qp.RZ, [g0, g1], [a], b)
        mux(qp.RY, [b0, b1], [a], b)
        state["pending"] = np.array([
            np.exp(1j * p0 - 0.5j * a0), np.exp(1j * p0 + 0.5j * a0),
            np.exp(1j * p1 - 0.5j * a1), np.exp(1j * p1 + 0.5j * a1)])

    def qsd(u, wires):
        if len(wires) == 2:
            leaf(u, wires)
            return
        top, rest = wires[0], wires[1:]
        l0, l1, theta, r0, r1 = cs_decomposition(u)
        v_mat, lam, w_mat = demux(r0, r1)
        qsd(w_mat, rest)
        mux(qp.RZ, -lam, rest, top)
        qsd(v_mat, rest)
        mux(qp.RY, 2 * theta, rest, top)
        v_mat, lam, w_mat = demux(l0, l1)
        qsd(w_mat, rest)
        mux(qp.RZ, -lam, rest, top)
        qsd(v_mat, rest)

    qsd(u_mat, list(range(n)))
    qp.GlobalPhase(-state["phase"], wires=0)
```

### What we did

This follows the Shannon decomposition itself: split on the top qubit with a cosine-sine decomposition, and "demultiplex" each block-diagonal half into two smaller unitaries plus an RZ multiplexor. Then recurse until only 2-qubit blocks remain. A general 2-qubit block costs 15 rotations, and the saving comes from not building each block in full. Every block except the last is implemented only up to a diagonal phase, which takes 13 rotations, and the leftover diagonal is handed to the next block. That works because every multiplexor in between uses the bottom two qubits as controls, so the diagonal commutes through it and merges into the next block's matrix for free. The last block absorbs everything with PennyLane's built-in 2-qubit decomposition (15 rotations). Multiplexed rotations are built recursively from CNOTs, so a multiplexor with k controls costs 2ᵏ rotations.

### Result

| Qubits | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Cost | 660 | 2,904 | 12,408 | 51,480 |
| Baseline | 660 | 3,168 | 13,728 | 57,024 |
| Saving | 0.0% | 8.3% | 9.6% | 9.7% |

The max error is about 1e-14, with no extra wires. Bronze passes.

---

## 5. Unitary synthesis, Silver

Official title: `[To be added]`

### Problem

Same as section 4, with a 20% saving needed at 5 qubits. That means at most 1,036 rotations, against a theoretical minimum of 1,023 for any rotation-based exact circuit.

### Solution

Replace the template's `submission_circ` with this function (keep its docstring if you like). It only uses the template's helpers.

```python
def submission_circ(u_mat):
    def zyz(m):
        phi = float(np.angle(np.linalg.det(m))) / 2
        su = m * np.exp(-1j * phi)
        a, b = su[0, 0], su[1, 0]
        beta = 2 * float(np.arctan2(abs(b), abs(a)))
        pa = float(np.angle(a)) if abs(a) > 1e-14 else 0.0
        pb = float(np.angle(b)) if abs(b) > 1e-14 else 0.0
        return phi, pb - pa, beta, -pa - pb

    def mux(rot, angles, controls, target):
        angles = [float(x) for x in angles]
        if not controls:
            rot(angles[0], wires=target)
            return
        half = len(angles) // 2
        a0, a1 = angles[:half], angles[half:]
        mux(rot, [(x + y) / 2 for x, y in zip(a0, a1)], controls[1:], target)
        qp.CNOT(wires=[controls[0], target])
        mux(rot, [(x - y) / 2 for x, y in zip(a0, a1)], controls[1:], target)
        qp.CNOT(wires=[controls[0], target])

    u_mat = _plain(u_mat)
    n = int(round(np.log2(len(u_mat))))
    state = {"phase": 0.0, "pending": np.ones(2 ** n, dtype=complex)}

    def split(diag, wire):
        # diag = (diagonal not touching `wire`) * (Rz multiplexor on `wire`)
        d = np.moveaxis(diag.reshape((2,) * n), wire, -1)
        ang0, ang1 = np.angle(d[..., 0]), np.angle(d[..., 1])
        omega = (ang1 - ang0).reshape(-1)
        psi = (ang0 + ang1) / 2
        rest = np.exp(1j * np.stack([psi, psi], axis=-1))
        rest = np.moveaxis(rest, -1, wire).reshape(-1)
        return omega, rest

    def leaf(blocks):
        p = state["pending"].reshape(-1, 2)
        gs, bs, trail = [], [], []
        for c in range(len(blocks)):
            ph, al, be, ga = zyz(blocks[c] * p[c][None, :])
            gs.append(ga)
            bs.append(be)
            trail += [np.exp(1j * ph - 0.5j * al), np.exp(1j * ph + 0.5j * al)]
        controls = list(range(n - 1))
        mux(qp.RZ, gs, controls, n - 1)
        mux(qp.RY, bs, controls, n - 1)
        state["pending"] = np.array(trail)

    def decompose(blocks, k):
        # blocks[c] acts on wires k..n-1, c indexes wires 0..k-1
        if k == n - 1:
            leaf(blocks)
            return
        ls, rs, thetas = [], [], []
        for blk in blocks:
            l0, l1, th, r0, r1 = cs_decomposition(blk)
            ls += [l0, l1]
            rs += [r0, r1]
            thetas.append(th)
        decompose(rs, k + 1)
        others = [w for w in range(n) if w != k]
        omega, rest = split(state["pending"], k)
        mux(qp.RZ, omega, others, k)
        state["pending"] = rest
        mux(qp.RY, 2 * np.concatenate(thetas), others, k)
        decompose(ls, k + 1)

    decompose([u_mat], 0)

    diag = state["pending"]
    for wire in range(n - 1, -1, -1):
        d = diag.reshape(-1, 2)
        a0, a1 = np.angle(d[:, 0]), np.angle(d[:, 1])
        mux(qp.RZ, a1 - a0, list(range(wire)), wire)
        diag = np.exp(1j * (a0 + a1) / 2)
    state["phase"] += float(np.angle(diag[0]))
    qp.GlobalPhase(-state["phase"], wires=0)
```

### What we did

The Bronze method wastes one multiplexor per recursion level on demultiplexing, so this version drops demultiplexing entirely. It keeps applying the cosine-sine split to the multiplexed blocks themselves, all the way down to single-qubit gates on the last wire, each controlled by every other qubit (the Möttönen et al. 2004 structure). The circuit then consists only of fully controlled RZ and RY multiplexors. Each leaf is written as Rz·Ry·Rz times a phase; only the Rz and Ry nearest in time are built, and the rest becomes a diagonal over all n qubits that is carried forward. Before each cosine-sine step on wire k, that diagonal is split into two parts:

- **The part that doesn't involve wire k.** It commutes past the RY multiplexor and merges into the next leaf for free.
- **An RZ multiplexor on wire k.** This is the only piece that costs rotations.

At the end, one last diagonal is built with a short chain of multiplexors, and the scalar phase goes into a `GlobalPhase` gate. Nothing in the circuit is redundant: it uses exactly 4ⁿ − 1 rotations, the number of real parameters in a unitary after the free global phase.

### Result

| Qubits | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Rotations | 15 | 63 | 255 | 1,023 |
| Cost | 660 | 2,772 | 11,220 | 45,012 |
| Baseline | 660 | 3,168 | 13,728 | 57,024 |
| Saving | 0.0% | 12.5% | 18.2% | 21.0% |

The platform's own run on seeds 7 and 2026 gave the same costs, with max errors of 1.5e-14 and 8.8e-15. I also checked it locally:

- No two rotations in the compiled circuit can be merged.
- No angle is a multiple of π/4 that a free Clifford or T gate could replace.

Silver passes, and the same code passes the Bronze version too.

---

## 6. Unitary synthesis, Gold

Official title: `[To be added]`

### Problem

Same as sections 4 and 5, with a 60% saving needed: a cost of 22,809 or less at 5 qubits, about 518 rotations' worth.

### Solution

Not solved. The best submission is the Silver code from section 5, which gets graded "Silver, 21.0%" on this version.

### What we did

Every rotation carries one real number, and a random 5-qubit unitary needs 1,023 of them (with the global phase free), so any exact circuit built from rotations needs at least 1,023 rotations. That costs 45,012, roughly double the Gold limit, and the Silver code already sits exactly on that floor. A circuit made of Clifford+T sequences isn't bound by that count, and on paper it could approximate a 5-qubit unitary with a few thousand T gates. But no known algorithm finds such sequences fast enough to run in seconds per sample. Every route we tested failed:

| Route | Estimated cost at 5 qubits | Why it fails |
|---|---|---|
| Merge or remove rotations in the Silver circuit | 45,012 | Zero mergeable pairs; already at the floor |
| Replace each rotation with a Clifford+T sequence | ~92,000 | Each rotation needs about 90 T gates for 1e-9 |
| Repeat-until-success circuits (Bocharov, Roetteler, Svore, arXiv:1404.5320) | ~90,000 | The 44 already comes from this paper; it also needs measurement (rejected by the grader) and an extra qubit (×2) |
| QROM / phase-gradient synthesis ("Unitary synthesis with fewer T gates") | — | Needs on the order of 170 extra qubits, against a cap of 3 |
| Flag decomposition (Xanadu) | 45,012 at best | Parameter-optimal, so it reaches the same floor as Silver |

To test the phase-gradient idea concretely, I wrote a small demo: an RZ replaced by adding an integer into a 3-qubit phase-gradient register. The rotation came out correct, with error around 1e-15. But the charged cost was between 16 and 14,928 depending on the angle, against 44 for a plain RZ, because the 3 extra qubits multiply everything by 8 and 3 bits only give multiples of π/4.

We didn't use grader workarounds, such as editing the cost table from inside `submission_circ`.

### Result

Not passed. 21.0% is the best honest score we found, and the Silver code is the submission to keep.
