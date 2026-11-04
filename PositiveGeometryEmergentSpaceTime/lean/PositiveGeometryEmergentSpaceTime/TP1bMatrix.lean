/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.TP1b

/-!
# TP-1b in matrix form (audit item A-6, 2026-10-13)

`adjE8` is the adjacency matrix of the E8 Dynkin diagram (the T(2,3,5) tree: chain 0–1–2–3–4–5–6
with node 7 attached to node 2), and `cartanE8 = 2·1 − adjE8` is the E8 Cartan matrix (simply laced).
We restate `TP1b.eigen` as a matrix eigen-equation and prove the Perron–Frobenius properties:

* `pf_abs_le`: for any entrywise nonnegative real matrix with a strictly positive eigenvector of
  eigenvalue `c`, every real eigenvalue `μ` satisfies `|μ| ≤ c` (general Collatz–Wielandt bound).
* `e8_eigenvalue_max`: hence `2cos(π/30)` is the largest real eigenvalue of `adjE8` in absolute value
  (equivalently `2 − 2cos(π/30)` is the smallest eigenvalue of `cartanE8`, see `cartan_eigen`).
* `e8_eigvec_unique`: every real eigenvector of `adjE8` for `2cos(π/30)` is a scalar multiple of
  `TP1b.e8Eigenvector`.

Scope: real eigenvalues/eigenvectors (`adjE8` is symmetric, so all its eigenvalues are real; that
spectral fact is not used or restated here). Nothing in `TP1b` is changed.
-/

namespace PositiveGeometryEmergentSpaceTime.TP1bMatrix
open Real Matrix

/-- Adjacency matrix of the E8 Dynkin diagram (T(2,3,5) tree, node 7 on node 2). -/
def adjE8 : Matrix (Fin 8) (Fin 8) ℝ :=
  !![0, 1, 0, 0, 0, 0, 0, 0;
     1, 0, 1, 0, 0, 0, 0, 0;
     0, 1, 0, 1, 0, 0, 0, 1;
     0, 0, 1, 0, 1, 0, 0, 0;
     0, 0, 0, 1, 0, 1, 0, 0;
     0, 0, 0, 0, 1, 0, 1, 0;
     0, 0, 0, 0, 0, 1, 0, 0;
     0, 0, 1, 0, 0, 0, 0, 0]

/-- E8 Cartan matrix `2·1 − adjE8` (simply-laced convention). -/
def cartanE8 : Matrix (Fin 8) (Fin 8) ℝ := (2 : ℝ) • (1 : Matrix (Fin 8) (Fin 8) ℝ) - adjE8

/-- The E₈ adjacency matrix is symmetric. -/
theorem adjE8_isSymm : adjE8.IsSymm := by
  ext i j; fin_cases i <;> fin_cases j <;> rfl

/-- The E₈ adjacency matrix has nonnegative entries. -/
theorem adjE8_nonneg (i j : Fin 8) : 0 ≤ adjE8 i j := by
  fin_cases i <;> fin_cases j <;> simp [adjE8]

/-- Explicit action of `adjE8`: the eight node sums. -/
theorem adjE8_mulVec (w : Fin 8 → ℝ) :
    adjE8 *ᵥ w = ![w 1, w 0 + w 2, w 1 + w 3 + w 7, w 2 + w 4, w 3 + w 5, w 4 + w 6, w 5, w 2] := by
  ext i; fin_cases i <;>
    simp [adjE8, Matrix.mulVec, dotProduct, Fin.sum_univ_eight]

/-- `TP1b.eigen` as a matrix eigen-equation. -/
theorem eigen_matrix (c : ℝ) (h : TP1b.charPolyE8 c = 0) : adjE8 *ᵥ TP1b.e8Eigenvector c = c • TP1b.e8Eigenvector c := by
  obtain ⟨e0, e1, e2, e3, e4, e5, e6, e7⟩ := TP1b.eigen c h
  rw [adjE8_mulVec]
  ext i; fin_cases i <;> simp <;> linarith

/-- Cartan form: `cartanE8 · v = (2 − c) v`. -/
theorem cartan_eigen (c : ℝ) (h : TP1b.charPolyE8 c = 0) :
    cartanE8 *ᵥ TP1b.e8Eigenvector c = (2 - c) • TP1b.e8Eigenvector c := by
  have hv := eigen_matrix c h
  ext i
  have hi := congrFun hv i
  simp only [Pi.smul_apply, smul_eq_mul] at hi ⊢
  rw [cartanE8, sub_mulVec, Pi.sub_apply, hi, smul_mulVec, one_mulVec]
  simp only [Pi.smul_apply, smul_eq_mul]; ring

