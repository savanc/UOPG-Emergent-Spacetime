#!/usr/bin/env python3
"""GRADED-POSITROID locked checker (mission rung, charge; continuous-mode own pick 2026-10-22).
Question: does a TORUS-WEIGHT-GRADED positroid object (columns of Gr+(k,15) = the 15 Weyl states of one SM
generation, each carrying its weight w_i in the Cartan torus of SU(3)xSU(2)xU(1): (H3, H8', T3, Y)) give any
anomaly-cancellation condition on the charges BEYOND the anomaly polynomial restricted to the Cartan, and is it
EARNED (not reproduced by rival measures, not a tautology of the input weights)?
Graded moment along a cocharacter z in Q^4:  m_r(z) = E_mu[ (sum_i (z.w_i) x_i)^r ],  mu uniform on the cell polytope.
Trials (prereg):
  G1  uniform cells Delta(k,15), k=1,2,3, + rival cube [0,1]^15: count hypercharge vectors (STRUCT-1 basis, yQ=1,
      p/q with |p|,|q|<=10) with m1 == 0 and m3 == 0 for ALL z (colour/isospin weights fixed by the multiplet table).
      On m1 = 0, m3(z) = kappa * sum_i (z.w_i)^3 (Lean BridgePLCharge.sym_cubic_reduction / GradedPositroid).
  G3  Weyl-group-invariant coordinate cells of Gr+(1,15) (faces of the simplex spanned by unions of W-orbits =
      the 5 multiplets): which proper non-empty unions have vanishing graded m1 and graded cubic tensor for the SM?
  G4  higher graded moments m4, m5 of Delta(2,15) along the Y direction for the SM: vanish? (a vanishing m5 would be
      a non-ACC condition satisfied by the SM).
Rule: WELL-POSED iff all planted OK. G1 REPRODUCES iff N(Delta(2,15)) == N_ACC; EARNED iff REPRODUCES and the
simplex rival N != N_ACC. NEW-CONDITION iff (G3 has a proper union satisfied by the SM) or (G4 m5_SM == 0).
LINK iff EARNED or NEW-CONDITION; otherwise NO-LINK (TAUTOLOGICAL-REPRODUCTION if REPRODUCES).
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main. No pass flag; caches keyed
by origin/main sha only; `git fetch` once per process.
"""
import hashlib, itertools, re, subprocess, sys
from fractions import Fraction as Fr
from math import comb, factorial
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/GRADED-POSITROID-2026-10-22.md'

def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)

