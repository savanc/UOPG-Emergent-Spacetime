#!/usr/bin/env python3
"""FL-1Z locked checker (prereg/FL-1Z-modular-fixed-point-2026-10-22.md).
Model (fixed in prereg, not chosen from outputs): Zee-Babu neutrino model with non-holomorphic modular A4
(Kobayashi-Okada-Orikasa, arXiv:2502.12662 v2): L_L ~ 3 (weight -1), l_R ~ 3 (+1), S- ~ 1 (+2), k++ ~ 1 (0).
  M_l   = ae*P + be*S(Y0) + ce*A(Y0)            (eq. III.2; v/sqrt2 dropped, ae, be, ce real)
  f     = A(Y0) (antisymmetric),  g = S(Y-2) + bk*P  (eq. III.16)
  m_nu  = f conj(M_l) g conj(M_l)^T f^T           (eq. III.14 up to the overall kappa)
Y0 = Y3^(0), Y-2 = Y3^(-2): q-expansions of App. A eqs. (A.1)-(A.6), truncated at n <= 4 (|q|^5 < 2e-12 near omega).
Dimensionless target: rho = (m2/m3)^2 = dm2_sol/dm2_atm (NH, m1 = 0).
Modes: planted | live.  GUARD: guard() in EVERY scoring function; no pass flag (METHOD 2026-10-20 pattern).
"""
import cmath, hashlib, json, math, random, re, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/FL-1Z-amendment-2-2026-10-22.md'   # A2 (A1 before; original prereg/FL-1Z-modular-fixed-point-2026-10-22.md)
RUN_ID = 'FL1Z-2026-10-22-r3'                         # A2: r2 lepton fit converged at only 27/383 points; r1 crashed
SEED = 20261022
PI = math.pi
W = cmath.exp(2j * PI / 3)          # omega = e^{2 pi i/3}
TAU_W = complex(-0.5, math.sqrt(3) / 2)
ME, MMU, MTAU = 0.51099895e-3, 0.1056583755, 1.77686   # GeV (PDG; input, ratios only)
RHO_EXP = (6.92e-5 / 2.606e-3, 8.05e-5 / 2.463e-3)    # 2502.12662 Tab. II 3-sigma columns (NuFit 6.0)

def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)

_FETCH_DONE = []
_ANC_BY_ORIGIN = {}

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
    m = re.search(r'fl1z_checker\.py` sha256 `([0-9a-f]{64})`', (REPO / PREREG).read_text())
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

# ---------------- modular forms (2502.12662 App. A, n <= 4) ----------------
def G3(z):
    return (z * z + 2 * z + 2) * math.exp(-z)   # incomplete Gamma(3, z)

def Y0(tau):
    y = tau.imag
    q = cmath.exp(2j * PI * tau); q13 = cmath.exp(2j * PI * tau / 3); q23 = q13 * q13
    c1 = [3, 9 / 2, 1, 21 / 4]
    y1 = y - 9 * math.log(3) / (4 * PI) - sum(c * (math.exp(-4 * PI * n * y) / q ** n + q ** n)
                                              for n, c in enumerate(c1, 1)) / PI
    a = [1 / 4, 1 / 5, 5 / 16, 2 / 11]            # y2 non-holo / y3 holo
    b = [1, 7 / 4, 8 / 7, 9 / 5]                  # y2 holo / y3 non-holo
    nh2 = sum(c * math.exp(-(4 * n - 1) * PI * y) / q ** n for n, c in enumerate(a, 1))
    h2 = sum(c * q ** n for n, c in enumerate(b))
    y2 = 27 * q13 * math.exp(PI * y / 3) / PI * nh2 + 9 * q13 / (2 * PI) * h2
    nh3 = sum(c * math.exp(-(4 * n - 2) * PI * y) / q ** n for n, c in enumerate(b, 1))
    h3 = sum(c * q ** n for n, c in enumerate(a))
    y3 = 9 * q23 * math.exp(2 * PI * y / 3) / (2 * PI) * nh3 + 27 * q23 / PI * h3
    return np.array([y1, y2, y3], dtype=complex)

