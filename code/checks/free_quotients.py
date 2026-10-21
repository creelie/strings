"""Checks for the table and the proposition on free quotients of 'Which String
Vibrations Become Which Generations on the Dwork Quintic': the thirteen one-parameter
complete intersections,
their intersection numbers and Euler characteristics from the Chern classes of the
ambient weighted space, the values chi(X, kL) by Riemann-Roch, their greatest common
divisor g_X, and the arithmetic showing that no free quotient carries three net
families.  Exact rational arithmetic only.  Run: python3 free_quotients.py"""
from fractions import Fraction
from math import gcd, prod

passes = fails = 0
def check(name, ok, info=''):
    global passes, fails
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else ''))
    if ok: passes += 1
    else: fails += 1

def primes(n):
    out, p = set(), 2
    while p * p <= n:
        while n % p == 0: out.add(p); n //= p
        p += 1
    if n > 1: out.add(n)
    return out

# type: (degrees, weights), and the row of the table: L^3, c2.L, chi, chi(kL) k=1..3, g_X, |chi|/6
ROWS = {
    'X5':      ((5,), (1,)*5,                 5, 50, -200, (5, 15, 35), 5, None),
    'X6':      ((6,), (1,)*4 + (2,),          3, 42, -204, (4, 11, 24), 1, 34),
    'X8':      ((8,), (1,)*4 + (4,),          2, 44, -296, (4, 10, 20), 2, None),
    'X10':     ((10,), (1,)*3 + (2, 5),       1, 34, -288, (3, 7, 13), 1, 48),
    'X3,3':    ((3, 3), (1,)*6,               9, 54, -144, (6, 21, 54), 3, 24),
    'X4,2':    ((4, 2), (1,)*6,               8, 56, -176, (6, 20, 50), 2, None),
    'X3,2,2':  ((3, 2, 2), (1,)*7,           12, 60, -144, (7, 26, 69), 1, 24),
    'X2,2,2,2':((2, 2, 2, 2), (1,)*8,        16, 64, -128, (8, 32, 88), 8, None),
    'X4,4':    ((4, 4), (1,)*4 + (2, 2),      4, 40, -144, (4, 12, 28), 4, 24),
    'X6,6':    ((6, 6), (1, 1, 2, 2, 3, 3),   1, 22, -120, (2, 5, 10), 1, 20),
    'X4,3':    ((4, 3), (1,)*5 + (2,),        6, 48, -156, (5, 16, 39), 1, 26),
    'X6,4':    ((6, 4), (1, 1, 1, 2, 2, 3),   2, 32, -156, (3, 8, 17), 1, 26),
    'X6,2':    ((6, 2), (1,)*5 + (3,),        4, 52, -256, (5, 14, 31), 1, None),
}

def series(ws, ds, n=4):
    """coefficients of prod(1 + w h) / prod(1 + d h) up to h^3"""
    c = [Fraction(1)] + [Fraction(0)] * (n - 1)
    for w in ws:
        c = [c[i] + (w * c[i - 1] if i else 0) for i in range(n)]
    for d in ds:   # multiply by 1/(1 + d h) = sum (-d h)^k
        inv = [Fraction((-d) ** k) for k in range(n)]
        c = [sum(c[i] * inv[k - i] for i in range(k + 1)) for k in range(n)]
    return c

trivial, pgroups = [], {}
for name, (ds, ws, L3, c2L, chi, vals, gX, order) in ROWS.items():
    check(f'{name}: Calabi-Yau condition sum d = sum w', sum(ds) == sum(ws))
    deg = Fraction(prod(ds), prod(ws))
    c = series(ws, ds)
    check(f'{name}: c1 = 0', c[1] == 0)
    got = (deg, c[2] * deg, c[3] * deg)
    check(f'{name}: L^3, c2.L, chi', got == (L3, c2L, chi), f'{tuple(map(str, got))}')
    rr = tuple(Fraction(k**3 * L3, 6) + Fraction(k * c2L, 12) for k in (1, 2, 3))
    check(f'{name}: chi(kL) for k = 1, 2, 3 by Riemann-Roch', rr == vals, str(tuple(map(str, rr))))
    # alpha_i of f(k) = a1 C(k,1) + a2 C(k,2) + a3 C(k,3): forward differences at 0
    f = [Fraction(0)] + list(rr)
    a1, a2, a3 = f[1] - f[0], f[2] - 2 * f[1] + f[0], f[3] - 3 * f[2] + 3 * f[1] - f[0]
    ok = all(x.denominator == 1 for x in (a1, a2, a3))
    g = gcd(gcd(int(a1), int(a2)), int(a3)) if ok else 0
    check(f'{name}: g_X = gcd of the binomial coefficients = gcd of chi(kL), k <= 3',
          ok and g == gX == gcd(gcd(*map(int, vals[:2])), int(vals[2])), f'g_X = {g}')
    check(f'{name}: chi(kL) divisible by g_X for k <= 40',
          all((Fraction(k**3 * L3, 6) + Fraction(k * c2L, 12)) % gX == 0 for k in range(1, 41)))
    if gX == 1: trivial.append(name)
    else: pgroups[name] = primes(gX)
    six = Fraction(abs(chi), 6)
    if order is None:
        check(f'{name}: |chi|/6 is not an integer', six.denominator != 1, str(six))
    else:
        bad = sorted(primes(order) - primes(gX))
        check(f'{name}: |chi|/6 = {order} has a prime factor not dividing g_X',
              six == order and bool(bad), f'primes {bad}')

check('no free action on X6, X10, X3,2,2, X6,6, X4,3, X6,4, X6,2',
      sorted(trivial) == sorted(['X6', 'X10', 'X3,2,2', 'X6,6', 'X4,3', 'X6,4', 'X6,2']))
check('free actions by a 5-group on X5, a 3-group on X3,3, 2-groups on X8, X4,2, X2,2,2,2, X4,4',
      pgroups == {'X5': {5}, 'X3,3': {3}, 'X8': {2}, 'X4,2': {2}, 'X2,2,2,2': {2}, 'X4,4': {2}})
# quintic: orders of free groups divide 200 and are powers of 5, so 5 or 25; families |chi|/(2|H|)
fam = sorted(200 // (2 * h) for h in (5, 25))
check('a free quotient of the quintic has 20 or 4 net families', fam == [4, 20], str(fam))

print(f'{passes} checks passed, {fails} failed')
