"""The five targets of the paper on the Anaxia engine: every failure, the change it forced, the retry.
Run from code/:  PYTHONPATH=<eBLLM>/src python3 bllm/strings_loop.py
Macaulay2 (M2 on the PATH, or the variable M2) is used for the socle functional."""
import sys, os, re, shutil, subprocess
from collections import Counter
from itertools import product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from loop import Check, Round, Target, run_target, write_outputs
from ebllm.package import ConjecturePackage

B = [b for b in product(range(4), repeat=5) if sum(b) == 5]
def esum(*bs): return tuple(sum(b[i] for b in bs) for i in range(5))
def invariant(e): return len({x % 5 for x in e}) == 1          # x^e fixed by Gamma
def sector(e):
    s = {x % 5 for x in e}
    return (3 - s.pop()) % 5 if len(s) == 1 else None
TRIPLES = [(i, j, k) for i in range(101) for j in range(i, 101) for k in range(j, 101)]

def symmetry_count():
    n = sum(invariant(esum(B[i], B[j], B[k])) for i, j, k in TRIPLES)
    return dict(ok=n == 1431, evidence=f"{n} unordered triples of labels with x^(b+b'+b'') fixed by "
                "Gamma, the count of Doran-Greene-Judes")

def allowed_nonzero():
    """At psi = 0 the Jacobian ideal is (x_i^4), so x^e of degree 15 is nonzero only for e = (3,3,3,3,3)."""
    allowed = [t for t in TRIPLES if invariant(esum(*(B[x] for x in t)))]
    alive = sum(esum(*(B[x] for x in t)) == (3,) * 5 for t in allowed)
    return dict(ok=alive == len(allowed),
                evidence=f"at psi = 0 only {alive} of the {len(allowed)} allowed couplings are nonzero, so "
                         "the symmetry count bounds the nonzero couplings from above and decides nothing more")

def socle_m2():
    m2 = os.environ.get('M2', 'M2')
    if not shutil.which(m2):
        return dict(ok=False, evidence="Macaulay2 not found")
    out = subprocess.run([m2, '--script', 'checks/socle.m2'], capture_output=True, text=True).stdout
    m = re.search(r'(\d+) checks passed, (\d+) failed', out)
    ok = bool(m) and m.group(2) == '0' and int(m.group(1)) == 8
    return dict(ok=ok, evidence="Jacobian ring at psi = 2 and psi = 1/3: socle functional psi^r in sector r, "
                f"zero elsewhere, on all 3876 monomials of degree 15 ({m.group(0) if m else 'no summary'})")

def coupling_powers():
    cnt = Counter(sector(esum(*(B[x] for x in t))) for t in TRIPLES)
    cnt.pop(None, None)
    ok = sum(cnt.values()) == 1431 and [cnt[r] for r in range(4)] == [566, 425, 280, 160] and cnt[4] == 0
    return dict(ok=ok, evidence=f"the allowed couplings are psi^r with r = 0, 1, 2, 3 on "
                f"{[cnt[r] for r in range(4)]} unordered triples; every other coupling vanishes")

def mass_pairing():
    """Partner of b under the invariant direction h = x1...x5: b + b' + (1,...,1) in a sector."""
    part = {b: [c for c in B if sector(esum(b, c, (1,) * 5)) is not None] for b in B}
    uniq = all(len(v) == 1 for v in part.values())
    sig = {b: v[0] for b, v in part.items()}
    inv = all(sig[sig[b]] == b for b in B)
    fixed = [b for b in B if sig[b] == b]
    pw = Counter(sector(esum(b, sig[b], (1,) * 5)) for b in B)
    det = sum(sector(esum(b, sig[b], (1,) * 5)) for b in B)     # one entry in each row and column
    ok = uniq and inv and fixed == [(1,) * 5] and pw == Counter({0: 51, 1: 30, 2: 20}) and det == 70
    return dict(ok=ok, evidence=f"each label has one partner; sigma is an involution fixing only (1,1,1,1,1); "
                f"entries psi^0, psi^1, psi^2 on {pw[0]}, {pw[1]}, {pw[2]} labels; determinant psi^{det}; "
                f"rank {pw[0]} at psi = 0")

def fermat_norms():
    mp.mp.dps = 30
    gam = lambda j: mp.gamma(mp.mpf(j) / 5) / mp.gamma(1 - mp.mpf(j) / 5)
    k2 = gam(1) / gam(2) ** 3
    G0 = 25 * gam(2) ** 5 / gam(1) ** 5
    ok = abs(k2 - mp.mpf('1.19324')) < 1e-5 and abs(G0 - mp.mpf('0.19226')) < 1e-5
    return dict(ok=ok, evidence=f"kappa^2 = gamma(1/5)/gamma(2/5)^3 = {mp.nstr(k2, 6)} (Distler-Greene 1.19324); "
                f"Weil-Petersson metric at psi = 0: {mp.nstr(G0, 5)}")

