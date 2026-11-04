#!/usr/bin/env python3
"""LEAN-CERT-1 locked checker (prereg/LEAN-CERT-1-certificate-upgrade-2026-10-23.md).
Sketch-and-verify linear-algebra certificates (Cosmic9 lesson 4, notes/LIT-REVIEW-2026-10-22-cosmic-nine-loops-ai-physics.md):
  sketch  = randomised rank of S*M*T modulo three primes (seeded);
  verify  = exact integer check of a split certificate  P*M + K*Q = d*I,  Q*K = d*I,  M*K = 0,  d != 0,
            which implies ker_Q(M) = image(K) and K injective (Lean PositiveGeometryEmergentSpaceTime.LeanCert.kernel_char / leftInv_injective).
Targets (declared in prereg):
  T0  known-result reproduction: ABHY 1711.09102 eq. (5), (6), (10): dim K_n = n(n-3)/2 for n = 5, 6 (n = 7 held out);
  T1  upgrade target: GRADED-POSITROID N_ACC = 2 (run GPOS-2026-10-22-r1, SIMULATED exact) -> certificate for the
      linear ACC line + cubic on the line + independent brute-force recount over the GPOS domain.
Emits Lean literals (sims/leancert1/certs_lean.txt) consumed by lean/PositiveGeometryEmergentSpaceTime/LeanCert.lean.
Modes: planted | live.  Run id + seed fixed in prereg.
GUARD (METHOD 2026-10-20 hardened pattern, copied from sims/int1): guard() in EVERY scoring function; no pass flag.
"""
import hashlib, itertools, json, random, re, subprocess, sys, time
from fractions import Fraction as Fr
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/LEAN-CERT-1-certificate-upgrade-2026-10-23.md'
RUN_ID = 'LEANCERT1-2026-10-23-r1'
SEED = 20261023
PRIMES = (1000003, 998244353, 2147483647)

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
    pre = REPO / PREREG
    m = re.search(r'leancert1_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------------- exact linear algebra (Fractions) ----------------
def matmul(A, B):
    guard()
    return [[sum(A[i][l] * B[l][j] for l in range(len(B))) for j in range(len(B[0]) if B else 0)] for i in range(len(A))]

def rref(M):
    """returns (R, pivots, E) with E*M = R (R in reduced row echelon form), exact."""
    guard()
    m = len(M); n = len(M[0]) if m else 0
    R = [[Fr(x) for x in row] for row in M]
    E = [[Fr(int(i == j)) for j in range(m)] for i in range(m)]
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if R[i][c] != 0), None)
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]; E[r], E[p] = E[p], E[r]
        inv = 1 / R[r][c]
        R[r] = [x * inv for x in R[r]]; E[r] = [x * inv for x in E[r]]
        for i in range(m):
            if i != r and R[i][c] != 0:
                f = R[i][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[r])]
                E[i] = [a - f * b for a, b in zip(E[i], E[r])]
        piv.append(c); r += 1
        if r == m:
            break
    return R, piv, E

def kernel_basis(M):
    """columns of an integer kernel basis (list of n-vectors)."""
    guard()
    n = len(M[0]); R, piv, _ = rref(M)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * n; v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        L = lcm(*[x.denominator for x in v])
        basis.append([int(x * L) for x in v])
    return basis

def solve_left(M, B):
    """P with P*M = B (exact), or None if some row of B is not in the row space of M."""
    guard()
    R, piv, E = rref(M)
    P = []
    for b in B:
        coeff = [Fr(b[c]) for c in piv]
        rec = [sum(coeff[i] * R[i][j] for i in range(len(piv))) for j in range(len(b))]
        if rec != [Fr(x) for x in b]:
            return None
        P.append([sum(coeff[i] * E[i][j] for i in range(len(piv))) for j in range(len(M))])
    return P

def transpose(A):
    return [list(r) for r in zip(*A)]

