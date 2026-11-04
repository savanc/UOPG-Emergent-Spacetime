/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# H-T5d certificate: exact Ising points in the five n = 10 tree-network tiles of OG≥0(5,10)

For each trivalent tree Ising network T_x (x = 1..5; leaf x on the middle vertex, cherries (x+1,x+2), (x+3,x+4)),
with tanh J = 1/2 on all seven edges, the GP matrix `Cx` satisfies `Cx η Cxᵀ = 0`. Three of its five consecutive
5×5 minors vanish, and the other two are nonzero (positive). Columns are 0-indexed.
-/

namespace PositiveGeometryEmergentSpaceTime.IsingTiling10

/-- The alternating signature `(+1, −1, …)` on 10 coordinates defining OG(5,10).

Also known as: OG eta, OG signature (+−+−…).
-/
def ogSignature : Fin 10 → ℚ := ![1, -1, 1, -1, 1, -1, 1, -1, 1, -1]

/-- Minor on columns a, b, c, d, e. -/
def isingMinor (C : Matrix (Fin 5) (Fin 10) ℚ) (a b c d e : Fin 10) : ℚ :=
  Matrix.det (Matrix.of fun r j : Fin 5 => C r (![a, b, c, d, e] j))

/-- Explicit 5×10 rational point `C1` (one of the five certified OG(5,10) points of the n = 10
  tiling check). -/
def C1 : Matrix (Fin 5) (Fin 10) ℚ :=
  !![1, 1, 1/8, -1/8, -1/8, 1/8, 1/8, -1/8, -1/8, 1/8;
     -1/8, 1/8, 1, 1, 1/4, -1/4, -1/16, 1/16, 1/16, -1/16;
     1/8, -1/8, -1/4, 1/4, 1, 1, 1/16, -1/16, -1/16, 1/16;
     -1/8, 1/8, 1/16, -1/16, -1/16, 1/16, 1, 1, 1/4, -1/4;
     1/8, -1/8, -1/16, 1/16, 1/16, -1/16, -1/4, 1/4, 1, 1]

/-- `C1 η C1ᵀ = 0` with η the alternating signature: `C1` lies in OG(5,10). -/
theorem C1_orth (i j : Fin 5) : ∑ m, C1 i m * ogSignature m * C1 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C1, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 8000000 in
/-- Exact values of the listed cyclically consecutive 5×5 minors of `C1` (kernel-checked rational
  arithmetic). -/
theorem C1_minors :
    isingMinor C1 0 1 2 3 4 = 0 ∧ isingMinor C1 1 2 3 4 5 = 0 ∧ isingMinor C1 2 3 4 5 6 = 0 ∧ isingMinor C1 3 4 5 6 7 = 9/128 ∧ isingMinor C1 4 5 6 7 8 = 9/128 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C1, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

/-- Explicit 5×10 rational point `C2` (one of the five certified OG(5,10) points of the n = 10
  tiling check). -/
def C2 : Matrix (Fin 5) (Fin 10) ℚ :=
  !![1, 1, 1/8, -1/8, -1/16, 1/16, 1/16, -1/16, -1/4, 1/4;
     -1/8, 1/8, 1, 1, 1/8, -1/8, -1/8, 1/8, 1/8, -1/8;
     1/16, -1/16, -1/8, 1/8, 1, 1, 1/4, -1/4, -1/16, 1/16;
     -1/16, 1/16, 1/8, -1/8, -1/4, 1/4, 1, 1, 1/16, -1/16;
     1/4, -1/4, -1/8, 1/8, 1/16, -1/16, -1/16, 1/16, 1, 1]

/-- `C2 η C2ᵀ = 0` with η the alternating signature: `C2` lies in OG(5,10). -/
theorem C2_orth (i j : Fin 5) : ∑ m, C2 i m * ogSignature m * C2 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C2, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 8000000 in
/-- Exact values of the listed cyclically consecutive 5×5 minors of `C2` (kernel-checked rational
  arithmetic). -/
theorem C2_minors :
    isingMinor C2 0 1 2 3 4 = 9/128 ∧ isingMinor C2 1 2 3 4 5 = 9/128 ∧ isingMinor C2 2 3 4 5 6 = 0 ∧ isingMinor C2 3 4 5 6 7 = 0 ∧ isingMinor C2 4 5 6 7 8 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C2, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

/-- Explicit 5×10 rational point `C3` (one of the five certified OG(5,10) points of the n = 10
  tiling check). -/
