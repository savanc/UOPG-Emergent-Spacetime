/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT2

/-!
# X6 / XD-6 / R2 — `chirality_orientation` lemma

Also known as: X6 chirality lemma, XD-6, STRUCT route R2, positroid sign / helicity orientation.

Result (NO-GO plus LINK-LEMMA).
* The positive Grassmannian's sign structure is invariant under parity (the twisted complement,
  k ↔ n − k, λ ↔ λ̃; CITED: Galashin–Lam arXiv:1805.00600) and under cyclic reflection. Proved here
  for Gr(2,4) Plücker data, so positivity cannot by itself select a chiral spectrum.
* Vector-like spectra satisfy all ACC power sums identically (the ACC are vacuous without chirality).
* The STRUCT-2 one-generation branch is vector-like at `N_c = 1` and chiral for `N_c ≥ 2`. With Witten
  this gives `N_c` odd and `N_c ≥ 3`; it still does not select 3.
-/

namespace PositiveGeometryEmergentSpaceTime.X6

/-- Plücker coordinates of a point of Gr(2,4), `p_ij` for `i < j`.
Also known as: Δ_ij, ⟨ij⟩ (4-point spinor brackets in the positroid picture). -/
structure Plucker24 where
  /-- Plücker coordinate p_12 (aka Δ_12). -/
  p12 : ℝ
  /-- Plücker coordinate p_13 (aka Δ_13). -/
  p13 : ℝ
  /-- Plücker coordinate p_14 (aka Δ_14). -/
  p14 : ℝ
  /-- Plücker coordinate p_23 (aka Δ_23). -/
  p23 : ℝ
  /-- Plücker coordinate p_24 (aka Δ_24). -/
  p24 : ℝ
  /-- Plücker coordinate p_34 (aka Δ_34). -/
  p34 : ℝ

/-- Plücker relation for Gr(2,4). Also known as: three-term Plücker / Schouten identity. -/
def Plucker24.rel (p : Plucker24) : Prop := p.p13 * p.p24 = p.p12 * p.p34 + p.p14 * p.p23

/-- Totally positive point of Gr(2,4). Also known as: Gr₊(2,4), positroid top cell. -/
def Plucker24.pos (p : Plucker24) : Prop :=
  0 < p.p12 ∧ 0 < p.p13 ∧ 0 < p.p14 ∧ 0 < p.p23 ∧ 0 < p.p24 ∧ 0 < p.p34

/-- Parity map on Gr(2,4): twisted complement, `p_I ↦ p_{Iᶜ}` (alternating column signs absorbed).
Also known as: parity duality, twist map (Marsh–Scott), λ ↔ λ̃, MHV ↔ anti-MHV, k ↔ n − k. -/
def parityDual (p : Plucker24) : Plucker24 := ⟨p.p34, p.p24, p.p23, p.p14, p.p13, p.p12⟩

/-- Cyclic reflection `i ↦ 5 − i`: `p_ij ↦ p_{5−j,5−i}` (overall sign −1 dropped projectively).
Also known as: orientation reversal, dihedral reflection of the positroid. -/
def reflect (p : Plucker24) : Plucker24 := ⟨p.p34, p.p24, p.p14, p.p23, p.p13, p.p12⟩

/-- C1: parity preserves positivity. -/
theorem parityDual_pos {p : Plucker24} (h : p.pos) : (parityDual p).pos := by
  obtain ⟨a, b, c, d, e, f⟩ := h; exact ⟨f, e, d, c, b, a⟩

/-- C1: parity preserves the Plücker relation. -/
theorem parityDual_rel {p : Plucker24} (h : p.rel) : (parityDual p).rel := by
  unfold Plucker24.rel at *; simp only [parityDual]; linarith

/-- Parity is an involution. -/
theorem parityDual_invol (p : Plucker24) : parityDual (parityDual p) = p := by
  cases p; rfl

