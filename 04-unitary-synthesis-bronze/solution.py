"""Unitary synthesis, Bronze: Shannon decomposition with diagonal absorption (9.7% saving)."""
# Paste this function into the challenge template in place of submission_circ.
# It uses the template's helpers (cs_decomposition, diagonalize_unitary, _plain)
# and the template's imports (pennylane as qp, pennylane.numpy as np).

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
