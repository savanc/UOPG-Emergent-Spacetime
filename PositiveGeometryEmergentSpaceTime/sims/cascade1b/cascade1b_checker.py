#!/usr/bin/env python3
"""CASCADE-1b locked checker v2 (prereg/CASCADE-1b-split-fix-blind-retest-2026-10-23.md).
Supersedes sims/cascade1/cascade1_checker.py (v1, locked, NOT edited) for the CASCADE-1b re-test only.
Independent blind re-test on a NEW held-out target (n = 6) with the split-test mass-mapping fix:
every near-zero locus is built from the physical c_ij with the SAME final-family substitution (masses and offsets)
that is applied to the amplitude (v1 defect: locus solved with symbolic m while A had m -> t).
Zero loci: causal diamonds anchored at every chord X_B (2312.16282 sec. 3.2, CITED): D(a,b) = {c_ij : i in [a, b-2],
j in [b, a-2] cyclic}; n(n-3)/2 of them (n = 6: 6 skinny rectangles of size 3, 3 big squares of size 4).
Stage 3 via translation: y = X - mu, c^X_ab = c^y_ab + o_ab(theta).  A_y vanishes on {c^y_D = v} iff v in V_D (computed,
Groebner in <= 4 variables), so Theta_3 = {theta : -o_D(theta) in V_D for all D}.
Held-out (never imposed): near-zero factorisation (eq. 3.8) on {c_D\\{c*} = 0}: (i) factor-count test (number of
variable-disjoint factors, max over elimination sets) must equal the massless reference k0 computed in the same run;
(ii) rank-1 identities for 2312.16282 eq. 3.7 (both lines) and all 6 rotations, at seeded rational family points
(+ one symbolic attempt under a time kill); (iii) n = 5: the v1 split templates with the mass-consistent locus.
Modes: planted | live.  Exact sympy rationals; LP only proposes (cone_dim, copied from v1).
GUARD: guard() in EVERY scoring function, no pass flag.
"""
import hashlib, itertools, json, random, re, signal, subprocess, sys, time
from fractions import Fraction as Fr
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/CASCADE-1b-split-fix-blind-retest-2026-10-23.md'
RUN_ID = 'CASCADE1b-2026-10-23-r1'
SEED = 202610231
V1_LIVE = 'sims/cascade1/cascade1_live.json'   # locked v1 output, read-only (known-result reproduction)
N_POINTS = 3
SYMBOLIC_KILL_S = 900
CELL_KILL_S = 3600

def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)

_FETCH_DONE = []
_ANC_BY_ORIGIN = {}

def _origin_sha():
    return _git('rev-parse', '--verify', '-q', 'refs/remotes/origin/main').stdout.strip()

def guard():
    if not _FETCH_DONE:
        if _git('fetch', '-q', 'origin').returncode != 0:
            sys.exit("GUARD REFUSED: git fetch failed")
        _FETCH_DONE.append(True)
    osha = _origin_sha()
    if not osha:
        sys.exit("GUARD REFUSED: no origin/main ref")
    if osha not in _ANC_BY_ORIGIN:
        psha = _git('log', '--format=%H', '--diff-filter=A', '-n', '1', '--', PREREG).stdout.strip()
        ok = bool(psha) and _git('merge-base', '--is-ancestor', psha, osha).returncode == 0
        _ANC_BY_ORIGIN[osha] = (psha, ok)
    psha, ok = _ANC_BY_ORIGIN[osha]
    if not psha:
        sys.exit(f"GUARD REFUSED: {PREREG} has no commit")
    if not ok:
        sys.exit(f"GUARD REFUSED: prereg commit {psha[:9]} is not an ancestor of origin/main (not pushed)")
    pre = REPO / PREREG
    m = re.search(r'cascade1b_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

class Kill(Exception):
    pass

def _alarm(signum, frame):
    raise Kill()

def with_kill(seconds, fn, *a, **k):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(seconds))
    try:
        return fn(*a, **k)
    finally:
        signal.alarm(0)

# ---------------- kinematics (2312.16282 sec. 2, CITED) ----------------
def chords(n):
    return [(a, b) for a in range(1, n + 1) for b in range(a + 2, n + 1) if (a, b) != (1, n)]

def crosses(P, Q):
    (a, b), (c, d) = P, Q
    return a < c < b < d or c < a < d < b

def canon(P):
    return tuple(sorted(P))

def cyc(n, i):
    return (i - 1) % n + 1

class Kin:
    """symbols X_ab (chords), mu_ab (offsets), m_i (external p_i^2); E0: m_i = 0. prefix 'y' gives the y-world."""
    def __init__(self, n, setting, prefix='X'):
        self.n, self.setting = n, setting
        self.ch = chords(n)
        self.X = {P: sp.Symbol(f'{prefix}{P[0]}{P[1]}') for P in self.ch}
        self.mu = {P: sp.Symbol(f'mu{P[0]}{P[1]}') for P in self.ch}
        self.m = {i: (sp.Symbol(f'm{i}') if setting == 'EM' else sp.Integer(0)) for i in range(1, n + 1)}
        self.theta = [self.mu[P] for P in self.ch] + ([self.m[i] for i in range(1, n + 1)] if setting == 'EM' else [])

    def Xv(self, i, j):
        n = self.n
        i, j = cyc(n, i), cyc(n, j)
        if i == j:
            return sp.Integer(0)
        a, b = sorted((i, j))
        if b - a == 1:
            return self.m[a]
        if (a, b) == (1, n):
            return self.m[n]
        return self.X[(a, b)]

    def c(self, i, j):
        """c_{i,j} = X_{i,j} + X_{i+1,j+1} - X_{i,j+1} - X_{i+1,j}  (eq. 2.4)."""
        return sp.expand(self.Xv(i, j) + self.Xv(i + 1, j + 1) - self.Xv(i, j + 1) - self.Xv(i + 1, j))

    def nonadj_pairs(self):
        n = self.n
        return sorted({canon((i, j)) for i in range(1, n + 1) for j in range(1, n + 1) if (j - i) % n not in (0, 1, n - 1)})

