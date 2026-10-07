import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
MVP-0 core definitions.

`plucker` is the 2×2 minor on a pair of columns of a `2 × 4` matrix, the Plücker
coordinate of a 2-plane in 4-space. `det2` is the determinant of a `2 × 2` matrix.
Neither definition is an extra axiom, and neither is a mass formula.
-/

namespace UOPG0

variable {α : Type*}

/-- Determinant of a `2 × 2` matrix, written out so the later `ring` proofs do not
depend on a particular Mathlib lemma name. `det2_eq_det` identifies it with
`Matrix.det`. -/
def det2 [Ring α] (m : Matrix (Fin 2) (Fin 2) α) : α :=
  m 0 0 * m 1 1 - m 0 1 * m 1 0

/-- Plücker coordinate `Pᵢⱼ`, the maximal minor on columns `i` and `j`. -/
def plucker [Ring α] (C : Matrix (Fin 2) (Fin 4) α) (i j : Fin 4) : α :=
  C 0 i * C 1 j - C 1 i * C 0 j

/-- The quadratic Plücker polynomial. It vanishes on every real 2-plane. -/
def pluckerQuad [Ring α] (C : Matrix (Fin 2) (Fin 4) α) : α :=
  plucker C 0 1 * plucker C 2 3 - plucker C 0 2 * plucker C 1 3 + plucker C 0 3 * plucker C 1 2

/-- Polar bilinear form of `pluckerQuad`. For a decomposable bivector,
`pairing C C = 2 * pluckerQuad C`. -/
def pairing [Ring α] (C D : Matrix (Fin 2) (Fin 4) α) : α :=
  plucker C 0 1 * plucker D 2 3 + plucker D 0 1 * plucker C 2 3
    - plucker C 0 2 * plucker D 1 3 - plucker D 0 2 * plucker C 1 3
    + plucker C 0 3 * plucker D 1 2 + plucker D 0 3 * plucker C 1 2

lemma det2_eq_det [CommRing α] (m : Matrix (Fin 2) (Fin 2) α) : det2 m = m.det :=
  (Matrix.det_fin_two m).symm

/-- Rows `(1 1 1 1)` and `(0 1 2 3)`. A rational point of the positive chamber. -/
def positiveExample : Matrix (Fin 2) (Fin 4) ℚ
  | 0, 0 => 1
  | 0, 1 => 1
  | 0, 2 => 1
  | 0, 3 => 1
  | 1, 0 => 0
  | 1, 1 => 1
  | 1, 2 => 2
  | 1, 3 => 3

end UOPG0
