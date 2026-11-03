/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MG2-1: Coulomb-branch algebra behind CGW 2601.16860 §VI.B (CITED).
⟨Φ⟩ = diag(v_i); particle i between index lines i, i+1 has κ_i = g(v_i - v_{i+1}), m_i = |κ_i|.
Planar shift X̃_{ij} = X_{ij} - g²(v_i - v_j)² (eq. 56); c_{ij} = X_{ij} + X_{i+1,j+1} - X_{i,j+1} - X_{i+1,j}.
-/

namespace PositiveGeometryEmergentSpaceTime.CoulombZero

/-- Second difference `c_ij = X_ij + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j}` of planar variables. -/
def cvar (X : ℕ → ℕ → ℝ) (i j : ℕ) : ℝ := X i j + X (i+1) (j+1) - X i (j+1) - X (i+1) j

/-- Shifted planar variables `X̃_ij = X_ij − g²(v_i − v_j)²`. -/
def Xt (g : ℝ) (v : ℕ → ℝ) (X : ℕ → ℕ → ℝ) (i j : ℕ) : ℝ := X i j - g^2 * (v i - v j)^2

/-- CGW eq. (57): c̃_{ij} = c_{ij} + 2 g²(v_i - v_{i+1})(v_j - v_{j+1}) = c_{ij} + 2 κ_i κ_j. -/
theorem eq57 (g : ℝ) (v : ℕ → ℝ) (X : ℕ → ℕ → ℝ) (i j : ℕ) :
    cvar (Xt g v X) i j = cvar X i j + 2 * (g * (v i - v (i+1))) * (g * (v j - v (j+1))) := by
  unfold cvar Xt; ring

/-- Mass form of eq. 57 up to sign: |2κ_iκ_j| = 2 m_i m_j. -/
theorem eq57_mass (g : ℝ) (v : ℕ → ℝ) (i j : ℕ) :
    |2 * (g * (v i - v (i+1))) * (g * (v j - v (j+1)))|
      = 2 * |g * (v i - v (i+1))| * |g * (v j - v (j+1))| := by
  rw [abs_mul, abs_mul]; norm_num

/-- Masses are differences of vev eigenvalues: κ's around a closed ordered amplitude sum to zero. -/
theorem kappa_sum4 (v : ℕ → ℝ) :
    (v 0 - v 1) + (v 1 - v 2) + (v 2 - v 3) + (v 3 - v 0) = 0 := by ring

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- D1 triangle: for ordered collinear vevs, m_ik = m_ij + m_jk. -/
@[nolint unusedArguments]
theorem D1_additive (g a b c : ℝ) (hg : 0 ≤ g) (h1 : b ≤ a) (h2 : c ≤ b) :
    g * |a - c| = g * |a - b| + g * |b - c| := by
  rw [abs_of_nonneg (by linarith : (0:ℝ) ≤ a - c), abs_of_nonneg (by linarith : (0:ℝ) ≤ a - b),
      abs_of_nonneg (by linarith : (0:ℝ) ≤ b - c)]; ring

/-- D1 general: triangle inequality m_ik ≤ m_ij + m_jk. -/
theorem D1_triangle (g a b c : ℝ) (hg : 0 ≤ g) : g * |a - c| ≤ g * |a - b| + g * |b - c| := by
  rw [← mul_add]; exact mul_le_mul_of_nonneg_left (abs_sub_le a b c) hg

/-- Null embedding (CGW eq. 58): K = (p, κ) with p² = κ² is null. -/
theorem null_embed (p2 κ : ℝ) (h : p2 = κ^2) : p2 - κ^2 = 0 := by rw [h]; ring

end PositiveGeometryEmergentSpaceTime.CoulombZero
