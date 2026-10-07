import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import UOPG0.Canonical
import UOPG0.Positive

/-!
MVP-2. The orthant coefficient factors onto a face by algebra.

`1/(x y z w)` is zero in the denominator exactly when one of `x, y, z, w` is zero,
and those four coordinates are the ordered adjacent minors of the chart. On each
codimension-1 face the non-adjacent minor `P13 = y z + x w` stays positive.

Multiplying the coefficient by the transverse coordinate cancels it. The result
does not depend on that coordinate, and it is the coefficient of the opposite
3-orthant. This is not a de Rham residue, not a cross section, and not a mutation.

The column update from the 2026 drafts is one rational point: at the witness and
`λ = 1` it sends `P23` from 1 to 0. It stays on the quadric because every 2-plane
does. That refuses the map. It does not define a cluster algebra.
-/

namespace UOPG0

section Field

variable {α : Type*} [Field α]

/-- The denominator vanishes exactly on a coordinate wall of the chart. -/
theorem chart_adjacentProduct_eq_zero_iff (x y z w : α) :
    adjacentProduct (chart x y z w) = 0 ↔ x = 0 ∨ y = 0 ∨ z = 0 ∨ w = 0 := by
  rw [chart_adjacentProduct]
  simp [mul_eq_zero, or_assoc]

/-- Those coordinates are the four ordered adjacent minors, so the wall is one of them.
`P13` is not among the four. -/
theorem chart_pole_iff_adjacent_minor (x y z w : α) :
    adjacentProduct (chart x y z w) = 0 ↔
      plucker (chart x y z w) 0 1 = 0 ∨ plucker (chart x y z w) 1 2 = 0 ∨
      plucker (chart x y z w) 0 3 = 0 ∨ plucker (chart x y z w) 2 3 = 0 := by
  simp only [chart_adjacentProduct_eq_zero_iff, chart_P01, chart_P12, chart_P03, chart_P23]

theorem residue_drop_x (x y z w : α) (hx : x ≠ 0) (hy : y ≠ 0) (hz : z ≠ 0) (hw : w ≠ 0) :
    x * orthantCoeff x y z w = (y * z * w)⁻¹ := by
  have h : y * z * w ≠ 0 := mul_ne_zero (mul_ne_zero hy hz) hw
  simp only [orthantCoeff]
  field_simp [hx, h]

theorem residue_drop_y (x y z w : α) (hx : x ≠ 0) (hy : y ≠ 0) (hz : z ≠ 0) (hw : w ≠ 0) :
    y * orthantCoeff x y z w = (x * z * w)⁻¹ := by
  have h : x * z * w ≠ 0 := mul_ne_zero (mul_ne_zero hx hz) hw
  simp only [orthantCoeff]
  field_simp [hy, h]

theorem residue_drop_z (x y z w : α) (hx : x ≠ 0) (hy : y ≠ 0) (hz : z ≠ 0) (hw : w ≠ 0) :
    z * orthantCoeff x y z w = (x * y * w)⁻¹ := by
  have h : x * y * w ≠ 0 := mul_ne_zero (mul_ne_zero hx hy) hw
  simp only [orthantCoeff]
  field_simp [hz, h]

theorem residue_drop_w (x y z w : α) (hx : x ≠ 0) (hy : y ≠ 0) (hz : z ≠ 0) (hw : w ≠ 0) :
    w * orthantCoeff x y z w = (x * y * z)⁻¹ := by
  have h : x * y * z ≠ 0 := mul_ne_zero (mul_ne_zero hx hy) hz
  simp only [orthantCoeff]
  field_simp [hw, h]

/-- `P13` can vanish while the adjacent product does not. This point is outside
the positive chamber: `z = -1`. -/
theorem nonadjacent_zero_off_chamber :
    plucker (chart (1 : ℚ) 1 (-1) 1) 1 3 = 0 ∧
      adjacentProduct (chart (1 : ℚ) 1 (-1) 1) ≠ 0 := by
  constructor
  · rw [chart_P13]; norm_num
  · rw [chart_adjacentProduct]; norm_num

end Field

section Ordered

variable {α : Type*} [Field α] [LinearOrder α] [IsStrictOrderedRing α]

theorem face_x_P13_pos (x y z w : α) (hx : 0 ≤ x) (hy : 0 < y) (hz : 0 < z) (hw : 0 < w) :
    0 < plucker (chart x y z w) 1 3 := by
  rw [chart_P13]
  exact (mul_pos hy hz).trans_le (le_add_of_nonneg_right (mul_nonneg hx hw.le))

theorem face_y_P13_pos (x y z w : α) (hx : 0 < x) (hy : 0 ≤ y) (hz : 0 < z) (hw : 0 < w) :
    0 < plucker (chart x y z w) 1 3 := by
  rw [chart_P13]
  exact (mul_pos hx hw).trans_le (le_add_of_nonneg_left (mul_nonneg hy hz.le))

theorem face_z_P13_pos (x y z w : α) (hx : 0 < x) (hy : 0 < y) (hz : 0 ≤ z) (hw : 0 < w) :
    0 < plucker (chart x y z w) 1 3 := by
  rw [chart_P13]
  exact (mul_pos hx hw).trans_le (le_add_of_nonneg_left (mul_nonneg hy.le hz))

theorem face_w_P13_pos (x y z w : α) (hx : 0 < x) (hy : 0 < y) (hz : 0 < z) (hw : 0 ≤ w) :
    0 < plucker (chart x y z w) 1 3 := by
  rw [chart_P13]
  exact (mul_pos hy hz).trans_le (le_add_of_nonneg_right (mul_nonneg hx.le hw))

end Ordered

/-- Column 3 is replaced by `column 3 + λ (column 1 + column 2)`. Not a mutation. -/
def columnShift {α : Type*} [Ring α] (lam : α) (C : Matrix (Fin 2) (Fin 4) α) :
    Matrix (Fin 2) (Fin 4) α
  | i, 0 => C i 0
  | i, 1 => C i 1
  | i, 2 => C i 2
  | i, 3 => C i 3 + lam * (C i 1 + C i 2)

theorem witness_columnShift_P23 : plucker (columnShift 1 positiveExample) 2 3 = 0 := by
  unfold plucker columnShift positiveExample
  norm_num

theorem witness_columnShift_quadric : pluckerQuad (columnShift 1 positiveExample) = 0 :=
  plucker_relation _

theorem witness_columnShift_leaves_positive :
    plucker positiveExample 2 3 = 1 ∧ plucker (columnShift 1 positiveExample) 2 3 = 0 :=
  ⟨positiveExample_P23, witness_columnShift_P23⟩

theorem residue_drop_x_witness :
    ((1 : ℚ) / 2) * orthantCoeff ((1 : ℚ) / 2) ((1 : ℚ) / 2) ((3 : ℚ) / 2) ((1 : ℚ) / 2) =
      (8 : ℚ) / 3 := by
  simp [orthantCoeff]
  norm_num

theorem residue_drop_z_witness :
    ((3 : ℚ) / 2) * orthantCoeff ((1 : ℚ) / 2) ((1 : ℚ) / 2) ((3 : ℚ) / 2) ((1 : ℚ) / 2) =
      (8 : ℚ) := by
  simp [orthantCoeff]
  norm_num

theorem face_x_P13_witness :
    plucker (chart (0 : ℚ) ((1 : ℚ) / 2) ((3 : ℚ) / 2) ((1 : ℚ) / 2)) 1 3 = (3 : ℚ) / 4 := by
  rw [chart_P13]
  norm_num

end UOPG0
