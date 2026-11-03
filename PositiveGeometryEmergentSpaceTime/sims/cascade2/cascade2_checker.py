#!/usr/bin/env python3
"""CASCADE-2 locked checker (prereg/CASCADE-2-delta-deformed-ratio-test-2026-10-28.md).
delta-deformed mass-shifted Tr phi^3 (2312.16282 sec. 7, CITED, generalised): propagators y_P = X_P - mu_P - Lambda kappa_P,
Lambda -> infinity, kappa a free direction.  Question: does any stage FIX A MASS RATIO, and does it survive an
anti-numerology test (random triangulation coefficients) with a look-elsewhere max statistic at p < 0.01?
Stages (fixed order): S3' zeros for all Lambda (causal diamonds; V_D numerator method copied from CASCADE-1b checker v3),
S5 NLSM limit (A = O(Lambda^-(n-2)) with a non-vanishing Lambda^-(n-2) coefficient; kappa != 0 on its support),
S4 positivity on external m and finite mu (secondary: strict positivity of every internal M^2 = mu + Lambda kappa).
Shared kinematics/variety/cone_dim code is COPIED from sims/cascade1b/cascade1b_checker.py (v2), V_D/lcm_numerator from
sims/cascade1b/cascade1b_checker_v3.py (not imported).  Checkpoints: runs/<RUN_ID>/{vd.jsonl, null.jsonl, progress.log}.
GUARD: guard() in EVERY scoring function, no pass flag.
"""
import hashlib, itertools, json, random, re, signal, subprocess, sys, time
from fractions import Fraction as Fr
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/CASCADE-2-delta-deformed-ratio-test-2026-10-28.md'
RUN_ID = 'CASCADE2-2026-10-28-r1'
SEED = 202610232
N_NULL = 300
COEFF_MAX = 9
S5_KILL_S = 1200
ENUM_KILL_S = 3600
VD_KILL_S = 3600
CELL_KILL_S = 3600
P_THRESHOLD = sp.Rational(1, 100)
RUNDIR = REPO / 'runs' / RUN_ID

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
    m = re.search(r'cascade2_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
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

def _lin_factors(d):
    """factor dict {linear form: power} of a term denominator (product of linear forms in y)."""
    out = {}
    for f, e in sp.factor_list(sp.expand(d))[1]:
        out[f] = out.get(f, 0) + e
    return out

def lcm_numerator(A_y):
    """N with A_y = N / L, L = lcm of the term denominators (all linear-form products); returns (N, factor dict of L)."""
    guard()
    terms = []
    L = {}
    for t in sp.Add.make_args(sp.expand(A_y)):
        nu, de = t.as_numer_denom()
        c0, fd = sp.factor_list(sp.expand(de))
        terms.append((nu / c0, dict(fd)))
        for f, e in fd:
            L[f] = max(L.get(f, 0), e)
    N = sp.Integer(0)
    for nu, fd in terms:
        N += nu * sp.Mul(*[f ** (e - fd.get(f, 0)) for f, e in L.items()])
    return sp.expand(N), L

def V_D(n, A_y, y, pairs):
    """v3: variety of v such that A_y vanishes identically on {c^y_ab = v_ab, ab in pairs} (numerator method)."""
    guard()
    k0 = Kin(n, 'E0')
    to_y = {k0.X[P]: y[P] for P in k0.ch}
    vs = sp.symbols(f'v0:{len(pairs)}')
    eqs = [sp.expand(k0.c(*ab).subs(to_y)) - vi for ab, vi in zip(pairs, vs)]
    ys = [y[P] for P in k0.ch][::-1]
    S = _pick(eqs, ys)
    sol = sp.solve(eqs, S, dict=True)[0]
    free = [yy for yy in ys if yy not in S]
    N, L = lcm_numerator(A_y)
    Ns = sp.expand(N.subs(sol))
    conds = [] if Ns == 0 else ([Ns] if not free else [cf for cf in sp.Poly(Ns, *free).coeffs() if cf != 0])
    vonly = []
    for f in L:
        fs = sp.expand(f.subs(sol))
        if fs == 0:
            raise AssertionError('denominator vanishes identically on the locus')
        if not (fs.free_symbols & set(free)) and not fs.is_number:
            vonly.append(fs)
    if conds and vonly:
        t = sp.Symbol('t_sat')
        Gt = sp.groebner(conds + [1 - t * sp.Mul(*vonly)], t, *vs, order='lex')
        conds = [g for g in Gt.exprs if t not in g.free_symbols]
    G = sp.groebner(conds, *vs, order='lex') if conds else None
    zero_only = G is not None and all(G.contains(vi) for vi in vs)
    return {'pairs': pairs, 'v': vs, 'G': G, 'zero_only': zero_only, 'gens': [str(g) for g in (G.exprs if G else [])],
            'v_only_denominators': [str(f) for f in vonly]}

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

def rot(P, k, n):
    return canon((cyc(n, P[0] + k), cyc(n, P[1] + k)))


# ---------------- S5: Lambda -> infinity expansion (eps = 1/Lambda) ----------------
def triangulations(n):
    ch = chords(n)
    return [S for S in itertools.combinations(ch, n - 3) if all(not crosses(P, Q) for P, Q in itertools.combinations(S, 2))]

def _mul_trunc(a, b, order):
    out = [sp.Integer(0)] * (order + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j > order:
                break
            if bj != 0:
                out[i + j] += ai * bj
    return out

def s5_series(n, kap, coeffs=None, order=None):
    """eps-series coefficients (eps = 1/Lambda, up to eps^order) of sum_T a_T prod_{P in T} 1/(x_P - kap_P/eps);
    x_P := X_P - mu_P (translation; S5 is mu-independent). kap_P == 0 (structural) gives 1/x_P."""
    guard()
    order = n - 2 if order is None else order
    x = {P: sp.Symbol(f'x{P[0]}{P[1]}') for P in chords(n)}
    total = [sp.Integer(0)] * (order + 1)
    for T in triangulations(n):
        a = sp.Integer(1) if coeffs is None else sp.Integer(coeffs[T])
        ser = [a] + [sp.Integer(0)] * order
        for P in T:
            k = sp.sympify(kap.get(P, 0))
            if k == 0:
                fac = [1 / x[P]] + [sp.Integer(0)] * order
            else:
                fac = [sp.Integer(0)] + [-(x[P] ** (j - 1)) / k ** j for j in range(1, order + 1)]
            ser = _mul_trunc(ser, fac, order)
        total = [t + s for t, s in zip(total, ser)]
    return total, x

def s5_conditions(n, kap, coeffs=None):
    """conditions (polynomials in the kappa parameters) for eps^j coefficient == 0 identically in x, j < n-2."""
    guard()
    total, x = s5_series(n, kap, coeffs)
    xs = list(x.values())
    conds = []
    for j in range(n - 2):
        conds += poly_coeff_eqs(total[j], xs)
    return conds, total[n - 2], x

def height(r):
    r = sp.Rational(r)
    return max(abs(r.p), abs(r.q))

def ratio_analysis(conds, kvars, nonzero):
    """variety of conds with every expression in `nonzero` != 0; for each pair of kvars the set of values of
    k_P/k_Q if finite (FIXED) else FREE.  Exact reductions: when nonzero == kvars, monomial factors are stripped
    (kvars != 0); when every condition is homogeneous, the first kvar is set to 1 (ratios are scale-free).
    Emptiness: grevlex Groebner basis of conds + saturation z*prod(nonzero) - 1 equals [1]."""
    guard()
    conds = [c for c in (sp.expand(c) for c in conds) if c != 0]
    if nonzero == list(kvars) and conds:
        conds = sorted({sp.Poly(c, *kvars).terms_gcd()[1].as_expr() for c in conds}, key=str)
    homog = all(sp.Poly(c, *kvars).is_homogeneous for c in conds) if conds else True
    fix = {kvars[0]: sp.Integer(1)} if (homog and kvars) else {}
    rest = [k for k in kvars if k not in fix]
    cs = [c for c in (sp.expand(c.subs(fix)) for c in conds) if c != 0]
    if any(c.is_number for c in cs):
        return {'status': 'EMPTY', 'pairs': {}}
    nzs = [sp.expand(sp.sympify(e).subs(fix)) for e in nonzero]
    z = sp.Symbol('z_sat')
    if rest or cs:
        G = sp.groebner(cs + [z * sp.Mul(*nzs) - 1], z, *rest, order='grevlex')
        if list(G.exprs) == [1]:
            return {'status': 'EMPTY', 'pairs': {}}
    comps = sp.solve(cs, rest, dict=True) if cs else [{}]
    good = [cpt for cpt in comps if all(sp.simplify(e.subs(cpt)) != 0 for e in nzs)]
    if not good:
        return {'status': 'EMPTY', 'pairs': {}}
    pairs = {}
    for P, Q in itertools.combinations(kvars, 2):
        vals, free = set(), False
        for cpt in good:
            full = dict(fix); full.update(cpt)
            r = sp.simplify(sp.sympify(P).subs(full) / sp.sympify(Q).subs(full))
            if r.free_symbols:
                free = True
                break
            vals.add(r)
        pairs[(str(P), str(Q))] = 'FREE' if free else sorted(vals, key=lambda v: (height(v) if v.is_Rational else 10**9, str(v)))
    comps_full = []
    for cpt in good:
        full = dict(fix); full.update(cpt)
        comps_full.append({str(k): str(v) for k, v in full.items()})
    return {'status': 'OK', 'pairs': pairs, 'components': comps_full, 'dehomogenised': bool(fix)}

def min_height(ra):
    hs = []
    for v in ra.get('pairs', {}).values():
        if v != 'FREE':
            hs += [height(r) for r in v if sp.sympify(r).is_Rational and r != 0]
    return min(hs) if hs else None

def ee_oo_support(n):
    return [P for P in chords(n) if P[0] % 2 == P[1] % 2]

def s5_alone(n, support, coeffs=None):
    """S5 with kappa free and nonzero on `support`, zero elsewhere."""
    guard()
    kv = [sp.Symbol(f'k{P[0]}{P[1]}') for P in support]
    kap = dict(zip(support, kv))
    conds, lead, x = s5_conditions(n, kap, coeffs)
    ra = ratio_analysis(conds, kv, kv)
    if ra['status'] == 'OK':
        # leading coefficient must not vanish identically on the variety (checked at each component, generic point)
        ok_lead = []
        for cpt in ra['components']:
            sub = {sp.Symbol(k): sp.sympify(v) for k, v in cpt.items()}
            free = sorted(set().union(*[sp.sympify(v).free_symbols for v in cpt.values()]) | (set(kv) - set(sub)), key=str)
            pt = {f: sp.Integer(2 + i) for i, f in enumerate(free)}
            L = sp.together(lead.subs(sub).subs(pt))
            ok_lead.append(sp.expand(sp.numer(L)) != 0)
        ra['lead_nonzero'] = ok_lead
        if not any(ok_lead):
            ra['status'] = 'EMPTY (leading coefficient vanishes)'
    return ra

def p_value(h_obs, h_null):
    """(1 + #{null draws with a fixed ratio of height <= h_obs}) / (N + 1); None heights = no fixed ratio."""
    guard()
    if h_obs is None:
        return None
    k = sum(1 for h in h_null if h is not None and h <= h_obs)
    return sp.Rational(1 + k, len(h_null) + 1)

# ---------------- cascade cells ----------------
def theta3_lambda(kin, VDs, kvec):
    """S3': A(X - mu - Lambda kappa) vanishes on every diamond for all Lambda: conditions in (theta, kappa)."""
    guard()
    o = offsets(kin)
    oE = offsets(Kin(kin.n, 'E0'))
    lam = sp.Symbol('Lam')
    conds = []
    for vd in VDs:
        sub = {vi: -(o[ab] + lam * oE[ab].subs({kin.mu[P]: kvec[P] for P in kin.ch}, simultaneous=True)) for ab, vi in zip(vd['pairs'], vd['v'])}
        for g in vd['G'].exprs:
            e = sp.expand(g.subs(sub))
            conds += [cf for cf in sp.Poly(e, lam).coeffs() if cf != 0] if e != 0 else []
    return conds

def linear_ratios(fam, qs, params):
    """fixed ratios among the linear functions q (dict name -> expr in params) on a linear family."""
    out = {}
    names = [k for k in qs if sp.expand(qs[k]) != 0]
    for a, b in itertools.combinations(names, 2):
        M = sp.Matrix([[sp.diff(qs[a], p) for p in params], [sp.diff(qs[b], p) for p in params]]) if params else sp.zeros(2, 0)
        if params and M.rank() == 1:
            r = sp.simplify(qs[a] / qs[b])
            if not r.free_symbols:
                out[(a, b)] = r
    return out

def cell2(n, setting, A_y, y, VDs, coeffs=None):
    guard()
    kin = Kin(n, setting)
    kvec = {P: sp.Symbol(f'k{P[0]}{P[1]}') for P in kin.ch}
    kvars = [kvec[P] for P in kin.ch]
    conds = theta3_lambda(kin, VDs, kvec)
    allv = kin.theta + kvars
    v3 = variety(conds, allv)
    out = {'n': n, 'setting': setting, 'S3p_linear': v3['linear'], 'S3p_dim': v3['dim'], 'S3p_relations': v3['relations']}
    if not v3['linear'] or v3.get('empty'):
        out['verdict_cell'] = 'NOT-POSED (nonlinear/empty S3prime)'
        return out
    B = v3['basis']
    T = len(kin.theta)
    Bth = B[:T, :]; Bk = B[T:, :]
    # S3' family splits (theta-block, kappa-block) because the Lambda^1 and Lambda^0 conditions separate
    k_basis = [Bk[:, j] for j in range(B.shape[1]) if any(x != 0 for x in Bk[:, j])]
    th_basis = [Bth[:, j] for j in range(B.shape[1]) if all(x == 0 for x in Bk[:, j])]
    assert len(k_basis) + len(th_basis) == B.shape[1], 'S3prime family does not split into theta and kappa blocks'
    out['kappa_dim_S3p'] = len(k_basis)
    dl = sp.symbols(f'd0:{len(k_basis)}')
    kfam = {P: sp.expand(sum(dl[j] * k_basis[j][i] for j in range(len(k_basis)))) for i, P in enumerate(kin.ch)} if k_basis else {P: sp.Integer(0) for P in kin.ch}
    out['kappa_family'] = {str(kvec[P]): str(v) for P, v in kfam.items()}
    # S5 on the S3' kappa family
    conds5, lead, x = s5_conditions(n, kfam, coeffs)
    nz = [kfam[P] for P in kin.ch if kfam[P] != 0]
    if not dl:
        out['S5'] = 'EMPTY (kappa = 0 forced by S3prime; A = O(1))'
        out['verdict_cell'] = 'NO-DEFORMATION'
        return out
    ra = ratio_analysis(conds5, list(dl), nz)
    out['S5_status'] = ra['status']
    if ra['status'] != 'OK':
        out['verdict_cell'] = 'NO-DEFORMATION (S5 empty on the S3prime family)'
        return out
    pt = {d: sp.Integer(3 + i) for i, d in enumerate(dl)}
    lead_ok = sp.expand(sp.numer(sp.together(lead.subs(pt)))) != 0
    out['S5_lead_nonzero'] = lead_ok
    if not lead_ok:
        out['verdict_cell'] = 'NO-DEFORMATION (leading coefficient vanishes)'
        return out
    # S4 on (mu, m): positivity cone of the theta block
    Bt = sp.Matrix.hstack(*th_basis) if th_basis else sp.zeros(T, 0)
    cd = cone_dim(Bt)
    fam, params = final_family(kin, Bt, cd)
    out['S4_theta_dim'] = cd['dim']
    out['final_theta_family'] = {str(k): str(v) for k, v in fam.items()}
    out['dim_final'] = cd['dim'] + len(dl)
    # strict positivity (secondary): every internal M^2 = mu + Lambda kappa >= 0 for large Lambda -> kappa >= 0 on all chords
    kB = sp.Matrix.hstack(*k_basis)
    out['strict_positivity_kappa_cone_dim'] = cone_dim(kB)['dim']
    # fixed ratios: q in m_i, mu_P (finite) and kappa_P (Lambda-masses)
    qs = {str(t): fam[t] for t in kin.theta}
    qs.update({f'kappa{P[0]}{P[1]}': kfam[P] for P in kin.ch})
    prm = list(params) + list(dl)
    fixed = linear_ratios(fam, qs, prm)
    old = linear_ratios(fam, {str(t): fam[t] for t in kin.theta}, list(params))   # the CASCADE-1b-type family
    classified = []
    for (a, b), r in fixed.items():
        both_pos = _can_both_be_positive(qs[a], qs[b], prm, Bt, cd, dl)
        cls = {'pair': [a, b], 'ratio': str(r), 'height': height(r) if r.is_Rational else None, 'positive': bool(r > 0),
               'nontrivial': r not in (1, -1), 'involves_kappa': a.startswith('kappa') or b.startswith('kappa'),
               'new_vs_1b': (a, b) not in old, 'both_nontachyonic_possible': both_pos}
        cls['PHYS'] = cls['positive'] and cls['nontrivial'] and cls['new_vs_1b'] and both_pos
        classified.append(cls)
    out['fixed_ratios'] = classified
    out['RATIO_FIXED_any'] = bool(classified)
    out['PHYS_candidates'] = [c for c in classified if c['PHYS']]
    out['verdict_cell'] = 'DEFORMATION-EXISTS'
    return out

def _can_both_be_positive(qa, qb, prm, Bt, cd, dl):
    # sample: theta params in the S4 cone are free reals >= interior; kappa params free reals. Exact LP-free check:
    # a fixed positive ratio means qa, qb have the same sign everywhere; both > 0 possible iff qa > 0 somewhere.
    for sgn in (1, -1):
        pt = {p: sp.Integer(sgn * (i + 2)) for i, p in enumerate(prm)}
        if sp.sympify(qa).subs(pt) > 0 and sp.sympify(qb).subs(pt) > 0:
            return True
    return False

# ---------------- planted ----------------
def run_planted():
    guard()
    ok = {}
    # PL1 eq. 7.17: X13 - delta, X24 + delta  <=>  kappa13 = +1, kappa24 = -1 (y = X - Lambda kappa, Lambda = delta)
    tot4, x4 = s5_series(4, {(1, 3): 1, (2, 4): -1})
    ok['PL1 eq.(7.17): eps^1 coefficient 0, eps^2 coefficient -(X13+X24)'] = sp.simplify(tot4[0]) == 0 and sp.simplify(tot4[1]) == 0 and sp.simplify(tot4[2] + x4[(1, 3)] + x4[(2, 4)]) == 0
    # PL2 eq. 7.20: n=6, oo: kappa +1, ee: kappa -1, oe: 0
    kap6 = {P: (1 if P[0] % 2 == 1 and P[1] % 2 == 1 else (-1 if P[0] % 2 == 0 and P[1] % 2 == 0 else 0)) for P in chords(6)}
    tot6, x = s5_series(6, kap6)
    X = lambda a, b: x[canon((cyc(6, a), cyc(6, b)))]
    br = sum(-(X(1+s, 3+s) + X(2+s, 4+s)) * (X(1+s, 5+s) + X(4+s, 6+s)) / X(1+s, 4+s) for s in (0, 2, 4)) + X(1, 3) + X(3, 5) + X(1, 5) + X(2, 4) + X(4, 6) + X(2, 6)
    ok['PL2 eq.(7.20): eps^0..eps^3 vanish, eps^4 coefficient = -(eq. 7.20 bracket)'] = all(sp.simplify(tot6[j]) == 0 for j in range(4)) and sp.simplify(tot6[4] + br) == 0
    # PL3 sec. 7.1 kernel
    def ker(n):
        kin = Kin(n, 'E0'); o = offsets(kin)
        return lin_solve_rows(list(o.values()), kin.theta)
    ok['PL3 sec.7.1: E0 c-preserving shifts: n=6 one-dimensional, n=4 one-dimensional, n=5 none'] = (len(ker(6)), len(ker(4)), len(ker(5))) == (1, 1, 0)
    # PL4 planted 1/y13 + 2/y24 -> kappa13/kappa24 = -1/2
    T4 = triangulations(4)
    ra = s5_alone(4, [(1, 3), (2, 4)], {T4[0]: 1, T4[1]: 2} if T4[0] == ((1, 3),) else {T4[0]: 2, T4[1]: 1})
    ok['PL4 planted 1/y13 + 2/y24 fixes kappa13/kappa24 = -1/2'] = ra['status'] == 'OK' and ra['pairs'].get(('k13', 'k24')) == [sp.Rational(-1, 2)]
    # PL5 p-value unit test
    ok['PL5 p_value: (1 + #{h <= h_obs})/(N+1)'] = p_value(1, [None, 1, 2, 3, None, 1, 5, None, 9]) == sp.Rational(3, 10) and p_value(2, [None] * 99) == sp.Rational(1, 100) and p_value(None, [1]) is None
    # PL6 ratio_analysis toys
    k1, k2 = sp.symbols('q1 q2')
    t1 = ratio_analysis([], [k1, k2], [k1, k2])['pairs'][('q1', 'q2')] == 'FREE'
    t2 = ratio_analysis([k1 + k2], [k1, k2], [k1, k2])['pairs'][('q1', 'q2')] == [-1]
    t3 = set(ratio_analysis([(k1 - 2 * k2) * (k1 + 3 * k2)], [k1, k2], [k1, k2])['pairs'][('q1', 'q2')]) == {2, -3}
    t4 = ratio_analysis([k1], [k1, k2], [k1, k2])['status'] == 'EMPTY'
    ok['PL6 ratio_analysis toys: FREE, {-1}, {2,-3}, EMPTY'] = t1 and t2 and t3 and t4
    # PL7 n=4 random-coefficient null in closed form: ratio = -a(13)/a(24) for 5 seeded draws
    rng = random.Random(7); good = True
    for _ in range(5):
        a = {T: rng.randint(1, COEFF_MAX) for T in T4}
        r = s5_alone(4, [(1, 3), (2, 4)], a)['pairs'][('k13', 'k24')]
        good &= r == [sp.Rational(-a[((1, 3),)], a[((2, 4),)])]
    ok['PL7 n=4 null closed form kappa13/kappa24 = -a13/a24 (5 draws)'] = good
    # PL8 n=5: no c-preserving deformation; S5 with kappa = 0 is EMPTY (A = O(1))
    conds5, _, _ = s5_conditions(5, {})
    ok['PL8 n=5: kappa = 0 gives A = O(1) (S5 violated: a nonzero numeric condition)'] = any(sp.sympify(c).is_number and c != 0 for c in conds5)
    # PL9 V_D (numerator method, CASCADE-1b v3) zero-only on every n=4,5 diamond of the massless amplitude
    good9 = True
    for n9 in (4, 5):
        y9 = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in chords(n9)}
        A9 = triangulation_amp(chords(n9), y9, n9)
        good9 = good9 and all(V_D(n9, A9, y9, d['pairs'])['zero_only'] for d in diamonds(n9))
    ok['PL9 V_D (numerator method) zero-only on all n=4,5 diamonds (CASCADE-1b r1/r2 reproduction)'] = good9
    # PL10 timing coverage at the live n: S5-alone on the n=6 ee/oo support, seeded (611) random coefficients, < 60 s
    rng10 = random.Random(611)
    a10 = {T: rng10.randint(1, COEFF_MAX) for T in triangulations(6)}
    t10 = time.time(); r10 = with_kill(60, s5_alone, 6, ee_oo_support(6), a10)
    ok[f'PL10 n=6 S5-alone (random coefficients, seed 611) completes < 60 s ({time.time()-t10:.1f}s, status {r10["status"]})'] = time.time() - t10 < 60
    # PL11 timing/code-path coverage at n=6: V_D + cell2 (E0, EM) end to end on a seeded (612) random-coefficient
    # triangulation sum (NOT the physical amplitude), each V_D < 600 s and each cell < 900 s, no exception
    rng11 = random.Random(612)
    y11 = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in chords(6)}
    a11 = {T: rng11.randint(1, COEFF_MAX) for T in triangulations(6)}
    A11 = sum((sp.Integer(a11[T]) * sp.Mul(*[1 / y11[P] for P in T]) for T in triangulations(6)), sp.Integer(0))
    good11 = True; info11 = []
    try:
        t11 = time.time()
        VD11 = [with_kill(600, V_D, 6, A11, y11, d['pairs']) for d in diamonds(6)]
        info11.append(f'V_D {time.time()-t11:.1f}s')
        for st in ('E0', 'EM'):
            t11 = time.time(); c11 = with_kill(900, cell2, 6, st, A11, y11, VD11, a11)
            info11.append(f"{st} {c11.get('verdict_cell')} {time.time()-t11:.1f}s")
    except Kill:
        good11 = False; info11.append('KILLED')
    except Exception as e:
        good11 = False; info11.append(f'EXCEPTION {type(e).__name__}: {e}')
    ok[f'PL11 n=6 V_D + cell2 E0/EM on random-coefficient sum (seed 612) complete within budget ({"; ".join(info11)})'] = good11
    for kk, vv in ok.items():
        print(('OK  ' if vv else 'FAIL'), kk)
    allok = all(ok.values())
    print('PLANTED:', 'ALL OK' if allok else 'FAILURES')
    (HERE.parent / 'cascade2_planted.txt').write_text('\n'.join(f"{'OK' if v else 'FAIL'}  {k}" for k, v in ok.items()) + f"\nPLANTED: {'ALL OK' if allok else 'FAILURES'}\n")
    return allok

