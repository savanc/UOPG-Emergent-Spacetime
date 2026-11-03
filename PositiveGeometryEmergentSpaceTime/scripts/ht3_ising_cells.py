"""H-T3 (a): Galashin-Pylyavskyy embedding of planar Ising networks (n = 2, 3, 4), exact checks.
Prereg: prereg/H-T3-ising-OG-2026-10-11.md. Exact rationals (x_e = tanh J_e); floats only for Jacobian rank."""
from fractions import Fraction as Fr
import itertools, random, json
import numpy as np
exec(open("scripts/ht2_cells.py").read().split("families = {")[0])   # reuse necklace / affine_perm / crossings / groves
random.seed(311)

def correlations(n, nodes, edges, x):
    num = {(i, j): Fr(0) for i in range(1, n+1) for j in range(i+1, n+1)}; Z = Fr(0)
    for r in range(len(edges)+1):
        for sub in itertools.combinations(range(len(edges)), r):
            deg = {v: 0 for v in nodes}; w = Fr(1)
            for e in sub:
                u, v = edges[e]; deg[u] += 1; deg[v] += 1; w *= x[e]
            odd = [v for v in nodes if deg[v] % 2]
            if all(isinstance(v, int) for v in odd): odd = sorted(odd)
            if not odd: Z += w
            elif len(odd) == 2 and all(isinstance(v, int) for v in odd): num[tuple(odd)] += w
    return {k: v / Z for k, v in num.items()}
def gp_matrix(n, m):
    M = [[Fr(0)]*(2*n) for _ in range(n)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i == j: M[i-1][2*i-2] = M[i-1][2*i-1] = Fr(1)
            else:
                mij = m[(min(i, j), max(i, j))]
                val = (-1)**(i + j + (1 if i < j else 0)) * mij
                M[i-1][2*j-2] = val; M[i-1][2*j-1] = -val
    return M
def det(A):
    A = [row[:] for row in A]; n = len(A); d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c+1, n):
            f = A[r][c] / A[c][c]
            for k in range(c, n): A[r][k] -= f * A[c][k]
    return d
def plucker(M, k, N):
    return {I: det([[row[i-1] for i in I] for row in M]) for I in itertools.combinations(range(1, N+1), k)}
def jac_rank(n, nodes, edges, x):
    keys = [(i, j) for i in range(1, n+1) for j in range(i+1, n+1)]
    def vec(xs): 
        c = correlations(n, nodes, edges, [Fr(v).limit_denominator(10**12) for v in xs]); return np.array([float(c[k]) for k in keys])
    base = [float(v) for v in x]
    if not edges: return 0
    J = []
    for e in range(len(edges)):
        h = 1e-6; xp = list(base); xm = list(base); xp[e] += h; xm[e] -= h
        J.append((vec(xp) - vec(xm)) / (2*h))
    s = np.linalg.svd(np.array(J), compute_uv=False)
    return int(np.sum(s > 1e-6 * max(1.0, s.max())))

def lam_tau(n, nodes, edges):
    """H-T2 (electrical) medial pairing of the same graph, via Lam's embedding."""
    cond = [Fr(random.randint(1, 9), random.randint(1, 5)) for _ in edges]
    L = groves(n, nodes, edges, cond)
    if not L: return None
    D = deltas(n, {s: L.get(s, Fr(0)) for s in nc_partitions(n)})
    f = affine_perm(necklace(D, 2*n, n-1), 2*n)
    return [f[i] % (2*n) + 1 for i in range(1, 2*n+1)]

families = {
    2: ([1, 2, 'c'], [(1, 2), (1, 'c'), (2, 'c')]),
    3: ([1, 2, 3, 'c'], [(1, 2), (2, 3), (3, 1), (1, 'c'), (2, 'c'), (3, 'c')]),
    4: ([1, 2, 3, 4, 'c'], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')]),
}
for n, (nodes, sup) in families.items():
    N = 2*n; stats = dict(subgraphs=0, og_ok=0, nonneg_ok=0, involution_ok=0, rank_ok=0, lam_match=0, lam_defined=0)
    cells = set(); fails = []
    for r in range(len(sup)+1):
        for sub in itertools.combinations(range(len(sup)), r):
            edges = [sup[e] for e in sub]; stats["subgraphs"] += 1
            x = [Fr(random.randint(1, 9), 10) for _ in edges]          # x = tanh J in (0,1)
            m = correlations(n, nodes, edges, x)
            D = plucker(gp_matrix(n, m), n, N)
            og = all(D[I] == D[tuple(sorted(set(range(1, N+1)) - set(I)))] for I in D)
            nn = all(v >= 0 for v in D.values())
            f = affine_perm(necklace(D, N, n), N)
            tau = [(f[i]-1) % N + 1 for i in range(1, N+1)]
            inv = all(tau[tau[i-1]-1] == i and tau[i-1] != i for i in range(1, N+1))
            tdict = {i: tau[i-1] for i in range(1, N+1)}
            xing = crossings(tdict, N) if inv else None
            rk = jac_rank(n, nodes, edges, x)
            lt = lam_tau(n, nodes, edges)
            stats["og_ok"] += og; stats["nonneg_ok"] += nn; stats["involution_ok"] += inv; stats["rank_ok"] += (rk == xing)
            if lt is not None: stats["lam_defined"] += 1; stats["lam_match"] += (lt == tau)
            cells.add(tuple(tau))
            if not (og and nn and inv and rk == xing): fails.append((edges, tau, xing, rk))
    print(f"n={n}: {stats}; distinct cells {len(cells)}; fails {len(fails)}")
    for fl in fails[:4]: print("   FAIL", fl)
# n = 2 one-edge example (Lean target): sigma = tanh J
m = {(1, 2): Fr(1, 3)}; D = plucker(gp_matrix(2, m), 2, 4)
print("n=2 one edge, sigma=1/3: M~ =", [[str(v) for v in row] for row in gp_matrix(2, m)], "minors", {I: str(v) for I, v in D.items()})
