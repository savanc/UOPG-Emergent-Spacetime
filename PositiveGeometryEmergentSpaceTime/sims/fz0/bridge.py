"""FZ-0 T2 (SIMULATED): existence of massive on-shell spinor pairs with w3 gamma^mu u1 = 0 for all mu
(Zhang-Zhu 2609.06552 fermion bridge), complex kinematics, equal masses M. Run: python3 bridge.py"""
import numpy as np
rng=np.random.default_rng(3)
I2=np.eye(2); Z=np.zeros((2,2)); sx=np.array([[0,1],[1,0]]); sy=np.array([[0,-1j],[1j,0]]); sz=np.diag([1,-1])
G=[np.block([[Z,I2],[I2,Z]])]+[np.block([[Z,s],[-s,Z]]) for s in (sx,sy,sz)]
eta=np.diag([1,-1,-1,-1])
def slash(p): return sum(eta[m,m]*p[m]*G[m] for m in range(4))
def onshell(M):
    v=rng.normal(size=3)+1j*rng.normal(size=3); return np.array([np.sqrt(M**2+v@v),*v])
def kern(A,left=False): return np.linalg.svd(A.T if left else A)[2].conj()[-2:].T
def analyse(p1,p3,M):
    u1=kern(slash(p1)-M*np.eye(4)); w3=kern(slash(p3)-M*np.eye(4),left=True)
    Mat=np.array([[w3[:,a]@G[m]@u1[:,b] for a in range(2) for b in range(2)] for m in range(4)])
    sv=np.linalg.svd(Mat,compute_uv=False); rank=int(np.sum(sv>1e-9*sv[0]))
    if rank<=2: return rank,True
    N=np.linalg.svd(Mat)[2].conj()[-1].reshape(2,2)
    return rank, bool(abs(np.linalg.det(N))<1e-9*np.linalg.norm(N)**2)
def null_perp(p1):
    P=lambda v: v-(v@eta@p1)/(p1@eta@p1)*p1
    a=P(rng.normal(size=4)+1j*rng.normal(size=4)); b=P(rng.normal(size=4)+1j*rng.normal(size=4))
    A=a@eta@a; B=2*a@eta@b; C=b@eta@b; return ((-B+np.sqrt(B*B-4*A*C))/(2*A))*a+b
M=1.0; out={}
out['generic']=[analyse(onshell(M),onshell(M),M) for _ in range(25)]
r=[]
for _ in range(25):
    p1=onshell(M); r.append(analyse(p1,p1-null_perp(p1),M))
out['q2=0']=r
r=[]
for _ in range(25):
    p1=onshell(M); r.append(analyse(p1,-p1+null_perp(p1),M))
out['P2=0 control']=r
for k,v in out.items(): print(k,'ranks',sorted(set(x[0] for x in v)),'bridge solvable',sum(x[1] for x in v),'/',len(v))
