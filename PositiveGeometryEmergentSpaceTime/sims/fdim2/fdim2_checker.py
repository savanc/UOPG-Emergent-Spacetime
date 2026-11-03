#!/usr/bin/env python3
"""F-DIM' (F-DIM2) locked checker: which spacetime dimensions D does partial-wave positivity (tree-level unitarity) of the
trunk's dual-resonance pion amplitude (Lovelace-Shapiro, Adler-zero intercept alpha0 = 1/2) allow, and is any D FORCED?

Modes: planted | broken | live.  Every mode first calls guard() (hard precondition, METHOD 2026-10-20).
Exact rational arithmetic (fractions.Fraction) throughout; no floats in any verdict.
"""
import hashlib, json, re, subprocess, sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/F-DIM2-2026-10-20.md'

_GUARD_OK = False

def guard():
    """Hard precondition (METHOD 2026-10-20, tightened for F-DIM'): called inside EVERY scoring/live function,
    so importing the functions cannot bypass it. Memoised only after success."""
    global _GUARD_OK
    if _GUARD_OK:
        return
    def git(*a):
        return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)
    if git('fetch', '-q', 'origin').returncode != 0:
        sys.exit("GUARD REFUSED: git fetch failed")
    sha = git('log', '--format=%H', '--diff-filter=A', '-n', '1', '--', PREREG).stdout.strip()
    if not sha:
        sys.exit(f"GUARD REFUSED: {PREREG} has no commit")
    if git('merge-base', '--is-ancestor', sha, 'origin/main').returncode != 0:
        sys.exit(f"GUARD REFUSED: prereg commit {sha[:9]} is not an ancestor of origin/main (not pushed)")
    text = (REPO / PREREG).read_text()
    m = re.search(r'fdim2_checker\.py` sha256 `([0-9a-f]{64})`', text)
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")
    _GUARD_OK = True
    print(f"GUARD OK: prereg {sha[:9]} on origin/main; checker hash matches")

# ---------- polynomials in x = cos(theta), coefficient lists (index = power) ----------
def pmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r

def residue_poly(model, N):
    """-Res_{s=s_N} A(s,t) as a polynomial in x (overall sign kept; a global sign is free).
    model = ('ls', alpha0): A = G(1-al(s))G(1-al(t))/G(1-al(s)-al(t)), al(s) = alpha0 + s (alpha' = 1),
        Adler-zero mass relation m^2 = 1/2 - alpha0 (Bianchi-Consoli-Di Vecchia 2021 eq. (2.4)); a = al - 1.
    model = ('bos', m2): A = G(-a(s))G(-a(t))/G(-a(s)-a(t)), a(s) = 1 + s; physical tachyons m2 = -1.
    """
    guard()
    kind, par = model
    if kind == 'ls':
        a0 = par - 1                       # a(s) = a0 + s
        m2 = F(1, 2) - par
        nfac = N + 1                       # residue ~ prod_{j=1}^{N+1} (a(t)+j) / N!
    elif kind == 'bos':
        a0 = F(1)
        m2 = par
        nfac = N
    else:
        raise ValueError(kind)
    sN = N - a0                            # a(s_N) = N
    K = sN - 4 * m2                        # t = -(K/2)(1 - x)
    p = [F(-1, factorial(N))]
    for j in range(1, nfac + 1):
        p = pmul(p, [a0 + j - K / 2, K / 2])
    return p

def poch(a, n):
    r = F(1)
    for i in range(n):
        r *= a + i
    return r