def diamonds(n):
    """causal diamond anchored at chord X_B = (a,b): pairs {c_ij: i in [a..b-2], j in [b..a-2] cyclic}; X_T = X_{b-1,a-1}."""
    out = []
    for (a, b) in chords(n):
        I = [cyc(n, a + s) for s in range(0, b - a - 1)]
        J = [cyc(n, b + s) for s in range(0, n - (b - a) - 1)]
        pairs = sorted({canon((i, j)) for i in I for j in J})
        T = canon((cyc(n, b - 1), cyc(n, a - 1)))
        out.append({'B': (a, b), 'T': T, 'pairs': pairs})
    return out

def triangulation_amp(chs, yv, k):
    tot = sp.Integer(0)
    for S in itertools.combinations(chs, k - 3):
        if all(not crosses(P, Q) for P, Q in itertools.combinations(S, 2)):
            tot += sp.Mul(*[1 / yv[P] for P in S])
    return tot

def lin_solve_rows(eqs, unknowns):
    guard()
    if not eqs:
        return [sp.Matrix([1 if k == i else 0 for k in range(len(unknowns))]) for i in range(len(unknowns))]
    M, b = sp.linear_eq_to_matrix(eqs, unknowns)
    assert all(x == 0 for x in b), "inhomogeneous system"
    return M.nullspace()

def poly_coeff_eqs(expr, gens):
    guard()
    num = sp.numer(sp.together(sp.expand(expr)))
    if num == 0:
        return []
    if not gens:
        return [sp.expand(num)]
    return [cf for cf in sp.Poly(sp.expand(num), *gens).coeffs() if cf != 0]

# ---------------- stages 0-2 (copied from v1; run at n = 4, 5 only) ----------------
def subpolygons(n, P):
    a, b = P
    return list(range(a, b + 1)), list(range(b, n + 1)) + list(range(1, a + 1))

def sub_chords(n, verts):
    k = len(verts); out = []
    for x, y in itertools.combinations(range(k), 2):
        if (y - x) % k in (1, k - 1):
            continue
        out.append((verts[x], verts[y]))
    return out

def run_stages012(n, D, lower=None):
    guard()
    ch = chords(n)
    y = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in ch}
    gens = [y[P] for P in ch]
    monos = sorted(sp.itermonomials(gens, D), key=sp.default_sort_key)
    a = sp.symbols(f'a0:{len(monos)}')
    N = sum(ai * mo for ai, mo in zip(a, monos))
    den = sp.Mul(*gens)
    res = {'n': n, 'D': D, 'n_monomials': len(monos), 'f0': len(monos) - 1}
    eq1 = []
    for P, Q in itertools.combinations(ch, 2):
        if crosses(P, Q):
            rest = [y[R] for R in ch if R not in (P, Q)]
            eq1 += poly_coeff_eqs(N.subs({y[P]: 0, y[Q]: 0}), rest) if rest else [sp.expand(N.subs({y[P]: 0, y[Q]: 0}))]
    ns1 = lin_solve_rows(eq1, list(a))
    res['f1'] = len(ns1) - 1
    kap = sp.Symbol('kappa')
    eq2 = list(eq1)
    for P in ch:
        prod = sp.Integer(1)
        for side in subpolygons(n, P):
            k = len(side)
            if k == 3:
                continue
            sc = [canon(Q) for Q in sub_chords(n, side)]
            if k == 4:
                prod *= lower[4]([y[sc[0]], y[sc[1]]]) if lower else triangulation_amp(sc, y, 4)
            else:
                prod *= triangulation_amp(sc, y, k)
        others = [y[Q] for Q in ch if Q != P]
        expr = sp.cancel(sp.together(N.subs(y[P], 0) - kap * sp.Mul(*others) * prod))
        eq2 += poly_coeff_eqs(expr, others)
    ns2 = lin_solve_rows(eq2, list(a) + [kap])
    res['f2'] = len(ns2) - 1
    res['_y'] = y
    if len(ns2) == 1:
        v = ns2[0]
        A = sp.cancel(sum(v[i] * monos[i] for i in range(len(monos))) / den / v[-1])
        res['_A'] = A
        res['A_equals_triangulation_sum'] = sp.simplify(A - triangulation_amp(ch, y, n)) == 0
    return res

# ---------------- stage 3 via translation ----------------
def offsets(kin):
    """o_ab(theta) := c^X_ab - c^y_ab with X = y + mu (y-world boundary 0)."""
    guard()
    ky = Kin(kin.n, 'E0', prefix='Y')
    out = {}
    for ab in kin.nonadj_pairs():
        cX = kin.c(*ab).subs({kin.X[P]: ky.X[P] + kin.mu[P] for P in kin.ch}, simultaneous=True)
        o = sp.expand(cX - ky.c(*ab))
        assert not (o.free_symbols & set(ky.X.values())), 'offset depends on kinematics'
        out[ab] = o
    return out

