"""FT-2: LO U(3) ChPT (quark-line basis) flavour-ordered tree amplitudes with unequal
quark masses; test hidden-zero loci p_i.p_j=0 at 4 and 6 points. Berends-Giele, numeric,
exact rationals (fractions) so 'zero' means exactly zero. Two parametrisations (exp, Cayley)
must agree on-shell (validation)."""
from fractions import Fraction as Fr
from math import factorial
import itertools, random, sys
I=complex(0,1)
def coeffs(param,N=8):
    # U = sum c_k (phi)^k ; c_k complex rational stored as (re,im) Fractions via gaussian ints
    if param=='exp': return [ (I**k)/factorial(k) for k in range(N)]
    if param=='cay': return [1]+[2*(I/2)**k for k in range(1,N)]
def cr(z):  # exact-ish: coefficients are Gaussian rationals; represent as pair of Fractions
    return (Fr(z.real).limit_denominator(10**6),Fr(z.imag).limit_denominator(10**6))
class G:  # Gaussian rational
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return G(-s.a,-s.b)
    def __sub__(s,o): return s+(-(o if isinstance(o,G) else G(o)))
    def __mul__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a*o.a-s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s): d=s.a*s.a+s.b*s.b; return G(s.a/d,-s.b/d)
    def conj(s): return G(s.a,-s.b)
    def iszero(s): return s.a==0 and s.b==0
    def __repr__(s): return f"({s.a}+{s.b}i)"
iG=G(0,1)
def mkc(param): return [G(*cr(z)) for z in coeffs(param)]
def amp(n,gram,mu,f,param):
    """ordered amplitude M(1..n); gram[i][j]=p_i.p_j (Fractions); leg k=(f[k],f[k+1]); mu[f]=B m_f"""
    c=mkc(param); cb=[x.conj() for x in c]
    def dot(A,B): return sum(gram[i][j] for i in A for j in B)
    def vert(moms,gaps):
        m=len(moms); tot=G(0)
        for k in range(1,m):
            l=m-k; coef=G(Fr(1,2))*c[k]*cb[l]
            s=Fr(0)
            for r in range(m):
                for a in range(k):
                    for b in range(k,m):
                        s+= -dot(moms[(a+r)%m],moms[(b+r)%m])
            tot=tot+coef*s
        cm=c[m]+cb[m]
        if not cm.iszero(): tot=tot+cm*sum(mu[g] for g in gaps)
        return iG*tot
    memo={}
    def J(a,b):  # current for legs a..b (inclusive), b<n-1 ; returns G
        if a==b: return G(1)
        if (a,b) in memo: return memo[(a,b)]
        P=list(range(a,b+1)); tot=G(0)
        for parts in splits(a,b):
            if len(parts)%2==0: continue  # need odd #subcurrents (even vertex)
            moms=[list(range(x,y+1)) for x,y in parts]+[[-1]]
            gaps=[f[x] for x,y in parts]+[f[b+1]]
            pr=G(1)
            for x,y in parts: pr=pr*J(x,y)
            tot=tot+vert2(moms,gaps,P)*pr
        prop=iG*G(dot(P,P)-mu[f[a]]-mu[f[b+1]]).inv()
        memo[(a,b)]=prop*tot; return memo[(a,b)]
    def vert2(moms,gaps,P):
        # replace [-1] (off-shell leg, momentum -P) using linearity
        mm=[]
        for x in moms:
            mm.append(x)
        # implement dot with sign: represent offshell leg as ('neg',P)
        return vertS(mm,gaps,P)
    def vertS(moms,gaps,P):
        def d(A,B):
            sa=-1 if A==[-1] else 1; sb=-1 if B==[-1] else 1
            A=P if A==[-1] else A; B=P if B==[-1] else B
            return sa*sb*dot(A,B)
        m=len(moms); tot=G(0)
        for k in range(1,m):
            l=m-k; coef=G(Fr(1,2))*c[k]*cb[l]; s=Fr(0)
            for r in range(m):
                for a in range(k):
                    for b in range(k,m): s+=-d(moms[(a+r)%m],moms[(b+r)%m])
            tot=tot+coef*s
        cm=c[m]+cb[m]
        if not cm.iszero(): tot=tot+cm*sum(mu[g] for g in gaps)
        return iG*tot
    # full amplitude: leg n-1 is the root
    tot=G(0)
    for parts in splits(0,n-2):
        if len(parts)%2==0: continue
        moms=[list(range(x,y+1)) for x,y in parts]+[[n-1]]
        gaps=[f[x] for x,y in parts]+[f[n-1]]
        pr=G(1)
        for x,y in parts: pr=pr*J(x,y)
        tot=tot+vertS(moms,gaps,[])*pr
    return tot*G(0,-1)  # iM -> M
def splits(a,b):
    # ordered compositions of [a..b] into >=2 contiguous blocks
    L=b-a+1
    for cut in range(1,2**(L-1)):
        parts=[];s=a
        for i in range(L-1):
            if cut>>i&1: parts.append((s,a+i)); s=a+i+1
        parts.append((s,b)); yield parts
def kin(n,msq,zeros,rng):
    """random rational Gram satisfying p_i^2=msq[i], sum_j p_i.p_j=0, and p_i.p_j=0 for (i,j) in zeros"""
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    free=[p for p in pairs if p not in zeros]
    import sympy as sp
    x=sp.symbols('x0:%d'%len(free)); val={p:x[k] for k,p in enumerate(free)}
    for z in zeros: val[z]=0
    eqs=[msq[i]+sum(val[tuple(sorted((i,j)))] for j in range(n) if j!=i) for i in range(n)]
    sol=sp.solve(eqs,[v for v in x],dict=True)[0]
    subs={v:sp.Rational(rng.randint(-40,40),rng.randint(1,7)) for v in x if v not in sol}
    g=[[Fr(0)]*n for _ in range(n)]
    for i in range(n): g[i][i]=Fr(msq[i])
    for p,v in val.items():
        e=sp.sympify(v).xreplace(sol).xreplace(subs) if v!=0 else 0
        e=sp.expand(sp.sympify(e).xreplace(subs))
        e=sp.Rational(e); g[p[0]][p[1]]=g[p[1]][p[0]]=Fr(int(e.p),int(e.q))
    return g
