"""Generate the K_7 Lean certificate data (post-live; not part of the locked checker; scoring untouched).
Imports only the pure graph builder from the locked checker module (no guarded function called)."""
import json, collections
import numpy as np
from scipy.optimize import linprog, linear_sum_assignment
import importlib.util, sys
spec = importlib.util.spec_from_file_location('c', 'hgdim1_checker.py'); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
n = 7
diags = [(a, b) for a in range(n) for b in range(a + 2, n) if not c.is_poly_edge(n, a, b)]
adj, pval, Ts = c.flip_graph(n, {})
mask = [sum(1 << diags.index(d) for d in t) for t in Ts]
N = len(Ts)
def bfs(s):
    dist = {s: 0}; par = {s: None}; q = collections.deque([s])
    while q:
        u = q.popleft()
        for w in sorted(adj[u]):
            if w not in dist: dist[w] = dist[u] + 1; par[w] = u; q.append(w)
    return dist, par
def path(s, t):
    _, par = bfs(s); p = [t]
    while p[-1] != s: p.append(par[p[-1]])
    return p[::-1]
def cert(x, y):
    A = sorted(adj[x] | {x}); B = sorted(adj[y] | {y})
    C = np.array([[bfs(a)[0][b] for b in B] for a in A]); r, cc = linear_sum_assignment(C); cost = int(C[r, cc].sum())
    walks = [path(A[i], B[j]) for i, j in zip(r, cc)]
    E = [(u, v) for u in range(N) for v in adj[u] if u < v]
    cvec = np.zeros(N)
    for a in A: cvec[a] -= 1
    for b in B: cvec[b] += 1
    Aub = []; bub = []
    for u, v in E:
        row = np.zeros(N); row[u] = 1; row[v] = -1; Aub.append(row); bub.append(1); Aub.append(-row); bub.append(1)
    bounds = [(0, 0) if i == y else (-10, 10) for i in range(N)]
    res = linprog(cvec, A_ub=np.array(Aub), b_ub=bub, bounds=bounds, method='highs')
    phi = [int(round(v)) for v in res.x]; gap = sum(phi[a] for a in A) - sum(phi[b] for b in B)
    assert gap == cost and all(abs(phi[u] - phi[v]) <= 1 for u, v in E)
    return dict(x=x, y=y, p=pval[(min(x, y), max(x, y))], A=A, B=B, cost=cost, walks=walks, phi=phi)
E = sorted((u, v) for u in range(N) for v in adj[u] if u < v)
e3 = next(e for e in E if pval[e] == 3); e1 = next(e for e in E if pval[e] == 1)
out = dict(diags=diags, mask=mask, neg=cert(*e3), pos=cert(*e1))
json.dump(out, open('lean_cert_k7.json', 'w'), indent=1); print(out['neg']['cost'], out['pos']['cost'], out['neg']['p'], out['pos']['p'], e3, e1)
