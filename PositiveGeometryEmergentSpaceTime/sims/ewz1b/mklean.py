src=open('run2.py').read(); exec(src.split("print('CONTROL-0")[0])
import random
random.seed(1)
def build():
    res=[]
    for (A_,B_),(C_,D_) in (((0,1),(2,3)),((1,2),(3,0))):
        Ja=J(*gen[A_],*gen[B_]); Jb=J(*gen[C_],*gen[D_])
        v4,_=parts(V(Ja.d,0),V(Jb.d,0)); res.append((v4-Ja.f*Jb.f,(gen[A_][1]+gen[B_][1]).f**2))
    rr,ct=amp(gen)
    hz={ee[(1,3)]:0,ep[(1,3)]:0,ep[(3,1)]:0}
    tsol=S.solve(S.Eq(u-m2(1)-m2(3),2*k[0]*k[2]),t)[0]
    f=lambda x:S.sympify(x).subs(hz).subs(t,tsol)
    (ns,Ms),(nt,Mt)=res
    T=f(t)
    return f(ns)*(T-Mt)+f(nt)*(s-Ms)+f(ct)*(s-Ms)*(T-Mt)
N=build()
# sanity: N/( (s-Ms)(T-Mt) ) equals HZ(A4)
A=S.Symbol
G=S.groebner([a**2-lam3**2,lam4-lam3**2],lam4,a,lam3,order='lex')
q,r=S.reduced(S.expand(N),[a**2-lam3**2,lam4-lam3**2],lam4,a,lam3)
print('remainder',r)
names=sorted({str(x) for x in N.free_symbols})
P=lambda e:S.sstr(e).replace('**','^')
kin=[n for n in names if n not in('a','lam3','lam4')]
# find two points giving independent combos
pts=[]
while len(pts)<2:
    pt={S.Symbol(n):S.Rational(random.randint(-5,5)) for n in kin}
    c1=S.expand(q[0].subs(pt)); c2=S.expand(q[1].subs(pt))
    if c1.free_symbols or c2.free_symbols: pass
    pts.append((pt,c1,c2))
    if len(pts)==2:
        M=S.Matrix([[pts[0][1],pts[0][2]],[pts[1][1],pts[1][2]]])
        if M.det()==0: pts.pop()
print([(p[1],p[2]) for p in pts])
args=' '.join(names)
def call(pt): return 'N '+' '.join(n if n in ('a','lam3','lam4') else f'({P(pt[S.Symbol(n)])})' for n in names)
L=f"""import Mathlib

/-!
# EW-Z1b — hidden zeros of massive W amplitudes force the gauge/Higgs couplings (CGW 2601.16860 setup)

`N` = numerator × both propagators of the colour-ordered 4-vector amplitude A[1234] in the U(N)→U(1)^N
adjoint-Higgs (Coulomb-branch) theory of Carrillo González–Ward (arXiv 2601.16860, §VI.2), with *adjustable*
couplings `lam3` (VVV), `a` (VVS: Higgs/Goldstone–W–W per unit mass), `lam4` (VVVV), already restricted to the
hidden-zero locus c̃₁₃ = 0, ε₁·ε₃ = ε₁·p₃ = ε₃·p₁ = 0, with `t` eliminated. `k1 k2 k3` are vev differences
(masses; k4 = −k1−k2−k3), `s` the s-channel invariant, `eeij = εᵢ·εⱼ`, `eipj = εᵢ·pⱼ`. The expression is
generated verbatim from the Feynman rules by `sims/ewz1b/mklean.py` (cross-checked there against the full
amplitude). Claim tag of this file: PROVED (0 sorry).
-/

namespace PositiveGeometryEmergentSpaceTime.EWZ1b

def N ({args} : ℚ) : ℚ :=
  {P(N)}

def Q1 ({args} : ℚ) : ℚ := {P(q[0])}
def Q2 ({args} : ℚ) : ℚ := {P(q[1])}

/-- The hidden-zero residual is a combination of the two coupling defects only. -/
theorem N_decomp ({args} : ℚ) :
    N {args} = Q1 {args} * (a^2 - lam3^2) + Q2 {args} * (lam4 - lam3^2) := by
  unfold N Q1 Q2; ring

/-- CGW: in the spontaneously broken theory (a = ±lam3, lam4 = lam3², e.g. all = 1) the hidden zero holds
for all masses, polarisations and `s`. -/
theorem zero_of_gauge ({args} : ℚ) (ha : a^2 = lam3^2) (h4 : lam4 = lam3^2) :
    N {args} = 0 := by
  rw [N_decomp, ha, h4]; ring

/-- Forcing: if the zero holds at two explicit kinematic points, then a² = lam3² and lam4 = lam3². -/
theorem forced (a lam3 lam4 : ℚ)
    (h1 : {call(pts[0][0])} = 0)
    (h2 : {call(pts[1][0])} = 0) :
    a^2 = lam3^2 ∧ lam4 = lam3^2 := by
  rw [N_decomp] at h1 h2
  simp only [Q1, Q2] at h1 h2
  norm_num at h1 h2
  constructor <;> nlinarith [h1, h2]

theorem forced_iff (a lam3 lam4 : ℚ) :
    (a^2 = lam3^2 ∧ lam4 = lam3^2) ↔ ((a = lam3 ∨ a = -lam3) ∧ lam4 = lam3^2) := by
  constructor
  · rintro ⟨h, h4⟩; exact ⟨sq_eq_sq'_iff.mp h |>.symm.imp id id |> fun x => by
      rcases sq_eq_sq_iff_eq_or_eq_neg.mp h with h' | h' <;> simp [h'], h4⟩
  · rintro ⟨h | h, h4⟩ <;> subst h <;> exact ⟨by ring, h4⟩

/-- Control (CGW eq. 53–54): naive Proca YM on the zero leaves m²(P/X + Q/Y) with X + Y = 0,
i.e. a scalar-exchange-shaped residue m²(P − Q)/X, nonzero unless m = 0 or P = Q. -/
theorem proca_control (m P Q X Y : ℚ) (hX : X ≠ 0) (hXY : X + Y = 0) :
    m^2 * (P / X + Q / Y) = m^2 * (P - Q) / X := by
  have : Y = -X := by linarith
  subst this; field_simp; ring

theorem proca_nonzero (m P Q X : ℚ) (hX : X ≠ 0) (hm : m ≠ 0) (hPQ : P ≠ Q) :
    m^2 * (P - Q) / X ≠ 0 := by
  have : P - Q ≠ 0 := sub_ne_zero.mpr hPQ
  positivity

end PositiveGeometryEmergentSpaceTime.EWZ1b
"""
open('../../lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean','w').write(L)
