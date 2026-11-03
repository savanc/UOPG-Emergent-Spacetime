"""KL-1 theory (no data): unequal-mass Lovelace-Shapiro piK amplitude with Adler/hidden-zero intercept.
A(pi+K+ -> pi+K+) = beta * G(1-a_r(t)) G(1-a_K(u)) / G(1-a_r(t)-a_K(u))  [Lovelace 1968; Kawarabayashi-Kitakado-Yabuki 1969;
Ademollo-Veneziano-Weinberg 1969 PRL 22, 83 (CITED from memory, not re-fetched)].
Intercepts fixed by demanding the dual zero line a_r(t)+a_K(u)=1 coincide with the CGW/MR-4 hidden-zero line s = mpi^2+mK^2:
 a_r(t)=1/2+a'(t-mpi^2), a_K(u)=1/2+a'(u-mK^2), a'=1/(2(mrho^2-mpi^2)) [universal slope = assumption].
Outputs: K*_J masses (KS-1) and Kpi partial-width ratios Gamma_J/Gamma_K* (MR-1f)."""
import sympy as sp, json, math
x, e = sp.symbols("x e")
mpi, mrho, mK = 0.13957, 0.77526, 0.4957   # OP-2 inputs (MR-1 S1) + strange-sector free unit mK (memory; MR-4 value)
ap = 1/(2*(mrho**2 - mpi**2))
mJ2 = lambda J: mK**2 + (2*J - 1)/(2*ap)
q2 = lambda m2: (m2 - (mK+mpi)**2)*(m2 - (mK-mpi)**2)/(4*m2)
def resid(J, m2):
    t = -2*q2(m2)*(1 - x)
    at = sp.Rational(1, 2) + sp.Float(ap)*(t - mpi**2)
    # residue of G(1-a_K) at a_K = J (in a_K): (-1)^J/(J-1)! * (-1); keep sign via limit
    lead = sp.limit(-sp.gamma(1 - (J + e))*e, e, 0)   # = coefficient of 1/(J - a_K)
    f = sp.expand(lead*sp.prod([(-at - k) for k in range(J)]))   # G(1-a)/G(1-a-J) = prod_{k<J}(-a-k)
    cJ = sp.integrate(f*sp.legendre(J, x), (x, -1, 1))*sp.Rational(2*J+1, 2)
    return float(cJ), f
def width(J, m2):   # Gamma_el ∝ G_J q /((2J+1) m^2)  (A = 16 pi Σ(2J+1) f_J P_J, BW residue); common beta, a', isospin CG cancel
    G, _ = resid(J, m2); return G*math.sqrt(q2(m2))/((2*J+1)*m2)
def pred(masses):  # masses: dict J -> m (GeV)
    W1 = width(1, masses[1]**2); return {J: width(J, masses[J]**2)/W1 for J in (2, 3, 4)}
if __name__ == "__main__":
    out = {"alpha_prime": ap, "inputs": dict(mpi=mpi, mrho=mrho, mK=mK)}
    mls = {J: math.sqrt(mJ2(J)) for J in (1, 2, 3, 4)}
    print("a' =", ap, "GeV^-2"); print("LS masses:", {J: round(m, 4) for J, m in mls.items()})
    for J in (1, 2, 3, 4):
        G, f = resid(J, mJ2(J)); print(f"J={J}: G_J={G:.5g} (sign must be >0); residue poly deg {sp.degree(sp.Poly(f, x))}")
    P = pred(mls); print("width ratios at LS masses:", {J: round(v, 5) for J, v in P.items()})
    out["mass_LS"] = mls; out["ratio_LS_masses"] = P
    json.dump(out, open("scripts/kl1_theory.json", "w"), indent=1)