def split_cert(M, Kcols):
    """integer (P, Q, d) with P*M + K*Q = d*I_n and Q*K = d*I_k; K = matrix whose columns are Kcols."""
    guard()
    n = len(M[0]); k = len(Kcols)
    K = transpose(Kcols) if k else [[] for _ in range(n)]
    if k:
        _, rows, _ = rref(Kcols)            # pivot columns of K^T = k independent rows of K
        S = [[Fr(K[r][j]) for j in range(k)] for r in rows]
        Sinv = solve_left(S, [[Fr(int(i == j)) for j in range(k)] for i in range(k)])   # Sinv*S = I
        Q0 = [[Fr(0)] * n for _ in range(k)]
        for a in range(k):
            for b, r in enumerate(rows):
                Q0[a][r] = Sinv[a][b]
        KQ = [[sum(Fr(K[i][a]) * Q0[a][j] for a in range(k)) for j in range(n)] for i in range(n)]
    else:
        Q0 = []; KQ = [[Fr(0)] * n for _ in range(n)]
    B = [[Fr(int(i == j)) - KQ[i][j] for j in range(n)] for i in range(n)]
    P0 = solve_left(M, B)
    if P0 is None:
        return None
    d = lcm(1, *[x.denominator for row in P0 + Q0 for x in row])
    P = [[int(x * d) for x in row] for row in P0]
    Q = [[int(x * d) for x in row] for row in Q0]
    return P, Q, d, K

def verify_cert(M, K, P, Q, d):
    """exact integer verification; returns dict of booleans (this is the 'verify' half)."""
    guard()
    n = len(M[0]); k = len(K[0]) if K and K[0] else 0
    MK = [[sum(M[i][l] * K[l][j] for l in range(n)) for j in range(k)] for i in range(len(M))]
    zero = all(x == 0 for row in MK for x in row)
    split = all(sum(P[i][l] * M[l][j] for l in range(len(M))) + sum(K[i][a] * Q[a][j] for a in range(k))
                == (d if i == j else 0) for i in range(n) for j in range(n))
    inj = all(sum(Q[a][l] * K[l][b] for l in range(n)) == (d if a == b else 0) for a in range(k) for b in range(k))
    return {'MK=0': zero, 'PM+KQ=dI': split, 'QK=dI': inj, 'd!=0': d != 0}

def rank_mod_p(M, p):
    guard()
    A = [[x % p for x in row] for row in M]
    m = len(A); n = len(A[0]) if m else 0; r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(a - f * b) % p for a, b in zip(A[i], A[r])]
        r += 1
    return r

def sketch_rank(M, rng):
    """randomised sketch: rank of S*M*T mod p for three primes (S, T uniform random, seeded)."""
    guard()
    m = len(M); n = len(M[0]); out = []
    for p in PRIMES:
        S = [[rng.randrange(p) for _ in range(m)] for _ in range(m)]
        T = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        SMT = [[sum(S[i][l] * sum(M[l][q] * T[q][j] for q in range(n)) for l in range(m)) % p for j in range(n)] for i in range(m)]
        out.append(rank_mod_p(SMT, p))
    return out

# ---------------- T0: ABHY kinematic space ----------------
def abhy_matrices(n):
    """A: s_ij (i<j) in terms of planar X (eq. 10, cyclic indices, X_{a,a+1} = X_{1,n} = X_{a,a} = 0);
       C: momentum conservation rows sum_{j != i} s_ij = 0 (eq. 5).  Built independently."""
    guard()
    diags = [(i, j) for i in range(1, n + 1) for j in range(i + 2, n + 1) if not (i == 1 and j == n)]
    idx = {dg: t for t, dg in enumerate(diags)}
    pairs = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    def X(a, b):
        a = (a - 1) % n + 1; b = (b - 1) % n + 1
        a, b = min(a, b), max(a, b)
        return idx.get((a, b))
    A = []
    for (i, j) in pairs:
        row = [0] * len(diags)
        for (a, b, s) in ((i, j + 1, 1), (i + 1, j, 1), (i, j, -1), (i + 1, j + 1, -1)):
            t = X(a, b)
            if t is not None:
                row[t] += s
        A.append(row)
    C = [[1 if i in pr else 0 for pr in pairs] for i in range(1, n + 1)]
    return A, C, diags, pairs

