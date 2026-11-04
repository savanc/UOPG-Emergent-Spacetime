"""EW-Z1b: full massive-vector 4-pt colour-ordered amplitudes, CGW 2601.16860 SSB setup (U(N)->U(1)^N adjoint Higgs).
Exact symbolic (sympy). Vectors = (4D part over basis {p1,p2,p3,e1..e4}, 5th 'Higgs-direction' component).
Couplings tagged by number of 5-indices per vertex term: lam3 (VVV), a (VVS: hWW / Goldstone-WW, ∝ mass),
gs (VSS), lam4 (VVVV), b (VVSS: hhWW). kap3 = h^3 added explicitly. All =1 <=> 5D YM = CGW SSB theory."""
import sympy as S, itertools as it
k=S.symbols('k1:5'); s,t=S.symbols('s t')
lam3,a,gs,lam4,b,kap3,mh=S.symbols('lam3 a gs lam4 b kap3 m_h')
E5=S.symbols('E5_1:5')  # 5th components of external polarisations (h legs)
B=['p1','p2','p3','e1','e2','e3','e4']
ee={(i,j):S.Symbol(f'ee{i}{j}') for i in range(1,5) for j in range(i+1,5)}
ep={(i,j):S.Symbol(f'e{i}p{j}') for i in range(1,5) for j in range(1,4) if i!=j}
def m2(i): return k[i-1]**2
m4sq=(k[0]+k[1]+k[2])**2
u=m2(1)+m2(2)+m2(3)+m4sq-s-t
pp={('p1','p1'):m2(1),('p2','p2'):m2(2),('p3','p3'):m2(3),
 ('p1','p2'):(s-m2(1)-m2(2))/2,('p2','p3'):(t-m2(2)-m2(3))/2,('p1','p3'):(u-m2(1)-m2(3))/2}
def d4(x,y):
    if x>y: x,y=y,x
    if x[0]=='p' and y[0]=='p': return pp[(x,y)]
    if x[0]=='e' and y[0]=='e':
        i,j=int(x[1]),int(y[1]); return 0 if i==j else ee[(i,j)]  # e_i.e_i irrelevant (never appears)
    # x=e?,y=p? after sort 'e'<'p'
    i,j=int(x[1]),int(y[1])
    if i==j: return 0
    if i==4: return -sum(ep[(4,l)] for l in (1,2,3) if l!=j) if False else ep4(j)
    return ep[(i,j)]
def ep4(j):  # e4.p_j with e4.p4=0, p4=-(p1+p2+p3): e4.p3 = -e4.p1-e4.p2
    return ep[(4,j)] if j in (1,2) else -ep[(4,1)]-ep[(4,2)]
ep[(4,3)]=None
def dot4(X,Y): return S.expand(sum(cx*cy*d4(bx,by) for bx,cx in X.items() for by,cy in Y.items()))
class V:
    def __init__(s_,d,f): s_.d={kk:v for kk,v in d.items() if v!=0}; s_.f=f
    def __add__(s_,o): d=dict(s_.d); [d.__setitem__(kk,d.get(kk,0)+v) for kk,v in o.d.items()]; return V(d,s_.f+o.f)
    def __rmul__(s_,c): return V({kk:c*v for kk,v in s_.d.items()},c*s_.f)
    def __neg__(s_): return (-1)*s_
    def __sub__(s_,o): return s_+(-o)
P=[None,V({'p1':1},k[0]),V({'p2':1},k[1]),V({'p3':1},k[2]),V({'p1':-1,'p2':-1,'p3':-1},-(k[0]+k[1]+k[2]))]
def Epol(i,h=False): return V({},E5[i-1]) if h else V({f'e{i}':1},0)
def parts(X,Y): return dot4(X.d,Y.d), -X.f*Y.f   # (4D part, 5th part) of 5D dot (mostly-minus in extra dim)
def J(E1,K1,E2,K2,c=None):
    """open-index current V3(1,2,-(1+2)) with couplings; returns V (4D,5th components). Tag by #5-indices."""
    K3=-(K1+K2)
    # term1: g^{mu nu}(k1-k2)^rho ; term2: g^{nu rho}(k2-k3)^mu ; term3: g^{rho mu}(k3-k1)^nu
    e12_4,e12_5=parts(E1,E2)
    out=V({},0)
    # term1: (E1.E2)(k1-k2)^rho : rho 4D part -> VVV if e12 4D else VSS ; rho 5th -> VVS(4D pair) / SSS
    D=K1-K2
    out=out+ (lam3*e12_4+gs*e12_5)*V(D.d,0) + (a*e12_4)*V({},D.f)   # SSS (e12_5*D.f) vanishes by cyclic sum; set 0
    # term2: E2^rho ((k2-k3).E1) ; term3: E1^rho ((k3-k1).E2)
    for (Ea,Kx,Ky,Eb) in ((E2,K2,K3,E1),(E1,K3,K1,E2)):
        q4,q5=parts(Kx-Ky,Eb)
        # open index carried by Ea: 4D part of Ea, 5th part of Ea
        out=out+ (lam3*q4+a*q5)*V(Ea.d,0) + (gs*q4)*V({},Ea.f)
    return out
def amp(ext,prop='feyn',Mint=None,hexch=1):
    """ext: list of 4 (E,K). Colour-ordered A[1234]: s-chan (12), t-chan (23), contact."""
    (E1,K1),(E2,K2),(E3,K3),(E4,K4)=ext
    res=0
    for (A_,B_),(C_,D_),X in (((0,1),(2,3),s),((1,2),(3,0),t)):
        Ja=J(*ext[A_],*ext[B_]); Jb=J(*ext[C_],*ext[D_])
        Pm=ext[A_][1]+ext[B_][1]; M2=Pm.f**2
        if prop=='feyn':
            v4,_=parts(V(Ja.d,0),V(Jb.d,0)); sc=-Ja.f*Jb.f
            res+= (v4 + hexch*sc)/(X-M2)
        elif prop=='proca':  # unitary/Proca: -(g-PP/M^2), no scalar
            M=Mint
            v4,_=parts(V(Ja.d,0),V(Jb.d,0)); ja,_=parts(V(Ja.d,0),V(Pm.d,0)); jb,_=parts(V(Jb.d,0),V(Pm.d,0))
            res+= (v4 - ja*jb/M**2)/(X-M**2)
    # contact: c*[2(E1.E3)(E2.E4)-(E1.E2)(E3.E4)-(E1.E4)(E2.E3)], tagged
    def pr(X,Y,Z,W):
        x4,x5=parts(X,Y); y4,y5=parts(Z,W)
        return lam4*x4*y4 + b*(x4*y5+x5*y4) + x5*y5
    Es=[e for e,_ in ext]
    cont=2*pr(Es[0],Es[2],Es[1],Es[3])-pr(Es[0],Es[1],Es[2],Es[3])-pr(Es[0],Es[3],Es[1],Es[2])
    return res, cont
