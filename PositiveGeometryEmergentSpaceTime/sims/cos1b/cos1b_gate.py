"""COS-1b: ordered 4-pt NLSM-type contact wavefunction numerator N_c = p1.p3 + p2.p4 + c E^2 (mostly plus)."""
import numpy as np, sympy as sp
rng=np.random.default_rng(7); n=10**6
k=rng.normal(size=(n,3,3)); K=np.concatenate([k,-k.sum(1)[:,None]],1); w=np.linalg.norm(K,axis=2)
dot=lambda i,j: -w[:,i]*w[:,j]+np.einsum('ij,ij->i',K[:,i],K[:,j])
N0=dot(0,2)+dot(1,3); E=w.sum(1); r=-N0/E**2
out=[f"T1 c=0: max N0 = {N0.max():.3e} (<=0 expected), any >0: {bool((N0>0).any())}, min |N0|/E^2 = {np.abs(N0/E**2).min():.3e}",
     f"T2 zero needs c = -N0/E^2 in [{r.min():.4e}, {r.max():.4f}] over physical scan -> every c in (0, {r.max():.3f}] puts zeros in the physical region; c<=0 none"]
# collinear check: k1=k3=a, k2=k4=-a -> N0 = 0
a=np.array([0.3,-1.2,0.5]); KK=np.array([a,-a,a,-a]); ww=np.linalg.norm(KK,axis=1)
d=lambda i,j:-ww[i]*ww[j]+KK[i]@KK[j]
out.append(f"T1 collinear k1=k3=a,k2=k4=-a: N0 = {d(0,2)+d(1,3):.2e} (boundary zero)")
# analytic bound: p_i.p_j = -|k_i||k_j|(1-cos) <= 0
x,y,cth=sp.symbols('x y c',positive=True)
out.append(f"T1 analytic: p_i.p_j = -|k_i||k_j|(1-cos theta_ij) = {sp.factor(-x*y+x*y*cth)} <= 0 for |cos|<=1, =0 iff parallel")
# T3: residue at E->0 independent of c: N_c/E has residue N_c|_{E=0} = N0|_{E=0}
c,Es=sp.symbols('c E'); out.append(f"T3 residue of (N0 + c E^2)/E at E=0: {sp.residue((sp.Symbol('N0')+c*Es**2)/Es,Es,0)} -> c-independent")
print("\n".join(out))
