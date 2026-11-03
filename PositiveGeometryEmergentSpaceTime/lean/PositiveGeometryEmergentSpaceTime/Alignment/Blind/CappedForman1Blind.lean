/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of CAPPED-FORMAN-1.
Written ONLY from the curvature paper v4 prose (Prop. "capped-Forman bound", eq. (forman),
Example "prisms and the truncated cube", Conjecture "capped-Forman equality", and the Lean table
rows "CappedForman: 8 theorems" / "CappedFormanCerts: 42 theorems"), BEFORE opening the original
modules or the blueprint.

Part 1 (algebra of the bound, any face list): with κ_F = (D+1) − Σ_F (k_F − 3) and
B = 1 − Σ_F min(3, k_F − 3)/(D+1):
  B·(D+1) = κ_F + Σ_F (k_F − 6)_+,  B ≥ κ_F/(D+1),  strict ↔ some k_F ≥ 7.
Also: on a k-cycle (k ≥ 3) the vertices u_F, v_F at cyclic distance 3 are at cycle distance
min(3, k − 3), which is the per-face coupling cost in the paper's proof.
Part 2 (certificates): exact graph distances (BFS) and the minimum PERFECT-MATCHING cost
between the two closed balls (uniform measure, idleness 1/(D+1)), for the k-gon and vertical edges
of C_7×K_2 and C_8×K_2 and both edge classes of the truncated cube. κ = 1 − cost/(D+1).
Restricting the transport to matchings is exact by Birkhoff (CITED, not proved here); so the
certificates give κ via that citation. The general inequality κ ≥ B for every simple polytope is
NOT formalised here (the paper cites Jost–Münch Cor. 6.2 for it).
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.CappedForman1Blind

/-! ### Part 1: algebra -/

/-- (D+1)·B, the capped numerator -/
def cappedNum (D : ℤ) (ks : List ℤ) : ℤ := (D + 1) - (ks.map fun k => min 3 (k - 3)).sum

/-- Forman curvature κ_F of the edge -/
def formanK (D : ℤ) (ks : List ℤ) : ℤ := (D + 1) - (ks.map fun k => k - 3).sum

def excess (ks : List ℤ) : ℤ := (ks.map fun k => max 0 (k - 6)).sum

theorem capped_eq_forman_plus_excess (D : ℤ) (ks : List ℤ) :
    cappedNum D ks = formanK D ks + excess ks := by
  induction ks with
  | nil => simp [cappedNum, formanK, excess]
  | cons k t ih =>
    simp only [cappedNum, formanK, excess, List.map_cons, List.sum_cons] at ih ⊢
    have : min 3 (k - 3) = (k - 3) - max 0 (k - 6) := by
      rcases le_total 3 (k - 3) with h | h
      · rw [min_eq_left h, max_eq_right (by omega)]; ring
      · rw [min_eq_right h, max_eq_left (by omega)]; ring
    rw [this]; linarith

theorem excess_nonneg (ks : List ℤ) : 0 ≤ excess ks := by
  unfold excess
  exact List.sum_nonneg fun x hx => by
    obtain ⟨k, _, rfl⟩ := List.mem_map.mp hx
    exact le_max_left _ _

theorem excess_pos_iff (ks : List ℤ) : 0 < excess ks ↔ ∃ k ∈ ks, 7 ≤ k := by
  induction ks with
  | nil => simp [excess]
  | cons k t ih =>
    have ht := excess_nonneg t
    simp only [excess, List.map_cons, List.sum_cons, List.mem_cons] at ih ht ⊢
    constructor
    · intro h
      by_cases hk : 7 ≤ k
      · exact ⟨k, Or.inl rfl, hk⟩
      · have : max 0 (k - 6) = 0 := max_eq_left (by omega)
        rw [this, zero_add] at h
        obtain ⟨j, hj, hj7⟩ := ih.mp h
        exact ⟨j, Or.inr hj, hj7⟩
    · rintro ⟨j, hj | hj, hj7⟩
      · subst hj; have : max 0 (j - 6) ≥ 1 := le_max_of_le_right (by omega); omega
      · have := ih.mpr ⟨j, hj, hj7⟩; have := le_max_left 0 (k - 6); omega

