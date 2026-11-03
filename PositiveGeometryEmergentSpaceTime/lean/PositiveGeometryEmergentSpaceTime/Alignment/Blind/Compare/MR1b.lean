/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.LSResidue
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Mr1bBlind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: MR-1b (LS residues at ρ₃, f₄)

The blind `residue N` is derived from the Γ-ratio of the LS amplitude. The original
`PositiveGeometryEmergentSpaceTime.LSResidue.rho3_residue` / `f4_residue` decompose hand-chosen polynomials.
Result: at N = 3, 4 the original polynomial is exactly the NEGATIVE of the blind (literal) residue;
at N = 1 they agree. The Legendre coefficients therefore agree in magnitude and the coupling
ratios 5/16, 49/240 agree exactly.
VERDICT: DIFFERENT (sign convention) — magnitudes / ratios EQUIV; the blind file additionally
derives the residue from Γ (`gamma_ratio`), the original hand-transcribes it.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR1b

open PositiveGeometryEmergentSpaceTime.Alignment.Mr1bBlind PositiveGeometryEmergentSpaceTime.Legendre

/-- ρ level: blind residue = original `1 + (x−1)/2`-type expression `1/2 + 1/2 x`. -/
theorem rho_agree (z : ℚ) : ((residue 1 z : ℚ) : ℝ) = 1 / 2 + 1 / 2 * legendreP1 (z : ℝ) := by
  rw [rho_residue]; simp [P0, P1, legendreP1]; ring

/-- ρ₃ level: original polynomial = − blind residue. -/
theorem rho3_neg (z : ℚ) :
    (let a : ℝ := 7 / 4 - 5 * (z : ℝ) / 4; (a - 1) * (a - 2) * (a - 3)) = -((residue 3 z : ℚ) : ℝ) := by
  rw [rho3_residue]; simp [P0, P1, P2, P3]; ring

/-- f₄ level: original polynomial = − blind residue. -/
theorem f4_neg (z : ℚ) :
    (let a : ℝ := 9 / 4 - 7 * (z : ℝ) / 4; -(1 / 3) * ((a - 1) * (a - 2) * (a - 3) * (a - 4)))
      = -((residue 4 z : ℚ) : ℝ) := by
  rw [f4_residue]; simp [P0, P1, P2, P3, P4]; ring

/-- The ratio theorems coincide numerically. -/
theorem ratios_agree :
    gSq (25 / 32) (mSq 3) / gSq (1 / 2) (mSq 1) = ((25 / 32 : ℚ) / 5) / (1 / 2) ∧
    gSq (343 / 480) (mSq 4) / gSq (1 / 2) (mSq 1) = ((343 / 480 : ℚ) / 7) / (1 / 2) := by
  rw [rho3_ratio, f4_ratio, PositiveGeometryEmergentSpaceTime.LSResidue.rho3_ratio, PositiveGeometryEmergentSpaceTime.LSResidue.f4_ratio]; simp

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR1b
