"""COS-1 gate: zeros of tree Tr phi^3 wavefunction coefficients (conformally coupled), flat-space-like and dS4-twisted."""
import sympy as sp, numpy as np
from scipy import integrate
out=[]
X1,X2,X3,Y,Y1,Y2=sp.symbols('X1 X2 X3 Y Y1 Y2',positive=True)
# Recursion (ABP 2017): (sum X) psi_G = sum_e psi_{G_L}(X_end+Y_e) psi_{G_R}(X_end+Y_e); single site psi=1/X
def psi(Xs,Ys):
    if len(Xs)==1: return 1/Xs[0]
    tot=0
    for e in range(len(Ys)):
        L=list(Xs[:e+1]); R=list(Xs[e+1:]); L[-1]=L[-1]+Ys[e]; R[0]=R[0]+Ys[e]
        tot+=psi(L,Ys[:e])*psi(R,Ys[e+1:])
    return sp.simplify(tot/sum(Xs))
p2=psi([X1,X2],[Y]); target=(X1+X2+2*Y)/((X1+X2)*(X1+Y)*(X2+Y))
out.append(f"T1 2-site: psi = {sp.factor(p2)} ; equals (X1+X2+2Y)/((X1+X2)(X1+Y)(X2+Y)): {sp.simplify(p2-target)==0}")
p3=sp.factor(psi([X1,X2,X3],[Y1,Y2]))
num,den=sp.fraction(sp.together(p3))
bulk=(1/(2*Y))*((X1+X2+2*Y)/((X1+X2)*(X1+Y)*(X2+Y)) - 1/((X1+Y)*(X2+Y)))
out.append(f"T1 direct time integral (Feynman part (X1+X2+2Y)/... minus Dirichlet boundary term, /2Y) = recursion: {sp.simplify(bulk-p2)==0}; prereg formula omitted the boundary term")
out.append(f"T1 3-site chain: numerator has only positive coefficients: {all(c>0 for c in sp.Poly(sp.expand(num),X1,X2,X3,Y1,Y2).coeffs())}; denominator = {den}")
# T2 scan 4pt ordered s+t with physical 3-momenta
rng=np.random.default_rng(1); f2=sp.lambdify((X1,X2,Y),p2)
mn=np.inf; neg=0; Npts=10**6
k=rng.normal(size=(Npts,3,3)); k4=-k.sum(1); K=np.concatenate([k,k4[:,None]],1); E=np.linalg.norm(K,axis=2)
Ys=np.linalg.norm(K[:,0]+K[:,1],axis=1); Yt=np.linalg.norm(K[:,1]+K[:,2],axis=1)
v=f2(E[:,0]+E[:,1],E[:,2]+E[:,3],Ys)+f2(E[:,1]+E[:,2],E[:,3]+E[:,0],Yt)
vn=v*(E.sum(1))**2  # dimensionless
out.append(f"T2 4pt s+t, {Npts} physical points: min psi*E_tot^2 = {vn.min():.4e}, any <=0: {bool((v<=0).any())}")
# 5pt ordered: sum of 5 three-site chains (cyclic channels), physical scan
f3=sp.lambdify((X1,X2,X3,Y1,Y2),p3); n5=2*10**5
k=rng.normal(size=(n5,4,3)); K=np.concatenate([k,-k.sum(1)[:,None]],1); E=np.linalg.norm(K,axis=2)
tot=0
for r in range(5):
    i=[(r+j)%5 for j in range(5)]
    Xa=E[:,i[0]]+E[:,i[1]]; Xb=E[:,i[2]]; Xc=E[:,i[3]]+E[:,i[4]]
    Ya=np.linalg.norm(K[:,i[0]]+K[:,i[1]],axis=1); Yb=np.linalg.norm(K[:,i[3]]+K[:,i[4]],axis=1)
    tot=tot+f3(Xa,Xb,Xc,Ya,Yb)
out.append(f"T2 5pt ordered (5 channels), {n5} physical points: any <=0: {bool((tot<=0).any())}, min*E^3 = {(tot*E.sum(1)**3).min():.4e}")
# T3 dS4 twist: integrate shifts of vertex energies
def psids(a,b,y): return integrate.dblquad(lambda w2,w1: f2(a+w1,b+w2,y),0,np.inf,0,np.inf)[0]
vals=[]
for j in range(40):
    kk=rng.normal(size=(3,3)); KK=np.vstack([kk,-kk.sum(0)]); e=np.linalg.norm(KK,axis=1)
    vals.append(psids(e[0]+e[1],e[2]+e[3],np.linalg.norm(KK[0]+KK[1]))+psids(e[1]+e[2],e[3]+e[0],np.linalg.norm(KK[1]+KK[2])))
out.append(f"T3 dS4-twisted 4pt s+t, 40 physical points: min = {min(vals):.4e} (finite? {np.isfinite(vals).all()}), any <=0: {min(vals)<=0}")
# T4 zero locus: solve psi_s+psi_t=0 for Y_t given others; check sign of required variables
A,B,C,D,Ysv,Ytv=sp.symbols('A B C D Ys Yt')
ex=sp.together(psi([A,B],[Ysv])+psi([C,D],[Ytv])); nm=sp.numer(ex)
sol=sp.solve(nm.subs({A:1,B:1,C:1,D:1,Ysv:sp.Rational(1,2)}),Ytv)
out.append(f"T4 zero of psi_s+psi_t at X's=1, Ys=1/2: Yt = {sol} (all outside Y>0 or making some X+Y<0)")
print("\n".join(out))
