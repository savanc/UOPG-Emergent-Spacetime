"""M3w: is the O(p^4) data inside R_full (any unitary large-N tree theory) and R_fam (M3b family)?
Pre-registration: prereg/M3w-wellposedness-2026-10-11.md (pushed before this script).
Exact sympy for the region algebra; mpmath + numpy MC for pulls."""
import sympy as sp, mpmath as mp, numpy as np
mp.mp.dps = 30
rng = np.random.default_rng(20261011)
NMC = 2_000_000
print("=" * 78)
# ---------------- region algebra (exact) ----------------
L2, L3, l1, l2, eps, w = sp.symbols('L2 L3 l1 l2 epsilon w', real=True)
g20_3, g21_3 = 2*(L3 + 4*L2), 4*L2            # SU(3), 2L1 = L2 (AR 4.26 with L1'=L2'=0), common 1/f^4 dropped
g20_2, g21_2 = (2*l1 + 3*l2)/2, l2            # SU(2) (AR 4.27)
rho3, rho2 = sp.simplify(g21_3/g20_3), sp.simplify(g21_2/g20_2)
print("[A1] rho = g21/g20: SU(3) =", rho3, "; SU(2) =", rho2)
r, q, rho = sp.symbols('r q rho', real=True)
print("     with r=L3/L2: rho =", sp.simplify(rho3.subs(L3, r*L2)), "; with q=l1/l2: rho =", sp.simplify(rho2.subs(l1, q*l2)))
print("     inverse: r = 2/rho - 4, q = 1/rho - 3/2")
assert sp.simplify(rho3.subs(L3, (2/rho - 4)*L2) - rho) == 0 and sp.simplify(rho2.subs(l1, (1/rho - sp.Rational(3, 2))*l2) - rho) == 0
for nm, rv in [("scalar edge", 0), ("hidden zero (eps=0)", 1), ("rho/Skyrme edge (eps=-1)", 2)]:
    rr = sp.oo if rv == 0 else 2/sp.Integer(rv) - 4
    qq = sp.oo if rv == 0 else 1/sp.Integer(rv) - sp.Rational(3, 2)
    print(f"     rho={rv} ({nm}): r={rr}, q={qq}")
# family: mixture of hidden-zero (g21=g20) and odd-only (g21=2g20) with g20-weights (1-w), w
print("[A2] family: g20 = (1-w)+w, g21 = (1-w)*1 + w*2 = 1+w  => rho = 1+w, eps = 1-rho = -w; w in [0,1] <=> eps in [-1,0]")
print("     r(eps) =", sp.simplify(2/(1 - eps) - 4), "; Delta_L/L2 = (3L2+L3)/L2 = 3 + r =", sp.simplify(3 + 2/(1 - eps) - 4))
print("     R_fam: rho in [1,2] <=> r in [-3,-2] <=> q in [-1,-1/2] <=> Delta_L/L2 in [0,1]")
print("     R_full: rho in [0,2] <=> L2>=0 & L3+3L2>=0 <=> l2>=0 & l1+l2>=0")

# ---------------- pull machinery ----------------
def pulls(x, s, lo, hi, band=0.30):
    g = 0.0 if lo <= x <= hi else (lo - x if x < lo else x - hi)
    zexp = g / s
    zN = g / mp.sqrt(s**2 + (band*abs(x))**2)
    fstar = 0.0 if g <= 2*s else mp.sqrt(g**2/4 - s**2)/abs(x)
    cls = "INSIDE" if zexp <= 1 else ("COMPATIBLE" if zexp <= 2 else "OUTSIDE")
    return g, zexp, zN, fstar, cls

def status(zfam, zNfull):
    return "WELL-POSED" if zfam <= 2 else ("ILL-POSED" if zNfull > 2 else "CONDITIONAL")

INF = mp.mpf('1e9')
print("\n[B] SU(3) datasets, variable r = L3/L2 at mu = 0.77 GeV (2L1 = L2 imposed, as in M3)")
sets = [("D1 BE14 NNLO preferred", 0.53, .06, 0.81, .04, -3.07, .20),
        ("D2 BE14 p4 fit (NLO)",   1.0, .1, 1.6, .2, -3.8, .3),
        ("D3 BE14 NNLO free fit",  0.64, .06, 0.59, .04, -2.80, .20),
        ("D4 GL 1985",             0.7, .3, 1.3, .7, -4.4, 2.5),
        ("D5 Pich/BEG",            None, None, 1.4, .3, -3.5, 1.1)]
