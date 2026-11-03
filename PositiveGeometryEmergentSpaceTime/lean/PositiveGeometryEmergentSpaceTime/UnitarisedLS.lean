/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
UL-1 gate: elastic K-matrix / IAM unitarisation of the Lovelace–Shapiro partial waves.
Real-variable model: K = LS tree partial wave (real below inelastic threshold), σ = phase space.
K-matrix: t = K/(1 - iσK), so Re t = K/(1+σ²K²).  IAM: t = t2²/(t2 - t4).
-/

namespace PositiveGeometryEmergentSpaceTime.UnitarisedLS

/-- Real part of the unitarised K-matrix amplitude: `K / (1 + σ² K²)`. -/
noncomputable def reK (K σ : ℝ) : ℝ := K / (1 + σ ^ 2 * K ^ 2)

/-- Exact shift produced by K-matrix unitarisation. -/
theorem reK_sub (K σ : ℝ) : reK K σ - K = -(σ ^ 2 * K ^ 3) / (1 + σ ^ 2 * K ^ 2) := by
  unfold reK
  have h : (1 + σ ^ 2 * K ^ 2) ≠ 0 := by positivity
  field_simp; ring

/-- The shift is bounded by σ²|K|³: cubic in the tree amplitude. -/
theorem reK_shift_le (K σ : ℝ) : |reK K σ - K| ≤ σ ^ 2 * |K| ^ 3 := by
  rw [reK_sub, abs_div, abs_neg]
  have hd : (1:ℝ) ≤ 1 + σ ^ 2 * K ^ 2 := by nlinarith [sq_nonneg (σ * K)]
  have hpos : (0:ℝ) < 1 + σ ^ 2 * K ^ 2 := by linarith
  rw [abs_of_pos hpos, div_le_iff₀ hpos]
  have : |σ ^ 2 * K ^ 3| = σ ^ 2 * |K| ^ 3 := by
    rw [abs_mul, abs_pow, abs_pow, sq_abs]
  rw [this]
  have : 0 ≤ σ ^ 2 * |K| ^ 3 := by positivity
  nlinarith

/-- Partial-wave zeros are preserved exactly (and not moved). -/
theorem reK_zero_iff (K σ : ℝ) : reK K σ = 0 ↔ K = 0 := by
  unfold reK
  have h : (1 + σ ^ 2 * K ^ 2) ≠ 0 := by positivity
  rw [div_eq_zero_iff]; simp [h]

/-- Exponent comparison only: 2l + 2 < 6l + 2 for l ≥ 1. The informal reading (with K = O(q^(2l)),
    σ = O(q), the K-matrix shift is O(q^(6l+2)), beyond the effective-range order q^(2l+2), so a_l, b_l
    for l ≥ 1 are untouched) is an ARGUMENT using this inequality plus `reK_shift_le`; the asymptotic
    statement itself is not formalised. [Audit 2026-10-13: docstring narrowed, statement unchanged.] -/
theorem shift_beyond_slope (l : ℕ) (hl : 1 ≤ l) : 2 * l + 2 < 6 * l + 2 := by omega

/-- For `l = 0` the inequality `2l + 2 < 6l + 2` fails: the S-wave slope is not protected by
  `shift_beyond_slope`. -/
theorem swave_slope_shifted : ¬ (2 * 0 + 2 < 6 * 0 + 2) := by omega

/-- IAM is degenerate where the LO tree vanishes (D, F waves of a contact LO): t_IAM = 0. -/
theorem iam_degenerate (t4 : ℝ) : (0:ℝ) ^ 2 / (0 - t4) = 0 := by simp

end PositiveGeometryEmergentSpaceTime.UnitarisedLS
