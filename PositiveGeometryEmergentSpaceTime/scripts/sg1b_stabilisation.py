"""SG-1b: does a Casimir / PF-style condition fix t = mu*R for an E8 PF-weighted KK tower?"""
import numpy as np
def adj(edges,n):
    A=np.zeros((n,n))
    for i,j in edges: A[i,j]=A[j,i]=1
    return A
def An(n): return adj([(i,i+1) for i in range(n-1)],n)
def En(n): return adj([(i,i+1) for i in range(n-2)]+[(2,n-1)],n)
def pf(A):
    w,v=np.linalg.eigh(A); k=np.argmax(w); x=v[:,k]; x=x*np.sign(x.sum()); return w[k],x
lam,x=pf(En(8)); m=np.sort(x)/x.min()          # mu = 1
N=np.arange(1,400)
f=lambda z:(3+3*z+z*z)*np.exp(-z)
def rho(L, masses, sign, alt):
    c=(-1.0)**N if alt else np.ones_like(N,dtype=float)
    return sign*sum((c*f(np.outer([mm*L],N)[0])/N**5).sum() for mm in masses)/L**5
Ls=np.geomspace(0.05,60,6000)
def minima(V):
    i=np.where((V[1:-1]<V[:-2])&(V[1:-1]<V[2:]))[0]+1
    return [(round(Ls[k]/(2*np.pi),4)) for k in i]   # t* = mu R = L/(2 pi)
out=[]
frames={"rho":0,"L*rho":1,"rho/L":-1,"L^-2 * L*rho (Einstein)":-1-0}  # report several frame powers
def report(name,V):
    for p in [0,1,-1,-2]:
        out.append(f"{name}: frame L^{p}*rho minima at t* = {minima(V*Ls**p)}")
# S1a: E8 bosons, periodic
Vb=np.array([rho(L,m,-1,False) for L in Ls]); report("S1a bosons periodic",Vb)
# S1b: + Scherk-Schwarz fermions with identical PF masses, equal dof
Vss=Vb+np.array([rho(L,m,+1,True) for L in Ls]); report("S1b bosons + SS fermions",Vss)
# S2: E8 bosons + N_f massless periodic fermions
for Nf in [1,4,8,9,16,32]:
    V=Vb+np.array([rho(L,[0.0]*Nf,+1,False) for L in Ls])
    out.append(f"S2 Nf={Nf}: minima rho {minima(V)}; maxima rho {[round(Ls[k]/(2*np.pi),4) for k in (np.where((V[1:-1]>V[:-2])&(V[1:-1]>V[2:]))[0]+1)]}")
# S2': E8 bosons + Nf SS-massless fermions + periodic massive fermion of PF mass m_a (one choice each)
for a in range(8):
    V=Vb+np.array([rho(L,[m[a]],+1,False)*8 for L in Ls])
    out.append(f"S2' bosons + 8 periodic fermions of mass m_{a+1}: minima t*={minima(V)}")
# S3: PF of A (x) 1 + kappa 1 (x) T_KK
T=An(10); la=lam; lt,_=pf(T); prev=None; cross=0; ks=np.linspace(0.01,5,2000)
gaps=[]
for k in ks:
    w=np.sort(np.linalg.eigvalsh(np.kron(En(8),np.eye(10))+k*np.kron(np.eye(8),T)))[::-1]
    gaps.append(w[0]-w[1])
gaps=np.array(gaps)
out.append(f"S3: PF eigenvalue = lam_A + kappa*lam_T for all kappa (max dev {max(abs(np.sort(np.linalg.eigvalsh(np.kron(En(8),np.eye(10))+k*np.kron(np.eye(8),T)))[-1]-la-k*lt) for k in ks):.1e}); min PF gap {gaps.min():.3f} > 0 => PF level never crosses, no kappa singled out")
wa=np.linalg.eigvalsh(En(8)); wt=np.linalg.eigvalsh(T)
ks_cross=set()
for i in range(8):
  for i2 in range(8):
    for j in range(10):
      for j2 in range(10):
        d=wt[j2]-wt[j]
        if abs(d)>1e-12:
          k=(wa[i]-wa[i2])/d
          if k>1e-9: ks_cross.add(round(k,9))
out.append(f"S3: distinct kappa>0 with some (non-PF) level crossing: {len(ks_cross)} values in ({min(ks_cross):.4f}, {max(ks_cross):.4f}) -> no unique kappa; picking one is a discrete input")
print("\n".join(out))
