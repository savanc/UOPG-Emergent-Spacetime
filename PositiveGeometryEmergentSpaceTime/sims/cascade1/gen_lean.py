#!/usr/bin/env python3
"""Generates lean/PositiveGeometryEmergentSpaceTime/Cascade1.lean statements from the locked checker's kinematics (Kin.c) and the r1 live
relations (cascade1_live.json).  Every linear identity used by `linarith` / `ring` in Lean is pre-checked here
with sympy.  Certificates (M, K, P, Q, d) via sims/leancert1 (exact rref; verified by kernel decide in Lean)."""
import json, sys
from pathlib import Path
import sympy as sp
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / 'leancert1'))
import cascade1_checker as C
import leancert1_checker as L

live = json.loads((HERE / 'cascade1_live.json').read_text())
kin = C.Kin(5, 'EM')
ch = kin.ch  # (1,3),(1,4),(2,4),(2,5),(3,5)
X, mu, m = kin.X, kin.mu, kin.m
y = {P: X[P] - mu[P] for P in ch}
R = [sp.sympify(r) for r in live['cells']['EM-n5']['S3']['relations']]
theta = kin.theta

def lean(e):
    s = str(sp.expand(e)).replace('**', '^')
    return s
def nm(P): return f'{P[0]}{P[1]}'
def rot(P, k): return C.rot(P, k, 5)

# role chords at k = 0 (locus Z_1: c13 = c14 = 0)
ROLES = {'a': (1, 3), 'd': (1, 4), 'b': (2, 4), 'f': (2, 5), 'e': (3, 5)}
loci = kin.zero_loci()
assert len(loci) == 5
Xargs = ' '.join(f'X{nm(P)}' for P in ch)
muargs = ' '.join(f'μ{nm(P)}' for P in ch)
margs = ' '.join(f'm{i}' for i in range(1, 6))
def tolean(e):
    s = lean(e)
    for P in ch:
        s = s.replace(f'mu{nm(P)}', f'μ{nm(P)}')
    return s
