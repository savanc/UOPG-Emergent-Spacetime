"""HG-DIM-2 locked checker (CPU only; exact integer transport costs via assignment; HiGHS LP as cross-check and for idleness 1/2, 0).
Question: on the permutohedron graph P_n (Cayley graph of S_n with adjacent transpositions s_1..s_{n-1}, D = n-1), does the
Ollivier curvature (idleness 1/(D+1), uniform on closed neighbourhoods) equal Forman curvature / (D+1) edge by edge
(the HG-DIM-1 "Ollivier-Forman link"), or do the hexagonal 2-faces break it? Predicted (prereg): link HOLDS,
kappa = (2-2h)/n, kappa_F = 2-2h, h = number of hexagonal 2-faces at the edge (1 end generator, 2 interior).
Prereg: prereg/HG-DIM-2-permutohedron-ollivier-curvature-2026-10-31.md. Modes: planted | broken | live (each guarded)."""
import sys, json, itertools, random
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linear_sum_assignment, linprog
HERE = str(Path(__file__).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guard import guard
PREREG = 'prereg/HG-DIM-2-permutohedron-ollivier-curvature-2026-10-31.md'
OUT = Path(__file__).resolve().parent
NS = list(range(3, 9))           # live n = 3..8 (D = 2..7), ALL edges exact
LP_ALL_N = 5                     # LP cross-check on all edges for n <= 5
LP_SAMPLE, LP_SEED = 100, 20261031
SYM_ALL_N = 6                    # left-multiplication automorphism checked for all g for n <= 6
TOL = 1e-9

# ---------------- permutohedron ----------------
def perm_graph(n, left=False):
    """Vertices: permutations of range(n) as image tuples. Right Cayley: w ~ w s_i (swap positions i, i+1).
    left=True: s_i w (swap values i, i+1). Returns adj (list of sets), lab {(u,v): i}, verts, idx."""
    Vs = list(itertools.permutations(range(n))); idx = {w: k for k, w in enumerate(Vs)}
    adj = [set() for _ in Vs]; lab = {}
    for k, w in enumerate(Vs):
        for i in range(n - 1):
            if left: v = tuple(i + 1 if a == i else i if a == i + 1 else a for a in w)
            else: v = list(w); v[i], v[i + 1] = v[i + 1], v[i]; v = tuple(v)
            j = idx[v]; adj[k].add(j); lab[(min(k, j), max(k, j))] = i
    return adj, lab, Vs, idx
def act(w, i, left=False):
    if left: return tuple(i + 1 if a == i else i if a == i + 1 else a for a in w)
    v = list(w); v[i], v[i + 1] = v[i + 1], v[i]; return tuple(v)
def perm_faces(n, Vs, idx, left=False):
    """2-faces = cosets w<s_i, s_j> (i < j), as vertex cycles in order (alternate s_i, s_j)."""
    seen = set(); faces = []
    for w in Vs:
        for i in range(n - 1):
            for j in range(i + 1, n - 1):
                cyc = [w]; g = (i, j); t = 0
                while True:
                    nx_ = act(cyc[-1], g[t % 2], left); t += 1
                    if nx_ == w: break
                    cyc.append(nx_)
                key = frozenset(cyc)
                if key in seen: continue
                seen.add(key); faces.append([idx[x] for x in cyc])
    return faces

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
def face_index(faces):
    inc = {}
    for fi, c in enumerate(faces):
        for k in range(len(c)):
            a, b = c[k], c[(k + 1) % len(c)]; inc.setdefault((min(a, b), max(a, b)), []).append(fi)
    return inc
def face_edges(c):
    return {(min(c[k], c[(k + 1) % len(c)]), max(c[k], c[(k + 1) % len(c)])) for k in range(len(c))}
def forman(adj, faces, inc, e, V):
    """De Loera et al. 2510.11894 Def 1.1/1.2: kappa_F(e) = |F_up(e)| + 2 - |E(e)|; E(e) = parallel edges:
    (i) share a vertex with e, no common 2-face; (ii) vertex-disjoint from e, in a common 2-face. Returns (kF, #F_up, hexagons, squares)."""
    u, v = e; Fup = inc.get(e, [])
    par = set()
    for z in (u, v):
        for t in adj[z]:
            f = (min(z, t), max(z, t))
            if f == e: continue
            if not (set(inc.get(f, [])) & set(Fup)): par.add(f)
    nii = 0
    for fi in Fup:
        disj = {f for f in face_edges(faces[fi]) if u not in f and v not in f}
        if V.get('hex_as_square'): nii += 1
        else: par |= disj
    kF = len(Fup) + 2 - len(par) - nii
    sizes = [len(faces[fi]) for fi in Fup]
    return kF, len(Fup), sizes.count(6), sizes.count(4)

# ---------------- planted graphs ----------------
def g_complete(m): return [set(range(m)) - {i} for i in range(m)]
def g_cycle(m): return [{(i - 1) % m, (i + 1) % m} for i in range(m)]
def g_cube(d): return [{i ^ (1 << k) for k in range(d)} for i in range(1 << d)]
def cube_faces(d):
    return [[b, b ^ (1 << i), b ^ (1 << i) ^ (1 << j), b ^ (1 << j)] for b in range(1 << d)
            for i in range(d) for j in range(i + 1, d) if not (b >> i) & 1 and not (b >> j) & 1]
def g_prism(m):
    adj = [set() for _ in range(2 * m)]
    for L in (0, 1):
        for k in range(m):
            a, b = k + m * L, (k + 1) % m + m * L; adj[a].add(b); adj[b].add(a)
    for k in range(m): adj[k].add(k + m); adj[k + m].add(k)
    faces = [list(range(m)), list(range(m, 2 * m))] + [[k, (k + 1) % m, (k + 1) % m + m, k + m] for k in range(m)]
    return adj, faces
def g_tree3(depth=4):
    adj = [set()]; frontier = [0]
    for lev in range(depth):
        nf = []
        for u in frontier:
            for _ in range(3 if u == 0 else 2):
                adj.append(set()); w = len(adj) - 1; adj[u].add(w); adj[w].add(u); nf.append(w)
        frontier = nf
    return adj
def link_gate(adj, faces, V, E=None):
    inc = face_index(faces); D = len(adj[0]); E = E if E is not None else edges_of(adj)
    return all(kappa_assign(adj, *e, V) == F(forman(adj, faces, inc, e, V)[0], D + 1) for e in E)

# ---------------- census and verdict ----------------
def census(n, V):
    adj, lab, Vs, idx = perm_graph(n); D = n - 1; E = edges_of(adj)
    faces = perm_faces(n, Vs, idx); inc = face_index(faces)
    ks = {e: kappa_assign(adj, *e, V) for e in E}
    fm = {e: forman(adj, faces, inc, e, V) for e in E}
    hpred = lambda i: 1 if i in (0, n - 2) else 2   # end generators (s_1, s_{n-1}) in 1 hexagon, interior in 2
    formula_ok = all(ks[e] == F(2 - 2 * fm[e][2], n) for e in E)
    forman_ok = all(fm[e][0] == 2 - 2 * fm[e][2] for e in E)
    link_ok = all(ks[e] == F(fm[e][0], D + 1) for e in E)
    hex_ok = all(fm[e][2] == (hpred(lab[e]) if n >= 3 else 0) and fm[e][3] == n - 2 - fm[e][2] and fm[e][1] == n - 2 for e in E) if n >= 4 else \
        all(fm[e][2] == 1 and fm[e][3] == 0 for e in E)
    gap = max(abs(ks[e] - F(fm[e][0], D + 1)) for e in E)
    per = {}
    for i in range(n - 1):
        Ei = [e for e in E if lab[e] == i]
        per[str(i + 1)] = dict(n_edges=len(Ei), kappa=sorted({str(ks[e]) for e in Ei}), kappaF=sorted({fm[e][0] for e in Ei}),
                               hexagons=sorted({fm[e][2] for e in Ei}), squares=sorted({fm[e][3] for e in Ei}))
    const_per_label = all(len(per[k]['kappa']) == 1 and len(per[k]['kappaF']) == 1 for k in per)
    kmean = sum(ks.values(), F(0)) / len(E); fmean = F(sum(fm[e][0] for e in E), len(E))
    mean_ok = kmean == F(-2 * (n - 3), n * (n - 1)) and fmean == F(-2 * (n - 3), n - 1)
    # LP cross-checks (lazy, idleness 1/2, idleness 0) and Cushing et al. 2310.15953 Thm 1.2 + Ex 1.5 (RACG reduction)
    r = random.Random(LP_SEED + n)
    reps = [(min(idx[tuple(range(n))], idx[act(tuple(range(n)), i)]), max(idx[tuple(range(n))], idx[act(tuple(range(n)), i)])) for i in range(n - 1)]
    sample = E if n <= LP_ALL_N else sorted(set(r.sample(E, min(LP_SAMPLE, len(E))) + reps))
    lp_agree = True; half_ok = True; zero_ok = True; cush_ok = True
    for e in sample:
        h = fm[e][2]; i = lab[e]
        if abs(kappa_lp(adj, *e, None, V) - float(ks[e])) > TOL: lp_agree = False
        k12 = kappa_lp(adj, *e, F(1, 2), V); k0 = kappa_lp(adj, *e, F(0), V)
        if abs(k12 - float(ks[e]) * (D + 1) / (2 * D)) > TOL or abs(k12 - (1 - h) / (n - 1)) > TOL: half_ok = False
        if abs(k0 - (2 - 2 * h) / (n - 1)) > TOL: zero_ok = False
        degH = sum(1 for j in range(n - 1) if abs(i - j) >= 2)
        if abs(2 * k12 - ((4 + 2 * degH) / D - 2)) > TOL or F(D + 1, D) * ks[e] != F(4 + 2 * degH, D) - 2: cush_ok = False
    # symmetry: left multiplication by g preserves edges and labels; w0-conjugation maps label i -> n-2-i (0-based)
    G = Vs if n <= SYM_ALL_N else [Vs[k] for k in r.sample(range(len(Vs)), 50)]
    comp = lambda g, w: tuple(g[a] for a in w)
    sym_ok = all(lab.get((min(idx[comp(g, Vs[u])], idx[comp(g, Vs[v])]), max(idx[comp(g, Vs[u])], idx[comp(g, Vs[v])]))) == lab[(u, v)]
                 for g in G for (u, v) in E)
    w0 = tuple(range(n - 1, -1, -1)); conj = lambda w: comp(w0, comp(w, w0))
    w0_ok = all(lab.get((min(idx[conj(Vs[u])], idx[conj(Vs[v])]), max(idx[conj(Vs[u])], idx[conj(Vs[v])]))) == n - 2 - lab[(u, v)] for (u, v) in E)
    return dict(n=n, D=D, N=len(adj), E=len(E), n_faces=len(faces), regular=all(len(a) == D for a in adj),
                formula_ok=formula_ok, forman_ok=forman_ok, link_ok=link_ok, hex_ok=hex_ok, link_gap_max=str(gap),
                const_per_label=const_per_label, kmean=str(kmean), kFmean=str(fmean), mean_ok=mean_ok,
                n_lp=len(sample), lp_agree=lp_agree, conv_half_ok=half_ok, conv_zero_ok=zero_ok, cushing_ok=cush_ok,
                sym_ok=sym_ok, n_sym_g=len(G), w0_ok=w0_ok, per_label=per,
                kmin=str(min(ks.values())), kmax=str(max(ks.values())))
def verdict(t):
    if not t['planted_ok'] or t['n_sizes'] == 0 or not t['lp_agree_all'] or not t['sym_all']: return 'ILL-DEFINED'
    if not t['link_all']: v = 'LINK-BREAKS'
    elif t['formula_all']: v = 'LINK-HOLDS'
    else: v = 'LINK-HOLDS-OFF-FORM'
    if not t['conv_all']: v += '+CONV-MISMATCH'
    return v

def _suite(V):
    guard(PREREG, HERE)
    res = {}
    k5 = g_complete(5); res['PL1_complete'] = all(kappa_assign(k5, *e, V) == 1 for e in edges_of(k5))
    c8 = g_cycle(8); c6 = g_cycle(6)
    res['PL2_cycles'] = (all(kappa_assign(c8, *e, V) == 0 for e in edges_of(c8)) and link_gate(c6, [list(range(6))], V)
                         and forman(c6, [list(range(6))], face_index([list(range(6))]), (0, 1), V)[0] == 0)
    q4 = g_cube(4); fq = cube_faces(4); iq = face_index(fq)
    res['PL3_cube4'] = (all(kappa_assign(q4, *e, V) == F(2, 5) for e in edges_of(q4))
                        and all(forman(q4, fq, iq, e, V)[0] == 2 for e in edges_of(q4)) and link_gate(q4, fq, V))
    t3 = g_tree3(); res['PL4_tree3'] = kappa_assign(t3, 0, 1, V) == F(-1, 2)
    a6, f6 = g_prism(6); i6 = face_index(f6); a8, f8 = g_prism(8); i8 = face_index(f8)
    res['PL5_prisms'] = (kappa_assign(a6, 0, 1, V) == 0 and forman(a6, f6, i6, (0, 1), V)[0] == 0
                         and kappa_assign(a6, 0, 6, V) == F(1, 2) and forman(a6, f6, i6, (0, 6), V)[0] == 2
                         and kappa_assign(a8, 0, 1, V) == 0 and forman(a8, f8, i8, (0, 1), V)[0] == -2
                         and kappa_assign(a8, 0, 8, V) == F(1, 2) and forman(a8, f8, i8, (0, 8), V)[0] == 2)
    # PL6 valid alternatives that must be accepted on P_4, P_5: orientation; left-Cayley convention; w0 symmetry; P_3 = C_6
    ok = True
    for n in (4, 5):
        adj, lab, Vs, idx = perm_graph(n); E = edges_of(adj)
        adjL, labL, VsL, idxL = perm_graph(n, left=True); EL = edges_of(adjL)
        byl = lambda A, L, EE: {i: sorted(kappa_assign(A, *e, V) for e in EE if L[e] == i) for i in range(n - 1)}
        b = byl(adj, lab, E); ok &= b == byl(adjL, labL, EL) and all(b[i] == b[n - 2 - i] for i in range(n - 1))
        ok &= all(kappa_assign(adj, u, v, V) == kappa_assign(adj, v, u, V) for u, v in E[:60])
    adj3, lab3, V3, idx3 = perm_graph(3)
    ok &= len(adj3) == 6 and all(len(a) == 2 for a in adj3) and all(kappa_assign(adj3, *e, V) == 0 for e in edges_of(adj3))
    res['PL6_alternatives'] = bool(ok)
    # PL7 LP cross-check and idleness relations on planted graphs (Q_4: kappa_1/2 = 1/4; K_5: kappa_0 = 3/4; tree lazy -1/2)
    res['PL7_lp'] = (abs(kappa_lp(q4, 0, 1, None, V) - 0.4) < TOL and abs(kappa_lp(q4, 0, 1, F(1, 2), V) - 0.25) < TOL
                     and abs(kappa_lp(k5, 0, 1, F(0), V) - 0.75) < TOL and abs(kappa_lp(t3, 0, 1, None, V) + 0.5) < TOL)
    # PL8 gate self-tests: link gate true on hexagonal prism, FALSE on octagonal prism; formula gate rejects a wrong formula
    adj4, lab4, V4, idx4 = perm_graph(4); f4 = perm_faces(4, V4, idx4); i4 = face_index(f4)
    wrongf = all(kappa_assign(adj4, *e, V) == F(2 - forman(adj4, f4, i4, e, V)[2], 4) for e in edges_of(adj4))
    res['PL8_gates'] = link_gate(a6, f6, V) and not link_gate(a8, f8, V) and not wrongf
    # PL9 verdict-map self-test (every branch reachable)
    b = dict(planted_ok=True, n_sizes=6, lp_agree_all=True, sym_all=True, link_all=True, formula_all=True, conv_all=True)
    res['PL9_verdict'] = (verdict(dict(b, planted_ok=False)) == 'ILL-DEFINED' and verdict(dict(b, n_sizes=0)) == 'ILL-DEFINED'
                          and verdict(dict(b, lp_agree_all=False)) == 'ILL-DEFINED' and verdict(dict(b, sym_all=False)) == 'ILL-DEFINED'
                          and verdict(b) == 'LINK-HOLDS' and verdict(dict(b, link_all=False)) == 'LINK-BREAKS'
                          and verdict(dict(b, formula_all=False)) == 'LINK-HOLDS-OFF-FORM'
                          and verdict(dict(b, conv_all=False)) == 'LINK-HOLDS+CONV-MISMATCH')
    # PL10 Cushing et al. Thm 1.2 (RACG) self-check on Q_4 = Cay((Z_2)^4), H = K_4: (4 + 2*3)/4 - 2 = 1/2 = kappa_LLY = (5/4)(2/5)
    res['PL10_cushing'] = F(4 + 2 * 3, 4) - 2 == F(5, 4) * kappa_assign(q4, 0, 1, V)
    return res
def _run(V):
    guard(PREREG, HERE)
    sizes = [] if V.get('empty') else NS
    rows = [census(n, V) for n in sizes]
    t = dict(planted_ok=all(_suite(V).values()), n_sizes=len(rows),
             lp_agree_all=all(r['lp_agree'] for r in rows) if rows else False,
             sym_all=all(r['sym_ok'] and r['w0_ok'] and r['regular'] for r in rows) if rows else False,
             link_all=all(r['link_ok'] for r in rows) if rows else False,
             formula_all=all(r['formula_ok'] and r['forman_ok'] and r['hex_ok'] and r['const_per_label'] and r['mean_ok'] for r in rows) if rows else False,
             conv_all=all(r['conv_half_ok'] and r['conv_zero_ok'] and r['cushing_ok'] for r in rows) if rows else False)
    t['verdict'] = verdict(t); t['rows'] = rows
    return json.loads(json.dumps(t, default=lambda v: (str(v) if isinstance(v, F) else v)))
VARIANTS = ['open_nbhd', 'dist_cap2', 'no_shared', 'hex_as_square', 'empty']
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
    (OUT / f'hgdim2_{mode}.json').write_text(json.dumps(r, indent=1, default=str)); print(json.dumps(r, default=str)[:4000])
