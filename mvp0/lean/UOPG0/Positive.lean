import UOPG0.Plucker

/-!
One explicit rational point of the positive chamber `Gr⁺(2,4)`.

All six ordered maximal minors are positive. This is a witness that the chamber
is nonempty over `ℚ`. It is not a fitted physical state.
-/

namespace UOPG0

theorem positiveExample_P01 : plucker positiveExample 0 1 = 1 := by
  simp [plucker, positiveExample]

theorem positiveExample_P02 : plucker positiveExample 0 2 = 2 := by
  simp [plucker, positiveExample]

theorem positiveExample_P03 : plucker positiveExample 0 3 = 3 := by
  simp [plucker, positiveExample]

theorem positiveExample_P12 : plucker positiveExample 1 2 = 1 := by
  simp [plucker, positiveExample]; norm_num

theorem positiveExample_P13 : plucker positiveExample 1 3 = 2 := by
  simp [plucker, positiveExample]; norm_num

theorem positiveExample_P23 : plucker positiveExample 2 3 = 1 := by
  simp [plucker, positiveExample]; norm_num

theorem positiveExample_minors_pos :
    0 < plucker positiveExample 0 1 ∧ 0 < plucker positiveExample 0 2 ∧
      0 < plucker positiveExample 0 3 ∧ 0 < plucker positiveExample 1 2 ∧
      0 < plucker positiveExample 1 3 ∧ 0 < plucker positiveExample 2 3 := by
  simp [positiveExample_P01, positiveExample_P02, positiveExample_P03, positiveExample_P12,
    positiveExample_P13, positiveExample_P23]

end UOPG0
