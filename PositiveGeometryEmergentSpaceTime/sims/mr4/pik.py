"""MR-4 Gate 1: tree-level pi+K+ -> pi+K+ (I=3/2) amplitude in SU(3) ChPT (GL85 Lagrangian),
brute-force expansion (reuses sims/mr2d/tree.py machinery), checks the conjectured hidden-zero line s = Mpi^2+MK^2."""
import sys, sympy as sp
sys.argv=['x']; sys.path.insert(0,'../mr2d')
src=open('../mr2d/tree.py').read().split("p2=sp.Symbol('p2')")[0]
exec(src)
E=lambda i,j: sp.Matrix(3,3,lambda a,b:1 if (a,b)==(i,j) else 0)
p2=sp.Symbol('p2')
def gam2(T,A,B): return sp.expand(evaluate(T,[(A,'a'),(B,'b')],lambda i,j:p2 if i==j else -p2))
out={}
for name,(A,B) in {'pi':(E(0,1),E(1,0)),'K':(E(0,2),E(2,0))}.items():
    g0=gam2(LO,A,B); g1=gam2(Lag4,A,B); n=g0.coeff(p2,1)
    m0=-g0.coeff(p2,0)/n; z=g1.coeff(p2,1)/n; dm=-g1.coeff(p2,0)/n
    out[name]=(m0,z,dm); print(name,'LO mass^2',m0)
Mp,MK,s,t=sp.symbols('Mp MK s t'); u=2*Mp**2+2*MK**2-s-t
# legs incoming: 1 pi+ (E01? ), 2 K+ , 3 pi- , 4 K-   ; s=(p1+p2)^2, t=(p1+p3)^2, u=(p1+p4)^2
m={1:Mp,2:MK,3:Mp,4:MK}
D={frozenset((1,2)):(s-Mp**2-MK**2)/2,frozenset((3,4)):(s-Mp**2-MK**2)/2,frozenset((1,3)):(t-2*Mp**2)/2,
   frozenset((2,4)):(t-2*MK**2)/2,frozenset((1,4)):(u-Mp**2-MK**2)/2,frozenset((2,3)):(u-Mp**2-MK**2)/2}
dot=lambda i,j:m[i]**2 if i==j else D[frozenset((i,j))]
legs=[(E(1,0),1),(E(2,0),2),(E(0,1),3),(E(0,2),4)]
V0=evaluate(LO,legs,dot); V1=evaluate(Lag4,legs,dot)
# express LO masses via physical: m0_pi = Mp^2(1+z)-dm ; first order
mpi0,zp,dmp=out['pi']; mK0,zK,dmK=out['K']
# solve chi entries ml2, ms2 in terms of physical (first order)
sol0=sp.solve([sp.Eq(mpi0,Mp**2),sp.Eq(mK0,MK**2)],[ml2,ms2],dict=True)[0]
shift_pi=(Mp**2*zp-dmp).subs(sol0); shift_K=(MK**2*zK-dmK).subs(sol0)
eps=sp.Symbol('eps')
sol1=sp.solve([sp.Eq(mpi0,Mp**2+eps*shift_pi),sp.Eq(mK0,MK**2+eps*shift_K)],[ml2,ms2],dict=True)[0]
V0p=sp.series(V0.subs(sol1),eps,0,2).removeO()
A=sp.expand(V0p.subs(eps,1) - (zp+zK).subs(sol0)*V0.subs(sol0) + V1.subs(sol0))
LOamp=sp.factor(V0.subs(sol0)); print('LO amp =',LOamp)
line=sp.expand(A.subs(s,Mp**2+MK**2)*F**4)
print('NLO on line s=Mp^2+MK^2, coefficients in t:')
for k in range(3): print(' t^%d:'%k, sp.factor(sp.expand(line).coeff(t,k)))
import pickle; pickle.dump((A,LOamp),open('pik.pkl','wb'))