res = {}
for nm, a1, s1, a2, s2, a3, s3 in sets:
    x = mp.mpf(a3)/a2; s = abs(x)*mp.sqrt((s3/a3)**2 + (s2/a2)**2)
    X2 = rng.normal(a2, s2, NMC); X3 = rng.normal(a3, s3, NMC); R = X3/X2
    lo68, med, hi68 = np.percentile(R, [16, 50, 84])
    pf_full = np.mean((X2 >= 0) & (X3 + 3*X2 >= 0)); pf_fam = np.mean((X3 + 3*X2 >= 0) & (X3 + 2*X2 <= 0) & (X2 > 0))
    gF, zF, zNF, fF, cF = pulls(x, s, -3, INF)
    gf, zf, zNf, ff, cf = pulls(x, s, -3, -2)
    st = status(zf, zNF)
    res[nm] = (x, s, zf, st)
    print(f"  {nm:24s} r = {mp.nstr(x,5):>8} +- {mp.nstr(s,3):<5} (MC median {med:.3f}, 68% [{lo68:.3f},{hi68:.3f}])")
    print(f"      R_full: gap {mp.nstr(gF,3)}, z_exp {mp.nstr(zF,3)}, z_N {mp.nstr(zNF,3)} -> {cF};  MC P(in R_full) = {pf_full:.4f}")
    print(f"      R_fam : gap {mp.nstr(gf,3)}, z_exp {mp.nstr(zf,3)}, z_N {mp.nstr(zNf,3)}, f* = {mp.nstr(ff,3)} -> {cf};  MC P(in R_fam) = {pf_fam:.4f}")
    # linear-combination cross-check (Gaussian): Delta_L = 3L2+L3 >= 0 ; HZ side L3+2L2 <= 0
    dL = a3 + 3*a2; sdL = mp.sqrt(s3**2 + 9*s2**2); hz = a3 + 2*a2; shz = mp.sqrt(s3**2 + 4*s2**2)
    print(f"      lin. check: Delta_L = 3L2+L3 = {dL:+.3f} +- {mp.nstr(sdL,3)} ({mp.nstr(dL/sdL,3)} sigma);  L3+2L2 = {hz:+.3f} +- {mp.nstr(shz,3)}")
    if a1 is not None:
        # FPRS mapping keeping L1 (no 2L1=L2): rho = 2L2/(2L1+3L2+L3); R_full: 2L1+2L2+L3>=0 ; R_fam: also 2L1+L2+L3<=0
        c_full = 2*a1 + 2*a2 + a3; sc_full = mp.sqrt(4*s1**2 + 4*s2**2 + s3**2)
        c_fam = 2*a1 + a2 + a3; sc_fam = mp.sqrt(4*s1**2 + s2**2 + s3**2)
        den = 2*a1 + 3*a2 + a3
        print(f"      FPRS map (keeps L1): rho = 2L2/(2L1+3L2+L3) = {2*a2/den:.3f}; 2L1+2L2+L3 = {c_full:+.3f} +- {mp.nstr(sc_full,3)} "
              f"({mp.nstr(c_full/sc_full,3)} sigma, >=0 needed); 2L1+L2+L3 = {c_fam:+.3f} +- {mp.nstr(sc_fam,3)} (<=0 needed for R_fam)")
        print(f"      large-Nc indicator L_A = 2L1-L2 = {2*a1-a2:+.2f} (= {mp.nstr((2*a1-a2)/a2,3)} L2)")
    print(f"      STATUS for M3b: {st}")

print("\n[C] scale window for D1 (L3 fixed, L2(mu) = 0.81e-3 + (3/16)/(16 pi^2) ln(0.77/mu))")
k = mp.mpf(3)/16/(16*mp.pi**2)
def mu_at(rtarget):  # L3/L2(mu) = rtarget
    L2need = mp.mpf('-3.07e-3')/rtarget
    return mp.mpf('0.77')*mp.e**(-(L2need - mp.mpf('0.81e-3'))/k)
print(f"     r = -3 at mu = {mp.nstr(mu_at(-3),4)} GeV ; r = -2 at mu = {mp.nstr(mu_at(-2),4)} GeV")
print(f"     => D1 central in R_fam for mu in [{mp.nstr(mu_at(-2),3)}, {mp.nstr(mu_at(-3),3)}] GeV, in R_full for mu <= {mp.nstr(mu_at(-3),3)} GeV")

