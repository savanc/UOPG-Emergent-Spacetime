/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — FL-1Z tie theorems for the NAME-ONLY definition `FL1Z.D3` (D169).
Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.FL1Z

/-!
# FL-1Z ties: (D.3) of arXiv:2502.12662 is derived from the model at τ = ω

At the fixed point, App. D of 2502.12662 gives `Y₃⁽⁰⁾ = b₀ v₁`, `Y₃⁽⁻²⁾ = b₋₂ v_ω` with
`v₁ = (−1, 2ω, 2ω²)/3`, `v_ω = (2, −ω, 2ω²)/3` (eqs. B.13–B.14) and `b̃ₖ = 0`. With `f` (eq. III.16, antisymmetric
in `Y₃⁽⁰⁾`), `g` (III.16, `Y₃⁽⁻²⁾` part) and `M_ℓ = s (aₑ P + bₑ B(y) + cₑ C(y))` (III.2, `s = v/√2`), the product
`f M_ℓ* g M_ℓ† fᵀ` (III.14 without κ) equals `(2s²/9) b₀² b₋₂ (aₑ − b₀(bₑ + cₑ))² · D3 ω`, which is (D.3) with
`v²/9 = 2s²/9`. Conjugation acts as `ω ↦ ω²` (real parameters), so `M*` is `Mℓ (ω²)`.
The only hypothesis is `ω² + ω + 1 = 0`.

* Tie (D169): `mnu_eq_D3` — the hand-transcribed `D3` is the model's mass matrix at τ = ω.
* Known values: `D3` symmetric; `trace D3 = −3ω`.
* Planted: ω = 2 (not a cube root of unity) breaks rank one and det = 0.
* Non-vacuity: a primitive cube root of unity exists in ℂ (ω ≠ 1); the scale factor is nonzero.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.FL1ZSanity
open Matrix PositiveGeometryEmergentSpaceTime.FL1Z

variable {R : Type*} [Field R] [CharZero R]

/-- Antisymmetric A₄ contraction `C(y)` (eq. III.2/III.16 `f`), `y = (y₁, y₂, y₃)`. -/
def Cm (y1 y2 y3 : R) : Matrix (Fin 3) (Fin 3) R :=
  Matrix.of fun i j =>
  match i, j with
    | 0, 0 => 0
    | 0, 1 => y3
    | 0, 2 => -y2
    | 1, 0 => -y3
    | 1, 1 => 0
    | 1, 2 => y1
    | 2, 0 => y2
    | 2, 1 => -y1
    | 2, 2 => 0
/-- Symmetric A₄ contraction `B(y)` (eq. III.2, III.16 `g`). -/
def Bm (y1 y2 y3 : R) : Matrix (Fin 3) (Fin 3) R :=
  Matrix.of fun i j =>
  match i, j with
    | 0, 0 => 2 * y1
    | 0, 1 => -y3
    | 0, 2 => -y2
    | 1, 0 => -y3
    | 1, 1 => 2 * y2
    | 1, 2 => -y1
    | 2, 0 => -y2
    | 2, 1 => -y1
    | 2, 2 => 2 * y3
/-- The `1 ⊕ 1` permutation `P` of eq. III.2. -/
def Pm : Matrix (Fin 3) (Fin 3) R :=
  Matrix.of fun i j =>
  match i, j with
    | 0, 0 => 1
    | 0, 1 => 0
    | 0, 2 => 0
    | 1, 0 => 0
    | 1, 1 => 0
    | 1, 2 => 1
    | 2, 0 => 0
    | 2, 1 => 1
    | 2, 2 => 0
/-- `Y₃⁽⁰⁾ = b₀ v₁`, `v₁ = (−1, 2ζ, 2ζ²)/3` (eq. B.13), fed to a contraction `K`. -/
def atY0 (K : R → R → R → Matrix (Fin 3) (Fin 3) R) (b0 ζ : R) : Matrix (Fin 3) (Fin 3) R :=
  K (b0 * (-1 / 3)) (b0 * (2 * ζ / 3)) (b0 * (2 * ζ ^ 2 / 3))
