/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# H-T5 certificate: an exact Ising point in the n = 6 ABJM orthogonal momentum amplituhedron

Star Ising network on 3 boundary spins with `tanh J = (1/2, 1/3, 1/4)`; boundary
correlations `⟨σᵢσⱼ⟩ = tᵢ tⱼ`; GP matrix `C` (3×6, positive OG branch); moment curve
`Λ` (rows `(1, x, …, x⁴)`, `x = 1..6`).  We certify `Y = C Λ`, the six adjacent brackets
`⟨Y i i+1⟩` and the sequence `⟨Y 1 j⟩` (sign flips `+ − + + −`: 3 = k flips).
Exact rationals, no `native_decide`.
-/

namespace PositiveGeometryEmergentSpaceTime.IsingTiling

/-- The certified 3×6 rational point of OG(3,6) used in the Ising tiling check. -/
def C : Matrix (Fin 3) (Fin 6) ℚ :=
  !![1, 1, 1/6, -1/6, -1/8, 1/8;
     -1/6, 1/6, 1, 1, 1/12, -1/12;
     1/8, -1/8, -1/12, 1/12, 1, 1]

/-- The 6×5 Vandermonde-type matrix `Λ_{ab} = (a + 1)^b`. -/
def Λ : Matrix (Fin 6) (Fin 5) ℚ := Matrix.of fun a b => ((a : ℚ) + 1) ^ (b : ℕ)

/-- The 3×5 product `C · Λ` written out explicitly (see `Y_eq`). -/
def Y : Matrix (Fin 3) (Fin 5) ℚ :=
  !![2, 71/24, 125/24, 341/24, 1721/24;
     2, 85/12, 295/12, 1015/12, 3403/12;
     2, 263/24, 1469/24, 8237/24, 46409/24]

/-- `C · Λ = Y` (exact rational matrix product). -/
theorem Y_eq : C * Λ = Y := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [C, Λ, Y, Matrix.mul_apply, Fin.sum_univ_succ] <;> norm_num

/-- Bracket `⟨Y j l⟩` (0-indexed particles).

Also known as: IsingTiling.br, ⟨Y j l⟩ Ising/positroid bracket.
-/
def isingBracket (j l : Fin 6) : ℚ := Matrix.det (Matrix.of ![Y 0, Y 1, Y 2, Λ j, Λ l])

/-- The split signature `(+1, −1, +1, −1, +1, −1)` defining OG(3,6). -/
def ogSignature : Fin 6 → ℚ := ![1, -1, 1, -1, 1, -1]

/-- `C η Cᵀ = 0`: the certified point lies in OG(3,6). -/
theorem C_orth (i j : Fin 3) : ∑ m, C i m * ogSignature m * C j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [C, ogSignature, Fin.sum_univ_succ] <;> norm_num

set_option maxHeartbeats 4000000 in
/-- The six cyclically adjacent brackets of the Ising point are `2040, 2094, 792, 2694, 1776, 6300`
  (all positive). -/
theorem adjacent_brackets :
    isingBracket 0 1 = 2040 ∧ isingBracket 1 2 = 2094 ∧ isingBracket 2 3 = 792 ∧ isingBracket 3 4 = 2694 ∧ isingBracket 4 5 = 1776 ∧
      isingBracket 5 0 = 6300 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingBracket, Y, Λ, Matrix.det_succ_row_zero, Fin.sum_univ_succ,
        Fin.succAbove] <;> norm_num

set_option maxHeartbeats 4000000 in
/-- The brackets `⟨0 j⟩` are `2040, −2082, 690, 6324, −6300` for `j = 1, …, 5`. -/
theorem first_row_brackets :
    isingBracket 0 1 = 2040 ∧ isingBracket 0 2 = -2082 ∧ isingBracket 0 3 = 690 ∧ isingBracket 0 4 = 6324 ∧ isingBracket 0 5 = -6300 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [isingBracket, Y, Λ, Matrix.det_succ_row_zero, Fin.sum_univ_succ,
        Fin.succAbove] <;> norm_num

/-- The certified point satisfies the n=6 sign-flip conditions: all adjacent brackets
positive and exactly `k = 3` sign flips in `⟨Y 1 j⟩`, j = 2..6. -/
theorem sign_flip_certificate :
    (0 < isingBracket 0 1 ∧ 0 < isingBracket 1 2 ∧ 0 < isingBracket 2 3 ∧ 0 < isingBracket 3 4 ∧ 0 < isingBracket 4 5 ∧ 0 < isingBracket 5 0) ∧
    (isingBracket 0 1 * isingBracket 0 2 < 0 ∧ isingBracket 0 2 * isingBracket 0 3 < 0 ∧ 0 < isingBracket 0 3 * isingBracket 0 4 ∧ isingBracket 0 4 * isingBracket 0 5 < 0) := by
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := adjacent_brackets
  obtain ⟨_, g2, g3, g4, g5⟩ := first_row_brackets
  rw [h1, h2, h3, h4, h5, h6, g2, g3, g4, g5]; norm_num

end PositiveGeometryEmergentSpaceTime.IsingTiling
