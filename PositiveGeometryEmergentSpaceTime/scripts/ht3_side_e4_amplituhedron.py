"""H-T3 (d) side test: Lam's E_4 (top network, 6 edges) pushed through Y = C.Z into the m=2 amplituhedron A_{8,3,2}.
Prereg: prereg/H-T3-ising-OG-2026-10-11.md (d). Exact rationals / sympy."""
import sympy as sp, itertools, random
from fractions import Fraction as Fr
exec(open("scripts/ht2_cells.py").read().split("families = {")[0])  # nc_partitions, dual, necklace, affine_perm, crossings
random.seed(4)
n, N, k, m = 4, 8, 3, 2
nodes = [1, 2, 3, 4, 'c']; E = [(1, 2), (2, 3), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')]
t = sp.Symbol('t', positive=True)
def groves_sym(edges, cond):
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
            w = sp.Integer(1)
            for e in sub: w *= cond[e]
            L[sig] = sp.expand(L.get(sig, 0) + w)
    return L
def deltas_sym(L):
    out = {}
    for I in itertools.combinations(range(1, N+1), n-1):
        comp = set(range(1, N+1)) - set(I); tot = sp.Integer(0)
        for sig, val in L.items():
            blocks = [{2*b-1 for b in B} for B in sig] + [{2*b for b in B} for B in dual(sig, n)]
            if all(len(B & comp) == 1 for B in blocks): tot += val
        out[I] = sp.expand(tot)
    return out
def C_from_plucker(D):
    I0 = min((I for I in D if D[I] != 0)); C = sp.zeros(k, N)
    for r, i in enumerate(I0): C[r, i-1] = 1
    for j in range(1, N+1):
        if j in I0: continue
        for r in range(k):
            S = tuple(sorted(set(I0) - {I0[r]} | {j}))
            T = sp.zeros(k, N)
            for rr, ii in enumerate(I0): T[rr, ii-1] = 1
            T[r, j-1] = 1; T[r, I0[r]-1] = 0
            sgn = T[:, [s-1 for s in S]].det()
            C[r, j-1] = sp.nsimplify(D[S] * sgn / D[I0])
    return C
Z = sp.Matrix([[sp.Integer(i)**p for p in range(k+m)] for i in range(1, N+1)])  # moment curve, positive
def brackets(C):
    Y = C * Z
    return {(i, j): (Y.col_join(Z[i-1, :]).col_join(Z[j-1, :])).det() for i in range(1, N+1) for j in range(i+1, N+1)}
def report(C, label):
    B = brackets(C)
    adj = [B[(i, i+1)] for i in range(1, N)] + [B[(1, N)]]
    seq = [B[(1, j)] for j in range(2, N+1)]
    flips = sum(1 for a, b in zip([s for s in seq if s != 0], [s for s in seq if s != 0][1:]) if a*b < 0)
    print(f"{label}: <Y i i+1> signs {[int(sp.sign(x)) for x in adj[:-1]]}, <Y 1 8> sign {int(sp.sign(adj[-1]))}, flips of <Y 1 j>: {flips}; zero adjacent brackets: {[i for i,x in enumerate(adj[:-1],1) if x == 0] + (['(8,1)'] if adj[-1]==0 else [])}")
    return adj
# 1. generic point, inside A?, full-dimensional?
cond = [sp.Rational(random.randint(1, 9), random.randint(1, 5)) for _ in E]
D = deltas_sym(groves_sym(E, cond)); C = C_from_plucker(D)
assert all(sp.simplify(C[:, [i-1 for i in I]].det() * D[min(J for J in D if D[J] != 0)] - D[I]) == 0 for I in D), "reconstruction"
report(C, "generic E4 point")
# Jacobian rank of gauge-fixed Y wrt conductances (numeric)
xs = sp.symbols('x0:6', positive=True)
Dsym = deltas_sym(groves_sym(E, list(xs)))
def Yfix(vals):
    Dv = {I: v.subs(dict(zip(xs, vals))) for I, v in Dsym.items()}
    Y = C_from_plucker(Dv) * Z; Y = Y[:, :3].inv() * Y
    return [Y[r, c] for r in range(3) for c in (3, 4)]
vals = [float(c) for c in cond]; base = sp.Matrix(Yfix([sp.Rational(v).limit_denominator(1000) for v in vals]))
h = sp.Rational(1, 10**6); Jrows = []
for e in range(6):
    vp = [sp.Rational(v).limit_denominator(1000) for v in vals]; vp[e] += h
    Jrows.append(list((sp.Matrix(Yfix(vp)) - base) / h))
print("Jacobian rank of Y (gauge-fixed) wrt 6 conductances:", sp.Matrix(Jrows).evalf(20).rank(iszerofunc=lambda z: abs(z) < 1e-8))
# 2. facets: single conductance -> 0 or oo
for e in range(6):
    for lim in ("0", "oo"):
        cs = list(cond); cs[e] = t
        Dt = deltas_sym(groves_sym(E, cs))
        polys = {I: sp.Poly(v, t) for I, v in Dt.items()}
        if lim == "0":
            d0 = min(min(m_[0] for m_ in p.monoms()) for p in polys.values() if not p.is_zero)
            Dl = {I: (p.as_expr().coeff(t, d0) if not p.is_zero else 0) for I, p in polys.items()}
        else:
            d0 = max(p.degree() for p in polys.values() if not p.is_zero)
            Dl = {I: (p.as_expr().coeff(t, d0) if not p.is_zero else 0) for I, p in polys.items()}
        Dl = {I: sp.nsimplify(v) for I, v in Dl.items()}
        neck = necklace({I: v for I, v in Dl.items()}, N, k); f = affine_perm(neck, N)
        g = {i: f[i] + 1 for i in f}; tau = {i: (g[i]-1) % N + 1 for i in g}
        c_ = crossings(tau, N) if all(tau[tau[i]] == i and tau[i] != i for i in tau) else None
        if c_ == 5:
            adj = report(C_from_plucker(Dl), f"  facet: edge {E[e]} -> {lim} (c=5)")
        else:
            print(f"  edge {E[e]} -> {lim}: limit stratum c={c_} (not a facet)")

# 3. structural reason for the rank deficit: E4 row spaces lie in a fixed 6-dim W and are isotropic for a
#    skew form on W (E4 is open in a Lagrangian Grassmannian LG(3,6), dim 6). A projection from a line kills
#    the alpha (x) alpha direction of Sym^2 -> rank 5 for every Z.
import numpy as np
rng = np.random.default_rng(2)
def Cnum(vals):
    Dv = deltas_sym(groves_sym(E, [sp.Rational(int(a*1000), 1000) for a in vals])); return np.array(C_from_plucker(Dv).tolist(), dtype=float)
Cs = [Cnum(rng.uniform(0.5, 3, 6)) for _ in range(8)]
S = np.vstack(Cs); U, sv, Vt = np.linalg.svd(S); W = Vt[:6]          # basis of the common row space
print("common row space dim:", int(np.sum(sv > 1e-9)), "; null vectors span alt-type vectors:", np.round(Vt[6:] , 4).tolist())
# solve for skew form w (6x6 on W) with (C_W) w (C_W)^T = 0 for all samples
idx = [(a, b) for a in range(6) for b in range(a+1, 6)]
rows = []
for C in Cs:
    CW = C @ W.T
    for r in range(3):
        for s in range(r+1, 3):
            rows.append([CW[r, a]*CW[s, b] - CW[r, b]*CW[s, a] for a, b in idx])
sA = np.linalg.svd(np.array(rows), compute_uv=False)
print("isotropic skew forms on W (null dim of 15-unknown system):", int(np.sum(sA < 1e-9 * sA[0])), "; smallest sv ratios:", sA[-2:] / sA[0])