/-- `Y₃⁽⁻²⁾ = b₋₂ v_ω`, `v_ω = (2, −ω, 2ω²)/3` (eq. B.14). -/
def atY2 (K : R → R → R → Matrix (Fin 3) (Fin 3) R) (bm ω : R) : Matrix (Fin 3) (Fin 3) R :=
  K (bm * (2 / 3)) (bm * (-ω / 3)) (bm * (2 * ω ^ 2 / 3))
/-- Charged-lepton matrix at τ = ω (`s = v/√2`), as a function of the root `ζ` (ζ = ω or its conjugate ω²). -/
def Ml (ae be ce b0 s ζ : R) : Matrix (Fin 3) (Fin 3) R :=
  s • (ae • Pm + be • atY0 Bm b0 ζ + ce • atY0 Cm b0 ζ)
/-- `f M_ℓ* g M_ℓ† fᵀ` at τ = ω (κ dropped). -/
def mnu (ae be ce b0 bm s ω : R) : Matrix (Fin 3) (Fin 3) R :=
  atY0 Cm b0 ω * Ml ae be ce b0 s (ω ^ 2) * atY2 Bm bm ω * (Ml ae be ce b0 s (ω ^ 2))ᵀ *
    (atY0 Cm b0 ω)ᵀ

/-- `D3` written entrywise (same matrix; used only to drive `simp`). -/
def D3m (ω : R) : Matrix (Fin 3) (Fin 3) R :=
  Matrix.of fun i j =>
  match i, j with
    | 0, 0 => 4
    | 0, 1 => -2 * ω ^ 2
    | 0, 2 => 4 * ω
    | 1, 0 => -2 * ω ^ 2
    | 1, 1 => ω
    | 1, 2 => -2
    | 2, 0 => 4 * ω
    | 2, 1 => -2
    | 2, 2 => 4 * ω ^ 2

omit [CharZero R] in
theorem D3_eq_D3m (ω : R) : D3 ω = D3m ω := by
  ext i j; fin_cases i <;> fin_cases j <;> rfl

