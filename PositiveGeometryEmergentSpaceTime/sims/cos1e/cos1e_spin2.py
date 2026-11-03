"""COS-1e': flat spin-2 exchange wavefunction between massless scalars; residue-matched instantaneous kernel and its off-shell lifts."""
import numpy as np, sympy as sp
out=[]
# ---- T1 symbolic: (N - N_TT)/(Y^2 - X^2) with conservation T^{z nu} = (X/Y) T^{0 nu}
X,Y=sp.symbols('X Y',positive=True)
def Tm(n):
    t00,t01,t02,t11,t12,t22=sp.symbols(f'{n}00 {n}01 {n}02 {n}11 {n}12 {n}22')
    M=sp.zeros(4,4); M[0,0]=t00;M[0,1]=M[1,0]=t01;M[0,2]=M[2,0]=t02;M[1,1]=t11;M[1,2]=M[2,1]=t12;M[2,2]=t22
    M[0,3]=M[3,0]=X/Y*t00;M[1,3]=M[3,1]=X/Y*t01;M[2,3]=M[3,2]=X/Y*t02;M[3,3]=(X/Y)**2*t00
    return M
eta=sp.diag(-1,1,1,1); A=Tm('a'); B=Tm('b'); lowB=eta*B*eta
tr=lambda M: sum(eta[i,i]*M[i,i] for i in range(4))
N=sum(A[i,j]*lowB[i,j] for i in range(4) for j in range(4))-sp.Rational(1,2)*tr(A)*tr(B)
tt=lambda M: (lambda t: t-sp.eye(2)*t.trace()/2)(sp.Matrix([[M[1,1],M[1,2]],[M[2,1],M[2,2]]]))
NTT=sum(tt(A)[i,j]*tt(B)[i,j] for i in range(2) for j in range(2))
I=sp.cancel((N-NTT)/(Y**2-X**2))
out.append(f"T1 kernel I = {I}")
out.append(f"T1 explicit X-dependence remains: {I.has(X)} -> off-shell lift of X^2 a00 b00 not fixed by the residue")
# ---- numerics
def comps(T,u):
    P=np.eye(3)-np.outer(u,u); a00=T[0,0]; a0p=P@T[0,1:]; S=T[1:,1:]; Sp=P@S@P; trp=np.trace(Sp); TT=Sp-P*trp/2
    return a00,a0p,trp,TT
def tensor(p1,p2):
    d=-p1[0]*p2[0]+p1[1:]@p2[1:]; etaU=np.diag([-1,1,1,1])
    return np.outer(p1,p2)+np.outer(p2,p1)-etaU*d
def lorentzN(TL,TR):
    e=np.diag([-1.,1,1,1]); TRl=e@TR@e
    return np.sum(TL*TRl)-0.5*np.trace(e@TL)*np.trace(e@TR)
def psi(k,w,lift,c=0.0):
    p=[np.concatenate([[w[i]],k[i]]) for i in range(4)]
    TL=tensor(p[0],p[1]); TR=tensor(p[2],p[3]); Yv=k[0]+k[1]; Yn=np.linalg.norm(Yv); u=Yv/Yn
    XL=w[0]+w[1]; XR=w[2]+w[3]; E=XL+XR
    a00,a0p,atr,aTT=comps(TL,u); b00,b0p,btr,bTT=comps(TR,u)
    X2={"XL2":XL**2,"XR2":XR**2,"mXLXR":-XL*XR,"fam":-XL*XR+c*E*(XL-XR)/2}[lift]
    I=((Yn**2-X2)*a00*b00+Yn**2*(a00*btr+atr*b00)-4*Yn**2*(a0p@b0p))/(2*Yn**4)
    return np.sum(aTT*bTT)/(E*(XL+Yn)*(XR+Yn))+I/E, (TL,TR,XL,Yn,E)
# residue check at E=0 using negative-energy null legs 3,4 (|k3|+|k4| = |k1|+|k2|)
rng=np.random.default_rng(5); dev=[]
for _ in range(200):
    k1,k2=rng.normal(size=(2,3)); Yv=k1+k2; S=np.linalg.norm(k1)+np.linalg.norm(k2)
    d=rng.normal(size=3); d/=np.linalg.norm(d)
    g=lambda t: np.linalg.norm(-Yv/2+t*d)+np.linalg.norm(-Yv/2-t*d)-S
    lo,hi=0,10*S
    for _ in range(200):
        m=(lo+hi)/2; (lo,hi)=(m,hi) if g(m)<0 else (lo,m)
    k3=-Yv/2+lo*d; k4=-Yv/2-lo*d; k=np.array([k1,k2,k3,k4]); w=np.array([np.linalg.norm(k1),np.linalg.norm(k2),-np.linalg.norm(k3),-np.linalg.norm(k4)])
    p=[np.concatenate([[w[i]],k[i]]) for i in range(4)]; TL=tensor(p[0],p[1]); TR=tensor(p[2],p[3])
    XL=w[0]+w[1]; Yn=np.linalg.norm(Yv); u=Yv/Yn
    a00,a0p,atr,aTT=comps(TL,u); b00,b0p,btr,bTT=comps(TR,u)
    lhs=np.sum(aTT*bTT)/(Yn**2-XL**2)+((Yn**2-XL**2)*a00*b00+Yn**2*(a00*btr+atr*b00)-4*Yn**2*(a0p@b0p))/(2*Yn**4)
    rhs=lorentzN(TL,TR)/(Yn**2-XL**2); dev.append(abs(lhs-rhs)/max(1e-12,abs(rhs)))
out.append(f"T1 residue check at E=0 (negative-energy null legs, 200 pts): max rel dev {max(dev):.1e} (median {np.median(dev):.1e})")
# T2 physical sampling for lifts
n=10**5; k=rng.normal(size=(n,3,3)); K=np.concatenate([k,-k.sum(1)[:,None]],1); W=np.linalg.norm(K,axis=2)
res={}
for name,c in [("XL2",0),("XR2",0),("mXLXR",0),("fam",-1.0),("fam",1.0)]:
    v=np.array([psi(K[i],W[i],name,c)[0] for i in range(n)]); res[(name,c)]=np.sign(v)
    out.append(f"T2 lift {name}{'' if name!='fam' else f' c={c}'}: frac psi>0 {np.mean(v>0):.4f}, <0 {np.mean(v<0):.4f}")
base=res[("mXLXR",0)]
for key,s in res.items():
    out.append(f"T2 sign disagreement vs -X_L X_R lift: {key}: {np.mean(s!=base):.4f}")
print("\n".join(out))
# T2b: margin of the symmetric lift (dimensionless psi*E^? : psi ~ [mom^4]/[mom^3] -> psi/E)
v=np.array([psi(K[i],W[i],"mXLXR")[0]/W[i].sum() for i in range(n)])
print(f"T2b symmetric lift -X_L X_R: min psi/E_tot = {v.min():.3e}, 0.01% quantile {np.quantile(v,1e-4):.3e}")
