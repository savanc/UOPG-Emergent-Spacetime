/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE C (2026-11-03) — JORD-1: sparse-vector lemmas shared by `Jord1Jordan` and `Jord1Der`.
Not part of `import PositiveGeometryEmergentSpaceTime`.
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Sanity

/-!
# JORD-1 sparse bridge

Lemmas about the sparse vectors `List (ℕ × ℤ)` used by the table `T1s`: coefficients of appends, scalings
and `flatMap`s; dense sums over `Fin 27` of an index-valid sparse vector; and the coefficients of the
sparse product `prodS`.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Bridge
open PositiveGeometryEmergentSpaceTime.Jord1 PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Sanity

/-- The structure constants are symmetric. -/
theorem bc_comm (i j l : Fin 27) : bc i j l = bc j i l := by
  have h := comm_ok_true
  simp only [comm_ok, allFin_iff, beq_iff_eq] at h
  exact h i j l

/-- Coefficients of an append. -/
theorem coefS_append (u v : List (ℕ × ℤ)) (l : ℕ) : coefS (u ++ v) l = coefS u l + coefS v l := by
  induction u with
  | nil => simp [coefS]
  | cons p r ih => simp only [List.cons_append, coefS, ih]; ring

/-- Coefficients of a scaled sparse vector. -/
theorem coefS_scale (c : ℤ) (u : List (ℕ × ℤ)) (l : ℕ) :
    coefS (u.map (fun r => (r.1, c * r.2))) l = c * coefS u l := by
  induction u with
  | nil => simp [coefS]
  | cons p r ih => simp only [List.map_cons, coefS, ih]; split_ifs <;> ring

/-- Coefficients of a `flatMap`. -/
theorem coefS_flatMap {α : Type} (u : List α) (f : α → List (ℕ × ℤ)) (l : ℕ) :
    coefS (u.flatMap f) l = (u.map fun p => coefS (f p) l).sum := by
  induction u with
  | nil => simp [coefS]
  | cons p r ih => simp only [List.flatMap_cons, coefS_append, ih, List.map_cons, List.sum_cons]

/-- A dense `Fin 27` sum against an index-valid sparse vector is a list sum over its entries. -/
theorem sum_coefS : ∀ (u : List (ℕ × ℤ)), idxOK u = true → ∀ g : ℕ → ℚ,
    ∑ a : Fin 27, (coefS u a : ℚ) * g a = (u.map fun p => (p.2 : ℚ) * g p.1).sum
  | [], _, g => by simp [coefS]
  | p :: r, h, g => by
    simp only [idxOK, List.all_cons, Bool.and_eq_true, decide_eq_true_eq] at h
    have ih := sum_coefS r h.2 g
    simp only [coefS, Int.cast_add, add_mul, Finset.sum_add_distrib, ih, List.map_cons, List.sum_cons]
    congr 1
    rw [Finset.sum_eq_single (⟨p.1, h.1⟩ : Fin 27)]
    · simp
    · intro b _ hb
      have : p.1 ≠ (b : ℕ) := fun he => hb (Fin.ext he.symm)
      simp [this]
    · intro hn; exact absurd (Finset.mem_univ _) hn

/-- Table entries use indices below 27. -/
theorem T1s_idx (a b : ℕ) (ha : a < 27) (hb : b < 27) : idxOK ((T1s.getD a []).getD b []) = true := by
  have h := idx_ok_true
  simp only [idx_ok, allFin_iff, Bool.and_eq_true] at h
  exact (h ⟨a, ha⟩ ⟨b, hb⟩).1

/-- `idxOK` as a statement about members. -/
theorem idxOK_iff (u : List (ℕ × ℤ)) : idxOK u = true ↔ ∀ p ∈ u, p.1 < 27 := by
  simp [idxOK, List.all_eq_true]

/-- The sparse product of index-valid vectors is index-valid. -/
theorem idxOK_prodS (u v : List (ℕ × ℤ)) (hu : idxOK u = true) (hv : idxOK v = true) :
    idxOK (prodS u v) = true := by
  rw [idxOK_iff] at *
  intro r hr
  simp only [prodS, List.mem_flatMap, List.mem_map] at hr
  obtain ⟨p, hp, q, hq, s, hs, rfl⟩ := hr
  exact (idxOK_iff _).1 (T1s_idx p.1 q.1 (hu p hp) (hv q hq)) s hs

/-- Coefficients of the sparse product `prodS`. -/
theorem coefS_prodS (u v : List (ℕ × ℤ)) (l : ℕ) :
    coefS (prodS u v) l = (u.map fun p => (v.map fun q => p.2 * q.2 * bc p.1 q.1 l).sum).sum := by
  unfold prodS
  rw [coefS_flatMap]
  congr 1; apply List.map_congr_left; intro p _
  rw [coefS_flatMap]
  congr 1; apply List.map_congr_left; intro q _
  rw [coefS_scale]; rfl

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Bridge
