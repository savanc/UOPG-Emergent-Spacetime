#!/usr/bin/env python3
"""BRIDGE-PL-ASSOC (charge rung) locked checker. Question: can the chain Pluecker -> torus orbit -> hypersimplex ->
associahedron (CITED: GGMS 1987; Speyer-Williams math/0312297; ABL 1703.04541; ABHY 1711.09102; AHL 1912.08707;
LPW 2002.06164) constrain a U(1) charge vector lambda (hypercharge), i.e. discharge an anomaly condition of STRUCT-1?
A charge enters Gr(2,n) only as a cocharacter of the column torus P -> P diag(exp(tau lambda)).
M1 (quotient level): cross-ratios / u-variables of the torus-moved point (associahedron data). CHARGE-BLIND iff all
    differences < 1e-40 for every declared charge vector.
M2 (equivariant level): moments of <lambda, mu> over the uniform measure on Delta(2,n), n = 15 Weyl states of one SM
    generation (no nu^c; multiplicities Q 6, u^c 3, d^c 3, L 2, e^c 1 -- content ASSUMED as in STRUCT-1).
    m1 = 0 <=> Tr Y = 0; on Tr Y = 0, m3 = kappa Tr Y^3 (Lean BridgePLCharge.sym_cubic_reduction).
    kappa computed EXACTLY (Irwin-Hall slice integrals, Fractions) for Delta(2,n) and rivals Delta(1,n), [0,1]^n.
    N_M2 = # solutions with yQ = 1 of {Tr Y = 0, Tr Y^3 = 0 (if kappa != 0)} in the fixed basis p/q, |p|,|q| <= 10;
    N_ACC = same with all four STRUCT-1 ACC (planted: must be 2).
Rule (prereg): M2 EARNED iff kappa_hyp != 0 AND kappa = 0 for BOTH rivals AND N_M2 == N_ACC. LINK iff M1 not
    charge-blind OR M2 earned. Otherwise NO-LINK. Planted failure -> ILL-DEFINED.
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main. No pass flag; caches keyed
by origin/main sha only; `git fetch` once per process.
"""
import hashlib, itertools, json, re, subprocess, sys
from fractions import Fraction as Fr
from math import comb, factorial
from pathlib import Path
import mpmath as mp
mp.mp.dps = 60

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/BRIDGE-PL-ASSOC-2026-10-20.md'
MULT = (6, 3, 3, 2, 1)   # Q, u^c, d^c, L, e^c Weyl states per generation
CHARGES = {               # multiplet-level charge vectors (Q, u^c, d^c, L, e^c); declared
    'SM_Y': (Fr(1, 6), Fr(-2, 3), Fr(1, 3), Fr(-1, 2), Fr(1)),
    'B-L': (Fr(1, 3), Fr(-1, 3), Fr(-1, 3), Fr(-1), Fr(1)),
    'rival_nonACC': (Fr(1, 7), Fr(2, 7), Fr(3, 7), Fr(4, 7), Fr(5, 7)),
}

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
    m = re.search(r'bplc_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- M1: torus action on Gr(2,n) ----------
def pos_matrix(n):
    """Totally positive 2 x n point: columns (1, x_i), x_i increasing (all ordered minors x_j - x_i > 0)."""
    guard()
    xs = [mp.mpf(i + 1) + mp.mpf(i * i) / 7 for i in range(n)]
    return [[mp.mpf(1)] * n, xs]

def plk(P, i, j):
    guard()
    return P[0][i] * P[1][j] - P[0][j] * P[1][i]

def cross_ratios(P):
    guard()
    n = len(P[0])
    return [plk(P, a, b) * plk(P, c, d) / (plk(P, a, c) * plk(P, b, d))
            for a, b, c, d in itertools.combinations(range(n), 4)]

def torus(P, lam, tau=mp.mpf('0.73')):
    guard()
    t = [mp.e ** (tau * mp.mpf(l.numerator) / l.denominator) for l in lam]
    return [[P[r][i] * t[i] for i in range(len(t))] for r in range(2)]

def state_vector(lam5):
    guard()
    return [y for y, m in zip(lam5, MULT) for _ in range(m)]

def m1_maxdiff(lam, n):
    guard()
    P = pos_matrix(n)
    u0, u1 = cross_ratios(P), cross_ratios(torus(P, lam))
    return max(abs(a - b) for a, b in zip(u0, u1))

# ---------- M2: exact moments ----------
def _orthant(bs, L, p):
    """int_{R+^3} prod x_i^{b_i} (L - sum x)_+^p dx."""
    if L <= 0:
        return Fr(0)
    tot = sum(bs) + p + 3
    num = factorial(p)
    for b in bs:
        num *= factorial(b)
    return Fr(L) ** tot * Fr(num, factorial(tot))

def _cube3(alpha, L, p):
    """int_{[0,1]^3} x^alpha (L - s)_+^p dx by inclusion-exclusion of upper bounds."""
    tot = Fr(0)
    for S in itertools.product((0, 1), repeat=3):
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
    """Irwin-Hall density f_m(z) (sum of m uniforms), exact."""
    if z <= 0 or z >= m:
        return Fr(0)
    return sum((-1) ** j * comb(m, j) * Fr(z - j) ** (m - 1) for j in range(m + 1) if z - j > 0) / factorial(m - 1)

def slice_moment(alpha, k, n):
    """E[x1^a x2^b x3^c] for the uniform measure on Delta(k,n) = [0,1]^n cap {sum = k} (n >= 4)."""
    guard()
    m = n - 3
    num = sum((-1) ** j * comb(m, j) * _cube3(alpha, Fr(k - j), m - 1) for j in range(m + 1)) / factorial(m - 1)
    return num / _ih(n, Fr(k))

def kappa_slice(k, n):
    guard()
    return slice_moment((3, 0, 0), k, n) - 3 * slice_moment((2, 1, 0), k, n) + 2 * slice_moment((1, 1, 1), k, n)

def kappa_cube():
    guard()
    return Fr(1, 4) - 3 * Fr(1, 3) * Fr(1, 2) + 2 * Fr(1, 8)

def kappa_dirichlet(n):
    guard()
    return Fr(2, n * (n + 1) * (n + 2))

# ---------- hypercharge solution counts ----------
def basis_ints(S=2520):
    guard()
    vals = {Fr(p, q) for p in range(-10, 11) for q in range(1, 11)}
    return sorted(int(v * S) for v in vals), S

def count_solutions(full_acc, cubic=True):
    guard()
    R, S = basis_ints()
    Rset = set(R)
    yQ = S
    sols = []
    for U in R:
        for D in R:
            if full_acc and 2 * yQ + U + D != 0:
                continue
            for L in R:
                if full_acc and 3 * yQ + L != 0:
                    continue
                E = -(6 * yQ + 3 * U + 3 * D + 2 * L)
                if E not in Rset:
                    continue
                if cubic and 6 * yQ ** 3 + 3 * U ** 3 + 3 * D ** 3 + 2 * L ** 3 + E ** 3 != 0:
                    continue
                sols.append(tuple(Fr(v, S) for v in (U, D, L, E)))
    return sols

def classify(m1_blind, k_hyp, k_rivals, n_m2, n_acc):
    guard()
    m2_earned = (k_hyp != 0) and all(k == 0 for k in k_rivals) and (n_m2 == n_acc)
    if (not m1_blind) or m2_earned:
        return 'LINK', m2_earned
    return 'NO-LINK', m2_earned

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    if mode == 'planted':
        cases = json.loads((HERE.parent / 'planted_cases.json').read_text())
        ok = True
        for n in cases['dirichlet_n']:
            a, b = kappa_slice(1, n), kappa_dirichlet(n)
            good = a == b; ok &= good
            print(f"planted kappa(Delta(1,{n})) slice-integral {a} == Dirichlet {b}: {'OK' if good else 'FAIL'}")
        a = kappa_slice(2, 4); good = a == 0; ok &= good
        print(f"planted kappa(Delta(2,4)) (octahedron, centrally symmetric) = {a}: {'OK' if good else 'FAIL'}")
        a = slice_moment((1, 0, 0), 2, 15); good = a == Fr(2, 15); ok &= good
        print(f"planted centroid E[mu1] on Delta(2,15) = {a} (expect 2/15): {'OK' if good else 'FAIL'}")
        sols = count_solutions(full_acc=True)
        good = sorted(sols) == sorted([(Fr(-4), Fr(2), Fr(-3), Fr(6)), (Fr(2), Fr(-4), Fr(-3), Fr(6))]); ok &= good
        print(f"planted full-ACC count at yQ=1: {len(sols)} {sols}: {'OK' if good else 'FAIL'}")
        d = m1_maxdiff(state_vector(CHARGES['SM_Y'])[:6], 6); good = d < mp.mpf('1e-40'); ok &= good
        print(f"planted M1 torus invariance (n=6 toy): maxdiff {mp.nstr(d, 5)}: {'OK' if good else 'FAIL'}")
        for c in cases['classify']:
            v, _ = classify(c['m1_blind'], Fr(c['k_hyp']), [Fr(x) for x in c['k_rivals']], c['n_m2'], c['n_acc'])
            good = v == c['expect']; ok &= good
            print(f"planted classify {c['name']}: {v} (expect {c['expect']}): {'OK' if good else 'FAIL'}")
        print('PLANTED', 'ALL OK' if ok else 'FAILED')
    elif mode == 'broken':
        P = pos_matrix(5)
        uY = cross_ratios(torus(P, CHARGES['SM_Y'])); uBL = cross_ratios(torus(P, CHARGES['B-L']))
        d = max(abs(a - b) for a, b in zip(uY, uBL))
        claim = d > mp.mpf('1e-30')
        print(f"broken claim 'SM hypercharge and B-L give different u-variables (n=5)': maxdiff = {mp.nstr(d, 5)}")
        print('BROKEN', 'ACCEPTED (checker defective)' if claim else 'REJECTED (as required; Lean BridgePLCharge.uCR_rival_indistinguishable)')
    else:
        blind = True
        for name, lam in CHARGES.items():
            d5 = m1_maxdiff(lam, 5); d15 = m1_maxdiff(state_vector(lam), 15)
            blind &= (d5 < mp.mpf('1e-40')) and (d15 < mp.mpf('1e-40'))
            print(f"M1 {name}: max |u(t.P) - u(P)| n=5: {mp.nstr(d5, 5)}; n=15: {mp.nstr(d15, 5)}")
        print('M1:', 'CHARGE-BLIND' if blind else 'CHARGE-SENSITIVE')
        kh = kappa_slice(2, 15); ks = kappa_slice(1, 15); kc = kappa_cube()
        print(f"M2 kappa: Delta(2,15) = {kh} ({float(kh):.6e}); rival Delta(1,15) = {ks} ({float(ks):.6e}); rival cube = {kc}")
        kh16 = kappa_slice(2, 16)
        print(f"M2 report-only: kappa Delta(2,16) (with nu^c) = {float(kh16):.6e}; kappa Delta(2,5) = {float(kappa_slice(2, 5)):.6e}")
        sY = CHARGES['SM_Y']
        print(f"M2 report-only, multiplet level n=5 (unit multiplicity): Tr Y = {sum(sY)}, Tr Y^3 = {sum(y**3 for y in sY)} (SM violates)")
        sols_m2 = count_solutions(full_acc=False, cubic=(kh != 0)); sols_acc = count_solutions(full_acc=True)
        print(f"M2 solutions at yQ=1 in basis: N_M2 = {len(sols_m2)}; N_ACC = {len(sols_acc)}")
        print('M2 sample non-SM solutions:', [tuple(str(x) for x in s) for s in sols_m2 if s not in sols_acc][:6])
        v, earned = classify(blind, kh, [ks, kc], len(sols_m2), len(sols_acc))
        print(f"M2 earned: {earned} (needs kappa_hyp != 0, both rivals 0, N_M2 == N_ACC)")
        print('VERDICT:', v)

if __name__ == '__main__':
    main()