/-- BLIND CLAIM: B ≥ κ_F/(D+1), i.e. (D+1)B ≥ κ_F. -/
theorem capped_ge_forman (D : ℤ) (ks : List ℤ) : formanK D ks ≤ cappedNum D ks := by
  rw [capped_eq_forman_plus_excess]; linarith [excess_nonneg ks]

/-- BLIND CLAIM: strict iff some face through e has ≥ 7 sides. -/
theorem capped_strict_iff (D : ℤ) (ks : List ℤ) :
    formanK D ks < cappedNum D ks ↔ ∃ k ∈ ks, 7 ≤ k := by
  rw [capped_eq_forman_plus_excess, ← excess_pos_iff]; constructor <;> intro h <;> linarith

/-- equality iff every face through e has ≤ 6 sides -/
theorem capped_eq_iff (D : ℤ) (ks : List ℤ) :
    cappedNum D ks = formanK D ks ↔ ∀ k ∈ ks, k ≤ 6 := by
  have h1 := capped_strict_iff D ks
  have h2 := capped_ge_forman D ks
  constructor
  · intro h k hk; by_contra hc; have := h1.mpr ⟨k, hk, by omega⟩; omega
  · intro h; by_contra hne
    obtain ⟨k, hk, hk7⟩ := h1.mp (lt_of_le_of_ne h2 (Ne.symm hne)); have := h k hk; omega

/-- cycle distance on Z/k -/
def cycDist (k i j : ℕ) : ℕ := min ((i + k - j) % k) ((j + k - i) % k)

/-- per-face cost in the coupling: positions 0 and 3 on a k-cycle (k ≥ 4 so that they are
distinct after removing x, y) are at cycle distance min(3, k−3). For a triangle u_F = v_F. -/
theorem face_cost (k : ℕ) (hk : 4 ≤ k) : cycDist k 0 3 = min 3 (k - 3) := by
  unfold cycDist
  rcases Nat.lt_or_ge k 7 with h | h
  · interval_cases k <;> decide
  · have e1 : (0 + k - 3) % k = k - 3 := by
      rw [Nat.mod_eq_of_lt (show 0 + k - 3 < k by omega)]; omega
    have e2 : (3 + k - 0) % k = 3 := by
      rw [Nat.sub_zero, Nat.add_comm, Nat.add_mod_left]; exact Nat.mod_eq_of_lt (show 3 < k by omega)
    rw [e1, e2]; omega

/-! ### Part 2: exact certificates -/

/-- vertices reachable within the BFS ball, expanded once -/
def expand (V : ℕ) (adj : ℕ → ℕ → Bool) (R : List ℕ) : List ℕ :=
  (List.range V).filter fun v => R.contains v || R.any fun u => adj u v

def bfsGo (V : ℕ) (adj : ℕ → ℕ → Bool) (t : ℕ) : ℕ → List ℕ → ℕ → ℕ
  | fuel, R, d => if R.contains t then d else
      match fuel with
      | 0 => 1000
      | f + 1 => bfsGo V adj t f (expand V adj R) (d + 1)

def gdist (V : ℕ) (adj : ℕ → ℕ → Bool) (s t : ℕ) : ℕ := bfsGo V adj t V [s] 0

def cball (V : ℕ) (adj : ℕ → ℕ → Bool) (x : ℕ) : List ℕ :=
  x :: (List.range V).filter (adj x)

def insertAll (x : ℕ) : List ℕ → List (List ℕ)
  | [] => [[x]]
  | y :: ys => (x :: y :: ys) :: (insertAll x ys).map (y :: ·)

def perms : List ℕ → List (List ℕ)
  | [] => [[]]
  | x :: xs => (perms xs).flatMap (insertAll x)

/-- minimum perfect-matching cost between the closed balls of x and y -/
def matchCost (V : ℕ) (adj : ℕ → ℕ → Bool) (x y : ℕ) : ℕ :=
  let bx := cball V adj x
  let by' := cball V adj y
  let n := bx.length
  let M := bx.map fun a => by'.map fun b => gdist V adj a b
  ((perms (List.range n)).map fun σ =>
    ((List.range n).zip σ).foldl (fun acc ij => acc + (M.getD ij.1 []).getD ij.2 0) 0).foldl
    min 1000000

