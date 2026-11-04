"""H-T5 (a,b,d): Ising-network cells vs the ABJM orthogonal momentum amplituhedron (HKWZ 2111.03037).
Prereg: prereg/H-T5-ising-tiling-2026-10-12.md. numpy/scipy, double precision."""
import numpy as np, itertools, random, json, fractions

def least_squares(f, x0, max_nfev=400, **kw):
    """Minimal Levenberg-Marquardt (numpy only; scipy unavailable on the box)."""
    x = np.array(x0, float); lam = 1e-3; r = f(x); c = r @ r
    for _ in range(max_nfev):
        h = 1e-7; J = np.array([(f(x + h*np.eye(len(x))[a]) - r)/h for a in range(len(x))]).T
        A = J.T @ J; g = J.T @ r
        while True:
            try: dx = np.linalg.solve(A + lam*np.diag(np.diag(A) + 1e-12), -g)
            except np.linalg.LinAlgError: dx = -g
            xn = x + dx; rn = f(xn); cn = rn @ rn
            if np.isfinite(cn) and cn < c: x, r, c = xn, rn, cn; lam = max(lam/3, 1e-12); break
            lam *= 4
            if lam > 1e12: break
        if lam > 1e12 or c < 1e-26: break
    class R: pass
    out = R(); out.x = x; out.fun = r; return out
_g = {}; exec(open("scripts/ht3_ising_cells.py").read().split("\nfamilies = {")[0], _g)
rng = np.random.default_rng(12); random.seed(12)

class Net:
    def __init__(s, n, edges):
        s.n = n; s.edges = edges
        nodes = sorted({v for e in edges for v in e} | set(range(1, n+1)), key=str)
        s.nodes = nodes; s.subs = []
        for mask in range(1 << len(edges)):
            deg = {v: 0 for v in nodes}
            for i, (a, b) in enumerate(edges):
                if mask >> i & 1: deg[a] += 1; deg[b] += 1
            odd = [v for v in nodes if deg[v] % 2]
            if not odd: s.subs.append((mask, None))
            elif len(odd) == 2 and all(isinstance(v, int) for v in odd): s.subs.append((mask, tuple(sorted(odd))))
    def corr(s, t):                      # t = tanh J (array)
        num = {}; Z = 0.0
        for mask, key in s.subs:
            w = 1.0
            for i in range(len(s.edges)):
                if mask >> i & 1: w *= t[i]
            if key is None: Z += w
            else: num[key] = num.get(key, 0.0) + w
        return {k: v/Z for k, v in num.items()}
    def C(s, t):
        n = s.n; m = s.corr(t); M = np.zeros((n, 2*n))
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i == j: M[i-1, 2*i-2] = M[i-1, 2*i-1] = 1
                else:
                    v = (-1)**(i + j + (1 if i < j else 0)) * m.get((min(i, j), max(i, j)), 0.0)
                    M[i-1, 2*j-2] = v; M[i-1, 2*j-1] = -v
        return M
    def tau(s):
        x = [fractions.Fraction(random.randint(2, 8), 10) for _ in s.edges]
        D = _g["plucker"](_g["gp_matrix"](s.n, _g["correlations"](s.n, s.nodes, s.edges, x)), s.n, 2*s.n)
        f = _g["affine_perm"](_g["necklace"](D, 2*s.n, s.n), 2*s.n); N = 2*s.n
        return tuple((f[i]-1) % N + 1 for i in range(1, N+1))

def Lam(k): x = np.arange(1, 2*k+1, dtype=float); return np.vander(x, k+2, increasing=True)
def perp(Y): return np.linalg.svd(Y)[2][Y.shape[0]:].T
def contains(net, Y, L, starts=20, want_all=False):
    P = perp(Y); sols = []
    f = lambda y: (net.C(np.tanh(np.exp(y))) @ L @ P).ravel()
    for _ in range(starts):
        r = least_squares(f, rng.uniform(-2.5, 2.0, len(net.edges)), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=200)
        J = np.exp(r.x)
        if np.linalg.norm(r.fun) < 1e-10 and np.all((J > 1e-4) & (J < 20)):
            if not want_all: return True, [J]
            if not any(np.linalg.norm(np.log(J) - np.log(q)) < 1e-5 for q in sols): sols.append(J)
    return (len(sols) > 0), sols
