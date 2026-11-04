"""FT-5a: generic single-trace operator engine (U(3) quark-line, flavour-ordered), Berends-Giele with dual numbers
eps (one O(p^4) insertion). Reuses Gaussian rationals + kinematics from sims/ft2/ft2.py."""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','ft2'))
from ft2 import G,Fr,mkc,splits,kin,amp as amp_ft2
class D:  # dual number a + eps b over G
    __slots__=('a','b')
    def __init__(s,a,b=None): s.a=a if isinstance(a,G) else G(a); s.b=b if b is not None else G(0)
    def __add__(s,o): o=o if isinstance(o,D) else D(o); return D(s.a+o.a,s.b+o.b)
    def __mul__(s,o): o=o if isinstance(o,D) else D(o); return D(s.a*o.a,s.a*o.b+s.b*o.a)
    def inv(s): ia=s.a.inv(); return D(ia,-(s.b*ia*ia))
# operator term: (coef(Fr), [factors]) factor=('U',idx)|('Ud',idx)|('M',)
LO=[(Fr(1,2),[('U',('m',)),('Ud',('m',))]),(Fr(1),[('M',),('U',())]),(Fr(1),[('M',),('Ud',())])]
OPS={'L0':[(Fr(1),[('U',('m',)),('Ud',('n',)),('U',('m',)),('Ud',('n',))])],
     'B': [(Fr(1),[('U',('m',)),('Ud',('m',)),('U',('n',)),('Ud',('n',))])]}
def comps(m,F,mins):
    if F==0:
        if m==0: yield []
        return
    for k in range(mins[0],m+1):
        for rest in comps(m-k,F-1,mins[1:]): yield [k]+rest
def vertex(terms,blocks,gaps,dot,c,cb):
    """blocks: list of momentum-objects in cyclic order; gaps[j]=mu of gap before block j. returns i*sum (G)"""
    m=len(blocks); tot=G(0)
    for coef,fac in terms:
        F=len(fac); mins=[0 if f[0]=='M' else (1 if f[1] else 0) for f in fac]
        maxs=[0 if f[0]=='M' else m for f in fac]
        for r in range(m):
            for ks in comps(m,F,mins):
                if any(k>mx for k,mx in zip(ks,maxs)): continue
                pos=r; val=G(coef); moms={}; ok=True
                for f,k in zip(fac,ks):
                    if f[0]=='M': val=val*G(gaps[pos%m]); continue
                    if k==0 and f[1]: ok=False;break
                    cc=(c if f[0]=='U' else cb)[k]; val=val*cc
                    legs=[blocks[(pos+j)%m] for j in range(k)]
                    for ix in f[1]: moms.setdefault(ix,[]).append(legs)
                    pos+=k
                if not ok or val.iszero(): continue
                # contractions: each index appears twice; (-i)^2 p.q = -p.q per pair
                for ix,(A,B) in moms.items(): val=val*G(-sum(dot(a,b) for a in A for b in B))
                tot=tot+val
    return G(0,1)*tot
def amp(n,gram,mu,f,param,ops=None,eps_terms=None):
    """dual-number amplitude: LO + eps*(single insertion of eps_terms). f has length n+1 (closed)."""
    c=mkc(param); cb=[x.conj() for x in c]
    def mk(P,sign):return (tuple(P),sign)
    def dot(A,B): return A[1]*B[1]*sum(gram[i][j] for i in A[0] for j in B[0])
    def V(blocks,gaps):
        v=D(vertex(LO,blocks,gaps,dot,c,cb))
        if eps_terms: v=v+D(G(0),vertex(eps_terms,blocks,gaps,dot,c,cb))
        return v
    memo={}
    def J(a,b):
        if a==b: return D(1)
        if (a,b) in memo: return memo[(a,b)]
        P=list(range(a,b+1)); tot=D(0)
        for parts in splits(a,b):
            blocks=[mk(range(x,y+1),1) for x,y in parts]+[mk(P,-1)]
            gaps=[mu[f[x]] for x,y in parts]+[mu[f[b+1]]]
            pr=D(1)
            for x,y in parts: pr=pr*J(x,y)
            tot=tot+V(blocks,gaps)*pr
        p2=sum(gram[i][j] for i in P for j in P)
        prop=D(G(0,1))*D(G(p2-mu[f[a]]-mu[f[b+1]])).inv()
        memo[(a,b)]=prop*tot; return memo[(a,b)]
    tot=D(0)
    for parts in splits(0,n-2):
        blocks=[mk(range(x,y+1),1) for x,y in parts]+[mk([n-1],1)]
        gaps=[mu[f[x]] for x,y in parts]+[mu[f[n-1]]]
        pr=D(1)
        for x,y in parts: pr=pr*J(x,y)
        tot=tot+V(blocks,gaps)*pr
    return tot*D(G(0,-1))
