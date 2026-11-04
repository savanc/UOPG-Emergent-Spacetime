#!/usr/bin/env python3
"""JORD-1 locked checker (exploration rung R1 of 3; author approved 2026-10-28).
Prereg: prereg/JORD-1-positivity-closure-2026-10-28.md.  Run id JORD1-2026-10-28-r1.
Question (tier A, primary): inside Der(h3(O)) = f4, is g_sm := stab(E1) ∩ setstab(B = h3(C)) CLOSED in the
  Galois sense, i.e. closure(g_sm) := stab(Fix(g_sm)) == g_sm ?  (closure(h) ⊇ h always.)  Equivalent (lemma, prereg
  §3): some set S of vectors -- hence some finite set of points of the closed positive cone, via spectral
  idempotents -- has pointwise stabiliser exactly g_sm  <=>  g_sm is closed.
  POSITIVITY-CLOSED iff dim closure == dim g_sm; NOT-POSITIVITY-CLOSED (NO-GO for positivity-native pointwise
  data) iff larger; UNCLASSIFIED otherwise.
Tier B (TAUT / OCT-1' audit, report + label): family F_B of 18 sub-algebra choices (X = h2(K1) on idx {2,3},
  B = h3(K2), K1 ⊆ K2 in R ⊂ C ⊂ H ⊂ O, 10 pairs; 4 B-only; 4 X-only).  Invariants: dim, rank (generic centraliser,
  min over 3 seeded draws), centre dim, derived dim, closure dim, compact-type candidates.  SM-type := (dim 12,
  rank 4, centre 1, derived 11).  Label CHOICE-UNIQUE / CHOICE-AMONG-k / CHOICE-NONE.
Family F_A (Galois-lemma consistency): 51 idempotents (E1,E2,E3 and P_ij(±e_k)), all subsets of size 1 and 2:
  SM-type stabiliser count must be 0 if NOT-POSITIVITY-CLOSED (else ILL-DEFINED, internal inconsistency).
Rival (report only): Krasnov J-commutant in stab(E1) on V_1/2(E1) = (b, c) coords, J ∈ {L⊕L, R⊕R, L⊕R, R⊕L}
  with u = e1.  Null: fraction of F_B closed; fraction of F_B SM-type.
Planted (CITED, must hold): P1 Fano table passes composition+alternativity; P2 dim Der = 52 (lower: rank of inner
  derivations; upper: mod-p nullity of the derivation system, two primes); P3 dim stab(E1) = 36; P4 dim
  stab(E1,E2,E3) = 28; P5 dim setstab(h3(C)) = 16; P6 g_sm SM-type (12,4,1,11); P7 Baez-Schwahn form
  setstab(h2(C) on {2,3}) ∩ setstab(h3(C)) == g_sm (same subspace); P8 dim Der h3(R), h3(C), h3(H) = 3, 8, 21.
Valid alternatives (must be ACCEPTED): V1 u = e2 gives the same (dim, rank, centre, derived, closure dim);
  V2 stab(E2+E3) == stab(E1) as subspaces; V3 rank of g_sm with seed+1 equals rank with seed.
Broken (must be REJECTED): B1 table with e1e2 = e2e1 = e4 fails the composition test; B2 claim dim stab(E1) = 52;
  B3 D = matrix unit E_00 (E1 -> E1) is not a derivation.
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main.  No pass flag; caches
keyed by origin/main sha only; `git fetch` once per process.
"""
import hashlib, itertools, json, random, re, subprocess, sys, time
from fractions import Fraction
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/JORD-1-positivity-closure-2026-10-28.md'
OUTDIR = HERE.parent
SEED = 20261028

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
    m = re.search(r'jord1_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------------- octonions ----------------
FANO = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]

def omul_table(lines=FANO, broken=False):
    """T[i][j] = (sign, k) with e_i e_j = sign e_k.  broken=True sets e2 e1 = +e4 (commuting pair)."""
    T = [[None] * 8 for _ in range(8)]
    for i in range(8):
        T[0][i] = (1, i); T[i][0] = (1, i)
    for i in range(1, 8):
        T[i][i] = (-1, 0)
    for (a, b, c) in lines:
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            T[x][y] = (1, z); T[y][x] = (-1, z)
    if broken:
        T[2][1] = (1, 4)
    return T