def Ym2(tau):
    y = tau.imag
    q = cmath.exp(2j * PI * tau); q13 = cmath.exp(2j * PI * tau / 3); q23 = q13 * q13
    z3, z4 = 1.2020569031595942, PI ** 4 / 90
    c1 = [21, 189 / 8, 169 / 9, 1533 / 64]        # non-holo coefficient x 16 pi^3 ; holo = 2x
    y1 = y ** 3 / 3 + PI * z3 / (40 * z4) + sum(c * (G3(4 * PI * n * y) / q ** n + 2 * q ** n)
                                                for n, c in enumerate(c1, 1)) / (16 * PI ** 3)
    a = [1 / 16, 7 / 125, 65 / 1024, 74 / 1331]   # y2' non-holo / y3' holo
    b = [1, 73 / 64, 344 / 343, 567 / 500]        # y2' holo / y3' non-holo
    nh2 = sum(c * G3((12 * n - 4) * PI * y / 3) / q ** n for n, c in enumerate(a, 1))
    h2 = sum(c * q ** n for n, c in enumerate(b))
    y2 = -729 * q13 / (16 * PI ** 3) * nh2 - 81 * q13 / (16 * PI ** 3) * h2
    nh3 = sum(c * G3((12 * n - 8) * PI * y / 3) / q ** n for n, c in enumerate(b, 1))
    h3 = sum(c * q ** n for n, c in enumerate(a))
    y3 = -81 * q23 / (32 * PI ** 3) * nh3 - 729 * q23 / (8 * PI ** 3) * h3
    return np.array([y1, y2, y3], dtype=complex)

V1 = np.array([-1, 2 * W, 2 * W ** 2]) / 3        # eq. (B.10)
VW = np.array([2, -W, 2 * W ** 2]) / 3            # eq. (B.11)
T_D3 = np.array([[4, -2 * W ** 2, 4 * W], [-2 * W ** 2, W, -2], [4 * W, -2, 4 * W ** 2]])  # eq. (D.3)
P = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)

def Smat(y):
    return np.array([[2 * y[0], -y[2], -y[1]], [-y[2], 2 * y[1], -y[0]], [-y[1], -y[0], 2 * y[2]]])

def Amat(y):
    return np.array([[0, y[2], -y[1]], [-y[2], 0, y[0]], [y[1], -y[0], 0]])

def Ml(y0, ae, be, ce):
    return ae * P + be * Smat(y0) + ce * Amat(y0)

def mnu(y0, ym2, bk, ae, be, ce, fbreak=0.0):
    f = Amat(y0) + fbreak * np.eye(3)
    B = np.conj(Ml(y0, ae, be, ce))
    g = Smat(ym2) + bk * P
    return f @ B @ g @ B.T @ f.T

def sv(m):
    return np.sort(np.linalg.svd(m, compute_uv=False))

# ---------------- charged-lepton fit (beta = be/ae, gamma = ce/ae) ----------------
TARGET = np.array([math.log((ME / MTAU) ** 2), math.log((MMU / MTAU) ** 2)])

def _res(y0, p):
    if not np.all(np.isfinite(p)) or np.max(np.abs(p)) > 1e6:   # A1: reject runaway Newton iterates
        return None
    ev = np.sort(np.linalg.eigvalsh((lambda M: M @ M.conj().T)(Ml(y0, 1.0, p[0], p[1]))))
    if ev[0] <= 0:
        return None
    return np.array([math.log(ev[0] / ev[2]), math.log(ev[1] / ev[2])]) - TARGET

GRID = np.concatenate([-np.logspace(3, -2, 70), np.logspace(-2, 3, 70)])   # A2: deterministic seeding grid

def _grid_starts(y0, nbest=30):
    Bg, Gg = np.meshgrid(GRID, GRID, indexing='ij')
    M = P[None, None] + Bg[..., None, None] * Smat(y0)[None, None] + Gg[..., None, None] * Amat(y0)[None, None]
    ev = np.sort(np.linalg.eigvalsh(M @ np.conj(np.swapaxes(M, -1, -2))), axis=-1)
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.abs(np.log(ev[..., 0] / ev[..., 2]) - TARGET[0]) + np.abs(np.log(ev[..., 1] / ev[..., 2]) - TARGET[1])
    r = np.where(np.isfinite(r), r, np.inf).ravel()
    idx = np.argsort(r)[:nbest]
    return [np.array([Bg.ravel()[i], Gg.ravel()[i]]) for i in idx]

