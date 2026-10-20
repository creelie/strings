/-
  Which string vibrations become which generations on the Dwork quintic:
  the finite arithmetic of Theorems 1 to 3 and of the Hessian in the socle,
  checked by the Lean kernel. Core Lean 4 only; every proof is `decide`.
  Labels are lists of five exponents; a vector of degree fifteen lies in
  sector r when all its entries are congruent to 3 - r modulo five.
-/

namespace Strings

/-- all lists of length `n` with entries in {0, ..., k - 1} -/
def tuples (k : Nat) : Nat → List (List Nat)
  | 0 => [[]]
  | n + 1 => (List.range k).flatMap (fun x => (tuples k n).map (x :: ·))

def total (v : List Nat) : Nat := v.foldl (· + ·) 0

/-- the exponent vectors b in {0,1,2,3}^5 with |b| = 5, a basis of R_5 -/
def B : List (List Nat) := (tuples 4 5).filter (fun v => total v == 5)

theorem labels_count : B.length = 101 := by decide +kernel

/-- the class of v in (Z/5)^5/<1>, normalised so that the last entry is zero -/
def cls (v : List Nat) : Nat :=
  match v with
  | [a, b, c, _, e] => ((a + 5 - e) % 5) * 25 + ((b + 5 - e) % 5) * 5 + (c + 5 - e) % 5
  | _ => 125

def chars : List Nat := B.map cls

/-- the 101 labels meet 101 of the 125 characters, so the characters are distinct -/
theorem characters_distinct : (List.range 125).countP (fun c => chars.contains c) = 101 := by
  decide +kernel

/-- the permutations of (0,1,2,3,4) -/
def perms : List (List Nat) :=
  (tuples 5 5).filter (fun v => (List.range 5).all (fun i => v.contains i))

def permChars : List Nat := perms.map cls

/-- the 24 characters that do not occur are exactly the classes of the 120 permutations -/
theorem missing_characters :
    perms.length = 120 ∧
    (List.range 125).countP (fun c => permChars.contains c) = 24 ∧
    (List.range 125).all (fun c => chars.contains c != permChars.contains c) = true := by
  decide +kernel

/-- the type of a label: the number of entries equal to 3, 2, 1 -/
def typeOf (v : List Nat) : Nat × Nat × Nat :=
  (v.countP (· == 3), v.countP (· == 2), v.countP (· == 1))

/-- the S5-orbits {1,1,1,1,1}, {2,1,1,1,0}, {2,2,1,0,0}, {3,1,1,0,0}, {3,2,0,0,0} -/
theorem orbit_sizes :
    B.countP (fun v => typeOf v == (0, 0, 5)) = 1 ∧
    B.countP (fun v => typeOf v == (0, 1, 3)) = 20 ∧
    B.countP (fun v => typeOf v == (0, 2, 1)) = 30 ∧
    B.countP (fun v => typeOf v == (1, 0, 2)) = 30 ∧
    B.countP (fun v => typeOf v == (1, 1, 0)) = 20 := by
  decide +kernel

/-- the third label c of a coupling in sector r with given a + b (entries at most six):
    c_i is the residue of 3 - r - a_i - b_i; it is a label when every residue is at most
    three and the residues sum to five -/
def third (r : Nat) (s : List Nat) : List Nat := s.map (fun x => (18 - r - x) % 5)

def isLabel (c : List Nat) : Bool := c.all (· ≤ 3) && total c == 5

def add (a b : List Nat) : List Nat := List.zipWith (· + ·) a b

/-- number of ordered triples (a, b, c) in sector r -/
def orderedSector (r : Nat) : Nat :=
  B.foldl (fun n a => B.foldl (fun n b => if isLabel (third r (add a b)) then n + 1 else n) n) 0

theorem ordered_by_sector :
    orderedSector 0 = 3391 ∧ orderedSector 1 = 2400 ∧
    orderedSector 2 = 1620 ∧ orderedSector 3 = 870 := by
  decide +kernel

/-- a pair (a, b) is excluded when no third label completes it in any sector -/
def excluded : Nat :=
  B.foldl (fun n a => B.foldl (fun n b =>
    if (List.range 4).any (fun r => isLabel (third r (add a b))) then n else n + 1) n) 0

