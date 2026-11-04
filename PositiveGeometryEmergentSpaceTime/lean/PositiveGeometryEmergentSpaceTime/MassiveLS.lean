/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
MR-3: the minimal massive Lovelace–Shapiro family, M(s,u) = -Γ(1-α_s)Γ(1-α_u)/Γ(1-α_s-α_u),
α(x) = α₀ + α' x.  Units m_ρ² = 1, r = m_π²/m_ρ².
Adler (Lovelace) zero at s = u = m_π²: 2α₀ + 2α' r = 1.  ρ on the leading trajectory: α₀ + α' = 1.
Level-n residue polynomial R_n(u) = ∏_{j<n}(α_u + j)/(n-1)!, with u = -(s-4r)(1-x)/2, x = cos θ.
Positivity (Albert–Rastelli 2203.11950 eq. 19): every Legendre coefficient of every R_n ≥ 0.
Result: the f₂-level (n = 2) J = 0 coefficient is r(2r-1)/(4(r-1)²), negative for 0 < r < 1/2,
so positivity inside this family forces r = 0 (the chiral limit).
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Legendre

namespace PositiveGeometryEmergentSpaceTime.MassiveLS
open PositiveGeometryEmergentSpaceTime.Legendre

/-- Regge slope α′ as a function of the chiral ratio `r` (units m_ρ² = 1).
Also known as: α′, α', alpha_prime, ap'; `r` is also known as m_π²/m_ρ². -/
noncomputable def ap (r : ℝ) : ℝ := 1 / (2 * (1 - r))
/-- Regge intercept α₀ as a function of the chiral ratio `r` (units m_ρ² = 1).
Also known as: α₀, alpha_0, Regge intercept. -/
noncomputable def a0 (r : ℝ) : ℝ := (1 - 2 * r) / (2 * (1 - r))
/-! Level decomps use shared `PositiveGeometryEmergentSpaceTime.Legendre.legendreP*`. -/

/-- The family solves both conditions for every r ≠ 1: m_π/m_ρ is not fixed by Adler + ρ-placement. -/
theorem adler_condition (r : ℝ) (hr : r ≠ 1) : 2 * a0 r + 2 * ap r * r = 1 := by
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  unfold a0 ap; field_simp; ring

/-- For `r ≠ 1`, `a0 r + ap r · 1 = 1`. -/
theorem rho_condition (r : ℝ) (hr : r ≠ 1) : a0 r + ap r * 1 = 1 := by
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  unfold a0 ap; field_simp; ring

/-- Level 1 (ρ, s = 1): R₁ = α_u decomposes as c₀ + c₁ P₁. -/
theorem level1_decomp (r x : ℝ) (hr : r ≠ 1) :
    a0 r + ap r * (-(1 - 4 * r) * (1 - x) / 2) =
      1 / (4 * (1 - r)) + (1 - 4 * r) / (4 * (1 - r)) * legendreP1 x := by
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  unfold a0 ap legendreP1; field_simp; ring

/-- Level-1 positivity holds exactly for r < 1/4 (m_ρ above the ππ threshold): no window beyond
  that. -/
theorem level1_positive (r : ℝ) (_h0 : 0 ≤ r) (h1 : r < 1 / 4) :
    0 < 1 / (4 * (1 - r)) ∧ 0 < (1 - 4 * r) / (4 * (1 - r)) := by
  constructor <;> apply div_pos <;> linarith

/-- Level 2 (f₂ level, s = 3 - 2r): R₂ = α_u(α_u+1) = c₀ + c₁P₁ + c₂P₂. -/
theorem level2_decomp (r x : ℝ) (hr : r ≠ 1) :
    let u := -((3 - 2 * r) - 4 * r) * (1 - x) / 2
    (a0 r + ap r * u) * (a0 r + ap r * u + 1) =
      r * (1 - 2 * r) * (-1) / (4 * (1 - r) ^ 2) + 3 * (1 - 2 * r) / (8 * (1 - r) ^ 2) * legendreP1 x
        + 3 * (1 - 2 * r) ^ 2 / (8 * (1 - r) ^ 2) * legendreP2 x := by
  intro u
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  simp only [u, a0, ap, legendreP1, legendreP2]; field_simp; ring

/-- The f₂-level scalar coefficient is strictly negative for every 0 < r < 1/2. -/
theorem level2_scalar_negative (r : ℝ) (h0 : 0 < r) (h1 : r < 1 / 2) :
    r * (1 - 2 * r) * (-1) / (4 * (1 - r) ^ 2) < 0 := by
  apply div_neg_of_neg_of_pos
  · nlinarith
  · have : 0 < 1 - r := by linarith
    positivity

/-- Positivity inside the minimal massive LS family forces the chiral limit r = 0. -/
theorem positivity_forces_chiral (r : ℝ) (h0 : 0 ≤ r) (h1 : r < 1 / 2)
    (hpos : 0 ≤ r * (1 - 2 * r) * (-1) / (4 * (1 - r) ^ 2)) : r = 0 := by
  rcases h0.lt_or_eq with h | h
  · exact absurd hpos (not_le.mpr (level2_scalar_negative r h h1))
  · exact h.symm

/-- Chiral-limit KSRF-type ratio (Albert–Rastelli normalisation eqs. 68, 92):
g₁₀ = λπα', J=1 ρ residue g²m² = λ c₁/α' with c₁ = 1/4, α' = 1/2, m = 1 ⇒ g̃ρ² = g²/(2 g₁₀) = 1/(2π).
KSRF (m_ρ² = 2g²f_π²) corresponds to g̃ρ² = 1/2. -/
theorem ksrf_ratio (lam : ℝ) (hl : lam ≠ 0) :
    (lam * (1 / 4) / (1 / 2)) / (2 * (lam * Real.pi * (1 / 2))) = 1 / (2 * Real.pi) := by
  have hp : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp; ring

/-- The LS ratio is below KSRF by exactly the factor π. -/
theorem ksrf_gap : (1 / 2 : ℝ) / (1 / (2 * Real.pi)) = Real.pi := by
  have hp : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp

end PositiveGeometryEmergentSpaceTime.MassiveLS
