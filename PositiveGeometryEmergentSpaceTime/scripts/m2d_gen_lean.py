import sympy as sp, itertools, re
exec(open('scripts/m2d_laurent.py').read().split("for n,p in")[0])
def L(e):
    s=str(e).replace('**','^').replace('epsilon','e')
    return s
def termsA(n):
    X=Xsym(n); chords=list(X)
    cross=lambda a,b:(a[0]<b[0]<a[1]<b[1]) or (b[0]<a[0]<b[1]<a[1])
    Ts=[T for T in itertools.combinations(chords,n-3) if all(not cross(a,b) for a,b in itertools.combinations(T,2))]
    return ' + '.join('1 / (' + ' * '.join(f'X{a}{b}' for a,b in T)+')' for T in Ts)
X6,D6,N6=run(6,4); X5,D5,N5=run(5,2); _,_,N51=run(5,1)
v6='X13 X14 X15 X24 X25 X26 X35 X36 X46'
sh6='(X13 - δ) X14 (X15 - δ) (X24 + δ) X25 (X26 + δ) (X35 - δ) X36 (X46 + δ)'
v5='X13 X14 X24 X25 X35'
sh5='(X13 - δ) X14 (X24 + δ) X25 (X35 - δ)'
# loci n=6 skinny rectangles
def getX(X,n,i,j):
    i,j=(i-1)%n+1,(j-1)%n+1
    if i>j:i,j=j,i
    if j-i<=1 or (i==1 and j==n): return sp.Integer(0)
    return X[(i,j)]
def c(X,n,i,j): return getX(X,n,i,j)+getX(X,n,i+1,j+1)-getX(X,n,i,j+1)-getX(X,n,i+1,j)
def locus(X,n,conds):
    eqs=[c(X,n,*q) for q in conds]
    for vs in itertools.combinations(list(X.values()),len(eqs)):
        if any(v in (X.get((1,4)),X.get((2,5)),X.get((3,6))) for v in vs) and n==6: continue
        sol=sp.solve(eqs,vs,dict=True)
        if sol and all(sp.simplify(e.subs(sol[0]))==0 for e in eqs): return eqs,sol[0]
nz6='(h14 : X14 ≠ 0) (h25 : X25 ≠ 0) (h36 : X36 ≠ 0)'
zeros6=[]
for i in range(1,7):
    eqs,sol=locus(X6,6,[(i,i+2),(i,i+3),(i,i+4)])
    hyps=' '.join(f'(hc{k} : {L(e)} = 0)' for k,e in enumerate(eqs))
    haves='\n'.join(f'  have e{k} : {L(v)} = {L(ex)} := by linarith' for k,(v,ex) in enumerate(sol.items()))
    substs=' '.join(f'e{k}' for k in range(len(sol)))
    zeros6.append(f'''/-- [H] §4.1: A6^NLSM vanishes on the skinny rectangle at index {i}: c_{{{i},j}} = 0 for all j non-adjacent. -/
theorem nlsm6_zero_{i} {{{v6} : ℝ}} {nz6}
    {hyps} :
    A6N {v6} = 0 := by
{haves}
  subst {substs}
  simp only [A6N]
  field_simp
  ring''')
loci5=[((1,3),(1,4)),((2,4),(2,5)),((3,5),(1,3)),((1,4),(2,4)),((2,5),(3,5))]
nzall5=lambda: None
zeros5=[]
for idx,zs in enumerate(loci5):
    eqs,sol=locus(X5,5,list(zs))
    hyps=' '.join(f'(hc{k} : {L(e)} = 0)' for k,e in enumerate(eqs))
    haves='\n'.join(f'  have e{k} : {L(v)} = {L(ex)} := by linarith' for k,(v,ex) in enumerate(sol.items()))
    substs=' '.join(f'e{k}' for k in range(len(sol)))
    zeros5.append(f'''/-- [H] §3.1.1 skinny-rectangle zero {{c{zs[0][0]}{zs[0][1]}, c{zs[1][0]}{zs[1][1]}}} = 0 in the full 5-dim kinematic space. -/
theorem m5f_zero_{idx} {{{v5} : ℝ}} (h13 : X13 ≠ 0) (h14 : X14 ≠ 0) (h24 : X24 ≠ 0) (h25 : X25 ≠ 0) (h35 : X35 ≠ 0)
    {hyps} :
    m5f {v5} = 0 := by
{haves}
  subst {substs}
  simp only [m5f]
  field_simp
  ring''')
