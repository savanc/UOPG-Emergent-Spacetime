"""COS-1r: mapped tree wavefunctions psi_G(s) of 2610.01775 (eq. 2.14); check that every quoted zero
needs some mapped channel s_S <= 0 (i.e. a non-positive tube energy under E_S <-> s_S)."""
import itertools, sympy as sp, random
def conn(S,E):
    S=set(S); st=[next(iter(S))]; seen={st[0]}
    while st:
        u=st.pop()
        for a,b in E:
            for x,y in ((a,b),(b,a)):
                if x==u and y in S and y not in seen: seen.add(y); st.append(y)
    return seen==S
def tubes(V,E): return [frozenset(S) for k in range(2,len(V)) for S in itertools.combinations(V,k) if conn(S,E)]
def compat(A,B,E,nonadj):
    if A<=B or B<=A: return True
    if A&B: return False
    return (not conn(A|B,E)) if nonadj else True
def psi(V,E,s,nonadj):
    T=tubes(V,E); tot=0; cnt=0
    for tau in itertools.combinations(T,len(V)-2):
        if all(compat(a,b,E,nonadj) for a,b in itertools.combinations(tau,2)):
            cnt+=1; tot+=sp.Mul(*[1/s(S) for S in tau])
    return tot,cnt,T
out=[]
def setup(V):
    t={p:sp.Symbol(f"t{p[0]}{p[1]}") for p in itertools.combinations(V,2)}
    s=lambda S: sum(t[p] for p in itertools.combinations(sorted(S),2))
    return t,s
# rule check: chain 1-2-3-4 -> 5 tubings, 222 star -> 6
for nonadj in (False,True):
    V=[1,2,3,4]; t,s=setup(V)
    c1=psi(V,[(1,2),(2,3),(3,4)],s,nonadj)[1]; c2=psi(V,[(1,3),(2,3),(3,4)],s,nonadj)[1]
    print(f"rule nonadjacent={nonadj}: chain4 tubings={c1} (paper 5), 222 tubings={c2} (paper 6)")
NONADJ=False  # paper rule: nested or disjoint (matches 5 and 6 tubings)
cases={
 "222 blob c12=c14=0 (5.11)":([1,2,3,4],[(1,3),(2,3),(3,4)],lambda t,s:[t[(1,2)],t[(1,4)]]),
 "222 non-blob (6.15)":([1,2,3,4],[(1,3),(2,3),(3,4)],lambda t,s:[s({1,3})+s({2,3}),s({1,3,4})+s({1,3})+s({3,4}),s({2,3,4})+s({2,3})+s({3,4})]),
 "2222 non-blob (6.16)":([1,2,3,4,5],[(1,3),(2,3),(3,4),(3,5)],lambda t,s:[s({1,3})+s({3,4}),s({2,3})+s({3,5}),s({1,2,3,4})+s({1,2,3,5}),s({1,2,3,5})+s({1,3,4,5})]),
 "223 non-blob (6.17)":([1,2,3,4,5],[(1,3),(2,3),(3,4),(4,5)],lambda t,s:[s({2,3,4})+s({3,4,5}),s({1,2,3,4})+s({4,5}),s({2,3})+s({1,3,4,5}),s({1,3,4})+s({4,5})-s({1,3,4,5})]),
}
random.seed(3)
for name,(V,E,conds) in cases.items():
    t,s=setup(V); P,cnt,T=psi(V,E,s,NONADJ)
    eqs=conds(t,s)+[s(set(V))]                     # mapped kinematics: s_V = 0
    vs=list(t.values()); (solt,)=sp.linsolve(eqs,vs); sol=dict(zip(vs,solt))
    Pz=sp.simplify(P.subs(sol))
    lin=[sp.expand(s(S).subs(sol)) for S in T]
    free=sorted(set().union(*[l.free_symbols for l in lin]),key=str)
    f=sp.lambdify(free,lin); allpos=0; tried=20000
    for _ in range(tried):
        allpos+=all(v>0 for v in f(*[random.uniform(-1,1) for _ in free]))
    print(f"{name}: tubings={cnt}; psi on locus = {Pz}; random points with ALL mapped channels > 0: {allpos}/{tried}")
    print(f"   channels on locus: "+", ".join(f"s{''.join(map(str,sorted(S)))}={l}" for S,l in zip(T,lin)))

