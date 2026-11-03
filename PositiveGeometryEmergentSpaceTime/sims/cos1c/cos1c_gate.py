"""COS-1c: spin-1 (Coulomb gauge) exchange wavefunction of charged conformally coupled scalars."""
import numpy as np, sympy as sp
out=[]
# T0: E->0 residue = Lorentz amplitude, solve for kappa
a,jL,jR,X,Y,k=sp.symbols('a jL jR X Y kappa')
NT=a-(jL*X)*(jR*X)/Y**2                       # J_L.Pi.J_R using J.Yvec = J0*X (null legs, E=0)
res=NT/((X+Y)*(Y-X))+k*jL*jR/Y**2
target=(a-jL*jR)/(Y**2-X**2)
ksol=sp.solve(sp.simplify(res-target),k)
out.append(f"T0 kappa from Lorentz residue: {ksol}  (hand derivation -1) -> {'OK' if ksol==[-1] else 'FAIL'}")
# also verify J0*X = J.Yvec numerically for null legs off energy shell
rng=np.random.default_rng(11); n=10**6
k=rng.normal(size=(n,3,3)); K=np.concatenate([k,-k.sum(1)[:,None]],1); w=np.linalg.norm(K,axis=2)
Yv=K[:,0]+K[:,1]; Yn=np.linalg.norm(Yv,axis=1)
JL0=w[:,0]-w[:,1]; JR0=w[:,2]-w[:,3]; JL=K[:,0]-K[:,1]; JR=K[:,2]-K[:,3]
XL=w[:,0]+w[:,1]; XR=w[:,2]+w[:,3]; E=XL+XR
out.append(f"T0 identity J_L0*X_L = J_L.Y holds: max dev {np.abs(JL0*XL-np.einsum('ij,ij->i',JL,Yv)).max():.1e}")
def psi(K,w):
    Yv=K[:,0]+K[:,1]; Y=np.linalg.norm(Yv,axis=1); u=Yv/Y[:,None]
    JL0=w[:,0]-w[:,1]; JR0=w[:,2]-w[:,3]; JL=K[:,0]-K[:,1]; JR=K[:,2]-K[:,3]
    XL=w[:,0]+w[:,1]; XR=w[:,2]+w[:,3]; E=XL+XR
    NT=np.einsum('ij,ij->i',JL,JR)-np.einsum('ij,ij->i',JL,u)*np.einsum('ij,ij->i',JR,u)
    return NT/(E*(XL+Y)*(XR+Y)) - JL0*JR0/(Y**2*E), (np.einsum('ij,ij->i',JL,JR)-JL0*JR0)
p,amp=psi(K,w)
pn=p*E  # dimensionless
out.append(f"T1 {n} physical points: frac psi>0 {np.mean(p>0):.4f}, psi<0 {np.mean(p<0):.4f}")
# T2 bisection along segments between opposite-sign configurations (interpolate 3-momenta k1..k3, k4 fixed by conservation)
pos=np.where(p>0)[0][:200]; neg=np.where(p<0)[0][:200]; zeros=[]; ampz=[]; mins=[]
for i,j in zip(pos,neg):
    A,B=k[i],k[j]; lo,hi=0.0,1.0
    f=lambda s: psi(*(lambda kk:(kk,np.linalg.norm(kk,axis=2)))(np.concatenate([((1-s)*A+s*B)[None],-((1-s)*A+s*B).sum(0)[None,None]],1)))
    for _ in range(60):
        mid=(lo+hi)/2; v=f(mid)[0][0]
        if v>0: lo=mid
        else: hi=mid
    kk=(1-lo)*A+lo*B; KK=np.concatenate([kk,-kk.sum(0)[None]]); ww=np.linalg.norm(KK,axis=1)
    pv,av=psi(KK[None],ww[None]); Yz=np.linalg.norm(KK[0]+KK[1])
    zeros.append(pv[0]*ww.sum()); ampz.append(av[0]/ww.sum()**2)
    mins.append(min(ww.sum(),ww[0]+ww[1]+Yz,ww[2]+ww[3]+Yz,Yz)/ww.sum())
out.append(f"T2 {len(zeros)} zeros by bisection: max |psi*E| at zero {np.max(np.abs(zeros)):.1e}; min normalised propagator scale {min(mins):.3e} (>0 => finite, physical)")
out.append(f"T3 flat-amplitude numerator (J_L.J_R)_Mink/E^2 on psi-zeros: median |.| {np.median(np.abs(ampz)):.3f}, frac with |.|<1e-3: {np.mean(np.abs(ampz)<1e-3):.3f}; overall corr sign(psi) vs sign(amp numerator): {np.mean(np.sign(p)==np.sign(amp)):.3f}")
print("\n".join(out))
