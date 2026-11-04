/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
M2b / P-EFT: the first non-linear face of the EFT-hedron.

Forward-limit coefficients of a crossing-symmetric, Froissart-bounded amplitude with
Im A ≥ 0 are moments `f k = ∫ x^k dμ` of a positive measure supported in `(0, xmax]`
(Bellazzini et al. arXiv:2011.00037 eqs. (3),(7); Arkani-Hamed–Huang–Huang
arXiv:2012.15849 §6). That physics step is a HYPOTHESIS here (CITED, not proved).
What is PROVED below: the moment ⇒ Hankel/gap step, for a finite measure on ℝ and for
finite positive combinations of point masses (any matrix size), plus exact toys and
counterexamples showing positivity is what makes the inequalities true.
Mathlib reused: `Matrix.PosSemidef`, `posSemidef_iff_dotProduct_mulVec`,
`PosSemidef.det_nonneg`, Bochner integral linearity / monotonicity.
-/
import Mathlib

open MeasureTheory Matrix Finset

namespace PositiveGeometryEmergentSpaceTime.Hankel

/-! ## Algebra: a nonnegative binary quadratic form has nonnegative discriminant gap -/

/-- If `a² p + 2ab q + b² r ≥ 0` for all real `a b`, then `q² ≤ p r`. -/
theorem sq_le_mul_of_quad_nonneg {p q r : ℝ}
    (h : ∀ a b : ℝ, 0 ≤ a ^ 2 * p + 2 * a * b * q + b ^ 2 * r) : q ^ 2 ≤ p * r := by
  have hp : 0 ≤ p := by simpa using h 1 0
  have hr : 0 ≤ r := by simpa using h 0 1
  rcases hp.eq_or_lt with hp0 | hp0
  · subst hp0
    by_cases hq : q = 0
    · simp [hq]
    · exfalso
      have h1 := h (-(r + 1) / (2 * q)) 1
      have : 2 * (-(r + 1) / (2 * q)) * 1 * q = -(r + 1) := by field_simp
      nlinarith
  · have h1 := h (-q) p
    have : 0 ≤ p * (p * r - q ^ 2) := by nlinarith
    nlinarith [(mul_nonneg_iff_of_pos_left hp0).mp this]

/-! ## (La)/(Lb): finite measures on ℝ -/

section Measure

variable {μ : Measure ℝ} [IsFiniteMeasure μ]

/-- `∫ (a + b x)² dμ` expanded in the first three moments. -/
theorem integral_sq_affine (h1 : Integrable (fun x : ℝ => x) μ)
    (h2 : Integrable (fun x : ℝ => x ^ 2) μ) (a b : ℝ) :
    ∫ x, (a + b * x) ^ 2 ∂μ
      = a ^ 2 * μ.real Set.univ + 2 * a * b * ∫ x, x ∂μ + b ^ 2 * ∫ x, x ^ 2 ∂μ := by
  have e : (fun x : ℝ => (a + b * x) ^ 2)
      = fun x => (a ^ 2 + (2 * a * b) * x) + b ^ 2 * x ^ 2 := by
    funext x; ring
  have i1 : Integrable (fun x : ℝ => a ^ 2 + (2 * a * b) * x) μ :=
    (integrable_const _).add (h1.const_mul _)
  have s1 : ∫ x, (a ^ 2 + (2 * a * b) * x) + b ^ 2 * x ^ 2 ∂μ
      = ∫ x, (a ^ 2 + (2 * a * b) * x) ∂μ + ∫ x, b ^ 2 * x ^ 2 ∂μ :=
    integral_add i1 (h2.const_mul _)
  have s2 : ∫ x, (a ^ 2 + (2 * a * b) * x) ∂μ = ∫ _x, a ^ 2 ∂μ + ∫ x, (2 * a * b) * x ∂μ :=
    integral_add (integrable_const _) (h1.const_mul _)
  rw [e, s1, s2, integral_const_mul, integral_const_mul, integral_const, smul_eq_mul]
  ring

/-- (La) Hankel / Cauchy–Schwarz: `f1² ≤ f0 · f2` for any finite measure on ℝ. -/
theorem moment_sq_le (h1 : Integrable (fun x : ℝ => x) μ)
    (h2 : Integrable (fun x : ℝ => x ^ 2) μ) :
    (∫ x, x ∂μ) ^ 2 ≤ μ.real Set.univ * ∫ x, x ^ 2 ∂μ := by
  apply sq_le_mul_of_quad_nonneg
  intro a b
  rw [← integral_sq_affine h1 h2]
  exact integral_nonneg fun x => sq_nonneg _

