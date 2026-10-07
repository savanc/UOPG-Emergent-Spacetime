import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.Order.Ring.Defs
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import UOPG0.Plucker

/-!
MVP-1. The positive chamber of `Gr⁺(2,4)`, in one GL(2) gauge, is the orthant.

The gauge fixes columns 0 and 2 to the identity. The remaining entries are four
positive coordinates `(x, y, z, w)`. Their dlog coefficient is `1/(x y z w)`,
which equals `1` over the product of the four ordered adjacent minors.

The cyclic Parke–Taylor product uses `⟨4 1⟩ = -P₀₃`, so that rational function
is the negative of the orthant coefficient. The sign is part of the theorem.

This file does not construct a de Rham 4-form, a helicity weight, or a cross section.
-/

namespace UOPG0

section Ring

variable {α : Type*} [CommRing α]

/-- Gauge-fixed `2 × 4` matrix. Columns 0 and 2 are the identity. -/
def chart (x y z w : α) : Matrix (Fin 2) (Fin 4) α
  | 0, 0 => 1
  | 0, 1 => y
  | 0, 2 => 0
  | 0, 3 => -w
  | 1, 0 => 0
  | 1, 1 => x
  | 1, 2 => 1
  | 1, 3 => z

@[simp] theorem chart_P01 (x y z w : α) : plucker (chart x y z w) 0 1 = x := by
  simp [plucker, chart]

@[simp] theorem chart_P02 (x y z w : α) : plucker (chart x y z w) 0 2 = 1 := by
  simp [plucker, chart]

@[simp] theorem chart_P03 (x y z w : α) : plucker (chart x y z w) 0 3 = z := by
  simp [plucker, chart]

@[simp] theorem chart_P12 (x y z w : α) : plucker (chart x y z w) 1 2 = y := by
  simp [plucker, chart]

@[simp] theorem chart_P23 (x y z w : α) : plucker (chart x y z w) 2 3 = w := by
  simp [plucker, chart]

theorem chart_P13 (x y z w : α) : plucker (chart x y z w) 1 3 = y * z + x * w := by
  simp only [plucker, chart]
  ring

/-- Product of the four ordered adjacent minors `P01 P12 P23 P03`. -/
def adjacentProduct (C : Matrix (Fin 2) (Fin 4) α) : α :=
  plucker C 0 1 * plucker C 1 2 * plucker C 2 3 * plucker C 0 3

/-- `⟨4 1⟩`, columns in that order. This is `-P03`, not the ordered minor. -/
def angle41 (C : Matrix (Fin 2) (Fin 4) α) : α :=
  C 0 3 * C 1 0 - C 1 3 * C 0 0

/-- Cyclic product `⟨1 2⟩⟨2 3⟩⟨3 4⟩⟨4 1⟩` in column order `0,1,2,3`. -/
def cyclicProduct (C : Matrix (Fin 2) (Fin 4) α) : α :=
  plucker C 0 1 * plucker C 1 2 * plucker C 2 3 * angle41 C

theorem angle41_eq_neg_P03 (C : Matrix (Fin 2) (Fin 4) α) : angle41 C = -plucker C 0 3 := by
  simp only [angle41, plucker]
  ring

theorem cyclicProduct_eq_neg_adjacent (C : Matrix (Fin 2) (Fin 4) α) :
    cyclicProduct C = -adjacentProduct C := by
  simp only [cyclicProduct, adjacentProduct, angle41_eq_neg_P03]
  ring

theorem chart_adjacentProduct (x y z w : α) :
    adjacentProduct (chart x y z w) = x * y * z * w := by
  simp only [adjacentProduct, chart_P01, chart_P12, chart_P23, chart_P03]
  ring

theorem chart_cyclicProduct (x y z w : α) :
    cyclicProduct (chart x y z w) = -(x * y * z * w) := by
  rw [cyclicProduct_eq_neg_adjacent, chart_adjacentProduct]

/-- The Plücker relation solves the non-adjacent minor from the other five. -/
theorem plucker13_from_adjacent (C : Matrix (Fin 2) (Fin 4) α) :
    plucker C 0 2 * plucker C 1 3 =
      plucker C 0 1 * plucker C 2 3 + plucker C 0 3 * plucker C 1 2 := by
  have h := plucker_relation C
  simp only [pluckerQuad] at h
  linear_combination -h

theorem adjacentProduct_gl_weight (g : Matrix (Fin 2) (Fin 2) α) (C : Matrix (Fin 2) (Fin 4) α) :
    adjacentProduct (g * C) = det2 g ^ 4 * adjacentProduct C := by
  simp only [adjacentProduct, plucker_gl_weight]
  ring

