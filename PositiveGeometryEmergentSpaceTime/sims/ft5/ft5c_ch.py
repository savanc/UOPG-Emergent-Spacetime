import numpy as np
from fractions import Fraction
rng=np.random.default_rng(20261013)
def ah(N):  # random traceless anti-Hermitian
    X=rng.normal(size=(N,N))+1j*rng.normal(size=(N,N)); H=X-X.conj().T; return H-np.trace(H)/N*np.eye(N)
def feats(N):
    A=[ah(N) for _ in range(4)]; tr=np.trace
    L0=sum(tr(A[m]@A[n]@A[m]@A[n]) for m in range(4) for n in range(4))
    O3=sum(tr(A[m]@A[m]@A[n]@A[n]) for m in range(4) for n in range(4))
    O1=sum(tr(A[m]@A[m]) for m in range(4))**2
    O2=sum(tr(A[m]@A[n])**2 for m in range(4) for n in range(4))
    return L0,[O3,O1,O2]
for N in (3,4):
    rows=[feats(N) for _ in range(60)]
    y=np.array([r[0] for r in rows]); X=np.array([r[1] for r in rows])
    co,*_=np.linalg.lstsq(X,y,rcond=None); res=np.max(np.abs(X@co-y))/np.max(np.abs(y))
    print(f"N={N} a,b,c =",np.round(co.real,10),"max rel residual",f"{res:.2e}",
          "rational:",[str(Fraction(float(x.real)).limit_denominator(100)) for x in co])
