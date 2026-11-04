/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
RE-1: finite-dimensional relative entropy (classical / commuting case).
Reuses Mathlib: `Real.log_le_sub_one_of_pos`, `InformationTheory.klFun_nonneg`
(Mathlib InformationTheory.KullbackLeibler, credit: Mathlib contributors).
Context: Dorau & Much, PRL 136, 091602 (2026); Jacobson 1995 first-law step.
-/

open Real Finset

namespace PositiveGeometryEmergentSpaceTime.RelEntropy

variable {n : ℕ}

/-- Relative entropy S(p‖q) = Σ p_i log(p_i/q_i) of positive vectors. -/
noncomputable def relEnt (p q : Fin n → ℝ) : ℝ := ∑ i, p i * Real.log (p i / q i)

/-- (a) Gibbs inequality via log x ≤ x - 1 (Mathlib). -/
theorem relEnt_nonneg (p q : Fin n → ℝ) (hp : ∀ i, 0 < p i) (hq : ∀ i, 0 < q i)
    (hs : ∑ i, p i = ∑ i, q i) : 0 ≤ relEnt p q := by
  unfold relEnt
  have key : ∀ i, p i - q i ≤ p i * Real.log (p i / q i) := by
    intro i
    have h1 := Real.log_le_sub_one_of_pos (div_pos (hq i) (hp i))
    have h2 : Real.log (q i / p i) = - Real.log (p i / q i) := by
      rw [← Real.log_inv, inv_div]
    rw [h2] at h1
    have h3 : p i * (q i / p i - 1) = q i - p i := by
      rw [mul_sub, mul_div_cancel₀ _ (hp i).ne', mul_one]
    nlinarith [hp i, h3, mul_le_mul_of_nonneg_left h1 (hp i).le]
  calc (0:ℝ) = ∑ i, (p i - q i) := by rw [sum_sub_distrib, hs, sub_self]
    _ ≤ _ := sum_le_sum fun i _ => key i

/-- (a') Same inequality, reusing Mathlib's `klFun` (f-divergence form):
S(p‖q) = Σ q_i klFun(p_i/q_i) when Σp = Σq. -/
theorem relEnt_eq_sum_klFun (p q : Fin n → ℝ) (hq : ∀ i, 0 < q i)
    (hs : ∑ i, p i = ∑ i, q i) :
    relEnt p q = ∑ i, q i * InformationTheory.klFun (p i / q i) := by
  unfold relEnt
  have : ∀ i, q i * InformationTheory.klFun (p i / q i)
      = p i * Real.log (p i / q i) + (q i - p i) := by
    intro i; unfold InformationTheory.klFun
    have hqi := (hq i).ne'
    rw [mul_sub, mul_add, ← mul_assoc, mul_div_cancel₀ _ hqi, mul_one]; ring
  simp_rw [this, sum_add_distrib, sum_sub_distrib, hs, sub_self, add_zero]

/-- Gibbs' inequality: for `p ≥ 0`, `q > 0` with equal totals, `S(p‖q) ≥ 0`. -/
theorem relEnt_nonneg' (p q : Fin n → ℝ) (hp : ∀ i, 0 ≤ p i) (hq : ∀ i, 0 < q i)
    (hs : ∑ i, p i = ∑ i, q i) : 0 ≤ relEnt p q := by
  rw [relEnt_eq_sum_klFun p q hq hs]
  exact sum_nonneg fun i _ => mul_nonneg (hq i).le
    (InformationTheory.klFun_nonneg (div_nonneg (hp i) (hq i).le))

/-- (b1) First-order stationarity: along σ_t = ρ + t d with Σ d = 0,
d/dt S(σ_t‖ρ) at t = 0 equals 0. -/
theorem relEnt_firstOrder_zero (ρ d : Fin n → ℝ) (hρ : ∀ i, 0 < ρ i)
    (hd : ∑ i, d i = 0) :
    HasDerivAt (fun t => relEnt (fun i => ρ i + t * d i) ρ) 0 0 := by
  unfold relEnt
  have hi : ∀ i ∈ (univ : Finset (Fin n)),
      HasDerivAt (fun t => (ρ i + t * d i) * Real.log ((ρ i + t * d i) / ρ i)) (d i) 0 := by
    intro i _
    have hlin : HasDerivAt (fun t => ρ i + t * d i) (d i) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).mul_const (d i)).const_add (ρ i)
    have hdiv : HasDerivAt (fun t => (ρ i + t * d i) / ρ i) (d i / ρ i) 0 := hlin.div_const _
    have hlog := hdiv.log (by simp [(hρ i).ne'])
    have := hlin.mul hlog
    convert this using 1
    simp [(hρ i).ne']
    rw [mul_div_cancel₀ _ (hρ i).ne']
  have := HasDerivAt.fun_sum hi
  simpa [hd] using this

/-- Gibbs reference state ρ_i = e^{-K_i}/Z. -/
noncomputable def gibbs (K : Fin n → ℝ) : Fin n → ℝ :=
  fun i => Real.exp (-K i) / ∑ j, Real.exp (-K j)

/-- Exact identity: S(σ‖ρ_K) = ⟨K⟩_σ - S_vN(σ) + log Z  (for Σσ = 1). -/
theorem relEnt_gibbs (K σ : Fin n → ℝ) (hσ : ∀ i, 0 < σ i) (h1 : ∑ i, σ i = 1)
    [NeZero n] :
    relEnt σ (gibbs K) = ∑ i, σ i * K i - (-∑ i, σ i * Real.log (σ i))
      + Real.log (∑ j, Real.exp (-K j)) := by
  have hZ : 0 < ∑ j, Real.exp (-K j) :=
    sum_pos (fun j _ => Real.exp_pos _) univ_nonempty
  unfold relEnt gibbs
  have : ∀ i, σ i * Real.log (σ i / (Real.exp (-K i) / ∑ j, Real.exp (-K j)))
      = σ i * K i + σ i * Real.log (σ i) + σ i * Real.log (∑ j, Real.exp (-K j)) := by
    intro i
    rw [Real.log_div (hσ i).ne' (div_pos (Real.exp_pos _) hZ).ne',
      Real.log_div (Real.exp_pos _).ne' hZ.ne', Real.log_exp]; ring
  simp_rw [this, sum_add_distrib, ← sum_mul, h1]; ring

/-- (b) First law of entanglement (classical): along σ_t = ρ_K + t d, Σ d = 0,
δS_vN = δ⟨K⟩ at first order. -/
theorem first_law (K d : Fin n → ℝ) [NeZero n] (hd : ∑ i, d i = 0) :
    HasDerivAt (fun t => -∑ i, (gibbs K i + t * d i) * Real.log (gibbs K i + t * d i))
      (∑ i, d i * K i) 0 ∧
    HasDerivAt (fun t => ∑ i, (gibbs K i + t * d i) * K i) (∑ i, d i * K i) 0 := by
  have hZ : 0 < ∑ j, Real.exp (-K j) :=
    sum_pos (fun j _ => Real.exp_pos _) univ_nonempty
  have hρ : ∀ i, 0 < gibbs K i := fun i => div_pos (Real.exp_pos _) hZ
  have hlin : ∀ i, HasDerivAt (fun t => gibbs K i + t * d i) (d i) 0 := fun i => by
    simpa using ((hasDerivAt_id (0:ℝ)).mul_const (d i)).const_add (gibbs K i)
  constructor
  · have hi : ∀ i ∈ (univ : Finset (Fin n)), HasDerivAt
        (fun t => (gibbs K i + t * d i) * Real.log (gibbs K i + t * d i))
        (d i * (-K i - Real.log (∑ j, Real.exp (-K j))) + d i) 0 := by
      intro i _
      have hl := (hlin i).log (by simp [(hρ i).ne'])
      convert (hlin i).mul hl using 1
      simp only [zero_mul, add_zero]
      unfold gibbs
      rw [Real.log_div (Real.exp_pos _).ne' hZ.ne', Real.log_exp]
      field_simp [(Real.exp_pos (-K i)).ne', hZ.ne']
    have := (HasDerivAt.fun_sum hi).neg
    convert this using 1
    simp only [mul_sub, sum_add_distrib, sum_sub_distrib, ← sum_mul, hd]
    simp [mul_neg, sum_neg_distrib]
  · have hi : ∀ i ∈ (univ : Finset (Fin n)),
        HasDerivAt (fun t => (gibbs K i + t * d i) * K i) (d i * K i) 0 :=
      fun i _ => (hlin i).mul_const _
    exact HasDerivAt.fun_sum hi

end PositiveGeometryEmergentSpaceTime.RelEntropy
