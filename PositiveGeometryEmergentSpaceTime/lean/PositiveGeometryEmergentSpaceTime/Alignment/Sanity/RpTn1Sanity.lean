/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — RP-TN-1 sanity and tie theorems for `RpTn1.corr2` (D184).
Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.RpTn1
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.BigOperators.Fin

/-!
# RP-TN-1 sanity

* Tie (D184): `corr2` is the spectral form of a two-state transfer matrix, and its reflected Gram form
  is a sum of weighted squares (`gram_form`), so reflection positivity of `corr2` holds for every finite
  family of times, not just the 2×2 minors of `RpTn1`.
* Known values: Hankel minor `1/36` at `w = (1,1)`, `x = (1/2, 1/3)`, agreeing with the factorisation.
* Planted: a negative weight breaks the Hankel minor; `a = 0` makes the Toeplitz minor vanish (so the
  `a ≠ 0` hypothesis of `toeplitz2_minor_neg` is needed).
* Non-vacuity: the Gram form is strictly positive on a nonzero vector.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.RpTn1Sanity
open PositiveGeometryEmergentSpaceTime.RpTn1 Finset

/-- Tie: `corr2 = u₁² x₁ᵗ + u₂² x₂ᵗ` is the `t`-th power of the diagonal transfer matrix read in a state
with amplitudes `uᵢ = √wᵢ`. -/
theorem corr2_spectral (u₁ u₂ x₁ x₂ : ℝ) (t : ℕ) :
    corr2 (u₁ ^ 2) (u₂ ^ 2) x₁ x₂ t = u₁ * x₁ ^ t * u₁ + u₂ * x₂ ^ t * u₂ := by
  unfold corr2; ring

/-- Tie: the reflected Gram form of `corr2` over any finite family of times is a weighted sum of squares. -/
theorem gram_form {ι : Type*} (s : Finset ι) (v : ι → ℝ) (t : ι → ℕ) (w₁ w₂ x₁ x₂ : ℝ) :
    ∑ i ∈ s, ∑ j ∈ s, v i * v j * corr2 w₁ w₂ x₁ x₂ (t i + t j)
      = w₁ * (∑ i ∈ s, v i * x₁ ^ t i) ^ 2 + w₂ * (∑ i ∈ s, v i * x₂ ^ t i) ^ 2 := by
  rw [sq, sq, Finset.sum_mul_sum, Finset.sum_mul_sum, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun j _ => ?_
  unfold corr2; rw [pow_add, pow_add]; ring

/-- Consequence: reflection positivity of `corr2` for nonnegative weights (any family, any nodes). -/
theorem gram_nonneg {ι : Type*} (s : Finset ι) (v : ι → ℝ) (t : ι → ℕ) (w₁ w₂ x₁ x₂ : ℝ)
    (hw₁ : 0 ≤ w₁) (hw₂ : 0 ≤ w₂) :
    0 ≤ ∑ i ∈ s, ∑ j ∈ s, v i * v j * corr2 w₁ w₂ x₁ x₂ (t i + t j) := by
  rw [gram_form]; positivity

/-- Known value: the reflected 2×2 minor is `1/36` at `w = (1,1)`, `x = (1/2,1/3)`, `a = c = 0`, `k = l = 1`,
and equals the factorised form of `hankel2_minor_identity`. -/
theorem hankel_value :
    corr2 1 1 (1 / 2) (1 / 3) 0 * corr2 1 1 (1 / 2) (1 / 3) 2 - corr2 1 1 (1 / 2) (1 / 3) 1 ^ 2 = 1 / 36 ∧
      (1 : ℝ) * 1 * ((1 / 2) * (1 / 3)) ^ 0 * (((1 / 3) ^ 1 - (1 / 2) ^ 1) * ((1 / 3) ^ 1 - (1 / 2) ^ 1)) = 1 / 36 := by
  unfold corr2; norm_num

/-- Known value: the Toeplitz minor at the same point is `−1/36`. -/
theorem toeplitz_value :
    corr2 1 1 (1 / 2) (1 / 3) 1 * corr2 1 1 (1 / 2) (1 / 3) 1
      - corr2 1 1 (1 / 2) (1 / 3) 0 * corr2 1 1 (1 / 2) (1 / 3) 2 = -1 / 36 := by
  unfold corr2; norm_num

/-- Planted: a negative weight `w₂ = −1` breaks the reflected minor (so `0 ≤ w₂` is needed). -/
theorem planted_neg_weight :
    corr2 1 (-1) (1 / 2) (1 / 3) 0 * corr2 1 (-1) (1 / 2) (1 / 3) 2 - corr2 1 (-1) (1 / 2) (1 / 3) 1 ^ 2 < 0 := by
  unfold corr2; norm_num

/-- Planted: with `a = 0` the Toeplitz minor is identically zero (so `a ≠ 0` is needed for strictness). -/
theorem planted_a_zero (w₁ w₂ x₁ x₂ : ℝ) (b : ℕ) :
    corr2 w₁ w₂ x₁ x₂ 0 * corr2 w₁ w₂ x₁ x₂ b - corr2 w₁ w₂ x₁ x₂ 0 * corr2 w₁ w₂ x₁ x₂ (0 + b) = 0 := by
  simp

/-- Non-vacuity: the Gram form is strictly positive for `v = (1, −1)` at times `(0, 1)`. -/
theorem nonvacuous :
    0 < ∑ i ∈ (univ : Finset (Fin 2)), ∑ j ∈ (univ : Finset (Fin 2)),
      (fun k : Fin 2 => if k = 0 then (1 : ℝ) else -1) i * (fun k : Fin 2 => if k = 0 then (1 : ℝ) else -1) j *
        corr2 1 1 (1 / 2) (1 / 3) ((fun k : Fin 2 => (k : ℕ)) i + (fun k : Fin 2 => (k : ℕ)) j) := by
  simp [Fin.sum_univ_two, corr2]; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.RpTn1Sanity