def _pick(eqs, xs):
    for S in itertools.combinations(xs, len(eqs)):
        J = sp.Matrix([[sp.diff(e, x) for x in S] for e in eqs])
        if J.det() != 0:
            return list(S)
    raise AssertionError('locus not solvable')

def V_D(n, A_y, y, pairs):
    """variety of v such that A_y vanishes identically on {c^y_ab = v_ab, ab in pairs}."""
    guard()
    k0 = Kin(n, 'E0')
    to_y = {k0.X[P]: y[P] for P in k0.ch}
    vs = sp.symbols(f'v0:{len(pairs)}')
    eqs = [sp.expand(k0.c(*ab).subs(to_y)) - vi for ab, vi in zip(pairs, vs)]
    ys = [y[P] for P in k0.ch][::-1]
    S = _pick(eqs, ys)
    sol = sp.solve(eqs, S, dict=True)[0]
    free = [yy for yy in ys if yy not in S]
    conds = poly_coeff_eqs(A_y.subs(sol), free)
    G = sp.groebner(conds, *vs, order='lex') if conds else None
    zero_only = G is not None and all(G.contains(vi) for vi in vs)
    return {'pairs': pairs, 'v': vs, 'G': G, 'zero_only': zero_only, 'gens': [str(g) for g in (G.exprs if G else [])]}

def variety(conds, theta):
    guard()
    conds = [sp.expand(c) for c in conds if sp.expand(c) != 0]
    if not conds:
        return {'linear': True, 'dim': len(theta), 'relations': [], 'basis': sp.eye(len(theta))}
    G = sp.groebner(conds, *theta, order='grevlex')
    rels = list(G.exprs)
    if any(r.is_number for r in rels):
        return {'linear': True, 'dim': -1, 'relations': [str(r) for r in rels], 'basis': None, 'empty': True}
    if all(sp.Poly(r, *theta).total_degree() <= 1 for r in rels):
        M, b = sp.linear_eq_to_matrix(rels, theta)
        assert all(x == 0 for x in b)
        ns = M.nullspace()
        B = sp.Matrix.hstack(*ns) if ns else sp.zeros(len(theta), 0)
        return {'linear': True, 'dim': len(ns), 'relations': [str(r) for r in rels], 'basis': B}
    comps = sp.solve(rels, theta, dict=True)
    return {'linear': False, 'relations': [str(r) for r in rels], 'components': [str(cpt) for cpt in comps],
            'dim': max((len(theta) - len(cpt)) for cpt in comps) if comps else -1}

def theta3(kin, VDs):
    guard()
    o = offsets(kin)
    conds = []
    for vd in VDs:
        sub = {vi: -o[ab] for ab, vi in zip(vd['pairs'], vd['v'])}
        conds += [sp.expand(g.subs(sub)) for g in vd['G'].exprs]
    return variety(conds, kin.theta), o

# ---------------- stage 4 (copied from v1) ----------------
def cone_dim(B):
    guard()
    from scipy.optimize import linprog
    import numpy as np
    m, k = B.shape
    if k == 0:
        return {'dim': 0, 'forced_zero': list(range(m)), 'certs': 'trivial'}
    Bq = [[Fr(int(sp.fraction(B[i, j])[0]), int(sp.fraction(B[i, j])[1])) for j in range(k)] for i in range(m)]
    Bf = np.array([[float(x) for x in row] for row in Bq])
    forced, witnesses, farkas = [], {}, {}
    for j in range(m):
        r = linprog(-Bf[j], A_ub=np.vstack([-Bf, Bf]), b_ub=np.concatenate([np.zeros(m), np.ones(m)]), bounds=[(None, None)] * k, method='highs')
        ok = False
        if r.status == 0 and -r.fun > 1e-9:
            t = [Fr(x).limit_denominator(10**6) for x in r.x]
            v = [sum(Bq[i][l] * t[l] for l in range(k)) for i in range(m)]
            if all(x >= 0 for x in v) and v[j] > 0:
                witnesses[j] = [str(x) for x in t]; ok = True
        if not ok:
            r2 = linprog(np.zeros(m), A_eq=np.vstack([Bf.T, np.eye(m)[j]]), b_eq=np.concatenate([np.zeros(k), [1.0]]), bounds=[(0, None)] * m, method='highs')
            if r2.status != 0:
                raise AssertionError(f'cone_dim: coordinate {j} unresolved (no witness, no Farkas)')
            lam = [Fr(x).limit_denominator(10**6) for x in r2.x]
            chk = [sum(lam[i] * Bq[i][l] for i in range(m)) for l in range(k)]
            if not (all(x >= 0 for x in lam) and lam[j] > 0 and all(x == 0 for x in chk)):
                raise AssertionError(f'cone_dim: Farkas certificate for {j} failed exact check')
            farkas[j] = [str(x) for x in lam]; forced.append(j)
    if forced:
        Mf = sp.Matrix([[B[j, l] for l in range(k)] for j in forced])
        d = k - Mf.rank()
    else:
        d = k
    return {'dim': d, 'forced_zero': forced, 'witness_t': witnesses, 'farkas_lambda': farkas}

