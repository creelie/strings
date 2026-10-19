-- The Jacobian rings of the weighted Fermat pencils F = sum x_i^{n_i} - d psi x_1...x_5:
-- the sextic in P(1,1,1,1,2), the octic in P(1,1,1,1,4), the dectic in P(1,1,1,2,5),
-- at psi = 1/3 and psi = -2.  Checks that the Jacobian ring is finite of dimension
-- prod (n_i - 1) (so the member is smooth), that the labels b (b_i <= n_i - 2, degree d)
-- form a basis of R_d, that R_{3d} is spanned by m0 = x^{n-2}, and the socle functional
-- on every monomial of degree 3d: psi^r prod w_i^{k_i} m0 in sector r
-- (e_i = n_i - 2 - r + n_i k_i), zero outside the sectors.   Run: M2 --script weighted.m2
fails = 0; passes = 0;
chk = (name, ok) -> (
    if ok then (passes = passes + 1; print("PASS " | name))
    else (fails = fails + 1; print("FAIL " | name)));
families = {("sextic", 6, {1,1,1,1,2}), ("octic", 8, {1,1,1,1,4}), ("dectic", 10, {1,1,1,2,5})};
sector = (e, n, w, d) -> (
    -- returns (r, k) with e_i = n_i - 2 - r + n_i k_i, k_i >= 0, sum k = r, or null
    result := null;
    for r from 0 to d - 1 do (
        if result === null and all(5, i -> (e#i - (n#i - 2 - r)) % (n#i) == 0) then (
            k := apply(5, i -> (e#i - (n#i - 2 - r)) // (n#i));
            if all(k, a -> a >= 0) and sum k == r then result = (r, k)));
    result);
for fam in families do (
    name := fam#0; d := fam#1; w := fam#2;
    n := apply(w, a -> d // a);
    R := QQ[x_1..x_5, Degrees => w];
    m0 := product(5, i -> x_(i+1)^(n#i - 2));
    labels := select(flatten entries basis(d, R), m -> all(5, i -> (first exponents m)#i <= n#i - 2));
    for psi in {1/3, -2} do (
        F := sum(5, i -> x_(i+1)^(n#i)) - d*psi*product(5, i -> x_(i+1));
        J := ideal apply(5, i -> diff(x_(i+1), F));
        A := R/J;
        tag := name | ", psi = " | toString psi | ": ";
        chk(tag | "dim R = prod(n_i - 1) = " | toString product(n, a -> a - 1)
            | ", dim R_d = " | toString(#labels) | ", dim R_3d = 1",
            dim A == 0 and numgens source basis A == product(n, a -> a - 1)
            and numgens source basis(d, A) == #labels and numgens source basis(3*d, A) == 1);
        nf := matrix {apply(labels, m -> m % J)};
        (mons, cf) := coefficients nf;
        chk(tag | "the " | toString(#labels) | " labels are independent in R_d", rank cf == #labels);
        n0 := m0 % J;
        top := flatten entries basis(3*d, R);
        bad := 0; insec := 0;
        for m in top do (
            e := first exponents m;
            s := sector(e, n, w, d);
            expected := if s === null then 0_R else (
                insec = insec + 1;
                psi^(s#0) * product(5, i -> (w#i)^((s#1)#i)) * n0);
            if (m % J) != expected then bad = bad + 1);
        chk(tag | "socle functional on all " | toString(#top) | " monomials of degree "
            | toString(3*d) | " (" | toString insec | " in sectors), m0 nonzero",
            bad == 0 and n0 != 0);
        ));
print(toString passes | " checks passed, " | toString fails | " failed");
if fails > 0 then exit 1;