s5=dict(zip(['X13','X14','X24','X25','X35'],['-1','0','1','0','-1']))
def denoms_nz(vs,shifts):
    out=[]
    for v in vs.split():
        sgn=shifts[v]
        if sgn=='0': continue
        out.append(f'have n{v} : {v} {"-" if sgn=="-1" else "+"} δ ≠ 0 := by intro h; have := le_abs_self {v}; have := neg_abs_le {v}; linarith [ALLABS]')
    return out
sh6d=dict(zip(v6.split(),['-1','0','-1','1','0','1','-1','0','1']))
def bound(vs,shifts): return ' + '.join(f'|{v}|' for v in vs.split() if shifts[v]!='0')+' + 1'
def invfacts(vs,shifts):
    out=[]
    for v in vs.split():
        sgn=shifts[v]
        if sgn=='0': continue
        op='-' if sgn=='-1' else '+'
        out.append(f'have i{v} : 1 {op} δ⁻¹ * {v} = (δ {"-" if sgn=="-1" else "+"} {v}) / δ := by field_simp')
    return out
def limit_thm(name,doc,vs,shiftstr,shifts,fn,power,N,D,target,extra_nz,valtac):
    oe=[v for v in vs.split() if shifts[v]=='0' and v in extra_nz]
    facs=[]
    for v in vs.split():
        if shifts[v]=='-1': facs.append((v,f'((-{v}) * e + 1)',f'((-{v}) * δ⁻¹ + 1)',f'(δ - {v})'))
        elif shifts[v]=='1': facs.append((v,f'({v} * e + 1)',f'({v} * δ⁻¹ + 1)',f'(δ + {v})'))
    Dstr=' * '.join(oe+[f[1] for f in facs])
    Dd=' * '.join(oe+[f[2] for f in facs])
    g=f'fun e : ℝ => ({L(N)}) / ({Dstr})'
    nzs=denoms_nz(vs,shifts)
    fl=[]
    for v,_,dd,num in facs:
        fl.append(f'have f{v} : {dd} ≠ 0 := by\n      rw [show {dd} = {num} / δ by field_simp; ring]\n      exact div_ne_zero (by intro h; have := le_abs_self {v}; have := neg_abs_le {v}; linarith [ALLABS]) hδ0')
    ind='    '
    return f'''/-- {doc} -/
theorem {name} {{{vs} : ℝ}} {extra_nz} :
    Tendsto (fun δ : ℝ => δ ^ {power} * {fn} {shiftstr}) atTop (𝓝 ({target})) := by
  have key := tendsto_atTop_of_inv (F := fun δ : ℝ => δ ^ {power} * {fn} {shiftstr})
    (g := {g}) ?_ ?_
  · convert key using 2
    {valtac}
  · apply ContinuousAt.div (by fun_prop) (by fun_prop)
    simp [*]
  · filter_upwards [eventually_gt_atTop ({bound(vs,shifts)})] with δ hδ
    have hδ0 : δ ≠ 0 := by
      intro h; rw [h] at hδ; linarith [{', '.join(f'abs_nonneg {v}' for v in vs.split() if shifts[v]!='0')}]
''' + '\n'.join(ind+x for x in nzs) + '\n' + '\n'.join(ind+x for x in fl) + f'''
    have hD : {Dd} ≠ 0 := by apply_rules [mul_ne_zero]
    show _ = _ / _
    rw [eq_div_iff hD]
    simp only [{fn}]
    field_simp
    ring'''
