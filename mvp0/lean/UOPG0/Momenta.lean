import UOPG0.Klein

/-!
Four massless momenta from four twistors, with momentum conservation.

A twistor is a pair `(λ, μ)` of vectors in `k²`, that is a vector in `k⁴`.
Given two twistors whose `λ` spinors are independent, there is a unique linear map
`x` with `x λ₀ = μ₀` and `x λ₁ = μ₁`. That map is the affine coordinate of the
spacetime event represented by the line through the two twistors.

Around a 4-cycle, the edge momenta `pᵢ = xᵢ - xᵢ₊₁` telescope, so they sum to
zero. Each `pᵢ` kills `λᵢ`, so `det pᵢ = 0`: every edge is null. Equivalently,
consecutive events are null-separated in the sense of `nullSeparation_iff`.
-/

namespace UOPG0

variable {α : Type*} [Field α]

/-- One twistor, split into the two `k²` factors of `k⁴`. -/
structure Twistor (α : Type*) where
  lam : Fin 2 → α
  mu : Fin 2 → α

/-- The area pairing `⟨λ, λ'⟩`. -/
def angle (u v : Fin 2 → α) : α :=
  u 0 * v 1 - u 1 * v 0

lemma angle_eq_zero_of_left_eq_zero {u v : Fin 2 → α} (hu : u = 0) : angle u v = 0 := by
  simp [angle, congrFun hu 0, congrFun hu 1]

lemma angle_eq_zero_of_right_eq_zero {u v : Fin 2 → α} (hv : v = 0) : angle u v = 0 := by
  simp [angle, congrFun hv 0, congrFun hv 1]

lemma ne_zero_of_angle_ne_zero {u v : Fin 2 → α} (h : angle u v ≠ 0) : u ≠ 0 ∧ v ≠ 0 := by
  constructor
  · intro hu
    exact h (angle_eq_zero_of_left_eq_zero hu)
  · intro hv
    exact h (angle_eq_zero_of_right_eq_zero hv)

/-- Affine coordinate of the line through `zp` and `z`. Requires `angle zp.lam z.lam ≠ 0`
for the reconstruction lemmas; the division is the field inverse of that area. -/
noncomputable def regionMatrix (zp z : Twistor α) : Matrix (Fin 2) (Fin 2) α :=
  fun a => fun
    | 0 => (z.lam 1 * zp.mu a - zp.lam 1 * z.mu a) / angle zp.lam z.lam
    | 1 => (-z.lam 0 * zp.mu a + zp.lam 0 * z.mu a) / angle zp.lam z.lam

private lemma region_col0 (zp z : Twistor α) (a : Fin 2) :
    regionMatrix zp z a 0 =
      (z.lam 1 * zp.mu a - zp.lam 1 * z.mu a) / angle zp.lam z.lam := by
  simp [regionMatrix]

private lemma region_col1 (zp z : Twistor α) (a : Fin 2) :
    regionMatrix zp z a 1 =
      (-z.lam 0 * zp.mu a + zp.lam 0 * z.mu a) / angle zp.lam z.lam := by
  simp [regionMatrix]

theorem regionMatrix_mulVec_left (zp z : Twistor α) (hδ : angle zp.lam z.lam ≠ 0) :
    (regionMatrix zp z).mulVec zp.lam = zp.mu := by
  funext a
  have hmul :
      (regionMatrix zp z).mulVec zp.lam a =
        regionMatrix zp z a 0 * zp.lam 0 + regionMatrix zp z a 1 * zp.lam 1 := by
    simp [Matrix.mulVec]
  rw [hmul, region_col0, region_col1]
  field_simp [hδ]
  simp only [angle]
  ring

theorem regionMatrix_mulVec_right (zp z : Twistor α) (hδ : angle zp.lam z.lam ≠ 0) :
    (regionMatrix zp z).mulVec z.lam = z.mu := by
  funext a
  have hmul :
      (regionMatrix zp z).mulVec z.lam a =
        regionMatrix zp z a 0 * z.lam 0 + regionMatrix zp z a 1 * z.lam 1 := by
    simp [Matrix.mulVec]
  rw [hmul, region_col0, region_col1]
  field_simp [hδ]
  simp only [angle]
  ring

/-- Spacetime event at the line through twistors `i - 1` and `i`. -/
noncomputable def xRegion (Z : Fin 4 → Twistor α) (i : Fin 4) : Matrix (Fin 2) (Fin 2) α :=
  regionMatrix (Z (i - 1)) (Z i)

/-- Edge momentum. Indices are mod 4, so the polygon closes. -/
noncomputable def edgeMomentum (Z : Fin 4 → Twistor α) (i : Fin 4) :
    Matrix (Fin 2) (Fin 2) α :=
  xRegion Z i - xRegion Z (i + 1)

theorem edgeMomentum_sum_eq_zero (Z : Fin 4 → Twistor α) :
    (∑ i : Fin 4, edgeMomentum Z i) = 0 := by
  simp only [edgeMomentum, Fin.sum_univ_four]
  have h01 : (0 : Fin 4) + 1 = 1 := by decide
  have h12 : (1 : Fin 4) + 1 = 2 := by decide
  have h23 : (2 : Fin 4) + 1 = 3 := by decide
  have h30 : (3 : Fin 4) + 1 = 0 := by decide
  simp only [h01, h12, h23, h30]
  abel

theorem edgeMomentum_mulVec_eq_zero (Z : Fin 4 → Twistor α)
    (h : ∀ i : Fin 4, angle (Z (i - 1)).lam (Z i).lam ≠ 0) (i : Fin 4) :
    (edgeMomentum Z i).mulVec (Z i).lam = 0 := by
  have hL : angle (Z (i - 1)).lam (Z i).lam ≠ 0 := h i
  have hR : angle (Z i).lam (Z (i + 1)).lam ≠ 0 := by
    simpa using h (i + 1)
  have hidx : (i + 1) - 1 = i := by
    fin_cases i <;> decide
  simp only [edgeMomentum, xRegion, Matrix.sub_mulVec, hidx]
  rw [regionMatrix_mulVec_right _ _ hL, regionMatrix_mulVec_left _ _ hR]
  abel

theorem edgeMomentum_det_eq_zero (Z : Fin 4 → Twistor α)
    (h : ∀ i : Fin 4, angle (Z (i - 1)).lam (Z i).lam ≠ 0) (i : Fin 4) :
    det2 (edgeMomentum Z i) = 0 := by
  have hv : (Z i).lam ≠ 0 := (ne_zero_of_angle_ne_zero (h i)).2
  exact det2_eq_zero_of_mulVec_eq_zero (edgeMomentum_mulVec_eq_zero Z h i) hv

/-- Each edge is a null separation of two events in `Gr(2,4)`. -/
theorem edge_nullSeparation (Z : Fin 4 → Twistor α)
    (h : ∀ i : Fin 4, angle (Z (i - 1)).lam (Z i).lam ≠ 0) (i : Fin 4) :
    pairing (graph (xRegion Z i)) (graph (xRegion Z (i + 1))) = 0 := by
  rw [pairing_graph]
  simpa [edgeMomentum] using edgeMomentum_det_eq_zero Z h i

end UOPG0
