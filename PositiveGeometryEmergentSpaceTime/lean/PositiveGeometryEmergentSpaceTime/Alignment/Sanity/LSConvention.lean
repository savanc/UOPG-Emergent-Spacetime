/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — MR-1b sanity theorems: mechanise the "Legendre coefficient → coupling"
step that `LSResidue.rho3_ratio` / `f4_ratio` transcribe by hand. Not part of `import PositiveGeometryEmergentSpaceTime`.
-/
import PositiveGeometryEmergentSpaceTime.LSResidue

/-!
# MR-1b: coefficient extraction and the coupling convention

* Coefficient extraction (tie): any Legendre expansion of the ρ, ρ₃, f₄ residue polynomials has the
  coefficients used in the paper (uniqueness; four or five evaluation points). So `25/32` and `343/480`
  are *derived*, not read off by hand.
* Convention `c_J = −g² m²` (AHRV eq. 2.12) as a function `gsq c m² = −c/m²`:
  `gsq` gives `g_ρ² = −1/2`, `g_ρ₃² = 5/32`, `g_f₄² = 49/480`. The paper's ratios `5/16`, `49/240`
  are the ratios of **magnitudes** `|c_J|/m²`; the literal signed ratio is `−5/16`, `−49/240`
  (finding recorded in SANITY-2026-11-03.md; wording only, numbers unchanged).
* Planted: the `(2J+1)`-normalised convention gives `15/112 ≠ 5/16` and `49/720 ≠ 49/240`, so it is rejected.
* Non-vacuity: the hypotheses of the extraction lemmas are met by `LSResidue.rho3_residue` / `f4_residue`.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LSConvention
open PositiveGeometryEmergentSpaceTime.Legendre PositiveGeometryEmergentSpaceTime.LSResidue

/-- ρ residue polynomial (units m_ρ² = 1). -/
noncomputable def resRho (x : ℝ) : ℝ := 1 + (x - 1) / 2
/-- ρ₃ residue polynomial. -/
noncomputable def resRho3 (x : ℝ) : ℝ :=
  (7 / 4 - 5 * x / 4 - 1) * (7 / 4 - 5 * x / 4 - 2) * (7 / 4 - 5 * x / 4 - 3)
/-- f₄ residue polynomial. -/
noncomputable def resF4 (x : ℝ) : ℝ :=
  -(1 / 3) * ((9 / 4 - 7 * x / 4 - 1) * (9 / 4 - 7 * x / 4 - 2) * (9 / 4 - 7 * x / 4 - 3) *
    (9 / 4 - 7 * x / 4 - 4))

/-- Uniqueness at the ρ level: the J = 1 coefficient is `1/2`. -/
theorem rho_coeff (c0 c1 : ℝ) (h : ∀ x, resRho x = c0 + c1 * legendreP1 x) : c0 = 1 / 2 ∧ c1 = 1 / 2 := by
  have h0 := h 0; have h1 := h 1
  simp only [resRho, legendreP1] at h0 h1
  constructor <;> linarith

/-- Uniqueness at the ρ₃ level: `c₃ = −25/32` (and the lower coefficients). -/
theorem rho3_coeff (c0 c1 c2 c3 : ℝ)
    (h : ∀ x, resRho3 x = c0 + c1 * legendreP1 x + c2 * legendreP2 x + c3 * legendreP3 x) :
    c0 = -5 / 32 ∧ c1 = -5 / 32 ∧ c2 = -25 / 32 ∧ c3 = -25 / 32 := by
  have h0 := h 0; have h1 := h 1; have h2 := h (-1); have h3 := h 2
  simp only [resRho3, legendreP1, legendreP2, legendreP3] at h0 h1 h2 h3
  norm_num at h0 h1 h2 h3
  refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith

