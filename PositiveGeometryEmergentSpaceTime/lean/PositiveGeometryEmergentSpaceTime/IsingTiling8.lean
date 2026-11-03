/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# H-T5b certificate: exact Ising points in the two n = 8 HW/BCFW cells of OG≥0(4,8)

Network N1 with one boundary edge deleted (tanh J = 1/2 on the five remaining edges), mapped by the
GP map. `C0` lies in cell (4,6,7,1,8,2,3,5) (HW σ2: M₁ = M₅ = 0) and `C2` lies in cell
(5,7,6,8,1,3,2,4) (HW σ1: M₃ = M₇ = 0). We certify `C η Cᵀ = 0`, the two vanishing consecutive minors of each cell, and three nonzero (positive) ones.
Columns are 0-indexed.
-/

namespace PositiveGeometryEmergentSpaceTime.IsingTiling8

/-- The alternating signature `(+1, −1, …)` on 8 coordinates defining OG(4,8).

Also known as: OG eta, OG signature (+−+−…).
-/
def ogSignature : Fin 8 → ℚ := ![1, -1, 1, -1, 1, -1, 1, -1]

/-- Explicit 4×8 rational point `C0` (one of the certified OG(4,8) points of the n = 8 tiling
  check). -/
def C0 : Matrix (Fin 4) (Fin 8) ℚ :=
  !![1, 1, 2/3, -2/3, -1/3, 1/3, 1/3, -1/3;
     -2/3, 2/3, 1, 1, 1/3, -1/3, -1/3, 1/3;
     1/3, -1/3, -1/3, 1/3, 1, 1, 1/4, -1/4;
     -1/3, 1/3, 1/3, -1/3, -1/4, 1/4, 1, 1]

/-- Explicit 4×8 rational point `C2` (one of the certified OG(4,8) points of the n = 8 tiling
  check). -/
def C2 : Matrix (Fin 4) (Fin 8) ℚ :=
  !![1, 1, 1/3, -1/3, -1/3, 1/3, 1/4, -1/4;
     -1/3, 1/3, 1, 1, 2/3, -2/3, -1/3, 1/3;
     1/3, -1/3, -2/3, 2/3, 1, 1, 1/3, -1/3;
     -1/4, 1/4, 1/3, -1/3, -1/3, 1/3, 1, 1]

/-- Minor on columns a, b, c, d. -/
def isingMinor (C : Matrix (Fin 4) (Fin 8) ℚ) (a b c d : Fin 8) : ℚ :=
  Matrix.det (Matrix.of fun r j : Fin 4 => C r (![a, b, c, d] j))

/-- `C0 η C0ᵀ = 0` with η the alternating signature: `C0` lies in OG(4,8). -/
theorem C0_orth (i j : Fin 4) : ∑ m, C0 i m * ogSignature m * C0 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C0, ogSignature, Fin.sum_univ_succ] <;> norm_num

/-- `C2 η C2ᵀ = 0` with η the alternating signature: `C2` lies in OG(4,8). -/
theorem C2_orth (i j : Fin 4) : ∑ m, C2 i m * ogSignature m * C2 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C2, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 4000000 in
/-- Exact values of the listed cyclically consecutive 4×4 minors of `C0` (kernel-checked rational
  arithmetic). -/
theorem C0_minors :
    isingMinor C0 0 1 2 3 = 0 ∧ isingMinor C0 1 2 3 4 = 1/6 ∧ isingMinor C0 2 3 4 5 = 2/9 ∧ isingMinor C0 3 4 5 6 = 1/6 ∧ isingMinor C0 4 5 6 7 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C0, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

set_option maxHeartbeats 4000000 in
/-- Exact values of the listed cyclically consecutive 4×4 minors of `C2` (kernel-checked rational
  arithmetic). -/
theorem C2_minors :
    isingMinor C2 0 1 2 3 = 2/9 ∧ isingMinor C2 1 2 3 4 = 1/6 ∧ isingMinor C2 2 3 4 5 = 0 ∧ isingMinor C2 3 4 5 6 = 1/6 ∧ isingMinor C2 6 7 0 1 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C2, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

end PositiveGeometryEmergentSpaceTime.IsingTiling8
