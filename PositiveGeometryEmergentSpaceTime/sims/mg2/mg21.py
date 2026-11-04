"""MG2-1: reproduce CGW 2601.16860 Sec VI.B: Coulomb-branch massive gluon 4-pt hidden zero,
massive polarisations built from BH-2 massive spinors (AHH 1709.04891), via d+1 null embedding (CGW eq 58)."""
import numpy as np
def brentq(f,a,b):
    fa=f(a)
    for _ in range(200):
        c=(a+b)/2; fc=f(c)
        if (fc>0)==(fa>0): a,fa=c,fc
        else: b=c
    return (a+b)/2
rng=np.random.default_rng(7)
eta5=np.diag([1,-1,-1,-1,-1.]); eta4=np.diag([1,-1,-1,-1.])
d5=lambda a,b:a@eta5@b; d4=lambda a,b:a@eta4@b
sig=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.array([[1,0],[0,-1]])]
def pmat(p): return p[0]*sig[0]-p[1]*sig[1]-p[2]*sig[2]-p[3]*sig[3]
def bivec(X):  # inverse of pmat: x0=tr/2, xi=-tr(X sig_i)/2
    return np.array([0.5*np.trace(X)]+[-0.5*np.trace(X@sig[i]) for i in (1,2,3)])
def pols(p,m):
    """BH-2 (AHH 1709.04891): p_{a ad} = lam_a^I lamt_{ad I}. Choose lamt_I = sqrt(m) e_I, lam^I = P e_I/sqrt(m).
    Raise little-group index on lamt with eps^{IJ}; eps^{IJ} = lam^(I lamt^J) / m as bispinor -> 4-vector."""
    P=pmat(p); lam=[P[:,I]/np.sqrt(m) for I in (0,1)]; lt=[np.sqrt(m)*np.eye(2)[:,I] for I in (0,1)]
    ltu=[lt[1],-lt[0]]
    out=[]
    for I,Jn in [(0,0),(0,1),(1,1)]:
        X=(np.outer(lam[I],ltu[Jn])+np.outer(lam[Jn],ltu[I]))/m
        e=bivec(X); out.append(e)
    return out
def J(ea,pa,eb,pb): return d5(ea,eb)*(pa-pb)+2*d5(ea,pb)*eb-2*d5(eb,pa)*ea
def amp(E,K,k):
    s=d5(K[0]+K[1],K[0]+K[1]); t=d5(K[1]+K[2],K[1]+K[2])
    c=2*d5(E[0],E[2])*d5(E[1],E[3])-d5(E[0],E[1])*d5(E[2],E[3])-d5(E[0],E[3])*d5(E[1],E[2])
    return d5(J(E[0],K[0],E[1],K[1]),J(E[2],K[2],E[3],K[3]))/s+d5(J(E[1],K[1],E[2],K[2]),J(E[3],K[3],E[0],K[0]))/t+k*c
def kin(masses,s,ct,phi=0.3):
    m1,m2,m3,m4=masses; rs=np.sqrt(s)
    def mom(m,ma,mb):  # |p| for 2-body
        return np.sqrt((s-(ma+mb)**2)*(s-(ma-mb)**2))/(2*rs)
    q=mom(0,m1,m2); qp=mom(0,m3,m4)
    p1=np.array([np.sqrt(q*q+m1*m1),0,0,q],dtype=complex); p2=np.array([np.sqrt(q*q+m2*m2),0,0,-q])
    st=np.sqrt(1-ct*ct+0j); n=np.array([st*np.cos(phi),st*np.sin(phi),ct])
    p3=-np.array([np.sqrt(qp*qp+m3*m3),*(qp*n)]); p4=-p1-p2-p3
    return [p1,p2,p3,p4]
v=np.array([0.0,1.0,2.5,1.7])  # vevs of U(4)->U(1)^4, g=1 ; kappa_i = v_i - v_{i+1}
kap=np.array([v[i]-v[(i+1)%4] for i in range(4)]); ms=np.abs(kap)
print('kappa',kap,'sum',kap.sum(),'masses',ms)
emb=lambda p,k:np.array([*p,k],dtype=complex)
# calibrate contact sign by 5d gauge invariance at a generic point
s0=(ms[0]+ms[1]+1.5)**2
K=[emb(p,k) for p,k in zip(kin(ms,s0,0.37),kap)]
print('null check K^2:',[abs(d5(x,x)) for x in K])
def epsof(i,p,coef): e=sum(c*x for c,x in zip(coef,pols(p,ms[i]) if p[0].real>0 else pols(-p,ms[i]))); return emb(e,0)
P4=kin(ms,s0,0.37); E=[epsof(i,P4[i],rng.normal(size=3)+1j*rng.normal(size=3)) for i in range(4)]
print('transversality eps.p:',[abs(d4(E[i][:4],P4[i])) for i in range(4)])
for k in (1,-1):
    Eg=list(E); Eg[0]=K[0].astype(complex)
    print('gauge test k=',k,abs(amp(Eg,K,k)),' |A| generic',abs(amp(E,K,k)))