theorem excluded_pairs : excluded = 1920 ∧ 101 * 101 - 1920 = 8281 ∧
    3391 + 2400 + 1620 + 870 = 8281 := by
  decide +kernel

/-- ordered triples (a, a, c) with c ≠ a in sector r -/
def repeated (r : Nat) : Nat :=
  B.foldl (fun n a => let c := third r (add a a)
    if isLabel c && c != a then n + 1 else n) 0

/-- D_r = 0, 50, 20, 30 and the unordered counts 566, 425, 280, 160, 1431 -/
theorem unordered_count :
    repeated 0 = 0 ∧ repeated 1 = 50 ∧ repeated 2 = 20 ∧ repeated 3 = 30 ∧
    (3391 - 0 - 1) / 6 + 0 + 1 = 566 ∧ (2400 - 3 * 50) / 6 + 50 = 425 ∧
    (1620 - 3 * 20) / 6 + 20 = 280 ∧ (870 - 3 * 30) / 6 + 30 = 160 ∧
    566 + 425 + 280 + 160 = 1431 := by
  decide +kernel

/-- O(e): ordered pairs (a, b) with e - a - b a label -/
def O (e : List Nat) : Nat :=
  B.foldl (fun n a => B.foldl (fun n b =>
    let c := List.zipWith (fun x y => x - y) e (add a b)
    if (List.zipWith (fun x y => decide (y ≤ x)) e (add a b)).all id && isLabel c then n + 1 else n) n) 0

theorem O_values :
    O [3, 3, 3, 3, 3] = 3391 ∧ O [7, 2, 2, 2, 2] = 480 ∧
    O [6, 6, 1, 1, 1] = 162 ∧ O [5, 5, 5, 0, 0] = 87 ∧
    5 * 480 = 2400 ∧ 10 * 162 = 1620 ∧ 10 * 87 = 870 := by
  decide +kernel

/-- the partner of b under h = x1...x5 in sector r: residues of 2 - r - b -/
def partnerIn (r : Nat) (b : List Nat) : List Nat := b.map (fun x => (17 - r - x) % 5)

def partnerCount (b : List Nat) : Nat := (List.range 4).countP (fun r => isLabel (partnerIn r b))

def power (b : List Nat) : Nat :=
  ((List.range 4).filter (fun r => isLabel (partnerIn r b))).headD 9

def sigma (b : List Nat) : List Nat := partnerIn (power b) b

/-- every label has exactly one partner, σ is a type-preserving involution with the single
    fixed point (1,1,1,1,1), the couplings are 1, ψ, ψ² on 51, 30, 20 labels, the determinant
    is ψ^70, and the fifty labels with a three are those paired with a power of ψ -/
theorem mass_map :
    B.all (fun b => partnerCount b == 1) = true ∧
    B.all (fun b => sigma (sigma b) == b && typeOf (sigma b) == typeOf b) = true ∧
    B.countP (fun b => sigma b == b) = 1 ∧ sigma [1, 1, 1, 1, 1] = [1, 1, 1, 1, 1] ∧
    B.countP (fun b => power b == 0) = 51 ∧ B.countP (fun b => power b == 1) = 30 ∧
    B.countP (fun b => power b == 2) = 20 ∧
    B.foldl (fun n b => n + power b) 0 = 70 ∧
    B.all (fun b => b.contains 3 == decide (power b > 0)) = true := by
  decide +kernel

/-! ## The Hessian in the socle -/

def moved (p : List Nat) : Nat := (List.range 5).countP (fun i => p.getD i i != i)

def inversions (p : List Nat) : Nat :=
  (List.range 5).foldl (fun n i => (List.range 5).foldl (fun n j =>
    if i < j && p.getD i 0 > p.getD j 0 then n + 1 else n) n) 0

/-- the monomial of the permutation term: x_k^3 from a fixed diagonal entry, and x_k from
    every off-diagonal entry (i, p i) with k ≠ i, p i -/
def monomial (p : List Nat) : List Nat :=
  (List.range 5).map (fun k =>
    (if p.getD k k == k then 3 else 0) +
    (List.range 5).countP (fun i => p.getD i i != i && i != k && p.getD i i != k))

/-- the rule: x^(3+m) at fixed points and x^(m-2) at moved points -/
theorem moved_point_rule :
    perms.all (fun p => monomial p == (List.range 5).map (fun k =>
      if p.getD k k == k then 3 + moved p else moved p - 2)) = true := by
  decide +kernel

