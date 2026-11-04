"""M3 audit (2026-10-12): re-derive the map, propagate errors with correlation sensitivity, scan sources and mu."""
import sympy as sp, numpy as np
# (3) mapping re-derivation (AR 4.21, 4.26, 4.27; large N: L1'=L2'=0)
L3p, L4p, l1, l2 = sp.symbols("L3p L4p l1 l2")
g20, g21 = 2*L3p + 4*L4p, 4*L4p
L2, L3 = L4p, L3p - 2*L4p
print("g21=g20 <=> L3p=0:", sp.solve(sp.Eq(g20, g21), L3p), "; then L3/L2 =", sp.simplify((L3/L2).subs(L3p, 0)))
print("SU(2): g21=g20 <=>", sp.solve(sp.Eq((2*l1+3*l2)/2, l2), l1), "(l1/l2 = -1/2)")
# LS check: M = -G(1/2-s)G(1/2-u)/G(-(s+u)), alpha'=1: expand
s, u = sp.symbols("s u")
M = -sp.gamma(sp.Rational(1,2)-s)*sp.gamma(sp.Rational(1,2)-u)/sp.gamma(-(s+u))
ser = sp.series(M.subs({s: s*sp.Symbol('e'), u: u*sp.Symbol('e')}), sp.Symbol('e'), 0, 3).removeO()
c2 = sp.Poly(sp.expand(sp.simplify(ser.coeff(sp.Symbol('e'), 2))), s, u)
print("LS O(p^4):", {m: sp.nsimplify(sp.N(c, 30)/sp.pi, [sp.log(2)]) for m, c in c2.terms()})
rng = np.random.default_rng(1)
def ratio_mc(a, sa, b, sb, rho=0.0, n=400000):
    cov = [[sa**2, rho*sa*sb], [rho*sa*sb, sb**2]]
    x = rng.multivariate_normal([a, b], cov, n); r = x[:, 0]/x[:, 1]
    return np.median(r), np.percentile(r, [2.275, 15.87, 84.13, 97.725])
def verdict(lo2, lo1, hi1, hi2, band):
    if not (hi2 < band[0] or lo2 > band[1]):
        return "PASS" if not (hi1 < band[0] or lo1 > band[1]) else "INCONCLUSIVE"
    return "FAIL"
print("\n(1,2) SU(3) BE14 NNLO preferred L3=-3.07(20), L2=0.81(4): correlation sensitivity, mu=0.77")
for rho in (-0.8, -0.5, 0, 0.5, 0.8):
    m, q = ratio_mc(-3.07, 0.20, 0.81, 0.04, rho); print(f"  rho={rho:+.1f}: median {m:.3f}, 2sig [{q[0]:.2f},{q[3]:.2f}] -> {verdict(q[0],q[1],q[2],q[3],(-2.6,-1.4))}")
# SU(2) sources: lbar1, lbar2 (CGL 2001 Roy; BCEGS 1997 Kl4 two-loop; GKPY-era dispersive values not opened -> not used)
Mpi = 0.13957
src = {"CGL01 (Roy eqs.) -0.4(6), 4.3(1)": (-0.4, 0.6, 4.3, 0.1),
       "BCEGS97 (Kl4, 2-loop) -1.7(1.0), 6.1(5)": (-1.7, 1.0, 6.1, 0.5),
       "GL84 -2.3(3.7), 6.0(1.3)": (-2.3, 3.7, 6.0, 1.3)}
print("\n(1) SU(2) l1r/l2r, prediction -1/2, band [-0.65,-0.35]; mu scan")
for name, (a, sa, b, sb) in src.items():
    for mu in (0.5, 0.77, 1.0):
        Lg = np.log(Mpi**2/mu**2)
        m, q = ratio_mc((a+Lg)/3, sa/3, 2*(b+Lg)/3, 2*sb/3)
        print(f"  {name:40s} mu={mu}: median {m:+.3f}, 1sig [{q[1]:+.2f},{q[2]:+.2f}] 2sig [{q[0]:+.2f},{q[3]:+.2f}] -> {verdict(*q,(-0.65,-0.35))}")
print("\n(1) SU(3) mu scan of BE14 NNLO (L2 runs, Gamma2=3/16; L3 Gamma3=0)")
for mu in (0.5, 0.6, 0.77, 1.0):
    dL2 = -3/16/(16*np.pi**2)*np.log(mu/0.77)*1e3  # L_i(mu2)=L_i(mu1)+Gamma_i/(16pi^2) ln(mu1/mu2)
    m, q = ratio_mc(-3.07, 0.20, 0.81+dL2, 0.04); print(f"  mu={mu}: L2={0.81+dL2:.3f}, median {m:.2f}, 2sig [{q[0]:.2f},{q[3]:.2f}] -> {verdict(*q,(-2.6,-1.4))}")
print("\n(2) band dependence (BE14 NNLO, mu=0.77): smallest band fraction f giving non-FAIL")
m, q = ratio_mc(-3.07, 0.20, 0.81, 0.04)
for f in (0.3, 0.4, 0.5, 0.6, 0.62, 0.65, 0.7):
    print(f"  band {f:.0%}: [{-2-2*f:.2f},{-2+2*f:.2f}] -> {verdict(*q,(-2-2*f,-2+2*f))}")