def bracket(Y, L, j, l): return np.linalg.det(np.vstack([Y, L[j-1], L[l-1]]))
def crossings(tau):
    N = len(tau); ch = [(i, tau[i-1]) for i in range(1, N+1) if i < tau[i-1]]
    return sum(1 for (a, b), (c, d) in itertools.combinations(ch, 2) if a < c < b < d or c < a < d < b)
out = {}
# ---------- (a) n = 6 ----------
k = 3; L = Lam(k)
Ynet = Net(3, [(1, 'c'), (2, 'c'), (3, 'c')]); Dnet = Net(3, [(1, 2), (1, 3), (2, 3)])
print("Y tau", Ynet.tau(), "Delta tau", Dnet.tau())
signs_ok = inj_ok = delta_ok = 0; S = 40
for _ in range(S):
    J = np.exp(rng.uniform(-1.5, 1.0, 3)); Y = Ynet.C(np.tanh(J)) @ L
    adj = [bracket(Y, L, i, i+1) for i in range(1, 6)]; last = bracket(Y, L, 6, 1)
    seq = [bracket(Y, L, 1, j) for j in range(2, 7)]
    flips = sum(1 for a, b in zip(seq, seq[1:]) if a*b < 0)
    sgn = np.sign(adj[0]); signs_ok += all(np.sign(a) == sgn for a in adj) and flips == 3
    _, sols = contains(Ynet, Y, L, starts=30, want_all=True); inj_ok += (len(sols) == 1)
    delta_ok += contains(Dnet, Y, L)[0]
