/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# M1, spinor form: real Minkowski space as Hermitian 2×2 matrices

* (a) `hermEquiv : (Fin 4 → ℝ) ≃ₗ[ℝ] Herm`, `σ(t,x,y,z) = [[t+z, x−iy],[x+iy, t−z]]`.
* (b) `det_sigma : det σ(v) = η(v)`, with η = t² − x² − y² − z².
* (c) `det_signature_one_three`: `det` on Hermitian matrices has sigPos = 1, sigNeg = 3 and
  zero radical, using Mathlib's Sylvester's law of inertia (`QuadraticForm.Signature`).
  Elementary form: `minkowskiQuad_basis`.
Pre-registration: `prereg/M1-spinor-2026-10-10.md`.
-/

open Matrix Complex

namespace PositiveGeometryEmergentSpaceTime

/-- 2×2 complex matrices. -/
abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

/-- The real subspace of Hermitian 2×2 complex matrices. -/
def Herm : Submodule ℝ M2 where
  carrier := {X | X.IsHermitian}
  add_mem' := fun ha hb => ha.add hb
  zero_mem' := isHermitian_zero
  smul_mem' := by
    intro c X hX
    show (c • X)ᴴ = c • X
    rw [conjTranspose_smul, hX.eq, star_trivial]

/-- Pauli map `σ(t, x, y, z) = [[t + z, x − i y], [x + i y, t − z]]`. -/
noncomputable def sigma (v : Fin 4 → ℝ) : M2 :=
  !![((v 0 + v 3 : ℝ) : ℂ), (v 1 : ℂ) - (v 2 : ℂ) * I; (v 1 : ℂ) + (v 2 : ℂ) * I,
      ((v 0 - v 3 : ℝ) : ℂ)]

/-- Minkowski quadratic form `t² − x² − y² − z²`.

Also known as: eta(v), η(v)=t²−x²−y²−z²; value of minkQ.
-/
def minkowskiQuad (v : Fin 4 → ℝ) : ℝ := v 0 ^ 2 - v 1 ^ 2 - v 2 ^ 2 - v 3 ^ 2

/-- `det σ(v) = t² − x² − y² − z²` (the Minkowski quadratic form of `v`). -/
theorem det_sigma (v : Fin 4 → ℝ) : (sigma v).det = (minkowskiQuad v : ℂ) := by
  rw [det_fin_two]
  apply Complex.ext <;> simp [sigma, minkowskiQuad, sq] <;> ring

/-- `σ(v)` is Hermitian for every real 4-vector `v`. -/
theorem sigma_isHermitian (v : Fin 4 → ℝ) : (sigma v).IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> apply Complex.ext <;> simp [sigma]

/-- `sigma` as an ℝ-linear map. -/
noncomputable def sigmaL : (Fin 4 → ℝ) →ₗ[ℝ] M2 where
  toFun := sigma
  map_add' := by
    intro v w; ext i j
    fin_cases i <;> fin_cases j <;> apply Complex.ext <;> simp [sigma] <;> ring
  map_smul' := by
    intro c v; ext i j
    fin_cases i <;> fin_cases j <;> apply Complex.ext <;> simp [sigma] <;> ring

/-- coordinates back from a Hermitian matrix -/
noncomputable def coords (X : M2) : Fin 4 → ℝ :=
  ![((X 0 0).re + (X 1 1).re) / 2, (X 1 0).re, (X 1 0).im, ((X 0 0).re - (X 1 1).re) / 2]

/-- `coords` is a left inverse of `sigma`. -/
theorem coords_sigma (v : Fin 4 → ℝ) : coords (sigma v) = v := by
  ext i; fin_cases i <;> simp [coords, sigma]

/-- A Hermitian 2×2 matrix has real diagonal and `X₀₁ = conj X₁₀`. -/
lemma herm_entries {X : M2} (hX : X.IsHermitian) :
    (X 0 0).im = 0 ∧ (X 1 1).im = 0 ∧ X 0 1 = star (X 1 0) := by
  have h := hX.eq
  have h00 := congrFun (congrFun h 0) 0
  have h11 := congrFun (congrFun h 1) 1
  have h01 := congrFun (congrFun h 0) 1
  simp [conjTranspose_apply] at h00 h11 h01
  refine ⟨?_, ?_, h01.symm⟩
  · have := congrArg Complex.im h00; simp at this; linarith
  · have := congrArg Complex.im h11; simp at this; linarith

/-- `sigma` is a left inverse of `coords` on Hermitian matrices. -/
theorem sigma_coords {X : M2} (hX : X.IsHermitian) : sigma (coords X) = X := by
  obtain ⟨h00, h11, h01⟩ := herm_entries hX
  ext i j
  fin_cases i <;> fin_cases j <;> apply Complex.ext <;>
    simp [sigma, coords, h00, h11, h01] <;> ring
/-! ## (a) linear bijection ℝ⁴ ≃ Hermitian 2×2 matrices -/

/-- Linear equivalence between ℝ⁴ and Hermitian 2×2 matrices given by `sigma` and `coords`. -/
noncomputable def hermEquiv : (Fin 4 → ℝ) ≃ₗ[ℝ] Herm where
  toFun v := ⟨sigma v, sigma_isHermitian v⟩
  invFun X := coords X.1
  map_add' v w := Subtype.ext (sigmaL.map_add v w)
  map_smul' c v := Subtype.ext (sigmaL.map_smul c v)
  left_inv v := coords_sigma v
  right_inv X := Subtype.ext (sigma_coords X.2)