/-- Columns 0 and 2, the pair normalised by the gauge. -/
def columnPair (C : Matrix (Fin 2) (Fin 4) α) : Matrix (Fin 2) (Fin 2) α
  | i, 0 => C i 0
  | i, 1 => C i 2

theorem columnPair_det (C : Matrix (Fin 2) (Fin 4) α) : det2 (columnPair C) = plucker C 0 2 := by
  simp only [det2, columnPair, plucker]
  ring

end Ring

section Field

variable {α : Type*} [Field α]

/-- Left GL(2) element sending columns 0 and 2 to the identity, when `P02 ≠ 0`. -/
def gaugeMatrix (C : Matrix (Fin 2) (Fin 4) α) : Matrix (Fin 2) (Fin 2) α
  | 0, 0 => C 1 2 / plucker C 0 2
  | 0, 1 => -C 0 2 / plucker C 0 2
  | 1, 0 => -C 1 0 / plucker C 0 2
  | 1, 1 => C 0 0 / plucker C 0 2

def chartX (C : Matrix (Fin 2) (Fin 4) α) : α := plucker C 0 1 / plucker C 0 2
def chartY (C : Matrix (Fin 2) (Fin 4) α) : α := plucker C 1 2 / plucker C 0 2
def chartZ (C : Matrix (Fin 2) (Fin 4) α) : α := plucker C 0 3 / plucker C 0 2
def chartW (C : Matrix (Fin 2) (Fin 4) α) : α := plucker C 2 3 / plucker C 0 2

/-- Coefficient of `dx∧dy∧dz∧dw` for the orthant dlog form. -/
def orthantCoeff (x y z w : α) : α := (x * y * z * w)⁻¹

/-- Cyclic Parke–Taylor rational function in the same coordinates. -/
def parkeTaylorCoeff (x y z w : α) : α := -orthantCoeff x y z w

theorem gaugeMatrix_det (C : Matrix (Fin 2) (Fin 4) α) (h : plucker C 0 2 ≠ 0) :
    det2 (gaugeMatrix C) = (plucker C 0 2)⁻¹ := by
  have hδ : C 0 0 * C 1 2 - C 1 0 * C 0 2 ≠ 0 := by simpa [plucker] using h
  simp only [det2, gaugeMatrix, plucker]
  field_simp [hδ]

theorem gaugeMatrix_mul_columnPair (C : Matrix (Fin 2) (Fin 4) α) (h : plucker C 0 2 ≠ 0) :
    gaugeMatrix C * columnPair C = 1 := by
  -- Keep `plucker` folded so the denominator matches `h`. Unfolding it first
  -- commutes the factors and `field_simp` no longer sees the hypothesis.
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, gaugeMatrix, columnPair] <;>
    field_simp [h] <;>
    simp only [plucker] <;>
    ring

theorem columnPair_mul_gaugeMatrix (C : Matrix (Fin 2) (Fin 4) α) (h : plucker C 0 2 ≠ 0) :
    columnPair C * gaugeMatrix C = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, gaugeMatrix, columnPair] <;>
    field_simp [h] <;>
    simp only [plucker] <;>
    ring

/-- Any matrix normalising the two columns equals this gauge. -/
theorem eq_gaugeMatrix (g : Matrix (Fin 2) (Fin 2) α) (C : Matrix (Fin 2) (Fin 4) α)
    (h : plucker C 0 2 ≠ 0) (hg : g * columnPair C = 1) : g = gaugeMatrix C := by
  have hR := columnPair_mul_gaugeMatrix C h
  calc
    g = g * 1 := by rw [Matrix.mul_one]
    _ = g * (columnPair C * gaugeMatrix C) := by rw [hR]
    _ = (g * columnPair C) * gaugeMatrix C := by rw [Matrix.mul_assoc]
    _ = 1 * gaugeMatrix C := by rw [hg]
    _ = gaugeMatrix C := by rw [Matrix.one_mul]

theorem gauge_mul_eq_chart (C : Matrix (Fin 2) (Fin 4) α) (h : plucker C 0 2 ≠ 0) :
    gaugeMatrix C * C = chart (chartX C) (chartY C) (chartZ C) (chartW C) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, gaugeMatrix, chart, chartX, chartY, chartZ, chartW] <;>
    field_simp [h] <;>
    simp only [plucker] <;>
    ring

theorem orthantCoeff_residue (x y z w : α) (hx : x ≠ 0) (hy : y ≠ 0) (hz : z ≠ 0) (hw : w ≠ 0) :
    x * y * z * w * orthantCoeff x y z w = 1 := by
  have h : x * y * z * w ≠ 0 := mul_ne_zero (mul_ne_zero (mul_ne_zero hx hy) hz) hw
  simp only [orthantCoeff]
  field_simp [h]

