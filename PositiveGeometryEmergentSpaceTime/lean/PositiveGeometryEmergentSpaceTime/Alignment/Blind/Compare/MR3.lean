/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.MassiveLS
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Mr3Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: MR-3 (massive LS, f₂-level positivity)

Blind coefficients `c0, c1, c2` (over ℚ) vs the original `PositiveGeometryEmergentSpaceTime.MassiveLS.level2_decomp`
coefficients (over ℝ). The coefficients coincide after the cast; the headline
(`positivity_forces_chiral`) is derivable from either side on rational `r`.
VERDICT: BLIND-STRONGER — headline EQUIV; the blind file additionally proves
`all_coeffs_nonneg_iff` (r = 0 ∨ r = 1/2) and `c1_neg_above_half`, which the original does not
state. Gap: the blind file works over ℚ, the original over ℝ (immaterial for these rational
identities; the original's ℝ version of the headline is not recovered from the blind file).
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR3

open PositiveGeometryEmergentSpaceTime.Alignment.Mr3Blind

theorem c0_cast (r : ℚ) : ((c0 r : ℚ) : ℝ) = (r : ℝ) * (1 - 2 * r) * (-1) / (4 * (1 - r) ^ 2) := by
  unfold c0; push_cast; ring

theorem c1_cast (r : ℚ) : ((c1 r : ℚ) : ℝ) = 3 * (1 - 2 * (r : ℝ)) / (8 * (1 - r) ^ 2) := by
  unfold c1; push_cast; ring

theorem c2_cast (r : ℚ) : ((c2 r : ℚ) : ℝ) = 3 * (1 - 2 * (r : ℝ)) ^ 2 / (8 * (1 - r) ^ 2) := by
  unfold c2; push_cast; ring

/-- Original headline ⇒ blind headline (on rational r). -/
theorem orig_to_blind (r : ℚ) (h0 : 0 ≤ r) (h1 : r < 1 / 2) : 0 ≤ c0 r ↔ r = 0 := by
  constructor
  · intro h
    have h' : (0 : ℝ) ≤ (r : ℝ) * (1 - 2 * r) * (-1) / (4 * (1 - r) ^ 2) := by
      rw [← c0_cast]; exact_mod_cast h
    have h0' : (0 : ℝ) ≤ (r : ℝ) := by exact_mod_cast h0
    have h1' : (r : ℝ) < 1 / 2 := by
      have : ((r : ℚ) : ℝ) < ((1 / 2 : ℚ) : ℝ) := Rat.cast_lt.mpr h1
      simpa using this
    have := PositiveGeometryEmergentSpaceTime.MassiveLS.positivity_forces_chiral (r : ℝ) h0' h1' h'
    exact_mod_cast this
  · rintro rfl; unfold c0; norm_num

/-- Blind headline ⇒ original headline (on rational r). -/
theorem blind_to_orig (r : ℚ) (h0 : 0 ≤ r) (h1 : r < 1 / 2)
    (hpos : (0 : ℝ) ≤ (r : ℝ) * (1 - 2 * r) * (-1) / (4 * (1 - r) ^ 2)) : r = 0 := by
  rw [← c0_cast] at hpos
  exact (positivity_forces_zero r h0 h1).1 (by exact_mod_cast hpos)

/-- The extra blind content, restated in the original's coefficient form: the J = 1 coefficient is
negative for r > 1/2 (so "only J = 0 can fail" needs r < 1/2). -/
theorem orig_c1_neg_above_half (r : ℚ) (h1 : 1 / 2 < r) (hr : r ≠ 1) :
    3 * (1 - 2 * (r : ℝ)) / (8 * (1 - r) ^ 2) < 0 := by
  rw [← c1_cast]; exact_mod_cast c1_neg_above_half r h1 hr

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR3
