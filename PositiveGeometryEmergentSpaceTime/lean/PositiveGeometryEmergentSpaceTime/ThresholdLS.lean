/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-! TH-1 kinematics: s-channel threshold variables for ππ (Mπ = 1) and λ-independence of ratios. -/
namespace PositiveGeometryEmergentSpaceTime.ThresholdLS

/-- s = 4(1+q²), t = -2q²(1-z), u = -2q²(1+z) satisfy s+t+u = 4 -/
theorem stu_sum (q2 z : ℝ) : 4*(1+q2) + (-2*q2*(1-z)) + (-2*q2*(1+z)) = 4 := by ring

/-- threshold ratios are independent of the overall normalisation λ -/
theorem ratio_lambda_free (lam a b : ℝ) (hl : lam ≠ 0) (ha : a ≠ 0) : (lam*b)/(lam*a) = b/a := by
  field_simp

/-- at threshold (q² = 0) t = u = 0 for every z, so a_ℓ comes only from the q^{2ℓ} Taylor term -/
theorem t_at_threshold (z : ℝ) : -2*(0:ℝ)*(1-z) = 0 := by ring

end PositiveGeometryEmergentSpaceTime.ThresholdLS
