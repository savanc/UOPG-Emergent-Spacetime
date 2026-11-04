#!/usr/bin/env python3
"""CASCADE-1 locked checker (prereg/CASCADE-1-parameter-cascade-2026-10-23.md).
Constraint cascade for mass-shifted Tr phi^3 at n = 4, 5 (lit review notes/LIT-REVIEW-2026-10-22-cosmic-nine-loops-ai-physics.md,
CASCADE-1 spec).  Ansatz A = N(y) / prod_chords y_ch,  y_ab = X_ab - mu_ab,  deg N <= D_n = (n-3)(n-2)/2 (fixed in prereg).
Stages (fixed order):  S0 ansatz | S1 poles/adjacency | S2 factorisation | S3 hidden zeros | S4 positivity.
Held-out family (never imposed): near-zero splits (2312.16282 eqs. 3.3/3.5 and cyclic images), as a mass-agnostic
rank-1 separability test on the final family.
Settings: E0 (external legs massless, Theta = chord offsets mu) and EM (Theta = (mu, external m_i^2)).
Count K_s = dim Theta_s + f_s,  f_s = projective dimension of the amplitude family at a generic point of Theta_s.
Exact arithmetic: sympy rationals; LP only proposes, every LP answer is re-verified exactly with Fractions.
Modes: planted | live | sens (pre-declared secondary sensitivity at D_n + 1).  Run id + seed fixed in prereg.
GUARD (METHOD 2026-10-20 hardened pattern, copied from sims/int1 / sims/leancert1): guard() in EVERY scoring function.
"""
import hashlib, itertools, json, random, re, subprocess, sys, time
from fractions import Fraction as Fr
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/CASCADE-1-parameter-cascade-2026-10-23.md'
RUN_ID = 'CASCADE1-2026-10-23-r1'
SEED = 20261023

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
    m = re.search(r'cascade1_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------------- kinematics (2312.16282 sec. 2, CITED) ----------------
def chords(n):
    return [(a, b) for a in range(1, n + 1) for b in range(a + 2, n + 1) if (a, b) != (1, n)]

def crosses(P, Q):
    (a, b), (c, d) = P, Q
    return a < c < b < d or c < a < d < b

class Kin:
    """symbols: X_ab (chords), mu_ab (chord offsets), m_i (external p_i^2). setting E0: m_i = 0."""
    def __init__(self, n, setting):
        self.n, self.setting = n, setting
        self.ch = chords(n)
        self.X = {P: sp.Symbol(f'X{P[0]}{P[1]}') for P in self.ch}
        self.mu = {P: sp.Symbol(f'mu{P[0]}{P[1]}') for P in self.ch}
        self.m = {i: (sp.Symbol(f'm{i}') if setting == 'EM' else sp.Integer(0)) for i in range(1, n + 1)}
        self.theta = [self.mu[P] for P in self.ch] + ([self.m[i] for i in range(1, n + 1)] if setting == 'EM' else [])

    def Xv(self, i, j):
        """X_{i,j} with cyclic labels; X_{i,i+1} = p_i^2 = m_i; X_{1,n} = m_n; X_{i,i} = 0."""
        n = self.n
        i, j = (i - 1) % n + 1, (j - 1) % n + 1
        if i == j:
            return sp.Integer(0)
        a, b = sorted((i, j))
        if b - a == 1:
            return self.m[a]
        if (a, b) == (1, n):
            return self.m[n]
        return self.X[(a, b)]

    def c(self, i, j):
        """c_{i,j} = X_{i,j} + X_{i+1,j+1} - X_{i,j+1} - X_{i+1,j}  (2312.16282 eq. 2.4)."""
        return sp.expand(self.Xv(i, j) + self.Xv(i + 1, j + 1) - self.Xv(i, j + 1) - self.Xv(i + 1, j))

    def nonadj(self, i):
        n = self.n
        return [j for j in range(1, n + 1) if (j - i) % n not in (0, 1, n - 1)]

    def zero_loci(self):
        """Z_i = {c_{i,j} = 0 for all j non-adjacent to i}; deduplicated (n(n-3)/2 distinct)."""
        out, seen = [], set()
        for i in range(1, self.n + 1):
            pairs = tuple(sorted(tuple(sorted((i, j))) for j in self.nonadj(i)))
            if pairs not in seen:
                seen.add(pairs)
                out.append((i, pairs, [self.c(*p) for p in pairs]))
        return out

def lin_solve_rows(eqs, unknowns):
    """nullspace of the homogeneous linear system eqs (expressions linear in unknowns), exact."""
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
    return [cf for cf in sp.Poly(sp.expand(num), *gens).coeffs() if cf != 0]

# ---------------- stages 0-2 (Theta-independent in y variables) ----------------
def triangulation_amp(chs, yv, k):
    """sum over sets of k-3 pairwise non-crossing chords of prod 1/y (the CITED planar cubic form)."""
    tot = sp.Integer(0)
    for S in itertools.combinations(chs, k - 3):
        if all(not crosses(P, Q) for P, Q in itertools.combinations(S, 2)):
            tot += sp.Mul(*[1 / yv[P] for P in S])
    return tot

def subpolygons(n, P):
    a, b = P
    s1 = list(range(a, b + 1))
    s2 = list(range(b, n + 1)) + list(range(1, a + 1))
    return s1, s2

def sub_chords(n, verts):
    """full-polygon chords with both ends among verts and non-adjacent inside the sub-polygon (cyclic order kept)."""
    k = len(verts); out = []
    for x, y in itertools.combinations(range(k), 2):
        if (y - x) % k in (1, k - 1):
            continue
        out.append((verts[x], verts[y]))
    return out

def canon(P):
    return tuple(sorted(P))

def run_stages012(n, D, lower=None):
    """returns dict with f0,f1,f2, the stage-2 basis (in y), the unique amplitude (if f2 = 0) and counts.
    lower: dict k -> function(list of 2 y-symbols for a 4-gon in cyclic order (v1v3, v2v4)) -> expr (from the n=4 cascade)."""
    guard()
    ch = chords(n)
    y = {P: sp.Symbol(f'y{P[0]}{P[1]}') for P in ch}
    gens = [y[P] for P in ch]
    monos = sorted(sp.itermonomials(gens, D), key=sp.default_sort_key)
    a = sp.symbols(f'a0:{len(monos)}')
    N = sum(ai * mo for ai, mo in zip(a, monos))
    den = sp.Mul(*gens)
    res = {'n': n, 'D': D, 'n_monomials': len(monos), 'f0': len(monos) - 1}
    # S1: no simultaneous pole on crossing chords
    eq1 = []
    for P, Q in itertools.combinations(ch, 2):
        if crosses(P, Q):
            rest = [y[R] for R in ch if R not in (P, Q)]
            eq1 += poly_coeff_eqs(N.subs({y[P]: 0, y[Q]: 0}), rest) if rest else [sp.expand(N.subs({y[P]: 0, y[Q]: 0}))]
    ns1 = lin_solve_rows(eq1, list(a))
    res['f1'] = len(ns1) - 1
    res['S1_equations'] = len(eq1)
    # S2: Res_{y_P=0} A = kappa * A_L * A_R
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
        expr = N.subs(y[P], 0) - kap * sp.Mul(*others) * prod
        expr = sp.cancel(sp.together(expr))
        eq2 += poly_coeff_eqs(expr, others)
    ns2 = lin_solve_rows(eq2, list(a) + [kap])
    res['f2'] = len(ns2) - 1
    res['kappa_nonzero_in_S2'] = any(v[-1] != 0 for v in ns2)
    basis = []
    for v in ns2:
        Nv = sum(v[i] * monos[i] for i in range(len(monos)))
        basis.append((sp.cancel(Nv / den), v[-1]))
    res['_basis'] = basis
    res['_y'] = y
    if len(ns2) == 1:
        A, k = basis[0]
        A = sp.cancel(A / k) if k != 0 else A
        res['_A'] = A
        res['A_equals_triangulation_sum'] = sp.simplify(A - triangulation_amp(ch, y, n)) == 0
    return res

# ---------------- stage 3 (hidden zeros) ----------------
def zero_conditions(kin, A_y, y):
    """polynomial conditions on Theta for A(X - mu) to vanish identically on every hidden-zero locus Z_i."""
    guard()
    sub = {y[P]: kin.X[P] - kin.mu[P] for P in kin.ch}
    A = A_y.subs(sub)
    conds, per = [], []
    Xs = [kin.X[P] for P in kin.ch]
    for i, pairs, cs in kin.zero_loci():
        sol = sp.solve(cs, Xs[::-1][:len(cs)] if False else _pick(cs, Xs), dict=True)
        assert len(sol) == 1
        free = [x for x in Xs if x not in sol[0]]
        expr = sp.together(A.subs(sol[0]))
        eqs = poly_coeff_eqs(expr, free)
        per.append({'i': i, 'pairs': pairs, 'n_coeff_conditions': len(eqs)})
        conds += eqs
    return conds, per

def _pick(cs, Xs):
    """choose |cs| X variables (last-first) with an invertible coefficient block."""
    for S in itertools.combinations(Xs[::-1], len(cs)):
        J = sp.Matrix([[sp.diff(c, x) for x in S] for c in cs])
        if J.det() != 0:
            return list(S)
    raise AssertionError('locus not solvable')

def variety(conds, theta):
    """reduced Groebner basis; if linear, returns (dim, basis matrix of the solution subspace, relations)."""
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

# ---------------- stage 4 (positivity: kappa > 0, all mu >= 0, all m_i >= 0) ----------------
def cone_dim(B):
    """exact dimension of {B t : B t >= 0} (B rational, columns = basis of Theta_3).
    For each coordinate: either an exact witness t with (Bt)_j > 0, Bt >= 0, or an exact Farkas certificate
    lam >= 0, lam_j > 0, lam^T B = 0 proving (Bt)_j = 0 on the cone.  LP (scipy) only proposes."""
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
        # propose witness: max (Bt)_j s.t. Bt >= 0, Bt <= 1
        r = linprog(-Bf[j], A_ub=np.vstack([-Bf, Bf]), b_ub=np.concatenate([np.zeros(m), np.ones(m)]), bounds=[(None, None)] * k, method='highs')
        ok = False
        if r.status == 0 and -r.fun > 1e-9:
            t = [Fr(x).limit_denominator(10**6) for x in r.x]
            v = [sum(Bq[i][l] * t[l] for l in range(k)) for i in range(m)]
            if all(x >= 0 for x in v) and v[j] > 0:
                witnesses[j] = [str(x) for x in t]; ok = True
            else:
                # snap: try scaling-free repair using exact LP on rationals is out of scope -> mark unresolved
                pass
        if not ok:
            # Farkas: lam >= 0, lam_j = 1, B^T lam = 0
            r2 = linprog(np.zeros(m), A_eq=Bf.T, b_eq=np.zeros(k), bounds=[(0, None)] * m,
                         A_ub=None, b_ub=None, method='highs', options={}) if False else \
                 linprog(np.zeros(m), A_eq=np.vstack([Bf.T, np.eye(m)[j]]), b_eq=np.concatenate([np.zeros(k), [1.0]]), bounds=[(0, None)] * m, method='highs')
            if r2.status != 0:
                raise AssertionError(f'cone_dim: coordinate {j} unresolved (no witness, no Farkas)')
            lam = [Fr(x).limit_denominator(10**6) for x in r2.x]
            chk = [sum(lam[i] * Bq[i][l] for i in range(m)) for l in range(k)]
            if not (all(x >= 0 for x in lam) and lam[j] > 0 and all(x == 0 for x in chk)):
                raise AssertionError(f'cone_dim: Farkas certificate for {j} failed exact check')
            farkas[j] = [str(x) for x in lam]; forced.append(j)
    # dimension: subspace of Theta_3 with forced coordinates zero; relative interior = sum of witnesses (exact)
    if forced:
        Mf = sp.Matrix([[B[j, l] for l in range(k)] for j in forced])
        d = k - Mf.rank()
    else:
        d = k
    return {'dim': d, 'forced_zero': forced, 'witness_t': witnesses, 'farkas_lambda': farkas}

# ---------------- held-out: near-zero splits (2312.16282 eqs. 3.3, 3.5 + cyclic images) ----------------
SPLIT_TEMPLATES = [  # (c_off pair, group1, group2, eliminated)  for i = 1, labels rotate by i-1
    ((1, 4), [(1, 3), (2, 5)], [(1, 4), (3, 5)], (2, 4)),   # eq. 3.3: c14 = 0 -> (1/X13+1/X25)(1/X14+1/X35)
    ((1, 3), [(1, 3), (2, 5)], [(2, 4), (3, 5)], (1, 4)),   # eq. 3.5: c13 = 0 -> (1/X13+1/X25)(1/X24+1/X35)
]

def rot(P, k, n):
    return canon(((P[0] - 1 + k) % n + 1, (P[1] - 1 + k) % n + 1))

def split_test(kin, A_X, cpair, g1, g2, elim):
    """A restricted to {c_cpair = 0} is a product F(g1) G(g2)  <=>  A(x,y)A(x',y') = A(x,y')A(x',y)."""
    guard()
    X = kin.X
    sol = sp.solve([kin.c(*cpair)], [X[elim]], dict=True)[0]
    Ar = sp.together(A_X.subs(sol))
    allv = [X[P] for P in g1 + g2]
    assert set(allv) | {X[elim]} == set(X.values()), 'split coordinates incomplete'
    p = {v: sp.Symbol(str(v) + 'p') for v in allv}
    def ev(use1p, use2p):
        s = {}
        for P in g1:
            s[X[P]] = p[X[P]] if use1p else X[P]
        for P in g2:
            s[X[P]] = p[X[P]] if use2p else X[P]
        return Ar.subs(s, simultaneous=True)
    expr = ev(False, False) * ev(True, True) - ev(False, True) * ev(True, False)
    return sp.expand(sp.numer(sp.together(expr))) == 0

def all_splits(kin, A_X):
    guard()
    out = []
    for k in range(kin.n):
        for cp, g1, g2, el in SPLIT_TEMPLATES:
            cpr = rot(cp, k, kin.n)
            out.append({'rotation': k, 'c_zero': cpr, 'ok': split_test(kin, A_X, cpr, [rot(P, k, kin.n) for P in g1],
                                                                       [rot(P, k, kin.n) for P in g2], rot(el, k, kin.n))})
    return out

# ---------------- cascade driver ----------------
def cascade(n, setting, D, s012, extra_stage=None):
    guard()
    kin = Kin(n, setting)
    A_y, y = s012.get('_A'), s012['_y']
    rows = []
    T = len(kin.theta)
    rows.append({'stage': 'S0 ansatz', 'dimTheta': T, 'f': s012['f0']})
    rows.append({'stage': 'S1 poles/adjacency', 'dimTheta': T, 'f': s012['f1']})
    rows.append({'stage': 'S2 factorisation', 'dimTheta': T, 'f': s012['f2']})
    out = {'n': n, 'setting': setting, 'D': D, 'theta': [str(t) for t in kin.theta], 'N_off': len(kin.ch)}
    if A_y is None:
        out['NOT_POSED'] = f"stage-2 family not a single amplitude (f2 = {s012['f2']}); stage 3 handled only in sens mode"
        out['rows'] = rows
        return out
    conds = []
    if extra_stage is not None:
        conds += extra_stage(kin)
        v = variety(conds, kin.theta)
        rows.append({'stage': 'PLANTED extra stage', 'dimTheta': v['dim'], 'f': 0})
    zc, per = zero_conditions(kin, A_y, y)
    conds += zc
    v3 = variety(conds, kin.theta)
    rows.append({'stage': 'S3 hidden zeros', 'dimTheta': v3['dim'], 'f': 0})
    out['S3'] = {'per_locus': per, 'relations': v3['relations'], 'linear': v3['linear']}
    if not v3['linear']:
        out['S3']['components'] = v3['components']
        out['rows'] = rows
        out['S4'] = 'NOT EVALUATED (nonlinear Theta_3; prereg sec. 6: K_final := max component dim of Theta_3)'
        for r in rows:
            r['K'] = r['dimTheta'] + r['f']
        K = rows[-1]['K']
        out['K_final'] = K
        out['outcome'] = 'MATCH' if K == len(kin.ch) else ('BELOW' if K < len(kin.ch) else 'ABOVE')
        out['ratio'] = 'RATIOS-FREE' if K >= 2 else ('RATIO-FIXED' if K == 1 else 'NO-MASSES-SURVIVE')
        out['heldout_splits'] = 'NOT EVALUATED (nonlinear Theta_3)'
        return out
    B = v3['basis']
    cd = cone_dim(B)
    rows.append({'stage': 'S4 positivity', 'dimTheta': cd['dim'], 'f': 0})
    out['S4'] = {k: v for k, v in cd.items()}
    out['S4']['forced_zero_names'] = [str(kin.theta[j]) for j in cd['forced_zero']]
    for r in rows:
        r['K'] = r['dimTheta'] + r['f']
    out['rows'] = rows
    # final family, parametrised: Theta = B t restricted to forced coordinates = 0
    k = B.shape[1]
    tt = sp.symbols(f't0:{k}') if k else ()
    th = (B * sp.Matrix(tt)) if k else sp.zeros(T, 1)
    if cd['forced_zero']:
        Mf = sp.Matrix([[B[j, l] for l in range(k)] for j in cd['forced_zero']])
        ns = Mf.nullspace()
        Bf = sp.Matrix.hstack(*ns) if ns else sp.zeros(k, 0)
        uu = sp.symbols(f'u0:{Bf.shape[1]}')
        th = B * (Bf * sp.Matrix(uu)) if Bf.shape[1] else sp.zeros(T, 1)
    final = {kin.theta[i]: sp.expand(th[i]) for i in range(T)}
    out['final_family'] = {str(kk): str(vv) for kk, vv in final.items()}
    A_X = A_y.subs({y[P]: kin.X[P] - kin.mu[P] for P in kin.ch}).subs(final)
    out['heldout_splits'] = all_splits(kin, A_X) if n == 5 else 'VACUOUS at n=4 (no proper split: each zero locus has one c)'
    K = rows[-1]['K']
    out['K_final'] = K
    out['outcome'] = 'MATCH' if K == len(kin.ch) else ('BELOW' if K < len(kin.ch) else 'ABOVE')
    dT = rows[-1]['dimTheta']
    out['ratio'] = 'RATIOS-FREE' if dT >= 2 else ('RATIO-FIXED' if dT == 1 else 'NO-MASSES-SURVIVE')
    return out

def strip(d):
    return {k: v for k, v in d.items() if not k.startswith('_')}

# ---------------- planted ----------------
def run_planted():
    guard()
    ok = {}
    # PL1: massless A5 from triangulations == 2312.16282 eq. (3.1), typed independently
    X13, X14, X24, X25, X35 = sp.symbols('X13 X14 X24 X25 X35')
    eq31 = 1/(X13*X14) + 1/(X24*X25) + 1/(X13*X35) + 1/(X14*X24) + 1/(X25*X35)
    k5 = Kin(5, 'E0')
    tri = triangulation_amp(k5.ch, k5.X, 5)
    ok['PL1 triangulation sum = eq.(3.1)'] = sp.simplify(tri - eq31) == 0
    # PL2: massless splits (3.3),(3.5) and all cyclic images hold; a planted non-separable function fails
    sp_ok = all(s['ok'] for s in all_splits(k5, eq31))
    bad = eq31 + 1/(X13*X24)
    sp_bad = split_test(k5, bad, (1, 4), [(1, 3), (2, 5)], [(1, 4), (3, 5)], (2, 4))
    ok['PL2 massless splits hold (10/10); planted non-separable rejected'] = sp_ok and not sp_bad
    # PL3: massless A5 vanishes on every Z_i (CITED sec. 3.1.1); planted A5 + 1/(X13 X14) does not vanish on Z_1
    zs = []
    for i, pairs, cs in k5.zero_loci():
        sol = sp.solve(cs, _pick(cs, list(k5.X.values())), dict=True)[0]
        zs.append(sp.simplify(eq31.subs(sol)) == 0)
    i, pairs, cs = k5.zero_loci()[0]
    sol = sp.solve(cs, _pick(cs, list(k5.X.values())), dict=True)[0]
    nz = sp.simplify((eq31 + 1/(X13*X14)).subs(sol)) != 0
    ok['PL3 zeros: 5 loci, A5 vanishes on all; planted extra term detected'] = len(zs) == 5 and all(zs) and nz
    # PL4: detector power for ratio fixing: E0 n=4 with a planted extra stage mu13 - 2 mu24 = 0
    s4 = run_stages012(4, 1)
    c = cascade(4, 'E0', 1, s4, extra_stage=lambda kin: [kin.mu[(1, 3)] - 2 * kin.mu[(2, 4)]])
    ok['PL4 planted ratio-fixing stage lowers dimTheta 2 -> 1'] = [r['dimTheta'] for r in c['rows']][3] == 1
    # PL5: stage 1 rejects the crossing double pole 1/(y13 y24) (N = const not in S1 space) at n=4, D=1
    ok['PL5 S1 excludes crossing double pole (f1 = 1 at n=4)'] = s4['f1'] == 1 and s4['f0'] == 2
    # PL6: cone dimension with exact certificates
    c1 = cone_dim(sp.Matrix([[1], [-1]]))['dim']   # {(t,-t) >= 0} = {0}
    c2 = cone_dim(sp.Matrix([[1], [1]]))['dim']    # {(t,t) >= 0} : ray
    c3 = cone_dim(sp.Matrix([[1, 0], [0, 1], [1, -1]]))['dim']
    ok['PL6 cone dims (0,1,2)'] = (c1, c2, c3) == (0, 1, 2)
    # PL7: 2312.16282 sec. 7.1 delta-shift (X_oo - delta, X_ee + delta) keeps the n=4 zeros: Y13 = X13 - d, Y24 = X24 + d
    k4 = Kin(4, 'E0'); d = sp.Symbol('d')
    A4 = 1/(k4.X[(1, 3)] - d) + 1/(k4.X[(2, 4)] + d)
    ok['PL7 delta-shift keeps n=4 zero (c13 = X13 + X24 = 0)'] = sp.simplify(A4.subs(k4.X[(2, 4)], -k4.X[(1, 3)])) == 0
    # PL8: variety() reports nonlinear components (detector for a non-linear Theta_3)
    a_, b_ = sp.symbols('pa pb')
    v = variety([a_ * b_], [a_, b_])
    ok['PL8 nonlinear Theta detected'] = (not v['linear']) and v['dim'] == 1
    for kk, vv in ok.items():
        print(('OK  ' if vv else 'FAIL'), kk)
    allok = all(ok.values())
    print('PLANTED:', 'ALL OK' if allok else 'FAILURES')
    (HERE.parent / 'cascade1_planted.txt').write_text('\n'.join(f"{'OK' if v else 'FAIL'}  {k}" for k, v in ok.items()) + f"\nPLANTED: {'ALL OK' if allok else 'FAILURES'}\n")
    return allok

# ---------------- live ----------------
def run_live():
    guard()
    t0 = time.time()
    out = {'run_id': RUN_ID, 'seed': SEED, 'cells': {}}
    s4 = run_stages012(4, 1)
    out['stages012_n4'] = strip(s4)
    if s4.get('_A') is None or not s4.get('A_equals_triangulation_sum'):
        out['verdict'] = 'NOT-POSED (n=4 stage-2 does not reproduce massless Tr phi^3)'
        print(out['verdict']); return out
    A4 = s4['_A']; y4 = s4['_y']
    lower = {4: lambda ys: A4.subs({y4[(1, 3)]: ys[0], y4[(2, 4)]: ys[1]}, simultaneous=True)}
    s5 = run_stages012(5, 3, lower=lower)
    out['stages012_n5'] = strip(s5)
    print('stages 0-2:', {k: v for k, v in strip(s4).items()}, {k: v for k, v in strip(s5).items()})
    for n, s in ((4, s4), (5, s5)):
        for setting in ('E0', 'EM'):
            c = cascade(n, setting, s['D'], s)
            out['cells'][f'{setting}-n{n}'] = c
            print(f'--- {setting} n={n}:', json.dumps({k: c[k] for k in ('rows', 'K_final', 'outcome', 'ratio') if k in c}, default=str))
            print('    S3 relations:', c.get('S3', {}).get('relations'))
            print('    final family:', c.get('final_family'))
            hs = c.get('heldout_splits')
            print('    held-out splits:', hs if isinstance(hs, str) else f"{sum(h['ok'] for h in hs)}/{len(hs)} OK")
    cells = out['cells']
    heldout_fail = any(isinstance(c.get('heldout_splits'), list) and not all(h['ok'] for h in c['heldout_splits']) for c in cells.values())
    outcomes = {k: c.get('outcome', 'NOT-POSED') for k, c in cells.items()}
    if heldout_fail:
        verdict = 'FAIL (held-out split violated)'
    elif any(v == 'NOT-POSED' for v in outcomes.values()):
        verdict = 'NOT-POSED'
    elif all(v == 'MATCH' for v in outcomes.values()):
        verdict = 'CONFIRMED (K_final = N_off in all four cells)'
    else:
        verdict = 'REFUTED-AS-STATED (cells: ' + ', '.join(f'{k}={v}' for k, v in outcomes.items()) + '); audit required'
    ratio = {k: c.get('ratio') for k, c in cells.items()}
    out['verdict'] = verdict; out['ratio'] = ratio; out['elapsed_s'] = round(time.time() - t0, 1)
    print('VERDICT (python):', verdict)
    print('RATIO:', ratio)
    (HERE.parent / 'cascade1_live.json').write_text(json.dumps(out, indent=1, default=str))
    return out

def run_sens():
    """pre-declared secondary: D_n + 1. Reports f0, f1, f2; if f2 > 0, f3 at 3 seeded random rational points of the
    main-run Theta_3 of each setting (read from cascade1_live.json). Not verdict-bearing."""
    guard()
    rng = random.Random(SEED + 1)
    live = json.loads((HERE.parent / 'cascade1_live.json').read_text())
    out = {'run_id': RUN_ID + '-sens', 'seed': SEED + 1}
    for n, D in ((4, 2), (5, 4)):
        s = run_stages012(n, D)
        out[f'n{n}'] = {k: v for k, v in strip(s).items()}
        if s['f2'] > 0:
            for setting in ('E0', 'EM'):
                kin = Kin(n, setting)
                fam = live['cells'][f'{setting}-n{n}'].get('final_family', {})
                pts = []
                for trial in range(3):
                    syms = sorted({str(x) for v in fam.values() for x in sp.sympify(v).free_symbols})
                    val = {sp.Symbol(u): sp.Rational(rng.randint(1, 50), rng.randint(1, 7)) for u in syms}
                    th = {sp.Symbol(k): sp.sympify(v).subs(val) for k, v in fam.items()}
                    y = s['_y']
                    tvec = sp.symbols(f'b0:{len(s["_basis"])}')
                    A = sum(tv * bv[0] for tv, bv in zip(tvec, s['_basis']))
                    zc, _ = zero_conditions(kin, A, y)
                    zc = [sp.expand(z.subs(th)) for z in zc]
                    zc = [z for z in zc if z != 0]
                    ns = lin_solve_rows(zc, list(tvec)) if zc else [None] * len(tvec)
                    pts.append({'theta': {str(k): str(v) for k, v in th.items()}, 'f3_at_point': len(ns) - 1})
                out[f'n{n}'][f'{setting}_f3_on_main_final_family'] = pts
        print(f'sens n={n} D={D}:', json.dumps(out[f'n{n}'], default=str))
    (HERE.parent / 'cascade1_sens.json').write_text(json.dumps(out, indent=1, default=str))
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    print(f"run {RUN_ID} seed {SEED} mode {mode} ({time.strftime('%Y-%m-%d %H:%M:%S %Z')})")
    if mode == 'planted':
        sys.exit(0 if run_planted() else 1)
    elif mode == 'live':
        run_live()
    elif mode == 'sens':
        run_sens()
    else:
        sys.exit(f"unknown mode {mode}")

if __name__ == '__main__':
    main()