k=min((1,-1),key=lambda k:abs(amp([K[0].astype(complex)]+E[1:],K,k)))
# hidden zero locus: c13 = -2 K1.K3 = 0  (massive: (p1+p3)^2 = (k1+k3)^2), plus E1.E3 = E1.K3 = E3.K1 = 0
# locus is outside the real physical region (K1.K3 linear in cos theta, root at |ct|>1): use complex kinematics
s0=(ms[0]+ms[1]+1.5)**2
g=lambda ct:d5(emb(kin(ms,s0,ct)[0],kap[0]),emb(kin(ms,s0,ct)[2],kap[2]))
a0=g(0.0); a1=g(1.0)-a0; ct=-a0/a1+0j
P4=kin(ms,s0,ct); K=[emb(p,kk) for p,kk in zip(P4,kap)]
print('s on locus',s0)
print('locus cos theta',ct,'s',s0,'K1.K3',d5(K[0],K[2]),' (p1+p3)^2-(k1+k3)^2 =',d4(P4[0]+P4[2],P4[0]+P4[2])-(kap[0]+kap[2])**2)
B1=[emb(x,0) for x in pols(P4[0],ms[0])]; B3=[emb(x,0) for x in pols(-P4[2],ms[2])]
# eps1 in span with eps1.p3=0
a=np.array([d5(b,K[2]) for b in B1]); c1=np.linalg.svd(a[None,:])[2].conj()[1:]; E1=sum(x*b for x,b in zip(rng.normal(size=2)@c1,B1))
A3=np.array([[d5(b,K[0]) for b in B3],[d5(E1,b) for b in B3]]); c3=np.linalg.svd(A3)[2].conj()[2]; E3=sum(x*b for x,b in zip(c3,B3))
E2=sum(x*b for x,b in zip(rng.normal(size=3)+1j*rng.normal(size=3),[emb(x,0) for x in pols(P4[1],ms[1])]))
E4=sum(x*b for x,b in zip(rng.normal(size=3)+1j*rng.normal(size=3),[emb(x,0) for x in pols(-P4[3],ms[3])]))
print('conds E1.K3,E3.K1,E1.E3:',abs(d5(E1,K[2])),abs(d5(E3,K[0])),abs(d5(E1,E3)))
Az=amp([E1,E2,E3,E4],K,k); scale=abs(amp([E1,E2,E3+0.3*B3[0],E4],K,k))
print('HIDDEN ZERO |A| on locus =',abs(Az),' off-condition |A| =',scale,' ratio',abs(Az)/scale)
# naive massive YM (CGW 52): same 4d momenta/masses, no kappa in dot products -> 4d Feynman w/ massive props (Proca, numerator eta - PP/m^2 ignored at equal-mass? use eta only) 

def trial(vv,s_,seed):
    global kap,ms
    r=np.random.default_rng(seed)
    kap=np.array([vv[i]-vv[(i+1)%4] for i in range(4)]); ms=np.abs(kap)
    s_=(max(ms[0]+ms[1],ms[2]+ms[3])+s_)**2
    g=lambda ct:d5(emb(kin(ms,s_,ct)[0],kap[0]),emb(kin(ms,s_,ct)[2],kap[2]))
    a0=g(0.0); ct=-a0/(g(1.0)-a0)+0j; P=kin(ms,s_,ct); KK=[emb(p,x) for p,x in zip(P,kap)]
    B=[[emb(x,0) for x in pols(P[i] if i<2 else -P[i],ms[i])] for i in range(4)]
    a=np.array([d5(b,KK[2]) for b in B[0]]); e1=sum(x*b for x,b in zip(r.normal(size=2)@np.linalg.svd(a[None,:])[2].conj()[1:],B[0]))
    A3=np.array([[d5(b,KK[0]) for b in B[2]],[d5(e1,b) for b in B[2]]]); e3=sum(x*b for x,b in zip(np.linalg.svd(A3)[2].conj()[2],B[2]))
    rnd=lambda Bi:sum(x*b for x,b in zip(r.normal(size=3)+1j*r.normal(size=3),Bi))
    e2,e4=rnd(B[1]),rnd(B[3]); z=abs(amp([e1,e2,e3,e4],KK,1))
    ref=abs(amp([e1,e2,rnd(B[2]),e4],KK,1))
    # control: 4d-only locus (ignore kappa): (p1+p3)^2 = 0 instead of (p1+p3)^2=(k1+k3)^2
    g4=lambda ct:d4(kin(ms,s_,ct)[0]+kin(ms,s_,ct)[2],kin(ms,s_,ct)[0]+kin(ms,s_,ct)[2])
    b0=g4(0.0); c4=-b0/(g4(1.0)-b0)+0j; P=kin(ms,s_,c4); KK=[emb(p,x) for p,x in zip(P,kap)]
    B=[[emb(x,0) for x in pols(P[i] if i<2 else -P[i],ms[i])] for i in range(4)]
    a=np.array([d5(b,KK[2]) for b in B[0]]); f1=sum(x*b for x,b in zip(r.normal(size=2)@np.linalg.svd(a[None,:])[2].conj()[1:],B[0]))
    A3=np.array([[d5(b,KK[0]) for b in B[2]],[d5(f1,b) for b in B[2]]]); f3=sum(x*b for x,b in zip(np.linalg.svd(A3)[2].conj()[2],B[2]))
    ctl=abs(amp([f1,rnd(B[1]),f3,rnd(B[3])],KK,1))
    return z/ref, ctl/ref
R=[trial(rng.normal(size=4)*2,0.5+rng.random()*3,i) for i in range(30)]
R=np.array(R); print('30 random Coulomb vevs: max |A_zero|/|A_ref| =',R[:,0].max(),' control (4d locus, no kappa) median ratio =',np.median(R[:,1]))
