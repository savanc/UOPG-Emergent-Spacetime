#!/usr/bin/env python3
"""LEAN-CERT-2 locked checker (one-rung own pick (author approved 2026-10-27)).
Prereg: prereg/LEAN-CERT-2-modp-frwzw-2026-10-28.md.  Run id LEANCERT2-2026-10-28-r1.
Target: the 8 exact rank counts of FR-WZW (sims/frwzw/rank_count.py, SIMULATED 2026-10-16; dims of the evaluated
constraint kernels for k = 0..3, sigma = +1/-1: 1,2,5,10 / 0,0,0,2; largest matrix 120 x 56) get integer split
certificates (M K = 0, P M + K Q = d 1, Q K = d 1) computed by MOD-P elimination + multi-prime CRT + rational
reconstruction (no exact rational elimination in the certificate path), verified exactly in Python (mirror of the
Lean list checker), then pasted into Lean (PositiveGeometryEmergentSpaceTime.LeanCert2) and checked by `decide +kernel`.
Matrices: regenerated verbatim from rank_count.py (same seed 20261016, same 40 points, same rows), each row scaled
to a primitive integer row (kernel unchanged).
Planted: PL1 ABHY 1711.09102 eq. (5) conservation matrices n = 5, 6, 7 (published control dim = n(n-3)/2);
  PL2 synthetic 120 x 56 integer matrix of rank 46 (kernel dim 10) with entries of live-like size (>= 25 digits);
  PL3 synthetic 120 x 56, kernel dim 2 (deformed/large-entry version of the sigma = -1 k = 3 shape).
Broken (already proved false): B1 the claim dim ker(ABHY eq5, n = 6) = 10, refuted by the PROVED
  `PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_finrank` (= 9); a 10-column certificate (true certificate plus column d*e_0 in K and
  row e_0 in Q) must be REJECTED by the mirror checker (and, in Lean, by `decide`).  B2 (supplementary) a dim-9
  claim on PL2 (true certificate minus its last kernel column) must be REJECTED.
Lean side (prereg section 4): a list-based checker (rows/columns as `List (List ℤ)`, dot products by structural
  recursion), whose soundness is proved once in `PositiveGeometryEmergentSpaceTime.LeanCert2` and which feeds `PositiveGeometryEmergentSpaceTime.LeanCert.finrank_ker`.
Null rates (no tuning): N1 mod-p sketch: ranks of every live matrix mod 20 fresh 31-bit primes vs the certified
  rank; disagreement fraction reported.  N2 corruption: 60 single-entry +-1 corruptions per live certificate
  (random among K, P, Q); acceptance fraction by the mirror checker must be 0.
Rival baseline (strong): the original FR-WZW exact Fraction Gaussian elimination (qrank, copied verbatim) on the
  same rows, plus sympy Matrix.rank on the integerised matrix; both must equal the certified rank.
Verdict rule (prereg): ILL-DEFINED if any planted case fails, B1/B2 is accepted, or N2 > 0.  CONTRADICTS if any
  certified dim differs from the SIMULATED FR-WZW dim.  Otherwise CERTS-OK (python); the Lean verdict is set by
  the Lean module (UPGRADED / PARTIAL-LIMIT), see prereg.
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main.  No pass flag; caches
keyed by origin/main sha only; `git fetch` once per process.
"""
import hashlib, itertools, json, random, re, subprocess, sys, time
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/LEAN-CERT-2-modp-frwzw-2026-10-28.md'
OUTDIR = HERE.parent
SIM_DIMS = {(0, 1): 1, (0, -1): 0, (1, 1): 2, (1, -1): 0, (2, 1): 5, (2, -1): 0, (3, 1): 10, (3, -1): 2}

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
    m = re.search(r'leancert2_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------------- primes / modular arithmetic ----------------
def _is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def primes_from(start, count):
    out, p = [], start
    while len(out) < count:
        if _is_prime(p): out.append(p)
        p += 1
    return out

def _rref_modp(A, p):
    """Row-reduce A mod p; return (rank, pivot columns)."""
    A = [[x % p for x in r] for r in A]
    m = len(A); n = len(A[0]) if A else 0
    r, piv = 0, []
    for c in range(n):
        q = next((i for i in range(r, m) if A[i][c]), None)
        if q is None: continue
        A[r], A[q] = A[q], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
        if r == m: break
    return r, piv

def _ratrec(a, mod):
    """Rational reconstruction of a mod `mod` (Wang); None if no |num|,den <= sqrt(mod/2)."""
    bound = isqrt(mod // 2)
    r0, r1, s0, s1 = mod, a % mod, 0, 1
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound: return None
    if s1 < 0: r1, s1 = -r1, -s1
    if gcd(r1, s1) != 1: return None
    return Fraction(r1, s1)

def _inv_modp(B, p):
    n = len(B)
    A = [[x % p for x in row] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(B)]
    for c in range(n):
        q = next((i for i in range(c, n) if A[i][c]), None)
        if q is None: return None
        A[c], A[q] = A[q], A[c]
        inv = pow(A[c][c], p - 2, p)
        A[c] = [x * inv % p for x in A[c]]
        for i in range(n):
            if i != c and A[i][c]:
                f = A[i][c]; A[i] = [(x - f * y) % p for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]

# ---------------- certificate pipeline (mod-p sketch + CRT + rational reconstruction) ----------------
def certify(M, max_primes=4000):
    """Integer certificate for ker M (M: list of integer rows).  Returns dict with Mr, Kc, Kr, Pr, Qr, d, rank."""
    guard()
    m = len(M); n = len(M[0])
    p0 = primes_from(2**31 + 11, 1)[0]
    rank, piv = _rref_modp(M, p0)
    # pivot rows: greedy mod p0 on the pivot columns
    rows = []; cur = []
    for i in range(m):
        trial = cur + [[M[i][c] for c in piv]]
        if _rref_modp(trial, p0)[0] == len(trial):
            cur = trial; rows.append(i)
            if len(rows) == rank: break
    free = [c for c in range(n) if c not in piv]
    r = len(rows)
    if r == 0:
        Binv = []
    else:
        B = [[M[i][c] for c in piv] for i in rows]
        # CRT + rational reconstruction of B^{-1}; stop when stable for two consecutive primes and exact check passes
        mod, acc, prev, Binv = 1, None, None, None
        plist = primes_from(2**31 + 101, max_primes)
        for p in plist:
            inv = _inv_modp(B, p)
            if inv is None: continue
            if acc is None:
                acc = inv; mod = p
            else:
                # CRT combine
                mi = pow(mod, -1, p)
                acc = [[a + mod * ((b - a) * mi % p) for a, b in zip(ra, rb)] for ra, rb in zip(acc, inv)]
                mod *= p
            rec = [[_ratrec(a, mod) for a in row] for row in acc]
            if any(x is None for row in rec for x in row):
                continue
            if rec == prev:
                # sketch-and-verify: exact check B * rec == I
                ok = all(sum(B[i][l] * rec[l][j] for l in range(r)) == (1 if i == j else 0)
                         for i in range(r) for j in range(r))
                if ok:
                    Binv = rec; break
            prev = rec
        if Binv is None:
            raise RuntimeError("rational reconstruction did not stabilise")
    den = 1
    for row in Binv:
        for x in row: den = den * x.denominator // gcd(den, x.denominator)
    d = den
    k = len(free)
    # K (n x k): K[free_j, j] = d ; K[piv_a, j] = -(d Binv M[R, free_j])_a
    Kr = [[0] * k for _ in range(n)]
    for j, fc in enumerate(free):
        Kr[fc][j] = d
        col = [M[i][fc] for i in rows]
        for a, pc in enumerate(piv):
            v = sum(Binv[a][l] * col[l] for l in range(r)) * d
            assert v.denominator == 1
            Kr[pc][j] = -int(v)
    # P (n x m): P[piv_a, rows_l] = d Binv[a][l]
    Pr = [[0] * m for _ in range(n)]
    for a, pc in enumerate(piv):
        for l, ri in enumerate(rows):
            v = Binv[a][l] * d; assert v.denominator == 1
            Pr[pc][ri] = int(v)
    # Q (k x n): Q[j, free_j] = 1
    Qr = [[1 if c == fc else 0 for c in range(n)] for fc in free]
    Kc = [[Kr[i][j] for i in range(n)] for j in range(k)]
    return dict(Mr=M, Kr=Kr, Kc=Kc, Pr=Pr, Qr=Qr, d=d, rank=r, k=k, m=m, n=n, primes_used=None)

def dotL(a, b):
    return sum(x * y for x, y in zip(a, b))

def mirror_check(c):
    """Mirror of the Lean list checker: lengths, M K = 0, P M + K Q = d 1, Q K = d 1, d != 0."""
    guard()
    Mr, Kr, Pr, Qr, d = c['Mr'], c['Kr'], c['Pr'], c['Qr'], c['d']
    m, n = len(Mr), len(Mr[0])
    k = len(Kr[0]) if Kr else 0
    if d == 0: return False
    if any(len(r) != n for r in Mr) or len(Kr) != n or any(len(r) != k for r in Kr): return False
    if len(Pr) != n or any(len(r) != m for r in Pr) or len(Qr) != k or any(len(r) != n for r in Qr): return False
    Mc = [[Mr[i][j] for i in range(m)] for j in range(n)]
    Kc = [[Kr[i][j] for i in range(n)] for j in range(k)]
    Qc = [[Qr[i][j] for i in range(k)] for j in range(n)]
    for r in Mr:
        for col in Kc:
            if dotL(r, col) != 0: return False
    for i in range(n):
        for j in range(n):
            if dotL(Pr[i], Mc[j]) + dotL(Kr[i], Qc[j]) != (d if i == j else 0): return False
    for a in range(k):
        for b in range(k):
            if dotL(Qr[a], Kc[b]) != (d if a == b else 0): return False
    return True

def integerise(rows):
    out = []
    for r in rows:
        fr = [Fraction(x) for x in r]
        den = 1
        for x in fr: den = den * x.denominator // gcd(den, x.denominator)
        ints = [int(x * den) for x in fr]
        g = 0
        for x in ints: g = gcd(g, x)
        out.append([x // g for x in ints] if g else ints)
    return out

# ---------------- FR-WZW matrices, verbatim construction from sims/frwzw/rank_count.py ----------------
def frwzw_matrices():
    guard()
    import sympy as sp
    random.seed(20261016)
    def kin():
        while True:
            lam = [sp.Matrix([random.randint(-9, 9), random.randint(-9, 9)]) for _ in range(5)]
            lt = [sp.Matrix([random.randint(-9, 9), random.randint(-9, 9)]) for _ in range(3)]
            A = sp.Matrix.hstack(lam[3], lam[4])
            if A.det() == 0: continue
            S = sum((lam[i] * lt[i].T for i in range(3)), sp.zeros(2, 2))
            X = A.solve(-S)
            lt += [X[0, :].T, X[1, :].T]
            P = [lam[i] * lt[i].T for i in range(5)]
            assert sum(P, sp.zeros(2, 2)) == sp.zeros(2, 2) and all(p.det() == 0 for p in P)
            if any(mm.det() == 0 for mm in [P[i] + P[(i + 1) % 5] for i in range(5)]): continue
            return P
    vec = lambda mm: [mm[0, 0], mm[0, 1], mm[1, 0], mm[1, 1]]
    def eps(a, b, c, d): return sp.Matrix([vec(a), vec(b), vec(c), vec(d)]).det()
    def s(P, i, j): return (P[i] + P[j]).det()
    def X(P): return [s(P, i, (i + 1) % 5) for i in range(5)]
    def monos(k):
        out = []
        for dd in range(k + 1):
            for c in itertools.combinations_with_replacement(range(5), dd): out.append(c)
        return out
    cyc = lambda P: [P[1], P[2], P[3], P[4], P[0]]
    rev = lambda P: [P[4], P[3], P[2], P[1], P[0]]
    par = lambda P: [p.T for p in P]
    def basisvals(P, ms):
        x = X(P); e = eps(P[0], P[1], P[2], P[3])
        return [e * sp.prod([x[i] for i in m]) for m in ms]
    pts = [kin() for _ in range(40)]
    mats, raw = {}, {}
    for k in range(4):
        ms = monos(k)
        for sigma in (1, -1):
            rows = []
            for P in pts:
                b = basisvals(P, ms)
                rows.append([u - v for u, v in zip(basisvals(cyc(P), ms), b)])
                rows.append([u - sigma * v for u, v in zip(basisvals(rev(P), ms), b)])
                rows.append([u + v for u, v in zip(basisvals(par(P), ms), b)])
            raw[(k, sigma)] = [[Fraction(int(sp.numer(x)), int(sp.denom(x))) for x in r] for r in rows]
            mats[(k, sigma)] = integerise(raw[(k, sigma)])
    return mats, raw

def qrank_original(A):
    """Verbatim logic of sims/frwzw/rank_count.py qrank (exact Fraction elimination), the rival baseline."""
    A = [list(r) for r in A]
    r = 0; nc = len(A[0]) if A else 0
    for c in range(nc):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r

# ---------------- planted / broken builders ----------------
def abhy_eq5(n):
    pairs = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    return [[1 if (p[0] == i or p[1] == i) else 0 for p in pairs] for i in range(1, n + 1)]

def synthetic(m, n, rank, seed, digits=25):
    rng = random.Random(seed)
    big = 10 ** digits
    L = [[rng.randint(-big, big) for _ in range(rank)] for _ in range(m)]
    R = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(rank)]
    return [[sum(L[i][t] * R[t][j] for t in range(rank)) for j in range(n)] for i in range(m)]

def maxdigits(c):
    return max(len(str(abs(x))) for key in ('Mr', 'Kr', 'Pr') for row in c[key] for x in row) if c['Mr'] else 0

# ---------------- modes ----------------
def run_planted():
    guard_banner()
    res = []
    for n in (5, 6, 7):
        c = certify(abhy_eq5(n)); ok = mirror_check(c)
        res.append(dict(case=f'PL1 ABHY n={n}', dim=c['k'], expect=n * (n - 3) // 2, mirror=ok,
                        pass_=ok and c['k'] == n * (n - 3) // 2))
    for name, rk, seed in (('PL2 synthetic 120x56 rank 46', 46, 1), ('PL3 synthetic 120x56 rank 54', 54, 2)):
        M = synthetic(120, 56, rk, seed)
        t = time.time(); c = certify(M); ok = mirror_check(c)
        res.append(dict(case=name, dim=c['k'], expect=56 - rk, mirror=ok, pass_=ok and c['k'] == 56 - rk,
                        maxdigits=maxdigits(c), secs=round(time.time() - t, 2)))
    lines = [json.dumps(r) for r in res]
    lines.append(f"PLANTED ALL OK: {all(r['pass_'] for r in res)}")
    print("\n".join(lines)); (OUTDIR / 'leancert2_planted.txt').write_text("\n".join(lines) + "\n")
    return all(r['pass_'] for r in res)

def run_broken():
    guard_banner()
    out = []
    c = certify(abhy_eq5(6))
    n = c['n']; d = c['d']
    # B1: force a 10-column claim by appending column d*e_0 to K and row e_0 to Q
    Kr = [row + [d if i == 0 else 0] for i, row in enumerate(c['Kr'])]
    Qr = c['Qr'] + [[1 if j == 0 else 0 for j in range(n)]]
    b1 = dict(c, Kr=Kr, Qr=Qr, k=c['k'] + 1)
    acc1 = mirror_check(b1)
    out.append(f"B1 ABHY n=6 claimed dim 10 (PROVED false: PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_finrank = 9): accepted={acc1}")
    c2 = certify(synthetic(120, 56, 46, 1))
    # B2: claim dim 9 (rank 47) on PL2 by dropping the last kernel column of K and the last row of Q
    b2 = dict(c2, Kr=[row[:-1] for row in c2['Kr']], Qr=c2['Qr'][:-1], k=c2['k'] - 1)
    acc2 = mirror_check(b2)
    out.append(f"B2 PL2 claimed dim 9 (true dim 10 by construction): accepted={acc2}")
    out.append(f"BROKEN ALL REJECTED: {not acc1 and not acc2}")
    print("\n".join(out)); (OUTDIR / 'leancert2_broken.txt').write_text("\n".join(out) + "\n")
    return not acc1 and not acc2

def to_lean(name, c):
    def L(rows): return "[" + ",\n  ".join("[" + ", ".join(str(x) for x in r) + "]" for r in rows) + "]"
    return (f"def {name}_M : List (List ℤ) := {L(c['Mr'])}\n"
            f"def {name}_K : List (List ℤ) := {L(c['Kr'])}\n"
            f"def {name}_P : List (List ℤ) := {L(c['Pr'])}\n"
            f"def {name}_Q : List (List ℤ) := {L(c['Qr'])}\n"
            f"def {name}_d : ℤ := {c['d']}\n"
            f"-- {name}: m = {c['m']}, n = {c['n']}, rank = {c['rank']}, k = {c['k']}\n")

def run_live():
    guard_banner()
    t0 = time.time()
    mats, raw = frwzw_matrices()
    gen_secs = round(time.time() - t0, 1)
    rng = random.Random(20261028)
    primes20 = primes_from(2**30 + 3, 20)
    report, lean_src = [], ["-- LEAN-CERT-2 certificates, run LEANCERT2-2026-10-28-r1 (generated by leancert2_checker.py live)"]
    corrupt_acc = corrupt_tot = 0; sketch_dis = sketch_tot = 0
    for (k, sigma), M in sorted(mats.items(), key=lambda kv: (kv[0][0], -kv[0][1])):
        guard()
        t = time.time(); c = certify(M); csecs = round(time.time() - t, 2)
        ok = mirror_check(c)
        # rival baselines
        rk_orig = qrank_original(raw[(k, sigma)])
        import sympy as sp
        rk_sym = sp.Matrix(M).rank() if c['n'] <= 21 else None
        # N1 mod-p sketch null rate
        dis = sum(1 for p in primes20 if _rref_modp(M, p)[0] != c['rank'])
        sketch_dis += dis; sketch_tot += len(primes20)
        # N2 corruption null rate (inlined loop)
        acc = 0
        for _ in range(60):
            which = rng.choice([w for w in ('Kr', 'Pr', 'Qr') if c[w] and c[w][0]])
            mat = [list(r) for r in c[which]]
            i = rng.randrange(len(mat)); j = rng.randrange(len(mat[0]))
            mat[i][j] += rng.choice((-1, 1))
            if mirror_check(dict(c, **{which: mat})): acc += 1
        corrupt_acc += acc; corrupt_tot += 60
        name = f"frwzw_k{k}{'p' if sigma == 1 else 'm'}"
        report.append(dict(case=name, k=k, sigma=sigma, m=c['m'], n=c['n'], rank=c['rank'], dim=c['k'],
                           sim_dim=SIM_DIMS[(k, sigma)], mirror=ok, rival_qrank=rk_orig, rival_sympy=rk_sym,
                           sketch_disagree=dis, corrupt_accepted=acc, d_digits=len(str(c['d'])),
                           maxdigits=maxdigits(c), cert_secs=csecs))
        lean_src.append(to_lean(name, c))
    ill = (not all(r['mirror'] for r in report)) or corrupt_acc > 0
    contra = any(r['dim'] != r['sim_dim'] for r in report)
    rival_ok = all(r['rival_qrank'] == r['rank'] and (r['rival_sympy'] in (None, r['rank'])) for r in report)
    verdict = 'ILL-DEFINED' if ill else ('CONTRADICTS' if contra else 'CERTS-OK')
    lines = [json.dumps(r) for r in report]
    lines += [f"matrix generation secs: {gen_secs}",
              f"N1 mod-p sketch disagreement: {sketch_dis}/{sketch_tot}",
              f"N2 corruption acceptance: {corrupt_acc}/{corrupt_tot}",
              f"rival baselines agree: {rival_ok}",
              f"PYTHON VERDICT: {verdict}"]
    print("\n".join(lines))
    (OUTDIR / 'leancert2_output.txt').write_text("\n".join(lines) + "\n")
    (OUTDIR / 'certs_lean.txt').write_text("\n".join(lean_src))
    (OUTDIR / 'leancert2_live.json').write_text(json.dumps(report, indent=1) + "\n")
    return verdict

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'planted': run_planted()
    elif mode == 'broken': run_broken()
    elif mode == 'live': run_live()
    else: sys.exit("usage: leancert2_checker.py planted|broken|live")
