/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# BH-1: Kerr black hole as the "minimal spinor structure" — algebraic and kinematic content

What is formalised (PROVED below): (a) massless little-group kinematics of a null momentum
`k = λ λ̃ᵀ` and the helicity weight of the minimal-coupling monomial `x^h · B^{2s}`;
(b) the exponentiation of minimal coupling, `(1 + y/(2s))^{2s} → exp y` (s → ∞), the finite-spin
coefficients `C(2s,ℓ)/(2s)^ℓ`, their vanishing for `ℓ > 2s`, and their convergence to `1/ℓ!`;
(c) the Kerr multipole sequence: `ℓ! · [z^ℓ] exp(i a z) = (i a)^ℓ`, with
`M_ℓ + i S_ℓ = m (i a)^ℓ` split into real/imaginary parts.

What is NOT formalised: general relativity, the Kerr metric, the identification of the
classical limit of amplitudes with Kerr. That identification is CITED (Arkani-Hamed–Huang–Huang
1709.04891; Guevara–Ochirov–Vines 1812.06895; Chung–Huang–Kim–Lee 1812.08752;
Arkani-Hamed–Huang–O'Connell 1906.10100; Vines 1709.06016).
-/

open Complex Filter Topology Matrix

namespace PositiveGeometryEmergentSpaceTime.KerrMinimal

/-! ## (a) Massless little group -/

/-- `k = λ λ̃ᵀ` (complexified null momentum as a 2×2 rank-≤1 matrix). -/
def nullMom (l lt : Fin 2 → ℂ) : Matrix (Fin 2) (Fin 2) ℂ := vecMulVec l lt

/-- Little-group invariance: `(λ, λ̃) ↦ (t λ, t⁻¹ λ̃)` leaves `k` fixed (`t ≠ 0`, GL(1)). -/
theorem nullMom_littleGroup (l lt : Fin 2 → ℂ) {t : ℂ} (ht : t ≠ 0) :
    nullMom (t • l) (t⁻¹ • lt) = nullMom l lt := by
  ext i j
  simp only [nullMom, vecMulVec_apply, Pi.smul_apply, smul_eq_mul]
  field_simp

/-- `k` is null: `det k = 0`. -/
theorem nullMom_det (l lt : Fin 2 → ℂ) : (nullMom l lt).det = 0 := by
  rw [det_fin_two]; simp [nullMom, vecMulVec_apply]; ring

/-- Real momenta: `λ̃ = λ*`, little group is the phase `U(1)`; `λ λᴴ` is invariant. -/
theorem outerH_phase (l : Fin 2 → ℂ) (θ : ℝ) :
    vecMulVec (exp (θ * I) • l) (star (exp (θ * I) • l)) = vecMulVec l (star l) := by
  ext i j
  simp only [vecMulVec_apply, Pi.smul_apply, smul_eq_mul, Pi.star_apply, star_mul']
  have h : exp (↑θ * I) * star (exp (↑θ * I)) = 1 := by
    have := Complex.mul_conj (exp (↑θ * I))
    simp only [Complex.normSq_eq_norm_sq, Complex.norm_exp_ofReal_mul_I] at this
    simpa using this
  calc exp (↑θ * I) * l i * (star (exp (↑θ * I)) * star (l j))
      = (exp (↑θ * I) * star (exp (↑θ * I))) * (l i * star (l j)) := by ring
    _ = l i * star (l j) := by rw [h, one_mul]

/-- The AHH `x`-factor carries little-group weight: if `x λ₃ = w` (with `w = p₁ λ̃₃ / m`) and
under `(λ₃, λ̃₃) ↦ (t λ₃, t⁻¹ λ̃₃)` we have `x' (t λ₃) = t⁻¹ w`, then `x' = t⁻² x`. -/
theorem x_weight {l w : Fin 2 → ℂ} (hl : l ≠ 0) {x x' t : ℂ} (ht : t ≠ 0)
    (hx : x • l = w) (hx' : x' • (t • l) = t⁻¹ • w) : x' = t⁻¹ ^ 2 * x := by
  obtain ⟨i, hi⟩ : ∃ i, l i ≠ 0 := by
    by_contra h; push Not at h; exact hl (funext h)
  have h1 := congrFun hx i
  have h2 := congrFun hx' i
  simp only [Pi.smul_apply, smul_eq_mul] at h1 h2
  rw [← h1] at h2
  have : (x' * t - t⁻¹ * x) * l i = 0 := by linear_combination h2
  rcases mul_eq_zero.mp this with h | h
  · field_simp at h ⊢; linear_combination h
  · exact absurd h hi

/-- Minimal-coupling monomial `x^h · B^{2s}` (B = ⟨𝟏𝟐⟩/m, blind to the massless little group). -/
def minimal (h s : ℕ) (x B : ℂ) : ℂ := x ^ h * B ^ (2 * s)

/-- Helicity weight: rescaling `x ↦ c x` rescales the minimal amplitude by `c^h`. -/
theorem minimal_weight (h s : ℕ) (x B c : ℂ) :
    minimal h s (c * x) B = c ^ h * minimal h s x B := by
  simp [minimal, mul_pow]; ring

/-! ## (b) Exponentiation of minimal coupling -/

/-- Classical limit: `(1 + y/(2s))^{2s} → exp y` as `s → ∞` (AHO eq. 24, GOV eq. 43). -/
theorem minimal_exponentiates (y : ℂ) :
    Tendsto (fun s : ℕ ↦ (1 + y / ((2 * s : ℕ) : ℂ)) ^ (2 * s)) atTop (𝓝 (exp y)) := by
  have h2 : Tendsto (fun s : ℕ ↦ 2 * s) atTop atTop :=
    tendsto_id.const_mul_atTop' (by norm_num)
  exact (Complex.tendsto_one_add_div_pow_exp y).comp h2

/-- Finite-spin multipole coefficient `c(n, ℓ) = C(n, ℓ)/n^ℓ`, with `n = 2s`. -/
noncomputable def coef (n ℓ : ℕ) : ℂ := (n.choose ℓ : ℂ) / (n : ℂ) ^ ℓ

/-- Binomial expansion: `(1 + y/n)^n = Σ_{ℓ ≤ n} c(n,ℓ) y^ℓ`. -/
theorem expand_finite (n : ℕ) (y : ℂ) :
    (1 + y / n) ^ n = ∑ ℓ ∈ Finset.range (n + 1), coef n ℓ * y ^ ℓ := by
  rw [add_comm, add_pow]
  refine Finset.sum_congr rfl fun ℓ _ ↦ ?_
  simp only [coef, one_pow, mul_one, div_pow]; ring

/-- Spin-s truncation (GOV eq. 41 nilpotency): no multipole beyond ℓ = 2s. -/
theorem coef_vanish {n ℓ : ℕ} (h : n < ℓ) : coef n ℓ = 0 := by
  simp [coef, Nat.choose_eq_zero_of_lt h]

/-- Monopole and dipole are exact at every finite spin: `c(n,0) = 1`, `c(n,1) = 1` (n ≥ 1). -/
theorem coef_zero (n : ℕ) : coef n 0 = 1 := by simp [coef]

/-- `coef n 1 = 1` for `n > 0`. -/
theorem coef_one {n : ℕ} (hn : 0 < n) : coef n 1 = 1 := by
  have : (n : ℂ) ≠ 0 := by exact_mod_cast hn.ne'
  simp [coef, this]

/-- For `ℓ ≤ n`, the descending factorial `n(n−1)⋯(n−ℓ+1)` cast to the field is `∏_{i<ℓ} (n − i)`. -/
lemma descFactorial_cast {n : ℕ} : ∀ ℓ, ℓ ≤ n →
    ((n.descFactorial ℓ : ℕ) : ℂ) = ∏ i ∈ Finset.range ℓ, ((n : ℂ) - i)
  | 0, _ => by simp
  | ℓ + 1, h => by
    rw [Nat.descFactorial_succ, Finset.prod_range_succ, Nat.cast_mul,
      descFactorial_cast ℓ (by omega), Nat.cast_sub (by omega)]
    ring

/-- Descending-product form: `ℓ! · c(n,ℓ) = ∏_{i<ℓ} (1 - i/n)` for `0 < n`, `ℓ ≤ n`. -/
theorem factorial_mul_coef {n ℓ : ℕ} (hn : 0 < n) (hℓ : ℓ ≤ n) :
    (ℓ.factorial : ℂ) * coef n ℓ = ∏ i ∈ Finset.range ℓ, (1 - (i : ℂ) / n) := by
  have hn' : (n : ℂ) ≠ 0 := by exact_mod_cast hn.ne'
  have key : (ℓ.factorial : ℂ) * (n.choose ℓ : ℂ) = ∏ i ∈ Finset.range ℓ, ((n : ℂ) - i) := by
    rw [← descFactorial_cast ℓ hℓ, Nat.descFactorial_eq_factorial_mul_choose]; push_cast; ring
  have : ∏ i ∈ Finset.range ℓ, (1 - (i : ℂ) / n) =
      (∏ i ∈ Finset.range ℓ, ((n : ℂ) - i)) / (n : ℂ) ^ ℓ := by
    have hp : (n : ℂ) ^ ℓ = ∏ _i ∈ Finset.range ℓ, (n : ℂ) := by
      rw [Finset.prod_const, Finset.card_range]
    rw [hp, ← Finset.prod_div_distrib]
    refine Finset.prod_congr rfl fun i _ ↦ ?_; field_simp
  rw [this, ← key, coef]; ring

/-- Large-spin limit of each multipole coefficient: `ℓ! · c(n,ℓ) → 1`, i.e. `c(n,ℓ) → 1/ℓ!`. -/
theorem coef_tendsto (ℓ : ℕ) :
    Tendsto (fun n : ℕ ↦ (ℓ.factorial : ℂ) * coef n ℓ) atTop (𝓝 1) := by
  have hlim : Tendsto (fun n : ℕ ↦ ∏ i ∈ Finset.range ℓ, (1 - (i : ℂ) / n)) atTop
      (𝓝 (∏ i ∈ Finset.range ℓ, (1 - (i : ℂ) * 0))) := by
    refine tendsto_finsetProd _ fun i _ ↦ ?_
    have h0 : Tendsto (fun n : ℕ ↦ (1 : ℂ) / n) atTop (𝓝 0) :=
      tendsto_one_div_atTop_nhds_zero_nat (𝕜 := ℂ)
    have := (h0.const_mul (i : ℂ)).const_sub 1
    refine this.congr fun n ↦ ?_
    rw [mul_one_div]
  simp only [mul_zero, sub_zero, Finset.prod_const_one] at hlim
  refine hlim.congr' ?_
  filter_upwards [eventually_ge_atTop (max ℓ 1)] with n hn
  exact (factorial_mul_coef (by omega) (by omega)).symm

/-! ## (c) Kerr multipoles: `M_ℓ + i S_ℓ = m (i a)^ℓ` -/

/-- Taylor coefficients of `exp(i a z)`: `ℓ! · [z^ℓ] = (i a)^ℓ` (Vines 1709.06016 eq. 1). -/
theorem kerr_coeff (a : ℂ) (ℓ : ℕ) :
    (ℓ.factorial : ℂ) * PowerSeries.coeff ℓ (PowerSeries.rescale (I * a) (PowerSeries.exp ℂ))
      = (I * a) ^ ℓ := by
  rw [PowerSeries.coeff_rescale, PowerSeries.coeff_exp]
  have : (ℓ.factorial : ℂ) ≠ 0 := by exact_mod_cast ℓ.factorial_ne_zero
  simp; field_simp

/-- Kerr mass multipoles `M_ℓ = m Re (i a)^ℓ` and current multipoles `S_ℓ = m Im (i a)^ℓ`. -/
noncomputable def massM (m a : ℝ) (ℓ : ℕ) : ℝ := m * ((I * a) ^ ℓ).re
/-- Current multipole `S_ℓ = m · Im((i a)^ℓ)` of the Kerr-type multipole tower. -/
noncomputable def currS (m a : ℝ) (ℓ : ℕ) : ℝ := m * ((I * a) ^ ℓ).im

/-- `(i a)^{2k} = (−1)^k a^{2k}` (a real number). -/
lemma pow_even (a : ℝ) (k : ℕ) : (I * a) ^ (2 * k) = (((-1) ^ k * a ^ (2 * k) : ℝ) : ℂ) := by
  rw [pow_mul, mul_pow, I_sq]; push_cast; rw [neg_one_mul, neg_pow, ← pow_mul]

/-- Even mass multipoles: `massM m a (2k) = m (−1)^k a^{2k}`. -/
theorem massM_even (m a : ℝ) (k : ℕ) : massM m a (2 * k) = m * (-1) ^ k * a ^ (2 * k) := by
  rw [massM, pow_even, ofReal_re]; ring

/-- Even current multipoles vanish: `currS m a (2k) = 0`. -/
theorem currS_even (m a : ℝ) (k : ℕ) : currS m a (2 * k) = 0 := by
  rw [currS, pow_even, ofReal_im, mul_zero]

/-- Odd mass multipoles vanish: `massM m a (2k+1) = 0`. -/
theorem massM_odd (m a : ℝ) (k : ℕ) : massM m a (2 * k + 1) = 0 := by
  rw [massM, pow_succ, pow_even, Complex.re_ofReal_mul]
  simp

/-- Odd current multipoles: `currS m a (2k+1) = m (−1)^k a^{2k+1}`. -/
theorem currS_odd (m a : ℝ) (k : ℕ) :
    currS m a (2 * k + 1) = m * (-1) ^ k * a ^ (2 * k + 1) := by
  rw [currS, pow_succ, pow_even, Complex.im_ofReal_mul]
  simp; ring

/-- Spin: `S_1 = m a`. Quadrupole: `M_2 = -m a²` (Kerr's oblateness). -/
theorem currS_one (m a : ℝ) : currS m a 1 = m * a := by simp [currS]
/-- Quadrupole: `massM m a 2 = −m a²`. -/
theorem massM_two (m a : ℝ) : massM m a 2 = -(m * a ^ 2) := by
  have := massM_even m a 1; simp at this; rw [this]

end PositiveGeometryEmergentSpaceTime.KerrMinimal
