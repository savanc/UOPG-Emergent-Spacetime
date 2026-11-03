"""M3: O(p^4) ratio fixed by the 4-point hidden zero, exact alpha'-expansions and data test.
Pre-registration: prereg/M3-lec-ratio-2026-10-10.md (committed before this file).
Exact: sympy. Numerics: mpmath (50 digits). Run: <local path> scripts/m3_lec_ratio.py
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
t, X, Y, a, d = sp.symbols('t X Y a delta')
s, u = sp.symbols('s u')
print("=" * 72)
print("M3 exact checks")


def taylor2(expr, order=4):
    """Taylor coefficients of expr(t*X, t*Y) up to t^(order-1)."""
    ser = sp.series(expr, t, 0, order).removeO()
    return [sp.expand(sp.simplify(ser.coeff(t, k))) for k in range(order)]


def g_coeffs(P2):
    """For a quadratic form P2 = A X^2 + B X Y + C Y^2 return (A, B, C)."""
    P = sp.Poly(sp.expand(P2), X, Y)
    return P.coeff_monomial(X**2), P.coeff_monomial(X*Y), P.coeff_monomial(Y**2)

# ---------- L1 (hidden zero <=> g21 = g20) ----------
g20, g21 = sp.symbols('g20 g21')
P = g20*(s**2 + u**2) + 2*g21*s*u
print("\n[L1] P(s,-s) =", sp.factor(P.subs(u, -s)), " -> zero for all s iff g21 = g20")
assert sp.expand(P.subs(g21, g20) - g20*(s + u)**2) == 0

# ---------- (C1) [H] stringy delta-family, eq. (7.10) with alpha'=1, a = alpha' delta ----------
fH = sp.gamma(t*X - a)*sp.gamma(t*Y + a)/sp.gamma(t*(X + Y))
cH = taylor2(fH, 4)
c0 = sp.simplify(cH[1]/(X + Y))
print("\n[C1] O(p^2):", sp.simplify(cH[1]), "  => c0 =", sp.simplify(c0))
assert sp.simplify(c0 - sp.gamma(-a)*sp.gamma(a)) == 0
q = sp.simplify(cH[2]/sp.gamma(-a)/sp.gamma(a))         # normalised O(p^4) quadratic form
q = sp.expand(sp.simplify(q.rewrite(sp.polygamma)))
A_, B_, C_ = g_coeffs(q)
print("[C1] normalised O(p^4): X^2:", sp.simplify(A_), " XY:", sp.simplify(B_), " Y^2:", sp.simplify(C_))
# C-even (s<->u symmetrised) part: g20 = (A+C)/2, 2 g21 = B
g20H = sp.simplify((A_ + C_)/2); g21H = sp.simplify(B_/2)
print("[C1] C-even: g20 - g21 =", sp.simplify(g20H - g21H), "(must be 0 for all a)")
assert sp.simplify(g20H - g21H) == 0
oddH = sp.simplify((A_ - C_)/2)
print("[C1] C-odd coefficient of (X^2 - Y^2):", oddH)
oddH_expected = (sp.polygamma(0, -a) - sp.polygamma(0, a))/2
assert sp.simplify(oddH - oddH_expected) == 0
for av in [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4)]:
    v1 = mp.mpf(sp.N(oddH_expected.subs(a, av), 40))
    v2 = (1/mp.mpf(av) + mp.pi*mp.cot(mp.pi*mp.mpf(av)))/2
    print(f"   a={av}: C-odd = {mp.nstr(v1, 15)}   (1/a + pi cot pi a)/2 = {mp.nstr(v2, 15)}")
    assert abs(v1 - v2) < mp.mpf(10)**-30
astar = mp.findroot(lambda z: 1/z + mp.pi*mp.cot(mp.pi*z), 0.65)
print("[C1] C-odd O(p^4) vanishes only at a* =", mp.nstr(astar, 20), "in (0,1) (root of tan(pi a) = -pi a)")
# uniqueness of root in (0,1): h(a) = 1/a + pi cot(pi a) is strictly decreasing on (0,1)
hp = lambda z: -1/z**2 - mp.pi**2/mp.sin(mp.pi*z)**2
assert all(hp(mp.mpf(k)/1000) < 0 for k in range(1, 1000))
# check the overall (X+Y) factor to O(p^6) as well (hidden zero to all orders: series of f/(X+Y) is regular)
assert all(sp.simplify(sp.expand(ck).subs(Y, -X)) == 0 for ck in cH[1:4])
print("[C1] hidden zero X13+X24=0 holds at O(p^2), O(p^4), O(p^6) for symbolic a")

# ---------- (C2) Lovelace-Shapiro, AR (2.22), alpha'=1 ----------
fLS = -sp.gamma(sp.Rational(1, 2) - t*X)*sp.gamma(sp.Rational(1, 2) - t*Y)/sp.gamma(-t*(X + Y))
cL = taylor2(fLS, 4)
cL = [sp.expand(sp.simplify(c.rewrite(sp.polygamma))) for c in cL]
cL = [sp.expand(sp.nsimplify(sp.simplify(c.subs({sp.polygamma(0, sp.Rational(1, 2)): -sp.EulerGamma - 2*sp.log(2),
                                                  sp.polygamma(1, sp.Rational(1, 2)): sp.pi**2/2}))))
      for c in cL]
print("\n[C2] LS O(p^2):", sp.factor(cL[1]))
A2, B2, C2 = g_coeffs(cL[2])
g10L = sp.simplify(sp.Poly(cL[1], X, Y).coeff_monomial(X))
g20L = sp.simplify(A2); g21L = sp.simplify(B2/2)
print("[C2] LS g10 =", g10L, " g20 =", g20L, " g21 =", g21L)
assert sp.simplify(g20L - g21L) == 0
# AR normalisation: M^2 = m_rho^2 = 1/(2 alpha')
gt2 = sp.simplify(g20L/g10L/2); gt2p = sp.simplify(2*g21L/g10L/2)
print("[C2] g~2 =", gt2, "=", sp.N(gt2, 12), "  g~2' =", gt2p, "  (AR 4.33: 0.693147, 1.38629)")
assert sp.simplify(gt2 - sp.log(2)) == 0
P3 = sp.Poly(cL[3], X, Y)
g30L = sp.simplify(P3.coeff_monomial(X**3)); g31L = sp.simplify(P3.coeff_monomial(X**2*Y))
print("[C2] LS g30 =", g30L, " g31 =", g31L)
han = sp.simplify(g10L*g30L - g20L**2)
print("[C2] forward Hankel g10 g30 - g20^2 =", han, "=", sp.N(han, 15), "(must be >= 0)")
assert sp.N(han) > 0
print("[C2] g~2 = ln 2 <= 1 (cutoff M = m_rho):", sp.N(sp.log(2)) <= 1)
# PV (4.6): L2 = F0^2 ln2 /(8 m_rho^2); from g21 = 4 L4'/f^4, g10 = 1/(2 f^2), alpha' = 1/(2 m_rho^2)
F0, mr = sp.symbols('F0 m_rho', positive=True)
L4p = sp.simplify((g21L/g10L)*(1/(2*mr**2))*(1/(2*F0**2))*F0**4/4)
print("[C2] L4' = L2 =", L4p, " (PV 4.6: F0^2 ln2/(8 m_rho^2))")
assert sp.simplify(L4p - F0**2*sp.log(2)/(8*mr**2)) == 0
print("     numerically with F0 = 92.4 MeV, m_rho = 770 MeV (PV's scale):",
      mp.nstr(mp.mpf('0.0924')**2*mp.log(2)/(8*mp.mpf('0.770')**2), 6), "(PV: 1.25e-3)  [needs F0/m_rho: not zero-parameter]")

# ---------- (C3) field-theory delta-shift (M2d), 4 points ----------
fF = -d**2*(1/(t*X - d) + 1/(t*Y + d))
cF = taylor2(fF, 4)
print("\n[C3] field theory: O(p^2):", sp.factor(cF[1]), " O(p^4):", sp.factor(cF[2]), " O(p^6):", sp.factor(cF[3]))
A3, B3, C3 = g_coeffs(cF[2])
assert sp.simplify((A3 + C3)/2) == 0 and B3 == 0
print("[C3] C-even O(p^4) = 0 ; C-odd O(p^4) =", sp.factor(cF[2]))

# ---------- (L3) map to LECs (AR 4.21, 4.26, 4.27) ----------
L3p, L4p_, l1, l2, f = sp.symbols("L3p L4p l1 l2 f", real=True)
g20m = (2*L3p + 4*L4p_)/f**4; g21m = 4*L4p_/f**4
sol = sp.solve(sp.Eq(g20m, g21m), L3p)
print("\n[L3] g21 = g20  =>  L3' =", sol)
L1_, L2_, L3_ = L4p_/2, L4p_, 0 - 2*L4p_  # with L1'=L2'=0, L3'=0
print("[L3] SU(3): L1 = L4'/2, L2 = L4', L3 = -2 L4'  =>  L3/L2 =", sp.simplify(L3_/L2_), ", 2L1 - L2 =", 2*L1_ - L2_)
print("[L3] SU(2): g20 = g21 <=>", sp.solve(sp.Eq((2*l1 + 3*l2)/2, l2), l1), "(l1 = -l2/2)")

# ---------- data ----------
print("\n" + "=" * 72 + "\nData (pre-registered rule)")


def ratio_lin(n, sn, dd, sd):
    r = n/dd
    return r, abs(r)*mp.sqrt((sn/n)**2 + (sd/dd)**2)


def verdict(band, r, sg):
    lo, hi = band
    I1 = (r - sg, r + sg); I2 = (r - 2*sg, r + 2*sg)
    ov = lambda A, B: max(A[0], B[0]) <= min(A[1], B[1])
    if ov(band, I1):
        return "PASS", I1, I2
    if not ov(band, I2):
        return "FAIL", I1, I2
    return "INCONCLUSIVE", I1, I2


def mc_ratio(n, sn, dd, sd, N=200000, seed=1):
    import random
    random.seed(seed)
    v = sorted(random.gauss(n, sn)/random.gauss(dd, sd) for _ in range(N))
    return v[N//2], v[int(0.16*N)], v[int(0.84*N)]


band3 = (mp.mpf('-2.6'), mp.mpf('-1.4'))
sets = [("BE14 NNLO preferred (Table 3) [PRIMARY]", '-3.07', '0.20', '0.81', '0.04'),
        ("BE14 NNLO free fit (Table 3)", '-2.80', '0.20', '0.59', '0.04'),
        ("BE14 p4 fit (Table 1 col. 6)", '-3.8', '0.3', '1.6', '0.2'),
        ("GL 1985 (BE14 Table 1 last col.)", '-4.4', '2.5', '1.3', '0.7'),
        ("Pich 1995 / BEG 1994 (Table 1)", '-3.5', '1.1', '1.4', '0.3')]
res = {}
for name, n, sn, dd, sd in sets:
    r, sg = ratio_lin(mp.mpf(n), mp.mpf(sn), mp.mpf(dd), mp.mpf(sd))
    v, I1, I2 = verdict(band3, r, sg)
    med, p16, p84 = mc_ratio(float(n), float(sn), float(dd), float(sd))
    pull = (r - (-2))/sg
    res[name] = (r, sg, v)
    print(f"[T1] {name}: L3/L2 = {mp.nstr(r, 4)} +- {mp.nstr(sg, 2)}  (MC median {med:.3f}, 68% [{p16:.3f},{p84:.3f}])"
          f"  pull of -2: {mp.nstr(pull, 3)} sigma ; band-edge gap {mp.nstr((r - band3[0])/sg, 3) if r < band3[0] else 0} sigma -> {v}")
# exact rational check of primary
rq = sp.Rational(-307, 81)
print("[T1] exact BE14 central ratio = -307/81 =", sp.N(rq, 8))

# scale scan for L2 (Gamma2 = 3/16, Gamma3 = 0; Pich hep-ph/9502366 eq. 4.5, 5.1)
print("\n[S5] scale scan, BE14 primary: L2(mu) = L2(0.77) + Gamma2/(16 pi^2) ln(0.77/mu), L3 fixed")
for mu in ['0.5', '0.6', '0.77', '0.9', '1.0']:
    L2mu = mp.mpf('0.81e-3') + mp.mpf(3)/16/(16*mp.pi**2)*mp.log(mp.mpf('0.77')/mp.mpf(mu))
    print(f"     mu = {mu} GeV: L2 = {mp.nstr(L2mu*1e3, 4)}e-3, L3/L2 = {mp.nstr(mp.mpf('-3.07e-3')/L2mu, 4)}")

# SU(2): CGL 2001 eq. 14.1
print("\n[S1] SU(2), CGL 2001: lbar1 = -0.4 +- 0.6, lbar2 = 4.3 +- 0.1; Mpi = 139.57 MeV")
Mpi = mp.mpf('0.13957')


def lr(lbar, gam, mu):
    return gam/(32*mp.pi**2)*(lbar + mp.log(Mpi**2/mu**2))


band2 = (mp.mpf('-0.65'), mp.mpf('-0.35'))
for mu in ['0.77', '0.77526']:
    m = mp.mpf(mu)
    L = mp.log(Mpi**2/m**2)
    r = (mp.mpf(1)/3*(mp.mpf('-0.4') + L))/(mp.mpf(2)/3*(mp.mpf('4.3') + L))
    # linear error: r = (lb1 + L)/(2 (lb2 + L))
    dr1 = 1/(2*(mp.mpf('4.3') + L)); dr2 = -(mp.mpf('-0.4') + L)/(2*(mp.mpf('4.3') + L)**2)
    sg = mp.sqrt((dr1*mp.mpf('0.6'))**2 + (dr2*mp.mpf('0.1'))**2)
    v, I1, I2 = verdict(band2, r, sg)
    l1r, l2r = lr(mp.mpf('-0.4'), mp.mpf(1)/3, m), lr(mp.mpf('4.3'), mp.mpf(2)/3, m)
    gt2 = (2*l1r + 3*l2r); gt2p = 4*l2r   # both times M^2/f^2: ratio only
    print(f"     mu = {mu}: l1r = {mp.nstr(l1r*1e3, 4)}e-3, l2r = {mp.nstr(l2r*1e3, 4)}e-3, l1/l2 = {mp.nstr(r, 4)} +- {mp.nstr(sg, 2)}"
          f" -> {v};  g~2'/g~2 = {mp.nstr(gt2p/gt2, 4)} (prediction 2, VMD/Skyrme 4)")
for mu in ['0.5', '0.6', '0.9', '1.0']:
    m = mp.mpf(mu); L = mp.log(Mpi**2/m**2)
    print(f"     scan mu = {mu}: l1/l2 = {mp.nstr((mp.mpf('-0.4') + L)/(2*(mp.mpf('4.3') + L)), 4)}")
# mu* where data ratio = -1/2: (lb1 + L) = -(lb2 + L) -> L = -(lb1+lb2)/2
Ls = -(mp.mpf('-0.4') + mp.mpf('4.3'))/2
print("     mu* (l1/l2 = -1/2 exactly) =", mp.nstr(Mpi*mp.e**(-Ls/2)*1000, 5), "MeV")
