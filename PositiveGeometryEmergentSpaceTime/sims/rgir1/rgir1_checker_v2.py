#!/usr/bin/env python3
"""RG-IR-1 locked checker v2 (supersedes rgir1_checker.py; only planted P3 changed, verdict rule verbatim): does the one-loop SM infrared (quasi-)fixed point of the top Yukawa remove y_t as an input?
Prereg: prereg/RG-IR-1-top-yukawa-uv-memory-2026-10-30.md.  Modes: planted | broken | null | live (each guarded).
Conventions (declared in prereg §3): t = ln(mu/M_Z); g1 = g' (SM normalisation); 16pi^2 dg_i/dt = b_i g_i^3;
16pi^2 dy/dt = y (a y^2 - sum_i c_i g_i^2), a = 9/2, c = (17/12, 9/4, 8), b = (41/6, -19/6, -7); m_t = y v / sqrt2.
u = 1/y^2 obeys the affine ODE du/dt = (2/16pi^2)(G u - a)  (Lean: PositiveGeometryEmergentSpaceTime.RgIr1.u_flow_affine), so
u_IR = S u_UV + A with S = exp(-int_0^L 2G/16pi^2) = prod_i (alpha_i(L)/alpha_i(0))^(-c_i/b_i)."""
import json, math, sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
from guard import guard
PREREG = 'prereg/RG-IR-1-v2-supersede-P3-2026-10-30.md'
K = 16 * math.pi ** 2
# Locked inputs (prereg §4). alpha_i(M_Z) from alpha_em^-1(M_Z) = 127.95, sin^2 thetaW(M_Z) = 0.23122, alpha_s(M_Z) = 0.1180.
INP = {'ainv_em': 127.95, 's2w': 0.23122, 'as': 0.1180}
MZ = 91.1876
L_PL = math.log(1.22e19 / MZ)
L_GUT = math.log(1.0e16 / MZ)
SM = {'b': (41 / 6, -19 / 6, -7.0), 'c': (17 / 12, 9 / 4, 8.0), 'a': 4.5}
Y_UV = (1.0, math.sqrt(4 * math.pi))      # primary UV interval for y_t(Lambda)
T_PASS, T_PART = 0.02, 0.2
NSTEP = 4000

class IllDefined(Exception):
    pass

def alphas0(inp):
    if inp['ainv_em'] <= 0 or not (0 < inp['s2w'] < 1) or inp['as'] <= 0:
        raise IllDefined('non-physical input')
    aem = 1 / inp['ainv_em']
    return (aem / (1 - inp['s2w']), aem / inp['s2w'], inp['as'])

def alpha_t(a0, b, t):
    """one-loop alpha_i(t); IllDefined on a Landau pole / non-perturbative (alpha >= 1) in range."""
    inv = 1 / a0 - b / (2 * math.pi) * t
    if inv <= 1.0:
        raise IllDefined('Landau pole or alpha >= 1 at t=%.3f' % t)
    return 1 / inv

def G_t(a0s, fl, t):
    return sum(c * 4 * math.pi * alpha_t(a0, b, t) for a0, b, c in zip(a0s, fl['b'], fl['c']))

def SA_closed(a0s, fl, L):
    """S from the closed-form exponent product, A by Simpson quadrature of (2a/K) e^{-F(t)} with e^{-F} closed form."""
    def emF(t):
        v = 1.0
        for a0, b, c in zip(a0s, fl['b'], fl['c']):
            if c == 0: continue
            if abs(b) < 1e-12:
                v *= math.exp(-c * a0 * t / (2 * math.pi))
            else:
                v *= (alpha_t(a0, b, t) / a0) ** (-c / b)
        return v
    n = NSTEP
    h = L / n
    s = emF(0) + emF(L) + sum((4 if k % 2 else 2) * emF(k * h) for k in range(1, n))
    A = 2 * fl['a'] / K * s * h / 3
    return emF(L), A

