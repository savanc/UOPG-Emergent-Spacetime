#!/usr/bin/env python3
"""STRUCT-NGEN sharpen locked checker: which DECLARED conditions bound N_gen, and does any CONSISTENCY set force 3?
One-loop b0 computed from representation content: b0 = 11/3 C_A - 2/3 sum_Weyl T(R) - 1/3 sum_complex-scalar T(R),
T(fund) = 1/2. Two-loop QCD b1 = 102 - 38/3 n_f. N scanned over 0..20; N >= 1 (matter exists) in every set.
Contents (declared): SM (15 Weyl/gen, 1 Higgs doublet); SM+nu^c (16); RIVAL 3-3-1 (Pisano-Pleitez/Frampton, CITED).
Condition kinds (prereg): K = theory consistency; C = conditional consistency (needs an extra gauged discrete symmetry);
E = experimental (CITED, report-only, never forcing).
Rule: SM verdict from the SM CORE set (K: anomalies [blind], Witten, AF SU(3), AF SU(2)): FORCES-3 iff window == {3},
else NOT-FORCED. Variants (+BZ two-loop, +triality Z9, +Spin-Z4 Z16) reported with their kind; a variant hitting {3} is
CONDITIONAL-3 (if kind C) or DYNAMICAL-3 (BZ), never FORCES-3. Rival core == {3} -> RIVAL-SINGLES-OUT-3.
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main. No pass flag; caches keyed
by origin/main sha only; `git fetch` once per process.
"""
import hashlib, json, re, subprocess, sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/STRUCT-NGEN-2026-10-20.md'
NMAX = 20
# per-generation content: (# Weyl colour (anti)triplets, # Weyl SU(2) doublets, Weyl count, complex scalar doublets)
CONTENT = {
    'SM':      {'trip': 4, 'doub': 4, 'weyl': 15, 'hdoub': 1},
    'SM+nuc':  {'trip': 4, 'doub': 4, 'weyl': 16, 'hdoub': 1},
    'R331':    {'trip': 6, 'L3': 4, 'weyl': 15, 'h3': 3},
}
TRIALITY = {'Ubar': (-1, 3), 'Q': (0, 6), 'Dbar': (1, 3), 'L': (-1, 2), 'Ebar': (-1, 1)}  # 1808.00009 Table 1 x mult.

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
    m = re.search(r'ngen_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

def b0_su3c(c, N):
    guard()
    return Fr(11) - Fr(2, 3) * Fr(1, 2) * c['trip'] * N

def b0_su2(c, N):
    guard()
    return Fr(22, 3) - Fr(2, 3) * Fr(1, 2) * c['doub'] * N - Fr(1, 3) * Fr(1, 2) * c['hdoub']

def b0_su3L(c, N):
    guard()
    return Fr(11) - Fr(2, 3) * Fr(1, 2) * c['L3'] * N - Fr(1, 3) * Fr(1, 2) * c['h3']

def b1_qcd(c, N):
    guard()
    nf = Fr(c['trip'], 2) * N
    return Fr(102) - Fr(38, 3) * nf

def witten_ok(c, N):
    guard()
    return (c['doub'] * N) % 2 == 0

def acc_blind(c, N):
    guard()
    return True   # perturbative ACC hold per generation (STRUCT-1/2; Lean STRUCT3.acc_ngen_blind)

def anomaly331(N):
    guard()
    return any(N + 3 * a == 3 * (N - a) for a in range(N + 1))

def triality_ok(N):
    guard()
    per = sum(r * m for r, m in TRIALITY.values())
    return (per * N) % 9 == 0

def z16_ok(c, N):
    guard()
    return (c['weyl'] * N) % 16 == 0

def km_ok(N):
    guard()
    return (N - 1) * (N - 2) // 2 > 0 if N >= 2 else False

def window(content, variant):
    guard()
    c = CONTENT[content]; out = []
    for N in range(1, NMAX + 1):
        if content == 'R331':
            ok = anomaly331(N) and b0_su3c(c, N) > 0 and b0_su3L(c, N) > 0
            if variant != 'core':
                ok = ok and (b1_qcd(c, N) > 0 if variant == '+BZ' else True)
                if variant in ('+triality', '+Z16'):
                    return None
        else:
            ok = acc_blind(c, N) and witten_ok(c, N) and b0_su3c(c, N) > 0 and b0_su2(c, N) > 0
            if variant == '+BZ': ok = ok and b1_qcd(c, N) > 0
            if variant == '+triality': ok = ok and triality_ok(N)
            if variant == '+Z16': ok = ok and z16_ok(c, N)
            if variant == '+KM(E)': ok = ok and km_ok(N)
        if ok: out.append(N)
    return out

def label(variant, w):
    guard()
    if w is None: return 'N/A'
    if w != [3]: return 'NOT-3'
    return {'core': 'FORCES-3', '+BZ': 'DYNAMICAL-3', '+triality': 'CONDITIONAL-3', '+Z16': 'CONDITIONAL-3', '+KM(E)': 'EMPIRICAL-3'}[variant]

def verdict(sm_core, rival_core):
    guard()
    v = 'FORCES-3 (SM, consistency only)' if sm_core == [3] else 'NOT-FORCED (SM, consistency only)'
    r = 'RIVAL-SINGLES-OUT-3' if rival_core == [3] else 'RIVAL-NOT-3'
    return v, r

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    if mode == 'planted':
        ok = True
        w = window('SM', '+KM(E)'); good = w == [3, 4, 5]; ok &= good
        print(f"planted STRUCT-3 window AF & KM = {w} (expect [3, 4, 5]): {'OK' if good else 'FAIL'}")
        b = b0_su2(CONTENT['SM'], 3); good = b == Fr(19, 6); ok &= good
        print(f"planted b0(SU2) at N=3 = {b} (expect 19/6): {'OK' if good else 'FAIL'}")
        m = max(N for N in range(0, NMAX + 1) if b0_su3c(CONTENT['SM'], N) > 0); good = m == 8; ok &= good
        print(f"planted AF(SU3) max N = {m} (expect 8): {'OK' if good else 'FAIL'}")
        s = sum(r * mm for r, mm in TRIALITY.values()); good = s == -3; ok &= good
        print(f"planted triality residue per generation = {s} (expect -3, 1808.00009 '3 per generation'): {'OK' if good else 'FAIL'}")
        good = anomaly331(3) and not anomaly331(2) and anomaly331(6); ok &= good
        print(f"planted 331 anomaly: N=3 {anomaly331(3)}, N=2 {anomaly331(2)}, N=6 {anomaly331(6)}: {'OK' if good else 'FAIL'}")
        good = b1_qcd(CONTENT['SM'], 3) == Fr(26); ok &= good
        print(f"planted QCD b1 at n_f=6 = {b1_qcd(CONTENT['SM'], 3)} (expect 26): {'OK' if good else 'FAIL'}")
        print('PLANTED', 'ALL OK' if ok else 'FAILED')
    elif mode == 'broken':
        w = window('SM', 'core')
        print(f"broken claim 'the SM unconditional consistency set forces N_gen = 3': window = {w}")
        print('BROKEN', 'ACCEPTED (checker defective)' if w == [3] else 'REJECTED (as required; Lean STRUCTNGen.sm_core_not_forced)')
    else:
        res = {}
        for content in CONTENT:
            for variant in ('core', '+BZ', '+triality', '+Z16'):
                w = window(content, variant); res[(content, variant)] = w
                print(f"{content:7s} {variant:10s} window = {w}  -> {label(variant, w)}")
        print(f"report-only E: SM + KM CP (empirical) window = {window('SM', '+KM(E)')}")
        v, r = verdict(res[('SM', 'core')], res[('R331', 'core')])
        hits = [f"{c}{vv}" for (c, vv), w in res.items() if w == [3]]
        print('windows equal to {3}:', hits, f'({len(hits)} of {sum(1 for w in res.values() if w is not None)} evaluated trials)')
        print('VERDICT:', v, '|', r)

if __name__ == '__main__':
    main()