def C3 : Matrix (Fin 5) (Fin 10) ℚ :=
  !![1, 1, 1/4, -1/4, -1/8, 1/8, 1/16, -1/16, -1/16, 1/16;
     -1/4, 1/4, 1, 1, 1/8, -1/8, -1/16, 1/16, 1/16, -1/16;
     1/8, -1/8, -1/8, 1/8, 1, 1, 1/8, -1/8, -1/8, 1/8;
     -1/16, 1/16, 1/16, -1/16, -1/8, 1/8, 1, 1, 1/4, -1/4;
     1/16, -1/16, -1/16, 1/16, 1/8, -1/8, -1/4, 1/4, 1, 1]

/-- `C3 η C3ᵀ = 0` with η the alternating signature: `C3` lies in OG(5,10). -/
theorem C3_orth (i j : Fin 5) : ∑ m, C3 i m * ogSignature m * C3 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C3, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 8000000 in
/-- Exact values of the listed cyclically consecutive 5×5 minors of `C3` (kernel-checked rational
  arithmetic). -/
theorem C3_minors :
    isingMinor C3 0 1 2 3 4 = 0 ∧ isingMinor C3 1 2 3 4 5 = 0 ∧ isingMinor C3 2 3 4 5 6 = 9/128 ∧ isingMinor C3 3 4 5 6 7 = 9/128 ∧ isingMinor C3 4 5 6 7 8 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C3, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

/-- Explicit 5×10 rational point `C4` (one of the five certified OG(5,10) points of the n = 10
  tiling check). -/
def C4 : Matrix (Fin 5) (Fin 10) ℚ :=
  !![1, 1, 1/16, -1/16, -1/16, 1/16, 1/8, -1/8, -1/4, 1/4;
     -1/16, 1/16, 1, 1, 1/4, -1/4, -1/8, 1/8, 1/16, -1/16;
     1/16, -1/16, -1/4, 1/4, 1, 1, 1/8, -1/8, -1/16, 1/16;
     -1/8, 1/8, 1/8, -1/8, -1/8, 1/8, 1, 1, 1/8, -1/8;
     1/4, -1/4, -1/16, 1/16, 1/16, -1/16, -1/8, 1/8, 1, 1]

/-- `C4 η C4ᵀ = 0` with η the alternating signature: `C4` lies in OG(5,10). -/
theorem C4_orth (i j : Fin 5) : ∑ m, C4 i m * ogSignature m * C4 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C4, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 8000000 in
/-- Exact values of the listed cyclically consecutive 5×5 minors of `C4` (kernel-checked rational
  arithmetic). -/
theorem C4_minors :
    isingMinor C4 0 1 2 3 4 = 9/128 ∧ isingMinor C4 1 2 3 4 5 = 0 ∧ isingMinor C4 2 3 4 5 6 = 0 ∧ isingMinor C4 3 4 5 6 7 = 0 ∧ isingMinor C4 4 5 6 7 8 = 9/128 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C4, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

/-- Explicit 5×10 rational point `C5` (one of the five certified OG(5,10) points of the n = 10
  tiling check). -/
def C5 : Matrix (Fin 5) (Fin 10) ℚ :=
  !![1, 1, 2/3, -2/3, -4/9, 4/9, 4/9, -4/9, -1/3, 1/3;
     -2/3, 2/3, 1, 1, 4/9, -4/9, -4/9, 4/9, 1/3, -1/3;
     4/9, -4/9, -4/9, 4/9, 1, 1, 2/3, -2/3, -1/3, 1/3;
     -4/9, 4/9, 4/9, -4/9, -2/3, 2/3, 1, 1, 1/3, -1/3;
     1/3, -1/3, -1/3, 1/3, 1/3, -1/3, -1/3, 1/3, 1, 1]

/-- `C5 η C5ᵀ = 0` with η the alternating signature: `C5` lies in OG(5,10). -/
theorem C5_orth (i j : Fin 5) : ∑ m, C5 i m * ogSignature m * C5 j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C5, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 8000000 in
/-- Exact values of the listed cyclically consecutive 5×5 minors of `C5` (kernel-checked rational
  arithmetic). -/
theorem C5_minors :
    isingMinor C5 0 1 2 3 4 = 0 ∧ isingMinor C5 1 2 3 4 5 = 8/81 ∧ isingMinor C5 2 3 4 5 6 = 8/81 ∧ isingMinor C5 3 4 5 6 7 = 0 ∧ isingMinor C5 4 5 6 7 8 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingMinor, C5, Matrix.det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove] <;> norm_num

end PositiveGeometryEmergentSpaceTime.IsingTiling10
