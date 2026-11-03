/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — RG-IR-1: sanity theorems and blind-vs-original comparison.
Original: `PositiveGeometryEmergentSpaceTime.RgIr1`. Blind: `PositiveGeometryEmergentSpaceTime.Alignment.RgIr1Blind`. The original is not edited.
Gap found (see notes/alignment/PILOT-2026-10-31.md): the original has no derivative or flow
object; `u_flow_affine` is the pointwise chain-rule algebra, and the affine UV→IR map used by
`affine_width` is assumed. `affine_time_map` below supplies that missing step.
-/
import PositiveGeometryEmergentSpaceTime.RgIr1
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.RgIr1Blind

namespace PositiveGeometryEmergentSpaceTime.Alignment.RgIr1Sanity
open PositiveGeometryEmergentSpaceTime.RgIr1

/-! ## 1. Blind claims, proved -/

theorem claim_linearises : RgIr1Blind.ClaimLinearises := by
  intro y G a k t hk hy hd
  have h2 := hd.pow 2
  have hinv := h2.inv (pow_ne_zero 2 hy)
  have hfun : (fun s => 1 / y s ^ 2) = fun s => (y s ^ 2)⁻¹ := by funext s; simp
  rw [hfun]
  convert hinv using 1
  simp only [Pi.pow_apply]
  field_simp
  ring

theorem claim_affine : RgIr1Blind.ClaimAffine := by
  intro u₁ u₂ α β t d₁ d₂ h1 h2 e1 e2
  have := h1.sub h2
  convert this using 1
  rw [e1, e2]; ring

theorem claim_width : RgIr1Blind.ClaimWidth := by
  intro A B lo hi _ _; exact affine_width A B lo hi

theorem claim_qcd : RgIr1Blind.ClaimQcdExponent := by
  refine ⟨qcd_sensitivity_exponent.1, ?_⟩
  rw [qcd_sensitivity_exponent.1]; norm_num

/-! ## 2. Comparison with the original -/

/-- The original `u_flow_affine` is exactly the derivative value in the blind calculus claim:
for y' = y κ (a y² − G), (1/y²)' = 2κ(G/y² − a). -/
theorem linearises_via_original (y G : ℝ → ℝ) (κ a t : ℝ) (hy : y t ≠ 0)
    (hd : HasDerivAt y (y t * κ * (a * y t ^ 2 - G t)) t) :
    HasDerivAt (fun s => 1 / y s ^ 2) (2 * κ * (G t / y t ^ 2 - a)) t := by
  have h2 := hd.pow 2
  have hinv := h2.inv (pow_ne_zero 2 hy)
  have hfun : (fun s => 1 / y s ^ 2) = fun s => (y s ^ 2)⁻¹ := by funext s; simp
  rw [hfun, ← u_flow_affine (y t) (G t) κ a hy]
  convert hinv using 1
  simp only [Pi.pow_apply]
  field_simp
  ring

/-- Blind width claim ⇐ original (the original needs neither `0 < A` nor `lo ≤ hi`). -/
theorem width_iff : RgIr1Blind.ClaimWidth ↔
    ∀ S A u0 u1 : ℝ, (S * u1 + A) - (S * u0 + A) = S * (u1 - u0) :=
  ⟨fun _ => affine_width, fun _ => claim_width⟩

/-- Blind QCD claim ↔ original `qcd_sensitivity_exponent` (both are closed numeric facts). -/
theorem qcd_iff : RgIr1Blind.ClaimQcdExponent ↔ ((-(8 : ℚ) / (-7)) - 1 = 1 / 7 ∧ (0 : ℚ) < 1 / 7) :=
  ⟨fun _ => qcd_sensitivity_exponent, fun _ => claim_qcd⟩