/-- C2: reflection preserves positivity and the Plücker relation. -/
theorem reflect_pos_rel {p : Plucker24} (h : p.pos) (hr : p.rel) : (reflect p).pos ∧ (reflect p).rel := by
  obtain ⟨a, b, c, d, e, f⟩ := h
  refine ⟨⟨f, e, c, d, b, a⟩, ?_⟩
  unfold Plucker24.rel at *; simp only [reflect]; linarith

/-- NO-GO (`chirality_orientation`): Gr₊(2,4) is mapped onto itself by both orientation-changing
maps, so positivity does not distinguish an orientation (helicity sign). -/
theorem positivity_orientation_blind {p : Plucker24} (h : p.pos) (hr : p.rel) :
    (parityDual p).pos ∧ (parityDual p).rel ∧ (reflect p).pos ∧ (reflect p).rel :=
  ⟨parityDual_pos h, parityDual_rel hr, (reflect_pos_rel h hr).1, (reflect_pos_rel h hr).2⟩

/-- C3: a vector-like spectrum (every Weyl state `y_i` paired with `−y_i`, multiplicity `m_i`)
has vanishing linear and cubic anomaly sums. Also known as: real / vector-like representation. -/
theorem vectorlike_acc_vanish {ι : Type*} (s : Finset ι) (m y : ι → ℚ) :
    (∑ i ∈ s, m i * y i + ∑ i ∈ s, m i * (-y i) = 0) ∧
    (∑ i ∈ s, m i * y i ^ 3 + ∑ i ∈ s, m i * (-y i) ^ 3 = 0) := by
  constructor <;> rw [← Finset.sum_add_distrib] <;> exact Finset.sum_eq_zero (fun i _ => by ring)

/-- One-generation hypercharge multiset on the STRUCT-2 branch with `yQ = 1`
(`yu = N_c − 1`, `yd = −N_c − 1`, `yL = −N_c`, `ye = 2 N_c`), each state with its multiplicity.
Also known as: SM Weyl charges (Q, uᶜ, dᶜ, L, eᶜ). -/
def branchCharges (N_c : ℕ) : List ℤ :=
  List.replicate (2 * N_c) 1 ++ List.replicate N_c ((N_c : ℤ) - 1) ++
    List.replicate N_c (-(N_c : ℤ) - 1) ++ List.replicate 2 (-(N_c : ℤ)) ++ [2 * (N_c : ℤ)]

/-- Vector-like: the charge multiset is closed under negation. -/
def VectorLike (l : List ℤ) : Prop := (l.map Neg.neg).Perm l

/-- C4a: at `N_c = 1` the anomaly-free branch is vector-like (ACC content is trivial). -/
theorem branch_one_vectorlike : VectorLike (branchCharges 1) := by
  unfold VectorLike branchCharges; decide

/-- C4b: for `N_c ≥ 2` the charge `−1` is absent while `1` (Q) is present, so the branch is chiral. -/
theorem branch_chiral {N_c : ℕ} (h : 2 ≤ N_c) : ¬ VectorLike (branchCharges N_c) := by
  intro hv
  have h1 : (1 : ℤ) ∈ branchCharges N_c := by
    simp [branchCharges, List.mem_replicate]; omega
  have h2 : (-1 : ℤ) ∈ branchCharges N_c := by
    have : (-1 : ℤ) ∈ (branchCharges N_c).map Neg.neg := List.mem_map.2 ⟨1, h1, rfl⟩
    exact hv.subset this
  simp [branchCharges, List.mem_replicate] at h2; omega

/-- LINK-LEMMA: chirality (`N_c ≥ 2`) plus Witten gives odd `N_c ≥ 3`; `N_c = 3` and `N_c = 5` both
  pass. -/
theorem chiral_witten_not_selected :
    (¬ VectorLike (branchCharges 3) ∧ STRUCT2.Witten 3) ∧ (¬ VectorLike (branchCharges 5) ∧ STRUCT2.Witten 5) :=
  ⟨⟨branch_chiral (by norm_num), ⟨2, rfl⟩⟩, ⟨branch_chiral (by norm_num), ⟨3, rfl⟩⟩⟩

end PositiveGeometryEmergentSpaceTime.X6
