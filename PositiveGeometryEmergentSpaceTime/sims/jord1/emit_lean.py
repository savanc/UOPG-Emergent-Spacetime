"""JORD-1 Lean data emitter (data only; no scoring, no verdicts).
Independent re-implementation of the Fano octonion table and the sparse h3(O) product 2X∘Y = XY+YX
(the Lean file re-derives the same table from the Fano lines and checks it by kernel computation).
Reads G (12 elements of g_sm) and W (closure element outside setstab h3(C)) from live_out.json,
re-checks them here, and builds the row-selection certificate d·W = Cm·Rsel (rows of the G_k)."""
import json, sys
from fractions import Fraction
from math import lcm
N = 27
LINES = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]
def omu(a, b):
    if a == 0: return (1, b)
    if b == 0: return (1, a)
    if a == b: return (-1, 0)
    for (x, y, z) in LINES:
        for (p, q, r) in ((x, y, z), (y, z, x), (z, x, y)):
            if (a, b) == (p, q): return (1, r)
            if (a, b) == (q, p): return (-1, r)
    raise ValueError
BLK = [(3, 1, 2), (11, 2, 0), (19, 0, 1)]
def basis(i):
    if i < 3: return [(i, i, 0, 1)]
    for base, r, c in BLK:
        if base <= i < base + 8:
            u = i - base
            return [(r, c, u, 1), (c, r, u, 1 if u == 0 else -1)]
def mprod(X, Y):
    return [(r1, c2, omu(u1, u2)[1], omu(u1, u2)[0] * s1 * s2) for (r1, c1, u1, s1) in X for (r2, c2, u2, s2) in Y if c1 == r2]
def coord(P, l):
    if l < 3: return sum(s for (r, c, u, s) in P if r == l and c == l and u == 0)
    for base, r0, c0 in BLK:
        if base <= l < base + 8:
            return sum(s for (r, c, u, s) in P if (r, c, u) == (r0, c0, l - base))
def jp(i, j):
    P = mprod(basis(i), basis(j)) + mprod(basis(j), basis(i))
    return [coord(P, l) for l in range(N)]
T1 = [[jp(i, j) for j in range(N)] for i in range(N)]
sp = lambda v: [(l, x) for l, x in enumerate(v) if x]
T1s = [[sp(T1[i][j]) for j in range(N)] for i in range(N)]
T2s = [[sp([T1[l][j][k] for l in range(N)]) for k in range(N)] for j in range(N)]
assert all(T1[i][j] == T1[j][i] for i in range(N) for j in range(N))
def isder(D):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                lhs = sum(T1[i][j][l] * D[k][l] for l in range(N))
                rhs = sum(D[l][i] * T1[l][j][k] + D[l][j] * T1[i][l][k] for l in range(N))
                if lhs != rhs: return False
    return True
d = json.load(open('sims/jord1/live_out.json'))['lean_data']
G, W = d['G'], d['W']
B = [0, 1, 2, 3, 4, 11, 12, 19, 20]
assert len(G) == 12 and all(isder(g) for g in G) and isder(W)
assert all(g[k][0] == 0 for g in G for k in range(N))
assert all(g[k][w] == 0 for g in G for k in range(N) if k not in B for w in B)
bad = [(k, w) for k in range(N) if k not in B for w in B if W[k][w] != 0]
assert bad
# row selection: greedy row basis of stacked G rows
sel, basisrows = [], []
def rank(rows):
    M = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(N):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
for k in range(12):
    for rho in range(N):
        row = G[k][rho]
        if any(row) and rank(basisrows + [row]) > len(basisrows):
            basisrows.append(row); sel.append((k, rho))
R = len(basisrows); print('rank of stacked G rows:', R)
# solve W[i] = sum_r c[i][r] basisrows[r]  (exact)
def solve(target):
    # least-squares-free exact: augment and rref on transpose system
    A = [[Fraction(basisrows[r][j]) for r in range(R)] + [Fraction(target[j])] for j in range(N)]
    piv, row = [], 0
    for c in range(R):
        p = next((i for i in range(row, N) if A[i][c]), None)
        assert p is not None
        A[row], A[p] = A[p], A[row]
        inv = 1 / A[row][c]; A[row] = [x * inv for x in A[row]]
        for i in range(N):
            if i != row and A[i][c]:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[row])]
        piv.append(c); row += 1
    assert all(A[i][R] == 0 for i in range(R, N)), 'W row not in span'
    return [A[r][R] for r in range(R)]
Cf = [solve(W[i]) for i in range(N)]
dd = 1
for row in Cf:
    for x in row: dd = lcm(dd, x.denominator)
Cm = [[int(x * dd) for x in row] for row in Cf]
for i in range(N):
    for j in range(N):
        assert sum(Cm[i][r] * basisrows[r][j] for r in range(R)) == dd * W[i][j]
print('d =', dd, 'max|C| =', max(abs(x) for r in Cm for x in r), 'W witness entry', bad[0], W[bad[0][0]][bad[0][1]])
tp = lambda M: [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]
L = lambda M: '[' + ',\n  '.join('[' + ', '.join(str(x) for x in r) + ']' for r in M) + ']'
Ls = lambda s: '[' + ', '.join(f'({l}, {x})' for l, x in s) + ']'
LL = lambda S: '[' + ',\n  '.join('[' + ', '.join(Ls(s) for s in row) + ']' for row in S) + ']'
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[2] / 'scripts'))
from lean_wrap import wrap_text  # noqa: E402
LIC = ('/-\nCopyright (c) 2026 Savan Chhaniyara. All rights reserved.\n'
       'Released under MIT license as described in the file LICENSE.\nAuthors: Savan Chhaniyara\n-/\n')
