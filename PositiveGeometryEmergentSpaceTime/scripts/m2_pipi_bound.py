"""M2 / P-EFT: reproduce the Manohar-Mateu dispersion bounds on lbar_1, lbar_2 from the
one-loop pi-pi amplitude, then compare with the CGL 2001 values (pre-registered rule).

Inputs (all CITED, see prereg/M2-positivity-2026-10-10.md):
  * O(p^4) amplitude, units M_pi = 1, x2 = M^2/F^2 (Bijnens et al., NPB 508 (1997) 263,
    hep-ph/9707291, eq. (4.14)-(4.15)):
      A(s,t,u) = x2 (s-1) + x2^2 [b1 + b2 s + b3 s^2 + b4 (t-u)^2
                 + F1(s) + G1(s,t) + G1(s,u)],
      F1(s) = Jb(s)(s^2-1)/2,  G1(s,t) = Jb(t)(14 - 4s - 10t + s t + 2 t^2)/6,
      16 pi^2 Jb(s) = sigma ln((sigma-1)/(sigma+1)) + 2,  sigma = sqrt(1-4/s).
  * Leading-order b3, b4 in terms of lbar (ibid. eqs. (D.1)-(D.3)):
      16 pi^2 b3 = lbar1/3 + lbar2/6 - 7/12,   16 pi^2 b4 = lbar2/6 - 5/36.
  * Isospin structure: T(pi0 pi0) = A(s,t,u)+A(t,s,u)+A(u,t,s);
    T(pi+ pi0 -> pi+ pi0) = A(t,s,u); T(pi+ pi+) = A(t,s,u)+A(u,t,s).
  * Positivity: d^2T/ds^2 >= 0 in region A = {s,t<4, t>0, s+t>0} (Manohar-Mateu eq. (15)).
"""
import sympy as sp
import mpmath as mp

s, t, l1, l2 = sp.symbols('s t lbar1 lbar2', real=True)
x = sp.symbols('x')

# --- Taylor series of 16 pi^2 Jb(x) at x = 0, checked numerically below
def Jb16_num(xv):
    xv = mp.mpf(xv)
    if xv < 0:
        sig = mp.sqrt(1 - 4/xv)
        return sig*mp.log((sig-1)/(sig+1)) + 2
    # 0 < x < 4: analytic continuation, sigma imaginary
    r = mp.sqrt(4/xv - 1)
    return 2 - 2*r*mp.atan(1/r)

# exact series: 16pi^2 Jb(x) = sum_{n>=1} c_n x^n with c_n = (n!)^2/((2n+1)! n)  -> 1/6, 1/60, 1/420, ...
def cn(n):
    return sp.Rational(sp.factorial(n)**2, sp.factorial(2*n+1)*n)
N = 8
Jser = sum(cn(n)*x**n for n in range(1, N+1))
for xv in [-0.3, -0.05, 0.05, 0.3]:
    approx = float(Jser.subs(x, xv)); exact = float(Jb16_num(xv))
    assert abs(approx-exact) < 1e-9, (xv, approx, exact)
print("16pi^2 Jbar series check OK: c1, c2, c3 =", cn(1), cn(2), cn(3))

# Everything below is in units of x2^2/(16 pi^2); constant b1, b2 and O(x2) tree terms drop
# out of the second s-derivative, as do Jb(t) at fixed t = 4 (multiplying s-polynomials: kept exactly).
J = lambda z: Jser.subs(x, z)
b3 = l1/3 + l2/6 - sp.Rational(7, 12)
b4 = l2/6 - sp.Rational(5, 36)
Jt4 = sp.Symbol('Jt4')  # 16pi^2 Jb(4) at threshold; = 2 exactly (sigma=0); kept symbolic to show it drops

def A(S, T, U, Jt=None):
    def Jf(z):
        return Jt if (Jt is not None and z == 4) else J(z)
    return (b3*S**2 + b4*(T-U)**2 + Jf(S)*(S**2-1)/2
            + Jf(T)*(14 - 4*S - 10*T + S*T + 2*T**2)/6
            + Jf(U)*(14 - 4*S - 10*U + S*U + 2*U**2)/6)

def second_deriv_at(Texpr, s0):
    return sp.nsimplify(sp.expand(sp.diff(Texpr, s, 2).subs(s, s0)))

