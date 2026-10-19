"""Checks for 'Which String Vibrations Become Which Generations on the Dwork Quintic'.
Every statement of Theorems 1 to 3 and of the Fermat section that involves a finite
computation is recomputed here, and the intersection numbers of Appendix C are checked
against the Seifert form of the Pham cycle.  Run: python3 verify.py"""
import itertools, math
import numpy as np
from collections import Counter
import sympy as sp
import mpmath as mp

passes = fails = 0
def check(name, ok, info=''):
    global passes, fails
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else ''))
    if ok: passes += 1
    else: fails += 1

def comps(t, n, m):
    if n == 1:
        if t <= m: yield (t,)
        return
    for a in range(min(t, m) + 1):
        for r in comps(t - a, n - 1, m): yield (a,) + r

B = sorted(comps(5, 5, 3))
check('101 labels b in {0..3}^5 with |b|=5', len(B) == 101)
def cls(v): # class of v in (Z/5)^5 / <1>, normalised so that the last entry is 0
    return tuple((x - v[-1]) % 5 for x in v)
chars = [cls(b) for b in B]
check('the 101 characters are distinct', len(set(chars)) == 101)
allchars = {cls(v) for v in itertools.product(range(5), repeat=5) if sum(v) % 5 == 0}
check('the character group has 125 elements', len(allchars) == 125)
missing = allchars - set(chars)
perms = {cls(p) for p in itertools.permutations(range(5))}
check('the 24 missing characters are the classes of permutations of (0,1,2,3,4)', missing == perms and len(missing) == 24)
orb = Counter(tuple(sorted(b, reverse=True)) for b in B)
check('S5-orbits of sizes 1, 20, 20, 30, 30', sorted(orb.values()) == [1, 20, 20, 30, 30], dict(orb))

def sector(e):
    s = {x % 5 for x in e}
    return (3 - s.pop()) % 5 if len(s) == 1 else None
cnt = Counter(); n = 0
for i in range(101):
    for j in range(i, 101):
        for k in range(j, 101):
            r = sector(tuple(B[i][t] + B[j][t] + B[k][t] for t in range(5)))
            if r is not None: cnt[r] += 1; n += 1
check('1431 unordered triples with a nonzero coupling', n == 1431)
check('566, 425, 280, 160 of them with r = 0, 1, 2, 3', [cnt[r] for r in range(4)] == [566, 425, 280, 160])
check('no sector 4 (exponents would be at least four each)', cnt[4] == 0)
excl = [(a, b) for a in B for b in B if len({(a[t] + b[t]) % 5 for t in range(5)}) == 5]
per = Counter(tuple(a[t] + b[t] for t in range(5)) for a, b in excl)
check('excluded ordered pairs: a+b is a permutation of (0,1,2,3,4), 16 pairs for each, 1920 in all',
      len(excl) == 1920 and set(per.values()) == {16} and len(per) == 120)
t = sp.symbols('t')
check('coefficient of t^5 in (1+t)(1+t+t^2)(1+t+t^2+t^3)(t+t^2+t^3) is 16',
      sp.Poly(sp.expand((1+t)*(1+t+t**2)*(1+t+t**2+t**3)*(t+t**2+t**3)), t).coeff_monomial(t**5) == 16)
