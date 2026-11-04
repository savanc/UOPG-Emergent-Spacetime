#!/usr/bin/env python3
"""F-DIM-MASS locked checker: does the trunk Lovelace-Shapiro pion amplitude with PHYSICAL masses stay unitary
(partial-wave positive) in D = 4, and does any pre-declared zero-parameter fix restore D = 4?

Modes: planted | broken | live.  Exact rationals (fractions.Fraction).
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() is called inside EVERY scoring function and re-verifies on
EVERY call (a) the checker's sha256 against the prereg and (b) that the prereg's commit is an ancestor of origin/main.
There is no pass flag. The only caches are keyed by commit sha (origin/main sha -> (prereg sha, ancestry)), and
`git fetch` runs once per process; the ancestry test itself is re-evaluated whenever origin/main's sha changes.
"""
import hashlib, json, re, subprocess, sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/F-DIM-MASS-2026-10-20.md'

def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)

_FETCH_DONE = []          # fetch once per process (not a pass flag: ancestry/hash are still checked every call)
_ANC_BY_ORIGIN = {}       # origin/main sha -> (prereg sha, is_ancestor)

def _origin_sha():
    r = _git('rev-parse', '--verify', '-q', 'refs/remotes/origin/main')
    return r.stdout.strip()

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
    text = (REPO / PREREG).read_text()
    m = re.search(r'fdimm_checker\.py` sha256 `([0-9a-f]{64})`', text)
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- polynomials ----------
def pmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r

def poch(a, n):
    r = F(1)
    for i in range(n):
        r *= a + i
    return r

def residue_poly(model, N):
    """-Res at level N, polynomial in x = cos(theta) (global sign free).
    ('lsm', alpha0, m2): A = G(1-al(s))G(1-al(t))/G(1-al(s)-al(t)), al(s) = alpha0 + s (alpha' = 1 units),
        external mass^2 = m2 (alpha' units), independent of alpha0.  Level N: al(s_N) = N + 1.
    """
    guard()
    kind, a0p, m2 = model
    if kind != 'lsm':
        raise ValueError(kind)
    a0 = a0p - 1
    sN = N - a0
    K = sN - 4 * m2
    p = [F(-1, factorial(N))]
    for j in range(1, N + 2):
        p = pmul(p, [a0 + j - K / 2, K / 2])
    return p

