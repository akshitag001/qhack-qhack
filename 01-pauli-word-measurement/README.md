# Pauli word measurement from probabilities

Official title: `[To be added]`

### Problem

A fixed `prepare(angles)` function builds a 3-qubit state. Write `measure_pauli_word(word, angles)`, where `word` is three letters from `I`, `X`, `Y`, `Z`. You may only return `qp.probs(wires=[0, 1, 2])` from the circuit; `qp.expval` and `qp.state` are blocked. Return three things:
- `basis`: the basis change per wire (`"none"`, `"H"` or `"SH"`).
- `signs`: the ±1 parity of each of the 8 outcomes, with wire 0 as the most significant bit.
- `value`: the expectation value, the sum of probability × sign.

### Result

Both public tests match: `"ZIZ"` gives 0.931986…, and `"XYI"` gives 0.967399…, with the exact basis and sign lists the grader expects.
