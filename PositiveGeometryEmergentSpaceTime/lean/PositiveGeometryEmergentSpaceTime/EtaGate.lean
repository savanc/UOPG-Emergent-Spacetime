/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-! DZ-1 gate: η→3π LO zero line s = 4M²/3 (π = charged pions of mass M; s = (p₊+p₋)²). -/
namespace PositiveGeometryEmergentSpaceTime.EtaGate

/-- on the line, p₊·p₋ = (s − 2M²)/2 = −M²/3 ≠ 0: not the CGW form p_a·p_b = 0 -/
theorem dot_on_line (M : ℝ) : ((4/3) * M^2 - 2 * M^2) / 2 = -(M^2) / 3 := by ring

/-- `−M²/3 ≠ 0` for `M ≠ 0` (the value computed by `dot_on_line` is nonzero). -/
theorem not_cgw (M : ℝ) (hM : M ≠ 0) : -(M^2) / 3 ≠ 0 := by
  have : M^2 ≠ 0 := pow_ne_zero 2 hM
  intro h; apply this; linarith

/-- with s + t + u = Mη² + 3M² and s = 4M²/3, one of t, u exceeds the ππ threshold 4M²
whenever Mη² > 19M²/3, so the line runs onto the t/u-channel cuts. -/
theorem crosses_cut (M Me t u : ℝ) (hsum : (4/3)*M^2 + t + u = Me^2 + 3*M^2)
    (hMe : Me^2 > 19/3 * M^2) : t > 4*M^2 ∨ u > 4*M^2 := by
  by_contra h; push Not at h; nlinarith [h.1, h.2]

end PositiveGeometryEmergentSpaceTime.EtaGate
