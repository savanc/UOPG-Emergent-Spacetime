"""FZ-1 (SIMULATED): massive f g fbar g ordered amplitude (adjoint = -Compton sum) with Pauli coupling kappa,
on the Zhang-Zhu massive locus (p1+p3)^2=0 + bridge ubar1 gamma^mu v3 = 0. Run: python3 fz1.py"""
import numpy as np
rng=np.random.default_rng(7)
I2=np.eye(2); Z=np.zeros((2,2)); S=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
G=[np.block([[Z,I2],[I2,Z]])]+[np.block([[Z,s],[-s,Z]]) for s in S]; eta=np.diag([1.,-1,-1,-1]); E4=np.eye(4)
dot=lambda a,b:a@eta@b
def sl(p): return sum(eta[m,m]*p[m]*G[m] for m in range(4))
def cr(n=4): return rng.normal(size=n)+1j*rng.normal(size=n)
def null_from(l,lt):
    K=np.outer(l,lt); return np.array([np.trace(K)/2]+[-np.trace(K@s)/2 for s in S])
def kerR(A): return np.linalg.svd(A)[2].conj()[-2:].T
def kerL(A): return np.linalg.svd(A.T)[2].conj()[-2:].T
def V(e,k,kap,m): E,K=sl(e),sl(k); return E+kap/(4*m)*(E@K-K@E)
def amp(ub,v,p1,legs,kap,m):
    tot=0
    for (ea,ka),(eb,kb) in (legs,legs[::-1]):
        q=p1+ka; tot+=ub@V(ea,ka,kap,m)@(sl(q)+m*E4)@V(eb,kb,kap,m)@v/(dot(q,q)-m*m)
    return -tot
def pol(k):
    e=cr(); r=cr(); return e-dot(e,k)/dot(r,k)*r
def locus(m):
    l=cr(2); k2=null_from(l,cr(2)); k4=null_from(rng.normal()*l,cr(2)); n=k2+k4
    r=cr(); P=lambda x:x-dot(x,n)/dot(r,n)*r
    a,b=P(cr()),P(cr()); A,B,C=dot(b,b),2*dot(a,b),dot(a,a)-m*m; lam=(-B+np.sqrt(B*B-4*A*C))/(2*A)
    p1=a+lam*b; p3=-p1-n; return p1,k2,p3,k4
def bridge(p1,p3,m):
    w=kerL(sl(p1)-m*E4); u=kerR(sl(p3)+m*E4)
    Mat=np.array([[w[:,a]@G[mu]@u[:,b] for a in range(2) for b in range(2)] for mu in range(4)])
    N=np.linalg.svd(Mat)[2].conj()[-1].reshape(2,2); U,s,Vh=np.linalg.svd(N)
    x,y=U[:,0]*np.sqrt(s[0]),Vh[0]*np.sqrt(s[0])
    ub,v=w@x,u@y
    return ub,v,s[1]/s[0],max(abs(ub@G[mu]@v) for mu in range(4))/np.linalg.norm(ub)/np.linalg.norm(v), w,u
if __name__=="__main__":
    m=1.0; ward=0; t1=[]; lin=[]; quad=[]; res=[]
    for i in range(20):
        p1,k2,p3,k4=locus(m)
        assert abs(dot(p1,p1)-m*m)<1e-9 and abs(dot(p3,p3)-m*m)<1e-9 and abs(dot(p1+p3,p1+p3))<1e-9
        ub,v,rk1,br,w,u=bridge(p1,p3,m); e2,e4=pol(k2),pol(k4)
        ctrl=[abs(amp(w@cr(2),u@cr(2),p1,[(e2,k2),(e4,k4)],0,m)) for _ in range(5)]
        for kap in (0,0.7):
            ward=max(ward,abs(amp(w@cr(2),u@cr(2),p1,[(k2,k2),(e4,k4)],kap,m))/np.median(ctrl))
        f=lambda kap:amp(ub,v,p1,[(e2,k2),(e4,k4)],kap,m)
        a0=f(0); a1=(f(1)-f(-1))/2; a2=(f(1)+f(-1))/2-a0; a3=f(2)-(a0+2*a1+4*a2)
        sc=np.median(ctrl); t1.append(abs(a0)/sc); lin.append(abs(a1)/sc); quad.append(abs(a2)/sc); res.append(abs(a3)/sc)
    print('T0 Ward max rel',ward)
    print('T1 kappa=0 max |A|/|ctrl|',max(t1),' (bridge rank-1 residual ok)')
    print('T2 linear coeff min,max',min(lin),max(lin),' quad coeff min,max',min(quad),max(quad),' cubic-residual max',max(res))
    # T3 real forward Compton: electron at rest, photon along z, spin basis along x, flip
    om=0.37; p=np.array([m,0,0,0.]); k=np.array([om,0,0,om])
    up=kerR(sl(p)-m*E4)  # u(p) space
    # x-basis spin states: eigvecs of Sigma_x = gamma5 gamma0 gamma1 restricted
    g5=1j*G[0]@G[1]@G[2]@G[3]; Sx=g5@G[0]@G[1]
    Ms=np.linalg.pinv(up)@Sx@up; ev,evec=np.linalg.eig(Ms); us=[up@evec[:,j] for j in range(2)]
    ubar=lambda x:x.conj()@G[0]
    out=[]
    for hel in (+1,-1):
        e=np.array([0,1,1j*hel,0])/np.sqrt(2)
        bridge_r=max(abs(ubar(us[1])@G[mu]@us[0]) for mu in range(4))
        # all-outgoing: p1=p (out), p3=-p (in u), k2=k (out, eps*), k4=-k (in, eps)
        g=lambda kap: -sum(ubar(us[1])@V(ea,ka,kap,m)@(sl(p+ka)+m*E4)@V(eb,kb,kap,m)@us[0]/(dot(p+ka,p+ka)-m*m)
                       for (ea,ka),(eb,kb) in [((e.conj(),k),(e,-k)),((e,-k),(e.conj(),k))])
        out.append((hel,bridge_r,abs(g(0)),abs(g(1)),abs(g(2))/abs(g(1)) if abs(g(1))>0 else None,
                    abs(ubar(us[0])@V(e.conj(),k,0,m)@(sl(p+k)+m*E4)@V(e,-k,0,m)@us[0]/(dot(p+k,p+k)-m*m))))
    for o in out: print('T3 hel %+d bridge %.1e |A(0)| %.2e |A(1)| %.3e A(2)/A(1) %s  [non-flip single-diagram scale %.2e]'%o)