SRC = ('JORD-1 (prereg/JORD-1-positivity-closure-2026-10-28.md, run JORD1-2026-10-28-r1). Generated\n'
       'by sims/jord1/emit_lean.py from sims/jord1/live_out.json (data only). No `sorry`, no\n'
       '`native_decide`.')
DOC_TABLE = (LIC + '/-!\n# JORD-1 product table\n\n## i. Overview\n\n' + SRC + '\n\n'
             'Sparse structure constants of the Jordan product on the 27-dimensional algebra `h3(O)`.\n\n'
             '## ii. Key results\n\nData only; the checks live in `PositiveGeometryEmergentSpaceTime.Jord1.Alg`.\n\n'
             '## iii. Table of contents\n\n- `T1s`: entries of `2 b_i∘b_j`.\n'
             '- `T2s`: the same constants indexed for the transpose check.\n\n'
             '## iv. References\n\n- prereg/JORD-1-positivity-closure-2026-10-28.md\n-/\n')
DOC_DATA = (LIC + '/-!\n# JORD-1 data\n\n## i. Overview\n\n' + SRC + '\n\n'
            'Integer matrices from the live run: a basis of 12 generators of `g_sm`, the derivation `W`,\n'
            'the selected rows and the integer certificate used by `PositiveGeometryEmergentSpaceTime.Jord1.NoGo`.\n\n'
            '## ii. Key results\n\nData only; the kernel checks live in `PositiveGeometryEmergentSpaceTime.Jord1.Gens` and\n'
            '`PositiveGeometryEmergentSpaceTime.Jord1.NoGo`.\n\n'
            '## iii. Table of contents\n\n- `Gs`, `GsC`: generators and their transposes.\n'
            '- `Wr`, `Wc`: the derivation `W` and its transpose.\n'
            '- `selIdx`, `Rsel`, `RselC`, `Cm`, `dW`, `nSel`: certificate data.\n'
            '- `wk`, `ww`: the witness entry.\n\n'
            '## iv. References\n\n- prereg/JORD-1-positivity-closure-2026-10-28.md\n-/\n')
open('lean/PositiveGeometryEmergentSpaceTime/Jord1/Table.lean', 'w').write(wrap_text(DOC_TABLE + f'''namespace PositiveGeometryEmergentSpaceTime.Jord1

/-- Sparse structure constants of `2 X∘Y = XY + YX` on `h3(O)`: entry `[i][j]` lists `(l, c)` with
`2 b_i∘b_j = Σ c b_l`. Checked against the Fano-defined product in `PositiveGeometryEmergentSpaceTime.Jord1.Alg`
(`T1s_ok`). -/
def T1s : List (List (List (Nat × Int))) :=
 {LL(T1s)}

/-- `T2s[j][k]` lists `(l, c)` with `c = T1[l][j][k]` (checked in `T2s_ok`). -/
def T2s : List (List (List (Nat × Int))) :=
 {LL(T2s)}

end PositiveGeometryEmergentSpaceTime.Jord1
'''))
open('lean/PositiveGeometryEmergentSpaceTime/Jord1/Data.lean', 'w').write(wrap_text(DOC_DATA + 'namespace PositiveGeometryEmergentSpaceTime.Jord1\n\n' +
  '/-- Rows of 12 elements of `g_sm` (integer basis from the live run). -/\ndef Gs : List (List (List Int)) :=\n [' + ',\n '.join(L(g) for g in G) + ']\n\n' +
  '/-- Columns (transposes) of `Gs`. -/\ndef GsC : List (List (List Int)) :=\n [' + ',\n '.join(L(tp(g)) for g in G) + ']\n\n' +
  f'/-- A derivation in the closure of `g_sm` that does not preserve `h3(C)`. -/\ndef Wr : List (List Int) :=\n {L(W)}\n\n/-- Integer matrix data `Wc` (transpose of `Wr`). -/\ndef Wc : List (List Int) :=\n {L(tp(W))}\n\n' +
  f'/-- Selected rows `(k, ρ)`: row `r` of `Rsel` is row `ρ` of `Gs[k]`. -/\ndef selIdx : List (Nat × Nat) := [' + ', '.join(f'({k}, {r})' for k, r in sel) + ']\n\n' +
  f'def Rsel : List (List Int) :=\n {L(basisrows)}\n\n/-- Transpose of `Rsel`. -/\ndef RselC : List (List Int) :=\n {L(tp(basisrows))}\n\n' +
  f'/-- Certificate `d • W = Cm * Rsel`. -/\ndef Cm : List (List Int) :=\n {L(Cm)}\n\n/-- Scalar `dW` used in the certificate `Cm * Rsel = dW • W`. -/\ndef dW : Int := {dd}\n\n' +
  f'def nSel : Nat := {R}\n\n/-- Witness entry `W[{bad[0][0]}][{bad[0][1]}] ≠ 0` with `{bad[0][0]} ∉ h3(C)`, `{bad[0][1]} ∈ h3(C)`. -/\ndef wk : Nat := {bad[0][0]}\n/-- Column index of the witness entry. -/\ndef ww : Nat := {bad[0][1]}\n\nend PositiveGeometryEmergentSpaceTime.Jord1\n'))
print('sizes', [len(open(f'lean/PositiveGeometryEmergentSpaceTime/Jord1/{f}.lean').read()) for f in ('Table', 'Data')])
