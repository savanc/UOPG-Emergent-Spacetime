#!/usr/bin/env python3
"""F-POSGEOM-DAUGHTER locked checker: WELL-POSEDNESS GATE W for the geometry-native stringy NLSM
(delta-shifted stringy Tr(phi^3), Arkani-Hamed-Cao-Dong-Figueiredo-He arXiv:2312.16282 sec. 7, eq. 7.10):
    I4(d; X, Y) = Gamma(a(X - d)) Gamma(a(Y + d)) / Gamma(a(X + Y)),   a = alpha' = 1 (units), d = alpha' delta in (0,1).
No physical input enters. Gate W asks whether the dimensionless content of the family depends on d (free continuous
parameter) and whether every member carries the unit-residue pole at X = d (mass^2 = -delta, Lean FDeltaNLSM).
Observables (all dimensionless, alpha' = 1):
    L2(d)  = Gamma(-d) Gamma(d)  (low-energy NLSM coefficient, eq. 7.11; 1/F^2 up to a d-independent convention)
    RV(d)  = (1 - d) * |L2(d)|   (first spin-1 mass^2 times 1/F^2 proxy: the rho-type dimensionless ratio)
    RES(d) = lim_{X->d} (X - d) I4  (numerical; Lean: = 1/alpha' = 1)
Modes: planted | broken | live.  mpmath 50 digits.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main. No pass flag; caches keyed
by origin/main sha only; `git fetch` once per process.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
import mpmath as mp
mp.mp.dps = 50

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/F-POSGEOM-DAUGHTER-2026-10-20.md'
GRID = [mp.mpf(k) / 10 for k in range(1, 10)]   # d = 0.1 ... 0.9 (declared, single trial: gate W only)
VARY = mp.mpf('0.01')                             # free-parameter criterion: max/min - 1 > 1% over GRID

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
    m = re.search(r'fpgd_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- family ----------
def I4(d, X, Y):
    guard()
    return mp.gamma(X - d) * mp.gamma(Y + d) * mp.rgamma(X + Y)

def residue(d, Y=mp.mpf('0.37')):
    guard()
    eps = mp.mpf('1e-30')
    return eps * I4(d, d + eps, Y)

def L2(d):
    guard()
    return mp.gamma(-d) * mp.gamma(d)

def lowenergy_ratio(d, X=mp.mpf('1e-12'), Y=mp.mpf('2e-12')):
    """I4 / (L2 (X + Y)) at tiny X, Y: eq. 7.11 says -> 1."""
    guard()
    return I4(d, X, Y) / (L2(d) * (X + Y))

def RV(d):
    guard()
    return (1 - d) * abs(L2(d))

def gate_w(rv_values, res_values):
    guard()
    spread = max(rv_values) / min(rv_values) - 1
    free = spread > VARY
    tach = all(abs(r - 1) < mp.mpf('1e-20') for r in res_values)
    if free:
        verdict = 'ILL-DEFINED (free continuous alpha\'delta changes dimensionless predictions; no fixing condition declared)'
    else:
        verdict = 'WELL-POSED (dimensionless content d-independent)'
    return spread, free, tach, verdict

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    if mode == 'planted':
        cases = json.loads((HERE.parent / 'planted_cases.json').read_text())
        ok = True
        for c in cases['lowenergy']:
            r = lowenergy_ratio(mp.mpf(c['d']))
            good = abs(r - 1) < mp.mpf(c['tol']); ok &= good
            print(f"planted low-energy eq7.11 d={c['d']}: I4/(L2 (X+Y)) = {mp.nstr(r, 15)}  {'OK' if good else 'FAIL'}")
        for c in cases['residue']:
            r = residue(mp.mpf(c['d']))
            good = abs(r - 1) < mp.mpf(c['tol']); ok &= good
            print(f"planted residue (Lean deltaAmp4_tachyon_residue) d={c['d']}: {mp.nstr(r, 15)}  {'OK' if good else 'FAIL'}")
        for c in cases['gate']:
            sp, fr, ta, v = gate_w([mp.mpf(x) for x in c['rv']], [mp.mpf(x) for x in c['res']])
            good = (fr == c['free']); ok &= good
            print(f"planted gate case {c['name']}: free={fr} expected={c['free']}  {'OK' if good else 'FAIL'}")
        print('PLANTED', 'ALL OK' if ok else 'FAILED')
    elif mode == 'broken':
        r = residue(mp.mpf('0.5'))
        claim_holds = abs(r) < mp.mpf('1e-10')
        print(f"broken claim 'alpha'delta = 1/2 member has no pole at X13 = delta (residue 0)': residue = {mp.nstr(r, 15)}")
        print('BROKEN', 'ACCEPTED (checker defective)' if claim_holds else 'REJECTED (as required; Lean deltaAmp4_tachyon_residue)')
    else:
        rvs, ress = [], []
        for d in GRID:
            rv, res = RV(d), residue(d)
            rvs.append(rv); ress.append(res)
            print(f"d={mp.nstr(d, 2)}  L2={mp.nstr(L2(d), 10)}  RV={mp.nstr(rv, 10)}  residue@X=d (mass^2=-delta)={mp.nstr(res, 12)}")
        sp, fr, ta, v = gate_w(rvs, ress)
        print(f"RV spread max/min-1 = {mp.nstr(sp, 6)} (criterion > {VARY}); tachyon pole with unit residue in every member: {ta}")
        print('GATE W:', v)

if __name__ == '__main__':
    main()
