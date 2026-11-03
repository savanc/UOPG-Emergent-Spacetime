# Independent check: Forman-Ricci (De Loera et al. Def 1.2 / Lemma 2.1) on associahedron K_n
import itertools, json
from fractions import Fraction as F
def diags(n): return [(i,j) for i in range(n) for j in range(i+2,n) if not (i==0 and j==n-1)]
def cross(a,b):
    (i,j),(k,l)=a,b
    return (i<k<j<l) or (k<i<l<j)
def ncsets(n,m):
    D=diags(n); out=[]
    def rec(start,cur):
        if len(cur)==m: out.append(frozenset(cur)); return
        for t in range(start,len(D)):
            if all(not cross(D[t],c) for c in cur): rec(t+1,cur+[D[t]])
    rec(0,[]); return out
def cells(n,S):
    # polygon cell sizes of dissection S
    polys=[list(range(n))]
    for (i,j) in S:
        for P in polys:
            if i in P and j in P:
                a,b=sorted((P.index(i),P.index(j)))
                if b-a>=2 and not (a==0 and b==len(P)-1):
                    polys.remove(P); polys+= [P[a:b+1], P[b:]+P[:a+1]]; break
    return sorted(len(P) for P in polys)
res={}
for n in range(5,11):
    D=n-3
    T=ncsets(n,n-3); E=ncsets(n,n-4); Fc=ncsets(n,n-5)
    f0,f1=len(T),len(E)
    pk={}
    for S in Fc:
        c=cells(n,S); k=5 if 5 in c else 4
        pk[k]=pk.get(k,0)+1
    f02=sum(k*v for k,v in pk.items())
    K=F(6*f02+4*f1-D*D*f0-sum(k*k*v for k,v in pk.items()),f1)
    target=F(10-n,2*n-5)
    oll=F(10-n,(n-2)*(2*n-5))
    res[n]=dict(f0=f0,f1=f1,squares=pk.get(4,0),pentagons=pk.get(5,0),K_Forman=str(K),pred_10mn_over_2nm5=str(target),match=K==target,K_over_Dplus1=str(K/(D+1)),ollivier_mean=str(oll),match_oll=K/(D+1)==oll)
    print(n,res[n])
json.dump(res,open('/tmp/sweep/forman_check.json','w'),indent=1)

print("direct per-edge p check")
for n in range(5,11):
    T=ncsets(n,n-3); D=n-3; S=set(T); tot=F(0); cnt=0
    for t in T:
        for d in t:
            rest=t-{d}
            others=[u for u in T if rest<=u and u!=t]
            assert len(others)==1
            u=others[0]
            if tuple(sorted(t))>tuple(sorted(u)): continue
            e=list(u-rest)[0]
            quad=sorted(set(d)|set(e))
            sides=[(quad[i],quad[(i+1)%4]) for i in range(4)]
            sides=[tuple(sorted(s)) for s in sides]
            p=sum(1 for s in sides if s in rest)
            tot+=2-p; cnt+=1
    print(n,cnt,tot/cnt,F(10-n,2*n-5))
