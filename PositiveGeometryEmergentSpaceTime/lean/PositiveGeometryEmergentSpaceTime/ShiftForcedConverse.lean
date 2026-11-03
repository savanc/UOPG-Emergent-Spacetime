/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.NLSM

/-!
M2e converse (L1): the canonical shift satisfies C1(4), C2 and C3.
C1(4) is `PositiveGeometryEmergentSpaceTime.NLSM.shift6_limit` (M2d): with a_oo = −1, a_ee = +1, a_oe = 0, δ⁴·A6(X + δa) → A6N ≠ 0.
C2: A6N · X14 · X25 · X36 is a polynomial, so the only poles are at the (o,e) chords X14, X25, X36.
C3: the soft image of A6N vanishes on all six legs.
-/

namespace PositiveGeometryEmergentSpaceTime.ShiftForced
open PositiveGeometryEmergentSpaceTime.NLSM Filter Topology

/-- C1(4) for the canonical shift (re-export of M2d). -/
theorem converse_C1 {X13 X14 X15 X24 X25 X26 X35 X36 X46 : ℝ} (h14 : X14 ≠ 0) (h25 : X25 ≠ 0) (h36 : X36 ≠ 0) :
    Tendsto (fun δ : ℝ => δ ^ 4 * A6 (X13 - δ) X14 (X15 - δ) (X24 + δ) X25 (X26 + δ) (X35 - δ) X36 (X46 + δ))
      atTop (𝓝 (A6N X13 X14 X15 X24 X25 X26 X35 X36 X46)) :=
  shift6_limit h14 h25 h36

/-- The limit is not identically zero: at X = (1,…,1), A6N = 6. -/
theorem converse_C1_nonzero : A6N 1 1 1 1 1 1 1 1 1 = 6 := by norm_num [A6N]

/-- C2 for the canonical shift: A6N = P / (X14 X25 X36) with P a polynomial; no (e,e)/(o,o) poles. -/
theorem converse_C2 {X13 X14 X15 X24 X25 X26 X35 X36 X46 : ℝ} (h14 : X14 ≠ 0) (h25 : X25 ≠ 0) (h36 : X36 ≠ 0) :
    A6N X13 X14 X15 X24 X25 X26 X35 X36 X46 * (X14 * X25 * X36) =
      X13*X14*X25*X35 - X13*X14*X25*X36 + X13*X14*X25*X46 + X13*X15*X25*X36 + X13*X25*X36*X46 + X14*X15*X24*X36 - X14*X15*X25*X36 + X14*X15*X35*X36 - X14*X24*X25*X36 + X14*X24*X26*X36 + X14*X25*X26*X35 - X14*X25*X26*X36 + X14*X25*X26*X46 - X14*X25*X35*X36 - X14*X25*X36*X46 + X14*X26*X35*X36 + X15*X24*X25*X36 + X24*X25*X36*X46 := by
  simp only [A6N]; field_simp; ring

/-- C3 for the canonical shift, leg 1: soft p1 sends A6^NLSM to 0. -/
theorem adler_leg1 {X24 X25 X35 X36 X46 : ℝ} (h0 : X24 ≠ 0) (h1 : X25 ≠ 0) (h2 : X36 ≠ 0) :
    A6N 0 X24 X25 X24 X25 0 X35 X36 X46 = 0 := by
  simp only [A6N]; field_simp; ring

/-- C3 for the canonical shift, leg 2: soft p2 sends A6^NLSM to 0. -/
theorem adler_leg2 {X14 X15 X35 X36 X46 : ℝ} (h0 : X14 ≠ 0) (h1 : X35 ≠ 0) (h2 : X36 ≠ 0) :
    A6N 0 X14 X15 0 X35 X36 X35 X36 X46 = 0 := by
  simp only [A6N]; field_simp; ring

/-- C3 for the canonical shift, leg 3: soft p3 sends A6^NLSM to 0. -/
theorem adler_leg3 {X14 X15 X25 X26 X46 : ℝ} (h0 : X14 ≠ 0) (h1 : X25 ≠ 0) (h2 : X46 ≠ 0) :
    A6N X14 X14 X15 0 X25 X26 0 X46 X46 = 0 := by
  simp only [A6N]; field_simp; ring

/-- C3 for the canonical shift, leg 4: soft p4 sends A6^NLSM to 0. -/
theorem adler_leg4 {X13 X15 X25 X26 X36 : ℝ} (h0 : X15 ≠ 0) (h1 : X25 ≠ 0) (h2 : X36 ≠ 0) :
    A6N X13 X15 X15 X25 X25 X26 0 X36 0 = 0 := by
  simp only [A6N]; field_simp; ring

/-- C3 for the canonical shift, leg 5: soft p5 sends A6^NLSM to 0. -/
theorem adler_leg5 {X13 X14 X24 X26 X36 : ℝ} (h0 : X14 ≠ 0) (h1 : X26 ≠ 0) (h2 : X36 ≠ 0) :
    A6N X13 X14 0 X24 X26 X26 X36 X36 0 = 0 := by
  simp only [A6N]; field_simp; ring

/-- C3 for the canonical shift, leg 6: soft p6 sends A6^NLSM to 0. -/
theorem adler_leg6 {X13 X14 X24 X25 X35 : ℝ} (h0 : X14 ≠ 0) (h1 : X25 ≠ 0) (h2 : X13 ≠ 0) :
    A6N X13 X14 0 X24 X25 0 X35 X13 X14 = 0 := by
  simp only [A6N]; field_simp; ring


end PositiveGeometryEmergentSpaceTime.ShiftForced
