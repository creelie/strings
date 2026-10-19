# Which String Vibrations Become Which Generations on the Dwork Quintic, release 1.1.0

This release adds Section VIII, Theorem E and Appendices D and E: the three other one-parameter pencils of Fermat type, the sextic in P(1,1,1,1,2), the octic in P(1,1,1,1,4) and the dectic in P(1,1,1,2,5).

- Each member with psi^d prod w_i^{w_i} ≠ 1 is a smooth Calabi–Yau threefold with h^{1,1} = 1 and h^{2,1} = 103, 149 and 145.
- The generations are the monomials x^b with 0 ≤ b_i ≤ n_i − 2 of weighted degree d, but they carry only 96, 122 and 100 distinct characters of the symmetry groups of order 108, 128 and 100: 7, 27 and 42 classes of two or three generations share a character, found by hand through the wrapping lemma.
- The socle functional is psi^r prod w_i^{k_i} in sector r and zero outside the sectors, so every coupling allowed by the symmetry is nonzero for psi ≠ 0.
- The mass map of the invariant direction has rank 99, 125 and 109 at every member with psi ≠ 0, leaving 4, 24 and 36 generations massless, and 44, 85 and 72 at psi = 0; the blocks are listed in Tables IV and V.
- No member and no free quotient of a member carries three families, by Riemann–Roch on the descended norm line bundle.

The quintic is the only one of the four pencils on which the characters label every generation and the invariant deformation gives every generation a mass.

The archive now holds 121 checks (Python and Macaulay2 checks of the weighted pencils added) and 14 Lean 4 theorems, each axiom-free or depending on propext only, and the engine record covers five targets, run on Anaxia release 3.1.0 (doi:10.5281/zenodo.23484160). The paper cites the archive by its concept DOI, 10.5281/zenodo.23480310.

Assets: the PDF, the LaTeX source with the figures as PNG (tex.zip), and the arXiv package (tar.gz) with the checks, the engine record and the Lean file in `anc/`.
