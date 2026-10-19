# Which String Vibrations Become Which Generations on the Dwork Quintic

First release of the paper "Which String Vibrations Become Which Generations on the Dwork Quintic" by Deep Bhattacharjee and Ushashi Bhattacharya, with its checks and the record of the Anaxia engine.

- The 101 generations of the heterotic string on the quintic pencil carry 101 distinct characters of the symmetry group (Z/5)^3; the 24 characters that do not occur are the classes of the permutations of (0,1,2,3,4).
- Every Yukawa coupling allowed by the symmetry is a power ψ^r of the modulus, with r = 0, 1, 2, 3 on 566, 425, 280 and 160 unordered triples, 1431 in all, and every other coupling vanishes.
- The invariant direction pairs each generation with exactly one partner; the mass matrix has determinant ψ^70, full rank for ψ ≠ 0, and rank 51 at the Fermat point, where the masses are given by the Gamma function.
- The Geometric Selection Conjecture is equivalent to the existence of one viable vacuum fixed by mirror symmetry; no smooth quintic and no free quotient of one carries three families with the standard embedding. The existence of a viable vacuum is open.

Every result is proved by hand in the paper. `code/run_checks.sh` runs 64 independent checks in C, C++, Python, Julia, Macaulay2, Lean 4 and shell, and `lean/Strings.lean` proves 11 Lean 4 theorems, each axiom-free or depending on propext only. `code/bllm/` holds the failure, change and retry record of the four targets on the Anaxia engine (creelie/eBLLM, release 3.0.5).

Assets: the PDF, the LaTeX source with the figures as PNG (tex.zip), and the arXiv package (tar.gz) with the checks, the engine record and the Lean file in `anc/`.
