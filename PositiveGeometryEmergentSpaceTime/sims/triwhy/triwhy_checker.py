#!/usr/bin/env python3
"""TRIALITY-WHY locked checker (continuous-mode own pick (author approved 2026-10-23)).
Question: is there a CONSISTENCY (K-class, not phenomenological) reason to gauge baryon triality B3, i.e. a declared
mechanism whose N_gen window is a proper subset of the SM core window {1..5} containing 3?
Charges: generation-universal Z_k, left-handed Weyl fields; qQ, qL, qH free; Yukawas fix qU = qH - qQ,
qD = -qQ - qH, qE = -qL - qH, qN = qH - qL.  Doublet charge c = 3 qQ + qL.
Trials (prereg, declared finite list; any undeclared mechanism stays OPEN):
  T1 [K]  exactness vs gauge-linear: for every (k, qQ, qL, qH) in the scan, the set of N in 1..20 where the
          SU(2) instanton vertex is Z_k-invariant (k | N c) equals the set where the Ibanez-Ross SU(2)^2-Z_k sum
          (sum over doublet components, N generations) vanishes mod k.  Also SU(3)^2-Z_k sum == 0 and
          gravity^2-Z_k sum with nu^c == 0 for all charges.  TAUT = all equal.
  T2 [C]  Dai-Freed Z_9 (3B) window (1808.00009, CITED: anomaly-free iff 3 | N) vs T1 exactness window of Z_9(3B).
  T3 [K-conj] no-global-symmetries dichotomy (exact global => gauged OR broken): BREAK = some SM-gauge-invariant
          dim-6 baryon-violating operator has B3 charge != 0 mod 3; then W_QG = core window, else W_QG = core cap 3Z.
  T4 [geometry] real column torus: number of real roots of x^3 = 1 (Z3 through a real torus); cyclic Z_n of
          Gr+(k,n), n = 4..20: fraction with 3 | n (FAMILY-CONSTANT iff fraction in {0, 1}).
  T5 [E]  proton stability (phenomenological): reported only, excluded from forcing by the gate.
Null: family {(k, c): 2 <= k <= 18, 0 <= c < k} (170 pairs, uniform); window = multiples of d = k / gcd(k, c);
  P3 = P(window cap {1..5} == {3}); P_used = 0.3 * P_naive is NOT applied to the null (it is the base rate).
Rival ORDER: "window = multiples of k / gcd(k, c)" (no physics input) must reproduce every T1/T2 window.
Rule: WELL-POSED iff all planted OK (else ILL-DEFINED).  W_K = intersection over K trials of their windows within
  core {1..5}.  FORCED-K iff W_K is a proper subset of core, contains 3, and P3 (Bonferroni x5 trials) < 0.01.
  NOT-FORCED / TAUTOLOGICAL-CONDITION iff W_K == core and TAUT and BREAK and (T4 blind) and ORDER reproduces all.
  NOT-FORCED / OTHER iff W_K == core but some of TAUT/BREAK/blind/ORDER false.  Otherwise UNCLASSIFIED.
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main.  No pass flag; caches
keyed by origin/main sha only; `git fetch` once per process.
"""
import hashlib, re, subprocess, sys
from fractions import Fraction as Fr
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/TRIALITY-WHY-2026-10-23.md'
CORE = frozenset(range(1, 6))
NRANGE = range(1, 21)

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
    m = re.search(r'triwhy_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- content ----------
# physical hypercharge and baryon number of the LH Weyl fields
Y = {'Q': Fr(1, 6), 'U': Fr(-2, 3), 'D': Fr(1, 3), 'L': Fr(-1, 2), 'E': Fr(1), 'N': Fr(0), 'H': Fr(1, 2)}
B = {'Q': Fr(1, 3), 'U': Fr(-1, 3), 'D': Fr(-1, 3), 'L': Fr(0), 'E': Fr(0), 'N': Fr(0), 'H': Fr(0)}
# (colour dim, SU(2) dim) of each LH Weyl multiplet
REP = {'Q': (3, 2), 'U': (3, 1), 'D': (3, 1), 'L': (1, 2), 'E': (1, 1), 'N': (1, 1)}
# B3 = R3 L3 of hep-ph/0512163 eq. (2.17), (m, n, p) = (1, 0, 1): qU = -m, qD = m - n, qL = -n - p, qE = m + p
B3 = {'Q': 0, 'U': -1, 'D': 1, 'L': -1, 'E': 2}

def charges(qQ, qL, qH):
    guard()
    return {'Q': qQ, 'U': qH - qQ, 'D': -qQ - qH, 'L': qL, 'E': -qL - qH, 'N': qH - qL, 'H': qH}

def sphaleron_charge(qQ, qL, N):
    """charge of the SU(2) instanton 't Hooft vertex: one zero mode per doublet per generation."""
    guard()
    return N * (REP['Q'][0] * qQ + qL)

def wwx_sum(ch, N):
    """Ibanez-Ross SU(2)^2-Z_k: sum over SU(2) doublets (each colour copy), N generations."""
    guard()
    return N * sum(REP[f][0] * ch[f] for f in REP if REP[f][1] == 2)

def ccx_sum(ch):
    """SU(3)^2-Z_k: sum over colour triplets (each SU(2) copy), one generation."""
    guard()
    return sum(REP[f][1] * ch[f] for f in REP if REP[f][0] == 3)

def grav_sum(ch, with_nuc=True):
    guard()
    return sum(REP[f][0] * REP[f][1] * ch[f] for f in REP if with_nuc or f != 'N')

def window_exact(k, qQ, qL):
    guard()
    return frozenset(N for N in NRANGE if sphaleron_charge(qQ, qL, N) % k == 0)

def window_wwx(k, qQ, qL, qH):
    guard()
    ch = charges(qQ, qL, qH)
    return frozenset(N for N in NRANGE if wwx_sum(ch, N) % k == 0)

def window_order(k, c):
    guard()
    d = k // gcd(k, c % k) if c % k else 1
    return frozenset(N for N in NRANGE if N % d == 0)

def trial_T1():
    """all arithmetic inline (one guard per call; per-element helpers would make ~10^6 guarded git calls)."""
    guard()
    n = bad = ccx_bad = grav_bad = 0
    for k in range(2, 19):
        for qQ in range(k):
            for qL in range(k):
                ex = frozenset(N for N in NRANGE if (N * (3 * qQ + qL)) % k == 0)
                for qH in range(k):
                    n += 1
                    ch = {'Q': qQ, 'U': qH - qQ, 'D': -qQ - qH, 'L': qL, 'E': -qL - qH, 'N': qH - qL}
                    dsum = sum(REP[f][0] * ch[f] for f in REP if REP[f][1] == 2)
                    ww = frozenset(N for N in NRANGE if (N * dsum) % k == 0)
                    bad += ex != ww
                    ccx_bad += sum(REP[f][1] * ch[f] for f in REP if REP[f][0] == 3) != 0
                    grav_bad += sum(REP[f][0] * REP[f][1] * ch[f] for f in REP) != 0
    return {'n': n, 'mismatch': bad, 'ccx_nonzero': ccx_bad, 'grav_nuc_nonzero': grav_bad,
            'TAUT': bad == 0 and ccx_bad == 0 and grav_bad == 0}

def trial_T2():
    guard()
    df = frozenset(N for N in NRANGE if N % 3 == 0)    # 1808.00009 (CITED): Z9 anomaly-free iff 3 | N
    ex = window_exact(9, 1, 0)
    return {'dai_freed': sorted(df), 'exact': sorted(ex), 'equal': df == ex}

def b3_charge(ops):
    guard()
    return sum(B3[f] for f in ops)

def op_invariants(ops):
    """(sum Y, number of colour triplets minus antitriplets mod 3, number of doublets mod 2, Delta B)."""
    guard()
    ty = sum(Y[f] for f in ops)
    col = sum(1 if f == 'Q' else -1 if f in ('U', 'D') else 0 for f in ops) % 3
    dbl = sum(1 for f in ops if REP[f][1] == 2) % 2
    return ty, col, dbl, sum(B[f] for f in ops)

DIM6_BNV = [('Q', 'Q', 'Q', 'L'), ('U', 'U', 'D', 'E'), ('Q', 'Q', 'U', 'E'), ('Q', 'L', 'U', 'D')]

def trial_T3():
    guard()
    rows = []
    for ops in DIM6_BNV:
        ty, col, dbl, db = op_invariants(ops)
        inv = ty == 0 and col == 0 and dbl == 0
        rows.append({'op': ''.join(ops), 'gauge_inv': inv, 'dB': str(db), 'B3': b3_charge(ops) % 3})
    brk = any(r['gauge_inv'] and r['dB'] != '0' and r['B3'] != 0 for r in rows)
    w = CORE if brk else frozenset(N for N in CORE if N % 3 == 0)
    return {'ops': rows, 'BREAK': brk, 'W_QG': sorted(w)}

def trial_T4():
    guard()
    # real roots of x^3 - 1 = (x - 1)(x^2 + x + 1); discriminant of the quadratic = -3 < 0
    disc = 1 - 4
    real_roots = 1 + (2 if disc > 0 else 1 if disc == 0 else 0)
    ns = list(range(4, 21))
    frac = Fr(sum(1 for n in ns if n % 3 == 0), len(ns))
    return {'real_roots_x3_1': real_roots, 'torus_blind': real_roots == 1,
            'cyclic_frac_3_div_n': str(frac), 'cyclic_family_constant': frac in (0, 1)}

def null_rate():
    guard()
    fam = [(k, c) for k in range(2, 19) for c in range(k)]
    n3 = nsing = 0
    for k, c in fam:
        d = k // gcd(k, c) if c else 1
        w = frozenset(N for N in CORE if N % d == 0)
        n3 += w == {3}
        nsing += len(w) == 1
    return {'n': len(fam), 'n3': n3, 'nsingleton': nsing, 'P3': Fr(n3, len(fam))}

def rival_order():
    """ORDER rule (k / gcd(k, c), no physics) vs direct exactness window; arithmetic inline."""
    guard()
    ok = True
    for k in range(2, 19):
        for qQ in range(k):
            for qL in range(k):
                c = (3 * qQ + qL) % k
                d = k // gcd(k, c) if c else 1
                ok &= frozenset(N for N in NRANGE if N % d == 0) == \
                    frozenset(N for N in NRANGE if (N * (3 * qQ + qL)) % k == 0)
    return ok

def classify(T1, T2, T3, T4, nul, order_ok):
    guard()
    wk = CORE & frozenset(T3['W_QG'])
    if T4['torus_blind'] is False:
        wk = wk & frozenset(N for N in CORE if N % 3 == 0)
    p_corr = min(1, 5 * nul['P3'])
    if wk < CORE and 3 in wk and p_corr < Fr(1, 100):
        return 'FORCED-K', wk, p_corr
    if wk == CORE:
        if T1['TAUT'] and T3['BREAK'] and T4['torus_blind'] and order_ok and T2['equal']:
            return 'NOT-FORCED / TAUTOLOGICAL-CONDITION (NO-GO)', wk, p_corr
        return 'NOT-FORCED / OTHER', wk, p_corr
    return 'UNCLASSIFIED', wk, p_corr

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    if mode == 'planted':
        ok = True
        w = window_exact(9, 1, 0); good = w == frozenset(N for N in NRANGE if N % 3 == 0); ok &= good
        print(f"P1 Z9(3B) exact window in 1..20 = multiples of 3 (STRUCTNGen.triality_iff): {'OK' if good else 'FAIL'}")
        neg = {f: -(B[f] - 2 * Y[f]) % 3 for f in B3}
        good = all(neg[f] == B3[f] % 3 for f in B3); ok &= good
        print(f"P2 B3 (hep-ph/0512163 eq 2.17) == -(B - 2Y) mod 3 on Q,U,D,L,E: {'OK' if good else 'FAIL'}")
        d3b = sphaleron_charge(1, 0, 3); good = d3b == 9; ok &= good
        print(f"P3 sphaleron N=3: Delta(3B) = {d3b} (Delta B = 3, Delta L_i = 1; B/3 - L_i conserved): {'OK' if good else 'FAIL'}")
        good = all(ccx_sum(charges(a, b, h)) == 0 for a in range(-3, 4) for b in range(-3, 4) for h in range(-3, 4)); ok &= good
        print(f"P4 SU(3)^2 sum == 0 for Yukawa-compatible charges: {'OK' if good else 'FAIL'}")
        good = window_exact(3, 1, -3) == frozenset(NRANGE); ok &= good
        print(f"P5 B-L (x3) exact for all N: {'OK' if good else 'FAIL'}")
        ty, col, dbl, db = op_invariants(('Q', 'Q', 'Q', 'L'))
        good = ty == 0 and col == 0 and dbl == 0 and db == 1 and b3_charge(('Q', 'Q', 'Q', 'L')) % 3 != 0; ok &= good
        print(f"P6 QQQL gauge-invariant, Delta B = 1, B3-odd (B3 forbids dim-6 proton decay): {'OK' if good else 'FAIL'}")
        ty, col, dbl, db = op_invariants(('Q', 'U', 'L'))
        good = not (ty == 0 and col == 0 and dbl == 0); ok &= good
        print(f"P7 detector: QUL (no H) is NOT gauge-invariant: {'OK' if good else 'FAIL'}")
        print("PLANTED:", "ALL OK" if ok else "FAILURE -> ILL-DEFINED")
    elif mode == 'broken':
        # declared false claim: "the gauged-triality window within the AF-SU(3) range {1..8} is {3}"
        # (already false by Lean PositiveGeometryEmergentSpaceTime.STRUCTNGen.triality_su3_only_not_forced: N = 6 passes)
        w = sorted(N for N in window_exact(9, 1, 0) if N <= 8)
        print(f"broken: Z9(3B) window within 1..8 = {w}")
        print("BROKEN:", "REJECTED" if w != [3] else "ACCEPTED (checker defective)")
    else:
        T1 = trial_T1(); print("T1", T1)
        T2 = trial_T2(); print("T2", T2)
        T3 = trial_T3(); print("T3", T3)
        T4 = trial_T4(); print("T4", T4)
        print("T5 [E] proton stability: phenomenological, excluded from forcing (reported only)")
        nul = null_rate(); print(f"NULL n = {nul['n']}, n3 = {nul['n3']}, nsingleton = {nul['nsingleton']}, P3 = {nul['P3']} ({float(nul['P3']):.4f})")
        order_ok = rival_order(); print(f"RIVAL ORDER reproduces every exactness window: {order_ok}")
        v, wk, p = classify(T1, T2, T3, T4, nul, order_ok)
        print(f"W_K = {sorted(wk)}; P3 Bonferroni x5 = {p} ({float(p):.4f})")
        print("VERDICT:", v)

if __name__ == '__main__':
    main()
