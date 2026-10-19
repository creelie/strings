/* Labels, couplings and the mass map of the Dwork quintic (Theorems 1 to 3).
 * Every count of Sections III, V and VI and of Appendix B is recomputed by
 * enumeration over the 101 exponent vectors.  Build: cc -O2 labels.c */
#include <stdio.h>
#include <string.h>

static int B[101][5], nB = 0, npass = 0, nfail = 0;

static void check(const char *name, int ok) {
    printf("%s %s\n", ok ? "PASS" : "FAIL", name);
    if (ok) npass++; else nfail++;
}

/* class of v in (Z/5)^5/<1>, normalised so that the last entry is 0, as an integer 0..124 */
static int cls(const int *v) {
    int c = 0;
    for (int i = 0; i < 3; i++) c = 5 * c + ((v[i] - v[4]) % 5 + 5) % 5;
    return c;
}

/* sector r of a vector of degree fifteen: all entries congruent to 3 - r mod 5; -1 otherwise */
static int sector(const int *e) {
    int s = ((e[0] % 5) + 5) % 5;
    for (int i = 1; i < 5; i++) if (((e[i] % 5) + 5) % 5 != s) return -1;
    return ((3 - s) % 5 + 5) % 5;
}

static int type_of(const int *b) { /* 0: 11111, 1: 21110, 2: 22100, 3: 31100, 4: 32000 */
    int c[4] = {0, 0, 0, 0};
    for (int i = 0; i < 5; i++) c[b[i]]++;
    if (c[1] == 5) return 0;
    if (c[3] == 0 && c[2] == 1) return 1;
    if (c[3] == 0 && c[2] == 2) return 2;
    if (c[3] == 1 && c[1] == 2) return 3;
    return 4;
}

