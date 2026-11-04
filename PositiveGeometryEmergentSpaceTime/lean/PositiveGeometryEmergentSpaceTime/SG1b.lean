/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-! SG-1b (2026-10-13, AutoResearch): single-signed Casimir terms are monotone, so they cannot
stabilise the radius; sums of same-direction monotone terms stay monotone. -/
namespace PositiveGeometryEmergentSpaceTime.SG1b
open Real Set
/-- Casimir profile of a 5D field: casimirProfile(x) = (3 + 3x + x²) e^{-x}.

Also known as: f, Casimir profile (3+3x+x²)e^{−x}.
-/
noncomputable def casimirProfile : ℝ → ℝ := fun x => (3 + 3 * x + x ^ 2) * Real.exp (-x)

/-- Derivative of the Casimir profile: `d/dx [(3 + 3x + x²) e^{−x}] = −(x + x²) e^{−x}`. -/
theorem hasDerivAt_casimirProfile (x : ℝ) : HasDerivAt casimirProfile (-(x + x ^ 2) * Real.exp (-x)) x := by
  have h1 : HasDerivAt (fun x : ℝ => 3 + 3 * x + x ^ 2) (3 + 2 * x) x := by
    have := (((hasDerivAt_id' x).const_mul 3).const_add 3).add ((hasDerivAt_id' x).pow 2)
    convert this using 1; simp
  have h2 : HasDerivAt (fun x : ℝ => Real.exp (-x)) (-Real.exp (-x)) x := by
    simpa using (hasDerivAt_neg x).exp
  show HasDerivAt (fun x => (3 + 3 * x + x ^ 2) * Real.exp (-x)) _ x
  exact (h1.mul h2).congr_deriv (by ring)

/-- casimirProfile is antitone on x ≥ 0. -/
theorem casimirProfile_antitoneOn : AntitoneOn casimirProfile (Ici 0) := by
  apply antitoneOn_of_deriv_nonpos (convex_Ici 0)
  · exact fun x _ => (hasDerivAt_casimirProfile x).continuousAt.continuousWithinAt
  · exact fun x _ => (hasDerivAt_casimirProfile x).differentiableAt.differentiableWithinAt
  · intro x hx
    rw [interior_Ici] at hx
    rw [(hasDerivAt_casimirProfile x).deriv]
    have : 0 ≤ x + x ^ 2 := by have := le_of_lt (mem_Ioi.mp hx); positivity
    have := Real.exp_pos (-x)
    nlinarith

/-- A finite sum of antitone terms is antitone: no interior strict minimum can be created. -/
theorem sum_antitone {ι : Type*} (s : Finset ι) (g : ι → ℝ → ℝ) (S : Set ℝ)
    (h : ∀ i ∈ s, AntitoneOn (g i) S) : AntitoneOn (fun L => ∑ i ∈ s, g i L) S := by
  intro a ha b hb hab
  exact Finset.sum_le_sum fun i hi => h i hi ha hb hab

/-- Same for monotone (single-signed negative Casimir contributions). -/
theorem sum_monotone {ι : Type*} (s : Finset ι) (g : ι → ℝ → ℝ) (S : Set ℝ)
    (h : ∀ i ∈ s, MonotoneOn (g i) S) : MonotoneOn (fun L => ∑ i ∈ s, g i L) S := by
  intro a ha b hb hab
  exact Finset.sum_le_sum fun i hi => h i hi ha hb hab
end PositiveGeometryEmergentSpaceTime.SG1b
