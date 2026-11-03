"""MR-1c: scan LS isospin-projected residues (levels n=1..6) for exact partial-wave zeros.
Units m_rho^2=1, alpha(s)=1/2+s/2, massless pions, t=-s(1-x)/2. Even part (A_st+A_su) -> I=0, odd -> I=1."""
import sympy as sp
x=sp.symbols('x')
for n in range(1,7):
    s=2*n-1; at=sp.Rational(1,2)-sp.Rational(s,4)*(1-x)
    r=sp.prod([(-at-k) for k in range(n)]); ru=r.subs(x,-x)
    for name,R,par in [('I0(even)',r+ru,0),('I1(odd)',r-ru,1)]:
        c=[sp.nsimplify(sp.integrate(sp.expand(R*sp.legendre(J,x)),(x,-1,1))*(2*J+1)/2) for J in range(n+1)]
        z=[J for J in range(n+1) if J%2==par and c[J]==0]
        print(f"n={n} m2={s} {name} coeffs={c} accidental_zeros={z}")
