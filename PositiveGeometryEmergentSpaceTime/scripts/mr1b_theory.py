"""MR-1b theory (no data): (a) resolve MR-1's 5% AHRV gap: generalized LS (AHRV C.1-C.2) with trajectory through rho and f2;
(b) LS couplings at levels n=2 (rho3, J=3, I=1) and n=3 (f4, J=4, I=0) in AHRV (2.12) normalisation; width kappas."""
import sympy as sp, json
x, e = sp.symbols("x e")
def gsq(r, m2, J):
    ap = 1/(r - 1); a0 = 1 - ap
    al = lambda v: a0 + ap*v
    u = m2*(x - 1)/2
    lead = sp.limit(-sp.gamma(1 - al(m2 + e))*e, e, 0)
    f = sp.expand(sp.gammasimp(lead*sp.gamma(1 - al(u))/sp.gamma(1 - al(m2) - al(u))))
    cJ = sp.integrate(f*sp.legendre(J, x), (x, -1, 1))*sp.Rational(2*J + 1, 2)
    return sp.nsimplify(-cJ/m2), f
out = {}
rphys = sp.Rational(12754, 7752.6)**2
for r in (sp.Integer(3), sp.nsimplify(rphys)):
    gr, _ = gsq(r, 1, 1); gf, _ = gsq(r, r, 2)
    print(f"r={float(r):.4f}: g_rho^2={sp.N(gr,8)}, g_f2^2={sp.N(gf,8)}, ratio={sp.N(gf/gr,8)}")
    out[f"gap_r={float(r):.4f}"] = float(gf/gr)
print("AHRV C.7 ratio 0.27790/0.52748 =", 0.27790/0.52748, "; C.5 ratio 0.22392/0.42502 =", 0.22392/0.42502)
r = sp.Integer(3); gr, _ = gsq(r, 1, 1)
for name, m2, J in [("rho", 1, 1), ("f2", 3, 2), ("rho3", 5, 3), ("f4", 7, 4)]:
    g, f = gsq(r, m2, J)
    allJ = {j: sp.nsimplify(sp.integrate(f*sp.legendre(j, x), (x, -1, 1))*sp.Rational(2*j+1, 2)) for j in range(J+1)}
    print(f"{name}: m^2={m2}, residue poly {sp.factor(f)}; Legendre coeffs {allJ}; g^2={g}; g^2/g_rho^2={sp.nsimplify(g/gr)}")
    out[name] = dict(m2=m2, J=J, residue=str(sp.expand(f)), g2_over_rho=str(sp.nsimplify(g/gr)), legendre={str(k): str(v) for k, v in allJ.items()})
kap = lambda I, J: sp.Rational({1: 4, 0: 6}[I], 2*J + 1)
for name, I, J in [("f2", 0, 2), ("rho3", 1, 3), ("f4", 0, 4)]:
    print(f"kappa_{name}/kappa_rho = {kap(I, J)/kap(1, 1)}"); out[f"kappa_{name}"] = str(kap(I, J)/kap(1, 1))
json.dump(out, open("scripts/mr1b_theory.json", "w"), indent=1)