# ---------------- T1: GPOS linear ACC (yQ = 1), unknowns (yu, yd, yL, ye) ----------------
GPOS_M = [[3, 3, 2, 1],      # grav^2 U(1):  6 yQ + 3 yu + 3 yd + 2 yL + ye = 0
          [0, 0, 1, 0],      # SU(2)^2 U(1): 3 yQ + yL = 0
          [1, 1, 0, 0]]      # SU(3)^2 U(1): 2 yQ + yu + yd = 0
GPOS_B = [-6, -3, -2]

def gpos_domain():
    guard()
    return sorted({Fr(p, q) for p in range(-10, 11) for q in range(1, 11)})

def acc_ok(u, d, l, e, yQ=1, cubic=True):
    # pure predicate (no guard: called ~2e6 times inside the guarded gpos_recount / run_planted / run_live)
    ok = (6 * yQ + 3 * u + 3 * d + 2 * l + e == 0) and (3 * yQ + l == 0) and (2 * yQ + u + d == 0)
    if cubic:
        ok = ok and (6 * yQ ** 3 + 3 * u ** 3 + 3 * d ** 3 + 2 * l ** 3 + e ** 3 == 0)
    return ok

def gpos_recount(cubic=True):
    """independent brute force over R^4 (pairs (yd, yL) x yu, ye derived from the gravitational ACC and tested in R)."""
    guard()
    R = gpos_domain(); Rs = set(R); sols = []
    for u in R:
        for d in R:
            for l in R:
                e = -(6 + 3 * u + 3 * d + 2 * l)
                if e in Rs and acc_ok(u, d, l, e, cubic=cubic):
                    sols.append((u, d, l, e))
    return sols

def gpos_line():
    guard()
    R, piv, E = rref(GPOS_M)
    x0 = [Fr(0)] * 4
    rhs = [sum(E[i][j] * GPOS_B[j] for j in range(3)) for i in range(len(piv))]
    for i, c in enumerate(piv):
        x0[c] = rhs[i]
    return [int(x) for x in x0], kernel_basis(GPOS_M)

def cubic_on_line(x0, k):
    """coefficients of the cubic ACC restricted to x0 + t k (exact polynomial in t, degree <= 3)."""
    guard()
    coeffs = [Fr(0)] * 4
    w = [3, 3, 2, 1]
    for wi, a, b in zip(w, x0, k):
        # (a + b t)^3
        for p_ in range(4):
            from math import comb
            coeffs[p_] += wi * comb(3, p_) * Fr(a) ** (3 - p_) * Fr(b) ** p_
    coeffs[0] += 6
    return coeffs

# ---------------- Lean emitter ----------------
def lean_mat(name, A, rows, cols):
    body = '; '.join(', '.join(str(x) for x in row) for row in A) if rows and cols else ''
    return f"def {name} : Matrix (Fin {rows}) (Fin {cols}) ℤ := !![{body}]"

def emit(target, M, K, P, Q, d):
    n = len(M[0]); k = len(K[0]) if K and K[0] else 0
    return '\n'.join([lean_mat(f'{target}_M', M, len(M), n), lean_mat(f'{target}_K', K, n, k),
                      lean_mat(f'{target}_P', P, n, len(M)), lean_mat(f'{target}_Q', Q, k, n),
                      f"def {target}_d : ℤ := {d}"])