set_option maxHeartbeats 4000000 in
/-- **Tie (D169).** The model's neutrino matrix at τ = ω is `(2s²/9) b₀² b₋₂ (aₑ − b₀(bₑ+cₑ))² · D3 ω`. -/
theorem mnu_eq_D3 (ae be ce b0 bm s ω : R) (hω : ω ^ 2 + ω + 1 = 0) :
    mnu ae be ce b0 bm s ω = (2 * s ^ 2 / 9 * b0 ^ 2 * bm * (ae - b0 * (be + ce)) ^ 2) • D3 ω := by
  rw [D3_eq_D3m]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp only [mnu, D3m, Ml, atY0, atY2, Cm, Bm, Pm, Matrix.mul_apply, Fin.sum_univ_three, Matrix.transpose_apply,
      Matrix.of_apply, Matrix.smul_apply, Matrix.add_apply, smul_eq_mul, Fin.isValue, Fin.zero_eta, Fin.mk_one,
      Fin.reduceFinMk]
  · linear_combination (8*b0^2*bm*s^2*(ω - 1)*(18*ae^2*ω^3 + 27*ae^2 - 66*ae*b0*be*ω^6 - 60*ae*b0*be*ω^3 - 54*ae*b0*be - 18*ae*b0*ce*ω^6 - 48*ae*b0*ce*ω^3 - 54*ae*b0*ce + 64*b0^2*be^2*ω^9 + 18*b0^2*be^2*ω^6 + 26*b0^2*be^2*ω^3 + 27*b0^2*be^2 + 40*b0^2*be*ce*ω^9 + 72*b0^2*be*ce*ω^6 + 56*b0^2*be*ce*ω^3 + 54*b0^2*be*ce + 8*b0^2*ce^2*ω^9 + 22*b0^2*ce^2*ω^6 + 30*b0^2*ce^2*ω^3 + 27*b0^2*ce^2)/243) * hω
  · linear_combination (4*b0^2*bm*s^2*ω^2*(ω - 1)*(-27*ae^2 + 54*ae*b0*be*ω^3 + 54*ae*b0*be + 42*ae*b0*ce*ω^3 + 60*ae*b0*ce + 8*b0^2*be^2*ω^9 - 62*b0^2*be^2*ω^3 - 27*b0^2*be^2 - 20*b0^2*be*ce*ω^6 - 24*b0^2*be*ce*ω^3 - 52*b0^2*be*ce - 8*b0^2*ce^2*ω^9 - 20*b0^2*ce^2*ω^6 - 34*b0^2*ce^2*ω^3 - 25*b0^2*ce^2)/243) * hω
  · linear_combination (-4*b0^2*bm*s^2*ω*(ω - 1)*(-45*ae^2 + 120*ae*b0*be*ω^3 + 114*ae*b0*be + 60*ae*b0*ce*ω^3 + 108*ae*b0*ce + 8*b0^2*be^2*ω^9 - 64*b0^2*be^2*ω^6 - 80*b0^2*be^2*ω^3 - 53*b0^2*be^2 - 60*b0^2*be*ce*ω^6 - 96*b0^2*be*ce*ω^3 - 108*b0^2*be*ce - 8*b0^2*ce^2*ω^9 - 28*b0^2*ce^2*ω^6 - 56*b0^2*ce^2*ω^3 - 55*b0^2*ce^2)/243) * hω
  · linear_combination (4*b0^2*bm*s^2*ω^2*(ω - 1)*(-27*ae^2 + 54*ae*b0*be*ω^3 + 54*ae*b0*be + 42*ae*b0*ce*ω^3 + 60*ae*b0*ce + 8*b0^2*be^2*ω^9 - 62*b0^2*be^2*ω^3 - 27*b0^2*be^2 - 20*b0^2*be*ce*ω^6 - 24*b0^2*be*ce*ω^3 - 52*b0^2*be*ce - 8*b0^2*ce^2*ω^9 - 20*b0^2*ce^2*ω^6 - 34*b0^2*ce^2*ω^3 - 25*b0^2*ce^2)/243) * hω
  · linear_combination (-8*b0^2*bm*s^2*ω*(ω - 1)*(-9*ae^2 - 12*ae*b0*be*ω^6 - 18*ae*b0*be*ω^3 + 12*ae*b0*be + 12*ae*b0*ce*ω^6 + 24*ae*b0*ce*ω^3 + 12*ae*b0*ce + 4*b0^2*be^2*ω^9 + 16*b0^2*be^2*ω^6 + 14*b0^2*be^2*ω^3 - 7*b0^2*be^2 - 8*b0^2*be*ce*ω^9 - 16*b0^2*be*ce*ω^6 - 22*b0^2*be*ce*ω^3 - 14*b0^2*be*ce + 4*b0^2*ce^2*ω^9 - 8*b0^2*ce^2*ω^6 - 4*b0^2*ce^2*ω^3 - 7*b0^2*ce^2)/243) * hω
  · linear_combination (2*b0^2*bm*s^2*(ω - 1)*(-63*ae^2 - 48*ae*b0*be*ω^6 - 18*ae*b0*be*ω^3 + 102*ae*b0*be + 48*ae*b0*ce*ω^6 + 138*ae*b0*ce*ω^3 + 108*ae*b0*ce + 24*b0^2*be^2*ω^9 + 64*b0^2*be^2*ω^6 - 6*b0^2*be^2*ω^3 - 55*b0^2*be^2 - 32*b0^2*be*ce*ω^9 - 84*b0^2*be*ce*ω^6 - 112*b0^2*be*ce*ω^3 - 108*b0^2*be*ce + 8*b0^2*ce^2*ω^9 - 52*b0^2*ce^2*ω^6 - 50*b0^2*ce^2*ω^3 - 53*b0^2*ce^2)/243) * hω
  · linear_combination (-4*b0^2*bm*s^2*ω*(ω - 1)*(-45*ae^2 + 120*ae*b0*be*ω^3 + 114*ae*b0*be + 60*ae*b0*ce*ω^3 + 108*ae*b0*ce + 8*b0^2*be^2*ω^9 - 64*b0^2*be^2*ω^6 - 80*b0^2*be^2*ω^3 - 53*b0^2*be^2 - 60*b0^2*be*ce*ω^6 - 96*b0^2*be*ce*ω^3 - 108*b0^2*be*ce - 8*b0^2*ce^2*ω^9 - 28*b0^2*ce^2*ω^6 - 56*b0^2*ce^2*ω^3 - 55*b0^2*ce^2)/243) * hω
  · linear_combination (2*b0^2*bm*s^2*(ω - 1)*(-63*ae^2 - 48*ae*b0*be*ω^6 - 18*ae*b0*be*ω^3 + 102*ae*b0*be + 48*ae*b0*ce*ω^6 + 138*ae*b0*ce*ω^3 + 108*ae*b0*ce + 24*b0^2*be^2*ω^9 + 64*b0^2*be^2*ω^6 - 6*b0^2*be^2*ω^3 - 55*b0^2*be^2 - 32*b0^2*be*ce*ω^9 - 84*b0^2*be*ce*ω^6 - 112*b0^2*be*ce*ω^3 - 108*b0^2*be*ce + 8*b0^2*ce^2*ω^9 - 52*b0^2*ce^2*ω^6 - 50*b0^2*ce^2*ω^3 - 53*b0^2*ce^2)/243) * hω
  · linear_combination (-4*b0^3*bm*s^2*ω^2*(ω - 1)*(-24*ae*be*ω^3 + 51*ae*be + 24*ae*ce*ω^3 + 99*ae*ce + 16*b0*be^2*ω^6 - 43*b0*be^2 - 16*b0*be*ce*ω^6 - 72*b0*be*ce*ω^3 - 104*b0*be*ce - 40*b0*ce^2*ω^3 - 53*b0*ce^2)/243) * hω