print("\n[D] SU(2): CGL 2001 lbar1 = -0.4(6), lbar2 = 4.3(1); l_i^r(mu) = gamma_i/(32 pi^2)(lbar_i + ln(Mpi^2/mu^2))")
Mpi = mp.mpf('0.13957')
def lr(lb, gam, mu): return gam/(32*mp.pi**2)*(lb + mp.log(Mpi**2/mp.mpf(mu)**2))
for mu in ['0.77', '0.775']:
    a1 = lr(-0.4, mp.mpf(1)/3, mu); a2 = lr(4.3, mp.mpf(2)/3, mu)
    s1 = mp.mpf(1)/3/(32*mp.pi**2)*0.6; s2 = mp.mpf(2)/3/(32*mp.pi**2)*0.1
    x = a1/a2; s = abs(x)*mp.sqrt((s1/a1)**2 + (s2/a2)**2)
    gF, zF, zNF, fF, cF = pulls(x, s, -1, INF); gf, zf, zNf, ff, cf = pulls(x, s, -1, -0.5)
    print(f"  mu={mu}: l1r={mp.nstr(a1*1e3,4)}e-3, l2r={mp.nstr(a2*1e3,4)}e-3, q = l1/l2 = {mp.nstr(x,4)} +- {mp.nstr(s,3)}")
    print(f"      R_full: z_exp {mp.nstr(zF,3)}, z_N {mp.nstr(zNF,3)} -> {cF}; R_fam: z_exp {mp.nstr(zf,3)}, z_N {mp.nstr(zNf,3)}, f* {mp.nstr(ff,3)} -> {cf}; STATUS {status(zf, zNF)}")
    c = a1 + a2; sc = mp.sqrt(s1**2 + s2**2)
    print(f"      lin. check: l1+l2 = {mp.nstr(c*1e3,4)}e-3 +- {mp.nstr(sc*1e3,3)}e-3 ({mp.nstr(c/sc,3)} sigma, >=0 needed);"
          f" lbar1+2 lbar2 = 8.2(6) vs AR eq.79 bound 3 ln(mu^2/Mpi^2) = {mp.nstr(3*mp.log(mp.mpf(mu)**2/Mpi**2),4)}")
print(f"     l1+l2 = 0 at mu* = Mpi exp((lbar1+2lbar2)/6) = {mp.nstr(Mpi*mp.e**(mp.mpf('8.2')/6),4)} GeV (central)")
print(f"     q = -1/2 (hidden zero) at mu where lbar1+L + (lbar2+L) = 0 with weights: solve")
mu_hz = mp.findroot(lambda m: lr(-0.4, mp.mpf(1)/3, m)/lr(4.3, mp.mpf(2)/3, m) + 0.5, 0.37)
mu_full = mp.findroot(lambda m: lr(-0.4, mp.mpf(1)/3, m)/lr(4.3, mp.mpf(2)/3, m) + 1, 0.5)
print(f"     q = -1/2 at mu = {mp.nstr(mu_hz,4)} GeV; q = -1 at mu = {mp.nstr(mu_full,4)} GeV => CGL central in R_fam for mu in [{mp.nstr(mu_hz,3)}, {mp.nstr(mu_full,3)}] GeV")

print("\n[E] AR Table 1 points (l_i^r(m_rho)), AR normalisation fpi = 92 MeV, M = m_rho = 775 MeV")
K = (mp.mpf('0.775')/mp.mpf('0.092'))**2
print(f"     M^2/fpi^2 = {mp.nstr(K,5)};  g2 = (2l1+3l2) M^2/f^2, g2' = 4 l2 M^2/f^2 (AR eq. 70)")
for nm, a1, s1, a2, s2 in [("GL84", -6.0, 3.9, 5.5, 2.7), ("BCG94", -5.4, 1.1, 5.7, 1.1), ("GKMS97", -4.0, 2.1, 1.6, 1.0), ("ABT00", -3.2, 2.5, 3.1, 2.1)]:
    g2 = (2*a1 + 3*a2)*1e-3*K; sg2 = mp.sqrt(4*s1**2 + 9*s2**2)*1e-3*K; g2p = 4*a2*1e-3*K; sg2p = 4*s2*1e-3*K
    x = mp.mpf(a1)/a2; s = abs(x)*mp.sqrt((s1/a1)**2 + (s2/a2)**2)
    gF, zF, zNF, _, cF = pulls(x, s, -1, INF); gf, zf, zNf, ff, cf = pulls(x, s, -1, -0.5)
    c = a1 + a2; sc = mp.sqrt(s1**2 + s2**2)
    print(f"  {nm:7s} g2 = {mp.nstr(g2,3)}({mp.nstr(sg2,2)}), g2' = {mp.nstr(g2p,3)}({mp.nstr(sg2p,2)}) [AR Table 1 cross-check];"
          f" q = {mp.nstr(x,3)} +- {mp.nstr(s,2)}; l1+l2 = {c:+.1f}({mp.nstr(sc,2)})")
    print(f"          R_full z_exp {mp.nstr(zF,3)} ({cF}); R_fam z_exp {mp.nstr(zf,3)} ({cf}); g2 <= 1: {'yes' if g2 <= 1 else 'NO'}; STATUS {status(zf, zNF)}")

print("\n[F] D8 large-Nc lattice (FPRS quote): Delta_L = 3L2+L3 = -0.12(22)e-3")
print(f"     R_full (Delta_L >= 0): gap 0.12, z = {0.12/0.22:.2f} -> INSIDE; R_fam needs 0 <= Delta_L <= L2: same lower edge -> INSIDE at the eps = -1 edge")
print("     (no 1/N_c band: already an N_c -> infinity extrapolation; L2 not given, so only the lower edge is testable)")
print("\n[G] summary table for the review written by hand from the lines above.")
