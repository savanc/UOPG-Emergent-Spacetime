/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# (f) Stretch: the affine chart `X ↦ rowspan [I | X]` of Gr(2,4) and the Klein quadric

For any 2×2 matrix `X` over a commutative ring, the 2×4 matrix `[I | X]` has Plücker
coordinates `(p₀₁, p₀₂, p₀₃, p₁₂, p₁₃, p₂₃) = (1, X₁₀, X₁₁, -X₀₀, -X₀₁, det X)` and they satisfy
the Plücker (Klein-quadric) relation `p₀₁p₂₃ − p₀₂p₁₃ + p₀₃p₁₂ = 0`. Conversely every
point of the quadric with `p₀₁ = 1` comes from exactly one `X`. So the chart `{p₀₁ ≠ 0}` of the
Klein quadric *is* the space of 2×2 matrices: Plücker coordinates are derived from the
spinor/matrix picture rather than assumed. The relation itself is the same statement as
`plucker_relation` in savanc/UOPG-Emergent-Spacetime (mvp0), reproved here in this setting.
-/

open Matrix

namespace PositiveGeometryEmergentSpaceTime

variable {R : Type*} [CommRing R]

/-- Plücker coordinate: the 2×2 minor on columns `i, j`. -/
def pl (P : Matrix (Fin 2) (Fin 4) R) (i j : Fin 4) : R :=
  (P.submatrix id ![i, j]).det

/-- Unfolded form of the 2×4 Plücker coordinate: `pl P i j = P₀ᵢ P₁ⱼ − P₀ⱼ P₁ᵢ`. -/
lemma pl_eq (P : Matrix (Fin 2) (Fin 4) R) (i j : Fin 4) :
    pl P i j = P 0 i * P 1 j - P 0 j * P 1 i := by
  simp [pl, det_fin_two]

/-- Plücker relation for any 2×4 matrix. -/
theorem plucker_rel (P : Matrix (Fin 2) (Fin 4) R) :
    pl P 0 1 * pl P 2 3 - pl P 0 2 * pl P 1 3 + pl P 0 3 * pl P 1 2 = 0 := by
  simp only [pl_eq]; ring

/-- The chart `[I | X]`. -/
def chart (X : Matrix (Fin 2) (Fin 2) R) : Matrix (Fin 2) (Fin 4) R :=
  !![1, 0, X 0 0, X 0 1; 0, 1, X 1 0, X 1 1]

/-- Plücker coordinates of the affine chart `[1 | X]`: `p₀₁ = 1`, `p₀₂ = X₁₀`, `p₀₃ = X₁₁`, `p₁₂ =
  −X₀₀`, `p₁₃ = −X₀₁`, `p₂₃ = det X`. -/
theorem chart_pl (X : Matrix (Fin 2) (Fin 2) R) :
    pl (chart X) 0 1 = 1 ∧ pl (chart X) 0 2 = X 1 0 ∧ pl (chart X) 0 3 = X 1 1 ∧
    pl (chart X) 1 2 = -X 0 0 ∧ pl (chart X) 1 3 = -X 0 1 ∧ pl (chart X) 2 3 = X.det := by
  simp [pl_eq, chart, det_fin_two]

/-- The image of the chart lies on the Klein quadric. -/
theorem chart_klein (X : Matrix (Fin 2) (Fin 2) R) :
    pl (chart X) 0 1 * pl (chart X) 2 3 - pl (chart X) 0 2 * pl (chart X) 1 3
      + pl (chart X) 0 3 * pl (chart X) 1 2 = 0 :=
  plucker_rel _

/-- **(f)** The chart is a bijection onto the affine piece `{p₀₁ = 1}` of the Klein quadric:
every sextuple with `p₀₁ = 1` satisfying the Plücker relation is the Plücker vector of
exactly one `[I | X]`. -/
theorem klein_affine_chart (p01 p02 p03 p12 p13 p23 : R) (h1 : p01 = 1)
    (hq : p01 * p23 - p02 * p13 + p03 * p12 = 0) :
    ∃! X : Matrix (Fin 2) (Fin 2) R,
      pl (chart X) 0 1 = p01 ∧ pl (chart X) 0 2 = p02 ∧ pl (chart X) 0 3 = p03 ∧
      pl (chart X) 1 2 = p12 ∧ pl (chart X) 1 3 = p13 ∧ pl (chart X) 2 3 = p23 := by
  refine ⟨!![-p12, -p13; p02, p03], ?_, ?_⟩
  · simp only [pl_eq, chart]
    simp
    subst h1
    exact ⟨rfl, by linear_combination (-1 : R) * hq⟩
  · rintro Y ⟨-, h2, h3, h4, h5, -⟩
    simp only [pl_eq, chart] at h2 h3 h4 h5
    simp at h2 h3 h4 h5
    ext i j
    fin_cases i <;> fin_cases j <;> simp [← h2, ← h3, ← h4, ← h5]

end PositiveGeometryEmergentSpaceTime