/-- `hermEquiv v` is `σ(v)` as an element of `Herm`. -/
@[simp] theorem hermEquiv_apply (v : Fin 4 → ℝ) : (hermEquiv v : M2) = sigma v := rfl

/-- (b) as a real number: the determinant of a Hermitian matrix is real and equals η. -/
theorem det_herm_real (X : Herm) : (X : M2).det = (minkowskiQuad (hermEquiv.symm X) : ℂ) := by
  have : (X : M2) = sigma (hermEquiv.symm X) := by
    rw [← hermEquiv_apply, LinearEquiv.apply_symm_apply]
  rw [this, det_sigma]

/-! ## (c) signature (1,3) via Mathlib's Sylvester machinery -/

/-- The Minkowski form as a weighted sum of squares with weights `(1, −1, −1, −1)`. -/
noncomputable def minkQ : QuadraticForm ℝ (Fin 4 → ℝ) :=
  QuadraticMap.weightedSumSquares ℝ (![1, -1, -1, -1] : Fin 4 → ℝ)

/-- `minkQ v = minkowskiQuad v`. -/
theorem minkQ_apply (v : Fin 4 → ℝ) : minkQ v = minkowskiQuad v := by
  simp [minkQ, QuadraticMap.weightedSumSquares_apply, Fin.sum_univ_four, minkowskiQuad]; ring

/-- `minkQ` has one positive direction. -/
theorem minkQ_sigPos : sigPos minkQ = 1 := by
  unfold minkQ; rw [QuadraticForm.sigPos_weightedSumSquares]
  have : {i : Fin 4 | (0:ℝ) < (![1, -1, -1, -1] : Fin 4 → ℝ) i} = {0} := by
    ext i; fin_cases i <;> simp
  rw [this, Set.ncard_singleton]

/-- `minkQ` has three negative directions (signature (1,3)). -/
theorem minkQ_sigNeg : sigNeg minkQ = 3 := by
  unfold minkQ; rw [QuadraticForm.sigNeg_weightedSumSquares]
  have : {i : Fin 4 | (![1, -1, -1, -1] : Fin 4 → ℝ) i < 0} = {1, 2, 3} := by
    ext i; fin_cases i <;> simp
  rw [this, show ({1, 2, 3} : Set (Fin 4)) = ((({1, 2, 3} : Finset (Fin 4))) : Set (Fin 4)) by simp,
    Set.ncard_coe_finset]; rfl

/-- The determinant, as a real quadratic form on the Hermitian matrices. -/
noncomputable def detQ : QuadraticForm ℝ Herm := minkQ.comp hermEquiv.symm.toLinearMap

/-- `detQ X` is the real part of `det X`. -/
theorem detQ_apply (X : Herm) : detQ X = ((X : M2).det).re := by
  rw [det_herm_real]; simp [detQ, minkQ_apply]

/-- The determinant on Hermitian 2×2 matrices is equivalent, as a real quadratic form, to the
  Minkowski form `minkQ`. -/
theorem detQ_equivalent : detQ.Equivalent minkQ :=
  ⟨{ hermEquiv.symm with map_app' := fun _ => rfl }⟩

/-- **M1 main theorem (c).** On real-4-dimensional Hermitian 2×2 matrices, `det` is a
quadratic form with maximal positive-definite subspace of dimension 1, maximal
negative-definite subspace of dimension 3, and zero radical: signature (1,3), nondegenerate.
Stated for *any* quadratic form agreeing pointwise with `re ∘ det`. -/
theorem det_signature_one_three (Q : QuadraticForm ℝ Herm)
    (hQ : ∀ X, Q X = ((X : M2).det).re) :
    sigPos Q = 1 ∧ sigNeg Q = 3 ∧ Module.finrank ℝ Q.radical = 0 := by
  have hQ' : Q = detQ := by ext X; rw [hQ, detQ_apply]
  subst hQ'
  have h1 : sigPos detQ = 1 := by rw [detQ_equivalent.sigPos_eq, minkQ_sigPos]
  have h3 : sigNeg detQ = 3 := by rw [detQ_equivalent.sigNeg_eq, minkQ_sigNeg]
  have : FiniteDimensional ℝ Herm := Module.Finite.equiv hermEquiv
  have hsum := QuadraticForm.sigPos_add_sigNeg_add_radical (Q := detQ)
  have h4 : Module.finrank ℝ Herm = 4 := by
    rw [← hermEquiv.finrank_eq]; simp
  refine ⟨h1, h3, ?_⟩
  omega

/-- (c) elementary form: the standard basis is η-orthogonal with values (+1,−1,−1,−1). -/
theorem minkowskiQuad_basis :
    minkQ (Pi.single 0 1) = 1 ∧ minkQ (Pi.single 1 1) = -1 ∧
    minkQ (Pi.single 2 1) = -1 ∧ minkQ (Pi.single 3 1) = -1 ∧
    ∀ i j : Fin 4, i ≠ j → QuadraticMap.polar minkQ (Pi.single i 1) (Pi.single j 1) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simp [minkQ_apply, minkowskiQuad]
  · simp [minkQ_apply, minkowskiQuad]
  · simp [minkQ_apply, minkowskiQuad]
  · simp [minkQ_apply, minkowskiQuad]
  · intro i j hij
    fin_cases i <;> fin_cases j <;>
      simp_all [QuadraticMap.polar, minkQ_apply, minkowskiQuad]

end PositiveGeometryEmergentSpaceTime
