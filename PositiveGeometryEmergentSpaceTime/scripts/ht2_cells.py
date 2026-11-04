"""H-T2 (a), (d): positroid cells of Lam's embedding for families of circular planar networks (n = 2, 3, 4).
Prereg: prereg/H-T2-positroid-cells-2026-10-11.md. Exact rationals for Pluecker data; floats only for Jacobian rank."""
from fractions import Fraction as Fr
import itertools, random, json
import numpy as np
random.seed(2026)

def set_partitions(s):
    s = list(s)
    if not s: yield []; return
    first, rest = s[0], s[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i+1:]
        yield [[first]] + p
def noncrossing(p):
    for A, B in itertools.permutations(p, 2):
        for a1, a2 in itertools.combinations(sorted(A), 2):
            if any(a1 < b < a2 for b in B) and any(b < a1 or b > a2 for b in B): return False
    return True
def nc_partitions(n): return [tuple(sorted(tuple(sorted(b)) for b in p)) for p in set_partitions(range(1, n+1)) if noncrossing(p)]
def dual(sig, n):
    """Kreweras dual on tildes 1..n (tilde i sits between bar i and bar i+1): i ~ j iff no block separates them."""
    def sep(i, j, B):  # positions 2i, 2j on circle of 2n; bar b at 2b-1
        lo, hi = sorted((2*i, 2*j)); inside = [b for b in B if lo < 2*b-1 < hi]
        return 0 < len(inside) < len(B)
    parent = list(range(n+1))
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    for i, j in itertools.combinations(range(1, n+1), 2):
        if not any(sep(i, j, B) for B in sig): parent[find(i)] = find(j)
    blocks = {}
    for i in range(1, n+1): blocks.setdefault(find(i), []).append(i)
    return [tuple(b) for b in blocks.values()]
def deltas(n, L):
    N = 2*n; out = {}
    for I in itertools.combinations(range(1, N+1), n-1):
        comp = set(range(1, N+1)) - set(I); tot = Fr(0)
        for sig, val in L.items():
            if val == 0: continue
            blocks = [{2*b-1 for b in B} for B in sig] + [{2*b for b in B} for B in dual(sig, n)]
            if all(len(B & comp) == 1 for B in blocks): tot += val
        out[I] = tot
    return out
def groves(n, nodes, edges, cond):
    """L_sigma: forests in which every component contains a terminal (terminals 1..n), grouped by boundary partition."""
    L = {}
    for r in range(len(edges)+1):
        for sub in itertools.combinations(range(len(edges)), r):
            parent = {v: v for v in nodes}
            def find(x):
                while parent[x] != x: x = parent[x]
                return x
            ok = True
            for e in sub:
                u, v = edges[e]; ru, rv = find(u), find(v)
                if ru == rv: ok = False; break
                parent[ru] = rv
            if not ok: continue
            comps = {}
            for v in nodes: comps.setdefault(find(v), []).append(v)
            if any(not any(isinstance(x, int) for x in c) for c in comps.values()): continue
            sig = tuple(sorted(tuple(sorted(x for x in c if isinstance(x, int))) for c in comps.values()))
            w = Fr(1)
            for e in sub: w *= cond[e]
            L[sig] = L.get(sig, Fr(0)) + w
    return L
def necklace(D, N, k):
    nz = [I for I, v in D.items() if v != 0]
    if not nz: return None
    neck = []
    for a in range(1, N+1):
        neck.append(min(nz, key=lambda I: sorted((i - a) % N for i in I)))
    return neck
def affine_perm(neck, N):
    f = {}
    for a in range(1, N+1):
        Ia, Ib = set(neck[a-1]), set(neck[a % N])
        if a not in Ia: f[a] = a
        else:
            new = Ib - (Ia - {a})
            j = a if not new else new.pop()
            f[a] = a + N if j == a else (j if j > a else j + N)
    return f