two = sum(1 for a in B for c in B if a != c and sector(tuple(2*a[x] + c[x] for x in range(5))) is not None)
check('ordered (a,a,c) with c != a: 100; unordered count 7980/6 + 100 + 1 = 1431',
      two == 100 and (10201 - 1920 - 3*100 - 1) == 7980 and 7980 // 6 + 100 + 1 == 1431)

one = (1, 1, 1, 1, 1)
partners = {}
for b in B:
    ps = [(c, sector(tuple(b[x] + c[x] + 1 for x in range(5)))) for c in B]
    ps = [(c, r) for c, r in ps if r is not None]
    partners[b] = ps
check('every label has exactly one partner under h', all(len(v) == 1 for v in partners.values()))
sigma = {b: v[0][0] for b, v in partners.items()}
check('sigma is an involution with one fixed point (1,1,1,1,1)',
      all(sigma[sigma[b]] == b for b in B) and [b for b in B if sigma[b] == b] == [one])
pw = Counter(v[0][1] for v in partners.values())
check('powers of psi on the pairing: 51 ones, 30 psi, 20 psi^2', pw == Counter({0: 51, 1: 30, 2: 20}), dict(pw))
check('determinant exponent 30*1 + 20*2 = 70 and rank 51 at psi = 0',
      sum(v[0][1] for v in partners.values()) == 70 and pw[0] == 51)
check('the 50 labels with an exponent three are exactly those paired with a power of psi',
      {b for b in B if 3 in b} == {b for b in B if partners[b][0][1] > 0})

psi = sp.symbols('psi'); x = sp.symbols('x1:6')
F = sum(v**5 for v in x) - 5*psi*sp.prod(x)
Hm = sp.Matrix(5, 5, lambda i, j: sp.diff(F, x[i], x[j]))
H = sp.Poly(sp.expand(Hm.det(method='berkowitz')), *x)
val = 0
for e, c in H.terms():
    r = sector(e)
    if r is not None: val += c * psi**r
check('Hessian in the socle: 3,200,000 (1 - psi^5) times x1^3...x5^3', sp.expand(val - 3200000*(1 - psi**5)) == 0)

mp.mp.dps = 30
G = lambda k: mp.gamma(mp.mpf(k)/5) / mp.gamma(1 - mp.mpf(k)/5)
def g(b): return mp.fprod(G(bi + 1) for bi in b)
check('Hodge norms are invariant under sigma (same multiset of k)', all(abs(g(b) - g(sigma[b])) < mp.mpf(10)**-20 for b in B))
m1 = 1 / g(one); m2 = 1 / g((2, 1, 1, 1, 0)); m3 = 1 / g((2, 2, 1, 0, 0))
r2 = m2 / m1; r3 = m3 / m1
print(f'  masses at the Fermat point relative to the singlet: 1, {mp.nstr(r2, 6)}, {mp.nstr(r3, 6)}')
check('mass ratios 0.8381 and 0.7023', abs(r2 - mp.mpf('0.838054')) < 1e-5 and abs(r3 - mp.mpf('0.702335')) < 1e-5)
# Appendix C: the Seifert form of y1^5 + ... + y4^5 on the Milnor lattice, by Sebastiani-Thom
L1 = -np.eye(4) + np.diag(np.ones(3), 1)      # one variable, in the basis T^j e0, j = 0..3
T1 = np.zeros((4, 4))
for j in range(3): T1[j + 1, j] = 1
T1[:, 3] = -1                                    # T^4 = -(1 + T + T^2 + T^3)
def kron(ms):
    M = ms[0]
    for m_ in ms[1:]: M = np.kron(M, m_)
    return M
L = kron([L1] * 4); Q = -L + L.T
Ts = [kron([T1 if j == i else np.eye(4) for j in range(4)]) for i in range(4)]
check('the intersection form Q = -L + L^T is invariant under the four monodromies',
      all(np.allclose(T.T @ Q @ T, Q) for T in Ts))
e0 = kron([np.array([[1.], [0], [0], [0]])] * 4)[:, 0]
orbit = np.zeros((5, 5, 5, 5, 256))
for a in itertools.product(range(5), repeat=4):
    v = e0.copy()
    for i in range(4):
        for _ in range(a[i]): v = Ts[i] @ v
    orbit[a] = v
U = np.fft.fftn(orbit, axes=(0, 1, 2, 3)) / 625
z = np.exp(2j * np.pi / 5); ratios = []
for k in itertools.product(range(1, 5), repeat=4):
    k5 = (-sum(k)) % 5
    if k5 == 0: continue
    u = U[k]
    ratios.append(abs(u @ Q @ np.conj(u)) / (np.prod([abs(1 - z**ki) for ki in list(k) + [k5]]) / 5**4))
check('|Q(u, conj u)| = 5^-4 prod |1 - zeta^k_i| for the 204 eigencomponents of the Pham cycle',
      len(ratios) == 204 and max(abs(r - 1) for r in ratios) < 1e-9)
check('Gamma(1/5), Gamma(2/5), Gamma(3/5), Gamma(4/5) = 4.59084, 2.21816, 1.48919, 1.16423',
      all(abs(mp.gamma(mp.mpf(j) / 5) - v) < 5e-6 for j, v in ((1, 4.59084), (2, 2.21816), (3, 1.48919), (4, 1.16423))))
f5 = lambda j: mp.gamma(mp.mpf(j) / 5)
kap2 = f5(3)**3 * f5(1) / (f5(2)**3 * f5(4))
check('kappa^2 = 1.19324 (Distler-Greene), the ratio of the second Hodge norm to the first',
      abs(kap2 - mp.mpf('1.19324')) < 5e-6 and abs(g((2, 1, 1, 1, 0)) / g(one) - kap2) < 1e-20)
check('Weil-Petersson metric at the Fermat point 25 gamma(2/5)^5/gamma(1/5)^5 = 0.19226',
      abs(25 * G(2)**5 / G(1)**5 - mp.mpf('0.19226')) < 5e-6)
print(f'{passes} checks passed, {fails} failed')