def geg_coeffs(p, D):
    """SO(D-1) partial-wave coefficients (Gegenbauer lam = (D-3)/2; Chebyshev at D = 3); signs = partial-wave signs."""
    guard()
    lam = F(D - 3, 2)
    c = [F(0)] * len(p)
    for n, r in enumerate(p):
        if r == 0:
            continue
        if D == 3:
            for l in (range((n - 1) // 2 + 1) if n >= 1 else []):
                c[n - 2 * l] += r * F(comb(n, l), 2 ** (n - 1))
            if n % 2 == 0:
                c[0] += r * F(comb(n, n // 2), 2 ** n)
        else:
            for l in range(n // 2 + 1):
                c[n - 2 * l] += r * F(factorial(n), 2 ** n) * (lam + n - 2 * l) / (factorial(l) * poch(lam, n - l + 1))
    return c

def positive_at(model, D, NMAX):
    """One global sign sigma with sigma*c_{N,j} >= 0 for all N <= NMAX, all j."""
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

DSCAN = range(3, 41)

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

def level1_Dc(a0, m2):
    """Real level-1 spin-0 threshold (float, report only): k^2/(D-1) + (a0-k)(a0+1-k) >= 0, k = (2-a0-4m2)/2."""
    guard()
    k = (2 - a0 - 4 * m2) / 2
    c = (a0 - k) * (a0 + 1 - k)
    if c >= 0:
        return float('inf')
    return float(1 + k * k / (-c))

# ---------- physical models (prereg: baseline + declared fixes) ----------
def models_from_masses(mpi, mrho, mf2):
    """All in GeV (exact decimals). Returns {name: ('lsm', alpha0, m2_in_alpha'_units)} or 'AUTO-FAIL: reason'."""
    guard()
    p2, r2, f2 = mpi * mpi, mrho * mrho, mf2 * mf2
    out = {}
    ap = 1 / (2 * (r2 - p2))                       # P_a baseline: al(m_rho^2) = 1, 2 al(m_pi^2) = 1 (Adler, s=t=m_pi^2)
    out['P_a baseline (Adler at s=t=m_pi^2)'] = ('lsm', 1 - ap * r2, ap * p2)
    ap = 1 / (2 * r2)                              # P_b: Adler point moved to s=t=0  -> alpha0 = 1/2
    out['P_b Adler at s=t=0'] = ('lsm', F(1, 2), ap * p2)
    ap = 1 / (2 * (r2 - F(4, 3) * p2))             # P_c: Adler point at symmetric s=t=u=4m^2/3
    out['P_c Adler at s=t=4m^2/3'] = ('lsm', 1 - ap * r2, ap * p2)
    ap = 1 / (f2 - r2)                             # F5: trajectory from rho and f2 (no Adler input)
    out['F5 rho-f2 trajectory'] = ('lsm', 1 - ap * r2, ap * p2)
    out['F6 daughter shift Gamma(lambda - al)'] = 'AUTO-FAIL: needs a fitted shift lambda'
    out['F7 Coon q-deformation'] = 'AUTO-FAIL: needs a fitted q'
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    guard_banner()
    spec = json.loads((HERE.parent / 'planted_cases.json').read_text())
    if mode == 'planted':
        ok = True
        for case in spec['planted']:
            model = ('lsm', F(case['alpha0']), F(case['m2']))
            got = classify(pass_set(model, case['nmax']))
            d4 = positive_at(model, 4, case['nmax_d4'])
            good = got == case['expect'] and d4 == case['expect_d4']
            ok &= good
            print(f"{case['name']}: {got}; D=4 positive to N<={case['nmax_d4']}: {d4} {'OK' if good else 'FAIL'}")
        print('recovered:', ok)
        sys.exit(0 if ok else 1)
    if mode == 'broken':
        case = spec['broken']
        got = classify(pass_set(('lsm', F(case['alpha0']), F(case['m2'])), case['nmax']))
        if got == case['must_not']:
            print(f"broken case {case['name']}: {got} -- NOT rejected (FAIL)")
            sys.exit(0)
        print(f"broken case {case['name']}: {got} != {case['must_not']} -> REJECT (as required)")
        sys.exit(1)
    if mode == 'live':
        mpath = HERE.parent / 'masses.json'
        if not mpath.exists():
            sys.exit("live refused: masses.json (fetched after the prereg) missing")
        data = json.loads(mpath.read_text())
        print('masses.json sha256', hashlib.sha256(mpath.read_bytes()).hexdigest())
        NMAX4, NMAXD = 40, 12
        res = {}
        for sname, s in data['sets'].items():
            mods = models_from_masses(F(s['m_pi']), F(s['m_rho']), F(s['m_f2']))
            for name, mod in mods.items():
                if isinstance(mod, str):
                    res.setdefault(name, {})[sname] = False
                    print(f"[{sname}] {name}: {mod}")
                    continue
                _, a0, m2 = mod
                d4 = positive_at(mod, 4, NMAX4)
                ps = pass_set(mod, NMAXD)
                res.setdefault(name, {})[sname] = d4
                print(f"[{sname}] {name}: alpha0 = {float(a0):.5f}, m2 = {float(m2):.5f}, level-1 D_c = {level1_Dc(a0, m2):.4f}; "
                      f"D=4 positive to N<={NMAX4}: {d4}; pass set (N<={NMAXD}): {classify(ps)}")
        base = [k for k in res if k.startswith('P_a')][0]
        base_fail = not all(res[base].values())
        fixes_pass = [k for k in res if k != base and all(res[k].values())]
        adler_line = {'P_a baseline (Adler at s=t=m_pi^2)'}   # only P_a keeps the LO zero line s+t = 2 m_pi^2
        print('baseline gate:', 'GATE-FAIL (trunk model)' if base_fail else 'GATE-PASS')
        print('fixes passing positivity at D=4 (both input sets):', fixes_pass)
        if not base_fail:
            v = 'UNCLASSIFIED (baseline passes, contradicting the analytic level-1 result)'
        elif any(k in adler_line for k in fixes_pass):
            v = 'GATE-FAIL-REPAIRED'
        elif fixes_pass:
            v = 'GATE-FAIL-REPAIRED-AT-COST (' + '; '.join(fixes_pass) + ')'
        else:
            v = 'GATE-FAIL-UNREPAIRED'
        print('verdict:', v)
        return
    sys.exit("usage: fdimm_checker.py planted|broken|live")

if __name__ == '__main__':
    main()
