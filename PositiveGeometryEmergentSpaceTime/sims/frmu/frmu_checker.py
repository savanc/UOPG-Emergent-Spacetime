#!/usr/bin/env python3
"""FR-MU locked checker: mu_n/mu_p from the spin-flavour-symmetric N_c-quark construction.
Construction: N_c quarks, colour totally antisymmetric => spin x flavour (4 modes u+,u-,d+,d-) totally SYMMETRIC
(bosonic occupation basis). Nucleon = the S = I = 1/2 state with S_z = +1/2, n_u = (N_c +/- 1)/2.
Magnetic operator (units of the quark magneton, equal u/d masses): mu_z = sum_f Q_f (n_{f+} - n_{f-}).
Charges: anomaly-consistent (STRUCT-2 branch, y_L = -1/2): Q_u = (1 + 1/N_c)/2, Q_d = (-1 + 1/N_c)/2.
Usage: frmu_checker.py {planted|broken|live|score <measured>}"""
import sys, itertools, numpy as np
from fractions import Fraction as F
MODES = ['u+', 'u-', 'd+', 'd-']
def basis(N, nu, two_sz):
    out = []
    for occ in itertools.product(range(N + 1), repeat=4):
        if sum(occ) == N and occ[0] + occ[1] == nu and (occ[0] - occ[1] + occ[2] - occ[3]) == two_sz: out.append(occ)
    return out
def S2_matrix(B):
    idx = {b: i for i, b in enumerate(B)}; M = np.zeros((len(B), len(B)))
    for j, b in enumerate(B):
        sz = (b[0] - b[1] + b[2] - b[3]) / 2; M[j, j] += sz * sz + sz
        # S- S+ : S+ = a+_{f+} a_{f-} summed over f in {u,d}
        for (p1, m1) in [(0, 1), (2, 3)]:            # apply S+
            if b[m1] == 0: continue
            c1 = np.sqrt(b[m1] * (b[p1] + 1)); b1 = list(b); b1[m1] -= 1; b1[p1] += 1
            for (p2, m2) in [(0, 1), (2, 3)]:        # apply S-
                if b1[p2] == 0: continue
                c2 = np.sqrt(b1[p2] * (b1[m2] + 1)); b2 = list(b1); b2[p2] -= 1; b2[m2] += 1
                M[idx[tuple(b2)], j] += c1 * c2
    return M
def moment(N, nu, Qu, Qd, target_S=0.5):
    B = basis(N, nu, 1); w, V = np.linalg.eigh(S2_matrix(B)); want = target_S * (target_S + 1)
    k = [i for i in range(len(w)) if abs(w[i] - want) < 1e-9]
    if len(k) != 1: raise SystemExit(f"no unique S={target_S} state (found {len(k)})")
    v = V[:, k[0]]; mu = sum(v[i] ** 2 * (Qu * (b[0] - b[1]) + Qd * (b[2] - b[3])) for i, b in enumerate(B))
    return float(mu)
def ratio(N, Qu, Qd, target_S=0.5):
    return moment(N, (N - 1) // 2, Qu, Qd, target_S) / moment(N, (N + 1) // 2, Qu, Qd, target_S)
def acc_charges(N): return float(F(1, 2) + F(1, 2 * N)), float(F(-1, 2) + F(1, 2 * N))
def closed(N): return F(3 - N * (N + 2), 3 + N * (N + 2))
BAND = 1 / 9            # preregistered relative band 1/N_c^2 at N_c = 3
NULL = (-1.0, 1.0)      # preregistered null: uniform on [-1, 1]
TRIALS = 13             # preregistered look-elsewhere count
mode = sys.argv[1]
if mode == 'planted':   # textbook SU(6) at N_c = 3 with SM charges: mu_p = 1, mu_n = -2/3 (units of quark magneton)
    mp = moment(3, 2, 2/3, -1/3); mn = moment(3, 1, 2/3, -1/3)
    ok = abs(mp - 1) < 1e-12 and abs(mn + 2/3) < 1e-12
    print(f"planted N_c=3 SM charges: mu_p={mp:.12f} mu_n={mn:.12f} recovered: {ok}"); sys.exit(0 if ok else 1)
if mode == 'broken':    # wrong state (S = 3/2, Delta-like): must NOT reproduce the nucleon -2/3 -> reject
    r = ratio(3, 2/3, -1/3, target_S=1.5)
    if abs(r + 2/3) > 1e-6: raise SystemExit(f"REJECT: S=3/2 state gives ratio {r:.6f} != -2/3")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'live':
    for N in (1, 3, 5, 7):
        Qu, Qd = acc_charges(N); r = ratio(N, Qu, Qd)
        print(f"N_c={N}: Q_u={Qu:.6f} Q_d={Qd:.6f} mu_n/mu_p={r:.12f} closed={float(closed(N)):.12f} agree={abs(r - float(closed(N))) < 1e-12}")
    print("prediction (N_c=3):", closed(3), "=", float(closed(3)))
if mode == 'score':
    meas = float(sys.argv[2]); pred = float(closed(3)); dev = abs(pred - meas) / abs(meas)
    lo, hi = sorted([meas * (1 - BAND), meas * (1 + BAND)]); width = hi - lo
    p1 = min(1.0, width / (NULL[1] - NULL[0])); pc = 1 - (1 - p1) ** TRIALS
    inband = dev <= BAND
    verdict = ('GATE-FAIL' if not inband else ('PASS' if pc < 0.01 else 'NUMEROLOGY'))
    print(f"pred={pred:.10f} meas={meas} rel_dev={dev:.5f} band={BAND:.5f} in_band={inband} p_single={p1:.5f} p_corrected(trials={TRIALS})={pc:.5f} verdict={verdict}")
