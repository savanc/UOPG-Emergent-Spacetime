/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.SC2
/-!
# SC-2b: SC-2's weights vs cell volumes of the Feynman fan (arXiv 2309.15913) (2026-10-15)
Every top cone of the g-vector fan is unimodular (eq. 22), so the cone Jacobian (I1) is 1 for both the
bubble cone {S₁,S₂} (eq. 101) and the triangle cone {e₁,e₂,e₃} (eq. 78). The projective slice
{ρ ≥ 0, Σρ = 1} (I2) has Lebesgue volume 1/2 for E = 3 and 1 for E = 2. Hence the SC-2 triangle factor
1/2 *is* a cell volume (I2), but the bubble factor 1/6 = ∫x(1-x) is an F/U moment, not a cell volume.
All identities proved here; nothing simulated. Verdict PARTIAL.
-/
namespace PositiveGeometryEmergentSpaceTime.SC2b
open MeasureTheory

/-- Bubble cone g-vectors (S₁, S₂) of 2309.15913 eq. 101, as matrix rows. -/
def bubbleCone : Matrix (Fin 2) (Fin 2) ℤ := !![0, -1; -1, 0]
/-- Triangle cone: one-peak triangulation, g = eᵢ (eq. 78). -/
def triCone : Matrix (Fin 3) (Fin 3) ℤ := 1

/-- I1 for the bubble cone: unimodular. -/
theorem bubble_jac : |bubbleCone.det| = 1 := by
  simp [bubbleCone, Matrix.det_fin_two]
/-- I1 for the triangle cone: unimodular. -/
theorem tri_jac : |triCone.det| = 1 := by simp [triCone]

/-- The five 5-point tree cones (eq. 81) are unimodular (planted check, formalised). -/
theorem tree5_unimodular :
    |(!![1, 0; 0, 1] : Matrix (Fin 2) (Fin 2) ℤ).det| = 1 ∧ |(!![0, 1; -1,
        1] : Matrix (Fin 2) (Fin 2) ℤ).det| = 1 ∧
    |(!![-1, 1; -1, 0] : Matrix (Fin 2) (Fin 2) ℤ).det| = 1 ∧ |(!![-1, 0; 0,
        -1] : Matrix (Fin 2) (Fin 2) ℤ).det| = 1 ∧
    |(!![0, -1; 1, 0] : Matrix (Fin 2) (Fin 2) ℤ).det| = 1 := by
  simp [Matrix.det_fin_two]

/-- Projective slice of a 3-edge cone in coordinates (ρ₁, ρ₂): the 2-simplex. -/
def slice3 : Set (ℝ × ℝ) := regionBetween (fun _ => (0:ℝ)) (fun x => 1 - x) (Set.Icc 0 1)

/-- I2 for the triangle cone: the slice has Lebesgue volume 1/2. -/
theorem slice3_volume : volume slice3 = ENNReal.ofReal (1 / 2) := by
  have hg : IntegrableOn (fun x : ℝ => 1 - x) (Set.Icc 0 1) :=
    (continuous_const.sub continuous_id).integrableOn_Icc
  rw [slice3, Measure.volume_eq_prod, volume_regionBetween_eq_integral (f := fun _ : ℝ => (0:ℝ))
    (g := fun x : ℝ => 1 - x) (integrableOn_const (by simp)) hg
    measurableSet_Icc (fun x hx => by simpa using hx.2)]
  congr 1
  rw [integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le zero_le_one]
  simp only [Pi.sub_apply, sub_zero]
  rw [intervalIntegral.integral_sub intervalIntegrable_const intervalIntegral.intervalIntegrable_id]
  simp [integral_id]; norm_num

/-- I2 for the bubble cone: the slice (a unit segment) has volume 1. -/
theorem slice2_volume : volume (Set.Icc (0:ℝ) 1) = 1 := by simp

/-- SC2's triangle weight (1/2) equals the Lebesgue volume of the triangle cell slice (I2). (In SC2 the
weight is Γ-residue 1/2 × 2! × area 1/2, so this equality is the area identity.) -/
theorem triangle_weight_eq_cell_volume :
    ((PositiveGeometryEmergentSpaceTime.SC2.triangle.w : ℚ) : ℝ) = (volume slice3).toReal := by
  rw [slice3_volume, ENNReal.toReal_ofReal (by norm_num)]
  simp [PositiveGeometryEmergentSpaceTime.SC2.triangle]

/-- The SC-2 bubble factor ∫₀¹ x(1-x) = 1/6 (SC2) is neither cell volume of the bubble cone (I1 = 1,
  I2 = 1). -/
theorem bubble_factor_not_cell_volume :
    (∫ x in (0:ℝ)..1, x * (1 - x)) ≠ ((|bubbleCone.det| : ℤ) : ℝ) ∧
    ENNReal.ofReal (∫ x in (0:ℝ)..1, x * (1 - x)) ≠ volume (Set.Icc (0:ℝ) 1) := by
  rw [PositiveGeometryEmergentSpaceTime.SC2.bubble_param_integral, bubble_jac, slice2_volume]
  refine ⟨by norm_num, ?_⟩
  rw [Ne, ENNReal.ofReal_eq_one]; norm_num

/-- Non-vacuity witness: the comparison is discriminating — a non-unimodular cone has |det| = 2. -/
theorem witness_nonunimodular : |(!![1, 0; 1, 2] : Matrix (Fin 2) (Fin 2) ℤ).det| = 2 := by
  simp [Matrix.det_fin_two]

end PositiveGeometryEmergentSpaceTime.SC2b
