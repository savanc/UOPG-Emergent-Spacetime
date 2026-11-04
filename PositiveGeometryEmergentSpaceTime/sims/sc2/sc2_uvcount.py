#!/usr/bin/env python3
"""SC-2 locked checker. One-loop beta coefficient of a single real scalar phi^k theory in D=Dc-2eps
from explicit one-loop UV poles (sympy, exact). Usage: sc2_uvcount.py {live|planted|broken}
Units: beta = b * g^3/(4pi)^{Dc/2} (phi^3) or b * lam^2/(4pi)^{Dc/2} (phi^4)."""
import sys, sympy as sp
eps, x, y = sp.symbols('eps x y', positive=True)

def pole(n, D):  # residue of 1/eps in Gamma(n-D/2)/Gamma(n) (loop measure, (4pi)^{D/2} stripped)
    e = sp.gamma(n - D/2) / sp.gamma(n)
    r = sp.residue(e, eps, 0)
    return sp.nsimplify(r)

def theory(name):
    if name == 'live':   # phi^3, Dc=6, L = g/3! phi^3
        Dc = 6; D = Dc - 2*eps
        # triangle (vertex): 1/(ABC) = 2! * int_simplex ; integrand power n=3, Delta^0 at pole
        T = 2 * pole(3, D) * sp.integrate(sp.integrate(1, (y, 0, 1 - x)), (x, 0, 1))
        # bubble (self-energy): n=2, Delta^{1} = x(1-x)p^2 ; coefficient of p^2 at pole (Gamma(-1+eps) -> -1/eps)
        Sb = pole(2, D) * sp.integrate(x*(1 - x), (x, 0, 1))
        curves = {'triangle': dict(count=1, sym=sp.Integer(1), w=T),
                  'bubble': dict(count=1, sym=sp.Rational(1, 2), w=Sb)}
        a_g = -curves['triangle']['sym'] * T          # vertex counterterm cancels triangle pole
        a_phi = curves['bubble']['sym'] * Sb          # Z_phi - 1 (p^2 pole of -Pi, sign: Pi ~ +g^2*S*bubble)
        c = a_g - sp.Rational(3, 2) * a_phi
        b = 2 * c                                     # beta = -eps g + 2 c g^3
        return dict(Dc=Dc, b=sp.nsimplify(b), curves=curves)
    if name == 'planted':  # phi^4, Dc=4, L = lam/4! phi^4 ; s,t,u bubbles sym 1/2; no p^2 pole at 1 loop
        Dc = 4; D = Dc - 2*eps
        B = pole(2, D) * sp.integrate(1, (x, 0, 1))
        curves = {'bubble_stu': dict(count=3, sym=sp.Rational(1, 2), w=B)}
        a_l = 3 * sp.Rational(1, 2) * B               # Z_lam - 1 = +3/2 * B
        b = 2 * a_l                                   # beta = -2eps lam + 2 c lam^2
        return dict(Dc=Dc, b=sp.nsimplify(b), curves=curves)
    if name == 'broken':  # phi^3 in D=5: no log divergence (odd D) -> must be rejected
        D = 5 - 2*eps
        T = pole(3, D)
        if T == 0:
            raise SystemExit("REJECT: no UV 1/eps pole (odd dimension) - beta coefficient undefined at one loop")
        return dict(Dc=5, b=T, curves={})
    raise SystemExit("unknown mode")

if __name__ == '__main__':
    r = theory(sys.argv[1])
    print(f"mode={sys.argv[1]} Dc={r['Dc']} b={r['b']}")
    ws = sorted({str(sp.Abs(v['sym']*v['w'])) for v in r['curves'].values()})
    for k, v in r['curves'].items():
        print(f"curve {k}: count={v['count']} sym={v['sym']} pole_weight={v['w']}")
    print(f"distinct |sym*weight| values: {ws} universal_weight={len(ws)==1}")
