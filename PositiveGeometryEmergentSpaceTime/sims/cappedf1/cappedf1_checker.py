"""CAPPED-FORMAN-1 locked checker (CPU only, exact integer optimal transport; two independent solvers + an LP cross-check).
Claim (papers/paper-curvature/main.tex prop:capped / conj:capped): for every edge e of a simple D-polytope,
    kappa(e) >= B(e) := 1 - sum_{2-faces F > e} min(3, k_F - 3) / (D+1)    (prop:capped, paper-proved; Jost-Munch Cor 6.2)
and (conj:capped) kappa(e) == B(e), where kappa = Ollivier curvature, uniform measure on the closed ball (idleness 1/(D+1)).
Prereg: prereg/CAPPED-FORMAN-1-capped-forman-equality-2026-10-31.md. Modes: planted | broken | live (each guarded).
Polytopes are combinatorial: a simple D-polytope is given by its vertex-facet incidences (vertex = frozenset of D facet
labels). Edges = vertex pairs sharing D-1 facets; the 2-face through a (D-2)-set S of facets = {v : S <= facets(v)}."""
import sys, json, itertools, random, time, os
from fractions import Fraction as Fr
from pathlib import Path
from math import comb, cos, pi
import numpy as np
import networkx as nx
from scipy.optimize import linear_sum_assignment, linprog
from scipy.spatial import ConvexHull
HERE = str(Path(__file__).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guard import guard
PREREG = 'prereg/CAPPED-FORMAN-1-capped-forman-equality-2026-10-31.md'
OUT = Path(__file__).resolve().parent
SEED = 20261031
WORKERS = 7
LP_TOL = 1e-6

# ============================ combinatorial engine ============================
class Poly:
    def __init__(self, name, family, verts):
        self.name, self.family = name, family
        self.V = [frozenset(v) for v in verts]
        if len(set(self.V)) != len(self.V): raise ValueError(f'{name}: duplicate vertices')
        Ds = {len(v) for v in self.V}
        if len(Ds) != 1: raise ValueError(f'{name}: not simple (facet counts {Ds})')
        self.D = D = Ds.pop()
        sub = {}
        for i, v in enumerate(self.V):
            for s in itertools.combinations(sorted(v, key=repr), D - 1): sub.setdefault(frozenset(s), []).append(i)
        self.adj = [set() for _ in self.V]; self.E = []
        for s, l in sub.items():
            if len(l) != 2: raise ValueError(f'{name}: (D-1)-set in {len(l)} vertices (not a simple polytope)')
            a, b = l; self.adj[a].add(b); self.adj[b].add(a); self.E.append((min(a, b), max(a, b)))
        if any(len(n) != D for n in self.adj): raise ValueError(f'{name}: not D-regular')
        self.E.sort()
        self.face = {}
        if D >= 2:
            for i, v in enumerate(self.V):
                for s in itertools.combinations(sorted(v, key=repr), D - 2): self.face.setdefault(frozenset(s), set()).add(i)
            for s, F in self.face.items():           # each 2-face must be an induced cycle
                if len(F) < 3 or any(len(self.adj[u] & F) != 2 for u in F): raise ValueError(f'{name}: 2-face not a cycle')
                comp = {next(iter(F))}; st = list(comp)
                while st:
                    u = st.pop()
                    for w in self.adj[u] & F:
                        if w not in comp: comp.add(w); st.append(w)
                if comp != F: raise ValueError(f'{name}: 2-face disconnected')
        if not nx.is_connected(nx.Graph(self.E)): raise ValueError(f'{name}: graph disconnected')
    def faces_at(self, x, y):
        S = self.V[x] & self.V[y]
        return [self.face[S - {f}] for f in S] if self.D >= 2 else []

def polygon(k): return Poly(f'C{k}', 'polygon', [{('p', i), ('p', (i - 1) % k)} for i in range(k)])
def simplex(n): return Poly(f'S{n}', 'simplex', [{('s', j) for j in range(n + 1) if j != i} for i in range(n + 1)])
def product(P, Q, name=None, family='product'):
    return Poly(name or f'{P.name}x{Q.name}', family,
                [{('L',) + (f,) for f in a} | {('R',) + (f,) for f in b} for a in P.V for b in Q.V])
def segment(): return Poly('I', 'segment', [{('s', 1)}, {('s', 0)}])
def cube(d):
    P = segment()
    for _ in range(d - 1): P = product(P, segment())
    return Poly(f'Q{d}', 'hypercube', P.V)
def permutohedron(n):
    return Poly(f'Pi{n}', 'permutohedron', [{frozenset(s[:j]) for j in range(1, n)} for s in itertools.permutations(range(n))])
def graph_associahedron(Gadj, name, family):
    n = len(Gadj); nodes = range(n)
    def connected(S):
        S = set(S); st = [next(iter(S))]; seen = {st[0]}
        while st:
            u = st.pop()
            for w in Gadj[u]:
                if w in S and w not in seen: seen.add(w); st.append(w)
        return seen == S
    tubes = [frozenset(S) for r in range(1, n) for S in itertools.combinations(nodes, r) if connected(S)]
    def compat(a, b):
        if a <= b or b <= a: return True
        if a & b: return False
        return not any(Gadj[u] & b for u in a)          # disjoint and non-adjacent
    idx = {t: i for i, t in enumerate(tubes)}
    C = [set(j for j, u in enumerate(tubes) if j != i and compat(t, u)) for i, t in enumerate(tubes)]
    out = []
    def bt(cur, cand):
        if len(cur) == n - 1: out.append(frozenset(tubes[i] for i in cur)); return
        for i in sorted(cand):
            if cur and i < cur[-1]: continue
            bt(cur + [i], cand & C[i])
    bt([], set(range(len(tubes))))
    return Poly(name, family, out)
def g_path(n): return [set(j for j in (i - 1, i + 1) if 0 <= j < n) for i in range(n)]
def g_cycle(n): return [{(i - 1) % n, (i + 1) % n} for i in range(n)]
def g_complete(n): return [set(range(n)) - {i} for i in range(n)]
def g_star(n): return [set(range(1, n))] + [{0} for _ in range(1, n)]
def truncate(P, T, tag):
    """Truncate the face {v : T <= facets(v)} (T a set of facet labels), new facet ('t', tag)."""
    T = frozenset(T); G = {i for i, v in enumerate(P.V) if T <= v}
    if not G or len(G) == len(P.V): raise ValueError('bad truncation face')
    nv = [v for i, v in enumerate(P.V) if i not in G]
    for i in G:
        for j in P.adj[i]:
            if j not in G: nv.append((P.V[i] & P.V[j]) | {('t', tag)})
    return Poly(f'{P.name}|t{tag}', 'truncation', nv)
def gale(D, m):
    out = []
    for S in itertools.combinations(range(m), D):
        s = set(S); ok = True
        for i, j in itertools.combinations([t for t in range(m) if t not in s], 2):
            if sum(1 for t in S if i < t < j) % 2: ok = False; break
        if ok: out.append({('c', t) for t in S})
    return Poly(f'Cyc{D}({m})*', 'dual-cyclic', out)
def random_dual(D, npts, rng, name):
    X = rng.standard_normal((npts, D)); X /= np.linalg.norm(X, axis=1)[:, None]
    H = ConvexHull(X)
    return Poly(name, f'random-dual-{D}D', [{('r', int(t)) for t in s} for s in H.simplices])
COX = {'A3': [[1, 3, 2], [3, 1, 3], [2, 3, 1]], 'B3': [[1, 4, 2], [4, 1, 3], [2, 3, 1]], 'H3': [[1, 5, 2], [5, 1, 3], [2, 3, 1]],
       'A4': [[1, 3, 2, 2], [3, 1, 3, 2], [2, 3, 1, 3], [2, 2, 3, 1]], 'B4': [[1, 4, 2, 2], [4, 1, 3, 2], [2, 3, 1, 3], [2, 2, 3, 1]],
       'F4': [[1, 3, 2, 2], [3, 1, 4, 2], [2, 4, 1, 3], [2, 2, 3, 1]]}
def wythoff(group, rings):
    M = np.array(COX[group]); n = len(M)
    Gm = np.array([[1.0 if i == j else -cos(pi / M[i][j]) for j in range(n)] for i in range(n)])
    R = np.linalg.cholesky(Gm)                     # rows = simple roots (unit, Gram = Gm)
    refl = [np.eye(n) - 2 * np.outer(r, r) for r in R]
    p = np.linalg.solve(R, np.array(rings, dtype=float))     # <r_j, p> = rings_j
    orbit = {tuple(np.round(p, 9)): p}; st = [p]
    while st:
        q = st.pop()
        for S in refl:
            w = S @ q; key = tuple(np.round(w, 9))
            if key not in orbit: orbit[key] = w; st.append(w)
    X = np.array(list(orbit.values())); H = ConvexHull(X)
    planes = {}
    for eq in H.equations:
        key = tuple(np.round(eq / np.linalg.norm(eq[:-1]), 7)); planes.setdefault(key, eq / np.linalg.norm(eq[:-1]))
    PL = list(planes.values())
    verts = [{('w', j) for j, e in enumerate(PL) if abs(e[:-1] @ x + e[-1]) < 1e-7} for x in X]
    return Poly(f'{group}{"".join(map(str, rings))}', 'wythoff', verts)

# ============================ curvature ============================
def dist_local(adj, u, v, V):
    if u == v: return 1 if V.get('no_shared') else 0
    if v in adj[u]: return 1
    if adj[u] & adj[v]: return 2
    return 2 if V.get('dist_cap2') else 3          # d <= 3 for u in B(x), v in B(y), x ~ y
def measures(adj, x, y, idle, V):
    """Integer masses. idle 'lazy': closed ball, 1 each; 'half': centre D, neighbours 1; 'zero': open ball, 1 each."""
    if V.get('open_nbhd') and idle == 'lazy': idle = 'zero'
    if V.get('half_as_lazy') and idle == 'half': idle = 'lazy'
    def m(z):
        D = len(adj[z])
        if idle == 'lazy': return {**{w: 1 for w in adj[z]}, z: 1}
        if idle == 'half': return {**{w: 1 for w in adj[z]}, z: D}
        return {w: 1 for w in adj[z]}
    return m(x), m(y)
def tot(mu): return sum(mu.values())
def cost_hungarian(adj, mx, my, V):
    A = [a for a, k in sorted(mx.items()) for _ in range(k)]; B = [b for b, k in sorted(my.items()) for _ in range(k)]
    C = np.array([[dist_local(adj, a, b, V) for b in B] for a in A], dtype=np.int64)
    if V.get('diag'): return int(np.trace(C))
    r, c = linear_sum_assignment(C); return int(C[r, c].sum())
def cost_flow(adj, mx, my, V):
    G = nx.DiGraph()
    for a, k in mx.items(): G.add_node(('a', a), demand=-k)
    for b, k in my.items(): G.add_node(('b', b), demand=k)
    for a in mx:
        for b in my: G.add_edge(('a', a), ('b', b), weight=dist_local(adj, a, b, V), capacity=tot(mx))
    c = int(nx.min_cost_flow_cost(G))
    return c + 1 if V.get('flow_offset') and (len(mx) % 2 == 0) else c
def kappa_jm_lp(adj, x, y, V):
    """Munch-Wojciechowski/Jost-Munch non-normalised Ollivier curvature (unit weights, combinatorial Laplacian):
    inf { Lap f(x) - Lap f(y) : f 1-Lipschitz, f(y) - f(x) = 1 },  Lap f(z) = sum_{w~z} (f(w) - f(z)). HiGHS LP."""
    U = sorted(adj[x] | adj[y] | {x, y}); ix = {u: i for i, u in enumerate(U)}; n = len(U)
    c = np.zeros(n)
    for w in adj[x]: c[ix[w]] += 1; c[ix[x]] -= 1
    for w in adj[y]: c[ix[w]] -= 1; c[ix[y]] += 1
    Aub, bub = [], []
    for a, b in itertools.permutations(U, 2):
        r = np.zeros(n); r[ix[a]] = 1; r[ix[b]] = -1; Aub.append(r); bub.append(dist_local(adj, a, b, V))
    Aeq = np.zeros((2, n)); Aeq[0, ix[y]] = 1; Aeq[0, ix[x]] = -1; Aeq[1, ix[x]] = 1
    res = linprog(c, A_ub=np.array(Aub), b_ub=bub, A_eq=Aeq, b_eq=[1, 0], bounds=[(None, None)] * n, method='highs')
    if res.status != 0: raise RuntimeError('LP failed')
    return float(res.fun)

def nonfacial_short_cycles(P, x, y):
    """Lengths of cycles of length <= 5 through the edge xy whose vertex set is not a 2-face (a k-cycle on a k-face's
    vertex set is that face's boundary, since 2-faces are induced cycles)."""
    adj = P.adj; faces = {frozenset(F) for F in P.face.values()}; out = []
    def dfs(path):
        u = path[-1]
        if len(path) >= 3 and x in adj[u] and len(path) <= 5:
            if frozenset(path) not in faces: out.append(len(path))
        if len(path) == 5: return
        for w in adj[u]:
            if w != x and w not in path: dfs(path + [w])
    dfs([x, y])
    return sorted(set(out))

def edge_record(P, x, y, V, sizes_override=None):
    adj, D = P.adj, P.D
    faces = P.faces_at(x, y)
    ks = sorted(len(F) for F in faces) if sizes_override is None else sorted(sizes_override)
    cap = (lambda k: k - 3) if V.get('uncapped') else (lambda k: min(3, k - 3))
    B = 1 - Fr(sum(cap(k) for k in ks), D + 1)
    kF = D + 1 - sum(k - 3 for k in ks)
    # independent Forman counts (original, and the <=5-gon subcomplex K) straight from the face cycles
    def forman(cells):
        par = 0
        for z, o in ((x, y), (y, x)):
            for w in adj[z] - {o}:
                if not any(w in F for F in cells): par += 1
        for F in cells:
            par += sum(1 for a in F for b in adj[a] & F if a < b and not ({a, b} & {x, y}))
        return len(cells) + 2 - par
    F_orig = forman(faces); F_K = forman([F for F in faces if len(F) <= 5])
    out = {'ks': ks, 'B': B, 'kF': kF, 'F_orig': F_orig, 'F_K': F_K}
    for idle in ('lazy', 'half', 'zero'):
        mx, my = measures(adj, x, y, idle, V)
        c1, c2 = cost_hungarian(adj, mx, my, V), cost_flow(adj, mx, my, V)
        out[idle] = (c1, c2, tot(mx))
    out['jm'] = kappa_jm_lp(adj, x, y, V) if not V.get('skip_lp') else None
    out['nfc'] = nonfacial_short_cycles(P, x, y) if sizes_override is None else None
    return out

def judge(rec, D):
    """Per-edge gates. Returns dict of booleans + exact values."""
    c1, c2, n = rec['lazy']; k = 1 - Fr(c1, n)
    h1, h2, nh = rec['half']; kh = 1 - Fr(h1, nh)
    z1, z2, nz = rec['zero']; k0 = 1 - Fr(z1, nz)
    B = rec['B']; csum = (D + 1) * (1 - B)
    b0 = 1 - Fr(1 + csum, D)
    g = {'kappa': k, 'B': B, 'kappa_half': kh, 'kappa0': k0, 'b0': b0,
         'solvers_agree': c1 == c2 and h1 == h2 and z1 == z2,
         'bourne_half': kh == Fr(D + 1, 2 * D) * k,
         'jm_norm': rec['jm'] is None or abs(rec['jm'] - (D + 1) * float(k)) < LP_TOL,
         'forman_id': rec['F_orig'] == rec['kF'] and Fr(rec['F_K']) == (D + 1) * B,
         'ineq': k >= B, 'eq': k == B, 'ineq0': k0 >= b0, 'eq0': k0 == b0,
         'uncapped_link': k == Fr(rec['kF'], D + 1)}
    return g

# ============================ planted controls ============================
def tree_graph(D=3, depth=4):
    adj = [set()]; frontier = [0]
    for d in range(depth):
        nf = []
        for u in frontier:
            for _ in range(D if u == 0 else D - 1):
                adj.append(set()); w = len(adj) - 1; adj[u].add(w); adj[w].add(u); nf.append(w)
        frontier = nf
    return adj
def graph_kappa(adj, x, y, V):
    mx, my = measures(adj, x, y, 'lazy', V); return 1 - Fr(cost_hungarian(adj, mx, my, V), tot(mx)), cost_flow(adj, mx, my, V)

def prism_edge(P, horizontal):
    """Return an edge of the prism C_k x I: horizontal = inside the k-gon, else the rung."""
    for (x, y) in P.E:
        ks = sorted(len(F) for F in P.faces_at(x, y))
        if horizontal and ks[-1] != 4 or not horizontal and ks == [4, 4]: return x, y
        if horizontal and len(P.V) == 8: return x, y
    raise ValueError
def planted_cases():
    """(label, thunk -> (value, expected)). Expected values derived by hand (prereg §4)."""
    T = []
    for k, kap, B in [(3, 1, 1), (4, Fr(2, 3), Fr(2, 3)), (5, Fr(1, 3), Fr(1, 3)), (6, 0, 0), (8, 0, 0)]:
        T.append((f'polygon C{k} lazy kappa=B={kap}', ('poly', k, Fr(kap), Fr(B))))
    T.append(('C6 idleness-0 kappa0=0, b0=-1', ('c6zero',)))
    T.append(('simplex S3=K4 lazy 1, half 2/3, zero 2/3=b0', ('k4',)))
    for n in (4, 5): T.append((f'simplex S{n} lazy 1', ('simplex', n)))
    for d, v in [(3, Fr(1, 2)), (4, Fr(2, 5)), (5, Fr(1, 3))]: T.append((f'Q{d} lazy {v} = B', ('cube', d, v)))
    for k, v in [(4, Fr(1, 2)), (5, Fr(1, 4)), (6, 0), (7, 0), (8, 0), (9, 0)]:
        T.append((f'prism k={k} horizontal kappa={v}=B', ('prism_h', k, v)))
    for k in (5, 7, 8): T.append((f'prism k={k} rung kappa=1/2=B', ('prism_v', k)))
    T.append(('prism k=8 horizontal: uncapped link kF/4=-1/2 fails (kappa 0)', ('prism8_uncapped',)))
    T.append(('truncated cube (B3 110): oct-oct -1/2, tri-oct 1/4', ('tcube',)))
    T.append(('3-regular tree root edge lazy -1/2 (graph only)', ('tree',)))
    T.append(('K5 lazy 1 (graph only)', ('k5',)))
    T.append(('EQ gate fires: Q3 with face sizes mislabelled 6 -> B=-1/2 < kappa=1/2', ('eqfire',)))
    T.append(('INEQ gate fires: Q3 with face sizes mislabelled 3 -> B=1 > kappa=1/2', ('ineqfire',)))
    T.append(('construction agreement: Pi4 orderings == K4-graph-associahedron == A3 Wythoff 111 (edge signatures)', ('pi4agree',)))
    T.append(('construction agreement: Q3 product == B3 Wythoff 100 cube; H3 100 == dodecahedron (20 v, all pentagons)', ('cubeagree',)))
    T.append(('non-facial short cycles: K4 edges {4}, triangular prism edges {5}, Q3 and truncated cube none', ('nfc',)))
    return T
def sig_multiset(P, V):
    out = []
    for x, y in P.E:
        r = edge_record(P, x, y, V); g = judge(r, P.D); out.append((tuple(r['ks']), g['kappa']))
    return sorted(out)
def run_planted(V):
    res = []
    for label, case in planted_cases():
        t = case[0]; ok = False; info = ''
        try:
            if t == 'poly':
                _, k, kap, B = case; P = polygon(k); r = edge_record(P, *P.E[0], V); g = judge(r, 2)
                ok = g['kappa'] == kap and g['B'] == B and g['solvers_agree'] and g['jm_norm']; info = f"{g['kappa']} {g['B']}"
            elif t == 'c6zero':
                P = polygon(6); g = judge(edge_record(P, *P.E[0], V), 2); ok = g['kappa0'] == 0 and g['b0'] == -1; info = f"{g['kappa0']} {g['b0']}"
            elif t == 'k4':
                P = simplex(3); g = judge(edge_record(P, *P.E[0], V), 3)
                ok = g['kappa'] == 1 and g['kappa_half'] == Fr(2, 3) and g['kappa0'] == Fr(2, 3) == g['b0']; info = f"{g['kappa']} {g['kappa_half']} {g['kappa0']}"
            elif t == 'simplex':
                P = simplex(case[1]); g = judge(edge_record(P, *P.E[0], V), P.D); ok = g['kappa'] == 1 == g['B']; info = str(g['kappa'])
            elif t == 'cube':
                P = cube(case[1]); g = judge(edge_record(P, *P.E[0], V), P.D); ok = g['kappa'] == case[2] == g['B']; info = str(g['kappa'])
            elif t == 'prism_h':
                P = product(polygon(case[1]), segment()); x, y = prism_edge(P, True); g = judge(edge_record(P, x, y, V), 3)
                ok = g['kappa'] == case[2] == g['B']; info = f"{g['kappa']} {g['B']}"
            elif t == 'prism_v':
                P = product(polygon(case[1]), segment()); x, y = prism_edge(P, False); g = judge(edge_record(P, x, y, V), 3)
                ok = g['kappa'] == Fr(1, 2) == g['B']; info = str(g['kappa'])
            elif t == 'prism8_uncapped':
                P = product(polygon(8), segment()); x, y = prism_edge(P, True); r = edge_record(P, x, y, V); g = judge(r, 3)
                ok = Fr(r['kF'], 4) == Fr(-1, 2) and not g['uncapped_link'] and g['kappa'] == 0 == g['B']; info = f"kF={r['kF']} B={g['B']}"
            elif t == 'tcube':
                P = wythoff('B3', [1, 1, 0]); vals = {}
                for x, y in P.E:
                    r = edge_record(P, x, y, V); g = judge(r, 3); vals.setdefault(tuple(r['ks']), set()).add((g['kappa'], g['B']))
                ok = len(P.V) == 24 and vals == {(3, 8): {(Fr(1, 4), Fr(1, 4))}, (8, 8): {(Fr(-1, 2), Fr(-1, 2))}}
                info = str({k: sorted(v) for k, v in vals.items()})
            elif t == 'tree':
                adj = tree_graph(); k, c2 = graph_kappa(adj, 0, 1, V); ok = k == Fr(-1, 2) and 4 * (1 - k) == c2; info = str(k)
            elif t == 'k5':
                adj = [set(range(5)) - {i} for i in range(5)]; k, c2 = graph_kappa(adj, 0, 1, V); ok = k == 1 and c2 == 0; info = str(k)
            elif t in ('eqfire', 'ineqfire'):
                P = cube(3); x, y = P.E[0]; s = 6 if t == 'eqfire' else 3
                g = judge(edge_record(P, x, y, V, sizes_override=[s, s]), 3)
                ok = (g['ineq'] and not g['eq']) if t == 'eqfire' else (not g['ineq']); info = f"{g['kappa']} {g['B']}"
            elif t == 'pi4agree':
                a = sig_multiset(permutohedron(4), V); b = sig_multiset(graph_associahedron(g_complete(4), 'GK4', 'x'), V)
                c = sig_multiset(wythoff('A3', [1, 1, 1]), V); ok = a == b == c and len(a) == 36; info = str(sorted(set(a)))
            elif t == 'cubeagree':
                a = sig_multiset(cube(3), V); b = sig_multiset(wythoff('B3', [1, 0, 0]), V); dd = wythoff('H3', [1, 0, 0])
                ok = a == b and len(dd.V) == 20 and all(len(F) == 5 for F in dd.face.values()); info = f'{len(b)} {len(dd.V)}'
            elif t == 'nfc':
                got = [sorted({tuple(nonfacial_short_cycles(P, x, y)) for x, y in P.E}) for P in
                       (simplex(3), product(polygon(3), segment()), cube(3), wythoff('B3', [1, 1, 0]))]
                ok = got == [[(4,)], [(5,)], [()], [()]]; info = str(got)
        except Exception as e:
            ok = False; info = f'EXC {type(e).__name__}: {e}'
        res.append({'label': label, 'pass': bool(ok), 'info': info})
    return res

# ============================ live families ============================
def live_specs():
    """Deterministic list of (name, builder-spec). Built inside workers."""
    S = []
    for k in range(3, 13): S.append(('polygon', k))
    for k in range(3, 13): S.append(('prism', k))
    for g, rings in [(g, r) for g in ('A3', 'B3', 'H3') for r in itertools.product((0, 1), repeat=3) if any(r)]:
        S.append(('wythoff', g, list(rings)))
    for g, rings in [(g, r) for g in ('A4', 'B4', 'F4') for r in itertools.product((0, 1), repeat=4) if any(r)]:
        S.append(('wythoff', g, list(rings)))
    for i in range(120): S.append(('rdual', 3, 6 + (i % 35), i))
    for i in range(60): S.append(('rdual', 4, 7 + (i % 24), 1000 + i))
    for i in range(40): S.append(('rdual', 5, 8 + (i % 13), 2000 + i))
    for i in range(16): S.append(('rdual', 6, 9 + (i % 6), 3000 + i))
    for d in range(3, 9): S.append(('simplex', d))
    for d in range(3, 9): S.append(('cube', d))
    for a in range(3, 11):
        for b in range(a, 11): S.append(('cc', a, b))
    for a in range(3, 7):
        for b in range(a, 7):
            for c in range(b, 7): S.append(('ccc', a, b, c))
    for k in range(3, 10):
        for m in (2, 3): S.append(('cq', k, m))
    for k in range(3, 9):
        for n in (2, 3): S.append(('cs', k, n))
    for n in range(4, 8): S.append(('perm', n))
    for n in range(4, 9): S.append(('ga', 'path', n))
    for n in range(4, 8): S.append(('ga', 'cycle', n))
    for n in range(4, 8): S.append(('ga', 'star', n))
    for n in range(4, 7): S.append(('ga', 'complete', n))
    for i in range(24): S.append(('ga', 'random', 5 + (i % 3), 4000 + i))
    for D, ms in [(4, range(6, 15)), (5, range(7, 14)), (6, range(8, 14)), (7, range(9, 13))]:
        for m in ms: S.append(('dcyc', D, m))
    for i in range(60): S.append(('trunc', i % 6, 3 + (i % 5), 5000 + i))
    return S
def ga_graph(kind, n, seed=None):
    if kind == 'path': return g_path(n)
    if kind == 'cycle': return g_cycle(n)
    if kind == 'star': return g_star(n)
    if kind == 'complete': return g_complete(n)
    rng = random.Random(seed)
    while True:
        adj = [set() for _ in range(n)]
        for i, j in itertools.combinations(range(n), 2):
            if rng.random() < 0.45: adj[i].add(j); adj[j].add(i)
        if nx.is_connected(nx.Graph([(i, j) for i in range(n) for j in adj[i]] + [(i, i) for i in range(n)])) and all(adj): return adj
def trunc_base(b):
    return [lambda: cube(3), lambda: wythoff('H3', [1, 0, 0]), lambda: simplex(4), lambda: cube(4),
            lambda: product(polygon(5), polygon(6)), lambda: simplex(5)][b]()
def build(spec):
    t = spec[0]
    if t == 'polygon': return polygon(spec[1])
    if t == 'prism': P = product(polygon(spec[1]), segment()); return Poly(f'prism{spec[1]}', 'prism', P.V)
    if t == 'wythoff': return wythoff(spec[1], spec[2])
    if t == 'rdual': return random_dual(spec[1], spec[2], np.random.default_rng(spec[3]), f'rdual{spec[1]}D-n{spec[2]}-s{spec[3]}')
    if t == 'simplex': return simplex(spec[1])
    if t == 'cube': return cube(spec[1])
    if t == 'cc': return product(polygon(spec[1]), polygon(spec[2]), family='polygon-product')
    if t == 'ccc': return product(product(polygon(spec[1]), polygon(spec[2])), polygon(spec[3]), family='polygon-product3')
    if t == 'cq': return product(polygon(spec[1]), cube(spec[2]), family='polygon-x-cube')
    if t == 'cs': return product(polygon(spec[1]), simplex(spec[2]), family='polygon-x-simplex')
    if t == 'perm': return permutohedron(spec[1])
    if t == 'ga':
        nm = {'path': 'associahedron', 'cycle': 'cyclohedron', 'star': 'stellohedron', 'complete': 'permutohedron-GA', 'random': 'graph-associahedron'}[spec[1]]
        return graph_associahedron(ga_graph(spec[1], spec[2], spec[3] if len(spec) > 3 else None), f'GA-{spec[1]}{spec[2]}' + (f'-s{spec[3]}' if len(spec) > 3 else ''), nm)
    if t == 'dcyc': return gale(spec[1], spec[2])
    if t == 'trunc':
        P = trunc_base(spec[1]); rng = random.Random(spec[3]); base = P.name
        for s in range(spec[2]):
            dim = rng.randrange(0, P.D - 1)                       # truncate a random face of dim 0..D-2
            v = rng.randrange(len(P.V)); T = rng.sample(sorted(P.V[v], key=repr), P.D - dim)
            P = truncate(P, T, f'{spec[3]}.{s}')
        return Poly(f'{base}+{spec[2]}trunc-s{spec[3]}', 'truncation', P.V)
    raise ValueError(t)

def process(args):
    spec, V = args
    t0 = time.time()
    try: P = build(spec)
    except ValueError as e: return {'spec': spec, 'skipped': str(e)}
    agg = {'spec': spec, 'name': P.name, 'family': P.family, 'D': P.D, 'nV': len(P.V), 'nE': len(P.E), 'nF2': len(P.face),
           'fails': {}, 'n_eq': 0, 'n_strict': 0, 'n_below': 0, 'max_gap': None, 'min_gap': None, 'strict_examples': [],
           'below_examples': [], 'n_scfree': 0, 'n_scfree_strict': 0, 'n_eq0': 0, 'n_ineq0_fail': 0, 'n_uncapped_link': 0, 'sig': {}}
    for x, y in P.E:
        r = edge_record(P, x, y, V); g = judge(r, P.D)
        for key in ('solvers_agree', 'bourne_half', 'jm_norm', 'forman_id'):
            if not g[key]: agg['fails'][key] = agg['fails'].get(key, 0) + 1
        gap = g['kappa'] - g['B']
        agg['max_gap'] = gap if agg['max_gap'] is None else max(agg['max_gap'], gap)
        agg['min_gap'] = gap if agg['min_gap'] is None else min(agg['min_gap'], gap)
        if g['eq']: agg['n_eq'] += 1
        elif g['ineq']:
            agg['n_strict'] += 1
            if len(agg['strict_examples']) < 5: agg['strict_examples'].append({'edge': [x, y], 'ks': r['ks'], 'kappa': str(g['kappa']), 'B': str(g['B']), 'nonfacial': r['nfc']})
        else:
            agg['n_below'] += 1
            if len(agg['below_examples']) < 5: agg['below_examples'].append({'edge': [x, y], 'ks': r['ks'], 'kappa': str(g['kappa']), 'B': str(g['B'])})
        if not r['nfc']: agg['n_scfree'] += 1; agg['n_scfree_strict'] += (not g['eq'])
        agg['n_eq0'] += g['eq0']; agg['n_ineq0_fail'] += (not g['ineq0']); agg['n_uncapped_link'] += g['uncapped_link']
        key = f"D{P.D}:{','.join(map(str, r['ks']))}:{g['kappa']}:nf{''.join(map(str, r['nfc']))}"
        agg['sig'][key] = agg['sig'].get(key, 0) + 1
    agg['max_gap'] = str(agg['max_gap']); agg['min_gap'] = str(agg['min_gap']); agg['secs'] = round(time.time() - t0, 2)
    return agg

def verdict(planted, polys):
    if not planted or not all(p['pass'] for p in planted): return 'ILL-DEFINED (planted control failed)'
    done = [p for p in polys if 'skipped' not in p]
    if not done or sum(p['nE'] for p in done) == 0: return 'ILL-DEFINED (empty run)'
    if any(p['fails'] for p in done): return 'ILL-DEFINED (integrity gate failed: ' + ','.join(sorted({k for p in done for k in p['fails']})) + ')'
    if any(p['n_below'] for p in done): return 'INEQ-FAILS'
    if any(p['n_strict'] for p in done): return 'INEQ-HOLDS+EQ-FAILS'
    return 'INEQ-HOLDS+EQ-HOLDS'

def _run(V, specs, tag):
    guard(PREREG, HERE)
    planted = run_planted(V)
    if V.get('empty'): specs = []
    if specs:
        from multiprocessing import Pool
        with Pool(WORKERS) as pool: polys = pool.map(process, [(s, V) for s in specs], chunksize=1)
    else: polys = []
    v = verdict(planted, polys)
    done = [p for p in polys if 'skipped' not in p]
    summ = {'mode': tag, 'variant': V, 'verdict': v, 'planted_pass': sum(p['pass'] for p in planted), 'planted_total': len(planted),
            'polytopes': len(done), 'skipped': [p for p in polys if 'skipped' in p], 'edges': sum(p['nE'] for p in done),
            'edges_eq': sum(p['n_eq'] for p in done), 'edges_strict': sum(p['n_strict'] for p in done),
            'edges_below': sum(p['n_below'] for p in done),
            'edges_scfree': sum(p['n_scfree'] for p in done), 'edges_scfree_strict': sum(p['n_scfree_strict'] for p in done),
            'max_gap': str(max((Fr(p['max_gap']) for p in done), default=None)) if done else None,
            'min_gap': str(min((Fr(p['min_gap']) for p in done), default=None)) if done else None,
            'by_dim': {}, 'by_family': {}}
    for p in done:
        for k, key in ((p['D'], 'by_dim'), (p['family'], 'by_family')):
            d = summ[key].setdefault(str(k), {'polytopes': 0, 'edges': 0, 'eq': 0, 'strict': 0, 'below': 0, 'scfree': 0, 'scfree_strict': 0, 'eq0': 0, 'ineq0_fail': 0, 'uncapped_link': 0, 'max_gap': '0'})
            d['polytopes'] += 1; d['edges'] += p['nE']; d['eq'] += p['n_eq']; d['strict'] += p['n_strict']; d['below'] += p['n_below']
            d['scfree'] += p['n_scfree']; d['scfree_strict'] += p['n_scfree_strict']
            d['eq0'] += p['n_eq0']; d['ineq0_fail'] += p['n_ineq0_fail']; d['uncapped_link'] += p['n_uncapped_link']
            d['max_gap'] = str(max(Fr(d['max_gap']), Fr(p['max_gap'])))
    return summ, planted, polys

BREAK_VARIANTS = [{'open_nbhd': 1}, {'dist_cap2': 1}, {'no_shared': 1}, {'uncapped': 1}, {'diag': 1}, {'empty': 1}, {'flow_offset': 1}, {'half_as_lazy': 1}]
BREAK_SPECS = [('prism', 7), ('wythoff', 'B3', [1, 1, 0]), ('cube', 4), ('dcyc', 4, 7)]
def planted():
    guard(PREREG, HERE)
    s, pl, polys = _run({}, [], 'planted'); s['verdict_planted_only'] = 'PASS' if s['planted_pass'] == s['planted_total'] else 'FAIL'
    json.dump({'summary': s, 'planted': pl}, open(OUT / 'cappedf1_planted.json', 'w'), indent=1, default=str)
    print(json.dumps({'planted_pass': s['planted_pass'], 'of': s['planted_total']}))
    for p in pl: print(('PASS ' if p['pass'] else 'FAIL ') + p['label'] + ' :: ' + p['info'])
    return s
def broken():
    guard(PREREG, HERE)
    rows = []
    for V in BREAK_VARIANTS:
        s, pl, polys = _run(V, BREAK_SPECS, 'broken')
        rej = s['verdict'].startswith('ILL-DEFINED')
        rows.append({'variant': V, 'verdict': s['verdict'], 'rejected': rej, 'planted_failed': [p['label'] for p in pl if not p['pass']]})
        print(('REJECTED ' if rej else 'NOT-REJECTED ') + json.dumps(V) + ' -> ' + s['verdict'])
    json.dump(rows, open(OUT / 'cappedf1_broken.json', 'w'), indent=1, default=str)
    print('all broken rejected:', all(r['rejected'] for r in rows))
    return rows
def live():
    guard(PREREG, HERE)
    s, pl, polys = _run({}, live_specs(), 'live')
    json.dump({'summary': s, 'planted': pl, 'polytopes': polys}, open(OUT / 'cappedf1_live.json', 'w'), indent=1, default=str)
    print(json.dumps({k: s[k] for k in ('verdict', 'planted_pass', 'planted_total', 'polytopes', 'edges', 'edges_eq', 'edges_strict', 'edges_below', 'edges_scfree', 'edges_scfree_strict', 'max_gap', 'min_gap')}))
    print('SC-DERIVATION:', 'CONSISTENT' if s['edges_scfree_strict'] == 0 else 'VIOLATED')
    print(json.dumps(s['by_dim'], indent=0)); print(json.dumps(s['by_family'], indent=0))
    print('skipped:', [(p['spec'], p['skipped']) for p in s['skipped']])
    return s

if __name__ == '__main__':
    guard(PREREG, HERE)
    {'planted': planted, 'broken': broken, 'live': live}[sys.argv[1]]()