/-- The 2×2 Hankel matrix of moments `[[f0, f1], [f1, f2]]`. -/
noncomputable def hankel2 (μ : Measure ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![μ.real Set.univ, ∫ x, x ∂μ; ∫ x, x ∂μ, ∫ x, x ^ 2 ∂μ]

/-- (Lb) the 2×2 moment Hankel matrix is positive semidefinite (Mathlib `PosSemidef`). -/
theorem hankel2_posSemidef (h1 : Integrable (fun x : ℝ => x) μ)
    (h2 : Integrable (fun x : ℝ => x ^ 2) μ) : (hankel2 μ).PosSemidef := by
  refine PosSemidef.of_dotProduct_mulVec_nonneg ?_ ?_
  · ext i j; fin_cases i <;> fin_cases j <;> simp [hankel2]
  · intro v
    have : star v ⬝ᵥ (hankel2 μ *ᵥ v) = ∫ x, (v 0 + v 1 * x) ^ 2 ∂μ := by
      rw [integral_sq_affine h1 h2]
      simp [hankel2, dotProduct, mulVec, Fin.sum_univ_two]
      ring
    rw [this]
    exact integral_nonneg fun x => sq_nonneg _

omit [IsFiniteMeasure μ] in
/-- (Lc, gap) support in `[0, xmax]` ⇒ `f_{k+1} ≤ xmax · f_k`. -/
theorem moment_succ_le (k : ℕ) (xmax : ℝ)
    (hsupp : ∀ᵐ x ∂μ, 0 ≤ x ∧ x ≤ xmax)
    (hk : Integrable (fun x : ℝ => x ^ k) μ) (hk1 : Integrable (fun x : ℝ => x ^ (k + 1)) μ) :
    ∫ x, x ^ (k + 1) ∂μ ≤ xmax * ∫ x, x ^ k ∂μ := by
  rw [← integral_const_mul]
  refine integral_mono_ae hk1 (hk.const_mul _) ?_
  filter_upwards [hsupp] with x hx
  rw [pow_succ, mul_comm xmax]
  exact mul_le_mul_of_nonneg_left hx.2 (pow_nonneg hx.1 k)

end Measure

/-! ## (Lc): finite positive combinations of point masses, any size -/

section Discrete

variable {ι : Type*}

/-- `k`-th moment of the point-mass measure `∑ w_l δ_{x_l}`. -/
def moment (S : Finset ι) (w x : ι → ℝ) (k : ℕ) : ℝ := ∑ l ∈ S, w l * x l ^ k

/-- Hankel matrix `H i j = f (i + j)`, optionally shifted by `s` (`H^s` of the papers). -/
def hankel (n s : ℕ) (f : ℕ → ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  Matrix.of fun i j => f (i + j + s)

/-- For a finite point-mass measure, the quadratic form of the Hankel matrix of moments is `Σ_l w_l
  x_l^s (Σ_i v_i x_l^i)²`. -/
theorem quadForm_hankel (n s : ℕ) (S : Finset ι) (w x : ι → ℝ) (v : Fin n → ℝ) :
    star v ⬝ᵥ (hankel n s (moment S w x) *ᵥ v)
      = ∑ l ∈ S, (w l * x l ^ s) * (∑ i, v i * x l ^ (i : ℕ)) ^ 2 := by
  simp only [star_trivial, dotProduct, mulVec, hankel, moment, Matrix.of_apply, sq,
    Finset.mul_sum, Finset.sum_mul]
  conv_lhs => arg 2; ext i; rw [Finset.sum_comm]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun l _ => ?_
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun i _ => ?_
  rw [pow_add, pow_add]; ring

/-- (Lc) For `w ≥ 0` the `n×n` Hankel matrix of moments is positive semidefinite. With a
shift `s` it needs `x^s ≥ 0` on the support (e.g. `x ≥ 0`, or `s` even). -/
theorem hankel_posSemidef (n s : ℕ) (S : Finset ι) (w x : ι → ℝ)
    (hw : ∀ l ∈ S, 0 ≤ w l * x l ^ s) : (hankel n s (moment S w x)).PosSemidef := by
  refine PosSemidef.of_dotProduct_mulVec_nonneg ?_ ?_
  · ext i j; simp [hankel, add_comm]
  · intro v
    rw [quadForm_hankel]
    exact Finset.sum_nonneg fun l hl => mul_nonneg (hw l hl) (sq_nonneg _)

/-- Unshifted case: only `w ≥ 0` is needed. -/
theorem hankel_posSemidef_of_nonneg (n : ℕ) (S : Finset ι) (w x : ι → ℝ)
    (hw : ∀ l ∈ S, 0 ≤ w l) : (hankel n 0 (moment S w x)).PosSemidef :=
  hankel_posSemidef n 0 S w x fun l hl => by simpa using hw l hl

/-- 2×2 Hankel inequality `f1² ≤ f0 f2` (determinant of the PSD matrix, Mathlib `det_nonneg`). -/
theorem moment_sq_le_discrete (S : Finset ι) (w x : ι → ℝ) (hw : ∀ l ∈ S, 0 ≤ w l) :
    moment S w x 1 ^ 2 ≤ moment S w x 0 * moment S w x 2 := by
  have h := (hankel_posSemidef_of_nonneg 2 S w x hw).det_nonneg
  simp [Matrix.det_fin_two, hankel] at h
  nlinarith [h]

/-- (Lc, stretch) 3×3 Hankel determinant `det [[f0,f1,f2],[f1,f2,f3],[f2,f3,f4]] ≥ 0`
(EFT-hedron eq. (6.28)). -/
theorem hankel3_det_nonneg (S : Finset ι) (w x : ι → ℝ) (hw : ∀ l ∈ S, 0 ≤ w l) :
    0 ≤ (hankel 3 0 (moment S w x)).det :=
  (hankel_posSemidef_of_nonneg 3 S w x hw).det_nonneg

/-- Gap (discrete): support in `[0, xmax]` ⇒ `f_{k+1} ≤ xmax f_k`. -/
theorem moment_succ_le_discrete (S : Finset ι) (w x : ι → ℝ) (xmax : ℝ) (k : ℕ)
    (hw : ∀ l ∈ S, 0 ≤ w l) (hx : ∀ l ∈ S, 0 ≤ x l ∧ x l ≤ xmax) :
    moment S w x (k + 1) ≤ xmax * moment S w x k := by
  unfold moment
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum fun l hl => ?_
  rw [pow_succ]
  have := mul_le_mul_of_nonneg_left (hx l hl).2 (mul_nonneg (hw l hl) (pow_nonneg (hx l hl).1 k))
  linarith

end Discrete

/-! ## (Ld): exact rational toys and counterexamples -/

noncomputable section Toys

/-- Toy positive spectral measure `δ_{1/2} + 2 δ_{1/3} + 3 δ_1` (support in `[0,1]`). -/
def wT : Fin 3 → ℝ := ![1, 2, 3]
/-- Support points `(1/2, 1/3, 1)` of the toy measure. -/
def xT : Fin 3 → ℝ := ![1/2, 1/3, 1]

/-- Exact moments of the three-point toy measure (weights `wT = (1,2,3)` at `xT = (1/2,1/3,1)`): `6,
  25/6, 125/36, 691/216, …`. -/
theorem toy_moments :
    moment Finset.univ wT xT 0 = 6 ∧ moment Finset.univ wT xT 1 = 25/6 ∧
    moment Finset.univ wT xT 2 = 125/36 ∧ moment Finset.univ wT xT 3 = 691/216 ∧
    moment Finset.univ wT xT 4 = 4001/1296 := by
  simp [moment, Fin.sum_univ_three, wT, xT]; norm_num

/-- H2, H3 and gap for the toy, checked directly on the exact numbers. -/
theorem toy_checks :
    (25/6 : ℝ) ^ 2 ≤ 6 * (125/36) ∧
    0 ≤ (hankel 3 0 (moment Finset.univ wT xT)).det ∧
    (hankel 3 0 (moment Finset.univ wT xT)).det = 1/54 ∧
    (25/6 : ℝ) ≤ 1 * 6 ∧ (125/36 : ℝ) ≤ 1 * (25/6) := by
  refine ⟨by norm_num, hankel3_det_nonneg _ _ _ (by simp [wT, Fin.forall_fin_succ]),
    ?_, by norm_num, by norm_num⟩
  simp [Matrix.det_fin_three, hankel, moment, Fin.sum_univ_three, wT, xT]; norm_num

/-- Single resonance (T1 analogue): one delta saturates H2: `f1² = f0 f2`. -/
theorem single_delta_saturates (g x₀ : ℝ) :
    moment ({()} : Finset Unit) (fun _ => g) (fun _ => x₀) 1 ^ 2
      = moment {()} (fun _ => g) (fun _ => x₀) 0 * moment {()} (fun _ => g) (fun _ => x₀) 2 := by
  simp [moment]; ring

/-- C1 (pre-registered): the signed measure `δ_{1/2} − ½ δ_1` violates H2. -/
def wC : Fin 2 → ℝ := ![1, -1/2]
/-- Support points `(1/2, 1)` of counterexample C1. -/
def xC : Fin 2 → ℝ := ![1/2, 1]

/-- Counterexample C1 (`wC = (1, −1/2)` at `xC = (1/2, 1)`): moments `1/2, 0, −1/4` and `f₀ f₂ <
  f₁²`, so the 2×2 Hankel inequality fails. -/
theorem C1_violates :
    moment Finset.univ wC xC 0 = 1/2 ∧ moment Finset.univ wC xC 1 = 0 ∧
    moment Finset.univ wC xC 2 = -1/4 ∧
    moment Finset.univ wC xC 0 * moment Finset.univ wC xC 2 < moment Finset.univ wC xC 1 ^ 2 := by
  simp [moment, Fin.sum_univ_two, wC, xC]; norm_num

/-- C3 (added after pre-registration; stronger): signed weights `-3/2, 3, -1/2` at `0, 1, 2`
give moments `f0 = 1, f1 = 2, f2 = 1`, each *positive* (so every linear positivity bound
`f_k ≥ 0` passes), yet `f0 f2 = 1 < 4 = f1²`. The non-linear face does work the linear ones can't. -/
def wC3 : Fin 3 → ℝ := ![-3/2, 3, -1/2]
/-- Support points `(0, 1, 2)` of counterexample C3. -/
def xC3 : Fin 3 → ℝ := ![0, 1, 2]

/-- Counterexample C3 (`wC3 = (−3/2, 3, −1/2)` at `xC3 = (0, 1, 2)`): moments `1, 2, 1`, all
  positive, yet `f₀ f₂ = 1 < 4 = f₁²`. -/
theorem C3_violates :
    moment Finset.univ wC3 xC3 0 = 1 ∧ moment Finset.univ wC3 xC3 1 = 2 ∧
    moment Finset.univ wC3 xC3 2 = 1 ∧
    moment Finset.univ wC3 xC3 0 * moment Finset.univ wC3 xC3 2 < moment Finset.univ wC3 xC3 1 ^ 2 := by
  simp [moment, Fin.sum_univ_three, wC3, xC3]; norm_num

/-- Positivity is doing the work: **no** finite positive spectral measure has moments
`(f0, f1, f2) = (1, 2, 1)` (nor C1's `(1/2, 0, -1/4)`). -/
theorem no_positive_measure {ι : Type*} (S : Finset ι) (w x : ι → ℝ) (hw : ∀ l ∈ S, 0 ≤ w l) :
    ¬ (moment S w x 0 = 1 ∧ moment S w x 1 = 2 ∧ moment S w x 2 = 1) ∧
    ¬ (moment S w x 0 = 1/2 ∧ moment S w x 1 = 0 ∧ moment S w x 2 = -1/4) := by
  have h := moment_sq_le_discrete S w x hw
  constructor
  · rintro ⟨h0, h1, h2⟩; rw [h0, h1, h2] at h; norm_num at h
  · rintro ⟨h0, h1, h2⟩; rw [h0, h1, h2] at h; norm_num at h

/-- Same for any finite measure on ℝ (measure-theoretic version). -/
theorem no_finite_measure (μ : Measure ℝ) [IsFiniteMeasure μ]
    (h1 : Integrable (fun x : ℝ => x) μ) (h2 : Integrable (fun x : ℝ => x ^ 2) μ) :
    ¬ (μ.real Set.univ = 1 ∧ ∫ x, x ∂μ = 2 ∧ ∫ x, x ^ 2 ∂μ = 1) := by
  rintro ⟨h0, h1', h2'⟩
  have h := moment_sq_le h1 h2
  rw [h0, h1', h2'] at h; norm_num at h

end Toys

end PositiveGeometryEmergentSpaceTime.Hankel