int main(void) {
    int v[5];
    for (v[0] = 0; v[0] < 4; v[0]++) for (v[1] = 0; v[1] < 4; v[1]++)
    for (v[2] = 0; v[2] < 4; v[2]++) for (v[3] = 0; v[3] < 4; v[3]++)
    for (v[4] = 0; v[4] < 4; v[4]++)
        if (v[0] + v[1] + v[2] + v[3] + v[4] == 5) memcpy(B[nB++], v, sizeof v);
    check("101 labels b in {0,...,3}^5 with |b| = 5", nB == 101);

    int seen[125] = {0}, distinct = 1;
    for (int i = 0; i < nB; i++) { if (seen[cls(B[i])]) distinct = 0; seen[cls(B[i])] = 1; }
    check("the 101 labels carry 101 distinct characters", distinct);

    /* the permutations of (0,1,2,3,4) and their classes */
    int perm[120][5], np = 0, permcls[125] = {0};
    for (int a = 0; a < 5; a++) for (int b = 0; b < 5; b++) for (int c = 0; c < 5; c++)
    for (int d = 0; d < 5; d++) for (int e = 0; e < 5; e++) {
        int p[5] = {a, b, c, d, e}, used = 0, ok = 1;
        for (int i = 0; i < 5; i++) { if (used & (1 << p[i])) ok = 0; used |= 1 << p[i]; }
        if (ok) { memcpy(perm[np++], p, sizeof p); permcls[cls(p)] = 1; }
    }
    int nmiss = 0, match = 1, nperm = 0;
    for (int c = 0; c < 125; c++) {
        if (!seen[c]) nmiss++;
        if (permcls[c]) nperm++;
        if ((!seen[c]) != permcls[c]) match = 0;
    }
    check("24 characters missed, exactly the classes of the 120 permutations", np == 120 && nmiss == 24 && nperm == 24 && match);

    int orbit[5] = {0};
    for (int i = 0; i < nB; i++) orbit[type_of(B[i])]++;
    check("S5-orbits of sizes 1, 20, 30, 30, 20", orbit[0] == 1 && orbit[1] == 20 && orbit[2] == 30 && orbit[3] == 30 && orbit[4] == 20);

    /* ordered triples */
    long ordered = 0, bysec[5] = {0}, o33333 = 0, o72222 = 0, o66111 = 0, o55500 = 0;
    for (int i = 0; i < nB; i++) for (int j = 0; j < nB; j++) for (int k = 0; k < nB; k++) {
        int e[5];
        for (int t = 0; t < 5; t++) e[t] = B[i][t] + B[j][t] + B[k][t];
        int r = sector(e);
        if (r < 0) continue;
        ordered++; bysec[r]++;
        static const int E1[5] = {3, 3, 3, 3, 3}, E2[5] = {7, 2, 2, 2, 2}, E3[5] = {6, 6, 1, 1, 1}, E4[5] = {5, 5, 5, 0, 0};
        if (!memcmp(e, E1, sizeof e)) o33333++;
        if (!memcmp(e, E2, sizeof e)) o72222++;
        if (!memcmp(e, E3, sizeof e)) o66111++;
        if (!memcmp(e, E4, sizeof e)) o55500++;
    }
    check("8281 = 101^2 - 1920 ordered triples with a nonzero coupling", ordered == 8281);
    check("ordered counts 3391, 2400, 1620, 870 by sector, none in sector 4",
          bysec[0] == 3391 && bysec[1] == 2400 && bysec[2] == 1620 && bysec[3] == 870 && bysec[4] == 0);
    check("O(3,3,3,3,3) = 3391, O(7,2,2,2,2) = 480, O(6,6,1,1,1) = 162, O(5,5,5,0,0) = 87",
          o33333 == 3391 && o72222 == 480 && o66111 == 162 && o55500 == 87);

    long excl = 0;
    for (int i = 0; i < nB; i++) for (int j = 0; j < nB; j++) {
        int res = 0;
        for (int t = 0; t < 5; t++) res |= 1 << ((B[i][t] + B[j][t]) % 5);
        if (res == 31) excl++;
    }
    check("1920 excluded ordered pairs (a + b a permutation of (0,1,2,3,4) mod 5)", excl == 1920);

    /* unordered triples, and the repeated ones */
    long unord = 0, usec[5] = {0}, rep[5] = {0}, trip = 0;
    for (int i = 0; i < nB; i++) for (int j = i; j < nB; j++) for (int k = j; k < nB; k++) {
        int e[5];
        for (int t = 0; t < 5; t++) e[t] = B[i][t] + B[j][t] + B[k][t];
        int r = sector(e);
        if (r < 0) continue;
        unord++; usec[r]++;
        if (i == j && j == k) trip++;
        else if (i == j || j == k) rep[r]++;
    }
    check("1431 unordered triples: 566, 425, 280, 160 by sector",
          unord == 1431 && usec[0] == 566 && usec[1] == 425 && usec[2] == 280 && usec[3] == 160);
    check("repeated labels {a,a,c}: D_r = 0, 50, 20, 30 and the one triple {1,1,1}",
          rep[0] == 0 && rep[1] == 50 && rep[2] == 20 && rep[3] == 30 && trip == 1);
    check("N_r = (O_r - 3 D_r - T_r)/6 + D_r + T_r",
          (3391 - 0 - 1) / 6 + 0 + 1 == 566 && (2400 - 150) / 6 + 50 == 425 &&
          (1620 - 60) / 6 + 20 == 280 && (870 - 90) / 6 + 30 == 160);

    /* the mass map of h = x1...x5: partners c with b + c + 1 in a sector */
    int partner[101], power[101], unique = 1;
    for (int i = 0; i < nB; i++) {
        int n = 0;
        for (int j = 0; j < nB; j++) {
            int e[5];
            for (int t = 0; t < 5; t++) e[t] = B[i][t] + B[j][t] + 1;
            int r = sector(e);
            if (r >= 0) { partner[i] = j; power[i] = r; n++; }
        }
        if (n != 1) unique = 0;
    }
    check("every label has exactly one partner under h", unique);
    int invol = 1, fixed = 0, sametype = 1, pw[5] = {0}, detexp = 0, threes = 1;
    for (int i = 0; i < nB; i++) {
        if (partner[partner[i]] != i) invol = 0;
        if (partner[i] == i) fixed++;
        if (type_of(B[i]) != type_of(B[partner[i]])) sametype = 0;
        pw[power[i]]++; detexp += power[i];
        int has3 = 0;
        for (int t = 0; t < 5; t++) if (B[i][t] == 3) has3 = 1;
        if (has3 != (power[i] > 0)) threes = 0;
    }
    check("sigma is a type-preserving involution with one fixed point", invol && fixed == 1 && sametype);
    check("couplings 1, psi, psi^2 on 51, 30, 20 labels; determinant psi^70", pw[0] == 51 && pw[1] == 30 && pw[2] == 20 && detexp == 70);
    check("sigma is fifty transpositions, an even permutation; rank 51 at psi = 0", (nB - fixed) / 2 == 50 && threes);

    printf("%d checks passed, %d failed\n", npass, nfail);
    return nfail != 0;
}