def Y(P): return f'(X{nm(P)} - μ{nm(P)})'
A5canon = 'A5 ' + ' '.join(Y(P) for P in ch)
Rhyps = ' '.join(f'(hR{j} : {tolean(r)} = 0)' for j, r in enumerate(R))
nz = ' '.join(f'(hy{nm(P)} : {Y(P)} ≠ 0)' for P in ch)
out = []
alphabeta = []
for k in range(5):
    rr = {r: rot(P, k) for r, P in ROLES.items()}
    cpairs = [rot((1, 3), k), rot((1, 4), k)]
    cs = [kin.c(*cp) for cp in cpairs]
    # locus identification
    assert any(set(map(tuple, pr)) == set(cpairs) for _, pr, _ in loci), (k, cpairs)
    yr = {r: y[P] for r, P in rr.items()}
    # IF: on R and cs = 0: d = a + b, f = -a
    sol = sp.solve(R + cs, [mu[P] for P in ch] + [X[rr['d']], X[rr['f']]], dict=True)[0]
    assert sp.expand((yr['d'] - yr['a'] - yr['b']).subs(sol)) == 0 and sp.expand((yr['f'] + yr['a']).subs(sol)) == 0
    # ONLY-IF parametrisation: alpha, beta such that X_a = a + mu_a, ..., X_d = a+b+alpha+mu_d, X_f = beta - a + mu_f
    a_, b_, e_, al, be = sp.symbols('a b e al be')
    Xsub = {X[rr['a']]: a_ + mu[rr['a']], X[rr['b']]: b_ + mu[rr['b']], X[rr['e']]: e_ + mu[rr['e']],
            X[rr['d']]: a_ + b_ + al + mu[rr['d']], X[rr['f']]: be - a_ + mu[rr['f']]}
    s2 = sp.solve([c.subs(Xsub) for c in cs], [al, be], dict=True)[0]
    alpha, beta = sp.expand(s2[al]), sp.expand(s2[be])
    assert all(sp.expand(c.subs(Xsub).subs({al: alpha, be: beta})) == 0 for c in cs)
    alphabeta += [alpha, beta]
    roleorder = ['a', 'd', 'b', 'f', 'e']
    A5roles = 'A5 ' + ' '.join(Y(rr[r]) for r in roleorder)
    chyps = ' '.join(f'(hc{j} : {tolean(c)} = 0)' for j, c in enumerate(cs))
    nza = ' '.join(f'hy{nm(rr[r])}' for r in roleorder)
    out.append(f"""/-- Z_{k+1} (c{nm(cpairs[0])} = c{nm(cpairs[1])} = 0 with physical masses): the S3 relations R give the hidden zero. -/
theorem zero5_of_rel_{k+1} ({Xargs} {muargs} {margs} : ℚ) {Rhyps}
    {chyps} {nz} :
    {A5canon} = 0 := by
  rw [show {A5canon} = {A5roles} by unfold A5; ring]
  exact core_zero _ _ _ _ _ {nza} (by linarith) (by linarith)
""")
    # splits: eq 3.3 on c_{rot14} = 0: y_b = y_d + y_f ; eq 3.5 on c_{rot13}=0: y_d = y_a + y_b
    for tag, cp, rel, fac in [('33', rot((1, 4), k), (yr['b'] - yr['d'] - yr['f']), ('a', 'f', 'd', 'e')),
                              ('35', rot((1, 3), k), (yr['d'] - yr['a'] - yr['b']), ('a', 'f', 'b', 'e'))]:
        c = kin.c(*cp)
        solx = sp.solve(R + [c], [mu[P] for P in ch] + [X[rr['b'] if tag == '33' else rr['d']]], dict=True)[0]
        assert sp.expand(rel.subs(solx)) == 0
        # template group check against checker SPLIT_TEMPLATES
        F = f'(1 / {Y(rr[fac[0]])} + 1 / {Y(rr[fac[1]])}) * (1 / {Y(rr[fac[2]])} + 1 / {Y(rr[fac[3]])})'
        out.append(f"""/-- Held-out split eq. 3.{tag[1]} (rotation {k}): on c{nm(cp)} = 0 (physical masses) with R, A5 factorises. -/
theorem split5_of_rel_{tag}_{k+1} ({Xargs} {muargs} {margs} : ℚ) {Rhyps}
    (hc : {tolean(c)} = 0) {nz} :
    {A5canon} = {F} := by
  rw [show {A5canon} = {A5roles} by unfold A5; ring]
  exact core_split{tag} _ _ _ _ _ {nza} (by linarith)
""")
    # only-if per locus
    Xvals = {}
    for P in ch:
        e = Xsub[X[P]].subs({al: sp.Symbol('ALPHA'), be: sp.Symbol('BETA')})
        Xvals[P] = e
    def lv(e):
        s = tolean(e).replace('ALPHA', f'({tolean(alpha)})').replace('BETA', f'({tolean(beta)})')
        return f'({s})'
    hyp = f"∀ {Xargs} : ℚ, {chyps.replace('(hc0 : ', '').replace(') (hc1 : ', ' → ').replace(' = 0)', ' = 0', 1)}"
    out.append(f"""/-- ONLY-IF on Z_{k+1}: if A5(X − μ) vanishes on all of Z_{k+1} (off poles), then α_{k+1} = β_{k+1} = 0. -/
theorem zero5_only_if_{k+1} ({muargs} {margs} : ℚ)
    (H : ∀ {Xargs} : ℚ, {tolean(cs[0])} = 0 → {tolean(cs[1])} = 0 →
      {' → '.join(f'{Y(P)} ≠ 0' for P in ch)} → {A5canon} = 0) :
    {tolean(alpha)} = 0 ∧ {tolean(beta)} = 0 := by
  apply core_only_if
  intro a b e ha hb he hd hf
  have h := H {' '.join(lv(Xvals[P]) for P in ch)} (by ring) (by ring)
    {' '.join('(by convert ' + {'a':'ha','b':'hb','e':'he','d':'hd','f':'hf'}[r] + ' using 1; ring)' for r in [next(rk for rk, PP in rr.items() if PP == P) for P in ch])}
  unfold A5 at h ⊢; linear_combination h
""")
# ---- assembled iff ----
Hs = []
for k in range(5):
    cpairs = [rot((1, 3), k), rot((1, 4), k)]; cs = [kin.c(*cp) for cp in cpairs]
    Hs.append(f"(∀ {Xargs} : ℚ, {tolean(cs[0])} = 0 → {tolean(cs[1])} = 0 →\n      {' → '.join(f'{Y(P)} ≠ 0' for P in ch)} → {A5canon} = 0)")