def omul(x, y, T):
    out = [0] * 8
    for i in range(8):
        if x[i] == 0: continue
        for j in range(8):
            if y[j] == 0: continue
            s, k = T[i][j]
            out[k] += s * x[i] * y[j]
    return out

def oconj(x):
    return [x[0]] + [-v for v in x[1:]]

def onorm(x):
    return sum(v * v for v in x)

def table_ok(T):
    """Composition N(xy) = N(x)N(y) and alternativity (xx)y = x(xy) on x, y in {e_i} ∪ {e_i ± e_j}."""
    guard()
    vecs = []
    for i in range(8):
        v = [0] * 8; v[i] = 1; vecs.append(v)
    for i in range(8):
        for j in range(i + 1, 8):
            for s in (1, -1):
                v = [0] * 8; v[i] = 1; v[j] = s; vecs.append(v)
    for x in vecs:
        xx = omul(x, x, T)
        for y in vecs:
            xy = omul(x, y, T)
            if onorm(xy) != onorm(x) * onorm(y): return False
            if omul(xx, y, T) != omul(x, xy, T): return False
    return True

# ---------------- h3(O) ----------------
# basis: 0..2 E1..E3; 3..10 'a' at (1,2) [0-based]; 11..18 'b' at (2,0); 19..26 'c' at (0,1).
OFF = {'a': (3, (1, 2)), 'b': (11, (2, 0)), 'c': (19, (0, 1))}
N = 27

def to_mat(v):
    M = [[[0] * 8 for _ in range(3)] for _ in range(3)]
    for d in range(3):
        M[d][d][0] = v[d]
    for _, (base, (r, c)) in OFF.items():
        o = list(v[base:base + 8])
        M[r][c] = o; M[c][r] = oconj(o)
    return M

def from_mat(M):
    v = [0] * N
    for d in range(3):
        assert all(x == 0 for x in M[d][d][1:]), "diagonal not real"
        v[d] = M[d][d][0]
    for _, (base, (r, c)) in OFF.items():
        assert M[c][r] == oconj(M[r][c]), "not hermitian"
        v[base:base + 8] = M[r][c]
    return v

def jprod2(x, y, T):
    """2 x∘y = xy + yx (octonion 3x3 matrices)."""
    X, Y = to_mat(x), to_mat(y)
    P = [[[0] * 8 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = [0] * 8
            for k in range(3):
                for t in (omul(X[i][k], Y[k][j], T), omul(Y[i][k], X[k][j], T)):
                    acc = [a + b for a, b in zip(acc, t)]
            P[i][j] = acc
    return from_mat(P)

def unit(i, n=N):
    v = [0] * n; v[i] = 1; return v

def ctable(T):
    return [[jprod2(unit(i), unit(j), T) for j in range(N)] for i in range(N)]

def sub_idx(units):
    """coordinates of h3(K) where K = span{e_u : u in units} (units must contain 0)."""
    idx = [0, 1, 2]
    for _, (base, _) in OFF.items():
        idx += [base + u for u in units]
    return sorted(idx)

KUNITS = {'R': [0], 'C': [0, 1], 'H': [0, 1, 2, 4], 'O': list(range(8))}
KUNITS_E2 = {'C': [0, 2], 'H': [0, 2, 3, 5]}   # V1: u = e2 (Fano line (2,3,5))

# ---------------- exact linear algebra ----------------
def rref(rows, ncols):
    M = [[Fraction(x) for x in r] for r in rows if any(r)]
    piv, r = [], 0
    for c in range(ncols):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    return M[:r], piv

def nullspace(rows, ncols):
    R, piv = rref(rows, ncols)
    ps = set(piv)
    out = []
    for f in range(ncols):
        if f in ps: continue
        v = [Fraction(0)] * ncols; v[f] = Fraction(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][f]
        out.append(v)
    return out

def rank(rows, ncols):
    return len(rref(rows, ncols)[1])

def intvec(v):
    den = 1
    for x in v:
        den = den * Fraction(x).denominator // gcd(den, Fraction(x).denominator)
    w = [int(Fraction(x) * den) for x in v]
    g = 0
    for x in w: g = gcd(g, abs(x))
    return [x // g for x in w] if g else w

def rank_modp(A, p):
    import numpy as np
    A = np.array(A, dtype=np.int64) % p
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        if r == rows: break
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0: continue
        i = r + int(nz[0])
        if i != r: A[[r, i]] = A[[i, r]]
        A[r] = (A[r] * pow(int(A[r, c]), p - 2, p)) % p
        col = A[:, c].copy(); col[r] = 0
        nzr = np.nonzero(col)[0]
        if len(nzr):
            A[nzr] = (A[nzr] - (col[nzr, None] * A[r][None, :]) % p) % p
        r += 1
    return r

# ---------------- derivations ----------------
def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n) if A[i][k]) for j in range(n)] for i in range(n)]

