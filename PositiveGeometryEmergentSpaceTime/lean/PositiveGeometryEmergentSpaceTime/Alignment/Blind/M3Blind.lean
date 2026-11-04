/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of M3 ("the rule arithmetic is
checked in Lean"). Written ONLY from Paper I v9 §"M3" prose: band [−2.6, −1.4],
L3/L2 = −3.79 ± 0.31, "the band edge is 3.84σ away: FAIL". Not a Paper II headline; included
because its PROVED content is fully specified by the prose (see BLIND-2026-11-03.md).
Reading: FAIL ⇔ the central value lies outside the band; the distance to the nearest band edge
in units of σ is (−2.6 − (−3.79))/0.31 = 119/31, which rounds to 3.84.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.M3Blind

def bandLo : ℚ := -26/10
def bandHi : ℚ := -14/10
def central : ℚ := -379/100
def sigma : ℚ := 31/100
/-- the zero-parameter prediction -/
def prediction : ℚ := -2

def nsigma : ℚ := (bandLo - central) / sigma

theorem prediction_in_band : bandLo ≤ prediction ∧ prediction ≤ bandHi := by
  unfold bandLo bandHi prediction; norm_num

theorem data_outside_band : ¬ (bandLo ≤ central ∧ central ≤ bandHi) := by
  unfold bandLo bandHi central; norm_num

theorem nearest_edge_is_lower : |central - bandLo| < |central - bandHi| := by
  unfold central bandLo bandHi; norm_num [abs_of_neg, abs_of_pos]

theorem nsigma_eq : nsigma = 119 / 31 := by
  unfold nsigma bandLo central sigma; norm_num

/-- "3.84σ" is the two-decimal rounding of 119/31. -/
theorem nsigma_rounds : 3835/1000 ≤ nsigma ∧ nsigma < 3845/1000 := by
  rw [nsigma_eq]; norm_num

/-- the band is symmetric about the prediction with half-width 0.6 -/
theorem band_symmetric : prediction - bandLo = bandHi - prediction ∧ bandHi - prediction = 6/10 := by
  unfold prediction bandLo bandHi; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.M3Blind
