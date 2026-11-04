/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.Spinor
import Physlib.Relativity.SL2C.Basic

/-!
# (d) SL(2,ℂ) acts on Hermitian matrices by Lorentz transformations

* Own (Mathlib-only) statements: `X ↦ A X Aᴴ` preserves Hermiticity (Mathlib's
  `Matrix.isHermitian_mul_mul_conjTranspose`) and `det`, so via `hermEquiv` it is an
  η-preserving linear map `lorentzOf A` of ℝ⁴; `lorentzOf` is multiplicative; its kernel is `{±1}`.
* Reused from PhysLean/Physlib (Apache-2.0, see `CREDITS.md`): the group homomorphism
  `Lorentz.SL2C.toLorentzGroup : SL(2,ℂ) →* LorentzGroup 3`, with image in the
  *restricted* (proper, orthochronous) Lorentz group.
* Bridge lemma: our `sigma` is the standard Pauli expansion `t σ₀ + x σ₁ + y σ₂ + z σ₃`,
  with Physlib's `PauliMatrix.pauliMatrix`.
-/

open Matrix Complex
open scoped MatrixGroups

namespace PositiveGeometryEmergentSpaceTime

/-- Bridge to Physlib's Pauli matrices. -/
theorem sigma_eq_pauli (v : Fin 4 → ℝ) :
    sigma v = (v 0 : ℂ) • PauliMatrix.pauliMatrix (Sum.inl 0)
      + (v 1 : ℂ) • PauliMatrix.pauliMatrix (Sum.inr 0)
      + (v 2 : ℂ) • PauliMatrix.pauliMatrix (Sum.inr 1)
      + (v 3 : ℂ) • PauliMatrix.pauliMatrix (Sum.inr 2) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [sigma, PauliMatrix.pauliMatrix] <;> ring

/-- Conjugating a 2×2 matrix by `A ∈ SL(2,ℂ)` (`X ↦ A X A†`) preserves its determinant. -/
lemma det_conj_SL (A : SL(2, ℂ)) (X : M2) : (A.1 * X * A.1ᴴ).det = X.det := by
  rw [det_mul, det_mul, det_conjTranspose, A.2]; simp

/-- `X ↦ A X Aᴴ` on our Hermitian submodule. -/
noncomputable def conjAct (A : SL(2, ℂ)) : Herm →ₗ[ℝ] Herm where
  toFun X := ⟨A.1 * X.1 * A.1ᴴ, isHermitian_mul_mul_conjTranspose A.1 X.2⟩
  map_add' X Y := by ext1; simp [Matrix.mul_add, Matrix.add_mul]
  map_smul' c X := by ext1; simp

/-- The induced real-linear map on ℝ⁴. -/
noncomputable def lorentzOf (A : SL(2, ℂ)) : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ) :=
  hermEquiv.symm.toLinearMap ∘ₗ conjAct A ∘ₗ hermEquiv.toLinearMap

/-- `σ(Λ_A v) = A σ(v) A†`: `lorentzOf A` is the vector action induced by `A ∈ SL(2,ℂ)`. -/
lemma sigma_lorentzOf (A : SL(2, ℂ)) (v : Fin 4 → ℝ) :
    sigma (lorentzOf A v) = A.1 * sigma v * A.1ᴴ := by
  rw [← hermEquiv_apply]
  simp [lorentzOf, conjAct]

/-- **(d)** `lorentzOf A` preserves the Minkowski form: it is a Lorentz transformation. -/
theorem minkowskiQuad_lorentzOf (A : SL(2,
    ℂ)) (v : Fin 4 → ℝ) : minkowskiQuad (lorentzOf A v) = minkowskiQuad v := by
  apply Complex.ofReal_injective
  rw [← det_sigma, ← det_sigma, sigma_lorentzOf, det_conj_SL]

