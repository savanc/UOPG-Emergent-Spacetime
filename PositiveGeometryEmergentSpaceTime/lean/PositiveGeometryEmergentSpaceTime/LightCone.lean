/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.Spinor
import PositiveGeometryEmergentSpaceTime.Null

/-!
# (e) in Minkowski coordinates: light-like separation ↔ ± rank-one Hermitian difference
-/

open Matrix

namespace PositiveGeometryEmergentSpaceTime

/-- `sigma` is additive in differences: `σ(u) − σ(w) = σ(u − w)`. -/
lemma sigma_sub (u w : Fin 4 → ℝ) : sigma u - sigma w = sigma (u - w) :=
  (sigmaL.map_sub u w).symm

/-- **(e)** Two events `u, w ∈ ℝ⁴` are light-like separated (η(u − w) = 0) iff
`σ(u) − σ(w) = ± v vᴴ` for some spinor `v ∈ ℂ²`. -/
theorem lightlike_iff_rank_one (u w : Fin 4 → ℝ) :
    minkowskiQuad (u - w) = 0 ↔ ∃ v : Fin 2 → ℂ, sigma u - sigma w = outerH v ∨
      sigma u - sigma w = -outerH v := by
  rw [sigma_sub, ← herm_det_eq_zero_iff (sigma_isHermitian _), det_sigma]
  exact_mod_cast Iff.rfl

end PositiveGeometryEmergentSpaceTime
