"""RP-TN-1 locked checker (exact rational arithmetic, CPU only).
Question: on a finite window of reflection-positive (OS) correlators f(t) = sum_k w_k lam_k^t, does total nonnegativity (TN,
the Gr>=0 positivity notion) of the OS Gram/Hankel matrix H0 = [f(i+j)]_{i,j<4} carry anything beyond the transfer-positivity
Krylov criterion RP2 = (H0 PSD and H1 = [f(i+j+1)]_{i,j<3} PSD)?
Prereg: prereg/RP-TN-1-reflection-positivity-total-nonnegativity-2026-10-30.md. Modes: planted | broken | live (each guarded)."""
import sys, json, random, itertools
from fractions import Fraction as F
from pathlib import Path
HERE = str(Path(__file__).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guard import guard
PREREG = 'prereg/RP-TN-1-reflection-positivity-total-nonnegativity-2026-10-30.md'
OUT = Path(__file__).resolve().parent
N, TMAX, SEED, NPER = 4, 6, 20261030, 1000

def corr(nodes, w):
    return [sum(F(wk) * F(l) ** t for l, wk in zip(nodes, w)) for t in range(TMAX + 1)]
def det(M):
    n = len(M)
    if n == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(n) if M[0][j] != 0)
def minors(M, principal_only=False, maxk=None):
    n = len(M)
    for k in range(1, (maxk or n) + 1):
        for R in itertools.combinations(range(n), k):
            for C in ([R] if principal_only else itertools.combinations(range(n), k)):
                yield det([[M[i][j] for j in C] for i in R])
def tn(M, V):
    if V.get('tn_principal_only'): return all(m >= 0 for m in minors(M, True))
    if V.get('strict'): return all(m > 0 for m in minors(M))
    return all(m >= 0 for m in minors(M))
def psd(M): return all(m >= 0 for m in minors(M, True))
def mats(f, V):
    if V.get('hankel_as_toeplitz'): H0 = [[f[abs(i - j)] for j in range(N)] for i in range(N)]
    else: H0 = [[f[i + j] for j in range(N)] for i in range(N)]
    H1 = [[f[i + j + (0 if V.get('wrong_window') else 1)] for j in range(N - 1)] for i in range(N - 1)]
    Tz = [[f[abs(i - j)] for j in range(N)] for i in range(N)]
    return H0, H1, Tz
def labels(nodes, w, V):
    f = corr(nodes, w); H0, H1, Tz = mats(f, V)
    rp2 = psd(H0) if V.get('rival_H0_only') else (psd(H0) and psd(H1))
    return dict(TN=tn(H0, V), RP2=rp2, H0PSD=psd(H0), TzTN2=all(m >= 0 for m in minors(Tz, maxk=2)))
def ensemble(V):
    if V.get('empty'): return []
    r = random.Random(SEED); out = []
    for cls in ('P', 'R'):
        pool = [F(k, 12) for k in (range(1, 12) if cls == 'P' else [k for k in range(-11, 12) if k != 0])]
        while sum(1 for c, _, _ in out if c == cls) < NPER:
            K = r.choice([2, 3, 4]); nodes = r.sample(pool, K); w = [F(r.randint(1, 6), 6) for _ in range(K)]
            if cls == 'R' and not any(l < 0 for l in nodes): continue
            out.append((cls, nodes, w))
    return out
def verdict(s):
    if not s['planted_ok']: return 'ILL-DEFINED'
    if s['n_tn_true'] < 50 or s['n_tn_false'] < 50: return 'ILL-DEFINED'
    if s['P_TN'] < 1: return 'NO-BRIDGE'
    if s['W'] > 0: return 'TN-WEAKER'
    if s['E'] > 0: return 'TN-EXTRA'
    if s['E'] == 0 and s['W'] == 0: return 'TN-TAUT'
    return 'UNCLASSIFIED'