/-- `lorentzOf` is multiplicative (a representation). -/
theorem lorentzOf_mul (A B : SL(2, ℂ)) (v : Fin 4 → ℝ) :
    lorentzOf (A * B) v = lorentzOf A (lorentzOf B v) := by
  apply hermEquiv.injective
  ext1
  simp only [hermEquiv_apply, sigma_lorentzOf]
  simp [Matrix.mul_assoc, conjTranspose_mul]

/-- `lorentzOf A` acts trivially iff `A = ±1`: kernel of SL(2,ℂ) → Lorentz is `{±1}`. -/
theorem lorentzOf_eq_id_iff (A : SL(2, ℂ)) :
    (∀ v, lorentzOf A v = v) ↔ A = 1 ∨ A = -1 := by
  constructor
  · intro h
    have hX : ∀ v, A.1 * sigma v * A.1ᴴ = sigma v := fun v => by
      rw [← sigma_lorentzOf, h]
    -- test matrices: E₀₀ = σ(½,0,0,½), E₁₁ = σ(½,0,0,-½), σ₁ = σ(0,1,0,0)
    have e00 := hX ![1/2, 0, 0, 1/2]
    have e11 := hX ![1/2, 0, 0, -1/2]
    have ex := hX ![0, 1, 0, 0]
    have g := fun (M N : M2) (hMN : M = N) (i j : Fin 2) => congrFun (congrFun hMN i) j
    have a1 := g _ _ e00 0 0
    have c0 := g _ _ e00 1 1
    have b0 := g _ _ e11 0 0
    have d1 := g _ _ e11 1 1
    have x01 := g _ _ ex 0 1
    simp [sigma, mul_apply, Fin.sum_univ_two, conjTranspose_apply] at a1 c0 b0 d1 x01
    norm_num at a1 c0 b0 d1 x01
    have hdet := A.2
    rw [det_fin_two] at hdet
    simp [b0, c0] at hdet x01
    have ha0 : A.1 0 0 ≠ 0 := by intro h0; simp [h0] at hdet
    have hconj : (starRingEnd ℂ) (A.1 1 1) = A.1 1 1 :=
      mul_left_cancel₀ ha0 (x01.trans hdet.symm)
    have hdd : A.1 1 1 * A.1 1 1 = 1 := by
      calc A.1 1 1 * A.1 1 1 = A.1 1 1 * (starRingEnd ℂ) (A.1 1 1) := by rw [hconj]
        _ = 1 := d1
    have haa : A.1 0 0 = A.1 1 1 := by
      calc A.1 0 0 = A.1 0 0 * (A.1 1 1 * A.1 1 1) := by rw [hdd, mul_one]
        _ = (A.1 0 0 * A.1 1 1) * A.1 1 1 := by ring
        _ = A.1 1 1 := by rw [hdet, one_mul]
    rcases mul_self_eq_one_iff.mp hdd with hd | hd
    · left; ext i j
      fin_cases i <;> fin_cases j <;> simp [haa, hd, b0, c0]
    · right; ext i j
      fin_cases i <;> fin_cases j <;> simp [haa, hd, b0, c0]
  · rintro (rfl | rfl) v
    · apply hermEquiv.injective; ext1; simp [hermEquiv_apply, sigma_lorentzOf]
    · apply hermEquiv.injective; ext1; simp [hermEquiv_apply, sigma_lorentzOf]

/-- **(d), reused from Physlib:** SL(2,ℂ) maps homomorphically into the Lorentz group
`LorentzGroup 3`, landing in the proper orthochronous (restricted) component. -/
theorem sl2c_to_restricted_lorentz (A : SL(2, ℂ)) :
    (Lorentz.SL2C.toLorentzGroup A).1 ∈ LorentzGroup 3 ∧
    (Lorentz.SL2C.toLorentzGroup A).1.det = 1 ∧
    LorentzGroup.IsOrthochronous (Lorentz.SL2C.toLorentzGroup A) :=
  ⟨(Lorentz.SL2C.toLorentzGroup A).2, Lorentz.SL2C.toLorentzGroup_det_one A,
    Lorentz.SL2C.toLorentzGroup_isOrthochronous A⟩

end PositiveGeometryEmergentSpaceTime
