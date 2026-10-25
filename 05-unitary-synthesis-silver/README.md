# Unitary synthesis, Silver

Official title: `[To be added]`

### Problem

Same as Bronze, with a 20% saving needed at 5 qubits. That means at most 1,036 rotations, against a theoretical minimum of 1,023 for any rotation-based exact circuit.

### Result

| Qubits | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Rotations | 15 | 63 | 255 | 1,023 |
| Cost | 660 | 2,772 | 11,220 | 45,012 |
| Baseline | 660 | 3,168 | 13,728 | 57,024 |
| Saving | 0.0% | 12.5% | 18.2% | 21.0% |

The platform's own run on seeds 7 and 2026 gave the same costs, with max errors of 1.5e-14 and 8.8e-15. Silver passes (21.0% saving), and the same code passes the Bronze version too.
