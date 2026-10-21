# Which String Vibrations Become Which Generations on the Dwork Quintic, release 1.2.0

This release adds the subsection "Free quotients of the one-parameter families" and sets the paper in a single column for submission.

- For a simply connected Calabi–Yau threefold with Picard group Z, an automorphism of prime order p without fixed points forces p to divide chi(X, kL) for every k, by the holomorphic Lefschetz formula of Atiyah and Bott.
- For the thirteen hypergeometric one-parameter complete intersections the greatest common divisor g_X of these values is 5, 1, 2, 1, 3, 2, 1, 8, 4, 1, 1, 1, 1 (X_5, X_6, X_8, X_10, X_{3,3}, X_{4,2}, X_{3,2,2}, X_{2,2,2,2}, X_{4,4}, X_{6,6}, X_{4,3}, X_{6,4}, X_{6,2}).
- Every prime dividing the order of a group acting freely divides g_X, so seven types, among them the sextic and the dectic, admit no free action at all, and no free quotient of any of the thirteen carries three families with the standard embedding.

The archive now holds 215 checks (94 new ones in `code/checks/free_quotients.py`, in exact arithmetic) and 14 Lean 4 theorems, each axiom-free or depending on propext only. The engine is cited at Anaxia release 3.2.1 (doi:10.5281/zenodo.23524945). `paper/paper1/` holds the compiled paper and `paper/paper2/` its LaTeX source as one zip. The paper cites this release by its release page and the concept DOI, 10.5281/zenodo.23480310.

Assets: the PDF, the LaTeX source with the figures as PNG (tex.zip), and the arXiv package (tar.gz) with the checks, the engine record and the Lean file in `anc/`.
