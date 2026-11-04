/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-! GB-1a (2026-10-13, AutoResearch): exact squared mass ratios of the registered closed-string glueball models. -/
namespace PositiveGeometryEmergentSpaceTime.GB1a
/-- Model A (Nambu–Goto, D=4): m² ∝ N − (D−2)/24. -/
noncomputable def mA2 (D N : ℝ) : ℝ := N - (D - 2) / 24
/-- Model A (Nambu–Goto, D = 4): `mA2 4 2 / mA2 4 1 = 23/11`. -/
theorem modelA_4_over_2 : mA2 4 2 / mA2 4 1 = 23 / 11 := by unfold mA2; norm_num
/-- Model A (Nambu–Goto, D = 4): `mA2 4 3 / mA2 4 1 = 35/11`. -/
theorem modelA_6_over_2 : mA2 4 3 / mA2 4 1 = 35 / 11 := by unfold mA2; norm_num
/-- Arithmetic: `(4 − 2)/24 = 1/12` (the D = 4 Nambu–Goto intercept). -/
theorem modelA_intercept : (4 - 2 : ℝ) / 24 = 1 / 12 := by norm_num
/-- Model B (LS-anchored): closed intercept 2α₀ with α₀ = 1/2; m² ∝ J − 2α₀. -/
noncomputable def mB2 (α₀ J : ℝ) : ℝ := J - 2 * α₀
/-- Model B (LS-anchored, α₀ = ½): `mB2 ½ 4 / mB2 ½ 2 = 3`. -/
theorem modelB_4_over_2 : mB2 (1/2) 4 / mB2 (1/2) 2 = 3 := by unfold mB2; norm_num
/-- Model B (LS-anchored, α₀ = ½): `mB2 ½ 6 / mB2 ½ 2 = 5`. -/
theorem modelB_6_over_2 : mB2 (1/2) 6 / mB2 (1/2) 2 = 5 := by unfold mB2; norm_num
/-- Ratios are unit-free (σ cancels). -/
theorem ratio_unit_free (σ x y : ℝ) (hσ : σ ≠ 0) : (σ * x) / (σ * y) = x / y :=
  mul_div_mul_left _ _ hσ
end PositiveGeometryEmergentSpaceTime.GB1a
