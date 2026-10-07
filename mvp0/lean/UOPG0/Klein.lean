import UOPG0.Plucker

/-!
Klein correspondence in the affine chart where the first Plücker coordinate is `1`.

A `2 × 2` matrix `x` is a linear map `k² → k²`. Its graph is the 2-plane of vectors
`(v, x v)` inside `k² ⊕ k² ≅ k⁴`, written as a `2 × 4` matrix in the usual
`Gr(2,4)` gauge. Two such events are null-separated exactly when `det(x - y) = 0`,
and that determinant is the Plücker bilinear of the two graphs.
-/

namespace UOPG0

section Ring

variable {α : Type*} [CommRing α]

/-- Graph of `x`, as a `2 × 4` matrix whose rows span `{(v, x v)}`. -/
def graph (x : Matrix (Fin 2) (Fin 2) α) : Matrix (Fin 2) (Fin 4) α
  | 0, 0 => 1
  | 0, 1 => 0
  | 0, 2 => x 0 0
  | 0, 3 => x 1 0
  | 1, 0 => 0
  | 1, 1 => 1
  | 1, 2 => x 0 1
  | 1, 3 => x 1 1

@[simp] lemma plucker_graph_01 (x : Matrix (Fin 2) (Fin 2) α) :
    plucker (graph x) 0 1 = 1 := by
  simp [plucker, graph]

@[simp] lemma plucker_graph_02 (x : Matrix (Fin 2) (Fin 2) α) :
    plucker (graph x) 0 2 = x 0 1 := by
  simp [plucker, graph]

@[simp] lemma plucker_graph_03 (x : Matrix (Fin 2) (Fin 2) α) :
    plucker (graph x) 0 3 = x 1 1 := by
  simp [plucker, graph]

@[simp] lemma plucker_graph_12 (x : Matrix (Fin 2) (Fin 2) α) :
    plucker (graph x) 1 2 = -x 0 0 := by
  simp [plucker, graph]

@[simp] lemma plucker_graph_13 (x : Matrix (Fin 2) (Fin 2) α) :
    plucker (graph x) 1 3 = -x 1 0 := by
  simp [plucker, graph]

@[simp] lemma plucker_graph_23 (x : Matrix (Fin 2) (Fin 2) α) :
    plucker (graph x) 2 3 = det2 x := by
  simp [plucker, graph, det2]

/-- The Plücker bilinear of two graphs is the Minkowski quadratic form `det(x - y)`. -/
theorem pairing_graph (x y : Matrix (Fin 2) (Fin 2) α) :
    pairing (graph x) (graph y) = det2 (x - y) := by
  simp only [pairing, plucker_graph_01, plucker_graph_02, plucker_graph_03, plucker_graph_12,
    plucker_graph_13, plucker_graph_23, det2, Matrix.sub_apply]
  ring

theorem graph_on_quadric (x : Matrix (Fin 2) (Fin 2) α) : pluckerQuad (graph x) = 0 :=
  plucker_relation (graph x)

end Ring

section Field

variable {α : Type*} [Field α]

