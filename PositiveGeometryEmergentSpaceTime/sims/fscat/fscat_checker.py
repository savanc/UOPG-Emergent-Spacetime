#!/usr/bin/env python3
"""F-SCATLEN locked checker: S-wave pi-pi scattering lengths a_0^0, a_0^2 of the Lovelace-Shapiro (LS) amplitude
(trunk baseline P_a and the F-DIM-MASS repair P_b), with the zero-fit normalisation N1, against data and rivals
(Weinberg LO current algebra; two-loop ChPT + Roy, CGL 2001).

Modes: planted | broken | live.   mpmath, 50 digits.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main. No pass flag; caches keyed
by origin/main sha only; `git fetch` once per process.

Amplitude (prereg section 3):  A(s,t,u) = lam [V(s,t) + V(s,u) - V(t,u)],
  V(s,t) = Gamma(1-al(s)) Gamma(1-al(t)) / Gamma(1-al(s)-al(t)),  al(s) = alpha0 + alpha' s,
  N1: lam = -1 / (2 pi alpha' F^2)  (soft matching at al = 1/2 using Gamma(1/2)^2 = pi; no fit).
  T0 = 3A(s,t,u) + A(t,s,u) + A(u,t,s);  T2 = A(t,s,u) + A(u,t,s);  a_0^I = T^I(4m^2, 0, 0) / (32 pi).
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
import mpmath as mp
mp.mp.dps = 50

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/F-SCATLEN-2026-10-20.md'
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
    m = re.search(r'fscat_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------- amplitudes ----------
def V(al_s, al_t):
    guard()
    return mp.gamma(1 - al_s) * mp.gamma(1 - al_t) * mp.rgamma(1 - al_s - al_t)

def amp(model, s, t, u):
    """model: ('ls', alpha0, alphap, F2) or ('lin', sA, F2): A = (s - sA)/F^2."""
    guard()
    if model[0] == 'lin':
        _, sA, F2 = model
        return (s - sA) / F2
    _, a0, ap, F2 = model
    al = lambda x: a0 + ap * x
    lam = -1 / (2 * mp.pi * ap * F2)
    return lam * (V(al(s), al(t)) + V(al(s), al(u)) - V(al(t), al(u)))

def scatlens(model, m2):
    """(a_0^0, a_0^2) at threshold s = 4 m^2, t = u = 0."""
    guard()
    s, t, u = 4 * m2, mp.mpf(0), mp.mpf(0)
    T0 = 3 * amp(model, s, t, u) + amp(model, t, s, u) + amp(model, u, t, s)
    T2 = amp(model, t, s, u) + amp(model, u, t, s)
    return T0 / (32 * mp.pi), T2 / (32 * mp.pi)

def models(m_pi, m_rho, F):
    guard()
    m2, r2, F2 = m_pi ** 2, m_rho ** 2, F ** 2
    apa = 1 / (2 * (r2 - m2))
    return {'P_a': ('ls', 1 - apa * r2, apa, F2),          # Adler zero at s = t = m^2 (F-DIM-MASS baseline)
            'P_b': ('ls', mp.mpf(1) / 2, 1 / (2 * r2), F2),  # Adler zero at s = t = 0 (F-DIM-MASS repair)
            'LO':  ('lin', m2, F2)}                         # Weinberg 1966 current algebra

# ---------- scoring ----------
def chi2(pred, perr, data):
    """data: list of (obs_name, value, err); pred/perr: dict obs -> value / model error. Returns chi2, pulls."""
    guard()
    c, pulls = mp.mpf(0), {}
    for name, x, ex in data:
        z = (pred[name] - x) / mp.sqrt(ex ** 2 + perr[name] ** 2)
        pulls[name] = z
        c += z ** 2
    return c, pulls

def classify(c_m, pulls_m, c_lo):
    guard()
    d = c_lo - c_m
    if d > DCHI2:
        return 'BEATS-LO' if max(abs(z) for z in pulls_m.values()) <= ZMAX else 'IMPROVES-BUT-EXCLUDED'
    if -d > DCHI2:
        return 'WORSE-THAN-LO'
    return 'MATCHES-LO'

def overall(c1, c2):
    guard()
    if c1 != c2:
        return 'UNCLASSIFIED-SPLIT'
    return {'BEATS-LO': 'PASS-BEATS-LO', 'MATCHES-LO': 'MATCH-LO (CITED/expected; not new)',
            'WORSE-THAN-LO': 'FAIL-WORSE-THAN-LO', 'IMPROVES-BUT-EXCLUDED': 'FAIL-EXCLUDED'}[c1]

def obs(a00, a02):
    return {'a00': a00, 'a02': a02, 'a00-a02': a00 - a02}

# ---------- modes ----------
def planted():
    guard_banner()
    ok = True
    spec = json.loads((HERE.parent / 'planted_cases.json').read_text())
    one, tiny = mp.mpf(1), mp.mpf('1e-12')
    for c in spec['planted']:
        if c['model'] == 'lin':
            mdl = ('lin', mp.mpf(c['sA']), one)
        else:
            mdl = ('ls', mp.mpf(c['alpha0_plus_ap_m2']) - tiny, tiny, one) if c['zero'] == 'm2' else ('ls', mp.mpf(1) / 2, tiny, one)
        a0, a2 = scatlens(mdl, one)
        got = (a0 * 32 * mp.pi, a2 * 32 * mp.pi)
        good = abs(got[0] - c['T0']) < 1e-6 and abs(got[1] - c['T2']) < 1e-6
        print(f"planted {c['name']}: 32pi(a00,a02) = ({mp.nstr(got[0], 12)}, {mp.nstr(got[1], 12)}) expect ({c['T0']}, {c['T2']}) -> {'OK' if good else 'FAIL'}")
        ok &= good
    for c in spec['classifier']:
        data = [(k, mp.mpf(v), mp.mpf(e)) for k, v, e in c['data']]
        z0 = {k: mp.mpf(0) for k in ('a00', 'a02', 'a00-a02')}
        pm = obs(mp.mpf(c['model'][0]), mp.mpf(c['model'][1])); plo = obs(mp.mpf(c['lo'][0]), mp.mpf(c['lo'][1]))
        cm, pu = chi2(pm, z0, data); cl, _ = chi2(plo, z0, data)
        got = classify(cm, pu, cl)
        print(f"classifier {c['name']}: {got} expect {c['expect']} -> {'OK' if got == c['expect'] else 'FAIL'}")
        ok &= got == c['expect']
    print('PLANTED:', 'RECOVERED' if ok else 'NOT RECOVERED (rung ILL-DEFINED)')
    return ok

def broken():
    guard_banner()
    spec = json.loads((HERE.parent / 'planted_cases.json').read_text())['broken']
    tiny = mp.mpf('1e-12')
    a0, a2 = scatlens(('ls', mp.mpf(1) / 2, tiny, mp.mpf(1)), mp.mpf(1))
    got = a2 * 32 * mp.pi
    claim_holds = abs(got - spec['claimed_T2']) < 1e-6
    print(f"broken {spec['name']}: 32pi a02 = {mp.nstr(got, 12)} vs claimed {spec['claimed_T2']} -> {'ACCEPTED (BAD)' if claim_holds else 'REJECT'}")
    return not claim_holds

def live():
    guard_banner()
    p = HERE.parent / 'inputs.json'
    if not p.exists():
        sys.exit("live: inputs.json missing")
    raw = p.read_bytes(); print('inputs.json sha256', hashlib.sha256(raw).hexdigest())
    I = json.loads(raw)
    M = json.loads((REPO / 'sims/fdimm/masses.json').read_text())['sets']
    Fs = {k: (mp.mpf(v['F']), mp.mpf(v['dF'])) for k, v in I['F_pi'].items()}
    combos = {}
    for sk, sv in M.items():
        for fk, (Fv, _) in Fs.items():
            mods = models(mp.mpf(sv['m_pi']), mp.mpf(sv['m_rho']), Fv)
            combos[(sk, fk)] = {n: obs(*scatlens(md, mp.mpf(sv['m_pi']) ** 2)) for n, md in mods.items()}
    prim = ('S1', 'F1')
    relF = Fs['F1'][1] / Fs['F1'][0]
    pred, perr = {}, {}
    for n in ('P_a', 'P_b', 'LO'):
        pred[n] = combos[prim][n]
        perr[n] = {}
        for o in pred[n]:
            vals = [combos[k][n][o] for k in combos]
            perr[n][o] = mp.sqrt((2 * abs(pred[n][o]) * relF) ** 2 + ((max(vals) - min(vals)) / 2) ** 2)
        print(f"{n}: " + ', '.join(f"{o} = {mp.nstr(pred[n][o], 6)} +- {mp.nstr(perr[n][o], 2)}" for o in pred[n]))
        for k in combos:
            print(f"   [{k[0]},{k[1]}] " + ', '.join(f"{o}={mp.nstr(combos[k][n][o], 6)}" for o in combos[k][n]))
    cg = I['CGL']; pred['CGL'] = obs(mp.mpf(cg['a00']), mp.mpf(cg['a02']))
    perr['CGL'] = {'a00': mp.mpf(cg['da00']), 'a02': mp.mpf(cg['da02']), 'a00-a02': mp.sqrt(mp.mpf(cg['da00']) ** 2 + mp.mpf(cg['da02']) ** 2)}
    res = {}
    for xk, xv in I['data'].items():
        data = [(d['obs'], mp.mpf(d['value']), mp.mpf(d['err'])) for d in xv]
        cs = {n: chi2(pred[n], perr[n], data) for n in pred}
        print(f"[{xk}] " + '; '.join(f"chi2({n}) = {mp.nstr(cs[n][0], 4)} pulls " + ','.join(f"{o}:{mp.nstr(z, 3)}" for o, z in cs[n][1].items()) for n in cs))
        res[xk] = {n: classify(cs[n][0], cs[n][1], cs['LO'][0]) for n in ('P_a', 'P_b')}
        print(f"[{xk}] class vs LO: {res[xk]}")
    ks = list(res)
    for n in ('P_a', 'P_b'):
        print(f"overall {n}: {overall(res[ks[0]][n], res[ks[1]][n])}")
    print(f"VERDICT (P_b, the F-DIM-MASS repair): {overall(res[ks[0]]['P_b'], res[ks[1]]['P_b'])}")

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'planted'
    if mode == 'planted':
        r = planted(); rb = broken(); sys.exit(0 if r and rb else 1)
    if mode == 'broken':
        sys.exit(0 if broken() else 1)
    if mode == 'live':
        live(); sys.exit(0)
    sys.exit('mode?')