/-- Collatz–Wielandt bound: a nonnegative matrix with a strictly positive eigenvector of
eigenvalue `c` has no real eigenvalue of larger absolute value. -/
theorem pf_abs_le {n : ℕ} (A : Matrix (Fin n) (Fin n) ℝ) (hA : ∀ i j, 0 ≤ A i j)
    (v : Fin n → ℝ) (hv : ∀ i, 0 < v i) (c : ℝ) (hAv : A *ᵥ v = c • v)
    (μ : ℝ) (w : Fin n → ℝ) (hw : w ≠ 0) (hAw : A *ᵥ w = μ • w) : |μ| ≤ c := by
  obtain ⟨i0, hi0⟩ : ∃ i, w i ≠ 0 := by
    by_contra h; push Not at h; exact hw (funext h)
  obtain ⟨k, -, hk⟩ := Finset.exists_max_image Finset.univ (fun i => |w i| / v i)
    ⟨i0, Finset.mem_univ _⟩
  set t := |w k| / v k with ht
  have hbound : ∀ j, |w j| ≤ t * v j := by
    intro j; have := hk j (Finset.mem_univ _)
    rwa [div_le_iff₀ (hv j)] at this
  have hwk : 0 < |w k| := by
    have h1 : 0 < |w i0| / v i0 := div_pos (abs_pos.mpr hi0) (hv i0)
    have h2 := hk i0 (Finset.mem_univ _)
    have : 0 < t := lt_of_lt_of_le h1 h2
    have := mul_pos this (hv k)
    rwa [ht, div_mul_cancel₀ _ (hv k).ne'] at this
  have hrow : μ * w k = ∑ j, A k j * w j := by
    have := congrFun hAw k; simp [Matrix.mulVec, dotProduct] at this; linarith
  have hrowv : c * v k = ∑ j, A k j * v j := by
    have := congrFun hAv k; simp [Matrix.mulVec, dotProduct] at this; linarith
  have key : |μ| * |w k| ≤ c * |w k| := by
    calc |μ| * |w k| = |∑ j, A k j * w j| := by rw [← abs_mul, hrow]
      _ ≤ ∑ j, |A k j * w j| := Finset.abs_sum_le_sum_abs _ _
      _ = ∑ j, A k j * |w j| := by
          refine Finset.sum_congr rfl fun j _ => ?_
          rw [abs_mul, abs_of_nonneg (hA k j)]
      _ ≤ ∑ j, A k j * (t * v j) :=
          Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hbound j) (hA k j)
      _ = t * (c * v k) := by rw [hrowv, Finset.mul_sum]; congr 1; ext j; ring
      _ = c * |w k| := by rw [ht]; field_simp [(hv k).ne']
  exact le_of_mul_le_mul_right key hwk

/-- The E8 Perron–Frobenius eigenvalue `2cos(π/30)` is maximal: every real eigenvalue `μ` of
`adjE8` has `|μ| ≤ 2cos(π/30)`. -/
theorem e8_eigenvalue_max (μ : ℝ) (w : Fin 8 → ℝ) (hw : w ≠ 0) (hAw : adjE8 *ᵥ w = μ • w) :
    |μ| ≤ 2 * cos (π / 30) :=
  pf_abs_le adjE8 adjE8_nonneg _ TP1b.e8Eigenvector_pos _ (eigen_matrix _ TP1b.charPolyE8_root) μ w hw hAw

/-- Kernel step: an eigenvector of `adjE8` (eigenvalue `c ≠ 0`) vanishing at leaf 6 is zero. -/
theorem eigvec_zero_of_leaf (c : ℝ) (hc : c ≠ 0) (u : Fin 8 → ℝ) (hu : adjE8 *ᵥ u = c • u)
    (h6 : u 6 = 0) : u = 0 := by
  rw [adjE8_mulVec] at hu
  have q : ∀ i, (![u 1, u 0 + u 2, u 1 + u 3 + u 7, u 2 + u 4, u 3 + u 5, u 4 + u 6, u 5, u 2] :
      Fin 8 → ℝ) i = c * u i := fun i => by simpa using congrFun hu i
  have q0 := q 0; have q1 := q 1; have q2 := q 2; have q3 := q 3
  have q4 := q 4; have q5 := q 5; have q6 := q 6; have q7 := q 7
  simp at q0 q1 q2 q3 q4 q5 q6 q7
  have u5 : u 5 = 0 := by rw [q6, h6, mul_zero]
  have u4 : u 4 = 0 := by linear_combination q5 + c * u5 - h6 - 0 * u5 + (c - c) * h6
  have u3 : u 3 = 0 := by linear_combination q4 - u5 + c * u4
  have u2 : u 2 = 0 := by linear_combination q3 - u4 + c * u3
  have u7 : u 7 = 0 := by
    have : c * u 7 = 0 := by rw [← q7, u2]
    exact (mul_eq_zero.mp this).resolve_left hc
  have u1 : u 1 = 0 := by linear_combination q2 - u3 - u7 + c * u2
  have u0 : u 0 = 0 := by linear_combination q1 - u2 + c * u1
  ext i; fin_cases i <;> simp [u0, u1, u2, u3, u4, u5, h6, u7]

/-- Uniqueness up to scale: every real eigenvector of `adjE8` for `2cos(π/30)` is
`(w 6 / c) • TP1b.e8Eigenvector c` with `c = 2cos(π/30)` (note `TP1b.e8Eigenvector c 6 = c`). -/
theorem e8_eigvec_unique (w : Fin 8 → ℝ)
    (hAw : adjE8 *ᵥ w = (2 * cos (π / 30)) • w) :
    w = (w 6 / (2 * cos (π / 30))) • TP1b.e8Eigenvector (2 * cos (π / 30)) := by
  set c := 2 * cos (π / 30) with hcdef
  have hc : c ≠ 0 := by have := TP1b.c_bounds.1; rw [← hcdef] at this; intro h; rw [h] at this; norm_num at this
  have hv := eigen_matrix c TP1b.charPolyE8_root
  set u := w - (w 6 / c) • TP1b.e8Eigenvector c with hu
  have hAu : adjE8 *ᵥ u = c • u := by
    rw [hu, mulVec_sub, mulVec_smul, hAw, hv, smul_sub, smul_comm]
  have h6 : u 6 = 0 := by
    have hv6 : TP1b.e8Eigenvector c 6 = c := by simp [TP1b.e8Eigenvector]
    show w 6 - (w 6 / c) * TP1b.e8Eigenvector c 6 = 0
    rw [hv6]; field_simp; ring
  have := eigvec_zero_of_leaf c hc u hAu h6
  exact sub_eq_zero.mp this

end PositiveGeometryEmergentSpaceTime.TP1bMatrix
