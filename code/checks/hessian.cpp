// The Hessian of F = x1^5 + ... + x5^5 - 5 psi x1...x5 in the socle (Theorem 6, Table I,
// Appendix A).  The determinant is expanded over the 120 permutations; each term is a
// monomial of degree fifteen, reduced to psi^r m0 by the socle functional, and the terms
// are grouped by cycle type.  Build: c++ -O2 -std=c++17 hessian.cpp
#include <algorithm>
#include <array>
#include <cstdio>
#include <map>
#include <string>
#include <vector>

static int npass = 0, nfail = 0;
static void check(const std::string &name, bool ok) {
    std::printf("%s %s\n", ok ? "PASS" : "FAIL", name.c_str());
    (ok ? npass : nfail)++;
}

using Vec = std::array<int, 5>;

static int sector(const Vec &e) {  // e_i = 3 - r mod 5 for all i, or -1
    int s = e[0] % 5;
    for (int x : e) if (x % 5 != s) return -1;
    return ((3 - s) % 5 + 5) % 5;
}

int main() {
    Vec p = {0, 1, 2, 3, 4};
    // cycle type -> {number of permutations, sign, sorted exponent, r, coefficient of psi^(m+r)}
    struct Row { int count = 0, sign = 0, r = 0, power = 0; long long coef = 0; Vec mono{}; bool rule = true; };
    std::map<std::string, Row> rows;
    std::map<int, long long> H;  // power of psi -> coefficient of m0
    int nperm = 0;
    do {
        nperm++;
        Vec e = {0, 0, 0, 0, 0};
        int m = 0;
        long long coef = 1;
        for (int i = 0; i < 5; i++) {
            if (p[i] == i) { e[i] += 3; coef *= 20; }
            else {
                m++; coef *= -5;
                for (int k = 0; k < 5; k++) if (k != i && k != p[i]) e[k] += 1;
            }
        }
        // sign and cycle type
        std::array<bool, 5> seen{};
        std::vector<int> cyc;
        for (int i = 0; i < 5; i++) if (!seen[i]) {
            int len = 0, j = i;
            while (!seen[j]) { seen[j] = true; j = p[j]; len++; }
            cyc.push_back(len);
        }
        std::sort(cyc.rbegin(), cyc.rend());
        int sign = 1;
        for (int len : cyc) if (len % 2 == 0) sign = -sign;
        std::string type;
        for (int len : cyc) type += char('0' + len);
        // the rule: fixed points x^(3+m), moved points x^(m-2)
        bool rule = true;
        for (int i = 0; i < 5; i++) rule = rule && (e[i] == (p[i] == i ? 3 + m : m - 2));
        int r = sector(e);
        long long c = sign * coef;
        Vec srt = e;
        std::sort(srt.rbegin(), srt.rend());
        Row &row = rows[type];
        row.count++; row.sign = sign; row.r = r; row.power = m + r; row.coef += c; row.mono = srt;
        row.rule = row.rule && rule;
        if (r >= 0) H[m + r] += c;
    } while (std::next_permutation(p.begin(), p.end()));

    check("120 permutations in 7 cycle types", nperm == 120 && rows.size() == 7);
    bool rule = true;
    for (auto &kv : rows) rule = rule && kv.second.rule;
    check("monomial of a permutation with m moved points: x^(3+m) at fixed, x^(m-2) at moved points", rule);

    struct Expect { const char *type; int count, sign; Vec mono; int r; long long contrib; };
    const Expect table[] = {
        {"11111", 1, +1, {3, 3, 3, 3, 3}, 0, 3200000},
        {"2111", 10, -1, {5, 5, 5, 0, 0}, 3, -2000000},
        {"311", 20, +1, {6, 6, 1, 1, 1}, 2, -1000000},
        {"41", 30, -1, {7, 2, 2, 2, 2}, 1, -375000},
        {"5", 24, +1, {3, 3, 3, 3, 3}, 0, -75000},
        {"221", 15, +1, {7, 2, 2, 2, 2}, 1, 187500},
        {"32", 20, -1, {3, 3, 3, 3, 3}, 0, 62500},
    };
    bool tab = true;
    for (const Expect &x : table) {
        const Row &row = rows[x.type];
        bool ok = row.count == x.count && row.sign == x.sign && row.mono == x.mono && row.r == x.r &&
                  row.coef == x.contrib && (row.power == 0 || row.power == 5);
        std::printf("   %-6s %3d %+d (%d,%d,%d,%d,%d) r=%d  %lld psi^%d\n", x.type, row.count, row.sign,
                    row.mono[0], row.mono[1], row.mono[2], row.mono[3], row.mono[4], row.r, row.coef, row.power);
        tab = tab && ok;
    }
    check("Table I: counts, signs, monomials, sectors and contributions of the seven cycle types", tab);
    long long c5 = 0;
    for (const Expect &x : table) if (x.r >= 0 && std::string(x.type) != "11111") c5 += x.contrib;
    check("the psi^5 contributions add up to -3,200,000", c5 == -3200000);
    check("Hess F = 3,200,000 (1 - psi^5) m0 in the socle",
          H.size() == 2 && H[0] == 3200000 && H[5] == -3200000);
    std::printf("%d checks passed, %d failed\n", npass, nfail);
    return nfail != 0;
}
