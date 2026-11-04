"""TP-1b: E8 eigenvector recursion from node 6, consistency polynomial P(c)."""
import sympy as sp, numpy as np
c=sp.symbols('c')
x={6:sp.Integer(1)}
x[5]=c*x[6]                 # node 6: x5 = c x6
x[4]=sp.expand(c*x[5]-x[6]) # node 5: x4 + x6 = c x5
x[3]=sp.expand(c*x[4]-x[5]) # node 4
x[2]=sp.expand(c*x[3]-x[4]) # node 3
# node 7 (leaf on 2): x2 = c x7 -> x7 = x2/c ; avoid division: rescale all by c
x={k:sp.expand(c*v) for k,v in x.items()}; x[7]=sp.expand(x[2]/c)
# node 2: x1 + x3 + x7 = c x2 -> x1
x[1]=sp.expand(c*x[2]-x[3]-x[7])
x[0]=sp.expand(c*x[1]-x[2])  # node 1: x0 + x2 = c x1
P=sp.factor(sp.expand(c*x[0]-x[1]))  # node 0: x1 = c x0
print("x components:"); [print(f"  x{k} = {x[k]}") for k in range(8)]
print("P(c) =",P)
roots=[complex(r) for r in sp.Poly(sp.expand(P),c).nroots()]
print("roots:",sorted(r.real for r in roots))
print("2cos(pi/30) =",2*np.cos(np.pi/30))
cs=2*np.cos(np.pi/30); print("x(c*) =",[float(x[k].subs(c,cs)) for k in range(8)])
