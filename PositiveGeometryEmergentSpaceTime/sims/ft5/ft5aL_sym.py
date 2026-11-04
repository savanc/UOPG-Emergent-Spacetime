# Symbolic 4-pt contact term of O_L0 and O_B (exp parametrisation), in terms of x_ij = p_i.p_j.
import sympy as sp, itertools
from math import factorial
x={}
for i in range(4):
    for j in range(4): x[(i,j)]=sp.Symbol(f'x{min(i,j)}{max(i,j)}')
c=[sp.I**k/factorial(k) for k in range(6)]; cb=[sp.conjugate(z) for z in c]
def comps(m,F):
    if F==0:
        if m==0: yield []
        return
    for k in range(1,m+1):
        for r in comps(m-k,F-1): yield [k]+r
def V(fac):
    tot=0
    for r in range(4):
        for ks in comps(4,len(fac)):
            pos=r; val=1; moms={}
            for (t,ix),k in zip(fac,ks):
                val*= (c if t=='U' else cb)[k]; legs=[(pos+j)%4 for j in range(k)]; moms.setdefault(ix,[]).append(legs); pos+=k
            for ix,(A,B) in moms.items(): val*=-sum(x[(a,b)] for a in A for b in B)
            tot+=val
    return sp.expand(sp.I*tot*(-sp.I))   # vertex i*L, M = -i * (i L)
L0=V([('U','m'),('Ud','n'),('U','m'),('Ud','n')]); B=V([('U','m'),('Ud','m'),('U','n'),('Ud','n')])
print('T_L0 =',L0); print('T_B =',B)
