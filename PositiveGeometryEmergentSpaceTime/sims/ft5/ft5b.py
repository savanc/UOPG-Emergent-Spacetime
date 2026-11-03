"""FT-5b: one insertion of single-trace O(p^4) MASS operators with exact 2-point handling (dual Gram, resummed
propagators to O(eps), corrected shell, LSZ sqrt(Z)). Dual numbers D over Gaussian rationals G."""
from ft5a import G,Fr,mkc,splits,kin,D,LO,comps,amp_ft2
def Dv(x): return x if isinstance(x,D) else D(G(x))
def vertexD(terms,blocks,gaps,dot,c,cb):
    m=len(blocks); tot=D(0)
    for coef,fac in terms:
        F=len(fac); mins=[0 if f[0]=='M' else (1 if f[1] else 0) for f in fac]
        maxs=[0 if f[0]=='M' else m for f in fac]
        for r in range(m):
            for ks in comps(m,F,mins):
                if any(k>mx for k,mx in zip(ks,maxs)): continue
                pos=r; val=D(G(coef)); moms={}
                for f,k in zip(fac,ks):
                    if f[0]=='M': val=val*D(G(gaps[pos%m])); continue
                    val=val*D((c if f[0]=='U' else cb)[k])
                    legs=[blocks[(pos+j)%m] for j in range(k)]
                    for ix in f[1]: moms.setdefault(ix,[]).append(legs)
                    pos+=k
                for ix,(A,B) in moms.items():
                    s=D(0)
                    for a in A:
                        for b in B: s=s+dot(a,b)
                    val=val*s*D(G(-1))
                tot=tot+val
    return D(G(0,1))*tot
OPS5={'O5':[(Fr(1),[('U',('m',)),('Ud',('m',)),('M',),('Ud',())]),(Fr(1),[('U',('m',)),('Ud',('m',)),('U',()),('M',)])],
      'O8':[(Fr(1),[('M',),('Ud',()),('M',),('Ud',())]),(Fr(1),[('U',()),('M',),('U',()),('M',)])],
      'Okin':[(Fr(1),[('U',('m',)),('Ud',('m',))])],
      'Omass':[(Fr(1),[('M',),('U',())]),(Fr(1),[('M',),('Ud',())])]}
def eps_only(v): return D(G(0),v.a)  # eps * (value at eps=0)
def k2(terms,s,ma,mb,c,cb):
    """eps-op 2-pt kernel k(s) = V2/i for a line with gaps (ma,mb) at p^2=s (plain G)."""
    gram=[[s]]; dot=lambda A,B: D(G(A[1]*B[1]*gram[0][0]))
    v=vertexD(terms,[((0,),1),((0,),-1)],[ma,mb],dot,c,cb).a
    return v*G(0,-1)
def amplitude(n,f,mu,g0,y,param,terms):
    """g0: LO Gram (Fr), y: eps-part Gram (Fr) ; f closed (len n+1). returns D."""
    c=mkc(param); cb=[x.conj() for x in c]
    gram=[[D(G(g0[i][j]),G(y[i][j])) for j in range(n)] for i in range(n)]
    def dot(A,B):
        s=D(0)
        for i in A[0]:
            for j in B[0]: s=s+gram[i][j]
        return s*D(G(A[1]*B[1]))
    def V(blocks,gaps): return vertexD(LO,blocks,gaps,dot,c,cb)+eps_only(vertexD(terms,blocks,gaps,dot,c,cb))
    memo={}
    def J(a,b):
        if a==b: return D(1)
        if (a,b) in memo: return memo[(a,b)]
        P=list(range(a,b+1)); tot=D(0)
        for parts in splits(a,b):
            blocks=[(tuple(range(x,y+1)),1) for x,y in parts]+[(tuple(P),-1)]
            gaps=[mu[f[x]] for x,y in parts]+[mu[f[b+1]]]
            pr=D(1)
            for x,y in parts: pr=pr*J(x,y)
            tot=tot+V(blocks,gaps)*pr
        bl=[(tuple(P),1),(tuple(P),-1)]; ga=[mu[f[a]],mu[f[b+1]]]
        K=vertexD(LO,bl,ga,dot,c,cb)*D(G(0,-1)) + eps_only(vertexD(terms,bl,ga,dot,c,cb)*D(G(0,-1)))
        memo[(a,b)]=D(G(0,1))*K.inv()*tot; return memo[(a,b)]
    tot=D(0)
    for parts in splits(0,n-2):
        blocks=[(tuple(range(x,y+1)),1) for x,y in parts]+[((n-1,),1)]
        gaps=[mu[f[x]] for x,y in parts]+[mu[f[n-1]]]
        pr=D(1)
        for x,y in parts: pr=pr*J(x,y)
        tot=tot+V(blocks,gaps)*pr
    M=tot*D(G(0,-1))
    lsz=D(1)
    for i in range(n):
        al=k2(terms,Fr(1),mu[f[i]],mu[f[i+1]],c,cb)-k2(terms,Fr(0),mu[f[i]],mu[f[i+1]],c,cb)
        lsz=lsz*D(G(1),G(Fr(-1,2))*al)
    return M*lsz
def shifts(n,f,mu,terms):
    c=mkc('exp'); cb=[x.conj() for x in c]; out=[]
    for i in range(n):
        M0=mu[f[i]]+mu[f[i+1]]
        b=k2(terms,Fr(0),mu[f[i]],mu[f[i+1]],c,cb); al=k2(terms,Fr(1),mu[f[i]],mu[f[i+1]],c,cb)-b
        d=-(al*G(M0)+b); assert d.b==0; out.append(d.a)
    return out
