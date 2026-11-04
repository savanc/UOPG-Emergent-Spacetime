/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
INT-1 (prereg/INT-1-chamber-constancy-2026-10-22.md): integer invariants of the n = 5 kinematic
associahedron with mass offsets are constant on each open chamber of the offset arrangement and can
change only on walls.

Reuses `PositiveGeometryEmergentSpaceTime.Assoc.X` (facet order X14, X24, X25, X35, X13; coordinates x = X13, y = X14).
The eight non-parallel facet-pair intersection points `pt` (X14 ∥ X35 and X25 ∥ X13 are parallel)
have slacks that are 0 or ± one of six linear forms in (c13, c14, c24) (`slack_eq`). Hence every sign
pattern, the labelled vertex set (`vertexType`), and any function of it (f-vector, …) factor through
the chamber sign vector (`faceType_locallyConstant`, `invariant_chamber_constant`). Mass offsets
X_k ≥ m_k are a translation with shifted constants (`mass_shift`, `massRegion_iff`).
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Associahedron

namespace PositiveGeometryEmergentSpaceTime.IntChamber

open PositiveGeometryEmergentSpaceTime.Assoc Finset

/-- The six wall forms in c-space: c13, c14, c24, c13+c14, c14+c24, c13+c14+c24. -/
def forms (a b e : ℝ) : Fin 6 → ℝ := ![a, b, e, a + b, b + e, a + b + e]

/-- Chamber sign vector. -/
noncomputable def chamberSign (a b e : ℝ) : Fin 6 → SignType := fun i => SignType.sign (forms a b e i)

/-- The eight pair points (x, y) = (X13, X14): X14∩X24, X14∩X25, X14∩X13, X24∩X25, X24∩X35,
X24∩X13, X25∩X35, X35∩X13. -/
def pt (a b e : ℝ) : Fin 8 → ℝ × ℝ :=
  ![(a, 0), (a + b, 0), (0, 0), (a + b, b), (a + b + e, b + e), (0, -a), (a + b, b + e), (0, b + e)]

/-- Slack table: `none` = 0, `some (true, i)` = + form i, `some (false, i)` = − form i. -/
def T : Fin 8 → Fin 5 → Option (Bool × Fin 6) :=
  ![![none, none, some (true, 1), some (true, 4), some (true, 0)],
    ![none, some (false, 1), none, some (true, 4), some (true, 3)],
    ![none, some (true, 0), some (true, 3), some (true, 4), none],
    ![some (true, 1), none, none, some (true, 2), some (true, 3)],
    ![some (true, 4), none, some (false, 2), none, some (true, 5)],
    ![some (false, 0), none, some (true, 3), some (true, 5), none],
    ![some (true, 4), some (true, 2), none, none, some (true, 3)],
    ![some (true, 4), some (true, 5), some (true, 3), none, none]]

/-- Real value of a table entry. -/
def val (f : Fin 6 → ℝ) : Option (Bool × Fin 6) → ℝ
  | none => 0
  | some (true, i) => f i
  | some (false, i) => -f i

/-- Sign of a table entry given only the chamber sign vector. -/
def dec (s : Fin 6 → SignType) : Option (Bool × Fin 6) → SignType
  | none => 0
  | some (true, i) => s i
  | some (false, i) => -s i

/-- Every slack at every pair point is 0 or ± a wall form. -/
theorem slack_eq (a b e : ℝ) (p : Fin 8) (k : Fin 5) :
    X a b e (pt a b e p).1 (pt a b e p).2 k = val (forms a b e) (T p k) := by
  fin_cases p <;> fin_cases k <;> simp [X, pt, T, val, forms] <;> ring

/-- The sign of a table entry's real value equals the entry decoded from the sign vector alone:
  `sign (val f o) = dec (sign ∘ f) o`. -/
theorem sign_val (f : Fin 6 → ℝ) (o : Option (Bool × Fin 6)) :
    SignType.sign (val f o) = dec (fun i => SignType.sign (f i)) o := by
  rcases o with _ | ⟨_ | _, i⟩ <;> simp [val, dec, Left.sign_neg]