# ---------------- modes ----------------
def run_planted():
    guard()
    ok = True
    # PL1 known small kernel: M = [[1,1,0],[0,1,1]], ker = span (1,-1,1)
    M = [[1, 1, 0], [0, 1, 1]]
    kb = kernel_basis(M)
    good = kb == [[1, -1, 1]]; ok &= good
    print(f"PL1 kernel of [[1,1,0],[0,1,1]] = {kb} (expect [[1,-1,1]]): {'OK' if good else 'FAIL'}")
    P, Q, d, K = split_cert(M, kb)
    v = verify_cert(M, K, P, Q, d); good = all(v.values()); ok &= good
    print(f"PL1 split cert P={P} Q={Q} d={d} verify {v}: {'OK' if good else 'FAIL'}")
    # PL2 planted wrong answer: kernel with one entry flipped must be REJECTED
    Kbad = [row[:] for row in K]; Kbad[2][0] = -Kbad[2][0]
    v = verify_cert(M, Kbad, P, Q, d); good = not v['MK=0'] and not v['PM+KQ=dI']; ok &= good
    print(f"PL2 flipped kernel entry {Kbad} -> verify {v}: {'REJECTED (OK)' if good else 'ACCEPTED (FAIL)'}")
    # PL3 corrupted split certificate (one P entry +1) must be REJECTED
    Pbad = [row[:] for row in P]; Pbad[0][0] += 1
    v = verify_cert(M, K, Pbad, Q, d); good = not v['PM+KQ=dI']; ok &= good
    print(f"PL3 corrupted P -> verify {v}: {'REJECTED (OK)' if good else 'ACCEPTED (FAIL)'}")
    # PL4 planted wrong dimension: claim a 2-dim kernel for M (extra vector e1) -> no valid cert
    v = verify_cert(M, [[1, 1], [-1, 0], [1, 0]], [[0, 0]] * 3, [[0, 0, 0]] * 2, 1); good = not v['MK=0']; ok &= good
    print(f"PL4 fake extra kernel vector -> MK=0 {v['MK=0']}: {'REJECTED (OK)' if good else 'ACCEPTED (FAIL)'}")
    # PL5 n = 4 Mandelstam formula: s12 = X13, s23 = X24, s13 = -X13 - X24 (u = -s - t)
    A4, C4, diags4, pairs4 = abhy_matrices(4)
    rows = dict(zip(pairs4, A4))
    good = rows[(1, 2)] == [1, 0] and rows[(2, 3)] == [0, 1] and rows[(1, 3)] == [-1, -1]; ok &= good
    print(f"PL5 ABHY n=4 eq.(10): s12 {rows[(1,2)]}, s23 {rows[(2,3)]}, s13 {rows[(1,3)]} over (X13, X24): {'OK' if good else 'FAIL'}")
    # PL6 sketch detects a rank-deficient matrix (row3 = row1 + row2)
    rng = random.Random(SEED + 6)
    Md = [[1, 2, 3], [0, 1, 4], [1, 3, 7]]
    sk = sketch_rank(Md, rng); good = sk == [2, 2, 2]; ok &= good
    print(f"PL6 sketch rank of rank-2 3x3 = {sk} (expect [2,2,2]): {'OK' if good else 'FAIL'}")
    # PL7 planted wrong N_ACC tuple (-4, 2, -3, 7) violates the ACC; true SM tuple satisfies them
    good = (not acc_ok(Fr(-4), Fr(2), Fr(-3), Fr(7))) and acc_ok(Fr(-4), Fr(2), Fr(-3), Fr(6)); ok &= good
    print(f"PL7 planted tuple (-4,2,-3,7) rejected, SM (-4,2,-3,6) accepted: {'OK' if good else 'FAIL'}")
    # PL8 detector power: dropping the cubic ACC must give a count > 2
    nlin = len(gpos_recount(cubic=False)); good = nlin > 2; ok &= good
    print(f"PL8 linear-ACC-only count = {nlin} (> 2 expected): {'OK' if good else 'FAIL'}")
    print('PLANTED:', 'ALL OK' if ok else 'FAIL')
    return ok

