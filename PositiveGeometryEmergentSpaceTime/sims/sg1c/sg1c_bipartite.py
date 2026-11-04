"""SG-1c: E8 bipartite colouring -> bosons/fermions; does the Casimir potential fix t = mu R?"""
import numpy as np
def adj(edges,n):
    A=np.zeros((n,n))
    for i,j in edges: A[i,j]=A[j,i]=1
    return A
A=adj([(i,i+1) for i in range(6)]+[(2,7)],8)
w,v=np.linalg.eigh(A); x=v[:,-1]; x=x*np.sign(x.sum()); m=x/x.min()
col=np.array([i%2 for i in range(7)]+[1])           # node 7 attached to node 2 (even) -> odd class
assert all(col[i]!=col[j] for i in range(8) for j in range(8) if A[i,j])
light=int(np.argmin(m)); bos=col==col[light]
out=[f"PF masses by node: {np.round(m,6).tolist()}", f"colour classes: {col.tolist()}; lightest node {light} (class {col[light]})",
     f"boson class masses {np.round(np.sort(m[bos]),4).tolist()}; fermion class masses {np.round(np.sort(m[~bos]),4).tolist()}"]
N=np.arange(1,400); f=lambda z:(3+3*z+z*z)*np.exp(-z)
def rho(L,ms,sign,alt):
    c=(-1.0)**N if alt else np.ones(len(N))
    return sign*sum((c*f(mm*L*N)/N**5).sum() for mm in ms)/L**5
Ls=np.geomspace(0.05,60,6000)
def ext(V):
    mi=np.where((V[1:-1]<V[:-2])&(V[1:-1]<V[2:]))[0]+1
    return [round(Ls[k]/(2*np.pi),4) for k in mi]
rules={"R1":(m[bos],m[~bos],False),"R2":(m[~bos],m[bos],False),"R3":(m[bos],m[~bos],True),"R4":(m[~bos],m[bos],True)}
for r,(B,F,alt) in rules.items():
    V=np.array([rho(L,B,-1,False)+rho(L,F,+1,alt) for L in Ls])
    out.append(r+": "+"; ".join(f"p={p}: min t*={ext(V*Ls**p)}" for p in [0,1,-1,-2]))
print("\n".join(out))
# Control: reproduce SG-1b S2' (all 8 bosons + 8 periodic fermions of mass m_2 = phi) -> expected t* ~ 0.7577
Vc=np.array([rho(L,m,-1,False)+8*rho(L,[np.sort(m)[1]],+1,False) for L in Ls])
print(f"CONTROL SG-1b S2' m2: t*={ext(Vc)} (expected [0.7577])")
for r,(B,F,alt) in rules.items():
    V=np.array([rho(L,B,-1,False)+rho(L,F,+1,alt) for L in Ls])
    print(f"{r}: sign of V*L^5 at L=0.05,1,10: {np.sign(V[[0,np.searchsorted(Ls,1),np.searchsorted(Ls,10)]]*1).tolist()}, monotone: {bool(np.all(np.diff(V)>=0) or np.all(np.diff(V)<=0))}")
