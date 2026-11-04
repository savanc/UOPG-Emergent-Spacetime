"""FR-WZW rank count (prereg notes/FR-WZW-PREREG-2026-10-16.md). Exact rationals, seed 20261016."""
import random, itertools, sympy as sp
from fractions import Fraction
def qrank(rows):
    A=[[Fraction(int(sp.numer(x)),int(sp.denom(x))) for x in r] for r in rows]
    r=0;nc=len(A[0]) if A else 0
    for c in range(nc):
        p=next((i for i in range(r,len(A)) if A[i][c]!=0),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        for i in range(len(A)):
            if i!=r and A[i][c]!=0:
                f=A[i][c]/A[r][c]; A[i]=[a-f*b for a,b in zip(A[i],A[r])]
        r+=1
    return r
random.seed(20261016)
R = sp.Rational
def kin():
    while True:
        lam=[sp.Matrix([random.randint(-9,9),random.randint(-9,9)]) for _ in range(5)]
        lt=[sp.Matrix([random.randint(-9,9),random.randint(-9,9)]) for _ in range(3)]
        A=sp.Matrix.hstack(lam[3],lam[4])
        if A.det()==0: continue
        S=sum((lam[i]*lt[i].T for i in range(3)),sp.zeros(2,2))
        X=A.solve(-S)  # rows: lt4^T, lt5^T
        lt+= [X[0,:].T, X[1,:].T]
        P=[lam[i]*lt[i].T for i in range(5)]
        assert sum(P,sp.zeros(2,2))==sp.zeros(2,2) and all(p.det()==0 for p in P)
        if any(m.det()==0 for m in [P[i]+P[(i+1)%5] for i in range(5)]): continue
        return P
vec=lambda m:[m[0,0],m[0,1],m[1,0],m[1,1]]
def eps(a,b,c,d): return sp.Matrix([vec(a),vec(b),vec(c),vec(d)]).det()
def s(P,i,j): return (P[i]+P[j]).det()
def X(P): return [s(P,i,(i+1)%5) for i in range(5)]
def monos(k):
    out=[]
    for d in range(k+1):
        for c in itertools.combinations_with_replacement(range(5),d): out.append(c)
    return out
def N(P,coef,ms):
    x=X(P); e=eps(P[0],P[1],P[2],P[3])
    return e*sum(cf*sp.prod([x[i] for i in m]) for cf,m in zip(coef,ms))
cyc=lambda P:[P[1],P[2],P[3],P[4],P[0]]
rev=lambda P:[P[4],P[3],P[2],P[1],P[0]]
par=lambda P:[p.T for p in P]   # transpose = one-axis spatial reflection (det -1 on components)
def basisvals(P,ms):
    x=X(P); e=eps(P[0],P[1],P[2],P[3])
    return [e*sp.prod([x[i] for i in m]) for m in ms]
pts=[kin() for _ in range(40)]
out=[]
for k in range(4):
    ms=monos(k)
    for sigma in (1,-1):
        rows=[]
        for P in pts:
            b=basisvals(P,ms)
            rows.append([u-v for u,v in zip(basisvals(cyc(P),ms),b)])
            rows.append([u-sigma*v for u,v in zip(basisvals(rev(P),ms),b)])
            rows.append([u+v for u,v in zip(basisvals(par(P),ms),b)])
        dim=len(ms)-qrank(rows)
        out.append(f"k={k} sigma={sigma:+d} monomials={len(ms)} dim_N_k={dim}")
# planted tests
def wzw_vertex(P):  # sum over 5 cyclic placements of undifferentiated field
    return sum(eps(*[P[(j+t)%5] for t in range(1,5)]) for j in range(5))
ok_plus=all(sp.simplify(wzw_vertex(P)-5*eps(P[0],P[1],P[2],P[3]))==0 for P in pts[:10])
ok_plus_sym=all(wzw_vertex(cyc(P))==wzw_vertex(P) and wzw_vertex(rev(P))==wzw_vertex(P) and wzw_vertex(par(P))==-wzw_vertex(P) for P in pts[:10])
dec_even=lambda P: X(P)[0]*X(P)[1]
rej_even=any(dec_even(par(P))!=-dec_even(P) for P in pts[:10])
dec_nc=lambda P: eps(P[0],P[1],P[2],P[3])*X(P)[0]
rej_nc=any(dec_nc(cyc(P))!=dec_nc(P) for P in pts[:10])
soft=[]  # Adler: eps vanishes when any argument -> 0 or args dependent (p5 soft => p4=-(p1+p2+p3))
P=pts[0]; soft.append(eps(P[0]*0,P[1],P[2],P[3])==0); soft.append(eps(P[0],P[1],P[2],-(P[0]+P[1]+P[2]))==0)
three=eps(P[0],P[1],-(P[0]+P[1]),P[3])==0
out+= [f"planted P+ (WZW vertex = 5*eps): {ok_plus}", f"planted P+ cyclic/reflection(+1)/parity-odd: {ok_plus_sym}",
       f"decoy parity-even rejected: {rej_even}", f"decoy non-cyclic rejected: {rej_nc}",
       f"Adler soft zeros (p1->0, p5->0): {all(soft)}", f"odd 3-pt factor vanishes (dependent args): {three}",
       "normalisation: constraint system homogeneous linear => solution space closed under c*N for every c in Q (no fixed scale)"]
print("\n".join(out)); open("rank_count_output.txt","w").write("\n".join(out)+"\n")