def is_der(D, C, idx):
    """D (matrix on coords idx, as full N x N with zeros elsewhere) satisfies D(b_i∘b_j) = Db_i∘b_j + b_i∘Db_j
    for all basis i, j in idx (C = 2∘ table)."""
    guard()
    cols = {i: [D[k][i] for k in range(N)] for i in idx}
    def prod(x, y):
        out = [0] * N
        for i in idx:
            if x[i] == 0: continue
            for j in idx:
                if y[j] == 0: continue
                for k, v in enumerate(C[i][j]):
                    if v: out[k] += x[i] * y[j] * v
        return out
    for i in idx:
        for j in idx:
            lhs = [sum(D[k][l] * C[i][j][l] for l in range(N)) for k in range(N)]
            rhs = [a + b for a, b in zip(prod(cols[i], unit(j)), prod(unit(i), cols[j]))]
            if lhs != rhs: return False
    return True

def der_upper_modp(C, idx, p):
    """nullity mod p of the linear system 'D is a derivation of the subalgebra on idx' (D: idx -> idx)."""
    guard()
    n = len(idx); pos = {g: a for a, g in enumerate(idx)}
    eqs = []
    for a, i in enumerate(idx):
        for b, j in enumerate(idx):
            if b < a: continue
            for c, k in enumerate(idx):
                row = [0] * (n * n)
                for l in idx:
                    v = C[i][j][l]
                    if v: row[c * n + pos[l]] += v           # (D C_ij)_k
                for l in idx:
                    v = C[l][j][k]
                    if v: row[pos[l] * n + a] -= v           # D[l,i] C[l][j]_k
                    v = C[i][l][k]
                    if v: row[pos[l] * n + b] -= v           # D[l,j] C[i][l]_k
                if any(row): eqs.append(row)
    return n * n - rank_modp(eqs, p)

def inner_derivations(C, idx):
    """[L_a, L_b] (scaled by 4) restricted to coords idx, a < b; returns a maximal independent list (int)."""
    guard()
    L = {}
    for a in idx:
        L[a] = [[C[a][j][k] if (j in idx) else 0 for j in range(N)] for k in range(N)]
    basis, ech = [], []   # ech: list of (pivot, Fraction row) reduced
    for a, b in itertools.combinations(idx, 2):
        AB, BA = matmul(L[a], L[b]), matmul(L[b], L[a])
        D = [[AB[i][j] - BA[i][j] for j in range(N)] for i in range(N)]
        flat = [Fraction(x) for row in D for x in row]
        for pv, er in ech:
            if flat[pv] != 0:
                f = flat[pv]; flat = [x - f * y for x, y in zip(flat, er)]
        pv = next((t for t, x in enumerate(flat) if x != 0), None)
        if pv is None: continue
        inv = 1 / flat[pv]; flat = [x * inv for x in flat]
        ech = [(q, [x - r[pv] * y for x, y in zip(r, flat)]) for q, r in ech]
        ech.append((pv, flat)); basis.append(D)
    return basis

