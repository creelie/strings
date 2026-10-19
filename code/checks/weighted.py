"""Checks for the weighted Fermat pencils of 'Which String Vibrations Become Which
Generations on the Dwork Quintic': the sextic in P(1,1,1,1,2), the octic in
P(1,1,1,1,4) and the dectic in P(1,1,1,2,5), each with the pencil
F = sum x_i^{n_i} - d psi x_1...x_5.  Recomputes the labels, the reduction to them,
the characters and the labels that share one, the characters that do not occur, the
sectors of the socle functional, the blocks and ranks of the mass map of the
invariant label, and the arithmetic that rules out three families on a free quotient.
The quintic is run through the same code as a control.  Run: python3 weighted.py"""
import itertools
from collections import Counter, defaultdict
from fractions import Fraction
import sympy as sp

passes = fails = 0
def check(name, ok, info=''):
    global passes, fails
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else ''))
    if ok: passes += 1
    else: fails += 1

psi = sp.Symbol('psi')
FAMILIES = {'quintic': (5, (1, 1, 1, 1, 1)), 'sextic': (6, (1, 1, 1, 1, 2)),
            'octic': (8, (1, 1, 1, 1, 4)), 'dectic': (10, (1, 1, 1, 2, 5))}

def deg(e, w): return sum(a * b for a, b in zip(e, w))
def add(*vs): return tuple(map(sum, zip(*vs)))