def final_family(kin, B, cd):
    T = len(kin.theta); k = B.shape[1]
    if k == 0:
        return {t: sp.Integer(0) for t in kin.theta}, []
    tt = sp.symbols(f't0:{k}')
    th = B * sp.Matrix(tt); params = list(tt)
    if cd['forced_zero']:
        Mf = sp.Matrix([[B[j, l] for l in range(k)] for j in cd['forced_zero']])
        ns = Mf.nullspace()
        Bf = sp.Matrix.hstack(*ns) if ns else sp.zeros(k, 0)
        uu = sp.symbols(f'u0:{Bf.shape[1]}')
        th = B * (Bf * sp.Matrix(uu)) if Bf.shape[1] else sp.zeros(T, 1)
        params = list(uu) if Bf.shape[1] else []
    return {kin.theta[i]: sp.expand(th[i]) for i in range(T)}, params

# ---------------- held-out: near-zero factorisation ----------------
def components(expr, xs):
    """number of variable-disjoint factors of a rational function (union-find over irreducible factors of num, den)."""
    guard()
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    if sp.expand(num) == 0:
        return 0
    xset = set(xs); parent = {x: x for x in xs}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    present = set()
    for poly in (num, den):
        _, fl = sp.factor_list(poly)
        for f, _e in fl:
            vs = sorted([s for s in f.free_symbols if s in xset], key=str)
            present |= set(vs)
            for v in vs[1:]:
                ra, rb = find(vs[0]), find(v)
                if ra != rb:
                    parent[rb] = ra
    return len({find(x) for x in present})

def amp_at(kin, A_y, y, tv):
    return A_y.subs({y[P]: kin.X[P] - tv.get(kin.mu[P], 0) for P in kin.ch}, simultaneous=True)

def nz_count(kin, A_y, y, tv, L):
    """max over elimination sets of the variable-disjoint factor count of A on {physical c_ab = 0, ab in L},
    with the SAME substitution tv applied to the locus (masses) and the amplitude (offsets, masses): the v2 fix."""
    guard()
    A = amp_at(kin, A_y, y, tv)
    eqs = [sp.expand(kin.c(*ab).subs(tv)) for ab in L]
    Xs = [kin.X[P] for P in kin.ch]
    inv = [x for x in Xs if any(x in e.free_symbols for e in eqs)]
    best, bestS = -1, None
    for S in itertools.combinations(inv, len(eqs)):
        J = sp.Matrix([[sp.diff(e, x) for x in S] for e in eqs])
        if J.det() == 0:
            continue
        sol = sp.solve(eqs, list(S), dict=True)[0]
        free = [x for x in Xs if x not in S]
        k = components(A.subs(sol), free)
        if k > best:
            best, bestS = k, [str(s) for s in S]
    return best, bestS

def rank1_test(kin, A_X, locus_eqs, groups, elim):
    """A restricted to the locus (solved for elim) is a product over groups: rank-1 identity for every bipartition
    (group g vs the rest)."""
    guard()
    X = kin.X
    sol = sp.solve(locus_eqs, [X[e] for e in elim], dict=True)[0]
    Ar = sp.together(A_X.subs(sol))
    allv = [X[P] for g in groups for P in g]
    assert set(allv) | {X[e] for e in elim} == set(X.values()), 'split coordinates incomplete'
    p = {v: sp.Symbol(str(v) + 'p') for v in allv}
    for gi in range(len(groups) - 1):
        g1 = [X[P] for P in groups[gi]]
        g2 = [X[P] for j, g in enumerate(groups) if j != gi for P in g]
        def ev(u1, u2):
            s = {}
            for v in g1:
                s[v] = p[v] if u1 else v
            for v in g2:
                s[v] = p[v] if u2 else v
            return Ar.subs(s, simultaneous=True)
        expr = ev(False, False) * ev(True, True) - ev(False, True) * ev(True, False)
        if sp.expand(sp.numer(sp.together(expr))) != 0:
            return False
    return True

def rot(P, k, n):
    return canon((cyc(n, P[0] + k), cyc(n, P[1] + k)))

# 2312.16282 eq. 3.7 (n = 6), rotation 0:  (zero pairs, groups, eliminated)
EQ37 = [
    ([(1, 3), (1, 5)], [[(1, 3), (2, 6)], [(2, 4), (1, 5), (3, 5), (3, 6), (4, 6)]], [(1, 4), (2, 5)]),
    ([(1, 4), (1, 5), (2, 5)], [[(1, 4), (3, 6)], [(1, 3), (2, 6)], [(1, 5), (4, 6)]], [(2, 4), (2, 5), (3, 5)]),
]
# v1 n = 5 templates (eqs. 3.3, 3.5): (zero pair, g1, g2, eliminated)
SPLIT5 = [((1, 4), [(1, 3), (2, 5)], [(1, 4), (3, 5)], (2, 4)), ((1, 3), [(1, 3), (2, 5)], [(2, 4), (3, 5)], (1, 4))]

def eq37_tests(kin, A_X, tv):
    guard()
    out = []
    for k in range(6):
        for li, (zp, groups, el) in enumerate(EQ37):
            zr = [rot(P, k, 6) for P in zp]
            eqs = [sp.expand(kin.c(*ab).subs(tv)) for ab in zr]
            ok = rank1_test(kin, A_X, eqs, [[rot(P, k, 6) for P in g] for g in groups], [rot(P, k, 6) for P in el])
            out.append({'line': li + 1, 'rotation': k, 'zero': zr, 'ok': ok})
    return out

def split5_tests(kin, A_X, tv):
    guard()
    out = []
    for k in range(5):
        for cp, g1, g2, el in SPLIT5:
            zr = [rot(cp, k, 5)]
            eqs = [sp.expand(kin.c(*ab).subs(tv)) for ab in zr]
            out.append({'rotation': k, 'zero': zr, 'ok': rank1_test(kin, A_X, eqs, [[rot(P, k, 5) for P in g1], [rot(P, k, 5) for P in g2]], [rot(el, k, 5)])})
    return out

