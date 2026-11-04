/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
MR-1: residue identities of the Lovelace–Shapiro amplitude at the ρ and f2 poles
(units m_ρ² = 1, α' = 1/2, a = 1/2 - y/2 with y = α'-scaled u).
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Legendre

namespace PositiveGeometryEmergentSpaceTime.LSResidue
open PositiveGeometryEmergentSpaceTime.Legendre

/-- Gamma recursion used at the f2 level: Γ(a) = (a-1)(a-2)Γ(a-2). -/
theorem gamma_two_step (a : ℝ) (h1 : a - 2 ≠ 0) (h2 : a - 2 ≠ -1) :
    Real.Gamma a = (a - 1) * (a - 2) * Real.Gamma (a - 2) := by
  have e1 : Real.Gamma (a - 2 + 1) = (a - 2) * Real.Gamma (a - 2) :=
    Real.Gamma_add_one (by simpa using h1)
  have e2 : Real.Gamma (a - 2 + 1 + 1) = (a - 2 + 1) * Real.Gamma (a - 2 + 1) :=
    Real.Gamma_add_one (by intro h; apply h2; linarith)
  have ha : a = a - 2 + 1 + 1 := by ring
  calc Real.Gamma a = Real.Gamma (a - 2 + 1 + 1) := by rw [← ha]
    _ = (a - 2 + 1) * ((a - 2) * Real.Gamma (a - 2)) := by rw [e2, e1]
    _ = (a - 1) * (a - 2) * Real.Gamma (a - 2) := by ring

/-! Residues use shared `PositiveGeometryEmergentSpaceTime.Legendre.legendreP*`. -/

/-- ρ level: residue polynomial 1 + y with y = (x-1)/2 equals (1/2)(1 + legendreP1): J=1 coefficient
  1/2. -/
theorem rho_residue (x : ℝ) : 1 + (x - 1) / 2 = (1 / 2) + (1 / 2) * legendreP1 x := by
  unfold legendreP1; ring

/-- f2 level: residue (1+y)(3+y)/2 with y = 3(x-1)/2 equals (3/4)(legendreP2 + legendreP1), so the J=0 coefficient is 0
and the J=2 coefficient is 3/4. -/
theorem f2_residue (x : ℝ) :
    (1 + 3 * (x - 1) / 2) * (3 + 3 * (x - 1) / 2) / 2 = 0 + (3 / 4) * legendreP1 x + (3 / 4) * legendreP2 x := by
  unfold legendreP1 legendreP2; ring

/-- On-shell couplings (AHRV 2.12: J-coefficient = -g² m²): g_ρ² = -1/2 (m²=1), g_f2² = -(3/4)/3.
Their ratio is 1/2. -/
theorem coupling_ratio : ((3 / 4 : ℚ) / 3) / (1 / 2) = 1 / 2 := by norm_num

/-- Partial-wave conversion: (27/20)/√3 width ratio = κ · (1/2) · √3 with κ = 9/10 (the prereg's 1.8
  was a slip). -/
theorem kappa_value : (27 / 20 : ℝ) / Real.sqrt 3 = (9 / 10) * (1 / 2) * Real.sqrt 3 := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hpos : Real.sqrt 3 ≠ 0 := by positivity
  field_simp; nlinarith [h]


/-! MR-1b: next Regge levels (ρ3 at m² = 5, f4 at m² = 7; units m_ρ² = 1). -/

/-- ρ3 level: Γ(a)/Γ(a-3) = (a-1)(a-2)(a-3) with a = 7/4 - 5x/4; Legendre decomposition. -/
theorem rho3_residue (x : ℝ) :
    let a := 7 / 4 - 5 * x / 4;
    (a - 1) * (a - 2) * (a - 3) = -(5 / 32) * (1 + legendreP1 x) - (25 / 32) * (legendreP2 x + legendreP3 x) := by
  intro a; simp only [a, legendreP1, legendreP2, legendreP3]; ring

/-- f4 level: -(1/3)(a-1)(a-2)(a-3)(a-4) with a = 9/4 - 7x/4; Legendre decomposition. -/
theorem f4_residue (x : ℝ) :
    let a := 9 / 4 - 7 * x / 4;
    -(1 / 3) * ((a - 1) * (a - 2) * (a - 3) * (a - 4)) =
      -(7 / 180) - (91 / 240) * legendreP1 x - (49 / 144) * legendreP2 x - (343 / 480) * (legendreP3 x + legendreP4 x) := by
  intro a; simp only [a, legendreP1, legendreP2, legendreP3, legendreP4]; ring

/-- Couplings (J-coefficient = -g² m², hand-transcribed from `rho3_residue`/`f4_residue`; the
step "Legendre coefficient → coupling" is not mechanised here, only this arithmetic). Relative to g_ρ² = 1/2: ρ3 → 5/16, f4 → 49/240. -/
theorem rho3_ratio : ((25 / 32 : ℚ) / 5) / (1 / 2) = 5 / 16 := by norm_num
/-- Arithmetic: `(343/480)/7 / (1/2) = 49/240`. -/
theorem f4_ratio : ((343 / 480 : ℚ) / 7) / (1 / 2) = 49 / 240 := by norm_num

/-- Width-conversion constants κ ∝ c_I/(2J+1) (c₁ = 4, c₀ = 6), relative to ρ. -/
theorem kappa_rho3 : ((4 : ℚ) / 7) / (4 / 3) = 3 / 7 := by norm_num
/-- Arithmetic: `(6/9)/(4/3) = 1/2`. -/
theorem kappa_f4 : ((6 : ℚ) / 9) / (4 / 3) = 1 / 2 := by norm_num


/-! MR-1c: isospin-projected residues at the f2 level (m² = 3). Even-under-x↦-x part feeds I = 0
(s-channel I = 0 ∝ A(s,t)+A(s,u)); odd part feeds I = 1. -/

/-- f2-level residue polynomial F(x) = (1+y)(3+y)/2, y = 3(x-1)/2. -/
noncomputable def Ff2 (x : ℝ) : ℝ := (1 + 3 * (x - 1) / 2) * (3 + 3 * (x - 1) / 2) / 2

/-- I = 0 (even) channel at the f2 level: pure J = 2, the J = 0 (scalar) coefficient is exactly 0. -/
theorem f2_level_I0_scalar_zero (x : ℝ) : Ff2 x + Ff2 (-x) = 0 + (3 / 2) * legendreP2 x := by
  unfold Ff2 legendreP2; ring

/-- I = 1 (odd) channel at the f2 level: pure J = 1 daughter (ρ'-like), coefficient 3/2 ≠ 0. -/
theorem f2_level_I1_vector (x : ℝ) : Ff2 x - Ff2 (-x) = (3 / 2) * legendreP1 x := by
  unfold Ff2 legendreP1; ring

/-- Contrast: at the ρ level the I = 0 even part has a nonzero scalar (σ-like) coefficient. -/
theorem rho_level_I0_scalar_nonzero (x : ℝ) :
    (1 + (x - 1) / 2) + (1 + (-x - 1) / 2) = 1 := by ring

/-- Daughter ρ' coupling relative to ρ (J-coefficient/m², same normalisation as `coupling_ratio`). -/
theorem rho_daughter_ratio : ((3 / 4 : ℚ) / 3) / (1 / 2) = 1 / 2 := by norm_num

end PositiveGeometryEmergentSpaceTime.LSResidue
