## couplings

| Round | Strategy | Failed checks | Change made | Label after round |
|---|---|---|---|---|
| 1 | count the couplings allowed by the symmetry | allowed-couplings-nonzero | evaluate the socle functional of the Jacobian ring on every monomial of degree fifteen | OPEN |
| 2 | socle functional on every monomial of degree fifteen | none | - | CANDIDATE |

- round 1, `symmetry-count`: pass. 1431 unordered triples of labels with x^(b+b'+b'') fixed by Gamma, the count of Doran-Greene-Judes
- round 1, `allowed-couplings-nonzero`: FAIL. at psi = 0 only 566 of the 1431 allowed couplings are nonzero, so the symmetry count bounds the nonzero couplings from above and decides nothing more
- round 2, `socle-functional`: pass. Jacobian ring at psi = 2 and psi = 1/3: socle functional psi^r in sector r, zero elsewhere, on all 3876 monomials of degree 15 (8 checks passed, 0 failed)
- round 2, `coupling-powers`: pass. the allowed couplings are psi^r with r = 0, 1, 2, 3 on [566, 425, 280, 160] unordered triples; every other coupling vanishes

Final label: **CANDIDATE**; blocking factors: human.

## mass map

| Round | Strategy | Failed checks | Change made | Label after round |
|---|---|---|---|---|
| 1 | pairing by the invariant class | none | - | CANDIDATE |

- round 1, `unique-partner`: pass. each label has one partner; sigma is an involution fixing only (1,1,1,1,1); entries psi^0, psi^1, psi^2 on 51, 30, 20 labels; determinant psi^70; rank 51 at psi = 0

Final label: **CANDIDATE**; blocking factors: human.

## Fermat point

| Round | Strategy | Failed checks | Change made | Label after round |
|---|---|---|---|---|
| 1 | Gamma-function norms against Distler-Greene | none | - | CANDIDATE |

- round 1, `fermat-norms`: pass. kappa^2 = gamma(1/5)/gamma(2/5)^3 = 1.19324 (Distler-Greene 1.19324); Weil-Petersson metric at psi = 0: 0.19226

Final label: **CANDIDATE**; blocking factors: human.

## selection conjecture

| Round | Strategy | Failed checks | Change made | Label after round |
|---|---|---|---|---|
| 1 | look for the viable vacuum on the quintic itself | three-families | separate the functional from the vacuum: the conjecture is equivalent to one viable vacuum fixed by mu | OPEN |
| 2 | functional and vacuum separated | viable-vacuum-exists | the existence of a viable vacuum stays open | OPEN |

- round 1, `three-families`: FAIL. standard embedding: 100/|H| net families on X/H; 3 does not divide 100, so no quintic and no free quotient carries three families
- round 2, `gsc-equivalence`: pass. Theorem D: a functional with (G1)-(G4) exists if and only if there is a viable vacuum fixed by mu (proved in Section 8 from geodesic wells and partitions of unity)
- round 2, `viable-vacuum-exists`: FAIL. the literature consulted (BHOP05, BD06, AGLP11, AGLP12) gives heterotic models with three families and the Standard Model group, but no vacuum is shown to meet all nine conditions (C1)-(C9), stabilised moduli and supersymmetry breaking included

Final label: **OPEN**; blocking factors: proof, human.

## weighted pencils

| Round | Strategy | Failed checks | Change made | Label after round |
|---|---|---|---|---|
| 1 | carry the proof of Theorem A over to the weighted pencils | distinct-characters | find the labels that share a character by their shift and evaluate the mass map block by block on the characters and their inverses | OPEN |
| 2 | labels by shift and the mass map by blocks | none | - | CANDIDATE |

- round 1, `distinct-characters`: FAIL. the 103 labels of the sextic carry 96 characters; 7 characters are shared, e.g. x1^4 x5 and x2^2 x3^2 x4^2 at shift 2
- round 2, `wrap-classes`: pass. labels sharing a character found by their shift and matched with the hand lists (7, 27, 42 classes; 96, 122, 100 characters); socle functional by sectors on all monomials of degree 3d (39 checks passed, 0 failed)
- round 2, `jacobian-rings`: pass. weighted Jacobian rings at psi = 1/3 and psi = -2: dimensions, labels a basis, socle functional by sectors (18 checks passed, 0 failed)
- round 2, `mass-blocks`: pass. mass map of the invariant label block by block: ranks [99, 125, 109] for the sextic, octic and dectic, so 4, 24 and 36 generations stay massless at every smooth member with psi != 0
- round 2, `three-families`: pass. three families on X/H needs |H| = 34 (sextic) or 48 (dectic), and then chi(O(D)) = D^3/6 + c2.D/12 is 1163/2, 593/12 or 2321/6; for the octic 296/6 is not an integer

Final label: **CANDIDATE**; blocking factors: human.