/-- `slack_sign_eq`: the sign table of all slacks is a function of the chamber sign vector. -/
theorem slack_sign_eq (a b e : ℝ) (p : Fin 8) (k : Fin 5) :
    SignType.sign (X a b e (pt a b e p).1 (pt a b e p).2 k) = dec (chamberSign a b e) (T p k) := by
  rw [slack_eq, sign_val]; rfl

/-- Labelled vertex set from a sign vector: tight-facet sets of the feasible pair points. -/
def vertexTypeσ (s : Fin 6 → SignType) : Finset (Finset (Fin 5)) :=
  (univ.filter fun p : Fin 8 => ∀ k, dec s (T p k) ≠ -1).image
    fun p => univ.filter fun k => dec s (T p k) = 0

open Classical in
/-- Labelled vertex set of the actual polygon `Assoc.region a b e`: tight sets of the feasible
facet-pair intersection points. -/
noncomputable def vertexType (a b e : ℝ) : Finset (Finset (Fin 5)) :=
  (univ.filter fun p : Fin 8 => ∀ k, 0 ≤ X a b e (pt a b e p).1 (pt a b e p).2 k).image
    fun p => univ.filter fun k => X a b e (pt a b e p).1 (pt a b e p).2 k = 0

/-- Each feasible pair point lies in the closed region. -/
theorem pt_mem_region {a b e : ℝ} {p : Fin 8}
    (h : ∀ k, 0 ≤ X a b e (pt a b e p).1 (pt a b e p).2 k) :
    region a b e (pt a b e p).1 (pt a b e p).2 := h

/-- The vertex type at real parameters `(a, b, e)` depends only on the chamber sign vector
  `chamberSign a b e`. -/
