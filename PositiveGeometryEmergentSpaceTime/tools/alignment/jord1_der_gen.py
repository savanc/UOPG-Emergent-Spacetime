#!/usr/bin/env python3
"""JORD-1 (Phase C): exact dim Der h3(O) = 52 over Q, as a Lean certificate.

Reads the sparse table T1s from lean/PositiveGeometryEmergentSpaceTime/Jord1/Table.lean and builds the 27^3 derivation constraints
on the 729 entries D[a][b] (unknown u = 27a+b). It then
  * greedily picks 52 free unknowns F such that "peeling" (repeatedly use a constraint row with exactly one
    unknown not yet known to vanish) forces all 729 unknowns to 0 when the F-entries are 0 (upper bound);
  * solves the peeling steps for the 52 derivations G_f with F-entries = delta (lower bound), clears
    denominators, checks every constraint exactly;
  * emits lean/PositiveGeometryEmergentSpaceTime/Alignment/Sanity/Jord1Der.lean.
Also reports the rank mod p as an independent cross-check."""
import ast, json, sys
from fractions import Fraction
from math import lcm
from collections import defaultdict
ROOT = __file__.rsplit('/tools/', 1)[0]
s = open(f'{ROOT}/lean/PositiveGeometryEmergentSpaceTime/Jord1/Table.lean').read()
a = s.index(':=', s.index('def T1s')) + 2
body = s[a:s.index('def T2s')]
body = body[:body.index('/--')] if '/--' in body else body
T1 = ast.literal_eval(body[:body.rindex(']') + 1].strip())
bc = [[[0] * 27 for _ in range(27)] for _ in range(27)]
for i in range(27):
    for j in range(27):
        for l, c in T1[i][j]:
            bc[i][j][l] += c
rows = []; RAW = []  # RAW: support as listed by Lean `rowS` (cancelling entries kept)
for i in range(27):
    for j in range(27):
        for k in range(27):
            r = {}
            for l in range(27):
                if bc[i][j][l]: r[27*k+l] = r.get(27*k+l, 0) + bc[i][j][l]
                if bc[l][j][k]: r[27*l+i] = r.get(27*l+i, 0) - bc[l][j][k]
                if bc[i][l][k]: r[27*l+j] = r.get(27*l+j, 0) - bc[i][l][k]
            raw = {27*k+l for l in range(27) if bc[i][j][l]} | {27*l+i for l in range(27) if bc[l][j][k]} | \
                  {27*l+j for l in range(27) if bc[i][l][k]}
            r = {u: c for u, c in r.items() if c}
            if r: rows.append(((i, j, k), r)); RAW.append(raw)
p = 1000003
piv = {}; rk = 0
for _, r in rows:
    v = {u: c % p for u, c in r.items()}
    while v:
        u = min(v)
        if u in piv:
            f = v[u]
            for w, c in piv[u].items(): v[w] = (v.get(w, 0) - f * c) % p
            v = {w: c for w, c in v.items() if c}
        else:
            inv = pow(v[u], p - 2, p); piv[u] = {w: c * inv % p for w, c in v.items()}; rk += 1; break
print('constraint rows', len(rows), 'rank mod p', rk, 'kernel dim', 729 - rk)
occ = defaultdict(list)
for idx in range(len(rows)):
    for u in RAW[idx]: occ[u].append(idx)
def peel(known, new):
    known = set(known) | set(new); steps = []
    cnt = [sum(1 for u in raw if u not in known) for raw in RAW]
    q = [i for i, c in enumerate(cnt) if c == 1]
    while q:
        i = q.pop()
        unk = [u for u in RAW[i] if u not in known]
        if len(unk) != 1 or unk[0] not in rows[i][1]: continue
        u = unk[0]; known.add(u); steps.append((i, u))
        for j in occ[u]:
            cnt[j] -= 1
            if cnt[j] == 1: q.append(j)
    return known, steps
F = []; known, _ = peel(set(), [])
while len(known) < 729:
    best = None
    for u in range(729):
        if u in known: continue
        k2, _ = peel(known, [u])
        if best is None or len(k2) > best[0]: best = (len(k2), u)
    F.append(best[1]); known, _ = peel(known, [best[1]])