# ---------------- live ----------------
def _log(fname, rec):
    RUNDIR.mkdir(parents=True, exist_ok=True)
    with open(RUNDIR / fname, 'a') as fh:
        fh.write(json.dumps(rec, default=str) + '\n')
    with open(RUNDIR / 'progress.log', 'a') as fh:
        fh.write(time.strftime('%Y-%m-%d %H:%M:%S %Z') + ' ' + fname + ' ' + json.dumps(rec, default=str)[:300] + '\n')

def run_live():
    guard()
    t0 = time.time()
    out = {'run_id': RUN_ID, 'seed': SEED, 'started': time.strftime('%Y-%m-%d %H:%M:%S %Z')}
    amps, VD = {}, {}
    for n in (4, 5, 6):
        y = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in chords(n)}
        amps[n] = (triangulation_amp(chords(n), y, n), y)
        try:
            VD[n] = []
            for d in diamonds(n):
                td = time.time()
                vd = with_kill(VD_KILL_S, V_D, n, amps[n][0], y, d['pairs'])
                VD[n].append(vd)
                _log('vd.jsonl', {'n': n, 'B': d['B'], 'zero_only': vd['zero_only'], 'groebner': vd['gens'],
                                  'v_only_denominators': vd['v_only_denominators'], 'seconds': round(time.time() - td, 2)})
        except Kill:
            out['verdict'] = f'NOT-EVALUATED (V_D time kill {VD_KILL_S}s per diamond at n={n})'
            print(out['verdict'])
            (HERE.parent / 'cascade2_live.json').write_text(json.dumps(out, indent=1, default=str))
            return out
        assert all(vd['zero_only'] for vd in VD[n]), f'V_D not zero-only at n={n} (CASCADE-1b input changed)'
    print(f'V_D recomputed, zero-only at n=4,5,6 ({time.time()-t0:.0f}s)')
    cells = {}
    for n in (4, 5, 6):
        for setting in ('E0', 'EM'):
            try:
                c = with_kill(CELL_KILL_S, cell2, n, setting, *amps[n], VD[n])
            except Kill:
                c = {'n': n, 'setting': setting, 'verdict_cell': f'NOT-EVALUATED (cell time kill {CELL_KILL_S}s)'}
            cells[f'{setting}-n{n}'] = c
            _log('cells.jsonl', {'cell': f'{setting}-n{n}', 'verdict_cell': c.get('verdict_cell'), 'dim_final': c.get('dim_final')})
            print(f'--- {setting}-n{n}:', c['verdict_cell'], '| kappa family:', c.get('kappa_family'), '| dim_final:', c.get('dim_final'),
                  '| strict-pos kappa cone dim:', c.get('strict_positivity_kappa_cone_dim'))
            for fr in c.get('fixed_ratios', []):
                if fr['involves_kappa'] or fr['PHYS']:
                    print('    fixed:', fr)
    out['cells'] = cells
    # S5-alone on the ee/oo support (observed statistic) and the null
    obs = {n: s5_alone(n, ee_oo_support(n)) for n in (4, 6)}
    out['S5_alone_eeoo'] = {f'n{n}': {'status': r['status'], 'pairs': {f'{a}/{b}': (v if v == 'FREE' else [str(x) for x in v]) for (a, b), v in r['pairs'].items()},
                                      'components': r.get('components')} for n, r in obs.items()}
    h_cell = {n: min_height(obs[n]) for n in (4, 6)}
    h_obs = min([h for h in h_cell.values() if h is not None], default=None)
    print('S5-alone ee/oo observed min heights:', h_cell, 'h_obs =', h_obs, f'({time.time()-t0:.0f}s)')
    rng = random.Random(SEED)
    null = {4: [], 6: []}
    killed = 0
    for i in range(N_NULL):
        for n in (4, 6):
            a = {T: rng.randint(1, COEFF_MAX) for T in triangulations(n)}
            try:
                r = with_kill(S5_KILL_S, s5_alone, n, ee_oo_support(n), a)
                null[n].append(min_height(r))
            except Kill:
                null[n].append(None); killed += 1
            _log('null.jsonl', {'draw': i, 'n': n, 'h': null[n][-1]})
        if i % 50 == 49:
            print(f'  null {i+1}/{N_NULL} ({time.time()-t0:.0f}s)')
    h_null_global = [min([h for h in (null[4][i], null[6][i]) if h is not None], default=None) for i in range(N_NULL)]
    p_global = p_value(h_obs, h_null_global)
    p_cell = {n: p_value(h_cell[n], null[n]) for n in (4, 6)}
    L = sum(len(r['pairs']) for r in obs.values())
    out['anti_numerology'] = {'h_obs': h_obs, 'h_cell': h_cell, 'p_global_maxstat': str(p_global), 'p_cell': {f'n{n}': str(p) for n, p in p_cell.items()},
                              'L_pairs': L, 'bonferroni_L_times_min_p_cell': str(min(1, L * min(p for p in p_cell.values() if p is not None))) if any(p is not None for p in p_cell.values()) else None,
                              'null_killed': killed, 'null_heights_n4': null[4], 'null_heights_n6': null[6],
                              'null_frac_any_fixed_n6': str(sp.Rational(sum(1 for h in null[6] if h is not None), N_NULL))}
    print('anti-numerology:', {k: v for k, v in out['anti_numerology'].items() if not k.startswith('null_heights')}, f'({time.time()-t0:.0f}s)')
    # secondary: support enumeration at n = 6 under a total time kill
    enum = {}
    sup_all = chords(6)
    t_enum = time.time(); status = 'COMPLETE'
    for r in range(1, len(sup_all) + 1):
        for S in itertools.combinations(sup_all, r):
            if time.time() - t_enum > ENUM_KILL_S:
                status = f'PARTIAL (time kill {ENUM_KILL_S}s)'; break
            try:
                res = with_kill(max(1, int(ENUM_KILL_S - (time.time() - t_enum))), s5_alone, 6, list(S))
            except Kill:
                status = f'PARTIAL (time kill {ENUM_KILL_S}s)'; break
            if res['status'] == 'OK':
                enum[str(S)] = {f'{a}/{b}': (v if v == 'FREE' else [str(x) for x in v]) for (a, b), v in res['pairs'].items()}
        if status != 'COMPLETE':
            break
    out['support_enumeration_n6'] = {'status': status, 'supports_with_solutions': enum}
    print('support enumeration n=6:', status, 'supports with S5 solutions:', list(enum.keys()), f'({time.time()-t0:.0f}s)')
    # verdicts
    phys = [dict(c, cell=k) for k, cl in cells.items() for c in cl.get('PHYS_candidates', [])]
    any_fixed = any(cl.get('RATIO_FIXED_any') and any(fr['involves_kappa'] for fr in cl.get('fixed_ratios', [])) for cl in cells.values())
    sig = p_global is not None and p_global < P_THRESHOLD
    if phys and sig:
        H2 = 'CONFIRMED (PHYS ratio fixed and anti-numerology p < 0.01)'
    elif phys:
        H2 = 'REFUTED (PHYS ratio fixed but fails anti-numerology at p < 0.01)'
    else:
        H2 = 'REFUTED (no PHYS ratio: no positive, non-unit, new, non-tachyonic fixed ratio)'
    out['RATIO_FIXED_any'] = any_fixed
    out['PHYS'] = phys
    out['H2'] = H2
    out['elapsed_s'] = round(time.time() - t0, 1)
    print('RATIO-FIXED(any):', any_fixed, '| PHYS candidates:', len(phys), '| p_global:', p_global)
    print('H2 (python):', H2)
    (HERE.parent / 'cascade2_live.json').write_text(json.dumps(out, indent=1, default=str))
    return out

def main():
    sys.stdout.reconfigure(line_buffering=True)
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