hdr='''/-
M2d — from Tr(φ³) to pions by the δ-shift.
Sources: [N] Arkani-Hamed, Cao, Dong, Figueiredo, He, "NLSM ⊂ Tr(φ³)", arXiv:2401.05483, eqs. (1)–(2);
[H] same authors, "Hidden zeros for particle/string amplitudes and the unity of colored scalars, pions and
gluons", arXiv:2312.16282, §3 (eqs. 3.1, 3.3, 3.5), §4 (eqs. 4.3, 4.4).
Shift: X_{e,e} ↦ X + δ, X_{o,o} ↦ X − δ, X_{o,e} unchanged.

Labels: LIMIT = a genuine `Filter.Tendsto … atTop`; IDENTITY = an exact rational-function identity.
Every LIMIT is proved by writing δ^k · A(X̃) = N(δ⁻¹)/D(δ⁻¹) eventually, with N, D polynomials, D(0) ≠ 0.
That N has no negative powers of ε = δ⁻¹ *is* the cancellation of the O(δ⁻ᵐ) terms.
N was generated by `scripts/m2d_nlsm_check.py`'s companion and is checked here by `field_simp; ring`,
so nothing is trusted from the script.
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Associahedron

open Filter Topology

namespace PositiveGeometryEmergentSpaceTime.NLSM

set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-- Limit at +∞ through ε = δ⁻¹. -/
theorem tendsto_atTop_of_inv {F g : ℝ → ℝ} (hg : ContinuousAt g 0)
    (hF : ∀ᶠ δ in atTop, F δ = g δ⁻¹) : Tendsto F atTop (𝓝 (g 0)) :=
  (hg.tendsto.comp tendsto_inv_atTop_zero).congr' (hF.mono fun _ h => h.symm)

/-! ## n = 4 -/

/-- Tr(φ³) 4-point amplitude. -/
noncomputable def A4 (X13 X24 : ℝ) : ℝ := 1 / X13 + 1 / X24
/-- NLSM 4-point amplitude in [H]'s normalisation (eq. 4.4). -/
def A4N (X13 X24 : ℝ) : ℝ := X13 + X24
/-- IDENTITY ([H] eq. 4.4): A4^NLSM = c13 (here c13 = X13 + X24 − X14 − X23 with X14 = X23 = 0), so it vanishes at c13 = 0. -/
theorem nlsm4_eq_c13 (X13 X24 : ℝ) : A4N X13 X24 = X13 + X24 - 0 - 0 := by simp [A4N]

'''
n4=limit_thm('shift4_limit','LIMIT ([N] eq. 2, n = 4 example): δ² · A4(X13 − δ, X24 + δ) → −(X13 + X24) = −A4^NLSM.','X13 X24','(X13 - δ) (X24 + δ)',{'X13':'-1','X24':'1'},'A4',2,-sp.Symbol('X13')-sp.Symbol('X24'),None,'-(X13 + X24)','','norm_num\n    try ring')
body5=f'''
/-! ## n = 5 (odd): not a pion amplitude -/

/-- m5 on the full 5-dim kinematic space (free planar variables), [H] eq. 3.1. -/
noncomputable def m5f ({v5} : ℝ) : ℝ := {termsA(5)}

/-- M2c's m5 on H is m5f restricted to H. -/
theorem m5_eq_m5f (c13 c14 c24 x y : ℝ) :
    PositiveGeometryEmergentSpaceTime.Assoc.m5 c13 c14 c24 x y = m5f x y (y - x + c13) (c13 + c14 - x) (c14 + c24 - y) := by
  simp only [PositiveGeometryEmergentSpaceTime.Assoc.m5, m5f]; ring

/-- Leading large-δ coefficient of the shifted 5-point amplitude (a mixed π/φ object, X⁰). -/
noncomputable def L5 ({v5} : ℝ) : ℝ := 1 - (X13 + X24) / X14 - (X24 + X35) / X25

'''
n51=limit_thm('shift5_limit_one','LIMIT: δ · m5(X̃) → 0. The O(δ⁻¹) terms cancel; there is no pion-order term.',v5,sh5,dict(zip(v5.split(),['-1','0','1','0','-1'])),'m5f',1,N51,None,'0','(h14 : X14 ≠ 0) (h25 : X25 ≠ 0)','norm_num\n    try ring')
n52=limit_thm('shift5_limit_two','LIMIT: δ² · m5(X̃) → L5, with poles only at the (o,e) chords X14, X25.',v5,sh5,dict(zip(v5.split(),['-1','0','1','0','-1'])),'m5f',2,N5,None,f'L5 {v5}','(h14 : X14 ≠ 0) (h25 : X25 ≠ 0)','simp only [L5]; field_simp; ring')
body5b=f'''
/-- IDENTITY: under the shift, among the five c's only c14 = X14 + X25 − X24 moves (by −δ). -/
theorem shift5_c (δ {v5} : ℝ) :
    ((X13 - δ) + (X24 + δ) - X14 = X13 + X24 - X14) ∧ (X14 + X25 - (X24 + δ) = X14 + X25 - X24 - δ) ∧
    ((X24 + δ) + (X35 - δ) - X25 = X24 + X35 - X25) ∧ (X25 + (X13 - δ) - (X35 - δ) = X25 + X13 - X35) ∧
    ((X35 - δ) + X14 - (X13 - δ) = X35 + X14 - X13) := by
  refine ⟨by ring, by ring, by ring, by ring, by ring⟩

/-! ## Hidden zeros and near-zero factorisation (n = 5) -/

''' + '\n\n'.join(zeros5) + f'''

/-- IDENTITY ([H] eq. 3.3): near the zero, c14 = 0 ⇒ m5 = (1/X13 + 1/X25)(1/X14 + 1/X35). -/
theorem m5f_factor_c14 {{{v5} : ℝ}} (h13 : X13 ≠ 0) (h14 : X14 ≠ 0) (h24 : X24 ≠ 0) (h25 : X25 ≠ 0)
    (h35 : X35 ≠ 0) (hc : X14 + X25 - X24 = 0) :
    m5f {v5} = (1 / X13 + 1 / X25) * (1 / X14 + 1 / X35) := by
  have e : X24 = X14 + X25 := by linarith
  subst e; simp only [m5f]; field_simp; ring

/-- IDENTITY ([H] eq. 3.5): c13 = 0 ⇒ m5 = (1/X13 + 1/X25)(1/X24 + 1/X35). -/
theorem m5f_factor_c13 {{{v5} : ℝ}} (h13 : X13 ≠ 0) (h14 : X14 ≠ 0) (h24 : X24 ≠ 0) (h25 : X25 ≠ 0)
    (h35 : X35 ≠ 0) (hc : X13 + X24 - X14 = 0) :
    m5f {v5} = (1 / X13 + 1 / X25) * (1 / X24 + 1 / X35) := by
  have e : X14 = X13 + X24 := by linarith
  subst e; simp only [m5f]; field_simp; ring

/-! ## n = 6 -/

/-- Tr(φ³) 6-point amplitude: the 14 planar cubic diagrams. -/
noncomputable def A6 ({v6} : ℝ) : ℝ :=
  {termsA(6)}

/-- NLSM 6-point amplitude, [H] eq. 4.3: (X13+X24)(X15+X46)/X14 − X13 − X24 + (i → i+2) + (i → i+4). -/
noncomputable def A6N ({v6} : ℝ) : ℝ :=
  ((X13 + X24) * (X15 + X46) / X14 - X13 - X24) + ((X35 + X46) * (X13 + X26) / X36 - X35 - X46)
    + ((X15 + X26) * (X35 + X24) / X25 - X15 - X26)

'''
n6=limit_thm('shift6_limit','LIMIT ([N] eq. 2, 2n = 6): δ⁴ · A6(X̃) → A6^NLSM ([H] eq. 4.3), sign +1 as pre-registered. The O(δ⁻¹), O(δ⁻²), O(δ⁻³) terms all cancel.',v6,sh6,sh6d,'A6',4,N6,None,f'A6N {v6}','(h14 : X14 ≠ 0) (h25 : X25 ≠ 0) (h36 : X36 ≠ 0)','simp only [A6N]; field_simp; ring')
tail=f'''

''' + '\n\n'.join(zeros6) + f'''

/-- IDENTITY ([H] §4.1, (e)): Adler zero. Soft p1 sends X13, X26 → 0, X14 → X24, X15 → X25; then A6^NLSM = 0. -/
theorem nlsm6_adler {{X24 X25 X35 X36 X46 : ℝ}} (h24 : X24 ≠ 0) (h25 : X25 ≠ 0) (h36 : X36 ≠ 0) :
    A6N 0 X24 X25 X24 X25 0 X35 X36 X46 = 0 := by
  simp only [A6N]; field_simp; ring

/-- IDENTITY: the δ-shifted A6 already vanishes at finite δ on the skinny rectangle c13 = c14 = c15 = 0
(the shift leaves every c unchanged for even n, [N] eq. 1). -/
theorem shift6_zero_1 {{δ {v6} : ℝ}}
    (n13 : X13 - δ ≠ 0) (h14 : X14 ≠ 0) (n15 : X15 - δ ≠ 0) (n24 : X24 + δ ≠ 0) (h25 : X25 ≠ 0)
    (n26 : X26 + δ ≠ 0) (n35 : X35 - δ ≠ 0) (h36 : X36 ≠ 0) (n46 : X46 + δ ≠ 0)
    (hc0 : X13 + X24 - X14 = 0) (hc1 : X14 + X25 - X24 - X15 = 0) (hc2 : X15 + X26 - X25 = 0) :
    A6 {sh6} = 0 := by
  have e0 : X24 = X14 - X13 := by linarith
  have e1 : X25 = X15 - X13 := by linarith
  have e2 : X26 = -X13 := by linarith
  subst e0 e1 e2
  simp only [A6]
  field_simp
  ring

end PositiveGeometryEmergentSpaceTime.NLSM
'''
txt=hdr+n4+body5+n51+'\n\n'+n52+body5b+n6+tail
blocks=txt.split('/-- ')
for bi,b in enumerate(blocks):
    m=re.search(r'eventually_gt_atTop \(([^)]*)\)',b)
    if m:
        vs=re.findall(r'\|(X\d\d)\|',m.group(1))
        blocks[bi]=b.replace('ALLABS',', '.join('abs_nonneg '+v for v in vs))
txt='/-- '.join(blocks)
open('lean/PositiveGeometryEmergentSpaceTime/NLSM.lean','w').write(txt)
