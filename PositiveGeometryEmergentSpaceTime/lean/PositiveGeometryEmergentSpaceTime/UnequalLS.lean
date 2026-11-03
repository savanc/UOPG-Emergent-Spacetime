/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.HadronKinematics

/-!
KL-1: unequal-mass Lovelace–Shapiro πK amplitude, intercepts fixed by the hidden-zero line.
a_ρ(t) = 1/2 + a (t - mπ²), a_K(u) = 1/2 + a (u - m_K²). Dual zero: a_ρ(t) + a_K(u) = 1.

Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/

namespace PositiveGeometryEmergentSpaceTime.UnequalLS
open PositiveGeometryEmergentSpaceTime.HadronKinematics

/-- The dual zero line of the KKY/Lovelace πK amplitude is exactly the CGW/MR-4 hidden-zero line s =
  mπ² + m_K². -/
theorem zero_line (a m_pi2 m_K2 s t u : ℝ) (ha : a ≠ 0) (hstu : s + t + u = stuSumPiK m_pi2 m_K2)
    (hz : (1/2 + a * (t - m_pi2)) + (1/2 + a * (u - m_K2)) = 1) : s = sigmaPiK m_pi2 m_K2 := by
  simp only [stuSumPiK, sigmaPiK] at hstu ⊢
  have h1 : a * (t + u - m_pi2 - m_K2) = 0 := by linarith
  have h2 : t + u - m_pi2 - m_K2 = 0 := by
    rcases mul_eq_zero.mp h1 with h | h
    · exact absurd h ha
    · exact h
  linarith

/-- Converse: on the hidden-zero line the dual zero condition holds. -/
theorem zero_line_conv (a m_pi2 m_K2 s t u : ℝ) (hstu : s + t + u = stuSumPiK m_pi2 m_K2)
    (hs : s = sigmaPiK m_pi2 m_K2) :
    (1/2 + a * (t - m_pi2)) + (1/2 + a * (u - m_K2)) = 1 := by
  simp only [stuSumPiK, sigmaPiK] at hstu hs
  have : u = m_pi2 + m_K2 - t := by linarith
  subst this; ring

/-- Spin-J pole of the K* trajectory: a_K(m²) = J ↔ m² = m_K² + (2J-1)/(2a). -/
theorem mass_formula (a m_K2 m2 J : ℝ) (ha : a ≠ 0) :
    1/2 + a * (m2 - m_K2) = J ↔ m2 = m_K2 + (2*J - 1) / (2*a) := by
  constructor
  · intro h; field_simp; linarith
  · intro h; rw [h]; field_simp; ring

/-- With the slope fixed by the ρ (a_ρ(mρ²) = 1), the J = 1 pole gives m_K*² - m_K² = mρ² - mπ²
(Ademollo–Veneziano–Weinberg / Mandelstam relation; CITED prior art). -/
theorem kstar_relation (m_pi2 m_rho2 m_K2 m2 : ℝ) (hne : m_rho2 - m_pi2 ≠ 0)
    (h : 1/2 + (1 / (2*(m_rho2 - m_pi2))) * (m2 - m_K2) = 1) : m2 - m_K2 = m_rho2 - m_pi2 := by
  field_simp at h; linarith

/-- Level spacing is universal: m_{J+1}² - m_J² = 1/a, the same as on the ρ trajectory. -/
theorem spacing (a m_K2 J : ℝ) (ha : a ≠ 0) :
    (m_K2 + (2*(J+1) - 1)/(2*a)) - (m_K2 + (2*J - 1)/(2*a)) = 1/a := by
  field_simp; ring

/-- Pochhammer form of the residue factor used in scripts/kl1_theory.py (J = 3 instance). -/
theorem poch3 (z : ℝ) (hz : ∀ n : ℕ, z - 3 ≠ -n) :
    Real.Gamma z = (z-1)*(z-2)*(z-3) * Real.Gamma (z - 3) := by
  have h3 : z - 3 ≠ 0 := by simpa using hz 0
  have h2 : z - 2 ≠ 0 := by intro h; exact hz 1 (by push_cast; linarith)
  have h1 : z - 1 ≠ 0 := by intro h; exact hz 2 (by push_cast; linarith)
  have e1 := Real.Gamma_add_one h3
  have e2 := Real.Gamma_add_one h2
  have e3 := Real.Gamma_add_one h1
  have : z - 3 + 1 = z - 2 := by ring
  have : z - 2 + 1 = z - 1 := by ring
  have : z - 1 + 1 = z := by ring
  simp_all only [sub_add_cancel]
  ring

end PositiveGeometryEmergentSpaceTime.UnequalLS
