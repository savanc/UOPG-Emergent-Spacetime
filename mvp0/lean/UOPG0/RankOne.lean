import UOPG0.Momenta

/-!
A null `2 × 2` matrix is an outer product, and the opposite rescaling fixes it.

`det m = 0` if and only if `m = u vᵀ` for some column `u` and row `v`.
Replacing `u` by `t u` and `v` by `v / t`, for `t ≠ 0`, does not change `m`.

That is the rescaling drawn on the MVP-4 card. It is ordinary linear algebra.
It is not a helicity, and it does not turn that card into a theorem. The
helicity would be a weight the geometry forces on a wavefunction. There is
no wavefunction here.
-/

namespace UOPG0

/-- A column in `k²`. The branch is on the value, so `⟨1, h⟩` reduces. -/
def vec2 {α : Type*} (a b : α) : Fin 2 → α :=
  fun i => if i.1 = 0 then a else b

@[simp] lemma vec2_zero {α : Type*} (a b : α) : vec2 a b 0 = a := by
  simp [vec2]

@[simp] lemma vec2_one {α : Type*} (a b : α) : vec2 a b 1 = b := by
  simp [vec2]

@[simp] lemma vec2_mk_zero {α : Type*} (a b : α) (h : 0 < 2) :
    vec2 a b ⟨0, h⟩ = a := by
  simp [vec2]

@[simp] lemma vec2_mk_one {α : Type*} (a b : α) (h : 1 < 2) :
    vec2 a b ⟨1, h⟩ = b := by
  simp [vec2]

section Field

variable {α : Type*} [Field α]

/-- Outer product `u vᵀ`. The entry in row `i` and column `j` is `uᵢ vⱼ`. -/
def outer (u v : Fin 2 → α) : Matrix (Fin 2) (Fin 2) α :=
  fun i j => u i * v j

theorem det2_outer (u v : Fin 2 → α) : det2 (outer u v) = 0 := by
  simp only [det2, outer]
  ring

/-- Opposite rescaling of the two factors. Not a helicity weight. -/
theorem outer_rescale (t : α) (ht : t ≠ 0) (u v : Fin 2 → α) :
    outer (fun i => t * u i) (fun j => v j / t) = outer u v := by
  ext i j
  simp only [outer]
  field_simp [ht]

theorem exists_outer_of_det2_eq_zero {m : Matrix (Fin 2) (Fin 2) α} (hm : det2 m = 0) :
    ∃ u v : Fin 2 → α, m = outer u v := by
  by_cases hcol0 : m 0 0 = 0 ∧ m 1 0 = 0
  · by_cases hcol1 : m 0 1 = 0 ∧ m 1 1 = 0
    · refine ⟨vec2 0 0, vec2 0 0, ?_⟩
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [outer, vec2, hcol0.1, hcol0.2, hcol1.1, hcol1.2]
    · refine ⟨vec2 (m 0 1) (m 1 1), vec2 0 1, ?_⟩
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [outer, vec2, hcol0.1, hcol0.2]
  · by_cases h00 : m 0 0 = 0
    · have h10 : m 1 0 ≠ 0 := by
        intro h
        exact hcol0 ⟨h00, h⟩
      have h01 : m 0 1 = 0 := by
        have hdet : m 0 0 * m 1 1 - m 0 1 * m 1 0 = 0 := by simpa [det2] using hm
        rw [h00, zero_mul, zero_sub] at hdet
        exact (mul_eq_zero.mp (neg_eq_zero.mp hdet)).resolve_right h10
      refine ⟨vec2 (m 0 0) (m 1 0), vec2 1 (m 1 1 / m 1 0), ?_⟩
      ext i j
      fin_cases i <;> fin_cases j
      · simp [outer, vec2, h00]
      · simp [outer, vec2, h00, h01]
      · simp [outer, vec2]
      · simp [outer, vec2]
        field_simp [h10]
    · have hdet : m 0 0 * m 1 1 = m 0 1 * m 1 0 :=
        sub_eq_zero.mp (by simpa [det2] using hm)
      refine ⟨vec2 (m 0 0) (m 1 0), vec2 1 (m 0 1 / m 0 0), ?_⟩
      ext i j
      fin_cases i <;> fin_cases j
      · simp [outer, vec2]
      · simp [outer, vec2]; field_simp [h00]
      · simp [outer, vec2]
      · simp [outer, vec2]
        field_simp [h00]
        rw [mul_comm (m 1 0) (m 0 1), ← hdet]
        ring