def families_quintic():
    h11, h21 = 1, 101
    net = h21 - h11
    sols = [n for n in range(1, net + 1) if net % n == 0 and net // n == 3]
    return dict(ok=bool(sols), evidence=f"standard embedding: {net}/|H| net families on X/H; "
                f"3 does not divide {net}, so no quintic and no free quotient carries three families")

def gsc_equivalence():
    return dict(ok=True, evidence="Theorem D: a functional with (G1)-(G4) exists if and only if there is a "
                "viable vacuum fixed by mu (proved in Section 8 from geodesic wells and partitions of unity)")

def viable_vacuum():
    return dict(ok=False, evidence="the literature consulted (BHOP05, BD06, AGLP11, AGLP12) gives heterotic "
                "models with three families and the Standard Model group, but no vacuum is shown to meet all "
                "nine conditions (C1)-(C9), stabilised moduli and supersymmetry breaking included")

def weighted_run():
    out = subprocess.run([sys.executable, 'checks/weighted.py'], capture_output=True, text=True).stdout
    return out

def sextic_characters():
    """Theorem A carried over unchanged: are the characters of the sextic labels distinct?"""
    n, w, d = (6, 6, 6, 6, 3), (1, 1, 1, 1, 2), 6
    labels = [b for b in product(*[range(m - 1) for m in n]) if sum(x * y for x, y in zip(b, w)) == d]
    cls = lambda b: min(tuple((x + k) % m for x, m in zip(b, n)) for k in range(d))
    chars = Counter(cls(b) for b in labels)
    shared = sum(1 for v in chars.values() if v > 1)
    return dict(ok=len(chars) == len(labels),
                evidence=f"the {len(labels)} labels of the sextic carry {len(chars)} characters; "
                         f"{shared} characters are shared, e.g. x1^4 x5 and x2^2 x3^2 x4^2 at shift 2")

def weighted_classes():
    out = weighted_run()
    m = re.search(r'(\d+) checks passed, (\d+) failed', out)
    ok = bool(m) and m.group(2) == '0' and int(m.group(1)) == 39
    return dict(ok=ok, evidence="labels sharing a character found by their shift and matched with the hand lists "
                "(7, 27, 42 classes; 96, 122, 100 characters); socle functional by sectors on all monomials of "
                f"degree 3d ({m.group(0) if m else 'no summary'})")

def weighted_mass():
    out = weighted_run()
    ranks = [int(x) for x in re.findall(r'mass map of h has rank (\d+) at psi = 3/7', out)]
    ok = ranks == [99, 125, 109, 101][:len(ranks)] and len(ranks) == 3
    return dict(ok=ok, evidence=f"mass map of the invariant label block by block: ranks {ranks} for the sextic, "
                "octic and dectic, so 4, 24 and 36 generations stay massless at every smooth member with psi != 0")

def weighted_jacobian_m2():
    m2 = os.environ.get('M2', 'M2')
    if not shutil.which(m2):
        return dict(ok=False, evidence="Macaulay2 not found")
    out = subprocess.run([m2, '--script', 'checks/weighted.m2'], capture_output=True, text=True).stdout
    m = re.search(r'(\d+) checks passed, (\d+) failed', out)
    ok = bool(m) and m.group(2) == '0' and int(m.group(1)) == 18
    return dict(ok=ok, evidence="weighted Jacobian rings at psi = 1/3 and psi = -2: dimensions, labels a basis, "
                f"socle functional by sectors ({m.group(0) if m else 'no summary'})")

def weighted_families():
    out = weighted_run()
    ok = 'never an integer  [m0=34: 1163/2]' in out and 'm0=24: 593/12, m0=48: 2321/6' in out \
        and '296/6 is not an integer' in out
    return dict(ok=ok, evidence="three families on X/H needs |H| = 34 (sextic) or 48 (dectic), and then "
                "chi(O(D)) = D^3/6 + c2.D/12 is 1163/2, 593/12 or 2321/6; for the octic 296/6 is not an integer")

def weighted_all_run():
    return subprocess.run([sys.executable, 'checks/weighted_all.py'], capture_output=True, text=True).stdout

def fermat_types():
    out = weighted_all_run()
    return dict(ok='PASS Fermat types' in out and 'PASS Vafa' in out,
                evidence="147 Fermat types; Vafa's Euler number agrees with PALP on all 7555 weight systems")

def free_quotients():
    out = weighted_all_run()
    ok = 'PASS free automorphisms of prime order exist only' in out and 'PASS |chi(X)| = 6|H|' in out
    return dict(ok=ok, evidence="free prime-order automorphisms only on the quintic (Z5), P(1,1,1,3,3)[9] (Z3) "
                "and P(1,1,2,4,8)[16] (Z2); |chi| = 200, 216, 288 is never 6 times a power of that prime")

def weighted_all_clean():
    out = weighted_all_run()
    return dict(ok=bool(re.search(r'^\d+ checks passed, 0 failed$', out, re.M)),
                evidence=out.strip().splitlines()[-1] if out.strip() else "no output")

pc = ConjecturePackage(name="Yukawa couplings of the Dwork pencil", domain="quintic threefolds X_psi",
                       hypothesis="psi generic", conclusion="each coupling is psi^r on its sector and zero otherwise")
T1 = Target("couplings", pc, "couplings", [
    Round("count the couplings allowed by the symmetry",
          [Check("symmetry-count", "computation", symmetry_count, "Doran-Greene-Judes 2008"),
           Check("allowed-couplings-nonzero", "computation", allowed_nonzero)],
          change="evaluate the socle functional of the Jacobian ring on every monomial of degree fifteen"),
    Round("socle functional on every monomial of degree fifteen",
          [Check("socle-functional", "computation", socle_m2, "checks/socle.m2"),
           Check("coupling-powers", "computation", coupling_powers, "checks/labels.c, lean/Strings.lean")],
          bridges=[(["socle-functional", "coupling-powers"], "couplings", 0.0)]),
])
pm = ConjecturePackage(name="Mass map of the invariant deformation", domain="quintic threefolds X_psi",
                       conclusion="each family has one partner; fifty families massless at psi = 0 only")
T2 = Target("mass map", pm, "mass-map", [
    Round("pairing by the invariant class",
          [Check("unique-partner", "computation", mass_pairing, "checks/labels.c, lean/Strings.lean")],
          bridges=[(["unique-partner"], "mass-map", 0.0)]),
])
pf = ConjecturePackage(name="Masses at the Fermat point", domain="Fermat quintic",
                       conclusion="closed forms in the Gamma function")
T3 = Target("Fermat point", pf, "fermat", [
    Round("Gamma-function norms against Distler-Greene",
          [Check("fermat-norms", "computation", fermat_norms, "Distler-Greene 1988, checks/fermat.jl")],
          bridges=[(["fermat-norms"], "fermat", 0.0)]),
])
ps = ConjecturePackage(name="Geometric Selection Conjecture", domain="heterotic vacua",
                       conclusion="a smooth proper mirror-invariant functional with a unique viable minimum")
T4 = Target("selection conjecture", ps, "selection", [
    Round("look for the viable vacuum on the quintic itself",
          [Check("three-families", "computation", families_quintic)],
          change="separate the functional from the vacuum: the conjecture is equivalent to one viable "
                 "vacuum fixed by mu"),
    Round("functional and vacuum separated",
          [Check("gsc-equivalence", "lemma", gsc_equivalence, "Theorem D"),
           Check("viable-vacuum-exists", "literature", viable_vacuum)],
          change="the existence of a viable vacuum stays open"),
], conditions=["a viable vacuum fixed by mu"], model_ok=False)

pw = ConjecturePackage(name="Weighted Fermat pencils", domain="sextic, octic and dectic pencils",
                       conclusion="labels, couplings and mass map of the invariant direction")
T5 = Target("weighted pencils", pw, "weighted", [
    Round("carry the proof of Theorem A over to the weighted pencils",
          [Check("distinct-characters", "computation", sextic_characters)],
          change="find the labels that share a character by their shift and evaluate the mass map "
                 "block by block on the characters and their inverses"),
    Round("labels by shift and the mass map by blocks",
          [Check("wrap-classes", "computation", weighted_classes, "checks/weighted.py"),
           Check("jacobian-rings", "computation", weighted_jacobian_m2, "checks/weighted.m2"),
           Check("mass-blocks", "computation", weighted_mass, "checks/weighted.py, lean/Strings.lean"),
           Check("three-families", "computation", weighted_families, "checks/weighted.py, lean/Strings.lean")],
          bridges=[(["wrap-classes", "jacobian-rings", "mass-blocks", "three-families"], "weighted", 0.0)]),
])

pa = ConjecturePackage(name="Hypersurfaces in weighted projective four-space",
                       domain="the 7555 quasi-smooth Calabi-Yau hypersurfaces and their free quotients",
                       hypothesis="standard embedding, Wilson-line breaking",
                       conclusion="no member carries three families with a Wilson line")
T6 = Target("weighted hypersurfaces", pa, "weighted-all", [
    Round("list the Fermat types and check Vafa's formula against PALP",
          [Check("fermat-types", "computation", fermat_types, "checks/weighted_all.py")]),
    Round("diagonal elements, fixed lines and divisibility of chi",
          [Check("free-quotients", "computation", free_quotients, "checks/weighted_all.py, lean/Strings.lean"),
           Check("all-checks", "computation", weighted_all_clean, "checks/weighted_all.py")],
          bridges=[(["fermat-types", "free-quotients", "all-checks"], "weighted-all", 0.0)]),
])

if __name__ == '__main__':
    factors = dict(proof=1, formal=1, code=1, trace=1, sim=1, risk=1, lit=1, human=0)
    res = [run_target(t, factors) for t in (T1, T2, T3, T4, T5, T6)]
    os.makedirs('bllm/out', exist_ok=True)
    write_outputs(res, 'bllm/out/strings')
    for r in res: print(r['target'], r['label'], 'blocking', r['blocking'])
