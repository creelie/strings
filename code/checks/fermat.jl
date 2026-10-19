# Hodge norms and masses at the Fermat point (Proposition 9, Table II, Appendix C).
# Base Julia only: the Gamma function is evaluated by the Lanczos formula (g = 7, nine
# terms, relative error about 1e-15) with the reflection formula below one half.
# Run: julia --startup-file=no fermat.jl

npass = 0; nfail = 0
function check(name, ok)
    global npass, nfail
    println(ok ? "PASS " : "FAIL ", name)
    ok ? (npass += 1) : (nfail += 1)
end

const LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
                 771.32342877765313, -176.61502916214059, 12.507343278686905,
                 -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]

function Γ(x::Float64)
    x < 0.5 && return π / (sin(π * x) * Γ(1 - x))
    x -= 1
    a = LANCZOS[1]
    t = x + 7.5
    for i in 1:8
        a += LANCZOS[i + 1] / (x + i)
    end
    sqrt(2π) * t^(x + 0.5) * exp(-t) * a
end

γ(t) = Γ(t) / Γ(1 - t)
near(a, b, tol) = abs(a - b) <= tol

# reference values of the Gamma function at integers and at one half
check("Gamma(n) = (n-1)! for n = 1..10 and Gamma(1/2) = sqrt(pi)",
      all(near(Γ(Float64(n)), factorial(n - 1), 1e-12 * factorial(n - 1)) for n in 1:10) &&
      near(Γ(0.5), sqrt(π), 1e-14))

check("Gamma(1/5), Gamma(2/5), Gamma(3/5), Gamma(4/5) = 4.59084, 2.21816, 1.48919, 1.16423",
      near(Γ(0.2), 4.59084, 5e-6) && near(Γ(0.4), 2.21816, 5e-6) &&
      near(Γ(0.6), 1.48919, 5e-6) && near(Γ(0.8), 1.16423, 5e-6))
check("gamma(1/5) = 3.94325, gamma(2/5) = 1.48951, gamma(t) gamma(1-t) = 1",
      near(γ(0.2), 3.94325, 5e-6) && near(γ(0.4), 1.48951, 5e-6) &&
      near(γ(0.6) * γ(0.4), 1, 1e-13) && near(γ(0.8) * γ(0.2), 1, 1e-13))

# the 204 characters k in {1,...,4}^5 with sum divisible by five
chars = [k for k in Iterators.product(1:4, 1:4, 1:4, 1:4, 1:4) if sum(k) % 5 == 0]
check("204 = (4^5 - 4)/5 characters of H_3(X_0) with sum divisible by five",
      length(chars) == 204 == (4^5 - 4) ÷ 5)

# g = |int_e omega|^2 / |Q(u, conj u)| with (C2) and (C3), against C prod gamma(k_i/5)
ζ = cis(2π / 5)
C = (2π)^3 / 5^4
function g_from_cycle(k)
    period = 5.0^-4 * prod(abs(1 - ζ^k[i]) for i in 1:4) * prod(Γ(k[i] / 5) for i in 1:4) / Γ(1 - k[5] / 5)
    Q = 5.0^-4 * prod(abs(1 - ζ^k[i]) for i in 1:5)
    period^2 / Q
end
ratios = [g_from_cycle(k) / (C * prod(γ(k[i] / 5) for i in 1:5)) for k in chars]
check("g_b = C prod gamma(k_i/5) with C = (2 pi)^3/5^4 for all 204 characters (Appendix C)",
      maximum(abs.(ratios .- 1)) < 1e-12)

# Table II: the five types b, with k = b + 1
types = [(1, 1, 1, 1, 1), (2, 1, 1, 1, 0), (2, 2, 1, 0, 0), (3, 1, 1, 0, 0), (3, 2, 0, 0, 0)]
gC(b) = prod(γ((bi + 1) / 5) for bi in b)
vals = [gC(b) for b in types]
println("   g_b/C: ", join([string(round(v, digits = 5)) for v in vals], ", "))
check("Table II: g_b/C = 7.33179, 8.74859, 10.4392, 8.74859, 10.4392",
      all(near.(vals, [7.33179, 8.74859, 10.4392, 8.74859, 10.4392], 5e-5)))
check("g_b/C = gamma(2/5)^5, gamma(2/5)^2 gamma(1/5), gamma(1/5)^2/gamma(2/5) (twice each)",
      near(vals[1], γ(0.4)^5, 1e-12) && near(vals[2], γ(0.4)^2 * γ(0.2), 1e-12) &&
      near(vals[3], γ(0.2)^2 / γ(0.4), 1e-12) && near(vals[4], vals[2], 1e-12) &&
      near(vals[5], vals[3], 1e-12))
masses = 1 ./ vals[1:3]
check("masses 0.136392, 0.114304, 0.0957935 in units of v/C; ratios 0.83805 and 0.70234",
      all(near.(masses, [0.136392, 0.114304, 0.0957935], 5e-7)) &&
      near(masses[2] / masses[1], 0.83805, 5e-6) && near(masses[3] / masses[1], 0.70234, 5e-6))

G0 = 25 * γ(0.4)^5 / γ(0.2)^5
check("Weil-Petersson metric at the Fermat point G(0) = 25 gamma(2/5)^5/gamma(1/5)^5 = 0.19226",
      near(G0, 0.19226, 5e-6) &&
      near(G0, 25 * Γ(0.4)^5 * Γ(0.8)^5 / (Γ(0.2)^5 * Γ(0.6)^5), 1e-12))
κ2 = Γ(0.6)^3 * Γ(0.2) / (Γ(0.4)^3 * Γ(0.8))
check("kappa^2 = Gamma(3/5)^3 Gamma(1/5)/(Gamma(2/5)^3 Gamma(4/5)) = 1.19324 = gamma(1/5)/gamma(2/5)^3, kappa = 1.09236",
      near(κ2, 1.19324, 5e-6) && near(sqrt(κ2), 1.09236, 5e-6) && near(κ2, γ(0.2) / γ(0.4)^3, 1e-12))
check("ratio of the second type to the first is gamma(1/5)/gamma(2/5)^3 = kappa^2",
      near(vals[2] / vals[1], κ2, 1e-12))

println("$npass checks passed, $nfail failed")
exit(nfail == 0 ? 0 : 1)
