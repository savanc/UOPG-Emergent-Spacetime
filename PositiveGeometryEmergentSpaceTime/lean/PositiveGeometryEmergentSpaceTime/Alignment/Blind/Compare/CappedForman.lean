/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.CappedForman
import PositiveGeometryEmergentSpaceTime.CappedFormanCerts
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.CappedForman1Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: CAPPED-FORMAN-1

Blind: integer numerators `cappedNum D ks = (D+1) − Σ min(3, k−3)`, `formanK`, equality iff all
faces `k ≤ 6` (plus strict-gap/excess form and the cycle-distance face cost); certificates by BFS
distance + minimum over all bijections on prisms `C₇×K₂`, `C₈×K₂` and the truncated cube.
Original: `capB`/`formanB` over ℚ with ℕ-subtraction, the `g_k` per-face optimisation
(`face_term_le`, `face_term_max`), and LP-dual walk certificates (`CappedFormanCerts`).

VERDICT: **DIFFERENT** (overlapping cores, each has extras).
* Bound algebra: EQUIV for faces with `k ≥ 3` (`capB_eq`, `formanB_eq`); the equality criterion is
  EQUIV unconditionally (`eq_iff_agree`). For `k < 3` the two definitions differ
  (`small_face_gap`) — physically vacuous (no 2-gons) but a real definitional gap.
* Blind extras: `capped_strict_iff`/`excess`, `face_cost`. Original extra: `g_k` optimisation.
* Certificates: same graphs, same edges, same numbers. Prisms share the labelling
  (`prism7_same_graph`, `prism8_same_graph`); the truncated cube is related by an explicit kernel-checked
  isomorphism `tcIso` sending the original's certified edges to the blind's. GAP: the two
  cost functionals (blind: BFS-distance assignment minimum; original: walk-realised matching with a
  Lipschitz dual) are not proved equal as functions — only their values on these edges coincide.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.CappedForman

open PositiveGeometryEmergentSpaceTime.Alignment.CappedForman1Blind
open PositiveGeometryEmergentSpaceTime.CappedForman (capB formanB)

theorem sum_cap_cast (ks : List ℕ) (h : ∀ k ∈ ks, 3 ≤ k) :
    (((ks.map fun k : ℕ => min 3 (k - 3)).sum : ℕ) : ℤ) =
      ((ks.map fun k : ℕ => (k : ℤ)).map fun k => min 3 (k - 3)).sum := by
  induction ks with
  | nil => simp
  | cons k ks ih =>
    have hk : 3 ≤ k := h k (by simp)
    simp only [List.map_cons, List.sum_cons, Nat.cast_add]
    rw [ih (fun k' hk' => h k' (by simp [hk']))]
    congr 1
    rw [Nat.cast_min, Nat.cast_sub hk]; norm_num

theorem sum_forman_cast (ks : List ℕ) (h : ∀ k ∈ ks, 3 ≤ k) :
    (((ks.map fun k : ℕ => k - 3).sum : ℕ) : ℤ) =
      ((ks.map fun k : ℕ => (k : ℤ)).map fun k => k - 3).sum := by
  induction ks with
  | nil => simp
  | cons k ks ih =>
    have hk : 3 ≤ k := h k (by simp)
    simp only [List.map_cons, List.sum_cons, Nat.cast_add]
    rw [ih (fun k' hk' => h k' (by simp [hk']))]
    congr 1
    rw [Nat.cast_sub hk]; norm_num

/-- Original capped bound = blind numerator / (D+1), for genuine faces (k ≥ 3). -/
theorem capB_eq (D : ℕ) (ks : List ℕ) (h : ∀ k ∈ ks, 3 ≤ k) :
    capB D ks = (cappedNum (D : ℤ) (ks.map fun k : ℕ => (k : ℤ)) : ℚ) / ((D : ℚ) + 1) := by
  have hD : (D : ℚ) + 1 ≠ 0 := by positivity
  unfold capB cappedNum
  have := congrArg (fun z : ℤ => (z : ℚ)) (sum_cap_cast ks h)
  simp only [Int.cast_natCast] at this
  rw [this]; push_cast; field_simp

