#!/usr/bin/env python3
"""INT-1 locked checker (prereg/INT-1-chamber-constancy-2026-10-22.md).
Claim: integer invariants of the ABHY kinematic associahedron with mass offsets (X_ij >= m_ij^2) are constant on each
open chamber of the offset arrangement; integers change only on walls.
Classes (declared): I_comb = any function of the labelled face lattice (f-vector, Euler char, facet set, vertex labels);
I_lat = number of lattice points |P cap Z^d| in the basis (X13, X14[, X15]) coordinates (finer walls, see prereg).
Geometry here is computed INDEPENDENTLY of the Lean sign tables: exact Fractions, brute-force vertex enumeration
from the massive inequalities, face lattice as the intersection-closure of facet vertex sets.
Modes: planted | live.  Run id + seed fixed in prereg.
GUARD (METHOD 2026-10-20 hardened pattern, copied from sims/bplc): guard() in EVERY scoring function; no pass flag.
"""
import hashlib, itertools, json, math, random, re, subprocess, sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/INT-1-chamber-constancy-2026-10-22.md'
RUN_ID = 'INT1-2026-10-22-r1'
SEED = 20261022

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
    m = re.search(r'int1_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

# ---------------- ABHY planar variables (eq. 24 of 1711.09102) ----------------
def diagonals(n):
    return [(i, j) for i in range(1, n + 1) for j in range(i + 2, n + 1) if not (i == 1 and j == n)]

def cpairs(n):
    """Non-adjacent pairs 1 <= i < j <= n-1 (ABHY eq. 24 index range)."""
    return [(i, j) for i in range(1, n) for j in range(i + 2, n)]

def planar_forms(n, c):
    """X_ij as affine forms in basis z_k = X_{1,k+3} (k = 0..n-4): dict (i,j) -> (coeffs list, const).
    Recurrence from c_ij = X_ij + X_{i+1,j+1} - X_{i,j+1} - X_{i+1,j}, X_{k,k+1} = X_{1,n} = 0."""
    d = n - 3
    zero = ([Fr(0)] * d, Fr(0))
    X = {}
    def get(i, j):
        if j == i + 1 or (i == 1 and j == n):
            return zero
        return X[(i, j)]
    for k in range(d):
        v = [Fr(0)] * d; v[k] = Fr(1)
        X[(1, k + 3)] = (v, Fr(0))
    for i in range(1, n):
        for j in range(i + 2, n):
            a = get(i, j); b = get(i, j + 1); e = get(i + 1, j)
            coeffs = [b[0][t] + e[0][t] - a[0][t] for t in range(d)]
            const = c[(i, j)] + b[1] + e[1] - a[1]
            new = (coeffs, const)
            key = (i + 1, j + 1)
            if key == (i + 1, i + 2) or key == (1, n):
                continue
            if key in X:
                if X[key] != new:
                    raise ValueError("inconsistent recurrence")
            else:
                X[key] = new
    return {dg: X[dg] for dg in diagonals(n)}

def solve(A, b):
    """Exact Gaussian elimination; returns unique solution or None."""
    m = len(A)
    M = [list(A[r]) + [b[r]] for r in range(m)]
    for col in range(m):
        piv = next((r for r in range(col, m) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(m):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [M[r][t] - f * M[col][t] for t in range(m + 1)]
    return tuple(M[r][m] / M[r][r] for r in range(m))

def rank(vecs):
    M = [list(v) for v in vecs]
    rk = 0
    if not M:
        return 0
    ncol = len(M[0])
    for col in range(ncol):
        piv = next((r for r in range(rk, len(M)) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][col] != 0:
                f = M[r][col] / M[rk][col]
                M[r] = [M[r][t] - f * M[rk][t] for t in range(ncol)]
        rk += 1
    return rk

def polytope(n, c, m2):
    """Facets: X_ij(z) - m2[ij] >= 0. Returns facet list and dict vertex -> frozenset(tight facets)."""
    guard()
    F = planar_forms(n, c)
    facets = diagonals(n)
    d = n - 3
    verts = {}
    for S in itertools.combinations(facets, d):
        A = [F[f][0] for f in S]
        b = [m2.get(f, Fr(0)) - F[f][1] for f in S]
        z = solve(A, b)
        if z is None:
            continue
        sl = {f: sum(F[f][0][t] * z[t] for t in range(d)) + F[f][1] - m2.get(f, Fr(0)) for f in facets}
        if all(v >= 0 for v in sl.values()):
            verts[z] = frozenset(f for f in facets if sl[f] == 0)
    return facets, verts, F

def face_lattice(n, c, m2):
    """Labelled face lattice: frozenset of faces, each face = frozenset of vertex labels (tight sets); with dims."""
    guard()
    facets, verts, _ = polytope(n, c, m2)
    if not verts:
        return {'key': ('empty',), 'f': (0,) * (n - 3), 'nverts': 0}
    lab = {v: verts[v] for v in verts}
    allv = frozenset(lab.values())
    faces = set()
    base = []
    for f in facets:
        Vf = frozenset(lab[v] for v in verts if f in verts[v])
        if Vf:
            base.append(Vf)
    frontier = set(base)
    faces |= frontier
    while frontier:
        new = set()
        for A in frontier:
            for B in base:
                I = A & B
                if I and I not in faces:
                    new.add(I)
        faces |= new
        frontier = new
    faces.discard(allv)
    inv = {lab[v]: v for v in verts}
    def dim(face):
        pts = [inv[t] for t in face]
        p0 = pts[0]
        return rank([[p[k] - p0[k] for k in range(n - 3)] for p in pts[1:]]) if len(pts) > 1 else 0
    fdim = {}
    for face in faces:
        fdim.setdefault(dim(face), 0)
        fdim[dim(face)] += 1
    pdim = rank([[p[k] - list(verts)[0][k] for k in range(n - 3)] for p in verts]) if len(verts) > 1 else 0
    fv = tuple(fdim.get(k, 0) for k in range(n - 3))
    key = (pdim, frozenset(faces), allv)
    return {'key': key, 'f': fv, 'nverts': len(verts), 'pdim': pdim}

def lattice_count(n, c, m2, box=12):
    guard()
    F = planar_forms(n, c)
    d = n - 3
    cnt = 0
    for z in itertools.product(range(-box, box + 1), repeat=d):
        if all(sum(F[f][0][t] * z[t] for t in range(d)) + F[f][1] - m2.get(f, Fr(0)) >= 0 for f in F):
            cnt += 1
    return cnt

def ceff(n, c, m2):
    """Effective constants c'_ij = c_ij - m2_ij - m2_{i+1,j+1} + m2_{i,j+1} + m2_{i+1,j} (m2 of non-diagonals = 0)."""
    guard()
    g = lambda i, j: m2.get((i, j), Fr(0))
    return {(i, j): c[(i, j)] - g(i, j) - g(i + 1, j + 1) + g(i, j + 1) + g(i + 1, j) for (i, j) in cpairs(n)}

def arrangement_forms(n):
    """Derive the wall forms in c-space: slack of every facet at every d-subset intersection point, massless,
    as linear forms in c (evaluated on unit vectors; linearity re-checked on a random point). Up to positive scale."""
    guard()
    cp = cpairs(n)
    d = n - 3
    facets = diagonals(n)
    def slacks(c):
        F = planar_forms(n, c)
        out = {}
        for S in itertools.combinations(facets, d):
            z = solve([F[f][0] for f in S], [-F[f][1] for f in S])
            if z is None:
                continue
            for f in facets:
                out[(S, f)] = sum(F[f][0][t] * z[t] for t in range(d)) + F[f][1]
        return out
    units = []
    for k in range(len(cp)):
        units.append(slacks({p: Fr(int(t == k)) for t, p in enumerate(cp)}))
    rng = random.Random(7)
    cr = {p: Fr(rng.randint(1, 50), rng.randint(1, 9)) for p in cp}
    sr = slacks(cr)
    forms = set()
    for key in units[0]:
        vec = tuple(units[k][key] for k in range(len(cp)))
        if sum(vec[k] * cr[cp[k]] for k in range(len(cp))) != sr[key]:
            raise ValueError("slack not linear in c")
        if any(vec):
            g = next(x for x in vec if x != 0)
            forms.add(tuple(x / abs(g) for x in vec))
    canon = set()
    for v in forms:
        neg = tuple(-x for x in v)
        canon.add(max(v, neg))
    return cp, sorted(canon)

def chamber_key(forms, cp, ce):
    guard()
    def sgn(x):
        return (x > 0) - (x < 0)
    return tuple(sgn(sum(v[k] * ce[cp[k]] for k in range(len(cp)))) for v in forms)

def rfr(rng, lo, hi, den=12):
    """Random rational in [lo, hi] with denominator <= den; strictly positive when lo > 0."""
    q = rng.randint(1, den)
    a = math.ceil(Fr(lo) * q)
    if lo > 0:
        a = max(a, 1)
    return Fr(rng.randint(a, math.floor(Fr(hi) * q)), q)

# ---------------- tests ----------------
def chamber_constancy(samples, inv):
    """samples: list of (chamber key, invariant value). Returns list of keys with >1 value."""
    guard()
    by = {}
    for k, v in samples:
        by.setdefault(k, set()).add(v)
    return [k for k, vs in by.items() if len(vs) > 1], len(by)

def run_planted():
    guard()
    out = {}
    c5 = lambda a, b, e: {(1, 3): Fr(a), (1, 4): Fr(b), (2, 4): Fr(e)}
    r = face_lattice(5, c5(1, 1, 1), {}); out['P1a_pentagon_c111'] = (r['f'], r['f'] == (5, 5))
    m = {(1, 3): Fr(1, 2), (1, 4): Fr(1, 3), (3, 5): Fr(1, 5)}
    ce = ceff(5, c5(2, 3, 5), m)
    r = face_lattice(5, c5(2, 3, 5), m); out['P1b_pentagon_massive'] = (r['f'], str(ce), r['f'] == (5, 5) and all(v > 0 for v in ce.values()))
    m = {(3, 5): Fr(1)}
    ce = ceff(5, c5(1, 1, 1), m)
    facets, verts, _ = polytope(5, c5(1, 1, 1), m)
    big = [sorted(t) for t in verts.values() if len(t) == 3]
    r = face_lattice(5, c5(1, 1, 1), m)
    out['P2a_merging_wall_m35sq=1'] = (r['f'], str(ce), big, r['f'] == (4, 4) and ce[(2, 4)] == 0 and big == [[(2, 4), (2, 5), (3, 5)]])
    m = {(3, 5): Fr(3, 2)}
    facets, verts, _ = polytope(5, c5(1, 1, 1), m)
    used = set().union(*verts.values())
    r = face_lattice(5, c5(1, 1, 1), m)
    out['P2b_beyond_wall_m35sq=3/2'] = (r['f'], sorted(set(facets) - used), r['f'] == (4, 4) and sorted(set(facets) - used) == [(2, 5)])
    out['P4_n6_c1'] = None
    c6 = {p: Fr(1) for p in cpairs(6)}
    r = face_lattice(6, c6, {}); out['P4_n6_c1'] = (r['f'], r['f'] == (14, 21, 9))
    cp, forms = arrangement_forms(5)
    expect = {(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 1, 1)}
    out['P5_forms_n5'] = ([tuple(str(x) for x in f) for f in forms], set(forms) == expect)
    out['P7_lattice_c111'] = (lattice_count(5, c5(1, 1, 1), {}), lattice_count(5, c5(1, 1, 1), {}) == 8)
    # P3 broken detector: floor(4 c13') must be flagged non-constant on the positive chamber; f-vector must not
    rng = random.Random(SEED + 3)
    sa, sb = [], []
    for _ in range(200):
        c = c5(rfr(rng, Fr(1, 12), 3), rfr(rng, Fr(1, 12), 3), rfr(rng, Fr(1, 12), 3))
        k = chamber_key(forms, cp, c)
        sa.append((k, int((4 * c[(1, 3)]).__floor__())))
        sb.append((k, face_lattice(5, c, {})['f']))
    bad_a, _ = chamber_constancy(sa, None); bad_b, _ = chamber_constancy(sb, None)
    out['P3_broken_detector'] = (len(bad_a), len(bad_b), len(bad_a) > 0 and len(bad_b) == 0)
    ok = all(v[-1] for v in out.values())
    return out, ok

def run_live():
    guard()
    rng = random.Random(SEED)
    res = {'run_id': RUN_ID, 'seed': SEED}
    c5 = lambda a, b, e: {(1, 3): a, (1, 4): b, (2, 4): e}
    cp5, forms5 = arrangement_forms(5)
    # S1: n=5 with mass offsets
    S, data = 4000, []
    for s in range(S):
        c = c5(rfr(rng, -2, 3), rfr(rng, -2, 3), rfr(rng, -2, 3))
        m2 = {} if s % 2 == 0 else {dg: rfr(rng, 0, Fr(3, 2)) for dg in diagonals(5)}
        ce = ceff(5, c, m2)
        fl = face_lattice(5, c, m2)
        fl0 = face_lattice(5, ce, {})
        data.append((c, m2, ce, fl, fl0))
    shift_ok = sum(1 for (_, _, _, fl, fl0) in data if fl['key'] == fl0['key'])
    keyed = [(chamber_key(forms5, cp5, ce), fl['key']) for (_, _, ce, fl, _) in data]
    bad_lab, nch = chamber_constancy(keyed, None)
    keyed_f = [(chamber_key(forms5, cp5, ce), fl['f']) for (_, _, ce, fl, _) in data]
    bad_f, _ = chamber_constancy(keyed_f, None)
    fdist = {}
    for (k, f) in keyed_f:
        fdist.setdefault(str(k), {}).setdefault(str(f), 0)
        fdist[str(k)][str(f)] += 1
    pos = [d for d in data if all(v > 0 for v in d[2].values())]
    res['S1'] = {'samples': S, 'chambers_seen': nch, 'massive_eq_shifted_lattice': f'{shift_ok}/{S}',
                 'chambers_with_nonconstant_labelled_lattice': len(bad_lab), 'chambers_with_nonconstant_fvector': len(bad_f),
                 'positive_chamber_samples': len(pos), 'positive_chamber_fvectors': sorted({str(d[3]['f']) for d in pos}),
                 'fvector_by_chamber': fdist}
    # S1b segments: same-chamber and crossing, in (c, m2)-space (c' is affine in (c, m2))
    def lerp(a, b, t):
        return {k: a.get(k, Fr(0)) * (1 - t) + b.get(k, Fr(0)) * t for k in set(a) | set(b)}
    same_fail = same_n = 0
    cross_fail = cross_n = jumps = roots_total = 0
    idx = list(range(S))
    bych = {}
    for i, (k, _) in enumerate(keyed):
        bych.setdefault(k, []).append(i)
    pairs_same = []
    for k, L in bych.items():
        for _ in range(min(len(L) - 1, 40)):
            pairs_same.append(tuple(rng.sample(L, 2)))
    pairs_same = pairs_same[:1000]
    for (i, j) in pairs_same:
        ci, mi = data[i][0], data[i][1]; cj, mj = data[j][0], data[j][1]
        ref = data[i][3]['key']
        same_n += 1
        for q in range(1, 16):
            t = Fr(q, 16)
            if face_lattice(5, lerp(ci, cj, t), lerp(mi, mj, t))['key'] != ref:
                same_fail += 1; break
    for _ in range(1000):
        i, j = rng.sample(idx, 2)
        ci, mi = data[i][0], data[i][1]; cj, mj = data[j][0], data[j][1]
        cei, cej = data[i][2], data[j][2]
        roots = set()
        for v in forms5:
            a = sum(v[k] * cei[cp5[k]] for k in range(3)); b = sum(v[k] * cej[cp5[k]] for k in range(3))
            if a != b:
                t = a / (a - b)
                if 0 < t < 1:
                    roots.add(t)
        pts = [Fr(0)] + sorted(roots) + [Fr(1)]
        roots_total += len(roots)
        cross_n += 1
        prev = None
        for lo, hi in zip(pts, pts[1:]):
            k1 = face_lattice(5, lerp(ci, cj, lo + (hi - lo) / 3), lerp(mi, mj, lo + (hi - lo) / 3))['key']
            k2 = face_lattice(5, lerp(ci, cj, lo + 2 * (hi - lo) / 3), lerp(mi, mj, lo + 2 * (hi - lo) / 3))['key']
            if k1 != k2:
                cross_fail += 1
            if prev is not None and prev != k1:
                jumps += 1
            prev = k1
    res['S1b'] = {'same_chamber_segments': same_n, 'same_chamber_failures': same_fail,
                  'crossing_segments': cross_n, 'open_interval_failures': cross_fail,
                  'wall_roots': roots_total, 'jumps_across_roots': jumps}
    # S2: lattice-point counts (I_lat) on the positive chamber
    lat = []
    for (c, m2, ce, fl, _) in pos[:600]:
        lat.append((chamber_key(forms5, cp5, ce), lattice_count(5, c, m2, box=8)))
    bad_lat, _ = chamber_constancy(lat, None)
    res['S2'] = {'positive_chamber_samples': len(lat), 'distinct_counts': sorted({v for _, v in lat})[:40],
                 'I_lat_varies_inside_comb_chamber': len(bad_lat) > 0}
    # S2b: I_lat changes only at lattice walls (slack of some facet at some integer point = 0)
    lat_fail = lat_seg = 0
    for _ in range(60):
        i, j = rng.sample(range(len(pos)), 2)
        ci, mi = pos[i][0], pos[i][1]; cj, mj = pos[j][0], pos[j][1]
        Fi, Fj = planar_forms(5, ci), planar_forms(5, cj)
        roots = set()
        for z in itertools.product(range(-8, 9), repeat=2):
            for f in Fi:
                a = sum(Fi[f][0][t] * z[t] for t in range(2)) + Fi[f][1] - mi.get(f, Fr(0))
                b = sum(Fj[f][0][t] * z[t] for t in range(2)) + Fj[f][1] - mj.get(f, Fr(0))
                if a != b:
                    t = a / (a - b)
                    if 0 < t < 1:
                        roots.add(t)
        pts = [Fr(0)] + sorted(roots) + [Fr(1)]
        lat_seg += 1
        for lo, hi in list(zip(pts, pts[1:]))[:30]:
            t1, t2 = lo + (hi - lo) / 3, lo + 2 * (hi - lo) / 3
            if lattice_count(5, lerp(ci, cj, t1), lerp(mi, mj, t1), 8) != lattice_count(5, lerp(ci, cj, t2), lerp(mi, mj, t2), 8):
                lat_fail += 1; break
    res['S2b'] = {'segments': lat_seg, 'lattice_cell_failures': lat_fail}
    # S3: n=6 with mass offsets
    cp6, forms6 = arrangement_forms(6)
    d6 = []
    for s in range(600):
        if s < 300:
            c = {p: rfr(rng, Fr(1, 12), 3) for p in cp6}; m2 = {}
        else:
            c = {p: rfr(rng, -1, 3) for p in cp6}; m2 = {dg: rfr(rng, 0, Fr(1, 2)) for dg in diagonals(6)}
        ce = ceff(6, c, m2)
        fl = face_lattice(6, c, m2)
        d6.append((c, m2, ce, fl))
    k6 = [(chamber_key(forms6, cp6, ce), fl['key']) for (_, _, ce, fl) in d6]
    bad6, nch6 = chamber_constancy(k6, None)
    pos6 = [d for d in d6 if all(v > 0 for v in d[2].values())]
    shift6 = sum(1 for (c, m2, ce, fl) in d6[300:] if face_lattice(6, ce, {})['key'] == fl['key'])
    seg6_fail = 0
    for _ in range(120):
        i, j = rng.sample(range(len(pos6)), 2)
        ci, mi = pos6[i][0], pos6[i][1]; cj, mj = pos6[j][0], pos6[j][1]
        for q in (1, 2, 3):
            t = Fr(q, 4)
            if face_lattice(6, lerp(ci, cj, t), lerp(mi, mj, t))['f'] != (14, 21, 9):
                seg6_fail += 1; break
    fd6 = {}
    for (_, _, ce, fl) in d6:
        fd6[str(fl['f'])] = fd6.get(str(fl['f']), 0) + 1
    res['S3'] = {'samples': 600, 'n_forms': len(forms6), 'chambers_seen': nch6, 'chambers_nonconstant': len(bad6),
                 'positive_samples': len(pos6), 'positive_fvectors': sorted({str(d[3]['f']) for d in pos6}),
                 'massive_eq_shifted': f'{shift6}/300', 'positive_segment_failures': seg6_fail, 'fvector_hist': fd6}
    # S4: integrality -> ratio set
    res['S4'] = {str(N): len({Fr(a, b) for a in range(1, N + 1) for b in range(1, N + 1)}) for N in (5, 10, 20, 40)}
    # S5: level sets project onto many mu = c13'/c14' values (kill if a level with >= 20 samples has < 10 distinct mu)
    levels = {}
    for (c, m2, ce, fl, _) in data:
        if ce[(1, 4)] != 0:
            levels.setdefault(('f', fl['f']), set()).add(ce[(1, 3)] / ce[(1, 4)])
    for (k, v), (c, m2, ce, fl, _) in zip(lat, pos[:600]):
        levels.setdefault(('lat', v), set()).add(ce[(1, 3)] / ce[(1, 4)])
    cnt = {}
    for (c, m2, ce, fl, _) in data:
        cnt[('f', fl['f'])] = cnt.get(('f', fl['f']), 0) + 1
    for (k, v) in lat:
        cnt[('lat', v)] = cnt.get(('lat', v), 0) + 1
    s5 = {str(L): {'n': cnt[L], 'distinct_mu': len(levels.get(L, ())),
                   'mu_min': float(min(levels[L])) if levels.get(L) else None,
                   'mu_max': float(max(levels[L])) if levels.get(L) else None} for L in cnt}
    kill5 = [L for L in cnt if cnt[L] >= 20 and len(levels.get(L, ())) < 10]
    res['S5'] = {'levels': s5, 'kill_levels': [str(L) for L in kill5]}
    # figure data: slice c13' = 1, (c14', c24') grid
    grid = []
    for a in range(-20, 21):
        for b in range(-20, 21):
            ce = c5(Fr(1), Fr(a, 10), Fr(b, 10))
            grid.append((a / 10, b / 10, list(face_lattice(5, ce, {})['f'])))
    res['figure_grid_c13eq1'] = grid
    kill = bool(bad_lab or bad_f or same_fail or cross_fail or bad6 or seg6_fail or lat_fail or kill5
                or shift_ok != S or shift6 != 300)
    res['verdict'] = 'KILL (P1 REOPENED)' if kill else 'PASS (CHAMBER-CONSTANT)'
    return res

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'planted'
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches; run {RUN_ID} seed {SEED}")
    out, ok = run_planted()
    print(json.dumps({k: str(v) for k, v in out.items()}, indent=1))
    print('PLANTED', 'PASS' if ok else 'FAIL -> ILL-DEFINED')
    if mode == 'live':
        if not ok:
            sys.exit('planted failed: ILL-DEFINED, live not run')
        res = run_live()
        Path(HERE.with_name('int1_live.json')).write_text(json.dumps(res, indent=1, default=str))
        print(json.dumps({k: v for k, v in res.items() if k != 'figure_grid_c13eq1'}, indent=1, default=str))
