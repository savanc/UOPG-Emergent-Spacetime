"""BH-2 exact cross-check (SIMULATED, sympy, non-blind). Mirrors PositiveGeometryEmergentSpaceTime.MassiveSpinor conventions."""
import random, sympy as sp
random.seed(20261012)
I=sp.I; eps=sp.Matrix([[0,1],[-1,0]])
def gr(): return sp.Rational(random.randint(-9,9),random.randint(1,5))+I*sp.Rational(random.randint(-9,9),random.randint(1,5))
def gm(): return sp.Matrix(2,2,lambda i,j: gr())
def gv(): return sp.Matrix([gr(),gr()])
ok=True; n=0
def chk(c,msg):
    global ok,n; n+=1
    if not c: ok=False; print("FAIL",msg)
for trial in range(40):
    # (b) little group SL(2): W with det 1
    W=gm(); W=W/sp.sqrt(W.det()) if False else W
    W=sp.Matrix([[W[0,0],W[0,1]],[W[1,0],(1+W[0,1]*W[1,0])/W[0,0]]]) if W[0,0]!=0 else sp.eye(2)
    L,Lt=gm(),gm(); p=L*Lt.T
    chk(sp.simplify(W.det()-1)==0,"detW")
    chk(sp.simplify((L*W)*(Lt*W.inv().T).T-p)==sp.zeros(2),"mom inv")
    chk(sp.simplify((L.T*eps*L)-L.det()*eps)==sp.zeros(2),"br_self")
    L2=gm(); W2=sp.eye(2)
    chk(sp.simplify((L*W).T*eps*(L2*W)-W.T*(L.T*eps*L2)*W)==sp.zeros(2),"covariance")
    A=W; chk(sp.simplify((A*L).T*eps*(A*L2)-L.T*eps*L2)==sp.zeros(2),"lorentz")
    # (a) decomposition with det p = m^2: Lambda = sqrt(m) I
    m=gr(); 
    if m==0: continue
    q=gm(); q=q*(m/sp.sqrt(q.det())) if q.det()!=0 else None
    if q is None: continue
    c=sp.sqrt(m); La=c*sp.eye(2); Lta=(q/c).T
    chk(sp.simplify(La*Lta.T-q)==sp.zeros(2) and sp.simplify(La.det()-m)==0 and sp.simplify(Lta.det()-m)==0,"decomp")
    # (c) x factor on equal-mass kinematics: choose l, solve lt on the condition ang(l,u)=0
    l=gv(); a,b=sp.symbols('a b')
    ltv=sp.Matrix([a,b]); uu=q*(eps*ltv); cond=sp.expand((l.T*eps*uu)[0])
    sol=sp.solve(cond,b)
    if not sol: continue
    ltv=ltv.subs(b,sol[0]).subs(a,gr()); uu=q*(eps*ltv)
    k=l*ltv.T
    chk(sp.simplify((q+k).det()-q.det())==0,"equal mass")
    x=sp.simplify(uu[0]/(m*l[0])) if l[0]!=0 else sp.simplify(uu[1]/(m*l[1]))
    chk(sp.simplify(uu-m*x*l)==sp.zeros(2,1),"x exists")
    z=gv(); den=(z.T*eps*l)[0]
    if den!=0: chk(sp.simplify((z.T*eps*uu)[0]/(m*den)-x)==0,"zeta indep")
    t=gr()
    if t!=0:
        u2=q*(eps*(ltv/t)); chk(sp.simplify(u2-m*(x/t**2)*(t*l))==sp.zeros(2,1),"weight")
# (d) power counting: CHKL term a ~ m^-a; bounded iff only a=0
ms=sp.symbols('m',positive=True); g=sp.symbols('g0:5')
A=sum(g[a]*ms**(-a) for a in range(5))
lim=[sp.limit(A.subs({g[j]:(1 if j==a else 0) for j in range(5)}),ms,0) for a in range(5)]
chk(lim[0]==1 and all(L_==sp.oo for L_ in lim[1:]),"power counting")
print(f"checks={n} all_pass={ok}; m->0 limits per structure a=0..4: {lim}")