class Family:
    def __init__(self, name):
        self.name = name
        self.d, self.w = FAMILIES[name]
        self.n = tuple(self.d // x for x in self.w)
        self.B = [e for e in itertools.product(*[range(m - 1) for m in self.n])
                  if deg(e, self.w) == self.d]
        self.index = {b: i for i, b in enumerate(self.B)}
    def cls(self, e):
        """the character of x^e: e modulo n, up to adding multiples of (1,...,1)"""
        return min(tuple((a + k) % m for a, m in zip(e, self.n)) for k in range(self.d))
    def neg(self, c): return self.cls(tuple(-a for a in c))
    def lam(self, e, value):
        """socle functional on x^e, deg e = 3d, normalised by lam(x^{n-2}) = 1:
        e in sector r (e_i = n_i - 2 - r + n_i k_i) gives psi^r prod w_i^{k_i}, else 0"""
        for r in range(self.d):
            k = [(a - (m - 2 - r)) for a, m in zip(e, self.n)]
            if all(x % m == 0 for x, m in zip(k, self.n)):
                k = [x // m for x, m in zip(k, self.n)]
                if min(k) < 0 or sum(k) != r: return 0
                v = value ** r
                for wi, ki in zip(self.w, k): v *= wi ** ki
                return v
        return 0

def rref(rows):
    """reduced row echelon form over Q; returns the rows and the pivot columns"""
    M = [[Fraction(x) for x in r] for r in rows]
    piv, rk = [], 0
    for col in range(len(M[0]) if M else 0):
        p = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        inv = 1 / M[rk][col]
        M[rk] = [x * inv for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        piv.append(col); rk += 1
    return M[:rk], piv

def rank(rows): return len(rref(rows)[1])

def nullspace(rows):
    R, piv = rref(rows)
    free = [j for j in range(len(rows[0])) if j not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * len(rows[0]); v[f] = Fraction(1)
        for r, p in zip(R, piv): v[p] = -r[f]
        basis.append(v)
    return basis

def monomials(w, D):
    """all exponent vectors e with sum w_i e_i = D"""
    def rec(i, left):
        if i == len(w) - 1:
            if left % w[i] == 0: yield (left // w[i],)
            return
        for a in range(left // w[i] + 1):
            for rest in rec(i + 1, left - a * w[i]): yield (a,) + rest
    return list(rec(0, D))

def esym(w, k): return sum(sp.prod(c) for c in itertools.combinations(w, k))

# hand lists of the labels that share a character (Proposition on coinciding labels)
def mono(*pairs):
    e = [0] * 5
    for i, a in pairs: e[i] += a
    return tuple(e)

def predicted_classes(name):
    P = []
    Q = range(4)
    if name == 'sextic':
        for i in Q:
            j, k, l = [t for t in Q if t != i]
            P.append({mono((i, 4), (4, 1)), mono((j, 2), (k, 2), (l, 2))})
        for i, j in itertools.combinations(Q, 2):
            k, l = [t for t in Q if t not in (i, j)]
            if i == 0: P.append({mono((i, 3), (j, 3)), mono((k, 3), (l, 3))})
    elif name == 'octic':
        for i, j in itertools.permutations(Q, 2):
            k, l = [t for t in Q if t not in (i, j)]
            P.append({mono((i, 6), (j, 2)), mono((j, 4), (k, 2), (l, 2))})
        for i in Q:
            for j, k in itertools.combinations([t for t in Q if t != i], 2):
                (l,) = [t for t in Q if t not in (i, j, k)]
                P.append({mono((i, 6), (j, 1), (k, 1)), mono((j, 3), (k, 3), (l, 2))})
        for i, j in itertools.combinations(Q, 2):
            k, l = [t for t in Q if t not in (i, j)]
            if i == 0: P.append({mono((i, 4), (j, 4)), mono((k, 4), (l, 4))})
    elif name == 'dectic':
        T = range(3)
        pairs = []
        for b in itertools.product(range(5), repeat=3):          # k = 2, b_4 = 3
            if sum(b) == 4: pairs.append((mono((0, b[0]), (1, b[1]), (2, b[2]), (3, 3)),
                                          mono((0, b[0] + 2), (1, b[1] + 2), (2, b[2] + 2))))
        for i in T:
            j, k = [t for t in T if t != i]
            pairs.append((mono((i, 8), (3, 1)), mono((j, 2), (k, 2), (3, 3))))
            pairs.append((mono((i, 8), (j, 1), (k, 1)), mono((j, 3), (k, 3), (3, 2))))
            pairs.append((mono((i, 8), (3, 1)), mono((i, 2), (j, 4), (k, 4))))       # k = 4
            pairs.append((mono((i, 6), (j, 1), (k, 1), (3, 1)), mono((j, 5), (k, 5))))
            pairs.append((mono((i, 6), (3, 2)), mono((j, 4), (k, 4), (3, 1))))
            for j in [t for t in T if t != i]:
                (k,) = [t for t in T if t not in (i, j)]
                pairs.append((mono((i, 8), (j, 2)), mono((j, 4), (k, 2), (3, 2))))
                pairs.append((mono((i, 6), (j, 2), (3, 1)), mono((j, 6), (k, 4))))
                pairs.append((mono((i, 7), (j, 1), (3, 1)), mono((i, 1), (j, 5), (k, 4))))
        check('dectic: 27 pairs at shift 2 and 21 at shift 4 in the hand list',
              len(pairs) == 48 and len(set(map(frozenset, pairs))) == 48)
        # classes: connected components of the graph of the pairs
        comp = {}
        for a, b in pairs:
            ca, cb = comp.get(a, {a}), comp.get(b, {b})
            u = ca | cb
            for x in u: comp[x] = u
        P = list({frozenset(c) for c in comp.values()})
    return {frozenset(p) for p in P}

def predicted_missing(F):
    out = set()
    if F.name == 'sextic':
        for p in itertools.permutations((0, 1, 3, 4)): out.add(F.cls(p + (2,)))
    elif F.name == 'octic':
        for p in itertools.permutations((0, 2, 4, 6)): out.add(F.cls(p + (1,)))
    elif F.name == 'quintic':
        for p in itertools.permutations(range(5)): out.add(F.cls(p))
    return out

def reduce_monomial(F, e):
    """apply x_i^{n_i-1} -> w_i psi prod_{j != i} x_j until the exponent is a label;
    returns (label, power of psi, factor) or None"""
    r, c = 0, 1
    for _ in range(4):
        if e in F.index: return e, r, c
        big = [i for i in range(5) if e[i] >= F.n[i] - 1]
        if len(big) != 1: return None
        i = big[0]
        e = tuple(a - (F.n[i] - 1) if j == i else a + 1 for j, a in enumerate(e))
        r, c = r + 1, c * F.w[i]
    return None

EXPECT = {  # |B|, chi, |Gamma|, characters, class sizes, missing, rank, rank at 0
    'quintic': (101, -200, 125, 101, {}, 24, 101, 51),
    'sextic': (103, -204, 108, 96, {2: 7}, 12, 99, 44),
    'octic': (149, -296, 128, 122, {2: 27}, 6, 125, 85),
    'dectic': (145, -288, 100, 100, {2: 39, 3: 3}, 0, 109, 72)}

for name in ['sextic', 'octic', 'dectic', 'quintic']:
    F = Family(name); d, w, n, B = F.d, F.w, F.n, F.B
    nB, chi_e, nG, nchar, sizes_e, nmiss, rk_e, rk0_e = EXPECT[name]
    L3 = Fraction(d, int(sp.prod(w)))
    chi = (esym(w, 3) - d * esym(w, 2)) * L3
    C = defaultdict(list)
    for b in B: C[F.cls(b)].append(b)
    K = {F.cls(e) for e in itertools.product(*[range(m) for m in n]) if deg(e, w) % d == 0}
    sizes = Counter(len(v) for v in C.values() if len(v) > 1)
    h = [b for b in B if F.cls(b) == F.cls((0,) * 5)]
    if name == 'quintic':
        miss = K - set(C)
        Mq = [[F.lam(add(h[0], b, c), Fraction(3, 7)) for c in B] for b in B]
        M0 = [[F.lam(add(h[0], b, c), 0) for c in B] for b in B]
        check('quintic through the same code: 101 labels, 101 characters of 125, the 24 '
              'missing ones the permutations, mass map rank 101 at psi = 3/7 and 51 at psi = 0',
              len(B) == 101 and len(C) == 101 and len(K) == 125 and miss == predicted_missing(F)
              and rank(Mq) == 101 and rank(M0) == 51)
        continue

    check(f'{name}: chi = (s3 - d s2) d/prod w = {chi_e}, h21 = 1 - chi/2 = |B| = {nB}',
          chi == chi_e and 1 - chi / 2 == nB == len(B), f'L^3 = {L3}')
    # the discriminant: a singular point exists when psi^d prod w^w = 1
    xs = sp.symbols('x1:6')
    P0 = {'sextic': (2 ** sp.Rational(-1, 3), (1, 1, 1, 1, 2 ** sp.Rational(1, 3))),
          'octic': (sp.Rational(1, 2), (1, 1, 1, 1, 2)),
          'dectic': (2 ** sp.Rational(-1, 5) / sp.sqrt(5), (1, 1, 1, 2 ** sp.Rational(1, 5), sp.sqrt(5)))}
    p0, pt = P0[name]
    Fp = sum(x ** m for x, m in zip(xs, n)) - d * p0 * sp.prod(xs)
    grad = [sp.simplify(sp.diff(Fp, x).subs(dict(zip(xs, pt)))) for x in xs]
    check(f'{name}: at psi_0 with psi_0^{d} prod w^w = 1 the point {pt} is singular',
          sp.simplify(p0 ** d * sp.prod([sp.Integer(x) ** x for x in w]) - 1) == 0
          and all(g == 0 for g in grad))
    # reduction lemma: every monomial of degree d reduces to a label in at most two steps
    allmon = monomials(w, d)
    red = [reduce_monomial(F, e) for e in allmon]
    check(f'{name}: each of the {len(allmon)} monomials of degree {d} reduces to w psi^r x^b, '
          f'b a label, r <= 2, at most one exponent >= n_i - 1',
          all(x is not None and x[1] <= 2 for x in red)
          and all(sum(e[i] >= n[i] - 1 for i in range(5)) <= 1 for e in allmon))
    check(f'{name}: |Gamma| = {nG}, the labels carry {nchar} characters, coinciding in '
          f'{sum(sizes.values())} classes',
          len(K) == nG == int(sp.prod(n)) // d ** 2 and len(C) == nchar and dict(sizes) == sizes_e,
          dict(sizes))
    coll = {frozenset(v) for v in C.values() if len(v) > 1}
    check(f'{name}: the labels that share a character are exactly those of the hand list',
          coll == predicted_classes(name))
    miss = K - set(C)
    neg_ok = all(F.neg(c) in C for c in C) and all(F.neg(c) in miss for c in miss)
    pm = predicted_missing(F)
    allrep = all(any(e[i] == n[i] - 1 for i in range(5))
                 for c in miss for e in [tuple((a + k) % m for a, m in zip(c, n)) for k in range(d)])
    check(f'{name}: {nmiss} characters do not occur, each representative has an entry n_i - 1'
          + ('' if nmiss == 0 else ', and they are the classes of the hand list')
          + '; occurring and missing sets closed under negation',
          len(miss) == nmiss and neg_ok and allrep and (pm == miss if nmiss else True))
    # sectors of the socle functional
    top = monomials(w, 3 * d)
    triv = [e for e in top if F.cls(e) == F.cls((0,) * 5)]
    insec = [e for e in top if F.lam(e, 2) != 0]
    check(f'{name}: of the {len(top)} monomials of degree {3*d}, the {len(triv)} with trivial '
          f'character are exactly those in a sector r < {d}', set(triv) == set(insec))
    # mass map of the invariant label
    hb = h[0]
    check(f'{name}: the invariant label is {hb}', len(h) == 1)
    def block_entries(val):
        return [[F.lam(add(hb, b, c), val) for c in B] for b in B]
    Mq = block_entries(Fraction(3, 7)); Mm = block_entries(Fraction(-2))
    M0 = block_entries(0)
    rq, rm, r0 = rank(Mq), rank(Mm), rank(M0)
    n0 = sum(all(b[i] <= n[i] - 2 - hb[i] for i in range(5)) for b in B)
    check(f'{name}: mass map of h has rank {rk_e} at psi = 3/7 and psi = -2, and rank {rk0_e} '
          f'= #(b <= n - 2 - h) at psi = 0', rq == rm == rk_e and r0 == rk0_e == n0)
    # kernel at psi = 3/7 lies in the span of the coinciding labels
    ker = nullspace(Mq)
    collab = {b for c in coll for b in c}
    supp_ok = all(all(v[i] == 0 for i in range(len(B)) if B[i] not in collab) for v in ker)
    check(f'{name}: the {len(B) - rk_e} massless directions at psi = 3/7 lie in the span of '
          f'the {len(collab)} coinciding labels', len(ker) == len(B) - rk_e and supp_ok)
    # blocks: one for each pair {chi, -chi}; generic rank, determinants
    seen, ok_blocks, dets, types = set(), True, [], Counter()
    disc = sp.prod([sp.Integer(x) ** x for x in w]) * psi ** d - 1
    for c in sorted(C):
        if c in seen: continue
        cn = F.neg(c); seen |= {c, cn}
        A = sp.Matrix(len(C[c]), len(C[cn]),
                      lambda i, j: F.lam(add(hb, C[c][i], C[cn][j]), psi))
        rk = A.rank(simplify=True)
        if any(a == 0 for a in A): ok_blocks = False
        types[(A.shape, c == cn, rk)] += 1
        if A.shape[0] == A.shape[1] and rk == A.shape[0]:
            dt = sp.factor(A.det())
            dets.append(dt)
            for fac, _ in sp.factor_list(dt, psi)[1]:
                if not (fac == psi or sp.Poly(disc, psi).rem(sp.Poly(fac, psi)).is_zero):
                    ok_blocks = False
        elif rk != 1:
            ok_blocks = False
    check(f'{name}: every block entry is a nonzero monomial in psi; blocks of full size have '
          f'determinant c psi^a (prod w^w psi^{d} - 1)^j; the other blocks have rank one',
          ok_blocks, dict((f'{s[0]}x{s[1]}{"s" if sd else ""} r{r}', v) for (s, sd, r), v in types.items()))
    # Riemann-Roch integrality on a free quotient Y = X/H with three net families
    c2L = esym(w, 2) * L3
    if (-chi) % 6:
        check(f'{name}: |chi|/6 = {-chi}/6 is not an integer, so no free quotient has three families',
              True)
    else:
        H = int(-chi) // 6
        good = []
        for m in range(1, H + 1):
            if H % m: continue
            D3 = Fraction(m ** 3) * L3 / H; c2D = m * c2L / H
            if D3.denominator == 1 and c2D.denominator == 1:
                good.append((m, D3 / 6 + c2D / 12))
        check(f'{name}: three families needs |H| = {H}; the m_0 with D^3, c2.D integral are '
              f'{[g[0] for g in good]}, and chi(O(D)) = D^3/6 + c2.D/12 is never an integer',
              len(good) > 0 and all(Fraction(g[1]).denominator != 1 for g in good),
              ', '.join(f'm0={g[0]}: {g[1]}' for g in good))
    if name == 'octic':
        Mh = block_entries(Fraction(1, 2))
        check('octic: at the singular member psi = 1/2 the rank drops to 122', rank(Mh) == 122)

print(f'{passes} checks passed, {fails} failed')
if fails: raise SystemExit(1)
