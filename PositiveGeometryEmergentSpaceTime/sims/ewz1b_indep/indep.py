"""EW-Z1b independent derivation (Phase C item 3).  Does NOT import or reuse sims/ewz1b/*.

Method: the CGW Coulomb-branch theory is 5D massless Yang-Mills dimensionally reduced, the 5th momentum
component of leg i being its vev difference k_i (so m_i = |k_i|).  We build the colour-ordered tree A[1234]
with textbook colour-ordered Feynman rules (Dixon conventions, overall i/2 dropped):
   V3^{MNR}(P1,P2,P3) = eta^{MN}(P1-P2)^R + eta^{NR}(P2-P3)^M + eta^{RM}(P3-P1)^N   (all outgoing)
   V4^{MNRS}          = 2 eta^{MR}eta^{NS} - eta^{MN}eta^{RS} - eta^{MS}eta^{NR}
   propagator         = eta_{MN} / P^2   (Feynman gauge; 5D P^2 = X - M^2)
by EXPLICIT INDEX SUMS over an 8-dim coordinate space (7 abstract 4D basis vectors p1,p2,p3,e1..e4 with a
random exact Gram matrix, plus the orthogonal 5th direction with eta_55 = -1).  Adjustable couplings are
attached per vertex index assignment by the number n5 of indices equal to the 5th direction:
   V3: n5=0 -> lam3, n5=1 -> a, n5=2 -> gs, n5=3 -> 0 ;  V4: n5=0 -> lam4, n5=2 -> b, n5=4 -> 1.
Then N_indep = A * (s - M_s^2)(T - M_t^2) on the hidden-zero locus (ee13 = e1p3 = e3p1 = 0,
u - m1^2 - m3^2 = 2 k1 k3) is compared, at random exact rational points, with the Lean definition
PositiveGeometryEmergentSpaceTime.EWZ1b.N parsed directly from lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean.
"""
import re, random, sys, json, hashlib, itertools as it
from fractions import Fraction as F
RUN_ID = 'EWZ1B-INDEP-2026-11-03-r1'
ROOT = __file__.rsplit('/sims/', 1)[0]

def lean_N():
    src = open(ROOT + '/lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean').read()
    m = re.search(r'def N \(([^:]*) : ℚ\) : ℚ :=\n(.*?)\n\n', src, re.S)
    args = m.group(1).split(); body = m.group(2).strip().replace('^', '**')
    return args, body

def inv(M):
    n = len(M); A = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        pv = A[c][c]; A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]

