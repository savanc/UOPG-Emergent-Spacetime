/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
FT-3 gate. At the 3→3 (and 2→4) threshold every meson is at rest, so each Gram entry is
p_a·p_b = ± m_a m_b. The CGW/FT-2 zero locus is p_a·p_b = 0, so the threshold point sits a full
m_a m_b away: the relative distance |p_a·p_b|/(m_a m_b) equals 1, i.e. there is no small
parameter in which a near-zero (splitting) expansion could be controlled at threshold.
-/

namespace PositiveGeometryEmergentSpaceTime.FT3Gate

/-- Audit 2026-10-13: the equation part is a tautology (x − 0 = x); the content is `0 < m₁ m₂`.
At threshold (E = m, zero three-momentum) the same-side dot product is m₁ m₂ > 0. -/
theorem threshold_dot_same (m1 m2 : ℝ) (h1 : 0 < m1) (h2 : 0 < m2) :
    m1 * m2 - 0 = m1 * m2 ∧ 0 < m1 * m2 - 0 := by
  refine ⟨by ring, by simpa using mul_pos h1 h2⟩

/-- Relative distance of the threshold point from the zero locus is exactly 1 (no small parameter). -/
theorem threshold_relative_distance (m1 m2 : ℝ) (h1 : 0 < m1) (h2 : 0 < m2) :
    |(m1 * m2)| / (m1 * m2) = 1 ∧ |(-(m1 * m2))| / (m1 * m2) = 1 := by
  have hp : 0 < m1 * m2 := mul_pos h1 h2
  refine ⟨?_, ?_⟩
  · rw [abs_of_pos hp]; exact div_self hp.ne'
  · rw [abs_neg, abs_of_pos hp]; exact div_self hp.ne'

end PositiveGeometryEmergentSpaceTime.FT3Gate