/-- Consequence of the tie: the model's matrix at τ = ω has determinant zero (two massless states,
as stated in 2502.12662 App. D). -/
theorem mnu_det_zero (ae be ce b0 bm s ω : R) (hω : ω ^ 2 + ω + 1 = 0) :
    (mnu ae be ce b0 bm s ω).det = 0 := by
  have h3 : ω ^ 3 = 1 := by linear_combination (ω - 1) * hω
  rw [mnu_eq_D3 ae be ce b0 bm s ω hω, Matrix.det_smul, D3_det_zero ω h3, mul_zero]

omit [CharZero R] in
/-- Known value: `D3` is symmetric. -/
theorem D3_symm (ω : R) : (D3 ω)ᵀ = D3 ω := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [D3]

omit [CharZero R] in
/-- Known value: `trace D3 = −3ω` at a primitive cube root of unity. -/
theorem D3_trace (ω : R) (hω : ω ^ 2 + ω + 1 = 0) : (D3 ω).trace = -3 * ω := by
  simp [Matrix.trace, D3, Fin.sum_univ_three]; linear_combination 4 * hω

/-- Planted: at ω = 2 (2³ ≠ 1) `D3` is not `w wᵀ` and `det D3 ≠ 0`. -/
theorem planted_omega2 : D3 (2 : ℚ) ≠ vecMulVec (w 2) (w 2) ∧ (D3 (2 : ℚ)).det ≠ 0 := by
  constructor
  · intro h; have := congrFun (congrFun h 1) 1; simp [D3, w, vecMulVec_apply] at this; norm_num at this
  · rw [Matrix.det_fin_three]; simp [D3]; norm_num

/-- Non-vacuity: a primitive cube root of unity exists in a characteristic-zero field
(ω = −1/2 + (√3/2) i in ℂ, ω ≠ 1), so the hypotheses of `mnu_eq_D3` and `D3_rank_one` are satisfiable. -/
theorem nonvacuous : ∃ ω : ℂ, ω ^ 2 + ω + 1 = 0 ∧ ω ≠ 1 := by
  refine ⟨⟨-1 / 2, Real.sqrt 3 / 2⟩, ?_, ?_⟩
  · have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
    apply Complex.ext <;> simp [pow_two] <;> nlinarith [h3]
  · intro h; have := congrArg Complex.re h; simp at this; norm_num at this

/-- Non-vacuity of the tie: at a primitive root, the scale factor can be nonzero, so `mnu` is not
identically zero (e.g. aₑ = s = b₀ = b₋₂ = 1, bₑ = cₑ = 0 gives the factor 2/9). -/
theorem tie_factor_nonzero : (2 * (1:ℚ) ^ 2 / 9 * 1 ^ 2 * 1 * (1 - 1 * (0 + 0)) ^ 2) = 2 / 9 := by norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.FL1ZSanity
