"""MR-1 theory side (no data): Lovelace-Shapiro (alpha0=1/2 Adler, alpha'=1/(2 m_rho^2)) residues -> I=1 J=1 (rho) and
I=0 J=2 (f2) partial-wave residues, on-shell couplings (AHRV 2.12 normalisation), width ratio under conventions C0-C3."""
import sympy as sp, mpmath as mp, json
mp.mp.dps = 30
s, t, u, z = sp.symbols("s t u z")
mr2 = sp.Integer(1)                       # units m_rho = 1 ; alpha' = 1/2
def M(x, y):                              # ordered amplitude, poles in x and y (FPRS 106 / AHRV C.1 up to overall sign)
    return sp.gamma(sp.Rational(1, 2) - x/2) * sp.gamma(sp.Rational(1, 2) - y/2) / sp.gamma(-(x + y)/2)
def A(x, y, w): return M(x, w) + M(x, y) - M(y, w)       # coefficient of delta_ab delta_cd (Tr of Pauli; overall 4 dropped)
def resM_s(m2, y):                        # residue in s at s=m2 of M(s, y) (exact, via gamma pole)
    n = int((m2 - 1)/2); eps = sp.Symbol("e")
    expr = sp.gamma(sp.Rational(1, 2) - (m2 + eps)/2) * eps
    r0 = sp.limit(expr, eps, 0)
    return sp.simplify(r0 * sp.gamma(sp.Rational(1, 2) - y/2) / sp.gamma(-(m2 + y)/2))
res = {}
for m2, I, J in [(1, 1, 1), (3, 0, 2), (3, 0, 0)]:
    tz, uz = -m2*(1 - z)/2, -m2*(1 + z)/2
    # residues at s=m2 of A-combinations: only terms with a pole in s contribute
    # A(s,t,u)=M(s,u)+M(s,t)-M(t,u); A(t,s,u)=M(t,u)+M(t,s)-M(s,u); A(u,t,s)=M(u,s)+M(u,t)-M(t,s)
    R = lambda y: resM_s(m2, y)
    RA_s = R(uz) + R(tz); RA_t = R(tz) - R(uz); RA_u = R(uz) - R(tz)
    TI = {0: 3*RA_s + RA_t + RA_u, 1: RA_t - RA_u}[I]
    rJ = sp.nsimplify(sp.integrate(sp.expand_func(TI) * sp.legendre(J, z), (z, -1, 1)) / (64*sp.pi))
    res[(I, J)] = sp.simplify(rJ)
    print(f"Res_s t^I={I}_J={J} at s={m2} m_rho^2: {res[(I,J)]} = {sp.N(res[(I,J)], 20)}")
# ordered-amplitude on-shell couplings in AHRV (2.12) normalisation: Res_s M(s,u) spin-J part = -g^2 m^2 P_J(1+2u/m^2)
def gsq(m2, J):
    x = sp.Symbol("x"); y = -m2*(1 - x)/2          # u = -m2(1-x)/2 -> 1+2u/m2 = x
    f = resM_s(m2, y); cJ = sp.integrate(sp.expand_func(f)*sp.legendre(J, x), (x, -1, 1))*(2*J + 1)/2
    return sp.simplify(-cJ/m2)
g_rho, g_f2 = gsq(1, 1), gsq(3, 2)
print("AHRV-normalised g^2: rho", g_rho, "f2", g_f2, "ratio g_f2^2/g_rho^2 =", sp.nsimplify(g_f2/g_rho), "=", sp.N(g_f2/g_rho, 15))
R = float(res[(0, 2)] / res[(1, 1)])
out = {"Res_ratio_f2_over_rho": R, "g2_ratio_AHRV": float(g_f2/g_rho)}
# Conventions for Gamma = -sigma(m) Res / m (BW: t ~ (1/sigma) m Gamma/(m^2-s-i m Gamma))
mpi, mrho, mf2 = mp.mpf("0.13957"), None, None   # pion mass is a standard constant; physical rho/f2 masses enter ONLY at data time
def sig(m2, mp2): return mp.sqrt(1 - 4*mp2/m2)
print("C0 (LS-native: massless pions, predicted masses m_f2^2=3 m_rho^2):", R/mp.sqrt(3))
out["C0"] = float(R/mp.sqrt(3))
json.dump(out, open("scripts/mr1_ls_prediction.json", "w"), indent=1)