tt = 4
u = 4 - s - tt
procs = {
    "pi+pi0": lambda: A(tt, s, u, Jt4),
    "pi0pi0": lambda: A(s, tt, u, Jt4) + A(tt, s, u, Jt4) + A(u, tt, s, Jt4),
    "pi+pi+": lambda: A(tt, s, u, Jt4) + A(u, tt, s, Jt4),
}
results = {}
for name, f in procs.items():
    d2 = sp.expand(sp.diff(f(), s, 2))
    assert not d2.has(Jt4) or name, None
    d2_0 = sp.simplify(d2.subs(s, 0))
    results[name] = (d2, d2_0)
    print(f"{name}: (16pi^2/x2^2) d^2T/ds^2 at (s=0,t=4) =", sp.factor(d2_0), " [Jt4 present:", d2_0.has(Jt4), "]")

# Solve for the bound constants at s = 0
P1 = sp.solve(sp.Eq(results["pi+pi0"][1], 0), l2)[0]
S1 = sp.solve(sp.Eq(results["pi0pi0"][1].subs(l1, sp.Symbol('C') - 2*l2), 0), sp.Symbol('C'))[0]
print("P1: lbar2 >=", P1, "=", float(P1), " (Manohar-Mateu Table 1: 27/20)")
print("S1: lbar1 + 2 lbar2 >=", S1, "=", float(S1), " (Manohar-Mateu Table 1: 157/40)")
assert P1 == sp.Rational(27, 20) and S1 == sp.Rational(157, 40)

# pi+pi+: maximise f(s) over 0 <= s < 4 at t = 4 (region A boundary), with the full Jbar.
# d^2/ds^2 T(pi+pi+) = alpha*(lbar1 + 3 lbar2) - f(s); use exact Jbar via mpmath and numeric derivative.
def T_pp_num(sv, L1, L2):
    def Jn(z): return Jb16_num(z) if z != 4 else mp.mpf(2)
    def Anum(S, T, U):
        b3n = L1/3 + L2/6 - mp.mpf(7)/12; b4n = L2/6 - mp.mpf(5)/36
        return (b3n*S**2 + b4n*(T-U)**2 + Jn(S)*(S**2-1)/2
                + Jn(T)*(14-4*S-10*T+S*T+2*T**2)/6 + Jn(U)*(14-4*S-10*U+S*U+2*U**2)/6)
    U = 4 - sv - 4
    return Anum(4, sv, U) + Anum(U, 4, sv)
mp.mp.dps = 30
def d2pp(sv, L1, L2):
    return mp.diff(lambda z: T_pp_num(z, L1, L2), sv, 2)
# coefficient structure: d2 = a*(L1+3L2) - f(s); get a and f from two evaluations
def af(sv):
    d00 = d2pp(sv, 0, 0); d10 = d2pp(sv, 1, 0); d01 = d2pp(sv, 0, 1)
    a = d10 - d00
    assert abs((d01 - d00) - 3*a) < 1e-12
    return a, -d00
best = max(((sv, af(sv)[1]/af(sv)[0]) for sv in [i*0.002 for i in range(1, 1000)] if sv not in (0,)), key=lambda p: p[1])
print("S2: lbar1 + 3 lbar2 >= max_s f/a = %.4f at s = %.3f (MM: 5.604 at s = 1.114)" % (best[1], best[0]))

# --- Data check, rule fixed in the pre-registration
def verdict(meas, sm, bound, sb):
    z = (meas - bound) / (sm**2 + sb**2) ** 0.5
    return z, ("PASS" if z >= 2 else "FAIL" if z <= -2 else "INCONCLUSIVE")

l1m, s1m = -0.4, 0.6   # CGL 2001 eq. (14.1); Bijnens-Ecker 2014 eq. (27)
l2m, s2m = 4.3, 0.1
rows = [
    ("P1 (primary) pi+pi0: lbar2", l2m, s2m, 27/20, 0.4),
    ("S1 pi0pi0: lbar1+2lbar2", l1m + 2*l2m, (s1m**2 + 4*s2m**2) ** 0.5, 157/40, 0.4),
    ("S2 pi+pi+: lbar1+3lbar2", l1m + 3*l2m, (s1m**2 + 9*s2m**2) ** 0.5, 5.604, 0.4),
]
print("\nData check (rule: z = (meas-bound)/sqrt(sm^2+sb^2); PASS z>=2, FAIL z<=-2):")
for name, m, sm, b, sb in rows:
    z, v = verdict(m, sm, b, sb)
    print(f"  {name:32s} meas = {m:6.3f} +- {sm:.3f}  bound = {b:.3f} +- {sb}  z = {z:5.2f}  {v}")
print("Cross-checks (not used for verdict):")
for name, m, sm in [("GL1984 one-loop lbar2 (via CGL sec.14)", 6.0, 1.3),
                    ("SU(3)-derived lbar2 (MM sec.VI, from ABT L1-L3)", 1.95, 0.23)]:
    z, v = verdict(m, sm, 27/20, 0.4)
    print(f"  {name:48s} {m} +- {sm}: z = {z:5.2f}  {v}")
