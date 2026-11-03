/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.HadronKinematics

/-!
MR-4: πK hidden-zero line algebra. Σ = Mπ² + MK²; s + t + u = 2Σ.
On the line s = Σ: s - u = t, so ν = (s-u)/(4 m_K) = t/(4 m_K). LO F^{3/2} ∝ (Σ - s) vanishes there.
Line coefficients of the BDM subthreshold polynomial (τ = t/mπ², ν/mπ = κ τ).

Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/

namespace PositiveGeometryEmergentSpaceTime.PiKZero
open PositiveGeometryEmergentSpaceTime.HadronKinematics

/-- If `s + t + u = 2S` and `s = S`, then `s − u = t`. -/
theorem line_su (S s t u : ℝ) (hst : s + t + u = 2 * S) (hs : s = S) : s - u = t := by
  subst hs; linarith

/-- Same as `line_su` with S = Σ_πK (shared). -/
theorem line_su_piK (m_pi2 m_K2 s t u : ℝ)
    (hst : s + t + u = stuSumPiK m_pi2 m_K2) (hs : s = sigmaPiK m_pi2 m_K2) :
    s - u = t := by
  simpa [stuSumPiK, sigmaPiK] using line_su (sigmaPiK m_pi2 m_K2) s t u (by simpa [stuSumPiK,
      sigmaPiK] using hst) hs

/-- Arithmetic: `(S − S)/(2F²) = 0`. -/
theorem lo_zero_on_line (S F : ℝ) : (S - S) / (2 * F ^ 2) = 0 := by simp

/-- Arithmetic: `(Σ − Σ)/(2F²) = 0` with `Σ = m_π² + m_K²`. -/
theorem lo_zero_on_line_piK (m_pi2 m_K2 F : ℝ) :
    (sigmaPiK m_pi2 m_K2 - sigmaPiK m_pi2 m_K2) / (2 * F ^ 2) = 0 :=
  lo_zero_on_line (sigmaPiK m_pi2 m_K2) F

/-- Equal-mass limit: the line s = 2M² is p_π·p_K = 0 (s = m1²+m2²+2p1·p2). -/
theorem line_is_orthogonal (m1 m2 d : ℝ) : m1^2 + m2^2 + 2*d = m1^2 + m2^2 ↔ d = 0 := by
  constructor <;> intro h <;> linarith

/-- Polynomial ansatz `F⁺(τ, x) = C₀₀ + C₁₀τ + C₂₀τ² + C₃₀τ³ + C₀₁x² + C₁₁τx²`. -/
noncomputable def Fp (C00 C10 C20 C01 C11 C30 τ x : ℝ) : ℝ :=
  C00 + C10*τ + C20*τ^2 + C30*τ^3 + C01*x^2 + C11*τ*x^2
/-- Polynomial ansatz `F⁻(τ, x) = x(D₀₀ + D₁₀τ + D₂₀τ² + D₀₁x²)`. -/
noncomputable def Fm (D00 D10 D20 D01 τ x : ℝ) : ℝ := x * (D00 + D10*τ + D20*τ^2 + D01*x^2)

/-- F^{3/2} = F⁺ − F⁻ on the line x = κτ equals the cubic g0 + g1 τ + g2 τ² + g3 τ³. -/
theorem line_poly (C00 C10 C20 C01 C11 C30 D00 D10 D20 D01 κ τ : ℝ) :
    Fp C00 C10 C20 C01 C11 C30 τ (κ*τ) - Fm D00 D10 D20 D01 τ (κ*τ)
      = C00 + (C10 - κ*D00)*τ + (C20 + κ^2*C01 - κ*D10)*τ^2
        + (C30 + κ^2*C11 - κ*D20 - κ^3*D01)*τ^3 := by
  unfold Fp Fm; ring

end PositiveGeometryEmergentSpaceTime.PiKZero

namespace PositiveGeometryEmergentSpaceTime.PiKZero
open PositiveGeometryEmergentSpaceTime.HadronKinematics
/-- Cross-check with BDM/BKM NLO subthreshold formulas (CITED, hep-ph/0310283 §6): the line combinations
g1 = C⁺10 − κC⁻00 and g2 = C⁺20 + κ²C⁺01 − κC⁻10 (L-parts, units F⁴ = 1, κ = mπ/(4mK)) equal the
brute-force tree line coefficients ×4mπ², ×4mπ⁴. -/
theorem bdm_g1 (m_pi m_K L1 L3 L4 L5 : ℝ) (hK : m_K ≠ 0) :
    (4 * sigmaPiK (m_pi^2) (m_K^2) * m_pi^2 * (-(4*L1+L3)+2*L4) + 2*m_pi^4*L5) -
      (m_pi/(4*m_K))*(8*m_K*m_pi^3*L5)
      = 4*m_pi^2*(-(sigmaPiK (m_pi^2) (m_K^2))*(4*L1+L3-2*L4)) := by
  simp only [sigmaPiK]; field_simp; ring
/-- Exact algebraic identity for the quadratic coefficient (requires `m_K ≠ 0`): the stated
  combination equals `4m_π⁴(2L₁ + L₂ + L₃)`. -/
theorem bdm_g2 (m_pi m_K L1 L2 L3 : ℝ) (hK : m_K ≠ 0) :
    2*m_pi^4*(4*L1+L2+5/4*L3) + (m_pi/(4*m_K))^2*(8*m_K^2*m_pi^2*(4*L2+L3)) - (m_pi/(4*m_K))*(-4*m_K*m_pi^3*L3)
      = 4*m_pi^4*(2*L1+L2+L3) := by
  field_simp; ring
/-- Exact algebraic identity for the constant coefficient: the two stated forms agree. -/
theorem bdm_g0 (m_pi m_K L1 L3 L4 L5 L6 L8 : ℝ) :
    8*m_pi^2*m_K^2*(4*L1+L3-(4*L4+L5)+2*(L8+2*L6)) = 4*(2*m_K^2*m_pi^2*(4*L1+L3-4*L4-L5+4*L6+2*L8)) := by ring

end PositiveGeometryEmergentSpaceTime.PiKZero
