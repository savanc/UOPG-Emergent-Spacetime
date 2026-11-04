/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.HadronKinematics

/-! LAT-2 gate algebra: c.m. momentum on the πK zero line s = Σ = Mπ²+MK², and its position
relative to the nearest left-hand singularity q² = -Mπ² (circular cut at s = MK²-Mπ²).
Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/
namespace PositiveGeometryEmergentSpaceTime.LatticeGate
open PositiveGeometryEmergentSpaceTime.HadronKinematics

/-- πK c.m. momentum² — alias of shared `HadronKinematics.q2PiK`.

Also known as: q2 (prior local def). -/
noncomputable abbrev q2 := q2PiK

/-- On the line `s = Σ` (nonzero), `q² = −m_π² m_K² / Σ`. -/
theorem q2_on_line (m_pi m_K : ℝ) (h : sigmaPiK (m_pi^2) (m_K^2) ≠ 0) :
    q2 m_pi m_K (sigmaPiK (m_pi^2) (m_K^2)) =
      -(m_pi^2 * m_K^2) / sigmaPiK (m_pi^2) (m_K^2) :=
  q2PiK_on_line m_pi m_K h

/-- At `s = m_K² − m_π²` (nonzero), `q² = −m_π²`. -/
theorem q2_at_circle (m_pi m_K : ℝ) (h : m_K^2 - m_pi^2 ≠ 0) :
    q2 m_pi m_K (m_K^2 - m_pi^2) = -m_pi^2 := by
  unfold q2 q2PiK; field_simp; ring

/-- the line lies strictly inside the ERE convergence disc |q²| < Mπ², with ratio MK²/Σ < 1 -/
theorem inside_disc (m_pi m_K : ℝ) (hp : 0 < m_pi) (hK : 0 < m_K) :
    m_pi^2 * m_K^2 / sigmaPiK (m_pi^2) (m_K^2) < m_pi^2 := by
  simp only [sigmaPiK]
  rw [div_lt_iff₀ (by positivity)]; nlinarith [pow_pos hp 2, pow_pos hK 2,
      mul_pos (pow_pos hp 2) (pow_pos hp 2)]

/-- circularity: an Adler-form s-wave with zero fixed at E*² = z²Σ, z² = 1, vanishes on the line. -/
theorem adler_fixed_on_line (S N : ℝ) : (S - 1 * S) * N = 0 := by ring

end PositiveGeometryEmergentSpaceTime.LatticeGate

namespace PositiveGeometryEmergentSpaceTime.LatticeGate
/-! LAT-3: ππ zero point P = (s,t,u) = (M², M², 2M²) in s-channel partial-wave variables. -/

/-- equal-mass c.m. momentum q² = s/4 − M² at s = M² -/
theorem pipi_q2_at_P (M : ℝ) : M^2 / 4 - M^2 = -(3/4) * M^2 := by ring

/-- ratio to the left-hand branch point (s = 0 ↔ q² = −M²) is 3/4 < 1 -/
theorem pipi_inside_disc (M : ℝ) (hM : 0 < M) : (3/4) * M^2 < M^2 := by nlinarith [pow_pos hM 2]

/-- scattering angle at P: cos θ = 1 + 2t/(s − 4M²) = 1/3, inside the physical interval -/
theorem pipi_cos_at_P (M : ℝ) (hM : M ≠ 0) : 1 + 2 * M^2 / (M^2 - 4 * M^2) = 1/3 := by
  have : M^2 - 4*M^2 = -3*M^2 := by ring
  rw [this]; field_simp; ring
end PositiveGeometryEmergentSpaceTime.LatticeGate