def sec (e : List Nat) : Nat :=
  match e with
  | [] => 5
  | x :: xs => if xs.all (fun y => y % 5 == x % 5) then (8 - x % 5) % 5 else 5

/-- magnitude 20^(5-m) 5^m and sign (-1)^(inversions + m) of the term of p -/
def magnitude (p : List Nat) : Nat := 20 ^ (5 - moved p) * 5 ^ moved p
def negative (p : List Nat) : Bool := (inversions p + moved p) % 2 == 1

/-- sums of the positive and negative terms with ψ-degree m + r = d -/
def termSum (d : Nat) (neg : Bool) : Nat :=
  perms.foldl (fun n p =>
    if moved p + sec (monomial p) == d && negative p == neg then n + magnitude p else n) 0

/-- every term lands in a sector, with ψ-degree 0 or 5, and
    Hess F = 3 200 000 (1 - ψ^5) m0 in the socle -/
theorem hessian_socle :
    perms.all (fun p => sec (monomial p) ≤ 3 &&
      (moved p + sec (monomial p) == 0 || moved p + sec (monomial p) == 5)) = true ∧
    termSum 0 false = 3200000 ∧ termSum 0 true = 0 ∧
    termSum 5 false = 250000 ∧ termSum 5 true = 3450000 ∧
    3450000 - 250000 = 3200000 := by
  decide +kernel

/-! ## The weighted Fermat pencils -/

/-- all lists whose i-th entry lies in {0, ..., k_i - 1} -/
def boxes : List Nat → List (List Nat)
  | [] => [[]]
  | k :: ks => (List.range k).flatMap (fun x => (boxes ks).map (x :: ·))

def wdeg (w v : List Nat) : Nat := (List.zipWith (· * ·) w v).foldl (· + ·) 0

/-- the labels of the pencil of degree d in P(w), n_i = d / w_i: b_i ≤ n_i - 2, degree d -/
def wlabels (d : Nat) (w n : List Nat) : List (List Nat) :=
  (boxes (n.map (· - 1))).filter (fun v => wdeg w v == d)

/-- the character of x^v: v modulo n up to multiples of (1,...,1), as the least of its
    d shifts written in base ten -/
def wcls (d : Nat) (n v : List Nat) : Nat :=
  ((List.range d).map (fun k =>
    (List.zipWith (fun x m => (x + k) % m) v n).foldl (fun a x => 10 * a + x) 0)).foldl min 1000000

def distinct : List Nat → Nat
  | [] => 0
  | x :: xs => (if xs.contains x then 0 else 1) + distinct xs

/-- number of labels whose character is shared with another label -/
def shared (L : List Nat) : Nat := L.countP (fun c => L.countP (· == c) ≥ 2)

def sextic : List (List Nat) := wlabels 6 [1, 1, 1, 1, 2] [6, 6, 6, 6, 3]
def octic : List (List Nat) := wlabels 8 [1, 1, 1, 1, 4] [8, 8, 8, 8, 2]
def dectic : List (List Nat) := wlabels 10 [1, 1, 1, 2, 5] [10, 10, 10, 5, 2]

/-- 103, 149, 145 labels carrying 96, 122, 100 characters; 14, 54, 87 labels share a
    character with another label -/
theorem weighted_labels :
    sextic.length = 103 ∧ distinct (sextic.map (wcls 6 [6, 6, 6, 6, 3])) = 96 ∧
    shared (sextic.map (wcls 6 [6, 6, 6, 6, 3])) = 14 ∧
    octic.length = 149 ∧ distinct (octic.map (wcls 8 [8, 8, 8, 8, 2])) = 122 ∧
    shared (octic.map (wcls 8 [8, 8, 8, 8, 2])) = 54 ∧
    dectic.length = 145 ∧ distinct (dectic.map (wcls 10 [10, 10, 10, 5, 2])) = 100 ∧
    shared (dectic.map (wcls 10 [10, 10, 10, 5, 2])) = 87 := by
  decide +kernel

def esym2 (w : List Nat) : Nat :=
  (List.range 5).foldl (fun s i => (List.range 5).foldl (fun s j =>
    if i < j then s + w.getD i 0 * w.getD j 0 else s) s) 0

