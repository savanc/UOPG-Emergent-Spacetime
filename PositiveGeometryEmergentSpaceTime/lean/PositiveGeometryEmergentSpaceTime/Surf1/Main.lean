/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
SURF-1′ main statement: no N ≥ 3 is colour-sign coherent (S = ∅), from kernel-enumerated colour
weights (`Enum.lean`, `Box.lean`) and the ℚ sign facts (`Signs.lean`).
Physics reading (CONJECTURE / SPECULATION, not claimed here): sign(K) = sign of one-loop/tree
interference under the prereg kinematic-sign assumption.
-/
import PositiveGeometryEmergentSpaceTime.Surf1.Box
import PositiveGeometryEmergentSpaceTime.Surf1.Signs

/-!
# PositiveGeometryEmergentSpaceTime.Surf1.Main

Supporting module of the `PositiveGeometryEmergentSpaceTime` Lean library. See the declarations below for
the statements; each theorem is checked by the Lean kernel.
-/


set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Surf1

/-- K_triangle at N = 3 from the enumerated weights: W(tetra)/W(theta) = −1. -/
theorem K_tri_three_enum : K (W1 tetra) (W1 theta) 3 = -1 := by
  rw [tetra_c1, theta_c1]; exact K_tri_three

/-- Crossed u-channel box from the enumerated weights is negative for every N ≥ 4. -/
theorem K_boxU_neg_enum (N : ℚ) (h : 4 ≤ N) : K (W1 boxU) (W1 ttU) N < 0 := by
  rw [boxU_c1, ttU_c1]; exact K_boxU_neg N h

/-- SURF-1′ (EXCLUSION `SURF1.nc_not_selected_by_colour_sign`): for every integer N ≥ 3, the
triangle (n = 3) or the crossed u-channel box (n = 4) has a negative colour-weighted
interference, so the sign-coherent set S is empty. -/
theorem no_sign_coherent_N (N : ℕ) (h : 3 ≤ N) :
    K (W1 tetra) (W1 theta) N < 0 ∨ K (W1 boxU) (W1 ttU) N < 0 := by
  rw [tetra_c1, theta_c1, boxU_c1, ttU_c1]; exact no_coherent_poly N h

end PositiveGeometryEmergentSpaceTime.Surf1