/-- A singular `2 × 2` matrix has a nonzero kernel vector. -/
theorem exists_ne_zero_mulVec_of_det2_eq_zero {m : Matrix (Fin 2) (Fin 2) α}
    (hm : det2 m = 0) : ∃ v : Fin 2 → α, v ≠ 0 ∧ m.mulVec v = 0 := by
  have mul (v : Fin 2 → α) (i : Fin 2) :
      m.mulVec v i = m i 0 * v 0 + m i 1 * v 1 := by
    simp [Matrix.mulVec]
  by_cases hrow : m 1 0 = 0 ∧ m 1 1 = 0
  · by_cases hrow0 : m 0 0 = 0 ∧ m 0 1 = 0
    · refine ⟨fun | 0 => 1 | 1 => 0, ?_, ?_⟩
      · intro h
        have := congrFun h 0
        simp at this
      · funext i
        fin_cases i <;> simp [mul, hrow0.1, hrow0.2, hrow.1, hrow.2]
    · refine ⟨fun | 0 => m 0 1 | 1 => -m 0 0, ?_, ?_⟩
      · intro h
        have h0 := congrFun h 0
        have h1 := congrFun h 1
        simp at h0 h1
        exact hrow0 ⟨h1, h0⟩
      · funext i
        fin_cases i
        · simp [mul, mul_neg]; ring
        · simp [mul, hrow.1, hrow.2]
  · refine ⟨fun | 0 => m 1 1 | 1 => -m 1 0, ?_, ?_⟩
    · intro h
      have h0 := congrFun h 0
      have h1 := congrFun h 1
      simp at h0 h1
      exact hrow ⟨h1, h0⟩
    · funext i
      fin_cases i
      · simp only [mul, mul_neg]
        rw [← sub_eq_add_neg]
        simpa [det2] using hm
      · simp [mul, mul_neg]; ring

/-- A nontrivial kernel forces the determinant to vanish. -/
theorem det2_eq_zero_of_mulVec_eq_zero {m : Matrix (Fin 2) (Fin 2) α} {v : Fin 2 → α}
    (hv : m.mulVec v = 0) (vne : v ≠ 0) : det2 m = 0 := by
  have eq0 : m 0 0 * v 0 + m 0 1 * v 1 = 0 := by
    have := congrFun hv 0
    simpa [Matrix.mulVec, Fin.sum_univ_two] using this
  have eq1 : m 1 0 * v 0 + m 1 1 * v 1 = 0 := by
    have := congrFun hv 1
    simpa [Matrix.mulVec, Fin.sum_univ_two] using this
  have hv0 : det2 m * v 0 = 0 := by
    calc
      det2 m * v 0
          = (m 0 0 * m 1 1 - m 0 1 * m 1 0) * v 0 := by simp [det2]
      _ = m 1 1 * (m 0 0 * v 0 + m 0 1 * v 1) - m 0 1 * (m 1 0 * v 0 + m 1 1 * v 1) := by
            ring_nf
      _ = 0 := by rw [eq0, eq1]; ring_nf
  have hv1 : det2 m * v 1 = 0 := by
    calc
      det2 m * v 1
          = (m 0 0 * m 1 1 - m 0 1 * m 1 0) * v 1 := by simp [det2]
      _ = m 0 0 * (m 1 0 * v 0 + m 1 1 * v 1) - m 1 0 * (m 0 0 * v 0 + m 0 1 * v 1) := by
            ring_nf
      _ = 0 := by rw [eq0, eq1]; ring_nf
  by_cases h0 : v 0 = 0
  · have h1 : v 1 ≠ 0 := by
      intro h1
      apply vne
      funext i
      fin_cases i <;> simp [h0, h1]
    exact (mul_eq_zero.mp hv1).resolve_right h1
  · exact (mul_eq_zero.mp hv0).resolve_right h0

/-- A `2 × 2` matrix is singular if and only if it has a nonzero kernel vector. -/
theorem singular_iff_exists_kernel (m : Matrix (Fin 2) (Fin 2) α) :
    det2 m = 0 ↔ ∃ v : Fin 2 → α, v ≠ 0 ∧ m.mulVec v = 0 := by
  constructor
  · exact exists_ne_zero_mulVec_of_det2_eq_zero
  · rintro ⟨_v, hv, hmul⟩
    exact det2_eq_zero_of_mulVec_eq_zero hmul hv

/-- Null separation in the affine chart. The Plücker bilinear vanishes if and only
if `x − y` is singular. Combined with `singular_iff_exists_kernel`, that is
equivalent to the two events sharing a nonzero direction. -/
theorem nullSeparation_iff (x y : Matrix (Fin 2) (Fin 2) α) :
    pairing (graph x) (graph y) = 0 ↔ det2 (x - y) = 0 := by
  rw [pairing_graph]

end Field

end UOPG0
