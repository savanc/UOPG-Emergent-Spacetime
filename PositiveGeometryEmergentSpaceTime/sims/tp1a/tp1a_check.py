"""TP-1a numeric cross-check: sin(k pi/(n+1)) is the PF eigenvector of A_n (n=1..8), eigenvalue 2cos(pi/(n+1))."""
import numpy as np
for n in range(1,9):
    A=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
    x=np.sin(np.arange(1,n+1)*np.pi/(n+1)); lam=2*np.cos(np.pi/(n+1))
    w,v=np.linalg.eigh(A); pf=v[:,-1]*np.sign(v[:,-1].sum())
    print(f"A{n}: ||Ax-lam x||={np.linalg.norm(A@x-lam*x):.1e}, lam_PF-lam={w[-1]-lam:.1e}, ratio dev={np.max(np.abs(pf/pf[0]-x/x[0])):.1e}")