def geg_coeffs(p, D):
    """Coefficients of p(x) in the SO(D-1) partial-wave basis: Gegenbauer C_j^{lam}, lam = (D-3)/2 (D > 3),
    Chebyshev T_j for D = 3. Basis norms are positive, so signs equal partial-wave-coefficient signs."""
    guard()
    lam = F(D - 3, 2)
    c = [F(0)] * len(p)
    for n, r in enumerate(p):
        if r == 0:
            continue
        if D == 3:
            for l in range((n - 1) // 2 + 1) if n >= 1 else []:
                c[n - 2 * l] += r * F(comb(n, l), 2 ** (n - 1))
            if n % 2 == 0:
                c[0] += r * F(comb(n, n // 2), 2 ** n)
        else:
            for l in range(n // 2 + 1):
                c[n - 2 * l] += r * F(factorial(n), 2 ** n) * (lam + n - 2 * l) / (factorial(l) * poch(lam, n - l + 1))
    return c

def positive_at(model, D, NMAX):
    """True iff there is a global sign sigma with sigma*c_{N,j} >= 0 for all levels N <= NMAX and all spins j."""
    guard()
    sigma = 0
    for N in range(NMAX + 1):
        for cj in geg_coeffs(residue_poly(model, N), D):
            if cj == 0:
                continue
            s = 1 if cj > 0 else -1
            if sigma == 0:
                sigma = s
            elif s != sigma:
                return False
    return True

DSCAN = range(3, 41)                       # 38 integer dimensions (look-elsewhere set, prereg)

def pass_set(model, NMAX):
    guard()
    return [D for D in DSCAN if positive_at(model, D, NMAX)]

def classify(ps):
    guard()
    if not ps:
        return 'NONE-ALLOWED'
    if len(ps) == 1:
        return f'FORCED-EQUALITY D={ps[0]}'
    if ps == list(range(3, ps[-1] + 1)) and ps[-1] < 40:
        return f'BOUND-ONLY D<={ps[-1]}'
    if ps == list(DSCAN):
        return 'NO-BOUND'
    return 'NON-INTERVAL'

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    guard()
    spec = json.loads((HERE.parent / 'planted_cases.json').read_text())
    if mode == 'planted':
        ok = True
        for case in spec['planted']:
            model = (case['kind'], F(case['par']))
            ps = pass_set(model, case['nmax'])
            got = classify(ps)
            good = got == case['expect']
            ok &= good
            print(f"{case['name']}: {got} (expect {case['expect']}) {'OK' if good else 'FAIL'}")
        print('recovered:', ok)
        sys.exit(0 if ok else 1)
    if mode == 'broken':
        case = spec['broken']
        ps = pass_set((case['kind'], F(case['par'])), case['nmax'])
        got = classify(ps)
        if got == case['must_not']:
            print(f"broken case {case['name']}: {got} -- NOT rejected (FAIL)")
            sys.exit(0)
        print(f"broken case {case['name']}: {got} != {case['must_not']} -> REJECT (as required)")
        sys.exit(1)
    if mode == 'live':
        NMAX = 40
        trunk = ('ls', F(1, 2))
        ps = pass_set(trunk, NMAX)
        verdict_dim = classify(ps)
        print(f"trunk LS (alpha0 = 1/2, m_pi = 0), levels N <= {NMAX}: pass set {ps[0] if ps else '-'}..{ps[-1] if ps else '-'} "
              f"({len(ps)} of {len(DSCAN)}) -> {verdict_dim}")
        # first failing level just above the bound, and saturation at the bound
        if ps and ps[-1] < 40:
            Dc = ps[-1]
            for N in range(NMAX + 1):
                c = geg_coeffs(residue_poly(trunk, N), Dc + 1)
                c0 = geg_coeffs(residue_poly(trunk, N), Dc)
                if any(x > 0 for x in c) and any(x < 0 for x in c):
                    print(f"first level violating at D = {Dc + 1}: N = {N}")
                    break
            zeros = [(N, j) for N in range(NMAX + 1) for j, x in enumerate(geg_coeffs(residue_poly(trunk, N), Dc)) if x == 0]
            print(f"exact zero partial-wave coefficients at D = {Dc} (saturations, first 6): {zeros[:6]}")
        cands = [4, 8, 10, 11, 16, 24, 26]
        print('candidate integers allowed by trunk positivity:', [d for d in cands if d in ps])
        print('candidate integers FORCED (equality):', [d for d in cands if ps == [d]])
        # diagnostic only (not in the verdict): Adler-zero relation off, intercept alpha0 varied
        for a in (F(3, 10), F(2, 5), F(1, 2), F(3, 5), F(7, 10)):
            print(f"  diag alpha0 = {a}: {classify(pass_set(('ls', a), 12))} (levels <= 12)")
        if not ps or 4 not in ps:
            v = 'TRUNK-INCONSISTENT-AT-D4'
        elif verdict_dim.startswith('FORCED'):
            v = 'FORCED-EQUALITY'
        elif verdict_dim == 'BOUND-ONLY D<=4':
            v = 'BOUND-ONLY (D <= 4)'
        elif verdict_dim.startswith('BOUND-ONLY'):
            v = 'BOUND-ONLY-OTHER (' + verdict_dim + ')'
        elif verdict_dim == 'NO-BOUND':
            v = 'NO-BOUND'
        else:
            v = 'UNCLASSIFIED'
        print('verdict:', v)
        return
    sys.exit("usage: fdim_checker.py planted|broken|live")

if __name__ == '__main__':
    main()
