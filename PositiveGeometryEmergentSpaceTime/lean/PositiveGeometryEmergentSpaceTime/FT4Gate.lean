/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.MassiveZeroOneLoop

/-!
FT-4 gate: one-loop (NLO ChPT) hidden zero, 4 points, unequal masses.
Reuses MR-2d1 `MassiveZeroOneLoop.bsum_matched`. GL85 running coefficients Γ_i are CITED.
-/

namespace PositiveGeometryEmergentSpaceTime.FT4Gate
open PositiveGeometryEmergentSpaceTime.MassiveZeroOneLoop

/-- The NLO zero condition at P depends on the L_i only through the single MR-2d combination Z:
shifting the L_i along any direction that keeps Z fixed leaves the condition unchanged. -/
theorem only_Z (L1 L2 L3 L4 L5 L6 L8 d1 d2 d3 d4 d5 d6 d8 nK ne L N : ℝ)
    (hZ : 8*d1 + 4*d2 + 4*d3 - 16*d4 - 8*d5 + 32*d6 + 16*d8 = 0) :
    bsum (4*(L1+d1) + 2*(L3+d3) - nK/24) (4*(L2+d2) - nK/12)
      (-8*(L4+d4) - 4*(L5+d5) + 16*(L6+d6) + 8*(L8+d8) - ne/18)
      (8*(L4+d4) + 4*(L5+d5) - nK/2) L N
    = bsum (4*L1 + 2*L3 - nK/24) (4*L2 - nK/12) (-8*L4 - 4*L5 + 16*L6 + 8*L8 - ne/18)
      (8*L4 + 4*L5 - nK/2) L N := by
  rw [bsum_matched, bsum_matched]; linear_combination hZ

/-- Running of Z from GL85 Γ_i (Γ1=3/32, Γ2=3/16, Γ3=0, Γ4=1/8, Γ5=3/8, Γ6=11/144, Γ8=5/48): nonzero,
so the zero is not a scale-free LEC relation; it is one renormalised relation Z^r(μ) = logs. -/
theorem Z_running :
    8*(3/32:ℚ) + 4*(3/16) + 4*0 - 16*(1/8) - 8*(3/8) + 32*(11/144) + 16*(5/48) = 11/18 := by norm_num

end PositiveGeometryEmergentSpaceTime.FT4Gate
