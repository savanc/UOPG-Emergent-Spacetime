"""COS-1d: structure of the zero surface of the Coulomb-gauge photon-exchange wavefunction (COS-1c)."""
import numpy as np, sympy as sp
out=[]
a,jL,jR,XL,XR,Y=sp.symbols('a jL jR X_L X_R Y')   # a = spatial J_L.J_R
E=XL+XR
# psi = [J_L.Pi.J_R]/(E(XL+Y)(XR+Y)) - jL jR/(Y^2 E);  J_L.Yv = jL XL ; J_R.Yv = -jR XR
JLY=jL*XL; JRY=-jR*XR
psi=(a-JLY*JRY/Y**2)/(E*(XL+Y)*(XR+Y)) - jL*jR/(Y**2*E)
P=sp.factor(sp.numer(sp.together(psi))); D=sp.factor(sp.denom(sp.together(psi)))
M=a-jL*jR
out.append(f"T1 numerator P = {P}")
out.append(f"T1 denominator D = {D}")
cand=Y*(Y*M - E*jL*jR)
ratio=sp.simplify(sp.expand(sp.numer(sp.together(psi)))/sp.expand(cand))
out.append(f"T1 P / [Y (Y*M - E*jL*jR)] = {ratio}  -> S2 form with alpha=Y, beta=E, G=jL*jR=(w1-w2)(w3-w4)")
# T2 numeric on regenerated zeros
rng=np.random.default_rng(11); n=10**6
k=rng.normal(size=(n,3,3)); K=np.concatenate([k,-k.sum(1)[:,None]],1); w=np.linalg.norm(K,axis=2)
def parts(K,w):
    Yv=K[:,0]+K[:,1]; Yn=np.linalg.norm(Yv,axis=1); u=Yv/Yn[:,None]
    JL0=w[:,0]-w[:,1]; JR0=w[:,2]-w[:,3]; JL=K[:,0]-K[:,1]; JR=K[:,2]-K[:,3]
    XLn=w[:,0]+w[:,1]; XRn=w[:,2]+w[:,3]; En=XLn+XRn
    NT=np.einsum('ij,ij->i',JL,JR)-np.einsum('ij,ij->i',JL,u)*np.einsum('ij,ij->i',JR,u)
    ps=NT/(En*(XLn+Yn)*(XRn+Yn))-JL0*JR0/(Yn**2*En)
    Mn=np.einsum('ij,ij->i',JL,JR)-JL0*JR0
    return ps, Yn*Mn-En*JL0*JR0, En
p,F,En=parts(K,w)
pos=np.where(p>0)[0][:200]; neg=np.where(p<0)[0][:200]; res=[]
for i,j in zip(pos,neg):
    A,B=k[i],k[j]; lo,hi=0.0,1.0
    def ev(s):
        kk=(1-s)*A+s*B; KK=np.concatenate([kk,-kk.sum(0)[None]])[None]; return parts(KK,np.linalg.norm(KK,axis=2))
    for _ in range(60):
        mid=(lo+hi)/2
        if ev(mid)[0][0]>0: lo=mid
        else: hi=mid
    _,Fz,Ez=ev(lo); res.append(abs(Fz[0])/Ez[0]**3)
out.append(f"T2 factored form Y*M - E*jL*jR at 200 zeros: max |.|/E^3 = {max(res):.1e}")
out.append(f"T2 sign agreement sign(psi)==sign(Y M - E jL jR) on 1e6 points: {np.mean(np.sign(p)==np.sign(F)):.6f}")
# T3 S1 test: c13=c24=0 with null legs forces collinear kinematics k3=l*k1, k4=m*k2, k2 antiparallel to k1
vals=[]
for _ in range(2000):
    k1=rng.normal(size=3); l,m=rng.uniform(0.1,3,2); k2=-(1+l)/(1+m)*k1
    KK=np.array([k1,k2,l*k1,m*k2])[None]; ww=np.linalg.norm(KK,axis=2)
    if np.linalg.norm(KK[0,0]+KK[0,1])<1e-9: continue
    vals.append(parts(KK,ww)[0][0]*ww.sum())
vals=np.array(vals)
out.append(f"T3 on c13=c24=0 locus ({len(vals)} pts): frac |psi*E|<1e-10: {np.mean(np.abs(vals)<1e-10):.3f}; median |psi*E| {np.median(np.abs(vals)):.3e} -> {'S1 holds' if np.all(np.abs(vals)<1e-10) else 'S1 fails'}")
print("\n".join(out))