def amplitude(v, cpl):
    """v: dict of numeric invariants; returns (A, Ms2, Mt2, s, T) with A the colour-ordered amplitude."""
    k = [v['k1'], v['k2'], v['k3']]; k.append(-(k[0] + k[1] + k[2]))
    m2 = [x * x for x in k]; s, t = v['s'], v['t']
    u = sum(m2) - s - t
    # 4D Gram on basis p1 p2 p3 e1 e2 e3 e4
    G = [[F(0)] * 7 for _ in range(7)]
    def put(i, j, x): G[i][j] = G[j][i] = F(x)
    put(0, 0, m2[0]); put(1, 1, m2[1]); put(2, 2, m2[2])
    put(0, 1, (s - m2[0] - m2[1]) / 2); put(1, 2, (t - m2[1] - m2[2]) / 2); put(0, 2, (u - m2[0] - m2[2]) / 2)
    for i in range(4):
        for j in range(3):
            if i == j: put(3 + i, j, 0)
            elif i == 3 and j == 2: put(6, 2, -v['e4p1'] - v['e4p2'])   # e4.p4 = 0
            else: put(3 + i, j, v[f'e{i+1}p{j+1}'])
        for j in range(i + 1, 4): put(3 + i, 3 + j, v[f'ee{i+1}{j+1}'])
        put(3 + i, 3 + i, v[f'ee{i+1}{i+1}'])     # arbitrary: must drop out
    eta = [[F(0)] * 8 for _ in range(8)]
    for i in range(7):
        for j in range(7): eta[i][j] = G[i][j]
    eta[7][7] = F(-1)
    etai = inv(eta)
    def vec(coeffs, fifth):
        x = [F(0)] * 8
        for b, c in coeffs.items(): x[b] = F(c)
        x[7] = F(fifth); return x
    P = [vec({0: 1}, k[0]), vec({1: 1}, k[1]), vec({2: 1}, k[2]), vec({0: -1, 1: -1, 2: -1}, k[3])]
    E = [vec({3 + i: 1}, 0) for i in range(4)]
    low = lambda x: [sum(eta[i][j] * x[j] for j in range(8)) for i in range(8)]
    add = lambda x, y: [p + q for p, q in zip(x, y)]
    neg = lambda x: [-p for p in x]
    def n5(*idx): return sum(1 for i in idx if i == 7)
    c3 = {0: cpl['lam3'], 1: cpl['a'], 2: cpl['gs'], 3: 0}
    c4 = {0: cpl['lam4'], 1: 0, 2: cpl['b'], 3: 0, 4: 1}
    def V3(M, N, R, P1, P2, P3):
        return c3[n5(M, N, R)] * (etai[M][N] * (P1[R] - P2[R]) + etai[N][R] * (P2[M] - P3[M]) + etai[R][M] * (P3[N] - P1[N]))
    def V4(M, N, R, S_):
        return c4[n5(M, N, R, S_)] * (2 * etai[M][R] * etai[N][S_] - etai[M][N] * etai[R][S_] - etai[M][S_] * etai[N][R])
    def current(i, j):     # J^R = V3^{MNR}(P_i, P_j, -(P_i+P_j)) e_iM e_jN  (contravariant)
        Pi, Pj = P[i], P[j]; Q = neg(add(Pi, Pj)); ei, ej = low(E[i]), low(E[j])
        return [sum(V3(M, N, R, Pi, Pj, Q) * ei[M] * ej[N] for M in range(8) for N in range(8) if ei[M] and ej[N])
                for R in range(8)], add(Pi, Pj)
    A = F(0); props = []
    for (i, j), (l, mm) in (((0, 1), (2, 3)), ((1, 2), (3, 0))):
        Ja, Pm = current(i, j); Jb, _ = current(l, mm)
        P2 = sum(Pm[x] * eta[x][y] * Pm[y] for x in range(8) for y in range(8))
        props.append(P2)
        A += sum(Ja[x] * eta[x][y] * Jb[y] for x in range(8) for y in range(8)) / P2
    el = [low(e) for e in E]
    A += sum(V4(M, N, R, S_) * el[0][M] * el[1][N] * el[2][R] * el[3][S_]
             for M, N, R, S_ in it.product(range(8), repeat=4) if el[0][M] and el[1][N] and el[2][R] and el[3][S_])
    return A, props

def main(npts=200, seed=20261103):
    args, body = lean_N(); rnd = random.Random(seed)
    R = lambda: F(rnd.randint(-9, 9), rnd.choice([1, 1, 2, 3]))
    ok = 0; rows = []; zero_gauge = 0
    for n in range(npts):
        v = {x: R() for x in args}
        for x in ('ee11', 'ee22', 'ee33', 'ee44', 'e3p1', 'e1p3', 'ee13', 'gs', 'b'): v[x] = R()
        v['ee13'] = v['e1p3'] = v['e3p1'] = F(0)                 # hidden-zero locus (polarisations)
        k1, k2, k3 = v['k1'], v['k2'], v['k3']; k4 = -(k1 + k2 + k3)
        v['t'] = k2 * k2 + k4 * k4 - v['s'] - 2 * k1 * k3          # u - m1^2 - m3^2 = 2 k1 k3
        if n % 4 == 0: v['a'] = rnd.choice([1, -1]) * v['lam3']; v['lam4'] = v['lam3'] ** 2   # gauge point
        cpl = {x: v[x] for x in ('lam3', 'a', 'gs', 'lam4', 'b')}
        A, (Ds, Dt) = amplitude(v, cpl)
        if Ds == 0 or Dt == 0: continue
        Nin = A * Ds * Dt
        Nl = eval(body, {}, {x: v[x] for x in args})
        good = (Nin == Nl); ok += good
        if n % 4 == 0 and Nin == 0: zero_gauge += 1
        rows.append((n, str(Nin), str(Nl), good))
    tot = len(rows)
    out = {'run_id': RUN_ID, 'points': tot, 'agree': ok, 'gauge_points_zero': zero_gauge,
           'gauge_points': sum(1 for r in rows if r[0] % 4 == 0), 'seed': seed,
           'lean_N_sha256': hashlib.sha256(body.encode()).hexdigest()[:16], 'first_rows': rows[:5]}
    print(json.dumps(out, indent=1))
    return out

if __name__ == '__main__':
    o = main()
    json.dump(o, open(ROOT + '/sims/ewz1b_indep/output_' + RUN_ID + '.json', 'w'), indent=1)
    sys.exit(0 if o['agree'] == o['points'] else 1)