/-- Uniqueness at the f₄ level: `c₄ = −343/480`. -/
theorem f4_coeff (c0 c1 c2 c3 c4 : ℝ)
    (h : ∀ x, resF4 x = c0 + c1 * legendreP1 x + c2 * legendreP2 x + c3 * legendreP3 x + c4 * legendreP4 x) :
    c4 = -343 / 480 ∧ c3 = -343 / 480 := by
  have h0 := h 0; have h1 := h 1; have h2 := h (-1); have h3 := h 2; have h4 := h (-2)
  simp only [resF4, legendreP1, legendreP2, legendreP3, legendreP4] at h0 h1 h2 h3 h4
  norm_num at h0 h1 h2 h3 h4
  constructor <;> linarith

/-- Non-vacuity: the extraction hypotheses hold (via the original residue theorems). -/
theorem rho3_hyp : ∀ x, resRho3 x = -(5 / 32) + -(5 / 32) * legendreP1 x + -(25 / 32) * legendreP2 x +
    -(25 / 32) * legendreP3 x := by
  intro x; have := rho3_residue x; simp only [resRho3] at this ⊢; rw [this]; ring

theorem f4_hyp : ∀ x, resF4 x = -(7 / 180) + -(91 / 240) * legendreP1 x + -(49 / 144) * legendreP2 x +
    -(343 / 480) * legendreP3 x + -(343 / 480) * legendreP4 x := by
  intro x; have := f4_residue x; simp only [resF4] at this ⊢; rw [this]; ring

/-- The AHRV convention `c_J = −g² m²`, solved for `g²`. -/
noncomputable def gsq (c m2 : ℝ) : ℝ := -c / m2

/-- Known values under the literal convention. -/
theorem gsq_values : gsq (1 / 2) 1 = -1 / 2 ∧ gsq (-25 / 32) 5 = 5 / 32 ∧ gsq (-343 / 480) 7 = 49 / 480 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num [gsq]

/-- **Tie.** Derived ratios: magnitudes give the paper's `5/16` and `49/240`; the literal signed ratios
are their negatives because `g_ρ² = −1/2` under `c_J = −g² m²`. -/
theorem ratios (c1 c3 c4 : ℝ) (hρ : c1 = 1 / 2) (h3 : c3 = -25 / 32) (h4 : c4 = -343 / 480) :
    |gsq c3 5| / |gsq c1 1| = 5 / 16 ∧ |gsq c4 7| / |gsq c1 1| = 49 / 240 ∧
    gsq c3 5 / gsq c1 1 = -5 / 16 ∧ gsq c4 7 / gsq c1 1 = -49 / 240 := by
  subst hρ h3 h4
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [gsq, abs_of_pos, abs_of_neg]

/-- End to end: from the residue polynomials alone, the magnitude ratio is `5/16`. -/
theorem rho3_ratio_derived : |gsq (-25 / 32) 5| / |gsq (1 / 2) 1| = 5 / 16 :=
  (ratios _ _ (-343 / 480) rfl rfl rfl).1

/-- Planted: the `(2J+1)` normalisation `g² = |c_J|/((2J+1) m²)` gives different ratios, rejected. -/
theorem planted_2J1 :
    ((25 / 32 : ℚ) / (7 * 5)) / ((1 / 2) / (3 * 1)) = 15 / 112 ∧ (15 / 112 : ℚ) ≠ 5 / 16 ∧
    ((343 / 480 : ℚ) / (9 * 7)) / ((1 / 2) / (3 * 1)) = 49 / 720 ∧ (49 / 720 : ℚ) ≠ 49 / 240 := by
  norm_num

/-- Planted: reading off the wrong Legendre coefficient (`c₂ = −25/32` is fine, but `c₁ = −5/32`) at ρ₃
gives `1/16`, not `5/16`. -/
theorem planted_wrong_J : |gsq (-5 / 32) 5| / |gsq (1 / 2) 1| = 1 / 16 := by
  norm_num [gsq, abs_of_pos]

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LSConvention
