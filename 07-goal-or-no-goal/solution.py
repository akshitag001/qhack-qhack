"""Goal or No Goal? (100 pts): GHZ state certification."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np).

def prepare_and_build_checks(n):
    # Step 1: prepare the GHZ state -- Hadamard on wire 0, then CNOT fan-out
    qp.Hadamard(wires=0)
    for i in range(1, n):
        qp.CNOT(wires=[0, i])

    # Step 2: global X parity X_0 X_1 ... X_(n-1)
    checks = [qp.prod(*[qp.PauliX(i) for i in range(n)])]

    # Step 3: neighbouring ZZ parities Z_i Z_(i+1)
    for i in range(n - 1):
        checks.append(qp.prod(qp.PauliZ(i), qp.PauliZ(i + 1)))

    # Step 4: return all n checks
    return checks
