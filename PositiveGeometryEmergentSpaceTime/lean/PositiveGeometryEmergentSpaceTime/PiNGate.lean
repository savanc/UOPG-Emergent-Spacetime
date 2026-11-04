/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-7 gate: on the would-be hidden-zero line s = M² + m² (πN, m = Mπ), with s + t + u = 2M² + 2m²:
(i) the u-channel nucleon pole M² - u vanishes at t = m² (the pole crosses the line);
(ii) the LO pseudovector-Born + WT amplitude D^{3/2} at t = 0 equals A⁺ = g_A² M / F² ≠ 0.
-/

namespace PositiveGeometryEmergentSpaceTime.PiNGate

/-- Arithmetic: `M² − (2M² + 2m² − (M² + m²) − t) = t − m²`. -/
theorem u_pole_on_line (M m t : ℝ) : M^2 - (2*M^2 + 2*m^2 - (M^2 + m^2) - t) = t - m^2 := by ring

/-- Arithmetic: `M² − (M² + m²) = −m²`. -/
theorem s_pole_offset (M m : ℝ) : M^2 - (M^2 + m^2) = -m^2 := by ring

/-- At t = 0, ν = 0 on the line, so D = A⁺ = (g_A M/F)²/M. -/
theorem D_at_t0 (M F gA : ℝ) (hM : 0 < M) (hF : 0 < F) (hg : gA ≠ 0) :
    (gA*M/F)^2 / M ≠ 0 := by
  have : gA*M/F ≠ 0 := div_ne_zero (mul_ne_zero hg hM.ne') hF.ne'
  exact div_ne_zero (pow_ne_zero 2 this) hM.ne'

end PositiveGeometryEmergentSpaceTime.PiNGate