theorem vertexType_eq (a b e : ℝ) : vertexType a b e = vertexTypeσ (chamberSign a b e) := by
  unfold vertexType vertexTypeσ
  have h0 : ∀ p k, (0 ≤ X a b e (pt a b e p).1 (pt a b e p).2 k) ↔
      dec (chamberSign a b e) (T p k) ≠ -1 := by
    intro p k; rw [← slack_sign_eq, Ne, sign_eq_neg_one_iff, not_lt]
  have hz : ∀ p k, (X a b e (pt a b e p).1 (pt a b e p).2 k = 0) ↔
      dec (chamberSign a b e) (T p k) = 0 := by
    intro p k; rw [← slack_sign_eq, sign_eq_zero_iff]
  ext t
  simp only [mem_image, mem_filter, mem_univ, true_and]
  refine exists_congr fun p => and_congr (forall_congr' (h0 p)) ?_
  rw [Finset.filter_congr (fun k _ => hz p k)]

/-- `faceType_locallyConstant`: equal chamber sign vectors ⇒ equal labelled vertex sets. -/
theorem faceType_locallyConstant {a b e a' b' e' : ℝ}
    (h : chamberSign a b e = chamberSign a' b' e') : vertexType a b e = vertexType a' b' e' := by
  rw [vertexType_eq, vertexType_eq, h]

/-- Any integer invariant of the labelled vertex set is chamber-constant. -/
theorem invariant_chamber_constant (F : Finset (Finset (Fin 5)) → ℤ) {a b e a' b' e' : ℝ}
    (h : chamberSign a b e = chamberSign a' b' e') : F (vertexType a b e) = F (vertexType a' b' e') := by
  rw [faceType_locallyConstant h]

/-! ## Walls: sign changes need a zero on the segment -/

/-- If `(1 − t)u + t v ≠ 0` for all `t ∈ [0, 1]`, then `u` and `v` have the same sign. -/
theorem sign_eq_of_segment {u v : ℝ} (h : ∀ t ∈ Set.Icc (0 : ℝ) 1, (1 - t) * u + t * v ≠ 0) :
    SignType.sign u = SignType.sign v := by
  have hu : u ≠ 0 := by simpa using h 0 (by simp)
  have hv : v ≠ 0 := by simpa using h 1 (by simp)
  rcases lt_or_gt_of_ne hu with hu' | hu' <;> rcases lt_or_gt_of_ne hv with hv' | hv'
  · simp [sign_neg hu', sign_neg hv']
  · exfalso
    refine h (u / (u - v)) ⟨div_nonneg_of_nonpos hu'.le (by linarith), ?_⟩ ?_
    · rw [div_le_one_of_neg (by linarith)]; linarith
    · field_simp [show u - v ≠ 0 by linarith]; ring
  · exfalso
    refine h (u / (u - v)) ⟨div_nonneg hu'.le (by linarith), ?_⟩ ?_
    · rw [div_le_one (by linarith)]; linarith
    · field_simp [show u - v ≠ 0 by linarith]; ring
  · simp [sign_pos hu', sign_pos hv']

/-- Each wall form is affine in the parameters: `forms` at the interpolated point is the
  interpolation of `forms`. -/
theorem forms_lerp (a b e a' b' e' t : ℝ) (i : Fin 6) :
    forms ((1 - t) * a + t * a') ((1 - t) * b + t * b') ((1 - t) * e + t * e') i =
      (1 - t) * forms a b e i + t * forms a' b' e' i := by
  fin_cases i <;> simp [forms] <;> ring

/-- `jump_only_on_wall`: if no wall form vanishes on the segment from c to c', the chamber (hence
the labelled vertex set and every invariant of it) is the same at both ends. -/
theorem jump_only_on_wall {a b e a' b' e' : ℝ}
    (h : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ i,
      forms ((1 - t) * a + t * a') ((1 - t) * b + t * b') ((1 - t) * e + t * e') i ≠ 0) :
    chamberSign a b e = chamberSign a' b' e' ∧ vertexType a b e = vertexType a' b' e' := by
  have hs : chamberSign a b e = chamberSign a' b' e' := by
    funext i
    exact sign_eq_of_segment fun t ht => by rw [← forms_lerp]; exact h t ht i
  exact ⟨hs, faceType_locallyConstant hs⟩

/-! ## Mass offsets are a translation (m : Fin 5 → ℝ in facet order X14, X24, X25, X35, X13) -/

/-- `mass_shift`: X_k − m_k = X at the effective constants c' and shifted coordinates. -/
theorem mass_shift (a b e x y : ℝ) (m : Fin 5 → ℝ) (k : Fin 5) :
    X a b e x y k - m k =
      X (a + m 0 - m 4 - m 1) (b - m 0 - m 2 + m 1) (e - m 1 - m 3 + m 2) (x - m 4) (y - m 0) k := by
  fin_cases k <;> simp [X] <;> ring

/-- `massRegion_iff`: the massive region {X_k ≥ m_k} is the region at c' translated by (m13, m14). -/
theorem massRegion_iff (a b e x y : ℝ) (m : Fin 5 → ℝ) :
    (∀ k, m k ≤ X a b e x y k) ↔
      region (a + m 0 - m 4 - m 1) (b - m 0 - m 2 + m 1) (e - m 1 - m 3 + m 2) (x - m 4) (y - m 0) := by
  unfold region
  refine forall_congr' fun k => ?_
  rw [← mass_shift]; constructor <;> intro h <;> linarith

/-! ## Planted chambers (decide on the sign tables) -/

/-- Number of distinct vertex types for a chamber sign vector (the vertex count of the region). -/
def f0 (s : Fin 6 → SignType) : ℕ := (vertexTypeσ s).card
/-- Facets carrying ≥ 2 distinct vertices (edges). -/
def f1 (s : Fin 6 → SignType) : ℕ :=
  (univ.filter fun k : Fin 5 => 2 ≤ ((vertexTypeσ s).filter fun t => k ∈ t).card).card

/-- Sign vector of the all-positive chamber (all six wall forms positive). -/
def σPos : Fin 6 → SignType := fun _ => 1
/-- Sign vector on the merging wall (wall form 2 zero, all others positive). -/
def σWall : Fin 6 → SignType := ![1, 1, 0, 1, 1, 1]
/-- Sign vector beyond the merging wall (wall form 2 negative, all others positive). -/
def σBeyond : Fin 6 → SignType := ![1, 1, -1, 1, 1, 1]

/-- In the positive chamber the region has 5 vertices and 5 edges (a pentagon), by `decide`. -/
theorem f_pos : f0 σPos = 5 ∧ f1 σPos = 5 := by decide
/-- On the merging wall the region has 4 vertices and 4 edges, by `decide`. -/
theorem f_wall : f0 σWall = 4 ∧ f1 σWall = 4 := by decide
/-- At the merging wall the three facets X24, X25, X35 meet at one vertex. -/
theorem wall_triple : ({1, 2, 3} : Finset (Fin 5)) ∈ vertexTypeσ σWall := by decide
/-- Beyond the wall the region has 4 vertices and 4 edges and facet 2 carries no vertex, by
  `decide`. -/
theorem f_beyond : f0 σBeyond = 4 ∧ f1 σBeyond = 4 ∧ ∀ t ∈ vertexTypeσ σBeyond, (2 : Fin 5) ∉ t := by
  decide

/-- For `a, b, e > 0` the chamber sign vector is `σPos`. -/
theorem chamberSign_pos {a b e : ℝ} (ha : 0 < a) (hb : 0 < b) (he : 0 < e) :
    chamberSign a b e = σPos := by
  funext i; fin_cases i <;> simp [chamberSign, forms, σPos] <;> rw [sign_eq_one_iff] <;> positivity

/-- For `a, b > 0` and `e = 0` the chamber sign vector is `σWall`. -/
theorem chamberSign_wall {a b : ℝ} (ha : 0 < a) (hb : 0 < b) : chamberSign a b 0 = σWall := by
  funext i; fin_cases i <;> simp [chamberSign, forms, σWall] <;> rw [sign_eq_one_iff] <;> positivity

/-- For `a > 0`, `e < 0`, `b + e > 0` the chamber sign vector is `σBeyond`. -/
theorem chamberSign_beyond {a b e : ℝ} (ha : 0 < a) (he : e < 0) (hbe : 0 < b + e) :
    chamberSign a b e = σBeyond := by
  funext i; fin_cases i <;> simp [chamberSign, forms, σBeyond]
  all_goals first
    | (rw [sign_eq_one_iff]; linarith)
    | (rw [sign_eq_neg_one_iff]; linarith)

/-- On the whole positive chamber the polygon is a labelled pentagon, f = (5, 5). -/
theorem pentagon_on_chamber {a b e : ℝ} (ha : 0 < a) (hb : 0 < b) (he : 0 < e) :
    vertexType a b e = vertexTypeσ σPos ∧ (vertexType a b e).card = 5 := by
  rw [vertexType_eq, chamberSign_pos ha hb he]; exact ⟨rfl, f_pos.1⟩

/-! ## The integers do not pin the offset ratio μ = c13'/c14' -/

/-- `ratio_free`: every μ > 0 is realised inside the pentagon chamber. -/
theorem ratio_free (r : ℝ) (hr : 0 < r) :
    ∃ a b e : ℝ, 0 < a ∧ 0 < b ∧ 0 < e ∧ a / b = r ∧ vertexType a b e = vertexTypeσ σPos :=
  ⟨r, 1, 1, hr, one_pos, one_pos, div_one r, (pentagon_on_chamber hr one_pos one_pos).1⟩

/-- `lattice_ratio`: integral constants (⇒ integral vertices `pt`) give every positive rational μ. -/
theorem lattice_ratio (q : ℚ) (hq : 0 < q) : ∃ a b : ℕ, 0 < a ∧ 0 < b ∧ (a : ℚ) / b = q := by
  refine ⟨q.num.toNat, q.den, ?_, q.den_pos, ?_⟩
  · have := Rat.num_pos.mpr hq; omega
  · have h0 : (0 : ℤ) ≤ q.num := (Rat.num_pos.mpr hq).le
    have : ((q.num.toNat : ℤ) : ℚ) = (q.num : ℚ) := by rw [Int.toNat_of_nonneg h0]
    rw [show ((q.num.toNat : ℕ) : ℚ) = ((q.num.toNat : ℤ) : ℚ) by norm_cast, this]
    exact Rat.num_div_den q

end PositiveGeometryEmergentSpaceTime.IntChamber
