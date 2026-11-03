/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# (e) Null separation for Hermitian 2×2 matrices

A Hermitian 2×2 matrix `D` has `det D = 0` iff `D = ± v vᴴ` for some `v ∈ ℂ²`.
This is the Hermitian (real Minkowski) refinement of the rank-one lemma
`det2_eq_zero_iff_exists_outer` in savanc/UOPG-Emergent-Spacetime (which says, over any field,
`det = 0 ↔ D = u vᵀ` with independent `u, v`): Hermiticity forces `u = ± conj v`.
-/

open Matrix Complex

namespace PositiveGeometryEmergentSpaceTime

/-- rank-one Hermitian matrix `v vᴴ` -/
def outerH (v : Fin 2 → ℂ) : Matrix (Fin 2) (Fin 2) ℂ := vecMulVec v (star v)

/-- The outer product `v v†` is Hermitian. -/
lemma outerH_isHermitian (v : Fin 2 → ℂ) : (outerH v).IsHermitian := by
  ext i j; simp [outerH, vecMulVec_apply, mul_comm]

/-- The outer product `v v†` has determinant 0 (rank ≤ 1, so it is a null vector under `sigma`). -/
lemma det_outerH (v : Fin 2 → ℂ) : (outerH v).det = 0 := by
  rw [det_fin_two]; simp [outerH, vecMulVec_apply]; ring

private lemma outer_of_pos_left (a d : ℝ) (b : ℂ) (ha : 0 < a) (h : a * d = normSq b) :
    !![(a : ℂ), star b; b, (d : ℂ)] = outerH ![(Real.sqrt a : ℂ), b / (Real.sqrt a : ℂ)] := by
  have hs : Real.sqrt a * Real.sqrt a = a := Real.mul_self_sqrt ha.le
  have hs0 : (Real.sqrt a : ℂ) ≠ 0 := by
    exact_mod_cast (Real.sqrt_pos.mpr ha).ne'
  have hd : (d : ℂ) = b * star b / ((Real.sqrt a : ℂ) * (Real.sqrt a : ℂ)) := by
    rw [← ofReal_mul, hs, Complex.star_def, Complex.mul_conj, ← h]
    have : (a : ℂ) ≠ 0 := by exact_mod_cast ha.ne'
    push_cast; field_simp
  ext i j
  fin_cases i <;> fin_cases j <;> simp [outerH, vecMulVec_apply]
  · exact_mod_cast hs.symm
  · field_simp
  · field_simp
  · rw [hd]; field_simp; simp

private lemma outer_of_pos_right (a d : ℝ) (b : ℂ) (hd : 0 < d) (h : a * d = normSq b) :
    !![(a : ℂ), star b; b, (d : ℂ)] =
      outerH ![star b / (Real.sqrt d : ℂ), (Real.sqrt d : ℂ)] := by
  have hs : Real.sqrt d * Real.sqrt d = d := Real.mul_self_sqrt hd.le
  have hs0 : (Real.sqrt d : ℂ) ≠ 0 := by
    exact_mod_cast (Real.sqrt_pos.mpr hd).ne'
  have ha : (a : ℂ) = star b * b / ((Real.sqrt d : ℂ) * (Real.sqrt d : ℂ)) := by
    rw [← ofReal_mul, hs, mul_comm (star b), Complex.star_def, Complex.mul_conj, ← h]
    have : (d : ℂ) ≠ 0 := by exact_mod_cast hd.ne'
    push_cast; field_simp
  ext i j
  fin_cases i <;> fin_cases j <;> simp [outerH, vecMulVec_apply]
  · rw [ha]; field_simp; simp [mul_comm]
  · field_simp
  · field_simp
  · exact_mod_cast hs.symm

/-- Every Hermitian 2×2 matrix has the form `!![a, b̄; b, d]` with `a d` real. -/
lemma herm_form {D : Matrix (Fin 2) (Fin 2) ℂ} (hD : D.IsHermitian) :
    D = !![((D 0 0).re : ℂ), star (D 1 0); D 1 0, ((D 1 1).re : ℂ)] := by
  have h := hD.eq
  have h00 := congrFun (congrFun h 0) 0
  have h11 := congrFun (congrFun h 1) 1
  have h01 := congrFun (congrFun h 0) 1
  simp [conjTranspose_apply] at h00 h11 h01
  have i00 : (D 0 0).im = 0 := by have := congrArg Complex.im h00; simp at this; linarith
  have i11 : (D 1 1).im = 0 := by have := congrArg Complex.im h11; simp at this; linarith
  ext i j
  fin_cases i <;> fin_cases j <;> simp
  · apply Complex.ext <;> simp [i00]
  · exact h01.symm
  · apply Complex.ext <;> simp [i11]

private lemma explicit_null (a d : ℝ) (b : ℂ)
    (hdet : (!![(a : ℂ), star b; b, (d : ℂ)]).det = 0) :
    ∃ v : Fin 2 → ℂ, !![(a : ℂ), star b; b, (d : ℂ)] = outerH v ∨
      !![(a : ℂ), star b; b, (d : ℂ)] = -outerH v := by
  have had : a * d = normSq b := by
    rw [det_fin_two] at hdet
    simp at hdet
    have := congrArg Complex.re hdet
    simp at this
    rw [Complex.normSq_apply]; linarith
  rcases lt_trichotomy a 0 with ha | ha | ha
  · refine ⟨![(Real.sqrt (-a) : ℂ), (-b) / (Real.sqrt (-a) : ℂ)], Or.inr ?_⟩
    have key := outer_of_pos_left (-a) (-d) (-b) (by linarith) (by rw [normSq_neg]; linarith)
    rw [← key]
    ext i j; fin_cases i <;> fin_cases j <;> simp
  · rcases lt_trichotomy d 0 with hd | hd | hd
    · refine ⟨![star (-b) / (Real.sqrt (-d) : ℂ), (Real.sqrt (-d) : ℂ)], Or.inr ?_⟩
      have key := outer_of_pos_right (-a) (-d) (-b) (by linarith)
        (by rw [normSq_neg]; linarith)
      rw [← key]
      ext i j; fin_cases i <;> fin_cases j <;> simp [ha]
    · have hb : b = 0 := by
        have : normSq b = 0 := by rw [← had, ha, zero_mul]
        exact normSq_eq_zero.mp this
      refine ⟨0, Or.inl ?_⟩
      ext i j; fin_cases i <;> fin_cases j <;> simp [outerH, ha, hd, hb]
    · exact ⟨_, Or.inl (outer_of_pos_right a d b hd had)⟩
  · exact ⟨_, Or.inl (outer_of_pos_left a d b ha had)⟩

/-- **(e)** For Hermitian `D`: `det D = 0 ↔ D = v vᴴ ∨ D = -(v vᴴ)` for some `v ∈ ℂ²`. -/
theorem herm_det_eq_zero_iff {D : Matrix (Fin 2) (Fin 2) ℂ} (hD : D.IsHermitian) :
    D.det = 0 ↔ ∃ v : Fin 2 → ℂ, D = outerH v ∨ D = -outerH v := by
  constructor
  · intro hdet
    rw [herm_form hD] at hdet ⊢
    exact explicit_null _ _ _ hdet
  · rintro ⟨v, rfl | rfl⟩
    · exact det_outerH v
    · rw [det_neg, det_outerH]; simp

end PositiveGeometryEmergentSpaceTime
