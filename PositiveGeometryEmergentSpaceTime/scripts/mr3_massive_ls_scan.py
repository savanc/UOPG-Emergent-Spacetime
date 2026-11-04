"""MR-3 well-posedness: is m_pi/m_rho fixed by Adler-zero LS + positivity?
Massive Lovelace-Shapiro ordered amplitude M(s,u) = -G(1-a_s)G(1-a_u)/G(1-a_s-a_u), a(x)=a0+ap*x.
Units m_rho^2 = 1, r = m_pi^2/m_rho^2.  Adler (Lovelace) zero at s=u=m_pi^2: 2a0+2ap*r = 1;
rho on leading trajectory: a0+ap = 1.  => ap = 1/(2(1-r)), a0 = (1-2r)/(2(1-r)).
Level n pole at a_s = n, residue polynomial R_n(u) = prod_{j<n}(a_u+j)/(n-1)!,
u = -(s-4r)(1-x)/2.  Positivity (Albert-Rastelli eq.19): all Legendre coefficients >= 0.
Exact rational arithmetic (sympy)."""
import sympy as sp
x = sp.symbols('x')
def coeffs(r, n):
    ap = sp.Rational(1,2)/(1-r); a0 = (1-2*r)*ap
    s = (n - a0)/ap
    if s <= 4*r: return None
    u = -(s-4*r)*(1-x)/2
    R = sp.prod([a0+ap*u+j for j in range(n)])/sp.factorial(n-1)
    R = sp.Poly(sp.expand(R), x)
    return [sp.nsimplify(sp.integrate(R.as_expr()*sp.legendre(J,x),(x,-1,1))*sp.Rational(2*J+1,2)) for J in range(n+1)]
NMAX = 8
grid = [sp.Rational(k,400) for k in range(0,100)]  # r in [0, 0.2475] i.e. m_pi/m_rho in [0, 0.497]
bad = []
for r in grid:
    for n in range(1,NMAX+1):
        c = coeffs(r,n)
        if c is None: continue
        if min(c) < 0: bad.append((r,n,[float(v) for v in c])); break
ok = [r for r in grid if r not in [b[0] for b in bad]]
print("grid points:", len(grid), "all-levels-positive (n<=%d):"%NMAX, len(ok))
if bad: print("first failures:", [(float(b[0]), b[1]) for b in bad[:10]])
print("max positive r:", float(max(ok)), "-> m_pi/m_rho up to", float(sp.sqrt(max(ok))))
r0 = sp.Rational(324,10000)  # (0.18)^2 example
print("level-1 coefficients at r=0.0324:", coeffs(r0,1))
# KSRF-type ratio  g~_rho^2 = g^2 f^2/m_rho^2  (Albert-Rastelli normalisation, eq.68,92)
# M ~ lam*pi*ap*(s+u) at low energy (massless) -> g10 = lam*pi*ap ; J=1 rho residue = lam*c1/ap -> g^2 m^2 = lam*c1/ap
lam = sp.symbols('lam', positive=True)
ap = sp.Rational(1,2); c1 = coeffs(sp.Integer(0),1)[1]
g2 = lam*c1/ap; g10 = lam*sp.pi*ap
print("chiral limit: J=1 coefficient", c1, " g~rho^2 =", sp.simplify(g2/(2*g10)), "=", float(g2/(2*g10)), " (KSRF: 1/2)")
# check normalisation against AR eq.75: g~2 = ln 2
s_ = sp.symbols('s'); M = -sp.gamma(sp.Rational(1,2)-s_/2)*sp.gamma(sp.Rational(1,2))/sp.gamma(-s_/2)
ser = sp.series(M, s_, 0, 3).removeO()
print("g~2(LS) =", sp.N(ser.coeff(s_,2)/ser.coeff(s_,1)), " AR eq.75: ln2 =", float(sp.log(2)))
print("g10 check (pi*ap):", sp.N(ser.coeff(s_,1)), float(sp.pi/2))