_FETCH_DONE = []          # fetch once per process (NOT a pass flag)
_ANC_BY_ORIGIN = {}       # origin/main sha -> (prereg sha, is_ancestor)

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
    m = re.search(r'gpos_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- content: multiplets -> Cartan weight states ----------
COL3 = [(1, 1), (-1, 1), (0, -2)]                 # (H3, H8') = diag(1,-1,0), diag(1,1,-2) on the triplet
COL3B = [(-a, -b) for a, b in COL3]
ISO2 = [Fr(1, 2), Fr(-1, 2)]
# (name, colour states, isospin states, multiplicity check)
MULT = [('Q', COL3, ISO2), ('u', COL3B, [Fr(0)]), ('d', COL3B, [Fr(0)]), ('L', [(0, 0)], ISO2), ('e', [(0, 0)], [Fr(0)])]
SM_Y = {'Q': Fr(1, 6), 'u': Fr(-2, 3), 'd': Fr(1, 3), 'L': Fr(-1, 2), 'e': Fr(1)}

def states(mults, Y):
    """list of (multiplet name, weight vector (H3,H8',T3,Y)) for every Weyl state."""
    guard()
    out = []
    for name, cols, isos in mults:
        for c in cols:
            for t in isos:
                out.append((name, (Fr(c[0]), Fr(c[1]), Fr(t), Fr(Y[name]))))
    return out

def m1_vec(st):
    guard()
    return tuple(sum(w[a] for _, w in st) for a in range(4))

def cubic_tensor(st):
    """all independent components T_abc = sum_i w_ia w_ib w_ic (a<=b<=c)."""
    guard()
    return {abc: sum(w[abc[0]] * w[abc[1]] * w[abc[2]] for _, w in st)
            for abc in itertools.combinations_with_replacement(range(4), 3)}

def power_Y(st, r):
    guard()
    return sum(w[3] ** r for _, w in st)

# ---------- exact moments of the uniform measure on Delta(k,n) = [0,1]^n cap {sum = k} ----------
def _orthant(bs, L, p):
    if L <= 0:
        return Fr(0)
    d = len(bs)
    tot = sum(bs) + p + d
    num = factorial(p)
    for b in bs:
        num *= factorial(b)
    return Fr(L) ** tot * Fr(num, factorial(tot))

def _cubeD(alpha, L, p):
    """int_{[0,1]^d} x^alpha (L - s)_+^p dx (inclusion-exclusion of the upper bounds)."""
    tot = Fr(0)
    d = len(alpha)
    for S in itertools.product((0, 1), repeat=d):
        sign = (-1) ** sum(S)
        Lp = L - sum(S)
        ranges = [range(a + 1) if s else [a] for a, s in zip(alpha, S)]
        for bs in itertools.product(*ranges):
            coef = 1
            for a, s, b in zip(alpha, S, bs):
                if s:
                    coef *= comb(a, b)
            tot += sign * coef * _orthant(bs, Lp, p)
    return tot

def _ih(m, z):
    if z <= 0 or z >= m:
        return Fr(0)
    return sum((-1) ** j * comb(m, j) * Fr(z - j) ** (m - 1) for j in range(m + 1) if z - j > 0) / factorial(m - 1)

_MOM = {}
def slice_moment(alpha, k, n):
    """E[prod x_i^alpha_i] (alpha over d distinct coordinates, all >= 1) on Delta(k,n); needs n - d >= 2."""
    guard()
    alpha = tuple(sorted(alpha, reverse=True))
    key = (alpha, k, n)
    if key not in _MOM:
        d = len(alpha)
        m = n - d
        num = sum((-1) ** j * comb(m, j) * _cubeD(alpha, Fr(k - j), m - 1) for j in range(m + 1)) / factorial(m - 1)
        _MOM[key] = num / _ih(n, Fr(k))
    return _MOM[key]

def kappa_slice(k, n):
    guard()
    return slice_moment((3,), k, n) - 3 * slice_moment((2, 1), k, n) + 2 * slice_moment((1, 1, 1), k, n)

def kappa_dirichlet(n):
    guard()
    return Fr(2, n * (n + 1) * (n + 2))

def kappa_cube():
    guard()
    return Fr(1, 4) - 3 * Fr(1, 3) * Fr(1, 2) + 2 * Fr(1, 8)

def moment_direct(y, r, k, n):
    """E[(sum_i y_i x_i)^r] on Delta(k,n), brute force over multisets of indices (exact)."""
    guard()
    tot = Fr(0)
    for ms in itertools.combinations_with_replacement(range(n), r):
        cnt = {}
        for i in ms:
            cnt[i] = cnt.get(i, 0) + 1
        mult = factorial(r)
        mono = Fr(1)
        for i, c in cnt.items():
            mult //= factorial(c)
            mono *= Fr(y[i]) ** c
        if mono:
            tot += mult * mono * slice_moment(tuple(cnt.values()), k, n)
    return tot

# ---------- G1: solution counts (vectorised exact integers) ----------
def basis_vals():
    guard()
    vals = sorted({Fr(p, q) for p in range(-10, 11) for q in range(1, 11)})
    S = 2520
    return np.array([int(v * S) for v in vals], dtype=np.int64), S

def count_G1(kappa, use_colour_isospin=True):
    """# (yu,yd,yL,ye) in the declared domain with yQ = 1 such that graded m1 == 0 and kappa*cubic tensor == 0.
    Component structure (exact, from the weight table): m1 -> Y-trace; cubic -> Y^3, T3^2 Y (SU(2)^2 U(1)),
    H^2 Y (SU(3)^2 U(1)); every other component vanishes for this multiplet table independent of Y (checked in
    planted mode from cubic_tensor)."""
    guard()
    R, S = basis_vals()
    Rset = set(R.tolist())
    yQ = S
    D, L = np.meshgrid(R, R, indexing='ij')
    D, L = D.ravel(), L.ravel()
    sols = []
    for U in R.tolist():
        E = -(6 * yQ + 3 * U + 3 * D + 2 * L)
        ok = np.isin(E, R)
        if kappa != 0:
            ok &= (6 * yQ ** 3 + 3 * U ** 3 + 3 * D ** 3 + 2 * L ** 3 + E ** 3) == 0
            if use_colour_isospin:
                ok &= (3 * yQ + L) == 0             # sum T3^2 Y = (1/4)(6 yQ + 2 yL)
                ok &= (2 * yQ + U + D) == 0         # sum H3^2 Y = 2 (2 yQ + yu + yd)
        sols += [(Fr(U, S), Fr(int(b), S), Fr(int(c), S), Fr(int(e), S))
                 for b, c, e in zip(D[ok], L[ok], E[ok]) if int(e) in Rset]
    return sols

def count_full_acc():
    guard()
    return count_G1(Fr(1), True)

def cubic_components_check(Y):
    """the tensor components that depend on Y must equal the three ACC combinations used in count_G1."""
    guard()
    st = states(MULT, Y)
    T = cubic_tensor(st)
    yQ, yu, yd, yL, ye = (Y[k] for k in 'QudLe')
    expect = {
        (3, 3, 3): 6 * yQ ** 3 + 3 * yu ** 3 + 3 * yd ** 3 + 2 * yL ** 3 + ye ** 3,
        (2, 2, 3): Fr(1, 4) * (6 * yQ + 2 * yL),
        (0, 0, 3): 2 * (2 * yQ + yu + yd),
    }
    bad = [abc for abc, v in expect.items() if T[abc] != v]
    # the remaining components must be Y-independent and zero
    for abc, v in T.items():
        if abc in expect:
            continue
        if abc in ((1, 1, 3),):     # H8'^2 Y: proportional to SU(3)^2 U(1) (= 3x the H3 one)
            if v != 3 * expect[(0, 0, 3)]:
                bad.append(abc)
            continue
        if v != 0:
            bad.append(abc)
    return bad, T

# ---------- G3: Weyl-invariant coordinate cells = unions of multiplets ----------
def union_scan(mults, Y):
    guard()
    names = [m[0] for m in mults]
    hits = []
    for r in range(1, len(names)):
        for sub in itertools.combinations(names, r):
            st = states([m for m in mults if m[0] in sub], Y)
            if all(v == 0 for v in m1_vec(st)) and all(v == 0 for v in cubic_tensor(st).values()):
                hits.append(sub)
    return hits

def classify(n_hyp, n_simplex, n_acc, union_hits, m5_sm):
    guard()
    reproduces = n_hyp == n_acc
    earned = reproduces and n_simplex != n_acc
    newcond = bool(union_hits) or m5_sm == 0
    if earned or newcond:
        return 'LINK', reproduces, earned, newcond
    return ('NO-LINK (TAUTOLOGICAL-REPRODUCTION)' if reproduces else 'NO-LINK'), reproduces, earned, newcond

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    if mode == 'planted':
        ok = True
        for n in (5, 15):
            a, b = kappa_slice(1, n), kappa_dirichlet(n)
            good = a == b; ok &= good
            print(f"planted kappa(Delta(1,{n})) slice {a} == Dirichlet {b}: {'OK' if good else 'FAIL'}")
        a = kappa_slice(2, 15); good = a == Fr(129017, 33392760); ok &= good
        print(f"planted kappa(Delta(2,15)) = {a} == BRIDGE 129017/33392760: {'OK' if good else 'FAIL'}")
        a = kappa_slice(2, 4); good = a == 0; ok &= good
        print(f"planted kappa(Delta(2,4)) octahedron = {a}: {'OK' if good else 'FAIL'}")
        # graded cubic reduction on a random p1 = 0 vector vs brute force (n = 6, Delta(2,6))
        y = [Fr(3), Fr(-1), Fr(2), Fr(-5), Fr(1), Fr(0)]
        lhs = moment_direct(y, 3, 2, 6); rhs = kappa_slice(2, 6) * sum(v ** 3 for v in y)
        good = lhs == rhs; ok &= good
        print(f"planted m3 = kappa p3 on p1 = 0 (Delta(2,6), brute force): {lhs} == {rhs}: {'OK' if good else 'FAIL'}")
        # m5 power-sum structure c5 p5 + c23 p2 p3 on p1 = 0, fitted on two vectors, checked on a third (Delta(2,7))
        # (5 non-zero entries needed: on p1 = 0, p5 - (5/6) p2 p3 = 5 e5)
        ys = [[Fr(2), Fr(-1), Fr(-1), 0, 0, 0, 0], [Fr(3), Fr(1), Fr(-1), Fr(-1), Fr(-2), 0, 0],
              [Fr(1), Fr(1), Fr(1), Fr(1), Fr(-1), Fr(-3), 0]]
        def ps(v, r): return sum(Fr(x) ** r for x in v)
        mm = [moment_direct(v, 5, 2, 7) for v in ys]
        a11, a12, a21, a22 = ps(ys[0], 5), ps(ys[0], 2) * ps(ys[0], 3), ps(ys[1], 5), ps(ys[1], 2) * ps(ys[1], 3)
        det = a11 * a22 - a12 * a21
        c5 = (mm[0] * a22 - a12 * mm[1]) / det; c23 = (a11 * mm[1] - a21 * mm[0]) / det
        pred = c5 * ps(ys[2], 5) + c23 * ps(ys[2], 2) * ps(ys[2], 3)
        good = pred == mm[2]; ok &= good
        print(f"planted m5 = c5 p5 + c23 p2 p3 on p1 = 0 (Delta(2,7)): c5 = {c5}, c23 = {c23}, check {'OK' if good else 'FAIL'}")
        # SM weight table: graded m1 == 0 and the cubic tensor components equal the declared ACC combinations
        bad, T = cubic_components_check(SM_Y)
        good = not bad and m1_vec(states(MULT, SM_Y)) == (0, 0, 0, 0); ok &= good
        print(f"planted SM table: m1 = 0 vector, tensor components = ACC combinations (bad {bad}): {'OK' if good else 'FAIL'}")
        Yr = {'Q': Fr(1), 'u': Fr(-7), 'd': Fr(0), 'L': Fr(8), 'e': Fr(-1)}
        bad, _ = cubic_components_check(Yr)
        good = not bad; ok &= good
        print(f"planted rival table (BRIDGE (-7,0,8,-1) at yQ=1): component identities hold (bad {bad}): {'OK' if good else 'FAIL'}")
        # full ACC count at yQ = 1 = the two STRUCT-1 branches
        n_acc = len(count_full_acc()); good = n_acc == 2; ok &= good
        print(f"planted N_ACC (full four ACC, yQ = 1) = {n_acc} (expect 2): {'OK' if good else 'FAIL'}")
        n_y = len(count_G1(Fr(1), use_colour_isospin=False)); good = n_y == 35; ok &= good
        print(f"planted Y-only graded count (= BRIDGE N_M2) = {n_y} (expect 35): {'OK' if good else 'FAIL'}")
        # G3 detector: SM + vector-like pair (E, Ebar) with Y = +-1 must reveal the pair as a proper anomaly-free union
        mults = MULT + [('Ev', [(0, 0)], [Fr(0)]), ('Evb', [(0, 0)], [Fr(0)])]
        Yp = dict(SM_Y); Yp['Ev'] = Fr(1); Yp['Evb'] = Fr(-1)
        hits = union_scan(mults, Yp)
        good = ('Ev', 'Evb') in hits; ok &= good
        print(f"planted G3 detector: SM + (E,Ebar) proper anomaly-free unions {hits}: {'OK' if good else 'FAIL'}")
        print("PLANTED:", "ALL OK" if ok else "FAILURE -> ILL-DEFINED")
    elif mode == 'broken':
        # declared false claim: "the Y-only grading (no colour/isospin weights) already gives the four ACC"
        n_acc = len(count_full_acc()); n_y = len(count_G1(kappa_slice(2, 15), use_colour_isospin=False))
        print(f"broken: Y-only graded Delta(2,15) count {n_y} vs N_ACC {n_acc}")
        print("BROKEN:", "REJECTED" if n_y != n_acc else "ACCEPTED (checker defective)")
    else:
        kh = {k: kappa_slice(k, 15) for k in (1, 2, 3)}
        kc = kappa_cube()
        for k, v in kh.items():
            print(f"G1 kappa(Delta({k},15)) = {v} ({float(v):.6e})")
        print(f"G1 kappa(cube) = {kc}")
        n_acc = len(count_full_acc())
        counts = {f"Delta({k},15)": len(count_G1(v)) for k, v in kh.items()}
        counts['cube'] = len(count_G1(kc))
        for name, c in counts.items():
            print(f"G1 N[{name}] (graded m1 = 0 and kappa*cubic tensor = 0, yQ = 1) = {c}")
        print(f"G1 N_ACC (four ACC) = {n_acc}")
        sols = count_G1(kh[2])
        print(f"G1 Delta(2,15) solutions (yu, yd, yL, ye): {[tuple(str(x) for x in s) for s in sols]}")
        hits = union_scan(MULT, SM_Y)
        print(f"G3 proper non-empty multiplet unions with vanishing graded m1 and cubic tensor (SM): {hits}")
        st = states(MULT, SM_Y)
        yv = [w[3] for _, w in st]
        m4 = moment_direct(yv, 4, 2, 15); m5 = moment_direct(yv, 5, 2, 15)
        print(f"G4 SM along Y: p2 = {power_Y(st, 2)}, p4 = {power_Y(st, 4)}, p5 = {power_Y(st, 5)}")
        print(f"G4 Delta(2,15) graded m4(Y) = {m4} ({float(m4):.6e}); m5(Y) = {m5} ({float(m5):.6e})")
        verdict, rep, earned, newc = classify(counts['Delta(2,15)'], counts['Delta(1,15)'], n_acc, hits, m5)
        print(f"REPRODUCES = {rep}; EARNED = {earned}; NEW-CONDITION = {newc}")
        print("VERDICT:", verdict)

if __name__ == '__main__':
    main()