def nz_cases(n):
    return [(d, cs) for d in diamonds(n) if len(d['pairs']) >= 2 for cs in d['pairs']]

# ---------------- planted ----------------
def run_planted():
    guard()
    ok = {}
    k5, k6 = Kin(5, 'E0'), Kin(6, 'E0')
    X = k6.X
    X13, X14, X24, X25, X35 = [k5.X[P] for P in [(1, 3), (1, 4), (2, 4), (2, 5), (3, 5)]]
    eq31 = 1/(X13*X14) + 1/(X24*X25) + 1/(X13*X35) + 1/(X14*X24) + 1/(X25*X35)
    x = lambda a, b: X[(a, b)]
    A6 = triangulation_amp(k6.ch, k6.X, 6)
    # eq. 3.6 states: 14 terms in three cyclic classes, representatives 1/(X13X14X15), 1/(X13X36X46), 1/(X13X35X15)
    # [+ 1/(X24X46X26)].  (Smoke-test finding: a literal 6-fold sum of the 2nd representative double-counts an
    # order-3 orbit, so the check is: 14 terms, representatives present, cyclic invariance.)
    terms = sp.Add.make_args(A6)
    reps = [1/(x(1, 3)*x(1, 4)*x(1, 5)), 1/(x(1, 3)*x(3, 6)*x(4, 6)), 1/(x(1, 3)*x(3, 5)*x(1, 5)), 1/(x(2, 4)*x(4, 6)*x(2, 6))]
    rot6 = {X[P]: X[rot(P, 1, 6)] for P in k6.ch}
    eq36_ok = len(terms) == 14 and all(r in terms for r in reps) and sp.expand(A6.subs(rot6, simultaneous=True) - A6) == 0
    ok['PL1 triangulation sum = eq.(3.1) (n=5); n=6: 14 terms, eq.(3.6) representatives, cyclic'] = sp.simplify(triangulation_amp(k5.ch, k5.X, 5) - eq31) == 0 and eq36_ok
    # PL2 diamonds
    d5, d6 = diamonds(5), diamonds(6)
    v1loci = sorted(tuple(sorted(canon((i, j)) for j in range(1, 6) if (j - i) % 5 not in (0, 1, 4))) for i in range(1, 6))
    tele = all(sp.expand(sum(k6.c(*ab) for ab in d['pairs']) - k6.Xv(*d['B']) - k6.Xv(*d['T'])) == 0 for d in d6) and \
           all(sp.expand(sum(k5.c(*ab) for ab in d['pairs']) - k5.Xv(*d['B']) - k5.Xv(*d['T'])) == 0 for d in d5)
    sizes6 = sorted(len(d['pairs']) for d in d6)
    ok['PL2 diamonds: n=5 = v1 Z_i; n=6 9 diamonds (6x3, 3x4); sum c = X_B + X_T'] = sorted(tuple(d['pairs']) for d in d5) == v1loci and sizes6 == [3]*6 + [4]*3 and tele
    # PL3 massless A6 vanishes on all 9 diamonds; planted extra term detected
    zs = []
    for d in d6:
        cs = [k6.c(*ab) for ab in d['pairs']]
        sol = sp.solve(cs, _pick(cs, list(X.values())[::-1]), dict=True)[0]
        zs.append(sp.simplify(A6.subs(sol)) == 0)
    d0 = [d for d in d6 if d['B'] == (1, 3)][0]
    cs = [k6.c(*ab) for ab in d0['pairs']]
    sol = sp.solve(cs, _pick(cs, list(X.values())[::-1]), dict=True)[0]
    nz = sp.simplify((A6 + 1/(x(1, 3)*x(1, 4)*x(1, 5))).subs(sol)) != 0
    ok['PL3 massless A6 vanishes on all 9 diamond loci; planted A6 + 1/(X13X14X15) detected'] = all(zs) and len(zs) == 9 and nz
    # PL4 eq. 3.7 massless (both lines, 6 rotations) + planted non-separable rejected
    t37 = eq37_tests(k6, A6, {})
    bad = A6 + 1/(x(1, 3)*x(2, 4)*x(4, 6))
    zp, groups, el = EQ37[1]
    bad_ok = rank1_test(k6, bad, [k6.c(*ab) for ab in zp], groups, el)
    ok['PL4 eq.(3.7) massless 12/12 (2 lines x 6 rotations); planted non-separable rejected'] = all(t['ok'] for t in t37) and not bad_ok
    # PL5 massless factor counts on the CITED cases
    ky6 = Kin(6, 'E0'); y6 = ky6.X
    k_a = nz_count(k6, A6, k6.X, {}, [(1, 3), (1, 5)])[0]
    k_b = nz_count(k6, A6, k6.X, {}, [(1, 4), (1, 5), (2, 5)])[0]
    A5 = eq31
    k_c = nz_count(k5, A5, k5.X, {}, [(1, 3)])[0]
    ok['PL5 massless factor counts: eq3.7 line1 = 2, line2 = 3, eq3.3 (n=5) = 2'] = (k_a, k_b, k_c) == (2, 3, 2)
    # PL6 v1-defect replica on the CASCADE-1 published n=5 relation family (Rel5, PROVED in PositiveGeometryEmergentSpaceTime.Cascade1):
    k5m = Kin(5, 'EM')
    m = k5m.m; mu = k5m.mu
    rel5 = {mu[(1, 3)]: m[3] - m[4] + m[5], mu[(1, 4)]: m[1] - m[2] + m[3], mu[(2, 4)]: m[1] + m[4] - m[5],
            mu[(2, 5)]: m[2] - m[3] + m[4], mu[(3, 5)]: -m[1] + m[2] + m[5]}
    y5 = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in k5m.ch}
    A5y = triangulation_amp(k5m.ch, y5, 5)
    A5X = amp_at(k5m, A5y, y5, rel5)
    fixed = split5_tests(k5m, A5X, rel5)
    tsub = {m[i]: sp.Symbol(f't{i}') for i in range(1, 6)}
    A5X_t = A5X.subs(tsub)                       # v1: A with m -> t, locus with symbolic m
    v1rep = [rank1_test(k5m, A5X_t, [sp.expand(k5m.c(*z))], [[rot(P, k, 5) for P in g1], [rot(P, k, 5) for P in g2]], [rot(el, k, 5)])
             for k in range(5) for (cp, g1, g2, el) in SPLIT5 for z in [rot(cp, k, 5)]]
    ok['PL6 Rel5 family: mass-consistent splits 10/10; v1-defect replica fails (0/10 as locked v1)'] = all(f['ok'] for f in fixed) and sum(v1rep) == 0
    # PL7 V_D detector: n=4 massless V = {0}; planted 1/y13 + 1/(y24 + 1) gives V = {-1} (flagged not zero-only)
    k4 = Kin(4, 'E0'); y4 = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in k4.ch}
    vA = V_D(4, 1/y4[(1, 3)] + 1/y4[(2, 4)], y4, [(1, 3)])
    vB = V_D(4, 1/y4[(1, 3)] + 1/(y4[(2, 4)] + 1), y4, [(1, 3)])
    ok['PL7 V_D: massless n=4 zero-only; planted shifted zero flagged (V = {-1})'] = vA['zero_only'] and (not vB['zero_only']) and [str(g) for g in vB['G'].exprs] == ['v0 + 1']
    # PL8 cone dims
    ok['PL8 cone dims (0,1,2)'] = (cone_dim(sp.Matrix([[1], [-1]]))['dim'], cone_dim(sp.Matrix([[1], [1]]))['dim'],
                                   cone_dim(sp.Matrix([[1, 0], [0, 1], [1, -1]]))['dim']) == (0, 1, 2)
    # PL9 2312.16282 sec. 7.1: kernel of the c-offset map (E0) is the delta-line at n=6 and trivial at n=5
    def ker(n):
        kin = Kin(n, 'E0'); o = offsets(kin)
        return lin_solve_rows(list(o.values()), kin.theta), kin
    K6, kk6 = ker(6); K5, _ = ker(5)
    dvec = sp.Matrix([(1 if (P[0] % 2 == 0 and P[1] % 2 == 0) else (-1 if (P[0] % 2 == 1 and P[1] % 2 == 1) else 0)) for P in kk6.ch])
    ok['PL9 sec.7.1: E0 c-preserving shifts = delta-line at n=6, none at n=5'] = len(K6) == 1 and sp.Matrix.hstack(K6[0], dvec).rank() == 1 and len(K5) == 0
    for kk, vv in ok.items():
        print(('OK  ' if vv else 'FAIL'), kk)
    allok = all(ok.values())
    print('PLANTED:', 'ALL OK' if allok else 'FAILURES')
    (HERE.parent / 'cascade1b_planted.txt').write_text('\n'.join(f"{'OK' if v else 'FAIL'}  {k}" for k, v in ok.items()) + f"\nPLANTED: {'ALL OK' if allok else 'FAILURES'}\n")
    return allok