theorem orthantCoeff_eq_inv_adjacent (x y z w : α) :
    orthantCoeff x y z w = (adjacentProduct (chart x y z w))⁻¹ := by
  rw [chart_adjacentProduct, orthantCoeff]

theorem parkeTaylorCoeff_eq_inv_cyclic (x y z w : α) :
    parkeTaylorCoeff x y z w = (cyclicProduct (chart x y z w))⁻¹ := by
  rw [chart_cyclicProduct, parkeTaylorCoeff, orthantCoeff, inv_neg]

end Field

section Ordered

variable {α : Type*} [Field α] [LinearOrder α] [IsStrictOrderedRing α]

theorem chart_minors_pos (x y z w : α) (hx : 0 < x) (hy : 0 < y) (hz : 0 < z) (hw : 0 < w) :
    0 < plucker (chart x y z w) 0 1 ∧ 0 < plucker (chart x y z w) 0 2 ∧
      0 < plucker (chart x y z w) 0 3 ∧ 0 < plucker (chart x y z w) 1 2 ∧
      0 < plucker (chart x y z w) 1 3 ∧ 0 < plucker (chart x y z w) 2 3 := by
  simp only [chart_P01, chart_P02, chart_P03, chart_P12, chart_P23, chart_P13]
  refine ⟨hx, zero_lt_one, hz, hy, ?_, hw⟩
  exact (mul_pos hy hz).trans (lt_add_of_pos_right _ (mul_pos hx hw))

theorem chartCoord_pos (C : Matrix (Fin 2) (Fin 4) α)
    (h01 : 0 < plucker C 0 1) (h02 : 0 < plucker C 0 2) (h03 : 0 < plucker C 0 3)
    (h12 : 0 < plucker C 1 2) (h23 : 0 < plucker C 2 3) :
    0 < chartX C ∧ 0 < chartY C ∧ 0 < chartZ C ∧ 0 < chartW C := by
  exact ⟨div_pos h01 h02, div_pos h12 h02, div_pos h03 h02, div_pos h23 h02⟩

/-- A positive matrix is GL(2)-equivalent to exactly one orthant chart matrix,
via the unique gauge that normalises columns 0 and 2. -/
theorem positive_gauge_chart (C : Matrix (Fin 2) (Fin 4) α)
    (h01 : 0 < plucker C 0 1) (h02 : 0 < plucker C 0 2) (h03 : 0 < plucker C 0 3)
    (h12 : 0 < plucker C 1 2) (h23 : 0 < plucker C 2 3) :
    gaugeMatrix C * C = chart (chartX C) (chartY C) (chartZ C) (chartW C) ∧
      0 < chartX C ∧ 0 < chartY C ∧ 0 < chartZ C ∧ 0 < chartW C := by
  have hδ : plucker C 0 2 ≠ 0 := ne_of_gt h02
  exact ⟨gauge_mul_eq_chart C hδ, chartCoord_pos C h01 h02 h03 h12 h23⟩

end Ordered

theorem positiveExample_chartX : chartX positiveExample = (1 : ℚ) / 2 := by
  unfold chartX plucker positiveExample
  norm_num

theorem positiveExample_chartY : chartY positiveExample = (1 : ℚ) / 2 := by
  unfold chartY plucker positiveExample
  norm_num

theorem positiveExample_chartZ : chartZ positiveExample = (3 : ℚ) / 2 := by
  unfold chartZ plucker positiveExample
  norm_num

theorem positiveExample_chartW : chartW positiveExample = (1 : ℚ) / 2 := by
  unfold chartW plucker positiveExample
  norm_num

theorem positiveExample_gauge :
    gaugeMatrix positiveExample * positiveExample =
      chart ((1 : ℚ) / 2) ((1 : ℚ) / 2) ((3 : ℚ) / 2) ((1 : ℚ) / 2) := by
  have hδ : plucker positiveExample 0 2 ≠ 0 := by
    unfold plucker positiveExample
    norm_num
  rw [gauge_mul_eq_chart positiveExample hδ, positiveExample_chartX, positiveExample_chartY,
    positiveExample_chartZ, positiveExample_chartW]

theorem orthantCoeff_witness :
    orthantCoeff ((1 : ℚ) / 2) ((1 : ℚ) / 2) ((3 : ℚ) / 2) ((1 : ℚ) / 2) = (16 : ℚ) / 3 := by
  simp [orthantCoeff]
  norm_num

theorem parkeTaylorCoeff_witness :
    parkeTaylorCoeff ((1 : ℚ) / 2) ((1 : ℚ) / 2) ((3 : ℚ) / 2) ((1 : ℚ) / 2) = -((16 : ℚ) / 3) := by
  simp [parkeTaylorCoeff, orthantCoeff]
  norm_num

end UOPG0
