/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — LEAN-CERT-2 ties for the FR-WZW k = 0 certificate data (D173).
Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.LeanCert2.FrwzwK0p
import PositiveGeometryEmergentSpaceTime.LeanCert2.FrwzwK0m
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# LEAN-CERT-2 ties: the k = 0 FR-WZW rows from the symmetry action on `eps`

`sims/frwzw/rank_count.py` builds, at each of 40 kinematic points, three rows from the basis
`eps(P₁..P₄)·∏X`: cyclic `b(cycP) − b(P)`, reversal `b(revP) − σ b(P)`, parity `b(Pᵀ) + b(P)`.
For k = 0 the basis is `eps` alone. We prove symbolically, for any 2×2 matrices `P₁..P₄` over a
commutative ring with `P₅ = −ΣPᵢ` (momentum conservation):

* `eps_cyc`: `eps(P₂,P₃,P₄,P₅) = eps(P₁,P₂,P₃,P₄)` (cyclic row is 0);
* `eps_rev`: `eps(P₅,P₄,P₃,P₂) = eps(P₁,P₂,P₃,P₄)` (reversal row is `(1 − σ) eps`);
* `eps_par`: `eps(P₁ᵀ,…,P₄ᵀ) = −eps(P₁,…,P₄)` (parity row is 0).

So for σ = +1 every row vanishes (dim 1) and for σ = −1 exactly the reversal rows are `2 eps`.
The certificate data match this pattern entry by entry (`k0p_rows_zero`, `k0m_rows_pattern`; the generator
normalises each nonzero row to `±1`). The masslessness `det Pᵢ = 0` is not needed.
* Planted: dropping momentum conservation (`P₅ = 0`) breaks the cyclic identity.
* Non-vacuity: `eps ≠ 0` at the matrix-unit point.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LeanCert2Sanity
open Matrix PositiveGeometryEmergentSpaceTime.LeanCert2

variable {R : Type*} [CommRing R]

/-- Components of a 2×2 matrix as a row (`vec` in `rank_count.py`). -/
def vecM (P : Matrix (Fin 2) (Fin 2) R) : Fin 4 → R := fun k =>
  match k with
  | 0 => P 0 0
  | 1 => P 0 1
  | 2 => P 1 0
  | 3 => P 1 1

/-- `eps(a,b,c,d)` = 4×4 determinant of the stacked component rows. -/
def eps (a b c d : Matrix (Fin 2) (Fin 2) R) : R :=
  (Matrix.of fun i : Fin 4 => match i with
    | 0 => vecM a
    | 1 => vecM b
    | 2 => vecM c
    | 3 => vecM d).det

/-- Cofactor expansion of a 4×4 determinant (helper). -/
theorem det4 (M : Matrix (Fin 4) (Fin 4) R) : M.det =
    M 0 0 * (M 1 1 * (M 2 2 * M 3 3 - M 2 3 * M 3 2) - M 1 2 * (M 2 1 * M 3 3 - M 2 3 * M 3 1)
        + M 1 3 * (M 2 1 * M 3 2 - M 2 2 * M 3 1))
    - M 0 1 * (M 1 0 * (M 2 2 * M 3 3 - M 2 3 * M 3 2) - M 1 2 * (M 2 0 * M 3 3 - M 2 3 * M 3 0)
        + M 1 3 * (M 2 0 * M 3 2 - M 2 2 * M 3 0))
    + M 0 2 * (M 1 0 * (M 2 1 * M 3 3 - M 2 3 * M 3 1) - M 1 1 * (M 2 0 * M 3 3 - M 2 3 * M 3 0)
        + M 1 3 * (M 2 0 * M 3 1 - M 2 1 * M 3 0))
    - M 0 3 * (M 1 0 * (M 2 1 * M 3 2 - M 2 2 * M 3 1) - M 1 1 * (M 2 0 * M 3 2 - M 2 2 * M 3 0)
        + M 1 2 * (M 2 0 * M 3 1 - M 2 1 * M 3 0)) := by
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_succ, Matrix.det_succ_row_zero, Fin.succAbove, Matrix.submatrix]
  ring

/-- Cyclic identity under momentum conservation. -/
theorem eps_cyc (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    eps P2 P3 P4 (-(P1 + P2 + P3 + P4)) = eps P1 P2 P3 P4 := by
  simp only [eps, det4, Matrix.of_apply, vecM, Matrix.neg_apply, Matrix.add_apply]; ring

/-- Reversal identity under momentum conservation. -/
theorem eps_rev (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    eps (-(P1 + P2 + P3 + P4)) P4 P3 P2 = eps P1 P2 P3 P4 := by
  simp only [eps, det4, Matrix.of_apply, vecM, Matrix.neg_apply, Matrix.add_apply]; ring

/-- Parity (transpose) is odd on `eps`. -/
theorem eps_par (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    eps P1ᵀ P2ᵀ P3ᵀ P4ᵀ = -eps P1 P2 P3 P4 := by
  simp only [eps, det4, Matrix.of_apply, vecM, Matrix.transpose_apply]; ring

/-- Symbolic k = 0 rows: for σ = +1 all three rows vanish; for σ = −1 the reversal row is `2 eps`. -/
theorem k0_rows (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) (sg : R) :
    eps P2 P3 P4 (-(P1 + P2 + P3 + P4)) - eps P1 P2 P3 P4 = 0 ∧
    eps (-(P1 + P2 + P3 + P4)) P4 P3 P2 - sg * eps P1 P2 P3 P4 = (1 - sg) * eps P1 P2 P3 P4 ∧
    eps P1ᵀ P2ᵀ P3ᵀ P4ᵀ + eps P1 P2 P3 P4 = 0 := by
  refine ⟨by rw [eps_cyc]; ring, by rw [eps_rev]; ring, by rw [eps_par]; ring⟩

/-- Data tie (σ = +1): every row of the k = 0, σ = +1 certificate matrix is `[0]`. -/
theorem k0p_rows_zero : frwzw_k0p_Mr.length = 120 ∧ frwzw_k0p_Mr.all (· = [0]) = true := by
  decide +kernel

/-- Data tie (σ = −1): rows `3p` (cyclic) and `3p+2` (parity) are `[0]`; rows `3p+1` (reversal) are `[±1]`. -/
theorem k0m_rows_pattern : frwzw_k0m_Mr.length = 120 ∧
    (List.range 120).all (fun i => if i % 3 = 1 then
      (frwzw_k0m_Mr.getD i [] = [1] || frwzw_k0m_Mr.getD i [] = [-1]) else frwzw_k0m_Mr.getD i [] = [0]) = true := by
  decide +kernel

/-- Matrix unit `E i j`. -/
def E (i j : Fin 2) : Matrix (Fin 2) (Fin 2) ℚ := fun a b => if a = i ∧ b = j then 1 else 0

/-- Non-vacuity: `eps ≠ 0` at the matrix-unit point (so the σ = −1 reversal rows are nonzero). -/
theorem eps_units : eps (E 0 0) (E 0 1) (E 1 0) (E 1 1) = 1 := by
  simp only [eps, det4, Matrix.of_apply, vecM, E]; norm_num

/-- Planted: without momentum conservation (`P₅ = 0`) the cyclic identity fails. -/
theorem planted_no_conservation : eps (E 0 1) (E 1 0) (E 1 1) 0 ≠ eps (E 0 0) (E 0 1) (E 1 0) (E 1 1) := by
  rw [eps_units]; simp only [eps, det4, Matrix.of_apply, vecM, E, Matrix.zero_apply]; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LeanCert2Sanity