# ---------------- live ----------------
def _rowspace_equal(rels_a, rels_b, theta):
    A, _ = sp.linear_eq_to_matrix([sp.sympify(r) for r in rels_a], theta)
    B, _ = sp.linear_eq_to_matrix([sp.sympify(r) for r in rels_b], theta)
    return A.rank() == B.rank() == sp.Matrix.vstack(A, B).rank()

def cell(n, setting, A_y, y, VDs):
    guard()
    kin = Kin(n, setting)
    v3, o = theta3(kin, VDs)
    out = {'n': n, 'setting': setting, 'N_off': len(kin.ch), 'dimTheta0': len(kin.theta), 'S3_linear': v3['linear'],
           'S3_relations': v3['relations'], 'S3_dim': v3['dim']}
    if not v3['linear'] or v3.get('empty'):
        out['S4_dim'] = None; out['K_final'] = v3['dim']; out['note'] = 'nonlinear/empty Theta_3: S4 not evaluated'
        return out, kin, None, None
    cd = cone_dim(v3['basis'])
    out['S4_dim'] = cd['dim']
    out['S4_forced_zero'] = [str(kin.theta[j]) for j in cd['forced_zero']]
    out['S4_certs'] = {'witness_t': cd.get('witness_t'), 'farkas_lambda': cd.get('farkas_lambda')}
    fam, params = final_family(kin, v3['basis'], cd)
    out['final_family'] = {str(k): str(v) for k, v in fam.items()}
    out['final_params'] = [str(p) for p in params]
    out['K_final'] = cd['dim']
    out['outcome'] = 'MATCH' if out['K_final'] == len(kin.ch) else ('BELOW' if out['K_final'] < len(kin.ch) else 'ABOVE')
    out['ratio'] = 'RATIOS-FREE' if cd['dim'] >= 2 else ('RATIO-FIXED' if cd['dim'] == 1 else 'NO-MASSES-SURVIVE')
    return out, kin, fam, params

