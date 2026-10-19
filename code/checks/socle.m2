-- The Jacobian ring of the Dwork pencil at two rational values of psi.
-- Checks dim R_5 = 101, dim R_15 = 1, the socle functional on all 3876 monomials of
-- degree fifteen (psi^r in sector r, zero outside the sectors), and
-- Hess F = 3200000 (1 - psi^5) m0 in R_15.   Run: M2 --script socle.m2
R = QQ[x_1..x_5];
m0 = product(5, i -> x_(i+1)^3);
sector = e -> (
    s := unique apply(e, a -> a % 5);
    if #s == 1 then (3 - s#0) % 5 else -1);
fails = 0; passes = 0;
chk = (name, ok) -> (
    if ok then (passes = passes + 1; print("PASS " | name))
    else (fails = fails + 1; print("FAIL " | name)));
for psi in {2, 1/3} do (
    F := sum(5, i -> x_(i+1)^5) - 5*psi*product(5, i -> x_(i+1));
    J := ideal apply(5, i -> diff(x_(i+1), F));
    A := R/J;
    chk("psi = " | toString psi | ": dim R_5 = 101, dim R_15 = 1, dim R_16 = 0",
        numgens source basis(5, A) == 101 and numgens source basis(15, A) == 1
        and numgens source basis(16, A) == 0);
    n0 := m0 % J;
    chk("psi = " | toString psi | ": m0 is nonzero in R_15", n0 != 0);
    mons := flatten entries basis(15, R);
    bad := 0; insector := 0;
    for m in mons do (
        e := first exponents m;
        r := sector e;
        expected := if r >= 0 then psi^r * n0 else 0_R;
        if r >= 0 then insector = insector + 1;
        if (m % J) != expected then bad = bad + 1);
    chk("psi = " | toString psi | ": socle functional on all " | toString(#mons)
        | " monomials of degree 15 (" | toString insector | " in sectors)", bad == 0);
    H := det matrix apply(5, i -> apply(5, j -> diff(x_(j+1), diff(x_(i+1), F))));
    chk("psi = " | toString psi | ": Hess F = 3200000 (1 - psi^5) m0 in R_15",
        (H % J) == 3200000*(1 - psi^5)*n0);
    );
print(toString passes | " checks passed, " | toString fails | " failed");
if fails > 0 then exit 1;
