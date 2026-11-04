#!/usr/bin/env python3
"""LEAN-CERT-2 convention-invariance re-check (CONV-LEANCERT2-2026-10-30-r1; author approved (2026-10-30)).
Prereg: prereg/CONV-LEAN-CERT-2-canonical-class-2026-10-30.md.  SUPERSEDES (does not edit) the N2 null step of the locked
sims/leancert2/leancert2_checker.py (imported read-only; its own guard still runs).
Equivalence: certificates (M,K,P,Q,d) and (M,K,P',Q,d) with P M = P' M are the same certificate class: validity
(MK=0, PM+KQ=dI, QK=dI) depends on P only through PM (Lean LeanCertConv.valid_iff_of_PM_eq).  Canonical class key
(K, PM, Q, d) (deviation from the screened 'Hermite/Smith normal form': PM is the minimal invariant; noted).
N2' : replay the locked N2 loop exactly (seed 20261028, 60 corruptions per certificate, order (k, sigma=+1 first)) and
count an accepted corruption only if the class key changes.  Expected 0/480 -> FLIPPED to CERTS-OK (python).
Planted: PL1 key unchanged by a P edit in a zero row of M (and still valid); PL2 key changes on any K/Q edit; PL3 raw
replay reproduces the locked 131.  Broken: raw-P key must give 131 (i.e. reproduce the locked failure).
Rival: zero-row canonicalisation (zero P columns at zero rows of M before keying)."""
import importlib.util, json, random, sys, time
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path.insert(0, str(HERE.parent))
from conv_guard import guard as _g, REPO
PREREG = 'prereg/CONV-LEAN-CERT-2-canonical-class-2026-10-30.md'
def guard(): return _g(PREREG, HERE)
sys.path.insert(0, str(REPO / 'sims/leancert2'))
import leancert2_checker as C
from emit_lean import parse_certs
def matmul(A, B): return tuple(tuple(sum(a * B[t][j] for t, a in enumerate(r)) for j in range(len(B[0]))) for r in A)
T = lambda X: tuple(tuple(r) for r in X)
def key(c):
    guard(); return (T(c['Kr']), matmul(c['Pr'], c['Mr']), T(c['Qr']), c['d'])
def key_raw(c):
    guard(); return (T(c['Kr']), T(c['Pr']), T(c['Qr']), c['d'])
def key_zr(c):
    guard(); z = [all(x == 0 for x in r) for r in c['Mr']]
    return (T(c['Kr']), tuple(tuple(0 if z[j] else x for j, x in enumerate(r)) for r in c['Pr']), T(c['Qr']), c['d'])
def run():
    guard(); t = time.time()
    blocks = parse_certs(REPO / 'sims/leancert2/certs_lean.txt')
    order = sorted(blocks, key=lambda s: (int(s[7]), s[8] == 'm'))
    rng = random.Random(20261028); _ = C.primes_from(2**30 + 3, 20)
    out = {'per_cert': {}, 'planted': {}}; tot = {'accepted': 0, 'key': 0, 'raw': 0, 'zr': 0}
    for name in order:
        b = blocks[name]
        c = dict(Mr=b['M'], Kr=b['K'], Pr=b['P'], Qr=b['Q'], d=b['d'], m=b['m'], n=b['n'], k=b['k'],
                 Kc=[[r[j] for r in b['K']] for j in range(b['k'])], rank=b['n'] - b['k'])
        k0, r0, z0 = key(c), key_raw(c), key_zr(c)
        # planted
        zrows = [j for j, r in enumerate(c['Mr']) if all(x == 0 for x in r)]
        pl = {}
        if zrows:
            P2 = [list(r) for r in c['Pr']]; P2[0][zrows[0]] += 1; c2 = dict(c, Pr=P2)
            pl['PL1_zero_row_P_edit_valid_same_key'] = C.mirror_check(c2) and key(c2) == k0
        if c['Kr'] and c['Kr'][0]:
            K2 = [list(r) for r in c['Kr']]; K2[0][0] += 1
            pl['PL2_K_edit_changes_key'] = key(dict(c, Kr=K2)) != k0
        out['planted'][name] = pl
        acc = cnt = cr = cz = 0
        for _ in range(60):
            which = rng.choice([w for w in ('Kr', 'Pr', 'Qr') if c[w] and c[w][0]])
            mat = [list(r) for r in c[which]]
            i = rng.randrange(len(mat)); j = rng.randrange(len(mat[0]))
            mat[i][j] += rng.choice((-1, 1)); cc = dict(c, **{which: mat})
            if C.mirror_check(cc):
                acc += 1; cnt += key(cc) != k0; cr += key_raw(cc) != r0; cz += key_zr(cc) != z0
        out['per_cert'][name] = {'accepted': acc, 'class_changed': cnt, 'raw_key_changed': cr, 'zero_row_key_changed': cz}
        for a, v in zip(tot, (acc, cnt, cr, cz)): tot[a] += v
    out['totals'] = tot
    out['PLANTED_OK'] = all(all(p.values()) and p for p in out['planted'].values()) and tot['accepted'] == 131
    out['BROKEN_raw_key_reproduces_131'] = tot['raw'] == 131
    out['RIVAL_zero_row_key'] = f"{tot['zr']}/480"
    out['N2prime'] = f"{tot['key']}/480"
    ok = out['PLANTED_OK'] and out['BROKEN_raw_key_reproduces_131']
    out['OUTCOME'] = ('FLIPPED (python CERTS-OK)' if tot['key'] == 0 else 'CONVENTION-ROBUST (ILL-DEFINED stands)') if ok else 'GATE-FAIL'
    out['seconds'] = round(time.time() - t, 1)
    print(json.dumps(out, indent=1)); (HERE.parent / 'leancert2_conv_live.json').write_text(json.dumps(out, indent=1))
if __name__ == '__main__': run()