known, steps = peel(set(), F)
assert len(known) == 729 and len(F) == 729 - rk == 52
steps = [(rows[i][0], u) for i, u in steps]
rowd = {key: r for key, r in rows}
B = []
for f in F:
    D = {u: Fraction(0) for u in range(729)}; D[f] = Fraction(1)
    for key, u in steps:
        r = rowd[key]; D[u] = Fraction(-sum(c * D[w] for w, c in r.items() if w != u)) / r[u]
    for key, r in rows: assert sum(c * D[w] for w, c in r.items()) == 0
    L = lcm(*[x.denominator for x in D.values()])
    B.append((L, [[int(D[27*a+b] * L) for b in range(27)] for a in range(27)]))
print('F', F); print('denominators', sorted(set(L for L, _ in B)), 'nnz', sum(1 for _, M in B for r in M for x in r if x))
json.dump({'F': F, 'steps': [(list(k), u) for k, u in steps], 'B': B, 'rank_mod_p': rk},
          open(f'{ROOT}/tools/alignment/out/jord1_der_cert.json', 'w'))

def L2(M): return '[' + ', '.join('[' + ', '.join(map(str, r)) + ']' for r in M) + ']'
out = []
out.append(open(f'{ROOT}/tools/alignment/jord1_der_template.lean').read())
data = []
data.append('/-- The 52 free entries (`u = 27a+b` stands for `D a b`). -/\ndef Fr : List ℕ := [' + ', '.join(map(str, F)) + ']\n')
data.append('/-- Peeling steps `(i, j, k, u)`: row `(i, j, k)` forces entry `u`. -/\ndef steps : List (ℕ × ℕ × ℕ × ℕ) := [' +
            ', '.join(f'({k[0]}, {k[1]}, {k[2]}, {u})' for k, u in steps) + ']\n')
data.append('/-- Denominators of the basis derivations. -/\ndef dB : List ℕ := [' + ', '.join(str(L) for L, _ in B) + ']\n')
def SP(M): return '[' + ', '.join(f'({a}, {b}, {M[a][b]})' for a in range(27) for b in range(27) if M[a][b]) + ']'
data.append('/-- Sparse integer entries `(a, b, v)` of the basis derivations (`G_t = dB[t]⁻¹ • B[t]`). -/\ndef Sp : List (List (ℕ × ℕ × ℤ)) :=\n  [' +
            ',\n   '.join(SP(M) for _, M in B) + ']\n')
data.append('''/-- Entry `(a, b)` of a sparse matrix. -/
def spGet (s : List (ℕ × ℕ × ℤ)) : ℕ → ℕ → ℤ := fun a b =>
  match s.find? (fun p => p.1 == a && p.2.1 == b) with
  | some p => p.2.2
  | none => 0

/-- Integer rows of the basis derivations (dense, from `Sp`). -/
def Bm : List (List (List ℤ)) :=
  Sp.map fun s => (List.range 27).map fun a => (List.range 27).map fun b => spGet s a b

/-- Columns of the basis derivations (dense, from `Sp`). -/
def BmC : List (List (List ℤ)) :=
  Sp.map fun s => (List.range 27).map fun a => (List.range 27).map fun b => spGet s b a
''')
tpl = out[0].replace('--DATA--', '\n'.join(data))
ders = ''.join(f'/-- Basis derivation {t} passes `derOK`. -/\ntheorem der_{t} : derOK {t} = true := by decide +kernel\n' for t in range(52))
ders += '/-- All 52 basis checks. -/\ntheorem derOK_all : ∀ t : Fin 52, derOK t = true := by\n  intro t\n  fin_cases t\n' + ''.join(f'  · exact der_{t}\n' for t in range(52))
tpl = tpl.replace('--DERS--', ders)
open(f'{ROOT}/lean/PositiveGeometryEmergentSpaceTime/Alignment/Sanity/Jord1Der.lean', 'w').write(tpl)