def lepton_branches(y0, rng, nstart=40):
    guard()
    sols = []
    starts = _grid_starts(y0) + [np.array([rng.choice((-1, 1)) * 10 ** rng.uniform(-1, 3), rng.choice((-1, 1)) * 10 ** rng.uniform(-1, 3)]) for _ in range(nstart)]
    for p0 in starts:
        p = p0.copy()
        for _ in range(80):
            r = _res(y0, p)
            if r is None:
                break
            if np.max(np.abs(r)) < 1e-11:
                break
            J = np.zeros((2, 2))
            for k in range(2):
                h = 1e-7 * max(1.0, abs(p[k])); dp = np.zeros(2); dp[k] = h
                r2 = _res(y0, p + dp)
                if r2 is None:
                    J = None; break
                J[:, k] = (r2 - r) / h
            if J is None or abs(np.linalg.det(J)) < 1e-300:
                break
            step = np.linalg.solve(J, r)
            lam = 1.0                                   # A2: backtracking line search
            while lam > 1e-4:
                r3 = _res(y0, p - lam * step)
                if r3 is not None and np.max(np.abs(r3)) < np.max(np.abs(r)):
                    break
                lam /= 2
            p = p - lam * step
        r = _res(y0, p)
        if r is not None and np.max(np.abs(r)) < 1e-9 and all(np.max(np.abs(p - s) / (1 + np.abs(s))) > 1e-6 for s in sols):
            sols.append(p.copy())
    return sols

def observables(y0, ym2, bk, beta, gamma):
    guard()
    M = Ml(y0, 1.0, beta, gamma)
    m = mnu(y0, ym2, bk, 1.0, beta, gamma)
    _, VL = np.linalg.eigh(M @ M.conj().T)                 # ascending: e, mu, tau
    w2, Vn = np.linalg.eigh(m.conj().T @ m)                # ascending: nu1, nu2, nu3
    s = np.sqrt(np.clip(w2, 0, None))
    U = VL.conj().T @ Vn
    A2 = np.abs(U) ** 2
    s13 = A2[0, 2]
    mp = VL.T @ m @ VL
    return {'m1_m3': s[0] / s[2], 'rho': (s[1] / s[2]) ** 2, 's13sq': s13,
            's23sq': A2[1, 2] / (1 - s13), 's12sq': A2[0, 1] / (1 - s13), 'mee_m3': abs(mp[0, 0]) / s[2]}

# ---------------- planted ----------------
def run_planted():
    guard()
    out = {'run_id': RUN_ID, 'mode': 'planted'}
    y0, ym2 = Y0(TAU_W), Ym2(TAU_W)
    b0 = np.vdot(V1, y0); bm2 = np.vdot(VW, ym2)
    out['L1'] = {'b0': [b0.real, b0.imag], 'b_m2': [bm2.real, bm2.imag],
                 'resid0': float(np.linalg.norm(y0 - b0 * V1) / np.linalg.norm(y0)),
                 'resid_m2': float(np.linalg.norm(ym2 - bm2 * VW) / np.linalg.norm(ym2))}
    out['L1']['pass'] = bool(abs(b0 - (-0.2623)) < 5e-4 and abs(bm2 - 0.4166) < 5e-4
                             and out['L1']['resid0'] < 1e-3 and out['L1']['resid_m2'] < 1e-3)
    rng = random.Random(SEED + 1)
    worst_r2, worst_cos = 0.0, 1.0
    for _ in range(20):
        ae, be, ce = (rng.uniform(-3, 3) for _ in range(3))
        m = mnu(-0.2623 * V1, 0.4166 * VW, 0.0, ae, be, ce)
        s = sv(m)
        worst_r2 = max(worst_r2, s[1] / s[2])
        cs = max(abs(np.vdot(T, m)) / (np.linalg.norm(T) * np.linalg.norm(m)) for T in (T_D3, np.conj(T_D3)))
        worst_cos = min(worst_cos, cs)
    out['L2'] = {'max_m2_m3': worst_r2, 'min_cos_D3': worst_cos, 'pass': bool(worst_r2 < 1e-8 and worst_cos > 1 - 1e-8)}
    worst_m1 = 0.0; neg = 1.0
    for _ in range(50):
        tau = TAU_W + complex(rng.uniform(-0.05, 0.05), rng.uniform(0, 0.1))
        bk = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
        ae, be, ce = (rng.uniform(-3, 3) for _ in range(3))
        s = sv(mnu(Y0(tau), Ym2(tau), bk, ae, be, ce))
        worst_m1 = max(worst_m1, s[0] / s[2])
        s = sv(mnu(Y0(tau), Ym2(tau), bk, ae, be, ce, fbreak=0.1))
        neg = min(neg, s[0] / s[2])
    out['L3'] = {'max_m1_m3': worst_m1, 'pass': bool(worst_m1 < 1e-10)}
    out['L4'] = {'min_m1_m3_broken_f': neg, 'pass': bool(neg > 1e-3)}
    out['PLANTED'] = 'PASS' if all(out[k]['pass'] for k in ('L1', 'L2', 'L3', 'L4')) else 'FAIL'
    return out

