# Pauli word measurement from probabilities

Official title: `[To be added]`

### Problem

A fixed `prepare(angles)` function builds a 3-qubit state. Write `measure_pauli_word(word, angles)`, where `word` is three letters from `I`, `X`, `Y`, `Z`. You may only return `qp.probs(wires=[0, 1, 2])` from the circuit; `qp.expval` and `qp.state` are blocked. Return three things:
- `basis`: the basis change per wire (`"none"`, `"H"` or `"SH"`).
- `signs`: the ±1 parity of each of the 8 outcomes, with wire 0 as the most significant bit.
- `value`: the expectation value, the sum of probability × sign.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

A quantum computer only measures in the Z basis, so measuring X or Y means rotating that axis onto Z first. A Hadamard does it for X because HXH = Z, and S† followed by H does it for Y. After those basis changes the word is a product of Z's, and each shot's value is a parity: +1 if an even number of the participating bits are 1, −1 if odd. 

Two decisions are kept apart on purpose:
1. The gate applied to a wire depends on its letter (I and Z both get none), but the parity depends only on whether the letter is I.
2. Z wires need no gate and still count toward the sign, and that's where people usually go wrong. The expectation value is then the probability-weighted sum of the signs.

### Result

Both public tests match: `"ZIZ"` gives 0.931986…, and `"XYI"` gives 0.967399…, with the exact basis and sign lists the grader expects.