def run_live():
    guard()
    rng = random.Random(SEED)
    out = {'run_id': RUN_ID, 'seed': SEED, 'primes': PRIMES, 'T0': {}, 'T1': {}}
    lean = []
    # T0: ABHY n = 5, 6 (declared), 7 (held out)
    for n in (5, 6, 7):
        t0 = time.time()
        A, C, diags, pairs = abhy_matrices(n)
        CA = matmul(C, A); held = all(x == 0 for row in CA for x in row)
        kerC = kernel_basis(C)
        sk = sketch_rank(C, rng); skA = sketch_rank(A, rng)
        cert = split_cert(C, transpose(A))
        if cert is None:
            res = {'C*A=0 (held-out eq.5 vs eq.10)': held, 'cert': None}
        else:
            P, Q, d, K = cert
            v = verify_cert(C, K, P, Q, d)
            res = {'C*A=0 (held-out eq.5 vs eq.10)': held, 'dim ker C (exact rref)': len(kerC),
                   'rank C sketch': sk, 'rank A sketch': skA, 'expected n(n-3)/2': n * (n - 3) // 2,
                   'verify': v, 'd': d, 'sizes': {'C': [len(C), len(C[0])], 'A': [len(A), len(A[0])]},
                   'seconds': round(time.time() - t0, 3)}
            if n in (5, 6, 7):
                lean.append(emit(f'abhy{n}', C, A, P, Q, d))
        out['T0'][n] = res
        print(f"T0 n={n}: {json.dumps(res, default=str)}")
    # T1: GPOS linear line + cubic + recount
    x0, kb = gpos_line()
    P, Q, d, K = split_cert(GPOS_M, kb)
    v = verify_cert(GPOS_M, K, P, Q, d)
    part = [sum(GPOS_M[i][j] * x0[j] for j in range(4)) for i in range(3)]
    cub = cubic_on_line(x0, kb[0])
    roots = sorted({t for t in (Fr(p, q) for p in range(-40, 41) for q in range(1, 5)) if sum(c * t ** i for i, c in enumerate(cub)) == 0})
    sols = gpos_recount(cubic=True)
    R = gpos_domain()
    out['T1'] = {'x0': x0, 'kernel': kb, 'M*x0': part, 'b': GPOS_B, 'verify': v, 'd': d, 'P': P, 'Q': Q,
                 'cubic_on_line_coeffs(t^0..t^3)': [str(c) for c in cub], 'rational_roots': [str(r) for r in roots],
                 'sketch_rank_M': sketch_rank(GPOS_M, rng), '|R|': len(R),
                 'recount_N_ACC': len(sols), 'solutions': [[str(x) for x in s] for s in sols]}
    print(f"T1: {json.dumps(out['T1'], default=str)}")
    lean.append(emit('gpos', GPOS_M, K, P, Q, d))
    lean.append(f"def gpos_x0 : Fin 4 → ℤ := ![{', '.join(map(str, x0))}]")
    t0ok = all(out['T0'][n].get('cert') is not None or 'verify' in out['T0'][n] for n in (5, 6, 7))
    certs_ok = all(all(out['T0'][n]['verify'].values()) for n in (5, 6, 7) if 'verify' in out['T0'][n]) and all(v.values())
    dims_ok = all(out['T0'][n].get('dim ker C (exact rref)') == n * (n - 3) // 2 for n in (5, 6, 7))
    held_ok = all(out['T0'][n]['C*A=0 (held-out eq.5 vs eq.10)'] for n in (5, 6, 7))
    sketch_ok = all(out['T0'][n]['rank C sketch'] == [n] * 3 for n in (5, 6, 7) if 'rank C sketch' in out['T0'][n])
    nacc_ok = len(sols) == 2 and [r for r in roots] == [Fr(-4), Fr(2)]
    out['summary'] = {'T0 certs verified': certs_ok and t0ok, 'T0 dims = n(n-3)/2': dims_ok, 'held-out C*A=0': held_ok,
                      'sketch = exact': sketch_ok, 'T1 N_ACC recount = 2 and line roots {-4,2}': nacc_ok}
    verdict = 'CERTS-VERIFIED (exact; Lean status in result)' if all(out['summary'].values()) else 'CERT-MISMATCH'
    out['verdict_python'] = verdict
    print('SUMMARY:', json.dumps(out['summary']))
    print('VERDICT (python half):', verdict)
    (HERE.parent / 'leancert1_live.json').write_text(json.dumps(out, indent=1, default=str))
    (HERE.parent / 'certs_lean.txt').write_text('\n\n'.join(lean) + '\n')
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    print(f"run {RUN_ID} seed {SEED} mode {mode} ({time.strftime('%Y-%m-%d %H:%M:%S %Z')})")
    if mode == 'planted':
        sys.exit(0 if run_planted() else 1)
    elif mode == 'live':
        run_live()
    else:
        sys.exit(f"unknown mode {mode}")

if __name__ == '__main__':
    main()
