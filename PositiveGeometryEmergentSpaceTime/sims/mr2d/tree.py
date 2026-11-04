"""MR-2d: tree-level O(p^4) SU(3) ChPT pi pi amplitude at P=(M^2,M^2,2M^2) via brute-force
Lagrangian expansion (GL85 Lagrangian, U=exp(i Phi/F0), Phi=phi_a lambda_a, chi=diag(m2l,m2l,m2s)).
Outputs A(P) as linear form in L_i, physical M, field renorm included. Loops NOT included."""
import sympy as sp, itertools, pickle
F,ml2,ms2=sp.symbols('F m2l m2s',positive=True)
L=sp.symbols('L1:11')
l1=sp.Matrix([[0,1,0],[1,0,0],[0,0,0]]); l2=sp.Matrix([[0,-sp.I,0],[sp.I,0,0],[0,0,0]])
chi=sp.diag(ml2,ml2,ms2)
def Uexp(sign,der,maxn=4):
    out=[]
    for n in range(maxn+1):
        c=(sign*sp.I/F)**n/sp.factorial(n)
        if der is None: out.append((c,tuple(('p',()) for _ in range(n))))
        else:
            for k in range(n): out.append((c,tuple(('p',(der,) if j==k else ()) for j in range(n))))
    return out
def mul(*facs):
    res=[(1,())]
    for f in facs: res=[(a*b,w1+w2) for a,w1 in res for b,w2 in f if sum(1 for i in w1+w2 if i[0]=='p')<=4]
    return res
C=[(1,(('c',),))]
tr=lambda *f:[(c,[w]) for c,w in mul(*f)]
prod=lambda t1,t2:[(a*b,w1+w2) for a,w1 in t1 for b,w2 in t2 if sum(1 for w in w1+w2 for i in w if i[0]=='p')<=4]
add=lambda *ts:[x for t in ts for x in t]
scale=lambda k,t:[(k*c,w) for c,w in t]
dU=lambda m:Uexp(1,m); dUd=lambda m:Uexp(-1,m); U=Uexp(1,None); Ud=Uexp(-1,None)
LO=add(scale(F**2/4,tr(dU('a'),dUd('a'))),scale(F**2/4,add(tr(C,Ud),tr(U,C))))
A1=tr(dUd('a'),dU('a')); X=add(tr(C,Ud),tr(U,C))
Lag4=add(scale(L[0],prod(A1,tr(dUd('c'),dU('c')))),scale(L[1],prod(tr(dUd('a'),dU('b')),tr(dUd('a'),dU('b')))),
 scale(L[2],tr(dUd('a'),dU('a'),dUd('b'),dU('b'))),scale(L[3],prod(A1,X)),
 scale(L[4],add(tr(dUd('a'),dU('a'),C,U),tr(dUd('a'),dU('a'),Ud,C))),
 scale(L[5],prod(X,X)),scale(L[7],add(tr(C,Ud,C,Ud),tr(U,C,U,C))))
def evaluate(terms,legs,dot):
    n=len(legs); tot=0
    for c,words in terms:
        slots=[(wi,pi) for wi,w in enumerate(words) for pi,it in enumerate(w) if it[0]=='p']
        if len(slots)!=n: continue
        for perm in itertools.permutations(range(n)):
            asg={slots[k]:legs[perm[k]] for k in range(n)}
            val=c
            for wi,w in enumerate(words):
                Mt=sp.eye(3)
                for pi,it in enumerate(w): Mt=Mt*(chi if it[0]=='c' else asg[(wi,pi)][0])
                val*=Mt.trace()
                if val==0: break
            if val==0: continue
            lab={}
            for wi,w in enumerate(words):
                for pi,it in enumerate(w):
                    if it[0]=='p':
                        for l in it[1]: lab.setdefault(l,[]).append(asg[(wi,pi)][1])
            for l,(i,j) in lab.items(): val*=-dot(i,j)
            tot+=val
    return sp.expand(tot)
p2=sp.Symbol('p2')
G0=evaluate(LO,[(l1,'a'),(l1,'b')],lambda i,j:p2 if i==j else -p2)
G1=evaluate(Lag4,[(l1,'a'),(l1,'b')],lambda i,j:p2 if i==j else -p2)
print('Gamma2 LO',sp.factor(G0)); print('Gamma2 NLO',sp.collect(sp.expand(G1),p2))
s,t,M2=sp.symbols('s t M2'); u=4*M2-s-t
D={frozenset((1,2)):(s-2*M2)/2,frozenset((3,4)):(s-2*M2)/2,frozenset((1,3)):(t-2*M2)/2,
   frozenset((2,4)):(t-2*M2)/2,frozenset((1,4)):(u-2*M2)/2,frozenset((2,3)):(u-2*M2)/2}
dot=lambda i,j:M2 if i==j else D[frozenset((i,j))]
legs=[(l1,1),(l1,2),(l2,3),(l2,4)]
V0=evaluate(LO,legs,dot); V1=evaluate(Lag4,legs,dot)
g0=sp.expand(G0); n0=g0.coeff(p2,1)  # should be 1
z1=sp.expand(G1).coeff(p2,1); dm=-sp.expand(G1).coeff(p2,0)
# pole: (1+z1)M2 - ml2 - dm = 0 -> ml2 = M2(1+z1) - dm  (first order)
V0p=sp.expand(V0.subs(ml2,M2)+sp.diff(V0,ml2).subs(ml2,M2)*(M2*z1-dm).subs(ml2,M2))
A=sp.expand(V0p - 2*z1.subs(ml2,M2)*V0.subs(ml2,M2) + V1.subs(ml2,M2))
print('LO A =',sp.factor(V0.subs(ml2,M2)))
AP=sp.expand(A.subs({s:M2,t:M2}))
print('A(P) F^4 =',sp.collect(sp.expand(AP*F**4),L))
pickle.dump((A,AP),open('A.pkl','wb'))