def points(fam, params, rng, k):
    pts = []
    for _ in range(k):
        val = {p: sp.Rational(rng.randint(1, 40), rng.randint(1, 6)) for p in params}
        pts.append({t: sp.expand(e.subs(val)) for t, e in fam.items()})
    return pts

def run_live():
    guard()
    t0 = time.time()
    rng = random.Random(SEED)
    out = {'run_id': RUN_ID, 'seed': SEED, 'started': time.strftime('%Y-%m-%d %H:%M:%S %Z'), 'cells': {}}
    # known-result reproduction: stages 0-2 at n = 4, 5 (v1 numbers), A6 := triangulation sum (eq. 3.6, PL1)
    s4 = run_stages012(4, 1)
    A4, y4 = s4['_A'], s4['_y']
    lower = {4: lambda ys: A4.subs({y4[(1, 3)]: ys[0], y4[(2, 4)]: ys[1]}, simultaneous=True)}
    s5 = run_stages012(5, 3, lower=lower)
    out['stages012'] = {'n4': {k: v for k, v in s4.items() if not k.startswith('_')}, 'n5': {k: v for k, v in s5.items() if not k.startswith('_')}}
    repro012 = (s4['f0'], s4['f1'], s4['f2'], s5['f0'], s5['f1'], s5['f2']) == (2, 1, 0, 55, 4, 0) and s4['A_equals_triangulation_sum'] and s5['A_equals_triangulation_sum']
    y6 = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in chords(6)}
    amps = {4: (A4, y4), 5: (s5['_A'], s5['_y']), 6: (triangulation_amp(chords(6), y6, 6), y6)}
    print('stages 0-2 reproduce v1:', repro012, f'({time.time()-t0:.0f}s)')
    VD = {}
    for n in (4, 5, 6):
        A_y, y = amps[n]
        try:
            VD[n] = [with_kill(CELL_KILL_S, V_D, n, A_y, y, d['pairs']) for d in diamonds(n)]
        except Kill:
            out['verdict'] = f'NOT-EVALUATED (V_D time kill {CELL_KILL_S}s at n={n})'
            (HERE.parent / 'cascade1b_live.json').write_text(json.dumps(out, indent=1, default=str))
            print('VERDICT (python):', out['verdict'])
            return out
        out[f'V_D_n{n}'] = [{'B': d['B'], 'pairs': vd['pairs'], 'zero_only': vd['zero_only'], 'groebner': vd['gens']} for d, vd in zip(diamonds(n), VD[n])]
        print(f'V_D n={n}: zero_only', [vd['zero_only'] for vd in VD[n]], f'({time.time()-t0:.0f}s)')
    fams = {}
    for n in (4, 5, 6):
        for setting in ('E0', 'EM'):
            c, kin, fam, params = cell(n, setting, *amps[n], VD[n])
            out['cells'][f'{setting}-n{n}'] = c; fams[(n, setting)] = (kin, fam, params)
            print(f'--- {setting}-n{n}:', json.dumps({k: c.get(k) for k in ('S3_dim', 'S4_dim', 'K_final', 'N_off', 'outcome', 'ratio')}))
            print('    relations:', c['S3_relations']); print('    family:', c.get('final_family'))
    # reproduction of v1 n = 4, 5 relations
    v1 = json.loads((REPO / V1_LIVE).read_text())
    rep = {}
    for n in (4, 5):
        for setting in ('E0', 'EM'):
            kin = fams[(n, setting)][0]
            rep[f'{setting}-n{n}'] = _rowspace_equal(v1['cells'][f'{setting}-n{n}']['S3']['relations'], out['cells'][f'{setting}-n{n}']['S3_relations'], kin.theta) and \
                v1['cells'][f'{setting}-n{n}']['K_final'] == out['cells'][f'{setting}-n{n}']['K_final']
    out['reproduces_v1_S3_S4'] = rep
    print('reproduces v1 relations and K at n=4,5:', rep)
    # n = 5 reproduction (non-blind): v1 templates with the mass-consistent locus, symbolic EM-n5 family
    kin5, fam5, _ = fams[(5, 'EM')]
    A5X = amp_at(kin5, *amps[5], fam5)
    s5t = split5_tests(kin5, A5X, fam5)
    out['repro_n5_split_fixed'] = s5t
    print('n=5 EM fixed v1 templates (symbolic):', f"{sum(t['ok'] for t in s5t)}/{len(s5t)}", f'({time.time()-t0:.0f}s)')
    # held-out n = 6 (BLIND, verdict-bearing): EM-n6 final family
    kin6, fam6, par6 = fams[(6, 'EM')]
    A6y, y6 = amps[6]
    kin6E0 = Kin(6, 'E0')
    ref = {}
    cases = nz_cases(6)
    for d, cs in cases:
        L = [ab for ab in d['pairs'] if ab != cs]
        ref[(d['B'], cs)] = nz_count(kin6E0, A6y, y6, {}, L)
    out['heldout_reference_k0'] = [{'B': B, 'c_on': cs, 'k0': v[0], 'elim': v[1]} for (B, cs), v in ref.items()]
    print('massless reference k0:', sorted(collections_count([v[0] for v in ref.values()]).items()), f'({time.time()-t0:.0f}s)')
    ho = {'factor_count': [], 'eq37_points': [], 'eq37_symbolic': None}
    pts = points(fam6, par6, rng, N_POINTS) if fam6 is not None else []
    out['heldout_points'] = [{str(k): str(v) for k, v in p.items()} for p in pts]
    for pi, tv in enumerate(pts):
        for d, cs in cases:
            L = [ab for ab in d['pairs'] if ab != cs]
            k, S = nz_count(kin6, A6y, y6, tv, L)
            k0 = ref[(d['B'], cs)][0]
            ho['factor_count'].append({'point': pi, 'B': d['B'], 'c_on': cs, 'k': k, 'k0': k0, 'elim': S, 'ok': k == k0 and k0 >= 2})
        A6X = amp_at(kin6, A6y, y6, tv)
        ho['eq37_points'] += [dict(t, point=pi) for t in eq37_tests(kin6, A6X, tv)]
        print(f'held-out point {pi}: factor-count', f"{sum(h['ok'] for h in ho['factor_count'] if h['point']==pi)}/{len(cases)}",
              'eq3.7', f"{sum(h['ok'] for h in ho['eq37_points'] if h['point']==pi)}/12", f'({time.time()-t0:.0f}s)')
    # one symbolic attempt (eq. 3.7, rotation 0, both lines) under a time kill
    if fam6 is not None:
        try:
            A6Xs = amp_at(kin6, A6y, y6, fam6)
            def sym():
                res = []
                for li, (zp, groups, el) in enumerate(EQ37):
                    eqs = [sp.expand(kin6.c(*ab).subs(fam6)) for ab in zp]
                    res.append({'line': li + 1, 'ok': rank1_test(kin6, A6Xs, eqs, groups, el)})
                return res
            ho['eq37_symbolic'] = with_kill(SYMBOLIC_KILL_S, sym)
        except Kill:
            ho['eq37_symbolic'] = f'NOT-EVALUATED (time kill {SYMBOLIC_KILL_S}s)'
    print('eq3.7 symbolic:', ho['eq37_symbolic'], f'({time.time()-t0:.0f}s)')
    out['heldout_n6_EM'] = ho
    # power control (D3-style): generic theta off Theta_3
    ctl = {t: sp.Rational(rng.randint(1, 40), rng.randint(1, 6)) for t in kin6.theta}
    cres = []
    for d, cs in cases:
        L = [ab for ab in d['pairs'] if ab != cs]
        k, S = nz_count(kin6, A6y, y6, ctl, L)
        cres.append({'B': d['B'], 'c_on': cs, 'k': k, 'k0': ref[(d['B'], cs)][0], 'ok': k == ref[(d['B'], cs)][0]})
    out['control_offfamily'] = {'theta': {str(k): str(v) for k, v in ctl.items()}, 'tests': cres, 'pass_count': sum(c['ok'] for c in cres)}
    print('control (off Theta_3):', f"{sum(c['ok'] for c in cres)}/{len(cres)} pass (power requires < {len(cres)})", f'({time.time()-t0:.0f}s)')
    # verdict
    fc_ok = all(h['ok'] for h in ho['factor_count']) and len(ho['factor_count']) == N_POINTS * len(cases)
    e37_ok = all(h['ok'] for h in ho['eq37_points']) and len(ho['eq37_points']) == N_POINTS * 12
    sym_ok = not (isinstance(ho['eq37_symbolic'], list) and not all(h['ok'] for h in ho['eq37_symbolic']))
    repro_ok = repro012 and all(rep.values()) and all(t['ok'] for t in s5t)
    vd_lin = all(vd['zero_only'] for n in VD for vd in VD[n])
    if not repro_ok:
        verdict = 'ILL-DEFINED (known-result reproduction failed)'
    elif fam6 is None:
        verdict = 'NOT-POSED (EM-n6 Theta_3 nonlinear or empty)'
    elif not (fc_ok and e37_ok and sym_ok):
        verdict = 'FAIL (held-out n=6 near-zero factorisation violated on the EM-n6 final family)'
    elif out['control_offfamily']['pass_count'] == len(cases):
        verdict = 'PASS-UNDERPOWERED (held-out passes but the off-family control also passes everywhere)'
    else:
        verdict = 'PASS (held-out n=6 near-zero factorisation holds on the EM-n6 final family; control fails off Theta_3)'
    cells = out['cells']
    H = 'CONFIRMED' if all(c.get('outcome') == 'MATCH' for c in cells.values()) else 'REFUTED-AS-STATED (' + ', '.join(f"{k}={c.get('outcome')}" for k, c in cells.items()) + ')'
    out['V_D_all_zero_only'] = vd_lin
    out['verdict'] = verdict; out['H_retest'] = H
    out['ratio'] = {k: c.get('ratio') for k, c in cells.items()}
    out['elapsed_s'] = round(time.time() - t0, 1)
    print('VERDICT (python):', verdict); print('H re-test:', H); print('RATIO:', out['ratio'])
    (HERE.parent / 'cascade1b_live.json').write_text(json.dumps(out, indent=1, default=str))
    return out

def collections_count(xs):
    d = {}
    for x in xs:
        d[x] = d.get(x, 0) + 1
    return d

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    print(f"run {RUN_ID} seed {SEED} mode {mode} ({time.strftime('%Y-%m-%d %H:%M:%S %Z')})")
    if mode == 'planted':
        sys.exit(0 if run_planted() else 1)
    elif mode == 'live':
        run_live()
    else:
        sys.exit(f"unknown mode {mode}")

if __name__ == '__main__':
    main()
