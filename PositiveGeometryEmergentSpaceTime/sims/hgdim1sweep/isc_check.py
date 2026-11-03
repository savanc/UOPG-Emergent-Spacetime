# (1) independent-short-cycle check on associahedron K_n; (2) idleness-0 Ollivier vs KTB-type prediction (1-p)/D
import itertools, json, sys
sys.path.insert(0,'/tmp/sweep')
from forman_check import ncsets, cells
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from collections import deque
out={}
for n in range(5,10):
    T=ncsets(n,n-3); idx={t:i for i,t in enumerate(T)}; D=n-3
    adj=[[] for _ in T]
    for t in T:
        for d in t:
            rest=t-{d}
            u=[x for x in T if rest<=x and x!=t][0]
            adj[idx[t]].append(idx[u])
    def bfs(s,cut=4):
        dist={s:0};q=deque([s])
        while q:
            x=q.popleft()
            if dist[x]>=cut: continue
            for y in adj[x]:
                if y not in dist: dist[y]=dist[x]+1;q.append(y)
        return dist
    # short cycles through edge (a,b): simple cycles length 3..5 containing edge
    viol=0; mismatch=0; lp_bad=0; nedges=0
    for a in range(len(T)):
        for b in adj[a]:
            if b<a: continue
            nedges+=1
            cyc=[]
            def dfs(path):
                if len(path)>5: return
                x=path[-1]
                for y in adj[x]:
                    if y==a and len(path)>=3: cyc.append(tuple(path))
                    elif y not in path: dfs(path+[y])
            dfs([a,b])
            cycsets=[frozenset(zip(c,c[1:]+(c[0],))) for c in cyc]
            cycsets=[frozenset(frozenset(e) for e in c) for c in cycsets]
            cycsets=list(set(cycsets))
            for c1,c2 in itertools.combinations(cycsets,2):
                if len(c1&c2)>1: viol+=1
            ta,tb=T[a],T[b]; rest=ta&tb
            dd=list(ta-rest)[0]; ee=list(tb-rest)[0]
            quad=sorted(set(dd)|set(ee))
            sides=[tuple(sorted((quad[i],quad[(i+1)%4]))) for i in range(4)]
            p=sum(1 for s in sides if s in rest)
            s4=sum(1 for c in cycsets if len(c)==4); s5=sum(1 for c in cycsets if len(c)==5); s3=sum(1 for c in cycsets if len(c)==3)
            if not (s3==0 and s5==p and s4==D-1-p): mismatch+=1
            # idleness-0 Ollivier via LP
            if n<=8:
                A=adj[a]; B=adj[b]; dist={x:bfs(x) for x in A}
                C=np.array([[dist[x].get(y,9) for y in B] for x in A],float)
                m=len(A); k=len(B)
                Aeq=[];beq=[]
                for i in range(m):
                    r=np.zeros(m*k); r[i*k:(i+1)*k]=1; Aeq.append(r); beq.append(1/D)
                for j in range(k):
                    r=np.zeros(m*k); r[j::k]=1; Aeq.append(r); beq.append(1/D)
                res=linprog(C.flatten(),A_eq=np.array(Aeq),b_eq=beq,bounds=(0,None),method='highs')
                k0=1-res.fun
                if abs(k0-(1-p)/D)>1e-9: lp_bad+=1
    out[n]=dict(edges=nedges,isc_violations=viol,cycle_count_mismatch=mismatch,idle0_mismatch=lp_bad if n<=8 else None)
    print(n,out[n],flush=True)
json.dump({str(k):v for k,v in out.items()},open('/tmp/sweep/isc_check.json','w'),indent=1)