def esym3 (w : List Nat) : Nat :=
  (List.range 5).foldl (fun s i => (List.range 5).foldl (fun s j => (List.range 5).foldl
    (fun s k => if i < j && j < k then s + w.getD i 0 * w.getD j 0 * w.getD k 0 else s) s) s) 0

/-- -χ = (d σ₂ - σ₃) d / ∏ w, and h^{2,1} = 1 - χ/2 is the number of labels -/
theorem weighted_euler :
    (6 * esym2 [1, 1, 1, 1, 2] - esym3 [1, 1, 1, 1, 2]) * (6 / 2) = 204 ∧
    (8 * esym2 [1, 1, 1, 1, 4] - esym3 [1, 1, 1, 1, 4]) * (8 / 4) = 296 ∧
    (10 * esym2 [1, 1, 1, 2, 5] - esym3 [1, 1, 1, 2, 5]) * (10 / 10) = 288 ∧
    204 / 2 + 1 = 103 ∧ 296 / 2 + 1 = 149 ∧ 288 / 2 + 1 = 145 ∧
    esym2 [1, 1, 1, 1, 2] * 3 = 42 ∧ esym2 [1, 1, 1, 2, 5] * 1 = 34 := by
  decide +kernel

/-- on a free quotient by H with π*D = m L, D³ = m³ L³/|H| and c₂·D = m c₂·L/|H|; the
    Riemann-Roch number D³/6 + c₂·D/12 is an integer only if 12 divides 2 D³ + c₂·D -/
def rrFails (H L3 c2L : Nat) : Bool :=
  (List.range (H + 1)).all (fun m =>
    !(m > 0 && H % m == 0 && (m ^ 3 * L3) % H == 0 && (m * c2L) % H == 0) ||
    (2 * (m ^ 3 * L3 / H) + m * c2L / H) % 12 != 0)

/-- three families needs |H| = 34 on the sextic and 48 on the dectic, and the Riemann-Roch
    number is never an integer there; 200 and 296 are not divisible by 6 -/
theorem no_three_families :
    204 / 6 = 34 ∧ 288 / 6 = 48 ∧ 200 % 6 ≠ 0 ∧ 296 % 6 ≠ 0 ∧
    rrFails 34 3 42 = true ∧ rrFails 48 1 34 = true := by
  decide +kernel

/-- Vafa's formula for a Fermat type, all weights dividing d: the sum over (l, r) of the
    products of 1 - d/w over the coordinates with d | l w and d | r w; the Euler number is
    this sum divided by d -/
def vafaSum (d : Nat) (w : List Nat) : Int :=
  ((List.range d).map (fun l => ((List.range d).map (fun r =>
    (w.filter (fun wi => (l * wi) % d == 0 && (r * wi) % d == 0)).foldl
      (fun acc wi => acc * (1 - ((d / wi : Nat) : Int))) 1)).foldl (· + ·) 0)).foldl (· + ·) 0

def isPowOf (p n : Nat) : Bool := (List.range 12).any (fun k => p ^ k == n)

/-- the three weighted hypersurfaces with free automorphisms have Euler numbers -200, -216
    and -288, and |chi|/6 is never a power of the prime that acts -/
theorem free_quotient_euler :
    vafaSum 5 [1, 1, 1, 1, 1] = -200 * 5 ∧ vafaSum 9 [1, 1, 1, 3, 3] = -216 * 9 ∧
    vafaSum 16 [1, 1, 2, 4, 8] = -288 * 16 ∧
    200 % 6 ≠ 0 ∧ isPowOf 3 (216 / 6) = false ∧ isPowOf 2 (288 / 6) = false := by
  decide +kernel

end Strings

#print axioms Strings.labels_count
#print axioms Strings.characters_distinct
#print axioms Strings.missing_characters
#print axioms Strings.orbit_sizes
#print axioms Strings.ordered_by_sector
#print axioms Strings.excluded_pairs
#print axioms Strings.unordered_count
#print axioms Strings.O_values
#print axioms Strings.mass_map
#print axioms Strings.moved_point_rule
#print axioms Strings.hessian_socle
#print axioms Strings.weighted_labels
#print axioms Strings.weighted_euler
#print axioms Strings.no_three_families
#print axioms Strings.free_quotient_euler
