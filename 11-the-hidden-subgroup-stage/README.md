# The Hidden Subgroup Stage (200 pts)

Official title: The Hidden Subgroup Stage

### Problem

Given binary strings with class labels and a candidate symmetry $s$, compute the score $S(s) = \sum_r \frac{|X_r|}{N} p_r(s)$. Here $p_r(s)$ is the probability that the Hadamard-based symmetry test passes for class $r$. A closed-form answer is allowed.

### Solution File
Implementation: [`solution.py`](solution.py)

### What we did

The quantum test has a simple classical shortcut: for each class, $p_r = \frac{1}{2}(1 + \text{fraction of points } x \text{ whose partner } x \oplus s \text{ is also in the class})$. A fully paired class scores 1, and a class with no pairs scores $\frac{1}{2}$, which is the coin-flip value a lone point gives after the Hadamards. The code groups points by label into sets, counts how many points find their XOR partner in the same set, turns that count into $p_r$, and weights each class by its size.

### Result

Completed on the platform. Re-checked: the worked example from the statement (`["000", "110", "001", "111", "101"]`, labels `[0, 0, 1, 1, 2]`, $s = 110$) gives 0.9, as expected.