out.append(f"""/-- S3 condition at n = 5: A5(X − μ) vanishes on all five physical zero loci Z_i. -/
def Zeros5 ({muargs} {margs} : ℚ) : Prop :=
  {(' ∧\n  ').join(Hs)}

/-- The five live S3 relations (cascade1_live.json, EM-n5). -/
def Rel5 ({muargs} {margs} : ℚ) : Prop :=
  {' ∧ '.join(f'{tolean(r)} = 0' for r in R)}

/-- n = 5, EM: hidden zeros on all Z_i ⟺ the five relations (both directions PROVED). -/
theorem em_n5_zero_iff ({muargs} {margs} : ℚ) : Zeros5 {muargs} {margs} ↔ Rel5 {muargs} {margs} := by
  unfold Zeros5 Rel5
  constructor
  · rintro ⟨H1, H2, H3, H4, H5⟩
    obtain ⟨a1, b1⟩ := zero5_only_if_1 {muargs} {margs} H1
    obtain ⟨a2, b2⟩ := zero5_only_if_2 {muargs} {margs} H2
    obtain ⟨a3, b3⟩ := zero5_only_if_3 {muargs} {margs} H3
    obtain ⟨a4, b4⟩ := zero5_only_if_4 {muargs} {margs} H4
    obtain ⟨a5, b5⟩ := zero5_only_if_5 {muargs} {margs} H5
    refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> linarith
  · rintro ⟨r0, r1, r2, r3, r4⟩
    refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> intro {Xargs} hc0 hc1 h13 h14 h24 h25 h35
    · exact zero5_of_rel_1 {Xargs} {muargs} {margs} r0 r1 r2 r3 r4 hc0 hc1 h13 h14 h24 h25 h35
    · exact zero5_of_rel_2 {Xargs} {muargs} {margs} r0 r1 r2 r3 r4 hc0 hc1 h13 h14 h24 h25 h35
    · exact zero5_of_rel_3 {Xargs} {muargs} {margs} r0 r1 r2 r3 r4 hc0 hc1 h13 h14 h24 h25 h35
    · exact zero5_of_rel_4 {Xargs} {muargs} {margs} r0 r1 r2 r3 r4 hc0 hc1 h13 h14 h24 h25 h35
    · exact zero5_of_rel_5 {Xargs} {muargs} {margs} r0 r1 r2 r3 r4 hc0 hc1 h13 h14 h24 h25 h35

/-- n = 5, E0 (m_i = 0): hidden zeros force every offset to vanish (Θ_3 = {{0}}, BELOW). -/
theorem e0_n5_zero_iff ({muargs} : ℚ) :
    Zeros5 {muargs} 0 0 0 0 0 ↔ ({' ∧ '.join(f'μ{nm(P)} = 0' for P in ch)}) := by
  rw [em_n5_zero_iff]; unfold Rel5
  constructor
  · rintro ⟨r0, r1, r2, r3, r4⟩; refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> linarith
  · rintro ⟨r0, r1, r2, r3, r4⟩; refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> linarith
""")
# check: the 10 alpha/beta span the same space as R
Ma = sp.Matrix([[sp.expand(e).coeff(t) for t in theta] for e in alphabeta])
MR = sp.Matrix([[sp.expand(r).coeff(t) for t in theta] for r in R])
assert Ma.rank() == 5 and sp.Matrix.vstack(Ma, MR).rank() == 5
print('alpha/beta:', alphabeta, file=sys.stderr)
# certificate for EM n=5 relation space and EM n=4
def cert(Mrows):
    Kc = L.kernel_basis(Mrows); P, Q, d, K = L.split_cert(Mrows, Kc); v = L.verify_cert(Mrows, K, P, Q, d)
    assert all(v.values()), v
    return K, P, Q, d
M5 = [[int(x) for x in row] for row in MR.tolist()]
K5, P5, Q5, d5 = cert(M5)
kin4 = C.Kin(4, 'EM')
R4 = [sp.sympify(r) for r in live['cells']['EM-n4']['S3']['relations']]
M4 = [[int(sp.expand(r).coeff(t)) for t in kin4.theta] for r in R4]
K4, P4, Q4, d4 = cert(M4)
certs = L.emit('em5', M5, K5, P5, Q5, d5) + '\n' + L.emit('em4', M4, K4, P4, Q4, d4)
(HERE / 'cascade1_lean_gen.lean.txt').write_text(certs + '\n\n' + '\n'.join(out))
json.dump({'R5': [str(r) for r in R], 'R4': [str(r) for r in R4], 'theta5': [str(t) for t in theta],
           'theta4': [str(t) for t in kin4.theta], 'alphabeta': [str(e) for e in alphabeta]},
          open(HERE / 'cascade1_lean_gen.json', 'w'), indent=1)
print('ok')
