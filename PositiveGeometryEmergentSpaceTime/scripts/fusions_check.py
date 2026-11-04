import itertools
def classes(adj,n):
    reach=[set([a]) for a in range(n)]
    for a in range(n):
        st=[a]
        while st:
            x=st.pop()
            for y in range(n):
                if adj[x][y] and y not in reach[a]: reach[a].add(y); st.append(y)
    cls=[frozenset(b for b in range(n) if b in reach[a] and a in reach[b]) for a in range(n)]
    # recurrent iff class closed
    rec=[all(reach[a] <= cls[a] for _ in [0]) for a in range(n)]
    return cls,rec
def sigma(adj,n):
    cls,rec=classes(adj,n); out=[]
    for a in range(n):
        if not rec[a]: out.append(a+1); continue
        others=[(c-a)%n for c in cls[a] if c!=a]
        out.append(a+1 + (max(others) if others else n))
    return tuple(out)
def total_decorated(n):
    return sum(1 for p in itertools.permutations(range(n)) for _ in range(2**sum(1 for i in range(n) if p[i]==i)))
for n in [2,3,4]:
    verts=set(); allk=set()
    for f in itertools.product(range(n),repeat=n):
        adj=[[1 if f[a]==b else 0 for b in range(n)] for a in range(n)]
        verts.add(sigma(adj,n))
    for rows in itertools.product([r for r in itertools.product([0,1],repeat=n) if any(r)],repeat=n):
        allk.add(sigma(rows,n))
    print(f"n={n}: vertices give {len(verts)} distinct; all kernels (support patterns) give {len(allk)}; total decorated perms of [n] = {total_decorated(n)}")
# reproduce paper's 9-state example
n=9; f={1:5,5:8,8:1,2:2,3:4,4:3,6:6,7:9,9:7}
adj=[[1 if f[a+1]==b+1 else 0 for b in range(n)] for a in range(n)]
print("example:", list(sigma(adj,n)), "paper: [8, 11, 4, 12, 10, 15, 9, 14, 16]")
for idx,f in [(1,(0,0,0)),(2,(0,0,1)),(3,(0,0,2)),(8,(0,2,1)),(13,(1,1,0)),(15,(1,1,2))]:
    adj=[[1 if f[a]==b else 0 for b in range(3)] for a in range(3)]
    print("vertex",idx,list(sigma(adj,3)))
