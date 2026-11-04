/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
FL-1Z (prereg/FL-1Z-modular-fixed-point-2026-10-22.md, amendments A1, A2): structural facts behind
"does a modular fixed point give a fit-free neutrino prediction?" for the Zee–Babu modular-A4 model of
arXiv:2502.12662.

* `valence_lt12`: the SL(2,ℤ) valence formula is a DECLARED HYPOTHESIS `hv`
  (12·n + 6·a + 4·b = k, where n counts cusp and interior zeros, a is the order at i and b the order at ω;
  CITED Serre, *A Course in Arithmetic*, VII.3). It is not a Mathlib theorem and not a FRONTIER-AXIOM.
  Under it, weight k < 12 forces n = 0: every zero of such a form sits at a fixed point.
  Scope: level 1 only. The level-3 model of 2502.12662 has a different count, which is not formalised here.
* `antisymm3_det_zero`, `antisymm3_kernel`: the Zee–Babu coupling f is antisymmetric in 3 flavours, so
  det f = 0 and f·(a,b,c) = 0. Hence m_ν = f·B·fᵀ has m1 = 0 for every τ. This is not a fixed-point fact.
* `D3_rank_one`, `D3_det_zero`: the eq. (D.3) neutrino matrix at τ = ω is w wᵀ (rank 1). This is the
  published exclusion of the exact fixed point.
* `hierarchy_ratio_surj`: every positive ratio is D2²/D3², so ρ = Δm²sol/Δm²atm carries no integer by itself.
-/

namespace PositiveGeometryEmergentSpaceTime.FL1Z

open Matrix

/-- Valence formula of level 1 (declared hypothesis `hv`): weight below 12 means no zeros away from
  i, ω. -/
theorem valence_lt12 (k n a b : ℕ) (hv : 12 * n + 6 * a + 4 * b = k) (hk : k < 12) : n = 0 := by
  omega

/-- No nonzero weight-2 level-1 form: the valence equation has no solution at k = 2. -/
theorem valence_k2_empty : ¬ ∃ n a b : ℕ, 12 * n + 6 * a + 4 * b = 2 := by
  rintro ⟨n, a, b, h⟩; omega

/-- Weight 4: the only zero is a simple zero at ω (E4). -/
theorem valence_k4 (n a b : ℕ) (hv : 12 * n + 6 * a + 4 * b = 4) : n = 0 ∧ a = 0 ∧ b = 1 := by
  omega

/-- Weight 6: the only zero is a simple zero at i (E6). -/
theorem valence_k6 (n a b : ℕ) (hv : 12 * n + 6 * a + 4 * b = 6) : n = 0 ∧ a = 1 ∧ b = 0 := by
  omega

/-- Weight 12 admits n = 1 (Δ, zero at the cusp): the bound 12 is sharp. -/
theorem valence_k12_free : ∃ n a b : ℕ, 12 * n + 6 * a + 4 * b = 12 ∧ n = 1 :=
  ⟨1, 0, 0, by norm_num, rfl⟩

/-- Antisymmetric 3×3 (Zee–Babu f) has zero determinant. -/
theorem antisymm3_det_zero {R : Type*} [CommRing R] (a b c : R) :
    (!![0, c, -b; -c, 0, a; b, -a, 0] : Matrix (Fin 3) (Fin 3) R).det = 0 := by
  rw [Matrix.det_fin_three]; simp; ring

/-- The vector (a, b, c) is in the kernel of f, so it is the massless direction for every τ. -/
theorem antisymm3_kernel {R : Type*} [CommRing R] (a b c : R) :
    (!![0, c, -b; -c, 0, a; b, -a, 0] : Matrix (Fin 3) (Fin 3) R) *ᵥ ![a, b, c] = 0 := by
  ext i; fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three] <;> ring

/-- Eq. (D.3) of 2502.12662 at τ = ω. -/
def D3 {R : Type*} [CommRing R] (ω : R) : Matrix (Fin 3) (Fin 3) R :=
  !![4, -2 * ω ^ 2, 4 * ω; -2 * ω ^ 2, ω, -2; 4 * ω, -2, 4 * ω ^ 2]

/-- The rank-one generator w = (2, -ω², 2ω). -/
def w {R : Type*} [CommRing R] (ω : R) : Fin 3 → R := ![2, -ω ^ 2, 2 * ω]

/-- (D.3) is the outer product w wᵀ whenever ω³ = 1, so it has rank one. -/
theorem D3_rank_one {R : Type*} [CommRing R] (ω : R) (hω : ω ^ 3 = 1) :
    D3 ω = vecMulVec (w ω) (w ω) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [D3, w, vecMulVec_apply]
  all_goals first
    | ring1
    | linear_combination (-2 : R) * hω
    | linear_combination ω * hω
    | linear_combination (-ω) * hω

/-- Corollary: det (D.3) = 0. -/
theorem D3_det_zero {R : Type*} [CommRing R] (ω : R) (hω : ω ^ 3 = 1) : (D3 ω).det = 0 := by
  rw [D3_rank_one ω hω, Matrix.det_fin_three]
  simp [vecMulVec_apply]; ring

/-- Every positive ratio is a squared mass ratio: ρ = (m2/m3)² carries no structural integer. -/
theorem hierarchy_ratio_surj (r : ℝ) (hr : 0 < r) :
    ∃ D2 D3 : ℝ, 0 < D2 ∧ 0 < D3 ∧ D2 ^ 2 / D3 ^ 2 = r :=
  ⟨Real.sqrt r, 1, Real.sqrt_pos.mpr hr, one_pos, by rw [Real.sq_sqrt hr.le]; simp⟩

end PositiveGeometryEmergentSpaceTime.FL1Z
