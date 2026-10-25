"""Unitary synthesis, Silver: full CSD with multiplexed rotations, 4^n - 1 rotations (21.0% saving)."""
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