# ---------------- f4 coordinate machinery ----------------
class F4:
    def __init__(self, T):
        guard()
        self.T = T
        self.C = ctable(T)
        self.idx = list(range(N))
        self.basis = inner_derivations(self.C, self.idx)       # list of int N x N
        self.dim = len(self.basis)
        flat = [[x for row in D for x in row] for D in self.basis]
        _, piv = rref(flat, N * N)
        self.piv = piv                                            # dim pivot positions
        Mp = [[Fraction(flat[a][q]) for a in range(self.dim)] for q in piv]   # (q, a)
        aug = [row + unit(i, self.dim) for i, row in enumerate(Mp)]
        R, pv = rref(aug, 2 * self.dim)
        assert pv[:self.dim] == list(range(self.dim))
        self.Minv = [r[self.dim:] for r in R]                    # coeffs = Minv @ X[piv]

    def mat(self, c):
        return [[sum(c[a] * self.basis[a][i][j] for a in range(self.dim) if c[a]) for j in range(N)] for i in range(N)]

    def coords(self, X):
        xp = [X[q // N][q % N] for q in self.piv]
        return [sum(m * x for m, x in zip(row, xp) if x) for row in self.Minv]

    # subalgebras as lists of coefficient vectors
    def stab_vecs(self, vecs, within=None):
        guard()
        if within is None:
            within, W = [unit(a, self.dim) for a in range(self.dim)], self.basis
        else:
            W = [self.mat(w) for w in within]
        rows = []
        for s in vecs:
            s = intvec(s)
            for k in range(N):
                rows.append([sum(Wm[k][l] * s[l] for l in range(N) if s[l]) for Wm in W])
        return self._lift(nullspace(rows, len(within)), within)

    def setstab(self, Wset, within=None):
        guard()
        if within is None:
            within, W = [unit(a, self.dim) for a in range(self.dim)], self.basis
        else:
            W = [self.mat(w) for w in within]
        Ws = set(Wset)
        rows = [[Wm[k][w] for Wm in W] for k in range(N) if k not in Ws for w in Wset]
        return self._lift(nullspace(rows, len(within)), within)

    def _lift(self, ns, within):
        return [[sum(l * w[a] for l, w in zip(v, within)) for a in range(self.dim)] for v in ns]

    def intersect(self, h1, h2):
        # x = sum s_i h1_i = sum t_j h2_j
        rows = [[h1[i][a] for i in range(len(h1))] + [-h2[j][a] for j in range(len(h2))] for a in range(self.dim)]
        ns = nullspace(rows, len(h1) + len(h2))
        return [[sum(v[i] * h1[i][a] for i in range(len(h1))) for a in range(self.dim)] for v in ns]

    def fix(self, h):
        guard()
        rows = []
        for c in h:
            rows += self.mat(c)
        return nullspace(rows, N)

    def closure(self, h):
        guard()
        F = self.fix(h)
        return self.stab_vecs(F) if F else [unit(a, self.dim) for a in range(self.dim)]

    def same_space(self, h1, h2):
        return len(h1) == len(h2) == rank(h1 + h2, self.dim)

    def invariants(self, h, seed=SEED):
        guard()
        import numpy as np
        d = len(h)
        if d == 0:
            return dict(dim=0, rank=0, centre=0, derived=0, subalg=True)
        h = [intvec(c) for c in h]                     # rescaling basis vectors does not change any invariant
        Ms = [np.array(self.mat(c), dtype=object) for c in h]
        BR = [[None] * d for _ in range(d)]
        zero = [Fraction(0)] * self.dim
        for i in range(d):
            BR[i][i] = zero
            for j in range(i + 1, d):
                X = (Ms[i].dot(Ms[j]) - Ms[j].dot(Ms[i])).tolist()
                c = self.coords(X)
                BR[i][j] = c; BR[j][i] = [-x for x in c]
        allbr = [BR[i][j] for i in range(d) for j in range(i + 1, d)]
        subalg = rank(h + allbr, self.dim) == d
        derived = rank(allbr, self.dim) if allbr else 0
        rows = [[BR[i][j][a] for i in range(d)] for j in range(d) for a in range(self.dim)]
        centre = len(nullspace(rows, d))
        rng = random.Random(seed)
        rk = None
        for _ in range(3):
            r = [rng.randint(-9, 9) for _ in range(d)]
            colsv = [[sum(r[i] * BR[i][j][a] for i in range(d) if r[i]) for a in range(self.dim)] for j in range(d)]
            rows2 = [[colsv[j][a] for j in range(d)] for a in range(self.dim)]
            cz = len(nullspace(rows2, d))
            rk = cz if rk is None else min(rk, cz)
        return dict(dim=d, rank=rk, centre=centre, derived=derived, subalg=subalg)

SIMPLE = []
for n in range(1, 9): SIMPLE.append((f'A{n}', n, n * (n + 2)))
for n in range(2, 9): SIMPLE.append((f'B{n}', n, n * (2 * n + 1)))
for n in range(3, 9): SIMPLE.append((f'C{n}', n, n * (2 * n + 1)))
for n in range(4, 9): SIMPLE.append((f'D{n}', n, n * (2 * n - 1)))
SIMPLE += [('G2', 2, 14), ('F4', 4, 52), ('E6', 6, 78), ('E7', 7, 133), ('E8', 8, 248)]

def type_candidates(inv):
    """compact reductive: semisimple part of rank (rank - centre), dim derived (requires dim = centre + derived)."""
    if inv['dim'] != inv['centre'] + inv['derived']:
        return ['NOT-REDUCTIVE-SPLIT']
    r, dd = inv['rank'] - inv['centre'], inv['derived']
    out = []
    def rec(start, r_left, d_left, acc):
        if r_left == 0:
            if d_left == 0: out.append('+'.join(acc) if acc else '0')
            return
        for t in range(start, len(SIMPLE)):
            nm, rr, dm = SIMPLE[t]
            if rr <= r_left and dm <= d_left:
                rec(t, r_left - rr, d_left - dm, acc + [nm])
    rec(0, r, dd, [])
    return [f"{x}+u1^{inv['centre']}" if inv['centre'] else x for x in out]

def sm_type(inv):
    return (inv['dim'], inv['rank'], inv['centre'], inv['derived']) == (12, 4, 1, 11)

# ---------------- configurations ----------------
def E(i):
    return unit(i)

def x_idx(units):
    """h2(K) on diagonal idx {2,3} (0-based 1,2): E2, E3 and the 'a' entry restricted to K."""
    return sorted([1, 2] + [3 + u for u in units])

def family_B(F):
    order = ['R', 'C', 'H', 'O']
    fam = []
    for i, k1 in enumerate(order):
        for k2 in order[i:]:
            fam.append((f'X=h2({k1}),B=h3({k2})', ('X', k1), ('B', k2)))
    for k in order:
        fam.append((f'B=h3({k}) only', None, ('B', k)))
    for k in order:
        fam.append((f'X=h2({k}) only', ('X', k), None))
    out = []
    for name, x, b in fam:
        h = [unit(a, F.dim) for a in range(F.dim)]
        if x: h = F.intersect(h, F.setstab(x_idx(KUNITS[x[1]])))
        if b: h = F.intersect(h, F.setstab(sub_idx(KUNITS[b[1]])))
        out.append((name, h))
    return out

def idempotents():
    """E1,E2,E3 and P_ij(s e_k) = (E_i + E_j + F_ij(s e_k))/2, scaled by 2 (stabilisers are scale-free)."""
    out = [('E1', E(0)), ('E2', E(1)), ('E3', E(2))]
    for nm, (base, (r, c)) in OFF.items():
        for k in range(8):
            for s in (1, -1):
                v = [0] * N; v[r] = 1; v[c] = 1; v[base + k] = s
                out.append((f'P{r+1}{c+1}({"+" if s > 0 else "-"}e{k})', v))
    return out

def is_idempotent2(v, C):
    """v = 2P: check P∘P = P  <=>  (2P)∘(2P) = 2(2P)  <=>  jprod2(v,v) = 4 v ... with jprod2 = 2∘: 2(v∘v) = 4v/... """
    # v∘v = 2v  (since v = 2P, v∘v = 4P = 2v); jprod2 gives 2 v∘v = 4 v
    out = [0] * N
    for i in range(N):
        if not v[i]: continue
        for j in range(N):
            if not v[j]: continue
            for k, x in enumerate(C[i][j]):
                if x: out[k] += v[i] * v[j] * x
    return out == [4 * x for x in v]

# ---------------- J rival ----------------
def lr_matrix(u, T, side):
    M = [[0] * 8 for _ in range(8)]
    for j in range(8):
        x = unit(j, 8); uu = unit(u, 8)
        y = omul(uu, x, T) if side == 'L' else omul(x, uu, T)
        for i in range(8): M[i][j] = y[i]
    return M

def j_commutant(F, s1, T, variant):
    guard()
    sides = {'LL': ('L', 'L'), 'RR': ('R', 'R'), 'LR': ('L', 'R'), 'RL': ('R', 'L')}[variant]
    J = [[0] * N for _ in range(N)]
    for blk, sd in zip((11, 19), sides):
        M = lr_matrix(1, T, sd)
        for i in range(8):
            for j in range(8): J[blk + i][blk + j] = M[i][j]
    W = [F.mat(w) for w in s1]
    rows = []
    for i in range(N):
        for j in range(N):
            rows.append([sum(Wm[i][k] * J[k][j] - J[i][k] * Wm[k][j] for k in range(N)) for Wm in W])
    return F._lift(nullspace(rows, len(s1)), s1)

# ---------------- modes ----------------
def jdump(obj, name):
    (OUTDIR / name).write_text(json.dumps(obj, indent=1, default=str) + '\n')

def run_planted():
    guard_banner()
    t0 = time.time(); res = {}
    T = omul_table()
    res['P1_table_ok'] = table_ok(T)
    F = F4(T)
    upp = [der_upper_modp(F.C, F.idx, p) for p in (2147483647, 1000000007)]
    res['P2_der_lower'] = F.dim; res['P2_der_upper_modp'] = upp
    res['P2_all_basis_are_derivations'] = all(is_der(D, F.C, F.idx) for D in F.basis)
    res['P2'] = F.dim == 52 and min(upp) == 52 and res['P2_all_basis_are_derivations']
    s1 = F.stab_vecs([E(0)]); res['P3_dim_stabE1'] = len(s1)
    s123 = F.stab_vecs([E(0), E(1), E(2)]); res['P4_dim_stabE123'] = len(s123)
    sb = F.setstab(sub_idx(KUNITS['C'])); res['P5_dim_setstab_h3C'] = len(sb)
    g = F.intersect(s1, sb); inv = F.invariants(g); res['P6_gsm_inv'] = inv
    res['P6_types'] = type_candidates(inv); res['P6'] = sm_type(inv) and inv['subalg']
    bs = F.intersect(F.setstab(x_idx(KUNITS['C'])), sb); res['P7_same'] = F.same_space(bs, g)
    p8 = {}
    for k in ('R', 'C', 'H'):
        idx = sub_idx(KUNITS[k])
        assert all(F.C[i][j][t] == 0 for i in idx for j in idx for t in range(N) if t not in idx), "subalgebra not closed"
        lo = len(inner_derivations(F.C, idx)); up = der_upper_modp(F.C, idx, 2147483647)
        p8[k] = (lo, up)
    res['P8'] = p8
    # valid alternatives
    gE2 = F.intersect(s1, F.setstab(sub_idx(KUNITS_E2['C'])))
    i2 = F.invariants(gE2)
    res['V1_inv_u=e2'] = i2
    c1, c2 = F.closure(g), F.closure(gE2)
    res['V1_closure_dims'] = (len(c1), len(c2))
    res['V1_accepted'] = (i2['dim'], i2['rank'], i2['centre'], i2['derived']) == (inv['dim'], inv['rank'], inv['centre'], inv['derived']) and len(c1) == len(c2)
    s23 = F.stab_vecs([[0, 1, 1] + [0] * 24]); res['V2_accepted'] = F.same_space(s23, s1)
    res['V3_accepted'] = F.invariants(g, seed=SEED + 1)['rank'] == inv['rank']
    ok = (res['P1_table_ok'] and res['P2'] and res['P3_dim_stabE1'] == 36 and res['P4_dim_stabE123'] == 28
          and res['P5_dim_setstab_h3C'] == 16 and res['P6'] and res['P7_same']
          and p8 == {'R': (3, 3), 'C': (8, 8), 'H': (21, 21)}
          and res['V1_accepted'] and res['V2_accepted'] and res['V3_accepted'])
    res['PLANTED_ALL_OK'] = ok; res['seconds'] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1, default=str)); jdump(res, 'planted_out.json')
    return ok

