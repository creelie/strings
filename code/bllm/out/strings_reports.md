# Run report: Yukawa couplings of the Dwork pencil

## 1. Axiom base

Lean's type theory with propext, Classical.choice, Quot.sound

## 2. Definition ledger (obligations)

- `couplings` (theorem, weight 1.0): UNK, certified through its bridges
- `symmetry-count` (computation, weight 1.0): PASS, verified by Doran-Greene-Judes 2008
- `allowed-couplings-nonzero` (computation, weight 1.0): FAIL
- `socle-functional` (computation, weight 1.0): PASS, verified by checks/socle.m2
- `coupling-powers` (computation, weight 1.0): PASS, verified by checks/labels.c, lean/Strings.lean

## 3. Dependency graph

- socle-functional, coupling-powers ⇒ couplings

## 5. Residue ledger

- none

## 8. Playbook

- core failures: 2, bullets: 2, density 1, rejected updates: 0
- [FAIL/FAIL] computation: allowed-couplings-nonzero failed its verifier
- [UNK/UNK] strategy: evaluate the socle functional of the Jacobian ring on every monomial of degree fifteen

## 14. Release label

**CANDIDATE**; factors {'proof': 1, 'formal': 1, 'code': 1, 'trace': 1, 'sim': 1, 'risk': 1, 'lit': 1, 'human': 0}; blocking: human

## 15. Human / referee checklist

- [ ] every definition typed, with its axiom scope
- [ ] proof, refutation and independence branches all considered
- [ ] every bridge has zero or named scope loss
- [ ] every unresolved star converted into a named residue
- [ ] the label is one of THEOREM, COUNTEREXAMPLE, CONDITIONAL, INDEPENDENCE, CANDIDATE, BUJ, OPEN

# Run report: Mass map of the invariant deformation

## 1. Axiom base

Lean's type theory with propext, Classical.choice, Quot.sound

## 2. Definition ledger (obligations)

- `mass-map` (theorem, weight 1.0): UNK, certified through its bridges
- `unique-partner` (computation, weight 1.0): PASS, verified by checks/labels.c, lean/Strings.lean

## 3. Dependency graph

- unique-partner ⇒ mass-map

## 5. Residue ledger

- none

## 8. Playbook

- core failures: 0, bullets: 0, density 0, rejected updates: 0

## 14. Release label

**CANDIDATE**; factors {'proof': 1, 'formal': 1, 'code': 1, 'trace': 1, 'sim': 1, 'risk': 1, 'lit': 1, 'human': 0}; blocking: human

## 15. Human / referee checklist

- [ ] every definition typed, with its axiom scope
- [ ] proof, refutation and independence branches all considered
- [ ] every bridge has zero or named scope loss
- [ ] every unresolved star converted into a named residue
- [ ] the label is one of THEOREM, COUNTEREXAMPLE, CONDITIONAL, INDEPENDENCE, CANDIDATE, BUJ, OPEN

# Run report: Masses at the Fermat point

## 1. Axiom base

Lean's type theory with propext, Classical.choice, Quot.sound

## 2. Definition ledger (obligations)

- `fermat` (theorem, weight 1.0): UNK, certified through its bridges
- `fermat-norms` (computation, weight 1.0): PASS, verified by Distler-Greene 1988, checks/fermat.jl

## 3. Dependency graph

- fermat-norms ⇒ fermat

## 5. Residue ledger

- none

## 8. Playbook

- core failures: 0, bullets: 0, density 0, rejected updates: 0

## 14. Release label

**CANDIDATE**; factors {'proof': 1, 'formal': 1, 'code': 1, 'trace': 1, 'sim': 1, 'risk': 1, 'lit': 1, 'human': 0}; blocking: human

## 15. Human / referee checklist

- [ ] every definition typed, with its axiom scope
- [ ] proof, refutation and independence branches all considered
- [ ] every bridge has zero or named scope loss
- [ ] every unresolved star converted into a named residue
- [ ] the label is one of THEOREM, COUNTEREXAMPLE, CONDITIONAL, INDEPENDENCE, CANDIDATE, BUJ, OPEN

# Run report: Geometric Selection Conjecture

## 1. Axiom base

Lean's type theory with propext, Classical.choice, Quot.sound

## 2. Definition ledger (obligations)

- `selection` (theorem, weight 1.0): UNK
- `three-families` (computation, weight 1.0): FAIL
- `gsc-equivalence` (lemma, weight 1.0): PASS, verified by Theorem D
- `viable-vacuum-exists` (literature, weight 1.0): FAIL

## 3. Dependency graph

- (no bridges)

## 5. Residue ledger

- selection

## 8. Playbook

- core failures: 4, bullets: 4, density 1, rejected updates: 0
- [FAIL/FAIL] computation: three-families failed its verifier
- [UNK/UNK] strategy: separate the functional from the vacuum: the conjecture is equivalent to one viable vacuum fixed by mu
- [FAIL/FAIL] literature: viable-vacuum-exists failed its verifier
- [UNK/UNK] strategy: the existence of a viable vacuum stays open

## 14. Release label

**OPEN**; factors {'proof': 0, 'formal': 1, 'code': 1, 'trace': 1, 'sim': 1, 'risk': 1, 'lit': 1, 'human': 0}; blocking: proof, human

## 15. Human / referee checklist

- [ ] every definition typed, with its axiom scope
- [ ] proof, refutation and independence branches all considered
- [ ] every bridge has zero or named scope loss
- [ ] every unresolved star converted into a named residue
- [ ] the label is one of THEOREM, COUNTEREXAMPLE, CONDITIONAL, INDEPENDENCE, CANDIDATE, BUJ, OPEN

# Run report: Weighted Fermat pencils

## 1. Axiom base

Lean's type theory with propext, Classical.choice, Quot.sound

## 2. Definition ledger (obligations)

- `weighted` (theorem, weight 1.0): UNK, certified through its bridges
- `distinct-characters` (computation, weight 1.0): FAIL
- `wrap-classes` (computation, weight 1.0): PASS, verified by checks/weighted.py
- `jacobian-rings` (computation, weight 1.0): PASS, verified by checks/weighted.m2
- `mass-blocks` (computation, weight 1.0): PASS, verified by checks/weighted.py, lean/Strings.lean
- `three-families` (computation, weight 1.0): PASS, verified by checks/weighted.py, lean/Strings.lean

## 3. Dependency graph

- wrap-classes, jacobian-rings, mass-blocks, three-families ⇒ weighted

## 5. Residue ledger

- none

## 8. Playbook

- core failures: 2, bullets: 2, density 1, rejected updates: 0
- [FAIL/FAIL] computation: distinct-characters failed its verifier
- [UNK/UNK] strategy: find the labels that share a character by their shift and evaluate the mass map block by block on the characters and their inverses

## 14. Release label

**CANDIDATE**; factors {'proof': 1, 'formal': 1, 'code': 1, 'trace': 1, 'sim': 1, 'risk': 1, 'lit': 1, 'human': 0}; blocking: human

## 15. Human / referee checklist

- [ ] every definition typed, with its axiom scope
- [ ] proof, refutation and independence branches all considered
- [ ] every bridge has zero or named scope loss
- [ ] every unresolved star converted into a named residue
- [ ] the label is one of THEOREM, COUNTEREXAMPLE, CONDITIONAL, INDEPENDENCE, CANDIDATE, BUJ, OPEN