def length(f, N):
    F = lambda j: f[(j-1) % N + 1] + N*((j-1)//N)
    return sum(1 for i in range(1, N+1) for j in range(i+1, i+N) if F(i) > F(j))
def crossings(tau, N):
    chords = {tuple(sorted((i, tau[i]))) for i in tau}
    return sum(1 for (a, b), (c, d) in itertools.combinations(chords, 2) if (a < c < b < d) or (c < a < d < b))
def jac_rank(n, nodes, edges, sigmas, cond):
    base = [float(c) for c in cond]
    def vec(cs):
        L = groves(n, nodes, edges, [Fr(c).limit_denominator(10**12) for c in cs])
        ref = L.get(tuple((i,) for i in range(1, n+1)), Fr(0))
        return np.array([float(L.get(s, 0) / ref) for s in sigmas]) if ref else None
    v0 = vec(base)
    if v0 is None: return None
    J = []
    for e in range(len(edges)):
        h = 1e-6 * base[e]; cp = list(base); cm = list(base); cp[e] += h; cm[e] -= h
        J.append((vec(cp) - vec(cm)) / (2*h))
    J = np.array(J)
    if J.size == 0: return 0
    s = np.linalg.svd(J, compute_uv=False)
    return int(np.sum(s > 1e-6 * max(1.0, s.max())))
def fusions_trace(n, edges):
    """Fusions Def. 2 on the trace chain on terminals: classes = terminals in the same connected component."""
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x: x = parent[x]
        return x
    for u, v in edges: parent[find(u)] = find(v)
    sig = {}
    for a in range(1, n+1):
        cls = [b for b in range(1, n+1) if find(b) == find(a)]
        others = [(b - a) % n for b in cls if b != a]
        sig[a] = a + (max(others) if others else n)
    return sig
def term_projection_perm(D, n):
    sub = {tuple((i+1)//2 for i in I): v for I, v in D.items() if all(i % 2 == 1 for i in I)}
    if all(v == 0 for v in sub.values()): return None
    return affine_perm(necklace(sub, n, n-1), n)

def run(n, nodes, sup_edges):
    sigmas = nc_partitions(n); N = 2*n; k = n-1; rows = []; fails = []
    for r in range(len(sup_edges)+1):
        for sub in itertools.combinations(range(len(sup_edges)), r):
            edges = [sup_edges[e] for e in sub]
            cond = [Fr(random.randint(1, 9), random.randint(1, 5)) for _ in edges]
            L = groves(n, nodes, edges, cond)
            if not L: rows.append({"edges": edges, "status": "no grove (interior node isolated)"}); continue
            D = deltas(n, {s: L.get(s, Fr(0)) for s in sigmas})
            neck = necklace(D, N, k); f = affine_perm(neck, N)
            g = {i: f[i] + 1 for i in f}; tau = {i: (g[i]-1) % N + 1 for i in g}
            inv = all(tau[tau[i]] == i and tau[i] != i for i in tau)
            ftau = {i: (tau[i] if i < tau[i] else tau[i] + N) - 1 for i in tau} if inv else None
            c = crossings(tau, N) if inv else None
            dimP = k*(N-k) - length(f, N)
            rk = jac_rank(n, nodes, edges, sigmas, cond)
            fus = fusions_trace(n, edges); proj = term_projection_perm(D, n)
            row = {"edges": edges, "f": [f[i] for i in range(1, N+1)], "tau_involution": inv, "f_eq_ftau": ftau == f,
                   "c": c, "dim_positroid": dimP, "jac_rank": rk, "dim_ok": inv and dimP == n-1+2*c, "rank_ok": rk == c,
                   "fusions_trace": [fus[a] for a in range(1, n+1)], "terminal_proj": None if proj is None else [proj[a] for a in range(1, n+1)]}
            row["fusions_eq_proj"] = row["terminal_proj"] == row["fusions_trace"]
            rows.append(row)
            if not (inv and row["f_eq_ftau"] and row["dim_ok"] and row["rank_ok"]): fails.append(row)
    return rows, fails

families = {
    2: ([1, 2, 'c'], [(1, 2), (1, 'c'), (2, 'c')]),
    3: ([1, 2, 3, 'c'], [(1, 2), (2, 3), (3, 1), (1, 'c'), (2, 'c'), (3, 'c')]),
    4: ([1, 2, 3, 4, 'c'], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')]),
}
summary = {}
for n, (nodes, sup) in families.items():
    rows, fails = run(n, nodes, sup)
    good = [r for r in rows if "f" in r]
    cells = sorted({tuple(r["f"]) for r in good})
    fus_conn = [r for r in good if r["terminal_proj"] is not None]
    summary[n] = {"subgraphs": len(rows), "with_point": len(good), "fails": len(fails), "distinct_cells": len(cells),
                  "c_values": sorted({r["c"] for r in good}),
                  "fusions_eq_proj_when_proj_defined": all(r["fusions_eq_proj"] for r in fus_conn),
                  "proj_defined": len(fus_conn),
                  "fusions_eq_lam_f": sum(1 for r in good if r["fusions_trace"] == r["f"][:n])}
    print(f"n={n}: {summary[n]}")
    for r in fails[:5]: print("   FAIL", r)
    top = [r for r in good if r["c"] == max(summary[n]["c_values"])][0]
    print(f"   top example: edges={top['edges']} f={top['f']} c={top['c']} dimPositroid={top['dim_positroid']} Fusions(trace)={top['fusions_trace']} proj={top['terminal_proj']}")
    json.dump(rows, open(f"scripts/ht2_cells_n{n}.json", "w"), default=str)
# n = 3 facet network: terminal 1 joined to 2 and 3
nodes, edges = [1, 2, 3], [(1, 2), (1, 3)]
L = groves(3, nodes, edges, [Fr(2), Fr(3)])
D = deltas(3, {s: L.get(s, Fr(0)) for s in nc_partitions(3)})
neck = necklace(D, 6, 2); f = affine_perm(neck, 6)
print("facet network 1-2, 1-3 (b=2, c=3): Deltas", {I: str(v) for I, v in D.items()}, "\n  necklace", neck, "f", [f[i] for i in range(1, 7)])
# (d) Fusions (trace chain) vs Lam cell: is Fusions a coarsening?
for n in (2, 3, 4):
    r = [x for x in json.load(open(f"scripts/ht2_cells_n{n}.json")) if "f" in x]
    m = {}
    for x in r: m.setdefault(tuple(x["f"]), set()).add(tuple(x["fusions_trace"]))
    con = [x for x in r if x["terminal_proj"] is not None]
    print(f"(d) n={n}: Lam cells {len(m)} -> Fusions labels {len({tuple(x['fusions_trace']) for x in r})}; "
          f"max labels per cell {max(len(v) for v in m.values())} (1 = Fusions is a function of the cell); "
          f"connected: {len({tuple(x['f']) for x in con})} cells -> {len({tuple(x['fusions_trace']) for x in con})} label")