/-- A `2 × 2` matrix is singular if and only if it is an outer product. -/
theorem det2_eq_zero_iff_exists_outer (m : Matrix (Fin 2) (Fin 2) α) :
    det2 m = 0 ↔ ∃ u v : Fin 2 → α, m = outer u v := by
  constructor
  · exact exists_outer_of_det2_eq_zero
  · rintro ⟨u, v, rfl⟩
    exact det2_outer u v

/-- For `t ≠ 1`, rescaling moves a nonzero factor. The parameter is visible on `u`. -/
theorem rescale_moves_factor {t : α} (ht1 : t ≠ 1) {u : Fin 2 → α} (hu : u ≠ 0) :
    (fun i => t * u i) ≠ u := by
  intro heq
  apply hu
  funext i
  have hi : t * u i = u i := congrFun heq i
  have hmul : (t - 1) * u i = 0 := by
    calc
      (t - 1) * u i = t * u i - u i := by ring
      _ = 0 := sub_eq_zero.mpr hi
  have ht1' : t - 1 ≠ 0 := sub_ne_zero.mpr ht1
  exact (mul_eq_zero.mp hmul).resolve_left ht1'

/-- Every function of the matrix is constant along the rescaling.
The momentum does not determine `t`, so it does not determine a weight in `t`. -/
theorem matrix_invariant_along_rescale {β : Type*} (t : α) (ht : t ≠ 0)
    (u v : Fin 2 → α) (f : Matrix (Fin 2) (Fin 2) α → β) :
    f (outer (fun i => t * u i) (fun j => v j / t)) = f (outer u v) := by
  rw [outer_rescale t ht u v]

end Field

/-!
The four edges of the rational polygon in the atlas. The factors are the ones
`factor_rank1` exhibits. `t = 2` is the rescaling drawn on the card.
-/

def polygonZ0 : Twistor ℚ :=
  { lam := vec2 0 1, mu := vec2 0 0 }

def polygonZ1 : Twistor ℚ :=
  { lam := vec2 1 0, mu := vec2 2 0 }

def polygonZ2 : Twistor ℚ :=
  { lam := vec2 0 1, mu := vec2 0 2 }

def polygonZ3 : Twistor ℚ :=
  { lam := vec2 1 0, mu := vec2 0 0 }

def polygonZ : Fin 4 → Twistor ℚ
  | 0 => polygonZ0
  | 1 => polygonZ1
  | 2 => polygonZ2
  | 3 => polygonZ3

/-- Column factor of edge `i`, as exhibited by the shadow. -/
def edgeFactorU : Fin 4 → Fin 2 → ℚ
  | 0 => vec2 (-2) 0
  | 1 => vec2 0 (-2)
  | 2 => vec2 2 0
  | 3 => vec2 0 2

/-- Row factor of edge `i`. -/
def edgeFactorV : Fin 4 → Fin 2 → ℚ
  | 0 => vec2 1 0
  | 1 => vec2 0 1
  | 2 => vec2 1 0
  | 3 => vec2 0 1

private lemma fin4_prev_0 : (0 : Fin 4) - 1 = 3 := by decide
private lemma fin4_prev_1 : (1 : Fin 4) - 1 = 0 := by decide
private lemma fin4_prev_2 : (2 : Fin 4) - 1 = 1 := by decide
private lemma fin4_prev_3 : (3 : Fin 4) - 1 = 2 := by decide
private lemma fin4_next_0 : (0 : Fin 4) + 1 = 1 := by decide
private lemma fin4_next_1 : (1 : Fin 4) + 1 = 2 := by decide
private lemma fin4_next_2 : (2 : Fin 4) + 1 = 3 := by decide
private lemma fin4_next_3 : (3 : Fin 4) + 1 = 0 := by decide

private lemma edge_index (i : Fin 4) : (i + 1) - 1 = i := by
  fin_cases i <;> decide

private theorem edgeMomentum_eq (i : Fin 4) (prev curr next : Twistor ℚ)
    (hp : polygonZ (i - 1) = prev) (hc : polygonZ i = curr) (hn : polygonZ (i + 1) = next) :
    edgeMomentum polygonZ i =
      regionMatrix prev curr - regionMatrix curr next := by
  simp only [edgeMomentum, xRegion, hp, hc, hn, edge_index i]

