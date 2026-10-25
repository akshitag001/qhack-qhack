# Fermionic VQE (200 pts)

Official title: Fermionic VQE

### Problem

The Hamiltonian is $H = c_0 a_0 a_0^\dagger + c_1 a_1 a_1^\dagger + c_2 a_2 a_2^\dagger$ on 6 fermionic modes. Write three functions:
- `build_hamiltonian(coeffs)`: maps $H$ to qubits with `qp.jordan_wigner` and rebuilds it with real coefficients.
- `vqe_circuit(params, coeffs)`: a QNode returning the energy of a trial state.
- `optimization(coeffs)`: returns the optimized ground-state energy.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

Each term $a_i a_i^\dagger$ is written as a `FermiWord`, scaled by its coefficient and summed. `qp.jordan_wigner` turns that into Pauli operators on 6 qubits. It returns complex coefficients with zero imaginary part, so the code keeps the real parts and rebuilds a `qp.Hamiltonian`. Every term in $H$ is diagonal in the computational basis, so one RY rotation per qubit can reach the ground state. Adam with step size 0.1 runs 300 steps from random starting angles.

### Result

Completed on the platform. Re-checked: the energy matches the exact ground energy for coefficients [1, 2, 3] (energy 0) and [−1, 0.5, −2] (energy −3).
