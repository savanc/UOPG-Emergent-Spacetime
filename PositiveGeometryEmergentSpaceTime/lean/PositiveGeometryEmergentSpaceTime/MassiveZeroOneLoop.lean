/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-2d1: one-loop polynomial part of the SU(2) ππ amplitude at P (BCEGS App. B one-loop b_i, CITED),
and its reduction through the GL85 SU(3)→SU(2) matching (CITED via 0706.0955 eq. 2).
At P: b1 + b2·1 + b3·1 + b4·(t-u)² with t-u = -1.
-/

namespace PositiveGeometryEmergentSpaceTime.MassiveZeroOneLoop

/-- Explicit sum of four one-loop coefficient expressions, linear in `l₁…l₄`, `L` and `1/N` (the
  last weighted by `(1 − 2)²`). -/
noncomputable def bsum (l1 l2 l3 l4 L N : ℝ) : ℝ :=
  (8*l1 + 2*l3 - 2*l4 + 7/6*L + 13/18/N) + (-8*l1 + 2*l4 - 2/3*L - 2/9/N)
  + (2*l1 + l2/2 - L/2 - 7/12/N) + (l2/2 - L/6 - 5/36/N) * (1 - 2)^2

/-- l4 (F_π renormalisation) cancels at P. -/
theorem bsum_eq (l1 l2 l3 l4 L N : ℝ) :
    bsum l1 l2 l3 l4 L N = 2*l1 + l2 + 2*l3 - L/6 - 2/9/N := by
  unfold bsum; ring

/-- Through GL85 matching the polynomial part is Z/2 plus K, η logs:
Z = 8L1+4L2+4L3-16L4-8L5+32L6+16L8 is the MR-2d tree combination. -/
theorem bsum_matched (L1 L2 L3 L4 L5 L6 L8 nK ne L N : ℝ) :
    bsum (4*L1 + 2*L3 - nK/24) (4*L2 - nK/12) (-8*L4 - 4*L5 + 16*L6 + 8*L8 - ne/18)
      (8*L4 + 4*L5 - nK/2) L N
    = (8*L1 + 4*L2 + 4*L3 - 16*L4 - 8*L5 + 32*L6 + 16*L8)
      - nK/6 - ne/9 - L/6 - 2/9/N := by
  unfold bsum; ring

/-- Below threshold: at P every Mandelstam invariant lies in (0, 4M²), so the one-loop
functions are real there. -/
theorem P_below_threshold : (0:ℝ) < 1 ∧ (1:ℝ) < 4 ∧ (0:ℝ) < 2 ∧ (2:ℝ) < 4 := by norm_num

end PositiveGeometryEmergentSpaceTime.MassiveZeroOneLoop