def run_broken():
    guard_banner()
    res = {}
    res['B1_broken_table_rejected'] = not table_ok(omul_table(broken=True))
    T = omul_table(); F = F4(T)
    s1 = F.stab_vecs([E(0)])
    res['B2_claim_dimstabE1_52_rejected'] = len(s1) != 52
    D = [[0] * N for _ in range(N)]; D[0][0] = 1
    res['B3_E00_not_derivation_rejected'] = not is_der(D, F.C, F.idx)
    res['BROKEN_ALL_REJECTED'] = all(res.values())
    print(json.dumps(res, indent=1)); jdump(res, 'broken_out.json')
    return res['BROKEN_ALL_REJECTED']

def run_live():
    guard_banner()
    t0 = time.time(); res = {'run_id': 'JORD1-2026-10-28-r1'}
    T = omul_table(); F = F4(T)
    s1 = F.stab_vecs([E(0)])
    g = F.intersect(s1, F.setstab(sub_idx(KUNITS['C'])))
    inv = F.invariants(g)
    Fx = F.fix(g); cl = F.closure(g); icl = F.invariants(cl)
    res['tierA'] = dict(gsm=inv, fix_dim=len(Fx), fix_basis=[intvec(v) for v in Fx], closure=icl,
                        closure_types=type_candidates(icl), closure_equals_stabE1=F.same_space(cl, s1))
    if len(cl) == len(g): vA = 'POSITIVITY-CLOSED'
    elif len(cl) > len(g) and rank(g + cl, F.dim) == len(cl): vA = 'NOT-POSITIVITY-CLOSED'
    else: vA = 'UNCLASSIFIED'
    res['tierA']['verdict'] = vA
    # tier B
    rows = []
    for name, h in family_B(F):
        iv = F.invariants(h); c = F.closure(h)
        rows.append(dict(config=name, **iv, closure_dim=len(c), closed=len(c) == len(h),
                         sm_type=sm_type(iv), types=type_candidates(iv)))
    res['tierB'] = rows
    k = sum(r['sm_type'] for r in rows)
    res['tierB_label'] = 'CHOICE-UNIQUE' if k == 1 else ('CHOICE-NONE' if k == 0 else f'CHOICE-AMONG-{k}')
    res['null_frac_closed'] = f"{sum(r['closed'] for r in rows)}/{len(rows)}"
    res['null_frac_smtype'] = f"{k}/{len(rows)}"
    # family F_A
    ids = idempotents()
    res['FA_all_idempotent'] = all(is_idempotent2(v, F.C) for _, v in ids)
    dims, smhits = {}, []
    for r_ in (1, 2):
        for comb in itertools.combinations(ids, r_):
            h = F.stab_vecs([v for _, v in comb])
            dims[len(h)] = dims.get(len(h), 0) + 1
            if len(h) == 12 and sm_type(F.invariants(h)):
                smhits.append([n for n, _ in comb])
    res['FA_configs'] = sum(dims.values()); res['FA_stab_dim_hist'] = dict(sorted(dims.items()))
    res['FA_smtype_hits'] = smhits
    # rival J
    jr = {}
    for var in ('LL', 'RR', 'LR', 'RL'):
        h = j_commutant(F, s1, T, var)
        iv = F.invariants(h)
        jr[var] = dict(**iv, types=type_candidates(iv), equals_gsm=F.same_space(h, g))
    res['rival_J'] = jr
    consistent = not (vA == 'NOT-POSITIVITY-CLOSED' and smhits) and res['FA_all_idempotent'] and k >= 1
    res['consistent'] = consistent
    res['VERDICT'] = (f"{vA} / {res['tierB_label']}" + (' / NO-GO' if vA == 'NOT-POSITIVITY-CLOSED' else '')) if consistent else 'ILL-DEFINED'
    # Lean data: integer basis of g_sm, a witness W in closure \ setstab(B)
    G = [F.mat([x for x in intvec(c)]) for c in g]
    B = set(sub_idx(KUNITS['C']))
    W = None
    for c in cl:
        M = F.mat(intvec(c))
        if any(M[kk][w] != 0 for kk in range(N) if kk not in B for w in B):
            W = M; break
    res['lean_data'] = dict(G=G, W=W)
    res['seconds'] = round(time.time() - t0, 1)
    out = {k_: v for k_, v in res.items() if k_ != 'lean_data'}
    print(json.dumps(out, indent=1, default=str)); jdump(res, 'live_out.json')
    print('VERDICT:', res['VERDICT'])
    return res

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    guard()
    {'planted': run_planted, 'broken': run_broken, 'live': run_live}.get(mode, lambda: sys.exit('mode?'))()