def y_rk4(a0s, fl, L, yUV):
    """Direct RK4 of the non-linear y ODE from t = L down to 0 (rival integrator for the consistency gate)."""
    n = NSTEP; h = -L / n; y = yUV; t = L
    f = lambda t, y: y * (fl['a'] * y * y - G_t(a0s, fl, t)) / K
    for _ in range(n):
        k1 = f(t, y); k2 = f(t + h / 2, y + h * k1 / 2); k3 = f(t + h / 2, y + h * k2 / 2); k4 = f(t + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6; t += h
    return y

def width(S, A, yint):
    lo, hi = yint
    if not (0 < lo < hi):
        raise IllDefined('UV interval not ordered/positive')
    ys = [1 / math.sqrt(S / (y * y) + A) for y in (lo, hi)]
    return abs(ys[1] - ys[0]) / ((ys[0] + ys[1]) / 2), ys

def consistency(a0s, fl, L, yint, S_override=None):
    S, A = SA_closed(a0s, fl, L)
    if S_override is not None: S = S_override
    err = max(abs(1 / math.sqrt(S / (y * y) + A) - y_rk4(a0s, fl, L, y)) for y in yint)
    return err < 1e-6, err

def verdict_of(W, ill=False):
    if ill: return 'ILL-DEFINED'
    if W <= T_PASS: return 'PASS (REMOVES-INPUT)'
    if W <= T_PART: return 'PARTIAL (QFP-NARROWING)'
    if W > T_PART: return 'FAIL (UV-MEMORY)'
    return 'UNCLASSIFIED'

def evaluate(fl, inp=INP, L=L_PL, yint=Y_UV, check=True):
    guard(PREREG, HERE)
    try:
        a0s = alphas0(inp)
        alpha_t(a0s[0], fl['b'][0], L); alpha_t(a0s[1], fl['b'][1], L); alpha_t(a0s[2], fl['b'][2], L)
        S, A = SA_closed(a0s, fl, L)
        W, ys = width(S, A, yint)
        ok, err = consistency(a0s, fl, L, yint) if check else (True, 0.0)
        return {'S': S, 'A': A, 'W': W, 'yIR': ys, 'consistency_ok': ok, 'cons_err': err,
                'verdict': verdict_of(W, ill=not ok)}
    except IllDefined as e:
        return {'verdict': 'ILL-DEFINED', 'reason': str(e)}

def gut_norm(fl):
    """E1: g1_GUT^2 = (5/3) g'^2 -> b1, c1 scale by 3/5 and alpha1(0) by 5/3 (physics-preserving)."""
    return {'b': (fl['b'][0] * 3 / 5,) + tuple(fl['b'][1:]), 'c': (fl['c'][0] * 3 / 5,) + tuple(fl['c'][1:]), 'a': fl['a'], 'gut': True}

def evaluate_gut(fl, inp=INP, L=L_PL, yint=Y_UV):
    guard(PREREG, HERE)
    a0 = list(alphas0(inp)); a0[0] *= 5 / 3
    g = gut_norm(fl)
    S, A = SA_closed(a0, g, L)
    return width(S, A, yint)[0]

def evaluate_lnmu2(fl, inp=INP, L=L_PL, yint=Y_UV):
    """E2: s = ln(mu^2) = 2t; all beta coefficients halve and the range doubles (physics-preserving)."""
    guard(PREREG, HERE)
    h = {'b': tuple(x / 2 for x in fl['b']), 'c': tuple(x / 2 for x in fl['c']), 'a': fl['a'] / 2}
    S, A = SA_closed(alphas0(inp), h, 2 * L)
    return width(S, A, yint)[0]

def planted():
    guard(PREREG, HERE)
    out = {}
    a0s = alphas0(INP)
    qcd = {'b': SM['b'], 'c': (0.0, 0.0, 8.0), 'a': 4.5}
    S, A = SA_closed(a0s, qcd, L_PL)
    S_cf = (alpha_t(a0s[2], -7.0, L_PL) / a0s[2]) ** (8 / 7)
    ok, err = consistency(a0s, qcd, L_PL, Y_UV)
    out['P1_qcd_closed_form'] = {'S': S, 'S_closed': S_cf, 'ok': abs(S - S_cf) < 1e-9 and ok, 'rk4_err': err}
    r = evaluate({'b': SM['b'], 'c': (17 / 12, 9 / 4, 80.0), 'a': 4.5})
    out['P2_strong_attraction'] = {'W': r.get('W'), 'verdict': r['verdict'], 'ok': r['verdict'].startswith('PASS')}
    r = evaluate({'b': SM['b'], 'c': (0.0, 0.0, 0.0), 'a': 4.5})
    A0 = 2 * 4.5 * L_PL / K   # c = 0: u_IR = u_UV + 2aL/K exactly (S = 1)
    W0 = width(1.0, A0, Y_UV)[0]
    out['P3_no_gauge'] = {'W': r.get('W'), 'W_analytic': W0, 'S': r.get('S'), 'verdict': r['verdict'],
                          'ok': abs(r['W'] - W0) < 1e-9 and abs(r['S'] - 1) < 1e-12}
    w0 = evaluate(SM)['W']; w1 = evaluate_gut(SM); w2 = evaluate_lnmu2(SM)
    out['P4_valid_alt_conventions'] = {'W_sm': w0, 'W_gutnorm': w1, 'W_lnmu2': w2, 'ok': abs(w0 - w1) < 1e-9 and abs(w0 - w2) < 1e-9}
    # gate self-tests: each boolean gate true once and false once
    c_true = consistency(a0s, SM, L_PL, Y_UV)[0]
    c_false = consistency(a0s, SM, L_PL, Y_UV, S_override=1.5 * SA_closed(a0s, SM, L_PL)[0])[0]
    pert_false = evaluate({'b': (200.0, -19 / 6, -7.0), 'c': SM['c'], 'a': 4.5})['verdict'] == 'ILL-DEFINED'
    pert_true = evaluate(SM)['verdict'] != 'ILL-DEFINED'
    vmap = [verdict_of(0.01), verdict_of(0.1), verdict_of(0.5), verdict_of(0.1, ill=True)]
    out['G_selftests'] = {'consistency_true': c_true, 'consistency_false_detected': not c_false,
                          'perturbative_true': pert_true, 'perturbative_false_detected': pert_false, 'verdict_map': vmap,
                          'ok': c_true and not c_false and pert_true and pert_false and
                                vmap == ['PASS (REMOVES-INPUT)', 'PARTIAL (QFP-NARROWING)', 'FAIL (UV-MEMORY)', 'ILL-DEFINED']}
    out['ALL_OK'] = all(v['ok'] for v in out.values())
    return out

def broken():
    guard(PREREG, HERE)
    out = {}
    r = evaluate({'b': (41 / 6, -19 / 6, 7.0), 'c': SM['c'], 'a': 4.5})
    out['B1_qcd_sign_flipped'] = {'verdict': r['verdict'], 'rejected': not r['verdict'].startswith('PASS')}
    r = evaluate(SM, inp={'ainv_em': 127.95, 's2w': 0.23122, 'as': -0.118})
    out['B2_negative_alpha'] = {'verdict': r['verdict'], 'rejected': r['verdict'] == 'ILL-DEFINED'}
    r = evaluate(SM, yint=(math.sqrt(4 * math.pi), 1.0))
    out['B3_reversed_interval'] = {'verdict': r['verdict'], 'rejected': r['verdict'] == 'ILL-DEFINED'}
    out['ALL_REJECTED'] = all(v['rejected'] for v in out.values())
    return out

def null(n=2000, seed=20261030):
    guard(PREREG, HERE)
    import random
    rng = random.Random(seed)
    cnt = {'PASS': 0, 'PARTIAL': 0, 'FAIL': 0, 'ILL': 0}
    for _ in range(n):
        b2 = rng.uniform(-7, 1)
        while abs(b2) < 0.1: b2 = rng.uniform(-7, 1)
        fl = {'b': (rng.uniform(0.5, 10), b2, rng.uniform(-11, -1)),
              'c': (rng.uniform(0, 3), rng.uniform(0, 5), rng.uniform(0, 12)), 'a': rng.uniform(1.5, 9)}
        try:
            a0s = alphas0(INP)
            for i in range(3): alpha_t(a0s[i], fl['b'][i], L_PL)
            S, A = SA_closed(a0s, fl, L_PL)
            W = width(S, A, Y_UV)[0]
            v = verdict_of(W)
            cnt[v.split()[0]] += 1
        except IllDefined:
            cnt['ILL'] += 1
    m = n - cnt['ILL']
    return {'n': n, 'seed': seed, 'counts': cnt, 'pass_rate': cnt['PASS'] / m, 'partial_or_better_rate': (cnt['PASS'] + cnt['PARTIAL']) / m}

def live():
    guard(PREREG, HERE)
    out = {'inputs': INP, 'L_planck': L_PL, 'L_gut': L_GUT, 'Y_UV': Y_UV}
    out['SM_planck'] = evaluate(SM)
    out['SM_gut_reportonly'] = evaluate(SM, L=L_GUT)
    out['rival_qcd_only'] = evaluate({'b': SM['b'], 'c': (0.0, 0.0, 8.0), 'a': 4.5})
    out['rival_no_running_W'] = width(1.0, 0.0, Y_UV)[0]
    out['rival_no_gauge_yukawa_only'] = evaluate({'b': SM['b'], 'c': (0.0, 0.0, 0.0), 'a': 4.5})
    out['reportonly_W_sm_over_W_nogauge'] = out['SM_planck']['W'] / out['rival_no_gauge_yukawa_only']['W']
    box = []
    for ae in (126.0, 127.95, 130.0):
        for s2 in (0.225, 0.23122, 0.237):
            for a3 in (0.110, 0.118, 0.126):
                r = evaluate(SM, inp={'ainv_em': ae, 's2w': s2, 'as': a3}, check=False)
                box.append((ae, s2, a3, r.get('W'), r['verdict']))
    out['box'] = box
    out['box_verdicts'] = sorted({b[4] for b in box})
    out['alt_intervals_reportonly'] = {str(yi): evaluate(SM, yint=yi, check=False).get('W') for yi in ((0.5, math.sqrt(4 * math.pi)), (0.1, math.sqrt(4 * math.pi)))}
    out['conv_E1_gutnorm_W'] = evaluate_gut(SM); out['conv_E2_lnmu2_W'] = evaluate_lnmu2(SM)
    out['null'] = null()
    v = out['SM_planck']['verdict']
    if v != 'ILL-DEFINED' and len(out['box_verdicts']) > 1: v += ' [BOX-STRADDLE]'
    out['VERDICT'] = v
    return out

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    fn = {'planted': planted, 'broken': broken, 'null': null, 'live': live}.get(mode)
    if fn is None: sys.exit('usage: rgir1_checker.py planted|broken|null|live')
    res = fn()
    print(json.dumps(res, indent=1, default=str))
