"""SG-1 gate: Perron-Frobenius spectra of ADE graphs (control: E8 Toda) and scale check."""
import numpy as np, itertools
from math import cos, pi, sqrt
def adj(edges,n):
    A=np.zeros((n,n));
    for i,j in edges: A[i,j]=A[j,i]=1
    return A
def An(n): return adj([(i,i+1) for i in range(n-1)],n)
def Dn(n): return adj([(i,i+1) for i in range(n-2)]+[(n-3,n-1)],n)
def En(n): return adj([(i,i+1) for i in range(n-2)]+[(2,n-1)],n)  # chain 0..n-2, branch at node 2
def pf(A):
    w,v=np.linalg.eigh(A); k=np.argmax(w); x=v[:,k]; x=x*np.sign(x.sum()); return w[k],x
out=[]
# Control C
lam,x=pf(En(8)); m=np.sort(x)/np.min(x)
c=cos; m2=2*c(pi/5)
closed=np.sort([1,m2,2*c(pi/30),2*m2*c(7*pi/30),2*m2*c(2*pi/15),2*m2*c(pi/30),4*m2*c(pi/5)*c(7*pi/30),4*m2*c(pi/5)*c(2*pi/15)])
out.append(f"C: PF eigenvalue {lam:.15f} vs 2cos(pi/30) {2*c(pi/30):.15f} diff {abs(lam-2*c(pi/30)):.1e}")
out.append(f"C: all components >0: {bool((x>0).all())}")
out.append("C: PF ratios  "+" ".join(f"{t:.12f}" for t in m))
out.append("C: closed     "+" ".join(f"{t:.12f}" for t in closed))
out.append(f"C: max |diff| {np.max(np.abs(m-closed)):.2e}; m2/m1={m[1]:.12f} phi={(1+sqrt(5))/2:.12f}")
okC = abs(lam-2*c(pi/30))<1e-12 and np.max(np.abs(m-closed))<1e-12
# G1
okG1=True
for name,f,rng in [("A",An,range(1,9)),("D",Dn,range(4,9)),("E",En,range(6,9))]:
    for n in rng:
        lam,x=pf(f(n)); h=(n+1) if name=="A" else (2*n-2) if name=="D" else {6:12,7:18,8:30}[n]
        pos=(x>1e-12).all(); okeig=abs(lam-2*cos(pi/h))<1e-12
        okG1&=bool(pos and okeig)
        out.append(f"G1 {name}{n}: PF>0 {pos}, lambda=2cos(pi/h) h={h}: {okeig}, ratios {np.round(np.sort(x)/x.min(),6).tolist()}")
# G2: homogeneity. PF vector of A: A(cx)=lam(cx) for every c>0 -> unit free.
lam,x=pf(En(8))
for cfac in [0.1,1,91.19]:
    out.append(f"G2: c={cfac}: ||A(cx)-lam(cx)||={np.linalg.norm(En(8)@(cfac*x)-lam*cfac*x):.1e}")
# KK x PF: M_{a,n}^2 = (mu x_a)^2 + (n/R)^2 ; only dimensionless combo mu*R; scan shows spectrum ratios depend continuously on it
for muR in [0.1,1.0,10.0]:
    spec=sorted(np.sqrt((muR*x/x.min())**2+np.arange(0,3)[:,None]**2).ravel())
    out.append(f"G2: mu*R={muR}: lowest ratios {np.round(np.array(spec[:5])/spec[0],6).tolist()}")
# PF of the combined positive operator A (x) 1 + 1 (x) T_KK (truncated tower graph) - eigenvector is product of PF vectors; still 2 free units
T=An(6); B=np.kron(En(8),np.eye(6))+np.kron(np.eye(8),T)
lb,xb=pf(B); la,xa=pf(En(8)); lt,xt=pf(T)
out.append(f"G2: PF(A(x)1+1(x)T) = PF(A)+PF(T): {abs(lb-la-lt):.1e}; eigvec = product: {np.linalg.norm(np.abs(xb)-np.abs(np.kron(xa,xt))):.1e}")
out.append(f"VERDICT C={'PASS' if okC else 'FAIL'} G1={'PASS' if okG1 else 'FAIL'} G2=FAIL (scale freedom survives: PF eigenvectors are projective; KK adds an independent unit 1/R; mu*R unconstrained)")
print("\n".join(out))
