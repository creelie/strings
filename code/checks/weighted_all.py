"""Free quotients of quasi-smooth Calabi-Yau hypersurfaces in weighted P^4 (Theorem F).

  (A) The 147 Fermat types: solutions of 1/n_1+...+1/n_5 = 1, weights w_i = d/n_i.
  (B) Euler numbers by Vafa's formula, checked against PALP for all 7555 transversal
      weight systems listed in data/wp4_hodge.txt (well-formedness and the
      transversality criterion of Kreuzer and Skarke are rechecked here too).
  (C) Free diagonal automorphisms of prime order p | chi on every Fermat type: an element
      a in prod (1/n_i)Z / Z_d is free iff the fixed lines {t : w_i t = a_i mod 1} are
      pairwise disjoint.  Only the quintic (p = 5), the nonic in P(1,1,1,3,3) (p = 3) and
      the hexadecic in P(1,1,2,4,8) (p = 2) have one.
  (D) |chi|/|H| is never 6 for a p-group H on those three; the hypersurfaces with |chi| = 6
      themselves are simply connected."""
from fractions import Fraction as F
from itertools import product, combinations
from math import gcd, lcm
import os, sys
passed = failed = 0
def check(name, ok, detail=""):
    global passed, failed
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))
    if ok: passed += 1
    else: failed += 1

def fr(x): return x - (x.numerator // x.denominator)

# (A) Fermat types
sols = []
def rec(k, start, rem, cur):
    if rem <= 0: return
    if k == 1:
        if rem.numerator == 1 and rem.denominator >= start: sols.append(cur + [rem.denominator])
        return
    n = max(start, -(-rem.denominator // rem.numerator))
    while F(k, n) >= rem:
        rec(k - 1, n, rem - F(1, n), cur + [n]); n += 1
rec(5, 2, F(1), [])
fermat = []
for n in sols:
    d = lcm(*n); w = [d // x for x in n]; g = gcd(*w); fermat.append((d // g, [x // g for x in w], n))
check("Fermat types: 1/n_1+...+1/n_5 = 1 has 147 solutions", len(fermat) == 147, str(len(fermat)))

# (B) Vafa's formula chi = (1/d) sum_{l,r} prod_{i: d | l w_i, d | r w_i} (1 - d/w_i)
def chi_vafa(d, w):
    cnt = {}
    for l in range(d):
        A = frozenset(i for i in range(5) if (l * w[i]) % d == 0)
        cnt[A] = cnt.get(A, 0) + 1
    tot = F(0)
    for A, a in cnt.items():
        for B, b in cnt.items():
            p = F(1)
            for i in A & B: p *= 1 - F(d, w[i])
            tot += a * b * p
    tot /= d
    assert tot.denominator == 1
    return int(tot)
check("Vafa's formula on the quintic", chi_vafa(5, [1] * 5) == -200)

def transversal(d, w):
    """Kreuzer-Skarke: for every nonempty I there is a monomial of degree d in x_I, or
    monomials x_I^m x_k of degree d for at least |I| distinct k outside I."""
    for r in range(1, 6):
        for I in combinations(range(5), r):
            def has(deg, I):
                # is deg a nonnegative integer combination of the weights in I?
                ok = [False] * (deg + 1); ok[0] = True
                for v in range(1, deg + 1):
                    ok[v] = any(v >= w[i] and ok[v - w[i]] for i in I)
                return deg >= 0 and ok[deg]
            if has(d, I): continue
            ks = [k for k in range(5) if k not in I and has(d - w[k], I)]
            if len(ks) < r: return False
    return True

data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "wp4_hodge.txt")
rows = []
for line in open(data):
    if line.startswith("#") or not line.strip(): continue
    t = list(map(int, line.split()))
    rows.append((t[0], t[1:6], t[6], t[7]))
check("PALP list: 7555 transversal weight systems", len(rows) == 7555, str(len(rows)))
check("every weight system has degree equal to the sum of the weights",
      all(d == sum(w) for d, w, _, _ in rows))
bad_wf = [w for d, w, _, _ in rows
          if any(gcd(*[w[i] for i in range(5) if i != k]) != 1 for k in range(5))
          or any(d % gcd(w[i], w[j], w[k]) for i, j, k in combinations(range(5), 3))]
check("every P(w) and every hypersurface is well formed", not bad_wf, str(bad_wf[:3]))
bad_tr = [w for d, w, _, _ in rows if not transversal(d, w)]
check("every weight system passes the transversality criterion", not bad_tr, str(bad_tr[:3]))
bad_chi = [(w, 2 * (h11 - h21)) for d, w, h11, h21 in rows if chi_vafa(d, w) != 2 * (h11 - h21)]
check("Vafa's Euler number equals 2(h11 - h21) from PALP for all 7555", not bad_chi, str(bad_chi[:3]))
six = [(w, h11, h21) for d, w, h11, h21 in rows if abs(h11 - h21) == 3]
print("   |chi| = 6:", len(six), "weight systems", six[:10])
fw = {tuple(sorted(w)) for d, w, _, _ in fermat}
check("the 147 Fermat types are among the 7555",
      fw <= {tuple(sorted(w)) for d, w, _, _ in rows})

# (C) free diagonal elements of prime order
def primes(n):
    p, out = 2, []
    while p * p <= n:
        if n % p == 0: out.append(p)
        while n % p == 0: n //= p
        p += 1
    if n > 1: out.append(n)
    return out
def free_diag(w, n, d, p):
    found = 0
    shifts = [[F(k, n[j]) for j in range(5)] for k in range(d)]
    for a4 in product(*[[F(k, n[j]) for k in range(n[j])] for j in range(4)]):
        a = list(a4) + [F(0)]
        if not any(all(fr(p * a[j] - s[j]) == 0 for j in range(5)) for s in shifts): continue
        if any(all(fr(a[j] - s[j]) == 0 for j in range(5)) for s in shifts): continue
        seen = set(); ok = True
        for j in range(5):
            S = {fr((a[j] + m) / w[j]) for m in range(w[j])}
            if seen & S: ok = False; break
            seen |= S
        if ok: found += 1
    return found
free = {}
for d, w, n in fermat:
    chi = chi_vafa(d, w)
    for p in (primes(abs(chi)) if chi else []):
        c = free_diag(w, n, d, p)
        if c: free[(tuple(sorted(w)), p)] = (c, chi)
expect = {((1, 1, 1, 1, 1), 5): (24, -200), ((1, 1, 1, 3, 3), 3): (4, -216),
          ((1, 1, 2, 4, 8), 2): (1, -288)}
check("free automorphisms of prime order exist only on the quintic (Z5), the nonic in "
      "P(1,1,1,3,3) (Z3) and the hexadecic in P(1,1,2,4,8) (Z2)", free == expect, str(free))

# (D) three families
ok = True
for (w, p), (c, chi) in free.items():
    k = 0
    while abs(chi) % p ** (k + 1) == 0: k += 1
    ok &= all(abs(chi) != 6 * p ** j for j in range(1, k + 1))
check("|chi(X)| = 6|H| has no solution with H a nontrivial p-group on these three", ok)

print(f"{passed} checks passed, {failed} failed")
sys.exit(1 if failed else 0)
