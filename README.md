# Which String Vibrations Become Which Generations on the Dwork Quintic

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23480310.svg)](https://doi.org/10.5281/zenodo.23480310)

Deep Bhattacharjee and Ushashi Bhattacharya

This repository holds the paper, the independent checks and the engine record
for *Which String Vibrations Become Which Generations on the Dwork Quintic*.
The paper is in
[`preprints/DworkGenerations.pdf`](preprints/DworkGenerations.pdf)
and its LaTeX source in [`paper/`](paper/).

## What is proved

The heterotic string with the standard embedding on a quintic threefold of the
Dwork pencil

    X_ψ = { x1^5 + x2^5 + x3^5 + x4^5 + x5^5 − 5ψ x1x2x3x4x5 = 0 } ⊂ P^4

has 101 families of charged particles, one for each class in H^{2,1}, and these
classes are the monomials x^b with b in {0,1,2,3}^5 and |b| = 5. The group
Γ ≅ (Z/5)^3 of diagonal phases acts on every member.

1. **Labels.** The 101 classes carry 101 distinct characters of Γ. The 24
   characters that do not occur are the classes of the permutations of
   (0,1,2,3,4). The coordinate permutations act in orbits of sizes 1, 20, 20,
   30 and 30.
2. **Couplings.** The Yukawa coupling of three families a, b, c is ψ^r when
   a + b + c ≡ (3 − r)(1,1,1,1,1) mod 5 for some r in {0,1,2,3}, and zero
   otherwise. There are 1431 unordered triples with a nonzero coupling, 566,
   425, 280 and 160 of them with r = 0, 1, 2, 3. This proves that the symmetry
   is the only source of zeros, which the count of Doran, Greene and Judes did
   not decide.
3. **Mass map.** The invariant direction x1x2x3x4x5 pairs each family with
   exactly one partner by an involution with one fixed point. The coupling is
   1, ψ or ψ^2 on 51, 30 and 20 labels, the mass matrix has determinant ψ^70,
   full rank for ψ ≠ 0, and rank 51 at the Fermat point.
4. **Fermat point.** The Hodge norms and the masses are given in closed form
   by the Gamma function; the two mass ratios are 0.83805 and 0.70234.
5. **Selection.** The Geometric Selection Conjecture holds if and only if
   there is one viable vacuum fixed by mirror symmetry. No smooth quintic and
   no free quotient of one carries three families with the standard embedding.
6. **Weighted pencils.** On the three other one-parameter families of Fermat
   type, the sextic in P(1,1,1,1,2), the octic in P(1,1,1,1,4) and the dectic
   in P(1,1,1,2,5), with 103, 149 and 145 families, the symmetry no longer
   separates the families: they carry 96, 122 and 100 distinct characters of
   groups of order 108, 128 and 100. Every coupling allowed by the symmetry is
   psi^r times a product of weights, and nonzero for psi ≠ 0. The mass map of
   the invariant direction has rank 99, 125 and 109 at every member with
   psi ≠ 0, so 4, 24 and 36 families stay massless, and no member or free
   quotient carries three families. The quintic is the only one of the four
   pencils on which the symmetry labels every family and the invariant
   deformation gives every family a mass.

The existence of a viable vacuum is open.

## Layout

| Path | Contents |
|---|---|
| `paper/` | `main.tex` and the figures as PNG |
| `figures/` | `make_figures.py`, which draws the five figures |
| `preprints/` | the compiled paper |
| `code/checks/` | independent checks in C, C++, Python, Julia and Macaulay2 |
| `code/run_checks.sh` | runs every check and prints one summary line |
| `code/bllm/` | the failure, change and retry record of the five targets on the Anaxia engine |
| `lean/Strings.lean` | 14 theorems in Lean 4 (core library only) on the counts, the arithmetic of the Hessian and the weighted pencils |

## Running the checks

```sh
python3 -m pip install -r requirements.txt
bash code/run_checks.sh          # 121 checks
```

The script needs gcc, g++, Python 3 with numpy, sympy and mpmath, Julia,
Macaulay2 and Lean 4 (the version in `lean/lean-toolchain`); a missing tool is
reported and its checks are skipped. The Lean file takes about two minutes.

The engine record is rebuilt with the Anaxia engine
([creelie/eBLLM](https://github.com/creelie/eBLLM), release 3.1.0,
[doi:10.5281/zenodo.23484160](https://doi.org/10.5281/zenodo.23484160)):

```sh
cd code && PYTHONPATH=/path/to/eBLLM/src python3 bllm/strings_loop.py
```

## Citation

See [`CITATION.cff`](CITATION.cff). Zenodo archives each GitHub release under
its own version DOI and gathers all of them under one concept DOI; the paper
of release v1.1.0 cites the concept DOI, which resolves to the newest
version.

| | DOI |
| --- | --- |
| release v1.1.0 (version DOI) | [10.5281/zenodo.23484427](https://doi.org/10.5281/zenodo.23484427) |
| release v1.0.2 (version DOI) | [10.5281/zenodo.23483470](https://doi.org/10.5281/zenodo.23483470) |
| release v1.0.1 (version DOI) | [10.5281/zenodo.23480492](https://doi.org/10.5281/zenodo.23480492) |
| release v1.0.0 (version DOI) | [10.5281/zenodo.23480311](https://doi.org/10.5281/zenodo.23480311) |
| all versions (concept DOI) | [10.5281/zenodo.23480310](https://doi.org/10.5281/zenodo.23480310) |

Everything in the paper, with the checks, the engine record and the release
assets, is also collected in one file,
[`DworkGenerations_masterzipfinal2.zip`](https://github.com/creelie/strings/raw/main/DworkGenerations_masterzipfinal2.zip).

## License

MIT for the code; the paper is licensed CC BY 4.0.
