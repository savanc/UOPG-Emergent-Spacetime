"""TS-1 (no data): LS (alpha0=1/2, r=m_f2^2/m_rho^2=3) leading-trajectory couplings g^2/g_rho^2 and width constants
kappa/kappa_rho for levels n=1..5 (rho, f2, rho3, f4, rho5, f6). Same code as scripts/mr1b_theory.py (gsq)."""
import sympy as sp, json
x, e = sp.symbols("x e")
def gsq(r, m2, J):
    ap = 1/(r - 1); a0 = 1 - ap
    al = lambda v: a0 + ap*v
    u = m2*(x - 1)/2
    lead = sp.limit(-sp.gamma(1 - al(m2 + e))*e, e, 0)
    f = sp.expand(sp.gammasimp(lead*sp.gamma(1 - al(u))/sp.gamma(1 - al(m2) - al(u))))
    cJ = sp.integrate(f*sp.legendre(J, x), (x, -1, 1))*sp.Rational(2*J + 1, 2)
    return sp.nsimplify(-cJ/m2)
r = sp.Integer(3); gr = gsq(r, 1, 1); out = {}
kap = lambda I, J: sp.Rational({1: 4, 0: 6}[I], 2*J + 1)
for name, m2, J, I in [("rho",1,1,1),("f2",3,2,0),("rho3",5,3,1),("f4",7,4,0),("rho5",9,5,1),("f6",11,6,0)]:
    g = sp.nsimplify(gsq(r, m2, J)/gr); k = kap(I, J)/kap(1, 1)
    out[name] = dict(m2_over_mrho2=m2, J=J, I=I, g2_over_grho2=str(g), value=float(g), kappa_over_rho=str(k))
    print(f"{name}: m^2/m_rho^2={m2} J={J} g^2/g_rho^2={g} = {float(g):.5f}  kappa/kappa_rho={k}")
json.dump(out, open("predictions/ts1/ts1_ls_output.json", "w"), indent=1)
