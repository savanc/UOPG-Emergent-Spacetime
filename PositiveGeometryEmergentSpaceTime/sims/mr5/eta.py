"""MR-5 gate: LO pi eta and K eta amplitudes (brute-force GL85 LO), look for a zero line."""
import sys, sympy as sp
src=open('../mr2d/tree.py').read().split("p2=sp.Symbol('p2')")[0]; exec(src)
E=lambda i,j: sp.Matrix(3,3,lambda a,b:1 if (a,b)==(i,j) else 0)
l8=sp.diag(1,1,-2)/sp.sqrt(3); l3=sp.diag(1,-1,0)
s,t=sp.symbols('s t'); ma,mb=sp.symbols('ma mb')
def amp(A1,B1,A2,B2):
    m={1:ma,2:mb,3:ma,4:mb}; u=2*ma**2+2*mb**2-s-t
    D={frozenset((1,2)):(s-ma**2-mb**2)/2,frozenset((3,4)):(s-ma**2-mb**2)/2,frozenset((1,3)):(t-2*ma**2)/2,
       frozenset((2,4)):(t-2*mb**2)/2,frozenset((1,4)):(u-ma**2-mb**2)/2,frozenset((2,3)):(u-ma**2-mb**2)/2}
    dot=lambda i,j:m[i]**2 if i==j else D[frozenset((i,j))]
    return sp.factor(evaluate(LO,[(A1,1),(B1,2),(A2,3),(B2,4)],dot))
Mp,MK,Me=sp.symbols('Mp MK Me')
# LO masses: pi: m2l ; K: (m2l+m2s)/2 ; eta: (m2l+2 m2s)/3
sub_pe={ml2:Mp**2, ms2:sp.Rational(3,2)*Me**2-Mp**2/2}
print('pi0 eta:',sp.factor(amp(l3,l8,l3,l8).subs(sub_pe).subs({ma:Mp,mb:Me})))
sub_ke={ml2:Mp**2, ms2:2*MK**2-Mp**2}
print('K+ eta:',sp.factor(amp(E(0,2),l8,E(2,0),l8).subs(sub_ke).subs({ma:MK,mb:Me})))