/-- The step the original assumes: for a linear flow u' = α(t) u + β(t) on ℝ (α with an
antiderivative A), any two solutions satisfy u₁(t) − u₂(t) = e^{A(t)−A(0)} (u₁(0) − u₂(0)). -/
theorem affine_time_map (u₁ u₂ α β A : ℝ → ℝ)
    (hA : ∀ s, HasDerivAt A (α s) s)
    (h1 : ∀ s, HasDerivAt u₁ (α s * u₁ s + β s) s)
    (h2 : ∀ s, HasDerivAt u₂ (α s * u₂ s + β s) s) (t : ℝ) :
    u₁ t - u₂ t = Real.exp (A t - A 0) * (u₁ 0 - u₂ 0) := by
  set f : ℝ → ℝ := fun s => (u₁ s - u₂ s) * Real.exp (-A s) with hfdef
  have hf : ∀ s, HasDerivAt f 0 s := by
    intro s
    have hw := (h1 s).sub (h2 s)
    have he := ((hA s).neg).exp
    convert hw.mul he using 1
    simp only [Pi.neg_apply, Pi.sub_apply]
    ring
  have hconst : f t = f 0 :=
    is_const_of_deriv_eq_zero (fun s => (hf s).differentiableAt) (fun s => (hf s).deriv) t 0
  simp only [hfdef] at hconst
  have e1 : Real.exp (-A t) * Real.exp (A t) = 1 := by rw [← Real.exp_add]; simp
  have e2 : Real.exp (A t - A 0) = Real.exp (A t) * Real.exp (-A 0) := by
    rw [sub_eq_add_neg, Real.exp_add]
  calc u₁ t - u₂ t = (u₁ t - u₂ t) * Real.exp (-A t) * Real.exp (A t) := by
        rw [mul_assoc, e1, mul_one]
    _ = (u₁ 0 - u₂ 0) * Real.exp (-A 0) * Real.exp (A t) := by rw [hconst]
    _ = Real.exp (A t - A 0) * (u₁ 0 - u₂ 0) := by rw [e2]; ring

/-- Hence "u_IR = S u_UV + A" with S > 0: the hypothesis behind `affine_width`, now proved
for any linear flow (given one reference solution u₂). -/
theorem affine_UV_IR (u₂ α β A : ℝ → ℝ) (hA : ∀ s, HasDerivAt A (α s) s)
    (h2 : ∀ s, HasDerivAt u₂ (α s * u₂ s + β s) s) (t : ℝ) :
    ∃ S B : ℝ, 0 < S ∧ ∀ u : ℝ → ℝ, (∀ s, HasDerivAt u (α s * u s + β s) s) →
      u t = S * u 0 + B := by
  refine ⟨Real.exp (A t - A 0), u₂ t - Real.exp (A t - A 0) * u₂ 0, Real.exp_pos _, ?_⟩
  intro u hu
  have := affine_time_map u u₂ α β A hA hu h2 t
  linarith

/-! ## 3. Sanity: known values, planted wrong cases, non-vacuity -/

/-- Known value (one-loop QCD-only fixed ratio y²/g₃² = 2/9, textbook, not refetched). -/
theorem known_fixed_ratio : (9 / 2 : ℚ) * (2 / 9) - 1 = 0 := (qcd_ratio_fixed _).2 rfl

/-- Planted wrong substitution: with u = 1/y the flow is not affine in u. For a = 1, G = 0,
u' = −a/u + G u takes values −1, −1/2, −1/3 at u = 1, 2, 3: not collinear. -/
theorem planted_inverse_not_affine :
    let f : ℚ → ℚ := fun u => -1 / u + 0 * u
    f 2 - f 1 ≠ f 3 - f 2 := by
  norm_num

/-- Planted wrong sign: with b₃ = +7 (no asymptotic freedom) the exponent is negative. -/
theorem planted_wrong_b3 : (-(8 : ℚ) / 7) - 1 < 0 := by norm_num

/-- Non-vacuity of `claim_linearises`: the fixed point y ≡ 1, a = G = k = 1 meets the
hypotheses. -/
theorem nonvacuous_linearises :
    ∃ (y G : ℝ → ℝ) (a k t : ℝ), k ≠ 0 ∧ y t ≠ 0 ∧
      HasDerivAt y (y t * (a * y t ^ 2 - G t) / k) t :=
  ⟨fun _ => 1, fun _ => 1, 1, 1, 0, one_ne_zero, one_ne_zero, by
    simpa using hasDerivAt_const (0 : ℝ) (1 : ℝ)⟩

/-- Non-vacuity of `affine_contracts` at the run's S = 0.0768 (S is SIMULATED, RG-IR-1 v2). -/
theorem nonvacuous_contracts : 0 < (768 / 10000 : ℝ) * (1 - 0) ∧ (768 / 10000 : ℝ) * (1 - 0) < 1 - 0 :=
  affine_contracts _ 0 1 (by norm_num) (by norm_num) (by norm_num)

/-- Non-vacuity of `affine_UV_IR`: a constant-coefficient flow has a solution. -/
theorem nonvacuous_affine_UV_IR :
    ∀ s : ℝ, HasDerivAt (fun _ : ℝ => (1 : ℝ)) ((-1) * 1 + 1) s := by
  intro s; simpa using hasDerivAt_const s (1 : ℝ)

end PositiveGeometryEmergentSpaceTime.Alignment.RgIr1Sanity
