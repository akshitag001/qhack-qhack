"""Time evolution under the NMR Hamiltonian."""
import jax
import jax.numpy as jnp
import pennylane as qp

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
