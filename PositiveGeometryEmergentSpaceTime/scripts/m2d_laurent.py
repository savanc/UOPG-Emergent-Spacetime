import sympy as sp, itertools
eps=sp.Symbol('epsilon')
exec(open('scripts/m2d_nlsm_check.py').read().split("out = []")[0].split("d, eps =")[0])
def Xsym(n):
    return {(i, j): sp.Symbol(f'X{i}{j}') for i in range(1, n + 1) for j in range(i + 2, n + 1) if not (i == 1 and j == n)}
def par(k):
    a,b=k
    return 'ee' if a%2==0 and b%2==0 else 'oo' if a%2 and b%2 else 'oe'
def run(n,power):
    X=Xsym(n)
    chords=list(X)
    cross=lambda a,b:(a[0]<b[0]<a[1]<b[1]) or (b[0]<a[0]<b[1]<a[1])
    Ts=[T for T in itertools.combinations(chords,n-3) if all(not cross(a,b) for a,b in itertools.combinations(T,2))]
    fac={k:(1-eps*X[k]) if par(k)=='oo' else (1+eps*X[k]) if par(k)=='ee' else X[k] for k in chords}
    D=sp.Mul(*fac.values())
    N=0
    for T in Ts:
        k=sum(1 for ch in T if par(ch)!='oe')
        sign=(-1)**sum(1 for ch in T if par(ch)=='oo')
        rest=sp.Mul(*[fac[c] for c in chords if c not in T])
        N+=sign*eps**(k-power)*rest
    N=sp.expand(N)
    return X,D,N
for n,p in ((4,2),(5,2),(5,1),(6,4)):
    X,D,N=run(n,p)
    print(n,p,'min eps power', min(sp.Poly(N*eps**10,eps).monoms())[0]-10 if N!=0 else None,'terms',len(N.as_ordered_terms()),'deg',sp.degree(N,eps))
    print('  D=',D); print('  N(0)=',sp.factor(N.subs(eps,0)))
    if n==6:
        pass