/-- prism C_k × K_2: vertex i + k·l -/
def prismAdj (k : ℕ) (a b : ℕ) : Bool :=
  let i := a % k; let l := a / k; let j := b % k; let m := b / k
  decide (a < 2 * k ∧ b < 2 * k) &&
  ((decide (l = m) && (decide ((i + 1) % k = j) || decide ((j + 1) % k = i))) ||
   (decide (i = j) && decide (l ≠ m)))

/-- truncated cube: vertex 3c + d, c ∈ {0..7} (cube corner), d ∈ {0,1,2} (direction) -/
def tcAdj (a b : ℕ) : Bool :=
  let c := a / 3; let d := a % 3; let c' := b / 3; let d' := b % 3
  decide (a < 24 ∧ b < 24) &&
  ((decide (c = c') && decide (d ≠ d')) ||
   (decide (d = d') && decide (c' = Nat.xor c (2 ^ d))))

theorem prism7_degree : ((List.range 14).all fun v => ((List.range 14).filter (prismAdj 7 v)).length == 3) = true := by decide +kernel
theorem prism8_degree : ((List.range 16).all fun v => ((List.range 16).filter (prismAdj 8 v)).length == 3) = true := by decide +kernel
theorem tc_degree : ((List.range 24).all fun v => ((List.range 24).filter (tcAdj v)).length == 3) = true := by decide +kernel
theorem tc_symm : ((List.range 24).all fun a => (List.range 24).all fun b => tcAdj a b == tcAdj b a) = true := by decide +kernel

/-- C_7 × K_2: k-gon edge 0–1 costs 4 (κ = 0), vertical edge 0–7 costs 2 (κ = 1/2). -/
theorem prism7_costs : matchCost 14 (prismAdj 7) 0 1 = 4 ∧ matchCost 14 (prismAdj 7) 0 7 = 2 := by
  decide +kernel

/-- C_8 × K_2: k-gon edge costs 4 (κ = 0), vertical edge 2 (κ = 1/2). -/
theorem prism8_costs : matchCost 16 (prismAdj 8) 0 1 = 4 ∧ matchCost 16 (prismAdj 8) 0 8 = 2 := by
  decide +kernel

/-- truncated cube: triangle–octagon edge (0,0)–(0,1) costs 3 (κ = 1/4); octagon–octagon edge
(c=0,d=0)–(c=1,d=0) costs 6 (κ = −1/2). -/
theorem tc_costs : tcAdj 0 1 = true ∧ matchCost 24 tcAdj 0 1 = 3 ∧
    tcAdj 0 3 = true ∧ matchCost 24 tcAdj 0 3 = 6 := by
  decide +kernel

def kappaOf (cost D : ℕ) : ℚ := 1 - (cost : ℚ) / (D + 1)

/-- BLIND CLAIM (Example prisms/truncated cube): every certified edge sits at the capped value B,
and strictly above κ_F/(D+1) for the 7/8-gon and octagon edges. D = 3. -/
theorem certs_eq_capped :
    kappaOf 4 3 = (cappedNum 3 [4, 7] : ℚ) / 4 ∧ kappaOf 4 3 = (cappedNum 3 [4, 8] : ℚ) / 4 ∧
    kappaOf 2 3 = (cappedNum 3 [4, 4] : ℚ) / 4 ∧
    kappaOf 3 3 = (cappedNum 3 [3, 8] : ℚ) / 4 ∧ kappaOf 6 3 = (cappedNum 3 [8, 8] : ℚ) / 4 ∧
    (formanK 3 [4, 7] : ℚ) / 4 = -1/4 ∧ (formanK 3 [4, 8] : ℚ) / 4 = -1/2 ∧
    (formanK 3 [3, 8] : ℚ) / 4 = -1/4 ∧ (formanK 3 [8, 8] : ℚ) / 4 = -3/2 := by
  simp [kappaOf, cappedNum, formanK]; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.CappedForman1Blind