theorem formanB_eq (D : ℕ) (ks : List ℕ) (h : ∀ k ∈ ks, 3 ≤ k) :
    formanB D ks = (formanK (D : ℤ) (ks.map fun k : ℕ => (k : ℤ)) : ℚ) / ((D : ℚ) + 1) := by
  have hD : (D : ℚ) + 1 ≠ 0 := by positivity
  unfold formanB formanK
  have := congrArg (fun z : ℤ => (z : ℚ)) (sum_forman_cast ks h)
  simp only [Int.cast_natCast] at this
  rw [this]; push_cast; field_simp

/-- The equality criteria agree (no face-size hypothesis needed). -/
theorem eq_iff_agree (D : ℕ) (ks : List ℕ) :
    capB D ks = formanB D ks ↔
      cappedNum (D : ℤ) (ks.map fun k : ℕ => (k : ℤ)) = formanK (D : ℤ) (ks.map fun k : ℕ => (k : ℤ)) := by
  rw [PositiveGeometryEmergentSpaceTime.CappedForman.capped_eq_forman_iff, capped_eq_iff]
  simp

/-- Definitional gap for k < 3 (ℕ-subtraction in the original). -/
theorem small_face_gap : capB 3 [2] ≠ (cappedNum 3 [2] : ℚ) / 4 := by
  unfold capB cappedNum; norm_num

/-! ### Certificates: same graphs, same edges, same values -/

theorem prism7_same_graph :
    ∀ a b : Fin 14, PositiveGeometryEmergentSpaceTime.CappedFormanCerts.Prism7H.adj a b = prismAdj 7 a.val b.val := by
  decide +kernel

theorem prism8_same_graph :
    ∀ a b : Fin 16, PositiveGeometryEmergentSpaceTime.CappedFormanCerts.Prism8H.adj a b = prismAdj 8 a.val b.val := by
  decide +kernel

/-- Explicit isomorphism original truncated-cube labelling → blind labelling (found by search,
checked by the kernel). Sends original edge 0–2 (TriOct) to blind 0–1 and 0–1 (OctOct) to 0–3. -/
def tcIso (i : Fin 24) : ℕ :=
  ([0, 3, 1, 7, 2, 14, 6, 9, 8, 20, 10, 4, 11, 23, 5, 17, 13, 19, 12, 15, 18, 21, 22, 16] : List ℕ).getD i.val 0

theorem tcIso_iso :
    (∀ a b : Fin 24, PositiveGeometryEmergentSpaceTime.CappedFormanCerts.TCubeTriOct.adj a b = tcAdj (tcIso a) (tcIso b)) ∧
    (∀ a b : Fin 24, tcIso a = tcIso b → a = b) ∧ (∀ a : Fin 24, tcIso a < 24) ∧
    tcIso 0 = 0 ∧ tcIso 2 = 1 ∧ tcIso 1 = 3 := by
  decide +kernel

/-- The orig OctOct certificate uses the same graph table as TriOct. -/
theorem tc_tables_same : PositiveGeometryEmergentSpaceTime.CappedFormanCerts.TCubeTriOct.nbrT = PositiveGeometryEmergentSpaceTime.CappedFormanCerts.TCubeOctOct.nbrT :=
  rfl

/-- Values: blind matching costs equal the original certified integers (4, 2, 4, 2, 3, 6), and the
blind κ equals the left side of each original `kappa_eq_B`. -/
theorem values_agree :
    kappaOf (matchCost 14 (prismAdj 7) 0 1) 3 = 1 - 4 / 4 ∧
    kappaOf (matchCost 14 (prismAdj 7) 0 7) 3 = 1 - 2 / 4 ∧
    kappaOf (matchCost 16 (prismAdj 8) 0 1) 3 = 1 - 4 / 4 ∧
    kappaOf (matchCost 16 (prismAdj 8) 0 8) 3 = 1 - 2 / 4 ∧
    kappaOf (matchCost 24 tcAdj 0 1) 3 = 1 - 3 / 4 ∧
    kappaOf (matchCost 24 tcAdj 0 3) 3 = 1 - 6 / 4 := by
  obtain ⟨a, b⟩ := prism7_costs
  obtain ⟨c, d⟩ := prism8_costs
  obtain ⟨-, e, -, f⟩ := tc_costs
  simp only [kappaOf, a, b, c, d, e, f]; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.CappedForman
