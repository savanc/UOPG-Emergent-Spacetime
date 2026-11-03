/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
M2 / P-EFT, Lean part 1: positivity of curvature from a positive spectral representation.

What is HYPOTHESIS here (tagged CITED, not proved):
  * the twice-subtracted fixed-t dispersion relation (analyticity + crossing + Froissart
    bound => n = 2 subtractions), Manohar-Mateu 2008 eq. (11), Adams et al. 2006 eq. (31);
  * Im T >= 0 on both cuts (optical theorem + P_l(z) >= 1 for z >= 1, for elastic processes
    whose u-channel is also elastic), Manohar-Mateu eqs. (13)-(15).
What is PROVED: the step from those hypotheses to the sign.
-/

open MeasureTheory Set

namespace PositiveGeometryEmergentSpaceTime.Dispersion

/-- L1. If the second s-derivative of the amplitude is given by the twice-subtracted
dispersion integral with right-hand (s) and crossed (u) cut discontinuities `imS`, `imU`
that are nonnegative above threshold `s₀`, and the evaluation point lies below both cuts,
then the second derivative is nonnegative. (`A2` is "d²T/ds²(s,t)"; its equality with the
integral is the CITED dispersion relation.) -/
theorem secondDeriv_nonneg_of_dispersion
    (s₀ s u A2 : ℝ) (imS imU : ℝ → ℝ)
    (hs : s < s₀) (hu : u < s₀)
    (himS : ∀ x, s₀ ≤ x → 0 ≤ imS x) (himU : ∀ x, s₀ ≤ x → 0 ≤ imU x)
    (hdisp : A2 = (2 / Real.pi) * ∫ x in Ici s₀, (imS x / (x - s) ^ 3 + imU x / (x - u) ^ 3)) :
    0 ≤ A2 := by
  rw [hdisp]
  apply mul_nonneg (div_nonneg zero_le_two Real.pi_pos.le)
  apply setIntegral_nonneg measurableSet_Ici
  intro x hx
  have hx' : s₀ ≤ x := hx
  have h1 : 0 < x - s := by linarith
  have h2 : 0 < x - u := by linarith
  exact add_nonneg (div_nonneg (himS x hx') (pow_pos h1 3).le)
    (div_nonneg (himU x hx') (pow_pos h2 3).le)

/-- The same statement for a general positive measure (any spectral measure `μ` on
`[s₀, ∞)`; the density with respect to Lebesgue is not needed). -/
theorem secondDeriv_nonneg_of_measure
    (s₀ s u A2 : ℝ) (μ : Measure ℝ) (hμ : μ (Iio s₀) = 0)
    (hs : s < s₀) (hu : u < s₀)
    (hdisp : A2 = ∫ x, (2 / (x - s) ^ 3 + 2 / (x - u) ^ 3) ∂μ) :
    0 ≤ A2 := by
  rw [hdisp]
  apply integral_nonneg_of_ae
  have : ∀ᵐ x ∂μ, s₀ ≤ x := by
    rw [ae_iff]
    simp only [not_le]
    exact hμ
  filter_upwards [this] with x hx
  have h1 : 0 < x - s := by linarith
  have h2 : 0 < x - u := by linarith
  simp only [Pi.zero_apply]
  positivity

/-- A single pole term `s ↦ 1/(x - s)` is convex on `s < x`. -/
theorem convexOn_pole_right (x : ℝ) : ConvexOn ℝ (Iio x) (fun s : ℝ => 1 / (x - s)) := by
  let g : ℝ →ᵃ[ℝ] ℝ := ⟨fun s => x - s, -LinearMap.id, by
    intro p v; simp [vadd_eq_add]; ring⟩
  have h := (convexOn_zpow (𝕜 := ℝ) (-1)).comp_affineMap g
  have hpre : g ⁻¹' Ioi 0 = Iio x := by
    ext s; simp [g]
  rw [hpre] at h
  refine h.congr ?_
  intro s _
  simp [g, zpow_neg]

/-- A crossed (u-channel) pole term `s ↦ 1/(x - (κ - s))` is convex on `κ - s < x`. -/
theorem convexOn_pole_left (x κ : ℝ) :
    ConvexOn ℝ (Ioi (κ - x)) (fun s : ℝ => 1 / (x - (κ - s))) := by
  let g : ℝ →ᵃ[ℝ] ℝ := ⟨fun s => x - (κ - s), LinearMap.id, by
    intro p v; simp [vadd_eq_add]; ring⟩
  have h := (convexOn_zpow (𝕜 := ℝ) (-1)).comp_affineMap g
  have hpre : g ⁻¹' Ioi 0 = Ioi (κ - x) := by
    ext s; simp [g]; constructor <;> intro h <;> linarith
  rw [hpre] at h
  refine h.congr ?_
  intro s _
  simp [g, zpow_neg]

/-- L2 (discretised dispersion relation, no derivative hypothesis). A finite positive
combination of s-channel and crossed u-channel poles, all above threshold `s₀`, plus any
linear subtraction polynomial `c₀ + c₁ s`, is convex in `s` on the interval where both
`s < s₀` and `κ - s < s₀` (κ = 4m² - t). This is "positive spectral weights ⇒ positive
curvature", the finite-sum version of L1. -/
theorem convexOn_discrete_dispersion {ι : Type*} (S : Finset ι) (w xs : ι → ℝ)
    (hw : ∀ i ∈ S, 0 ≤ w i) (s₀ κ c₀ c₁ : ℝ) (hx : ∀ i ∈ S, s₀ ≤ xs i) :
    ConvexOn ℝ (Ioo (κ - s₀) s₀)
      (fun s => c₀ + c₁ * s + ∑ i ∈ S, w i * (1 / (xs i - s) + 1 / (xs i - (κ - s)))) := by
  classical
  have hconv : Convex ℝ (Ioo (κ - s₀) s₀) := convex_Ioo _ _
  have hlin : ConvexOn ℝ (Ioo (κ - s₀) s₀) (fun s : ℝ => c₀ + c₁ * s) :=
    (LinearMap.convexOn (c₁ • LinearMap.id) hconv).add_const c₀ |>.congr
      (fun s _ => by simp [add_comm])
  have hsum : ConvexOn ℝ (Ioo (κ - s₀) s₀)
      (fun s => ∑ i ∈ S, w i * (1 / (xs i - s) + 1 / (xs i - (κ - s)))) := by
    induction S using Finset.induction_on with
    | empty => simpa using convexOn_const (0 : ℝ) hconv
    | insert a S ha ih =>
      have hwa := hw a (Finset.mem_insert_self a S)
      have hxa := hx a (Finset.mem_insert_self a S)
      have ih' := ih (fun i hi => hw i (Finset.mem_insert_of_mem hi))
        (fun i hi => hx i (Finset.mem_insert_of_mem hi))
      have hR : ConvexOn ℝ (Ioo (κ - s₀) s₀) (fun s : ℝ => 1 / (xs a - s)) :=
        (convexOn_pole_right (xs a)).subset
          (fun s hs => by simp only [mem_Iio]; exact lt_of_lt_of_le hs.2 hxa) hconv
      have hL : ConvexOn ℝ (Ioo (κ - s₀) s₀) (fun s : ℝ => 1 / (xs a - (κ - s))) :=
        (convexOn_pole_left (xs a) κ).subset
          (fun s hs => by simp only [mem_Ioi]; linarith [hs.1]) hconv
      have hterm := (hR.add hL).smul hwa
      have := hterm.add ih'
      refine this.congr ?_
      intro s _
      simp [Finset.sum_insert ha, smul_eq_mul]
  refine (hlin.add hsum).congr ?_
  intro s _
  simp only [Pi.add_apply]

/-- L3 (kernel calculus). The first and second derivatives of a pole term:
d/ds (x - s)⁻¹ = (x - s)⁻² and d²/ds² (x - s)⁻¹ = 2 (x - s)⁻³, for s ≠ x. -/
theorem hasDerivAt_pole (x s : ℝ) (h : s ≠ x) :
    HasDerivAt (fun s : ℝ => (x - s)⁻¹) (((x - s) ^ 2)⁻¹) s := by
  have hne : x - s ≠ 0 := sub_ne_zero.mpr (Ne.symm h)
  have h1 : HasDerivAt (fun s : ℝ => x - s) (-1) s := by
    simpa using (hasDerivAt_id s).const_sub x
  convert h1.inv hne using 1
  field_simp

/-- Derivative of `s ↦ ((x − s)²)⁻¹` at `s ≠ x` is `2 ((x − s)³)⁻¹`. -/
theorem hasDerivAt_pole_deriv (x s : ℝ) (h : s ≠ x) :
    HasDerivAt (fun s : ℝ => ((x - s) ^ 2)⁻¹) (2 * ((x - s) ^ 3)⁻¹) s := by
  have hne : x - s ≠ 0 := sub_ne_zero.mpr (Ne.symm h)
  have h0 : HasDerivAt (fun s : ℝ => x - s) (-1) s := by
    simpa using (hasDerivAt_id s).const_sub x
  have h1 : HasDerivAt (fun s : ℝ => (x - s) ^ 2) (↑(2:ℕ) * (x - s) ^ (2 - 1) * (-1)) s :=
    h0.fun_pow 2
  convert h1.inv (pow_ne_zero 2 hne) using 1
  field_simp
  norm_num

/-- Second derivative of `s ↦ (x − s)⁻¹` at `s ≠ x` is `2 ((x − s)³)⁻¹`. -/
theorem deriv2_pole (x s : ℝ) (h : s ≠ x) :
    deriv (deriv fun s : ℝ => (x - s)⁻¹) s = 2 * ((x - s) ^ 3)⁻¹ := by
  have hev : deriv (fun s : ℝ => (x - s)⁻¹) =ᶠ[nhds s] fun s => ((x - s) ^ 2)⁻¹ := by
    filter_upwards [isOpen_ne.mem_nhds h] with y hy
    exact (hasDerivAt_pole x y hy).deriv
  rw [hev.deriv_eq]
  exact (hasDerivAt_pole_deriv x s h).deriv

end PositiveGeometryEmergentSpaceTime.Dispersion
