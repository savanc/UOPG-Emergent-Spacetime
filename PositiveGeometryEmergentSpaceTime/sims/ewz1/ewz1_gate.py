# EW-Z1 gate: HEFT Goldstone 4-pt (equivalence theorem), F(h)=1+2a h/v+b h^2/v^2.
# O(4)->O(3) ordered amplitude A(1234)=A(s)+A(u) (SU(2)xSU(2) trace basis); hidden zero locus t=0 (massless pions).
import sympy as sp
s,u,a,m,v=sp.symbols('s u a m v')
A=lambda x: x/v**2 - a**2*x**2/(v**2*(x-m**2))
ordered=sp.simplify(A(s)+A(u))
at0=sp.factor(ordered.subs(u,-s))
print("ordered A(1234) at t=0:",at0)
print("solutions for a (m!=0):",sp.solve(sp.numer(sp.together(at0)),a))
print("m=0:",sp.simplify(at0.subs(m,0)))
# unitarity (CLT / Llewellyn Smith): large-s growth of A(s)
print("A(s) s->inf leading:",sp.limit(A(s)*v**2/s,s,sp.oo))