print(f"(a) n=6: sign pattern+3 flips {signs_ok}/{S}; unique positive preimage {inj_ok}/{S}; Delta chart contains {delta_ok}/{S}; last-bracket sign example {np.sign(last)} vs adj {sgn}")
out["a"] = dict(signs=signs_ok, injective=inj_ok, delta=delta_ok, S=S)
# ---------- (b) n = 8 ----------
k = 4; L = Lam(k)
tops = {"N1": [(1, 2), (2, 3), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')],
        "N2": [(1, 'd'), (2, 'd'), ('d', 'c'), ('c', 3), ('c', 4), (2, 3)],
        "N3": [(1, 'd'), (2, 'd'), (2, 3), ('d', 3), ('d', 4), (3, 4)]}
allm = []
def matchings(rest):
    if not rest: yield []; return
    a = rest[0]
    for b in rest[1:]:
        for m in matchings([x for x in rest if x not in (a, b)]): yield [(a, b)] + m
for m in matchings(list(range(1, 9))):
    tau = [0]*8
    for a, b in m: tau[a-1] = b; tau[b-1] = a
    if crossings(tuple(tau)) == 5: allm.append(tuple(tau))
print("5-crossing matchings of [8]:", len(allm))
cells = {}       # tau -> (net, provenance list)
for G, E in tops.items():
    for i, e in enumerate(E):
        for lim in ("0", "inf"):
            if lim == "0": E2 = [x for j, x in enumerate(E) if j != i]
            else:
                a, b = e
                if isinstance(a, int) and isinstance(b, int): continue
                keep, gone = (a, b) if isinstance(a, int) else ((b, a) if isinstance(b, int) else (a, b))
                E2 = [tuple(keep if v == gone else v for v in x) for j, x in enumerate(E) if j != i]
                if len(set(tuple(sorted(map(str, x))) for x in E2)) < len(E2): continue
            net = Net(4, E2); tau = net.tau()
            if crossings(tau) != 5: continue
            cells.setdefault(tau, [net, []])[1].append((G, e, lim))
print("5-dim cells realised:", len(cells), "of", len(allm))
taus = sorted(cells)
for t in taus: print("  ", t, cells[t][1])
# Jacobian rank of each cell's Y map (gauge-fixed)
def ymap(net, logJ):
    Y = net.C(np.tanh(np.exp(logJ))) @ L; Y = np.linalg.solve(Y[:, :4], Y); return Y[:, 4:].ravel()
for t in taus:
    x0 = rng.uniform(-1, 1, 5); h = 1e-6
    Jm = np.array([(ymap(cells[t][0], x0 + h*np.eye(5)[a]) - ymap(cells[t][0], x0 - h*np.eye(5)[a]))/(2*h) for a in range(5)])
    sv = np.linalg.svd(Jm, compute_uv=False); print("   rank", t, int(np.sum(sv > 1e-7*sv[0])))
SAMPLE_Y = []; top = Net(4, tops["N1"]); NS = 200; memb = np.zeros((NS, len(taus)), dtype=int)
for s in range(NS):
    Y = top.C(np.tanh(np.exp(rng.uniform(-1.5, 1.2, 6)))) @ L
    SAMPLE_Y.append(Y) if 'SAMPLE_Y' in globals() else None
    for c, t in enumerate(taus): memb[s, c] = contains(cells[t][0], Y, L)[0]
print("cells containing each sample: histogram", np.bincount(memb.sum(1)))
import collections
print("membership patterns (prereg run):", collections.Counter(map(tuple, memb.tolist())))
# Post-hoc diagnostic (NOT prereg verdict): re-test zero entries with 100 starts, wider J box
memb2 = memb.copy()
def contains_wide(net, Y):
    P = perp(Y); f = lambda y: (net.C(np.tanh(np.exp(y))) @ L @ P).ravel()
    for _ in range(100):
        r = least_squares(f, rng.uniform(-6, 4, len(net.edges)), max_nfev=300)
        if np.linalg.norm(r.fun) < 1e-10 and np.all(np.isfinite(r.x)) and np.all(np.abs(r.x) < 12): return 1
    return 0
SAMPLE_Y = []
for s_ in range(NS):
    for c, t in enumerate(taus):
        if memb2[s_, c] == 0 and s_ < len(SAMPLE_Y): memb2[s_, c] = contains_wide(cells[t][0], SAMPLE_Y[s_])
print("post-hoc histogram:", np.bincount(memb2.sum(1)), collections.Counter(map(tuple, memb2.tolist())))
tilings2 = [(taus[a], taus[b]) for a, b in itertools.combinations(range(len(taus)), 2) if np.all(memb2[:, a] + memb2[:, b] == 1)]
print("post-hoc tiling pairs:", tilings2)
tilings = []
for a, b in itertools.combinations(range(len(taus)), 2):
    if np.all(memb[:, a] + memb[:, b] == 1): tilings.append((taus[a], taus[b]))
print("tiling pairs:", tilings)
s1 = (5, 7, 6, 8, 1, 3, 2, 4); s2 = (4, 6, 7, 1, 8, 2, 3, 5)
print("HW sigma1, sigma2 realised:", s1 in cells, s2 in cells, " HW pair tiles:", (min(s1, s2), max(s1, s2)) in [tuple(sorted(p)) for p in tilings])
# (d) H_KW pairs: same top network, same edge, 0 vs inf
kw = set()
for t in taus:
    for (G, e, lim) in cells[t][1]:
        for t2 in taus:
            if t2 != t and (G, e, "inf" if lim == "0" else "0") in cells[t2][1]: kw.add(tuple(sorted((t, t2))))
tl = set(tuple(sorted(p)) for p in tilings)
print("H_KW pairs:", len(kw), "; of which tile:", len(kw & tl), "; tiling pairs that are H_KW:", len(tl & kw), "/", len(tl))
json.dump(dict(cells={str(t): cells[t][1] for t in taus}, tilings=[list(map(list, p)) for p in tilings],
               kw=[list(map(list, p)) for p in kw], hist=np.bincount(memb.sum(1)).tolist(), memb=memb.tolist(), memb_posthoc=memb2.tolist(), a=out["a"]),
          open("scripts/ht5_tiling.json", "w"), indent=1, default=str)
