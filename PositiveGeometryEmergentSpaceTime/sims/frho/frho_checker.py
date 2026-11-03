#!/usr/bin/env python3
"""F-RHOWIDTH locked checker: zero-parameter rho width ratio Gamma_rho/m_rho of the Lovelace-Shapiro (LS) amplitude
with the F-SCATLEN normalisation N1 (lambda = -1/(2 pi alpha' F^2)), vs KSRF and dispersive POLE data.

Target r = Gamma/m (POLE definition: m = Re sqrt(s_pole), Gamma = -2 Im sqrt(s_pole)); inputs x = m_pi/m, f = F/m.
Gamma = g^2 p^3 / (6 pi m^2), p = sqrt(m^2/4 - m_pi^2)  =>  r = g^2 (1/4 - x^2)^(3/2) / (6 pi).
LS: g^2 extracted NUMERICALLY from the full amplitude: g^2 = lim (m^2 - s) T1(s,t,u) / (2 (t - u)),
    T1 = A(t,s,u) - A(u,t,s), A = lam [V(s,t) + V(s,u) - V(t,u)]  (Lean FRhoWidth: g^2 = 1/(2 pi alpha' F^2)).
KSRF: g^2 = m^2 / (2 F^2)  =>  r = (1/4 - x^2)^(3/2) / (12 pi f^2).
Modes: planted | broken | live.  mpmath 60 digits.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main. No pass flag; caches keyed
by origin/main sha only; `git fetch` once per process.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
import mpmath as mp
mp.mp.dps = 60

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/F-RHOWIDTH-2026-10-20.md'
DCHI2 = mp.mpf('7.879')     # chi2_1 quantile p = 0.005 (= 0.01 Bonferroni over 2 model trials P_a, P_b)
ZMAX = 3

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
    m = re.search(r'frho_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- amplitude and coupling ----------
def V(al_s, al_t):
    guard()
    return mp.gamma(1 - al_s) * mp.gamma(1 - al_t) * mp.rgamma(1 - al_s - al_t)

def A(model, s, t, u):
    guard()
    a0, ap, F2 = model
    al = lambda x: a0 + ap * x
    lam = -1 / (2 * mp.pi * ap * F2)
    return lam * (V(al(s), al(t)) + V(al(s), al(u)) - V(al(t), al(u)))

def g2_ls(model, mr2, mp2):
    """Numerical rho residue: (m^2 - s) T1 / (2 (t - u)) at s = m^2 (1 - 1e-25), cos(theta) = 0.3."""
    guard()
    s = mr2 * (1 - mp.mpf('1e-25'))
    q2 = s / 4 - mp2
    t = -2 * q2 * (1 - mp.mpf('0.3')); u = 4 * mp2 - s - t
    T1 = A(model, t, s, u) - A(model, u, t, s)
    return (mr2 - s) * T1 / (2 * (t - u))

def models(m_pi, m_rho, F):
    guard()
    m2, r2, F2 = m_pi ** 2, m_rho ** 2, F ** 2
    apa = 1 / (2 * (r2 - m2))
    return {'P_a': (1 - apa * r2, apa, F2), 'P_b': (mp.mpf(1) / 2, 1 / (2 * r2), F2)}

def ratio_from_g2(g2, m_pi, m_rho):
    guard()
    x = m_pi / m_rho
    return g2 * (mp.mpf(1) / 4 - x ** 2) ** mp.mpf(1.5) / (6 * mp.pi)

def predict(m_pi, m_rho, F):
    guard()
    out = {}
    for n, md in models(m_pi, m_rho, F).items():
        out[n] = ratio_from_g2(g2_ls(md, m_rho ** 2, m_pi ** 2), m_pi, m_rho)
    out['KSRF'] = ratio_from_g2(m_rho ** 2 / (2 * F ** 2), m_pi, m_rho)
    return out

# ---------- scoring ----------
def z(pred, perr, x, ex):
    guard()
    return (pred - x) / mp.sqrt(ex ** 2 + perr ** 2)

def classify(z_m, z_k):
    guard()
    d = z_k ** 2 - z_m ** 2
    if d > DCHI2:
        return 'BEATS-KSRF' if abs(z_m) <= ZMAX else 'IMPROVES-BUT-EXCLUDED'
    if -d > DCHI2:
        return 'WORSE-THAN-KSRF'
    return 'MATCHES-KSRF'

def overall(c1, c2):
    guard()
    if c1 != c2:
        return 'UNCLASSIFIED-SPLIT'
    return {'BEATS-KSRF': 'PASS-BEATS-KSRF', 'MATCHES-KSRF': 'MATCH-KSRF (CITED/expected; implied by KSRF)',
            'WORSE-THAN-KSRF': 'FAIL-WORSE-THAN-KSRF', 'IMPROVES-BUT-EXCLUDED': 'FAIL-EXCLUDED'}[c1]

# ---------- modes ----------
def planted():
    guard_banner()
    spec = json.loads((HERE.parent / 'planted_cases.json').read_text())
    ok = True
    for c in spec['residue']:
        mpi, mr, F = (mp.mpf(c[k]) for k in ('m_pi', 'm_rho', 'F'))
        md = models(mpi, mr, F)[c['model']]
        g2 = g2_ls(md, mr ** 2, mpi ** 2)
        exp = eval(c['g2_expr'], {'pi': mp.pi, 'mpf': mp.mpf})
        good = abs(g2 - exp) < mp.mpf('1e-15')
        print(f"planted residue {c['name']}: g2 = {mp.nstr(g2, 15)} expect {mp.nstr(exp, 15)} -> {'OK' if good else 'FAIL'}")
        ok &= good
    k = spec['ksrf']
    r = predict(mp.mpf(k['m_pi']), mp.mpf(k['m_rho']), mp.mpf(k['F']))['KSRF']
    exp = eval(k['r_expr'], {'pi': mp.pi, 'mpf': mp.mpf})
    good = abs(r - exp) < mp.mpf('1e-30')
    print(f"planted KSRF width: r = {mp.nstr(r, 15)} expect {mp.nstr(exp, 15)} -> {'OK' if good else 'FAIL'}"); ok &= good
    for c in spec['classifier']:
        got = classify(mp.mpf(c['z_m']), mp.mpf(c['z_k']))
        print(f"classifier {c['name']}: {got} expect {c['expect']} -> {'OK' if got == c['expect'] else 'FAIL'}")
        ok &= got == c['expect']
    print('PLANTED:', 'RECOVERED' if ok else 'NOT RECOVERED (rung ILL-DEFINED)')
    return ok

def broken():
    guard_banner()
    b = json.loads((HERE.parent / 'planted_cases.json').read_text())['broken']
    mpi, mr, F = (mp.mpf(b[k]) for k in ('m_pi', 'm_rho', 'F'))
    g2 = g2_ls(models(mpi, mr, F)['P_a'], mr ** 2, mpi ** 2)
    claim = mr ** 2 / (2 * F ** 2)
    holds = abs(g2 - claim) < mp.mpf('1e-6')
    print(f"broken {b['name']}: g2_LS = {mp.nstr(g2, 12)} vs claimed KSRF {mp.nstr(claim, 12)} -> {'ACCEPTED (BAD)' if holds else 'REJECT'}")
    return not holds

def live():
    guard_banner()
    p = HERE.parent / 'inputs.json'
    if not p.exists():
        sys.exit("live: inputs.json missing")
    raw = p.read_bytes(); print('inputs.json sha256', hashlib.sha256(raw).hexdigest())
    I = json.loads(raw)
    mpi = mp.mpf(json.loads((REPO / 'sims/fdimm/masses.json').read_text())['sets']['S1']['m_pi'])
    Fpi = json.loads((REPO / 'sims/fscat/inputs.json').read_text())['F_pi']
    F1, dF1, F2v = mp.mpf(Fpi['F1']['F']), mp.mpf(Fpi['F1']['dF']), mp.mpf(Fpi['F2']['F'])
    res = {}
    for dk, d in I['sets'].items():
        m, dm, G, dG = (mp.mpf(d[k]) for k in ('m', 'dm', 'Gamma', 'dGamma'))
        r_data = G / m; dr = r_data * mp.sqrt((dG / G) ** 2 + (dm / m) ** 2)
        P1, P2 = predict(mpi, m, F1), predict(mpi, m, F2v)
        zs = {}
        for n in ('P_a', 'P_b', 'KSRF'):
            pe = mp.sqrt((2 * P1[n] * dF1 / F1) ** 2 + ((P1[n] - P2[n]) / 2) ** 2)
            zs[n] = z(P1[n], pe, r_data, dr)
            print(f"[{dk}] {n}: r = {mp.nstr(P1[n], 6)} +- {mp.nstr(pe, 2)} (Gamma = {mp.nstr(P1[n] * m, 5)} MeV); data r = {mp.nstr(r_data, 6)} +- {mp.nstr(dr, 2)}; z = {mp.nstr(zs[n], 4)}")
        print(f"[{dk}] g2_LS(P_a)/g2_KSRF = {mp.nstr(P1['P_a'] / P1['KSRF'], 8)}; (2/pi)(1 - x^2) = {mp.nstr(2 / mp.pi * (1 - (mpi / m) ** 2), 8)}")
        if d.get('role') == 'verdict':
            res[dk] = {n: classify(zs[n], zs['KSRF']) for n in ('P_a', 'P_b')}
            print(f"[{dk}] class vs KSRF: {res[dk]}")
        else:
            print(f"[{dk}] report-only ({d.get('role')}): class would be " + str({n: classify(zs[n], zs['KSRF']) for n in ('P_a', 'P_b')}))
    ks = list(res)
    for n in ('P_a', 'P_b'):
        print(f"overall {n}: {overall(res[ks[0]][n], res[ks[1]][n])}")
    print(f"VERDICT (P_a, LS trunk): {overall(res[ks[0]]['P_a'], res[ks[1]]['P_a'])}")

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'planted'
    if mode == 'planted':
        r = planted(); rb = broken(); sys.exit(0 if r and rb else 1)
    if mode == 'broken':
        sys.exit(0 if broken() else 1)
    if mode == 'live':
        live(); sys.exit(0)
    sys.exit('mode?')
