"""Diffuse and Conquer (400 pts): diffusion step solved with QSVT."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np).

phi = np.array([0.03, 0.04, 0.07, 0.09])
source = np.array([1., 2., 1., 0.5])
dt = 0.01
h = 0.2

# Odd degree-15 polynomial approximating C/x on [0.15, 1]
poly = [0.0, 2.943948799795254, 0.0, -38.29551590171806, 0.0, 234.37837795175182,
        0.0, -776.9382045460882, 0.0, 1476.698615967201, 0.0, -1607.753358505814,
        0.0, 931.7941734998069, 0.0, -222.7637805415573]
phi_qsvt = qp.poly_to_angles(poly, "QSVT")
C = 0.075

b = phi + dt * source


def build_A(nu, k):
    D2 = (np.diag([-2.] * 4) + np.diag([1.] * 3, 1) + np.diag([1.] * 3, -1)) / h**2
    A = (1 + k * dt) * np.eye(4) - nu * dt * D2
    alpha = 1 + k * dt + 4 * nu * dt / h**2
    return A / alpha


def qsvt_op(A_n, angles):
    block = qp.BlockEncode(A_n, wires=[1, 2, 3])
    projectors = [qp.PCPhase(angle, dim=4, wires=[1, 2, 3]) for angle in angles]
    return qp.QSVT(block, projectors)


device = qp.device("default.qubit", wires=4)


@qp.qnode(device)
def qsvt_diffusion(nu, k):
    A_n = build_A(nu, k)
    qp.StatePrep(b / np.linalg.norm(b), wires=[2, 3])

    with qp.QueuingManager.stop_recording():
        U_plus = qsvt_op(A_n, np.array(phi_qsvt))    # block = P(A) + iQ(A)
        U_minus = qsvt_op(A_n, -np.array(phi_qsvt))  # block = P(A) - iQ(A)

    # LCU on wire 0: (U_plus + U_minus) / 2 keeps only the real part P(A)
    qp.Hadamard(wires=0)
    qp.ctrl(U_plus, control=0, control_values=0)
    qp.ctrl(U_minus, control=0, control_values=1)
    qp.Hadamard(wires=0)
    return qp.state()
