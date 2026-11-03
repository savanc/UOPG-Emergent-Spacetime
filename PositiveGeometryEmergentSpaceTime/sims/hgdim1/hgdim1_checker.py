"""HG-DIM-1 locked checker (CPU only, exact integer transport costs; HiGHS LP only as a cross-check).
Question: on the 1-skeleton (flip graph) K_n of the associahedron (trunk positive geometry, ABHY; vertices = triangulations
of a convex n-gon, D = n-3 regular), is Ollivier-Ricci curvature (idleness 1/(D+1), uniform on closed neighbourhoods)
nonnegative ("geometry-bearing", the HYPERGRAPH-note draft prediction), or is it the local polygon count
kappa(e) = (2 - p(e))/(D+1), p(e) = number of sides of the flip quadrilateral that are diagonals (mixed sign for n >= 7)?
Prereg: prereg/HG-DIM-1-associahedron-ollivier-curvature-2026-10-31.md. Modes: planted | broken | live (each guarded)."""
import sys, json, itertools, random
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linear_sum_assignment, linprog
from scipy.stats import ks_2samp
import networkx as nx
HERE = str(Path(__file__).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guard import guard
PREREG = 'prereg/HG-DIM-1-associahedron-ollivier-curvature-2026-10-31.md'
OUT = Path(__file__).resolve().parent
NS = list(range(6, 12))          # live polygons n = 6..11 (D = 3..8)
NULL_NS = [8, 9, 10, 11]         # separation gate sizes
NULL_SEEDS = [20261031, 20261032, 20261033]
LP_SAMPLE, LP_SEED = 300, 20261031
KS_P = 0.01

# ---------------- graphs ----------------
def is_poly_edge(n, a, b):
    a, b = min(a, b), max(a, b); return b - a == 1 or (a == 0 and b == n - 1)
def cross(d1, d2):
    (a, b), (c, d) = sorted(d1), sorted(d2)
    return (a < c < b < d) or (c < a < d < b)
def triangulations(n):
    def tri(i, j):
        if j - i < 2: return [frozenset()]
        out = []
        for k in range(i + 1, j):
            for L in tri(i, k):
                for R in tri(k, j):
                    s = set(L) | set(R)
                    if not is_poly_edge(n, i, k): s.add((i, k))
                    if not is_poly_edge(n, k, j): s.add((k, j))
                    out.append(frozenset(s))
        return out
    return sorted(set(tri(0, n - 1)), key=lambda t: sorted(t))
def flip_graph(n, V):
    Ts = triangulations(n); idx = {t: i for i, t in enumerate(Ts)}
    diags = [(a, b) for a in range(n) for b in range(a + 2, n) if not is_poly_edge(n, a, b)]
    adj = [set() for _ in Ts]; pval = {}
    for t in Ts:
        for d in t:
            rest = t - {d}
            cand = [e for e in diags if e != d and cross(d, e) and not any(cross(e, f) for f in rest)]
            assert len(cand) == 1, 'flip not unique'
            e = cand[0]; u = idx[t]; v = idx[rest | {e}]
            adj[u].add(v); adj[v].add(u)
            a, c = d; b, dd = e
            sides = [(a, b), (b, c), (c, dd), (dd, a)]
            if V.get('p_count_edges'): p = sum(1 for s in sides if is_poly_edge(n, *s))
            else: p = sum(1 for s in sides if not is_poly_edge(n, *s))
            pval[(min(u, v), max(u, v))] = p
    return adj, pval, Ts

# ---------------- curvature ----------------
def dist_local(adj, u, v, V):
    if u == v: return 1 if V.get('no_shared') else 0
    if v in adj[u]: return 1
    if adj[u] & adj[v]: return 2
    return 2 if V.get('dist_cap2') else 3
def supports(adj, x, y, V):
    A = sorted(adj[x]) if V.get('open_nbhd') else sorted(adj[x] | {x})
    B = sorted(adj[y]) if V.get('open_nbhd') else sorted(adj[y] | {y})
    return A, B
def kappa_assign(adj, x, y, V):
    """Uniform closed neighbourhoods, equal degree: exact min-cost assignment; returns Fraction."""
    A, B = supports(adj, x, y, V)
    if len(A) != len(B): raise ValueError('unequal degrees')
    C = np.array([[dist_local(adj, a, b, V) for b in B] for a in A], dtype=np.int64)
    r, c = linear_sum_assignment(C)
    return 1 - F(int(C[r, c].sum()), len(A))
def kappa_lp(adj, x, y, alpha, V):
    """General idleness alpha (Fraction or None = uniform closed nbhd); LP (HiGHS); returns float."""
    if V.get('empty_lp'): return float('nan')
    def meas(z):
        nb = sorted(adj[z])
        if alpha is None: return {w: 1.0 / (len(nb) + 1) for w in nb + [z]}
        m = {w: (1 - float(alpha)) / len(nb) for w in nb}; m[z] = m.get(z, 0) + float(alpha); return m
    mx, my = meas(x), meas(y); A, B = list(mx), list(my)
    C = np.array([[dist_local(adj, a, b, V) for b in B] for a in A], dtype=float)
    na, nb = len(A), len(B); Aeq = []; beq = []
    for i in range(na):
        row = np.zeros(na * nb); row[i * nb:(i + 1) * nb] = 1; Aeq.append(row); beq.append(mx[A[i]])
    for j in range(nb):
        row = np.zeros(na * nb); row[j::nb] = 1; Aeq.append(row); beq.append(my[B[j]])
    res = linprog(C.ravel(), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method='highs')
    return 1 - res.fun
def edges_of(adj):
    return [(u, v) for u in range(len(adj)) for v in adj[u] if u < v]

# ---------------- planted graphs ----------------
def g_complete(m): return [set(range(m)) - {i} for i in range(m)]
def g_cycle(m): return [{(i - 1) % m, (i + 1) % m} for i in range(m)]
def g_cube(d): return [{i ^ (1 << k) for k in range(d)} for i in range(1 << d)]
def g_tree3(depth=4):
    adj = [set()]; frontier = [0]
    for lev in range(depth):
        nf = []
        for u in frontier:
            for _ in range(3 if u == 0 else 2):
                adj.append(set()); w = len(adj) - 1; adj[u].add(w); adj[w].add(u); nf.append(w)
        frontier = nf
    return adj
def g_null(N, D, seed, V, ref=None):
    if V.get('null_same') and ref is not None: return ref
    G = nx.random_regular_graph(D, N, seed=seed)
    return [set(G.neighbors(i)) for i in range(N)]

# ---------------- statistics and verdict ----------------
def census(n, V):
    adj, pval, Ts = flip_graph(n, V); D = n - 3; E = edges_of(adj)
    ks = {e: kappa_assign(adj, *e, V) for e in E}
    formula_ok = all(ks[e] == F(2 - pval[e], D + 1) for e in E)
    vals = list(ks.values())
    s = dict(n=n, D=D, N=len(adj), E=len(E), regular=all(len(a) == D for a in adj),
             formula_ok=formula_ok, n_formula_bad=sum(1 for e in E if ks[e] != F(2 - pval[e], D + 1)),
             kmin=min(vals), kmax=max(vals), kmean=sum(vals, F(0)) / len(vals),
             frac_neg=F(sum(1 for k in vals if k < 0), len(vals)), frac_zero=F(sum(1 for k in vals if k == 0), len(vals)),
             p_hist={str(p): sum(1 for e in E if pval[e] == p) for p in range(5)})
    # LP cross-check of the assignment (all edges n <= 8, seeded sample above)
    r = random.Random(LP_SEED + n); sample = E if len(E) <= LP_SAMPLE or n <= 8 else r.sample(E, LP_SAMPLE)
    s['lp_agree'] = all(abs(kappa_lp(adj, *e, None, V) - float(ks[e])) < 1e-9 for e in sample)
    # convention check (idleness 1/2) on n <= 9: kappa_1/2 = (D+1)/(2D) kappa_1/(D+1) (Bourne et al. 2018, Remark 5.4)
    if n <= 9:
        s['conv_half_ok'] = all(abs(kappa_lp(adj, *e, F(1, 2), V) - float(ks[e]) * (D + 1) / (2 * D)) < 1e-9 for e in E)
    s['_vals'] = vals; s['_adj'] = adj
    return s
def separation(s, V):
    D, N = s['D'], s['N']; out = []
    for seed in NULL_SEEDS:
        g = g_null(N, D, seed, V, ref=s['_adj']); E = edges_of(g)
        vals = [kappa_assign(g, *e, V) for e in E]; m = sum(vals, F(0)) / len(vals)
        p = ks_2samp([float(v) for v in s['_vals']], [float(v) for v in vals]).pvalue
        out.append(dict(seed=seed, null_mean=float(m), null_frac_neg=float(F(sum(1 for v in vals if v < 0), len(vals))),
                        gap=float(s['kmean'] - m), ks_p=float(p), ok=bool(s['kmean'] - m >= F(1, D + 1) and p < KS_P)))
    return out
def verdict(t):
    if not t['planted_ok']: return 'ILL-DEFINED'
    if t['n_sizes'] == 0: return 'ILL-DEFINED'
    if not t['lp_agree_all']: return 'ILL-DEFINED'
    if not t['sep_all']: return 'NULL-LIKE'
    if t['kmin_all'] >= 0: return 'POS-CURVED'
    if t['formula_all'] and t['neg_from7']: return 'LOCAL-COUNT'
    if not t['formula_all']: return 'MIXED-NONLOCAL'
    return 'UNCLASSIFIED'

def _suite(V):
    guard(PREREG, HERE)
    res = {}
    k5 = g_complete(5); res['PL1_complete'] = all(kappa_assign(k5, *e, V) == 1 for e in edges_of(k5))
    c8 = g_cycle(8); res['PL2_cycle8'] = all(kappa_assign(c8, *e, V) == 0 for e in edges_of(c8))
    q4 = g_cube(4); res['PL3_cube4'] = all(kappa_assign(q4, *e, V) == F(2, 5) for e in edges_of(q4))
    t3 = g_tree3(); res['PL4_tree3'] = kappa_assign(t3, 0, 1, V) == F(-1, 2)
    adj5, p5, T5 = flip_graph(5, V)
    res['PL5_pentagon'] = (len(T5) == 5 and all(kappa_assign(adj5, *e, V) == F(1, 3) for e in edges_of(adj5))
                           and all(kappa_assign(adj5, *e, V) == F(2 - p5[e], 3) for e in edges_of(adj5)))
    # PL6 valid alternatives that must be accepted: edge orientation and polygon relabelling (rotation) leave kappa unchanged
    adj7, p7, T7 = flip_graph(7, V); E7 = edges_of(adj7)
    k7 = sorted(kappa_assign(adj7, *e, V) for e in E7)
    rot = {t: frozenset(tuple(sorted(((a + 1) % 7, (b + 1) % 7))) for a, b in t) for t in T7}
    idx = {t: i for i, t in enumerate(T7)}; perm = [idx[rot[t]] for t in T7]
    res['PL6_alternatives'] = (all(kappa_assign(adj7, u, v, V) == kappa_assign(adj7, v, u, V) for u, v in E7[:40])
                               and sorted(kappa_assign(adj7, perm[u], perm[v], V) for u, v in E7) == k7
                               and all(p7[(min(perm[u], perm[v]), max(perm[u], perm[v]))] == p7[(u, v)] for u, v in E7))
    # PL7 LP cross-check and idleness-1/2 relation on planted graphs (cube: kappa_1/2 = 1/4)
    res['PL7_lp'] = (abs(kappa_lp(q4, 0, 1, None, V) - 0.4) < 1e-9 and abs(kappa_lp(q4, 0, 1, F(1, 2), V) - 0.25) < 1e-9
                     and abs(kappa_lp(t3, 0, 1, None, V) + 0.5) < 1e-9)
    # PL8 gate self-tests: formula gate true/false, separation gate true/false
    fq = lambda wrong: all(kappa_assign(q4, *e, V) == (F(2, 4) if wrong else F(2, 5)) for e in edges_of(q4))
    s_cube = dict(D=4, N=16, kmean=F(2, 5), _vals=[F(2, 5)] * 32, _adj=q4)
    sep_true = all(r['ok'] for r in separation(s_cube, V))
    s_self = dict(D=4, N=16, kmean=F(2, 5), _vals=[F(2, 5)] * 32, _adj=q4)
    sep_false = not all(r['ok'] for r in separation(s_self, dict(V, null_same=True)))
    res['PL8_gates'] = fq(False) and not fq(True) and sep_true and sep_false
    # PL9 verdict-map self-test (every branch reachable)
    b = dict(planted_ok=True, n_sizes=6, lp_agree_all=True, sep_all=True, kmin_all=-1, formula_all=True, neg_from7=True)
    res['PL9_verdict'] = (verdict(dict(b, planted_ok=False)) == 'ILL-DEFINED' and verdict(dict(b, n_sizes=0)) == 'ILL-DEFINED'
                          and verdict(dict(b, lp_agree_all=False)) == 'ILL-DEFINED' and verdict(dict(b, sep_all=False)) == 'NULL-LIKE'
                          and verdict(dict(b, kmin_all=0)) == 'POS-CURVED' and verdict(b) == 'LOCAL-COUNT'
                          and verdict(dict(b, formula_all=False)) == 'MIXED-NONLOCAL'
                          and verdict(dict(b, neg_from7=False)) == 'UNCLASSIFIED')
    return res
def _run(V):
    guard(PREREG, HERE)
    sizes = [] if V.get('empty') else NS
    rows = []; seps = {}
    for n in sizes:
        s = census(n, V)
        if n in NULL_NS: seps[n] = separation(s, V)
        s.pop('_vals'); s.pop('_adj'); rows.append(s)
    t = dict(planted_ok=all(_suite(V).values()), n_sizes=len(rows),
             lp_agree_all=all(r['lp_agree'] for r in rows) if rows else False,
             conv_half_all=all(r.get('conv_half_ok', True) for r in rows) if rows else False,
             sep_all=all(x['ok'] for n in seps for x in seps[n]) if rows else False,
             kmin_all=min((r['kmin'] for r in rows), default=F(0)),
             formula_all=all(r['formula_ok'] for r in rows) if rows else False,
             neg_from7=all((r['frac_neg'] > 0) == (r['n'] >= 7) for r in rows) if rows else False)
    t['verdict'] = verdict(t); t['rows'] = rows; t['separation'] = seps
    return json.loads(json.dumps(t, default=lambda v: (str(v) if isinstance(v, F) else v)))
VARIANTS = ['open_nbhd', 'dist_cap2', 'no_shared', 'p_count_edges', 'empty']
def planted():
    guard(PREREG, HERE)
    r = _suite({}); r['ALL_OK'] = all(r.values()); return r
def broken():
    guard(PREREG, HERE)
    out = {}
    for b in VARIANTS:
        if b == 'empty': out[b] = _run({b: True})['verdict']; continue
        r = _suite({b: True}); out[b] = sorted(k for k, v in r.items() if not v)
    out['ALL_REJECTED'] = all(out[b] for b in VARIANTS if b != 'empty') and out['empty'] == 'ILL-DEFINED'
    return out
def live():
    guard(PREREG, HERE)
    return _run({})
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode not in ('planted', 'broken', 'live'): sys.exit('usage: planted|broken|live')
    guard(PREREG, HERE)
    r = {'planted': planted, 'broken': broken, 'live': live}[mode]()
    (OUT / f'hgdim1_{mode}.json').write_text(json.dumps(r, indent=1, default=str)); print(json.dumps(r, default=str)[:4000])
