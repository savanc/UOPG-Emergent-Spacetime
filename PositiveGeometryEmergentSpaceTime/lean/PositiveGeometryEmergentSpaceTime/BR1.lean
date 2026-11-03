/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.MassShift
import PositiveGeometryEmergentSpaceTime.UnequalLS
import PositiveGeometryEmergentSpaceTime.HadronKinematics
/-!
# BR-1: KKY dual zero line (UnequalLS, credited KL-LAT) ↔ δ-shift NLSM zero (MassShift) (2026-10-14)
Ordering (1234), legs 2, 4 = π, K; planar variables X13 = s12, X24 = s23; s12 + s23 + s13 = 2(mπ² + m_K²).
ASSUMPTION (not derived here): offsets fixed by the on-shell boundary values, μ13 + μ24 = −(m2² + m4²) =
−(mπ² + m_K²) — the unequal-mass extension of CGW's uniform prescription (`mshift4_uniform`).
Under it the δ-shift limit is exactly s13 − (mπ² + m_K²), so its zero is the KKY/CGW line.

Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/
namespace PositiveGeometryEmergentSpaceTime.BR1
open Filter Topology PositiveGeometryEmergentSpaceTime.NLSM PositiveGeometryEmergentSpaceTime.HadronKinematics

/-- δ-shift limit with on-shell boundary offsets equals s13 − (mπ² + m_K²). -/
theorem limit_onshell (s12 s23 s13 m_pi2 m_K2 μ13 μ24 : ℝ)
    (hsum : s12 + s23 + s13 = stuSumPiK m_pi2 m_K2) (hμ : μ13 + μ24 = -(sigmaPiK m_pi2 m_K2)) :
    Tendsto (fun δ : ℝ => δ ^ 2 * A4 (s12 + μ13 - δ) (s23 + μ24 + δ)) atTop
      (𝓝 (s13 - sigmaPiK m_pi2 m_K2)) := by
  simp only [stuSumPiK, sigmaPiK] at hsum hμ ⊢
  have h := PositiveGeometryEmergentSpaceTime.MassShift.mshift4_limit s12 s23 μ13 μ24
  have e : -(s12 + s23 + μ13 + μ24) = s13 - (m_pi2 + m_K2) := by linarith
  rwa [e] at h

/-- The limit vanishes iff the KKY dual zero condition holds (slope a ≠ 0). -/
theorem limit_zero_iff_KKY (a s12 s23 s13 m_pi2 m_K2 : ℝ) (ha : a ≠ 0)
    (hsum : s12 + s23 + s13 = stuSumPiK m_pi2 m_K2) :
    s13 - sigmaPiK m_pi2 m_K2 = 0 ↔
      (1/2 + a * (s12 - m_pi2)) + (1/2 + a * (s23 - m_K2)) = 1 := by
  have hstu : s13 + s12 + s23 = stuSumPiK m_pi2 m_K2 := by
    simpa [stuSumPiK, sigmaPiK, add_comm, add_left_comm, add_assoc] using hsum
  constructor
  · intro h
    have hs : s13 = sigmaPiK m_pi2 m_K2 := by
      simp only [sigmaPiK] at h ⊢; linarith
    exact PositiveGeometryEmergentSpaceTime.UnequalLS.zero_line_conv a m_pi2 m_K2 s13 s12 s23 hstu hs
  · intro h
    have hz := PositiveGeometryEmergentSpaceTime.UnequalLS.zero_line a m_pi2 m_K2 s13 s12 s23 ha hstu h
    simp only [sigmaPiK] at hz ⊢; linarith

/-- Non-vacuity witness: all hypotheses satisfiable on the zero line (mπ² = 1, m_K² = 3, a = 1). -/
theorem br1_witness : ∃ s12 s23 s13 : ℝ, s12 + s23 + s13 = 2 * ((1:ℝ) + 3) ∧
    s13 - ((1:ℝ) + 3) = 0 ∧ (1/2 + 1 * (s12 - 1)) + (1/2 + 1 * (s23 - 3)) = (1:ℝ) :=
  ⟨2, 2, 4, by norm_num, by norm_num, by norm_num⟩

end PositiveGeometryEmergentSpaceTime.BR1
