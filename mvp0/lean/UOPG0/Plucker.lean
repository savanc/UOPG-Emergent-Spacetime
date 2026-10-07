import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Abel
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import UOPG0.Basic

/-!
Algebraic content of MVP-0 that holds over any commutative ring.

* the Plücker quadratic vanishes for every `2 × 4` matrix
* left `GL(2)` multiplies every Plücker coordinate by `det`
* therefore `SL(2)` (`det = 1`) leaves the coordinates fixed
-/

namespace UOPG0

variable {α : Type*} [CommRing α]

theorem plucker_relation (C : Matrix (Fin 2) (Fin 4) α) : pluckerQuad C = 0 := by
  simp only [pluckerQuad, plucker]
  ring

/-- Left multiplication by `g` scales every minor by `det2 g`. -/
theorem plucker_gl_weight (g : Matrix (Fin 2) (Fin 2) α) (C : Matrix (Fin 2) (Fin 4) α)
    (i j : Fin 4) : plucker (g * C) i j = det2 g * plucker C i j := by
  simp only [plucker, det2, Matrix.mul_apply, Fin.sum_univ_two]
  ring

theorem plucker_sl_invariant (g : Matrix (Fin 2) (Fin 2) α) (C : Matrix (Fin 2) (Fin 4) α)
    (hg : det2 g = 1) (i j : Fin 4) : plucker (g * C) i j = plucker C i j := by
  rw [plucker_gl_weight, hg, one_mul]

/-- The same weight, stated with Mathlib's determinant. -/
theorem plucker_gl_weight_det (g : Matrix (Fin 2) (Fin 2) α) (C : Matrix (Fin 2) (Fin 4) α)
    (i j : Fin 4) : plucker (g * C) i j = g.det * plucker C i j := by
  rw [← det2_eq_det, plucker_gl_weight]

theorem plucker_specialLinear_invariant (g : Matrix (Fin 2) (Fin 2) α)
    (C : Matrix (Fin 2) (Fin 4) α) (hg : g.det = 1) (i j : Fin 4) :
    plucker (g * C) i j = plucker C i j := by
  rw [plucker_gl_weight_det, hg, one_mul]

end UOPG0
