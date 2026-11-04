/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.GradedPositroid
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.GradedPositroidBlind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: GRADED-POSITROID

The ACC predicates are syntactically identical. The weight matrices differ by a convention
(blind uses integer-scaled SU(2)/SU(3) weights, the original half-integers), but both moment
conditions are proved equivalent to the same ACC, hence to each other. VERDICT: EQUIV.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.GPOS

open PositiveGeometryEmergentSpaceTime.Alignment.GradedPositroidBlind

theorem acc_iff (yQ yu yd yL ye : ℚ) :
    ACC ⟨yQ, yu, yd, yL, ye⟩ ↔ PositiveGeometryEmergentSpaceTime.GradedPositroid.ACC yQ yu yd yL ye := Iff.rfl

/-- Blind moment condition ⇔ original graded moment condition (through the shared ACC). -/
theorem moments_equiv (yQ yu yd yL ye : ℚ) :
    (firstMomentsVanish ⟨yQ, yu, yd, yL, ye⟩ ∧ cubicMomentsVanish ⟨yQ, yu, yd, yL, ye⟩) ↔
      ((∀ a, PositiveGeometryEmergentSpaceTime.GradedPositroid.m1 (PositiveGeometryEmergentSpaceTime.GradedPositroid.genW yQ yu yd yL ye) a = 0) ∧
        (∀ a b c, PositiveGeometryEmergentSpaceTime.GradedPositroid.cub (PositiveGeometryEmergentSpaceTime.GradedPositroid.genW yQ yu yd yL ye) a b c = 0)) := by
  rw [moments_iff_acc, PositiveGeometryEmergentSpaceTime.GradedPositroid.graded_cubic_iff_acc]; exact acc_iff _ _ _ _ _

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.GPOS
