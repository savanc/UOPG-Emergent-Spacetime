"""M2f (d2): generate a Lean certificate that the massive hidden zeros (with (P): internal pion poles at M^2)
force the oo/ee offsets onto the a* line. Evaluation points + rational linear combinations, found here,
re-checked by Lean's `linear_combination` (Lean does not trust this script)."""
import itertools, random
import sympy as sp
exec(open('scripts/m2f_mass_shift.py').read().split('# ---------------------------------------------------------------- (a) n = 4')[0])
CH = chords(6); oe = [(1, 4), (2, 5), (3, 6)]
v = {ch: (sp.Integer(0) if ch in oe else sp.Symbol(f'v{ch[0]}{ch[1]}')) for ch in CH}
V = [v[ch] for ch in CH if ch not in oe]
Z = Xsym(6, 'Z')
def locus(conds):
    eqs_ = [cc(Z, 6, *q) for q in conds]
    for vs in itertools.combinations([Z[ch] for ch in CH if ch not in oe], len(eqs_)):
        sol = sp.solve(eqs_, vs, dict=True)
        if sol and all(sp.simplify(e.subs(sol[0])) == 0 for e in eqs_):
            return sol[0]
    raise ValueError
loci = []
import os
USE = [int(x) for x in os.environ.get('LOCI', '1,2,3,4,5,6').split(',')]
for i in USE:
    L = locus([(i, i + 2), (i, i + 3), (i, i + 4)])
    free = [Z[ch] for ch in CH if Z[ch] not in L]
    loci.append((i, L, free))
random.seed(7)
pts, eqs = [], []
for (i, L, free) in loci:
    for trial in range(12):
        val = {f: sp.Integer(random.randint(-3, 3)) for f in free}
        for ch in oe:
            if Z[ch] in val and val[Z[ch]] == 0: val[Z[ch]] = sp.Integer(random.choice([1, 2, -1]))
        full = {Z[ch]: (L[Z[ch]].subs(val) if Z[ch] in L else val[Z[ch]]) for ch in CH}
        if any(full[Z[ch]] == 0 for ch in oe): continue
        Y = {ch: full[Z[ch]] + v[ch] for ch in CH}
        E = sp.expand(A6N(Y))
        pts.append((i, val, full)); eqs.append(E)
mons = sorted({m for E in eqs for m in sp.Poly(E, *V).monoms()})
def certificate(target):
    cs = sp.symbols(f'k0:{len(eqs)}')
    comb = sp.expand(sum(c * E for c, E in zip(cs, eqs)) - target)
    sol = sp.solve(sp.Poly(comb, *V).coeffs(), cs, dict=True)
    if not sol: return None
    s0 = {c: sol[0].get(c, c) for c in cs}
    s0 = {c: sp.sympify(x).subs({cc_: 0 for cc_ in cs}) for c, x in s0.items()}
    assert sp.expand(sum(s0[c] * E for c, E in zip(cs, eqs)) - target) == 0
    return [s0[c] for c in cs]
targets = {'h1': v[(1, 3)] + v[(4, 6)], 'h2': v[(1, 5)] + v[(4, 6)], 'h3': v[(3, 5)] + v[(4, 6)],
           'h4': v[(2, 4)] - v[(4, 6)], 'h5': v[(2, 6)] - v[(4, 6)]}
certs = {k: certificate(t) for k, t in targets.items()}
print('LOCI', USE, {k: (c is not None) for k, c in certs.items()})
import sys
if not all(c is not None for c in certs.values()): sys.exit(0)
# --- emit Lean
args = lambda full: ' '.join(f'({full[Z[ch]]} + {v[ch]})' if ch not in oe else f'({full[Z[ch]]})' for ch in CH)
def lean_expr(e):
    return str(e).replace('**', '^')
usedloci = sorted({pts[j][0] for c in certs.values() for j, x in enumerate(c) if x != 0})
lines = []
lines.append('/-- (d2) UNIQUENESS from hidden zeros. With (P) (v_oe = 0), if A6N(X̃ + v) vanishes on the massive')
lines.append(f'skinny-rectangle loci c = 0 with indices {usedloci} (the M2d loci, in X̃), then v lies on the a* line: uniform mass up to')
lines.append('δ-reparametrisation. Proof: evaluation at explicit points on the loci; the rational combinations were')
lines.append('found by `scripts/m2f_d2_cert.py` and are re-checked here by `linear_combination`. -/')
lines.append('theorem hidden_zeros_force6 (v13 v15 v24 v26 v35 v46 : ℝ)')
for (i, L, free) in [l for l in loci if l[0] in usedloci]:
    fv = ' '.join(str(f) for f in free)
    Lsub = {Z[ch]: (L[Z[ch]] if Z[ch] in L else Z[ch]) for ch in CH}
    argsym = ' '.join(f'({lean_expr(Lsub[Z[ch]])} + {v[ch]})' if ch not in oe else f'({lean_expr(Lsub[Z[ch]])})' for ch in CH)
    poles = ' → '.join(f'{lean_expr(Lsub[Z[ch]])} ≠ 0' for ch in oe)
    lines.append(f'    (z{i} : ∀ {fv} : ℝ, {poles} →')
    lines.append(f'      A6N {argsym} = 0)')
lines.append('    : v13 = -v46 ∧ v15 = -v46 ∧ v35 = -v46 ∧ v24 = v46 ∧ v26 = v46 := by')
used = sorted({j for c in certs.values() for j, x in enumerate(c) if x != 0})
for j in used:
    i, val, full = pts[j]
    L, free = [(l[1], l[2]) for l in loci if l[0] == i][0]
    vals = ' '.join(f'({val[f]})' for f in free)
    lines.append(f'  have e{j} := z{i} {vals} (by norm_num) (by norm_num) (by norm_num)')
lines.append('  simp only [A6N] at ' + ' '.join(f'e{j}' for j in used))
for k, t in targets.items():
    comb = ' + '.join(f'({lean_expr(c)} : ℝ) * e{j}' for j, c in enumerate(certs[k]) if c != 0)
    lines.append(f'  have {k} : {lean_expr(t)} = 0 := by linear_combination {comb}')
lines.append('  refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith⟩')
open('scripts/m2f_d2_cert_lean.txt', 'w').write('\n'.join(lines) + '\n')
print('used points:', len(used), 'of', len(eqs))
