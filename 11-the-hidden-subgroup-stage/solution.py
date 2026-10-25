"""The Hidden Subgroup Stage (200 pts): symmetry score."""
# Paste into the challenge template. It uses the template's imports
# (pennylane as qp, numpy as np).

def symmetry_score(data, labels, s):
    N = len(data)
    rows = [tuple(int(b) for b in x) for x in data]
    s_t = tuple(int(b) for b in s)
    score = 0.0
    for r in set(int(l) for l in labels):
        members = {rows[i] for i in range(N) if int(labels[i]) == r}
        paired = sum(1 for x in members
                     if tuple(a ^ b for a, b in zip(x, s_t)) in members)
        p_r = 0.5 * (1 + paired / len(members))
        score += len(members) / N * p_r
    return float(score)