# ---------------- live ----------------
def run_live():
    guard()
    rng = random.Random(SEED)
    res = {'run_id': RUN_ID, 'seed': SEED, 'mode': 'live'}
    def point(tau, bk, tag):
        y0, ym2 = Y0(tau), Ym2(tau)
        br = lepton_branches(y0, rng)
        return [dict(tag=tag, tau=[tau.real, tau.imag], bk=[bk.real, bk.imag], branch=i, beta=float(p[0]), gamma=float(p[1]),
                     **observables(y0, ym2, bk, p[0], p[1])) for i, p in enumerate(br)], len(br)
    rows, nbr = [], []
    for d in (1e-3, 3e-3, 6e-3, 1e-2, 3e-2):                       # D1
        for j in range(8):
            r, n = point(TAU_W + d * cmath.exp(1j * (PI * j / 8)), 0j, f'D1 d={d}'); rows += r; nbr.append(n)
    for b in (0.1, 0.3, 0.5, 0.7, 1.0):                             # D2
        for j in range(8):
            r, n = point(TAU_W, b * cmath.exp(2j * PI * j / 8), f'D2 b={b}'); rows += r; nbr.append(n)
    for sgn in (1, -1):                                             # D3 (report only)
        r, n = point(complex(-0.4958, 0.8709), 0.511 * cmath.exp(sgn * 2.07j), f'D3 sgn={sgn}'); rows += r; nbr.append(n)
    r, n = point(1j, 0j, 'D5 tau=i'); rows += r; nbr.append(n)       # D5 (report only)
    for _ in range(300):                                            # D4 random
        d = 0.03 * math.sqrt(rng.random()); ph = rng.uniform(0, PI)
        bk = rng.uniform(0, 1) * cmath.exp(1j * rng.uniform(-PI, PI))
        r, n = point(TAU_W + d * cmath.exp(1j * ph), bk, 'D4'); rows += r; nbr.append(n)
    res['rows'] = rows
    res['branches_per_point'] = {'min': min(nbr), 'max': max(nbr), 'n_points': len(nbr)}
    keys = ['m1_m3', 'rho', 's12sq', 's13sq', 's23sq', 'mee_m3']
    d4 = [x for x in rows if x['tag'].startswith(('D1', 'D2', 'D4'))]
    spread = {}
    for k in keys:
        v = np.array([x[k] for x in d4])
        med = float(np.median(v))
        spread[k] = {'min': float(v.min()), 'max': float(v.max()), 'median': med,
                     'rel_spread': float((v.max() - v.min()) / med) if med > 0 else None}
    res['spread'] = spread
    res['constant_observables'] = [k for k in keys if k != 'm1_m3' and spread[k]['rel_spread'] is not None and spread[k]['rel_spread'] < 0.01]
    d1 = {}
    for x in rows:
        if x['tag'].startswith('D1') or x['tag'].startswith('D2'):
            d1.setdefault(x['tag'], []).append(x['rho'])
    res['rho_by_tag'] = {k: [min(v), max(v)] for k, v in d1.items()}
    inexp = [x for x in d4 if RHO_EXP[0] <= x['rho'] <= RHO_EXP[1]]
    res['n_rho_in_exp'] = len(inexp)
    res['VERDICT'] = 'NOT-WELL-POSED (confirmed)' if not res['constant_observables'] else 'WELL-POSED-CANDIDATE: ' + ','.join(res['constant_observables'])
    return res

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'planted'
    out = run_planted() if mode == 'planted' else run_live()
    print(json.dumps(out if mode == 'planted' else {k: v for k, v in out.items() if k != 'rows'}, indent=1, default=str))
    if mode == 'live':
        (HERE.parent / 'fl1z_live.json').write_text(json.dumps(out, indent=1, default=str))