PLANTED = [  # (id, nodes, weights, expected labels subset)
    ('P1', [F(1, 2)], [1], dict(TN=True, RP2=True, TzTN2=True)),
    ('P2', [F(1, 3), F(2, 3)], [1, 1], dict(TN=True, RP2=True, TzTN2=False)),
    ('P3', [F(-1, 2)], [1], dict(TN=False, RP2=False, H0PSD=True)),
    ('P4', [F(1, 2), F(-1, 2)], [1, 1], dict(TN=False, RP2=False, H0PSD=True)),
    ('P9', [F(1, 5), F(3, 5), F(9, 10)], [F(1, 6), 1, 1], dict(TN=True, RP2=True)),
    ('P10', [F(1, 5), F(4, 5)], [1, 2], dict(TzTN2=False, TN=True)),
]
def _suite(V):
    guard(PREREG, HERE)
    res = {}
    for pid, nodes, w, exp in PLANTED:
        got = labels(nodes, w, V); res[pid] = all(got[k] == v for k, v in exp.items())
    # P5 valid alternative: operator normalisation (weights x3) leaves labels unchanged
    res['P5'] = labels([F(1, 4), F(3, 4)], [1, 1], V) == labels([F(1, 4), F(3, 4)], [3, 3], V)
    # P6 joint reversal J H J preserves TN
    for nodes in ([F(1, 3), F(2, 3)], [F(1, 2), F(-1, 2)]):
        H0 = mats(corr(nodes, [1, 1]), V)[0]; J = [r[::-1] for r in H0[::-1]]
        res.setdefault('P6', True); res['P6'] &= tn(H0, V) == tn(J, V)
    # P7 gate self-tests on hand-fed matrices (PSD/TN true and false)
    res['P7'] = (psd([[1, 2], [2, 1]]) is False and tn([[1, 2], [2, 1]], V) is False and psd([[1, 1], [1, 1]]) and tn([[1, 1], [1, 1]], V))
    # P8 verdict-map self-test
    b = dict(planted_ok=True, n_tn_true=60, n_tn_false=60, P_TN=1, W=0, E=0)
    res['P8'] = (verdict(dict(b, planted_ok=False)) == 'ILL-DEFINED' and verdict(dict(b, n_tn_false=0)) == 'ILL-DEFINED'
                 and verdict(dict(b, P_TN=F(99, 100))) == 'NO-BRIDGE' and verdict(dict(b, W=1)) == 'TN-WEAKER'
                 and verdict(dict(b, E=1)) == 'TN-EXTRA' and verdict(b) == 'TN-TAUT')
    return res
def _run(V):
    guard(PREREG, HERE)
    ens = ensemble(V); rows = []
    for cls, nodes, w in ens:
        L = labels(nodes, w, V); rows.append((cls, L))
    nP = sum(1 for c, _ in rows if c == 'P'); nR = len(rows) - nP
    s = dict(planted_ok=all(_suite(V).values()), N=len(rows), nP=nP, nR=nR,
             n_tn_true=sum(L['TN'] for _, L in rows), n_tn_false=sum(not L['TN'] for _, L in rows),
             P_TN=F(sum(L['TN'] for c, L in rows if c == 'P'), nP) if nP else F(0),
             E=sum(1 for _, L in rows if not L['TN'] and L['RP2']), W=sum(1 for _, L in rows if L['TN'] and not L['RP2']),
             agree=sum(1 for _, L in rows if L['TN'] == L['RP2']),
             R_det=sum(1 for c, L in rows if c == 'R' and not L['TN']), R_rp2fail=sum(1 for c, L in rows if c == 'R' and not L['RP2']),
             P_Tz_fail=sum(1 for c, L in rows if c == 'P' and not L['TzTN2']), H0PSD_all=all(L['H0PSD'] for _, L in rows))
    if rows:
        pt = F(s['n_tn_true'], len(rows)); pr = F(sum(L['RP2'] for _, L in rows), len(rows))
        s['null_agree_independent'] = float(pt * pr + (1 - pt) * (1 - pr))
    s['verdict'] = verdict(s)
    return {k: (float(v) if isinstance(v, F) else v) for k, v in s.items()}
VARIANTS = ['tn_principal_only', 'hankel_as_toeplitz', 'rival_H0_only', 'strict', 'wrong_window', 'empty']
def planted():
    guard(PREREG, HERE)
    r = _suite({}); r['ALL_OK'] = all(r.values()); return r
def broken():
    guard(PREREG, HERE)
    out = {}
    for b in VARIANTS:
        if b == 'empty': out[b] = _run({b: True})['verdict']; continue
        r = _suite({b: True}); out[b] = sorted(k for k, v in r.items() if not v)
    out['ALL_REJECTED'] = all(out[b] for b in VARIANTS if b != 'empty') and out['empty'] == 'ILL-DEFINED'
    return out
def live():
    guard(PREREG, HERE)
    return _run({})
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode not in ('planted', 'broken', 'live'): sys.exit('usage: planted|broken|live')
    guard(PREREG, HERE)
    r = {'planted': planted, 'broken': broken, 'live': live}[mode]()
    (OUT / f'rptn1_{mode}.json').write_text(json.dumps(r, indent=1, default=str)); print(json.dumps(r, default=str))