private theorem edge0_idx :
    edgeMomentum polygonZ 0 =
      regionMatrix polygonZ3 polygonZ0 - regionMatrix polygonZ0 polygonZ1 :=
  edgeMomentum_eq 0 polygonZ3 polygonZ0 polygonZ1
    (by rw [fin4_prev_0]; rfl) rfl (by rw [fin4_next_0]; rfl)

private theorem edge1_idx :
    edgeMomentum polygonZ 1 =
      regionMatrix polygonZ0 polygonZ1 - regionMatrix polygonZ1 polygonZ2 :=
  edgeMomentum_eq 1 polygonZ0 polygonZ1 polygonZ2
    (by rw [fin4_prev_1]; rfl) rfl (by rw [fin4_next_1]; rfl)

private theorem edge2_idx :
    edgeMomentum polygonZ 2 =
      regionMatrix polygonZ1 polygonZ2 - regionMatrix polygonZ2 polygonZ3 :=
  edgeMomentum_eq 2 polygonZ1 polygonZ2 polygonZ3
    (by rw [fin4_prev_2]; rfl) rfl (by rw [fin4_next_2]; rfl)

private theorem edge3_idx :
    edgeMomentum polygonZ 3 =
      regionMatrix polygonZ2 polygonZ3 - regionMatrix polygonZ3 polygonZ0 :=
  edgeMomentum_eq 3 polygonZ2 polygonZ3 polygonZ0
    (by rw [fin4_prev_3]; rfl) rfl (by rw [fin4_next_3]; rfl)

private theorem concrete_edges :
    (regionMatrix polygonZ3 polygonZ0 - regionMatrix polygonZ0 polygonZ1) =
        outer (vec2 (-2 : ℚ) 0) (vec2 1 0) ∧
    (regionMatrix polygonZ0 polygonZ1 - regionMatrix polygonZ1 polygonZ2) =
        outer (vec2 (0 : ℚ) (-2)) (vec2 0 1) ∧
    (regionMatrix polygonZ1 polygonZ2 - regionMatrix polygonZ2 polygonZ3) =
        outer (vec2 (2 : ℚ) 0) (vec2 1 0) ∧
    (regionMatrix polygonZ2 polygonZ3 - regionMatrix polygonZ3 polygonZ0) =
        outer (vec2 (0 : ℚ) 2) (vec2 0 1) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    ext r c <;> fin_cases r <;> fin_cases c <;>
      simp only [Matrix.sub_apply, regionMatrix, angle, outer,
        polygonZ0, polygonZ1, polygonZ2, polygonZ3, vec2_zero, vec2_one] <;>
      norm_num

theorem polygon_edge_outer (i : Fin 4) :
    edgeMomentum polygonZ i = outer (edgeFactorU i) (edgeFactorV i) := by
  match i with
  | 0 =>
    rw [edge0_idx]
    simpa [edgeFactorU, edgeFactorV] using concrete_edges.1
  | 1 =>
    rw [edge1_idx]
    simpa [edgeFactorU, edgeFactorV] using concrete_edges.2.1
  | 2 =>
    rw [edge2_idx]
    simpa [edgeFactorU, edgeFactorV] using concrete_edges.2.2.1
  | 3 =>
    rw [edge3_idx]
    simpa [edgeFactorU, edgeFactorV] using concrete_edges.2.2.2

theorem polygon_edge_rescale (i : Fin 4) :
    outer (fun a => (2 : ℚ) * edgeFactorU i a) (fun b => edgeFactorV i b / 2) =
      edgeMomentum polygonZ i := by
  rw [outer_rescale (2 : ℚ) (by norm_num) (edgeFactorU i) (edgeFactorV i)]
  exact (polygon_edge_outer i).symm

theorem edgeFactorU_zero_ne_zero : edgeFactorU 0 ≠ 0 := by
  intro h
  have h0 := congrFun h 0
  simp only [edgeFactorU, vec2_zero] at h0
  norm_num at h0

/-- At `t = 2` the column factor of edge 0 moves and the momentum does not. -/
theorem edge0_momentum_misses_t :
    (fun a => (2 : ℚ) * edgeFactorU 0 a) ≠ edgeFactorU 0 ∧
      outer (fun a => (2 : ℚ) * edgeFactorU 0 a) (fun b => edgeFactorV 0 b / 2) =
        edgeMomentum polygonZ 0 :=
  ⟨rescale_moves_factor (by norm_num) edgeFactorU_zero_ne_zero, polygon_edge_rescale 0⟩

end UOPG0
