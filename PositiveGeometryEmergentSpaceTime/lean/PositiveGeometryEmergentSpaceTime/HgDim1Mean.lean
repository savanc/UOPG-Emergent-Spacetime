import Mathlib.Combinatorics.Enumerative.Catalan.Basic
import Mathlib.Data.Nat.Choose.Central
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.IntervalCases
import PositiveGeometryEmergentSpaceTime.Associahedron

/-!
# HgDim1Mean — mean Ollivier curvature of the associahedron flip graph (HG-DIM-1 addendum, 2026-10-31)

Paper proof: notes/HG-DIM-1-mean-curvature-proof-2026-10-31.md. Notation: convex n-gon, triangulation T
(n − 3 diagonals), flip pair (T, d) with d ∈ T, p(T, d) = number of the 4 sides of the flip quadrilateral of d
that are diagonals, e(T) = number of ears. Per-edge formula κ = (2 − p)/(n − 2) (paper-proved, all n ≥ 4).

* General (all n): `catalan_succ_ratio`, `sumP_closed` (Σ p over pairs, written (2n − 12)C_{n−2} + 2nC_{n−3},
  times (2n − 5) equals 5(n − 4)(n − 3)C_{n−2}), `mean_kappa_closed` (the mean κ closed form (10 − n)/((n − 2)(2n − 5))
  follows from that sum), and the two counting steps of the per-triangulation identity (`tri_weight`, `ear_relation`).
* Instances (`decide +kernel`, n = 5..8 here, n = 9 in `PositiveGeometryEmergentSpaceTime.HgDim1Mean9`): over the enumerated triangulations `tris n` (complete: equal up to order
  to `PositiveGeometryEmergentSpaceTime.Assoc.triangulations n`, the definitional enumeration over all subsets, for n ≤ 7; for n = 8, 9 valid,
  duplicate-free and of Catalan size), the per-triangulation identity Σ_d p = 2n − 12 + 2e(T), Σ_T e(T) = n C_{n−3},
  and Σ_{(T,d)} p = (2n − 12)C_{n−2} + 2nC_{n−3}; hence `mean_kappa_instance`.
Not formalised: the per-triangulation identity and the ear count for general n (paper-proved), and the per-edge
curvature formula for general n (paper-proved; Lean certificates for two K_7 edges in `PositiveGeometryEmergentSpaceTime.HgDim1`).
-/

namespace PositiveGeometryEmergentSpaceTime.HgDim1Mean
open PositiveGeometryEmergentSpaceTime.Assoc (diags crosses noncrossing triangulations)

/-! ## General algebra (all n) -/

/-- Catalan ratio: (m + 2) C_{m+1} = 2(2m + 1) C_m. -/
theorem catalan_succ_ratio (m : ℕ) : (m + 2) * catalan (m + 1) = 2 * (2 * m + 1) * catalan m := by
  have h1 := succ_mul_catalan_eq_centralBinom (m + 1)
  have h2 := succ_mul_catalan_eq_centralBinom m
  have h3 := Nat.succ_mul_centralBinom_succ m
  refine Nat.eq_of_mul_eq_mul_left (n := m + 1) (by omega) ?_
  calc (m + 1) * ((m + 2) * catalan (m + 1)) = (m + 1) * (m + 1).centralBinom := by rw [← h1]
    _ = 2 * (2 * m + 1) * m.centralBinom := h3
    _ = (m + 1) * (2 * (2 * m + 1) * catalan m) := by rw [← h2]; ring

/-- Catalan numbers are positive. -/
theorem catalan_pos' (n : ℕ) : 0 < catalan n := by
  have h := succ_mul_catalan_eq_centralBinom n
  have hb := Nat.centralBinom_pos n
  rcases Nat.eq_zero_or_pos (catalan n) with h0 | h0
  · rw [h0, mul_zero] at h; omega
  · exact h0

/-- Σ_{(T,d)} p as (2n − 12) C_{n−2} + 2n C_{n−3}, with n = m + 4. -/
def sumP (m : ℕ) : ℤ := (2 * (m : ℤ) - 4) * catalan (m + 2) + 2 * ((m : ℤ) + 4) * catalan (m + 1)

/-- (2n − 5) Σ p = 5 (n − 4)(n − 3) C_{n−2}, n = m + 4, i.e. E[p] = 5(n − 4)/(2n − 5). -/
theorem sumP_closed (m : ℕ) : (2 * (m : ℤ) + 3) * sumP m = 5 * m * (m + 1) * catalan (m + 2) := by
  have h : ((m + 1 + 2 : ℕ) : ℤ) * catalan (m + 1 + 1) = 2 * (2 * ((m + 1 : ℕ) : ℤ) + 1) * catalan (m + 1) := by
    exact_mod_cast catalan_succ_ratio (m + 1)
  unfold sumP; push_cast at h ⊢; linear_combination (-((m : ℤ) + 4)) * h

/-- Mean curvature closed form: if κ = (2 − p)/(n − 2) per pair, the mean over the (n − 3) C_{n−2} pairs is
(10 − n)/((n − 2)(2n − 5)); n = m + 4. -/
theorem mean_kappa_closed (m : ℕ) :
    ((2 : ℚ) - (sumP m : ℚ) / (((m : ℚ) + 1) * catalan (m + 2))) / ((m : ℚ) + 2)
      = (6 - (m : ℚ)) / (((m : ℚ) + 2) * (2 * m + 3)) := by
  have hc : (0 : ℚ) < catalan (m + 2) := by exact_mod_cast catalan_pos' (m + 2)
  have hS : (2 * (m : ℚ) + 3) * sumP m = 5 * m * (m + 1) * catalan (m + 2) := by exact_mod_cast sumP_closed m
  have h1 : (0 : ℚ) < (m : ℚ) + 1 := by positivity
  have h2 : (0 : ℚ) < (m : ℚ) + 2 := by positivity
  have h3 : (0 : ℚ) < 2 * (m : ℚ) + 3 := by positivity
  rw [div_eq_div_iff (by positivity) (by positivity)]
  field_simp
  linear_combination (-1 : ℚ) * hS

/-- Per-triangle weight in the per-triangulation double count: a triangle with k ≤ 2 polygon sides contributes
(3 − k) k = 2·[k ≥ 1] polygon sides to the flip quadrilaterals of its diagonal sides. -/
theorem tri_weight (k : ℕ) (hk : k ≤ 2) : (3 - k) * k = 2 * (if 1 ≤ k then 1 else 0) := by
  interval_cases k <;> rfl

/-- Triangle-type relations: e ears, t₁ one-side and t₀ internal triangles in an n-gon triangulation satisfy
2e + t₁ = n and e + t₁ + t₀ = n − 2; then 2(e + t₁) = 2(n − e) and t₀ = e − 2. -/
theorem ear_relation (e t1 t0 n : ℤ) (h1 : 2 * e + t1 = n) (h2 : e + t1 + t0 = n - 2) :
    2 * (e + t1) = 2 * (n - e) ∧ t0 = e - 2 := by omega

/-! ## Instances by kernel computation -/

/-- Pruned enumeration of k pairwise noncrossing diagonals chosen in list order. -/
def gen : ℕ → List (ℕ × ℕ) → List (ℕ × ℕ) → List (List (ℕ × ℕ))
  | 0, acc, _ => [acc.reverse]
  | _ + 1, _, [] => []
  | k + 1, acc, d :: r =>
      (if acc.all (fun q => !crosses d q) then gen k (d :: acc) r else []) ++
      (if k + 1 ≤ r.length then gen (k + 1) acc r else [])

/-- Triangulations of the convex n-gon as lists of n − 3 noncrossing diagonals. -/
def tris (n : ℕ) : List (List (ℕ × ℕ)) := gen (n - 3) [] (diags n)

/-- Polygon side u < v of the n-gon. -/
def isSide (n u v : ℕ) : Bool := v == u + 1 || (u == 0 && v == n - 1)
/-- u, v joined by a polygon side or a diagonal of s. -/
def isEdge (n : ℕ) (s : List (ℕ × ℕ)) (u v : ℕ) : Bool :=
  isSide n (min u v) (max u v) || s.contains (min u v, max u v)
/-- Apexes of the two triangles on d = (a, c): inside the arc a..c and outside it. -/
def apexes (n : ℕ) (s : List (ℕ × ℕ)) (d : ℕ × ℕ) (inside : Bool) : List ℕ :=
  (List.range n).filter fun v => (decide (d.1 < v ∧ v < d.2) == inside) && v != d.1 && v != d.2 &&
    isEdge n s d.1 v && isEdge n s v d.2
/-- p(T, d): diagonal sides of the flip quadrilateral (both apexes unique; checked in `tris_valid`). -/
def pOf (n : ℕ) (s : List (ℕ × ℕ)) (d : ℕ × ℕ) : ℕ :=
  let x := (apexes n s d true).headD 0; let y := (apexes n s d false).headD 0
  ([(d.1, x), (x, d.2), (d.1, y), (y, d.2)].filter fun q => !isSide n (min q.1 q.2) (max q.1 q.2)).length
/-- e(T): number of ears (vertex v whose two neighbours are joined by a diagonal of s). -/
def ears (n : ℕ) (s : List (ℕ × ℕ)) : ℕ :=
  ((List.range n).filter fun v =>
    s.contains (min ((v + n - 1) % n) ((v + 1) % n), max ((v + n - 1) % n) ((v + 1) % n))).length
/-- Σ_{d ∈ T} p(T, d). -/
def sumPT (n : ℕ) (s : List (ℕ × ℕ)) : ℕ := (s.map (pOf n s)).sum
/-- Validity of an enumerated triangulation: n − 3 distinct diagonals, noncrossing, each with a unique apex on each side. -/
def validT (n : ℕ) (s : List (ℕ × ℕ)) : Bool :=
  s.length == n - 3 && noncrossing s && s.all (fun d => (diags n).contains d) && decide s.Nodup &&
    s.all (fun d => (apexes n s d true).length == 1 && (apexes n s d false).length == 1)
/-- All instance checks for one n: validity, the per-triangulation identity Σ_d p + 12 = 2n + 2e(T). -/
def checkAll (n : ℕ) : Bool := (tris n).all fun s => validT n s && sumPT n s + 12 == 2 * n + 2 * ears n s

theorem catalan_vals : catalan 1 = 1 ∧ catalan 2 = 2 ∧ catalan 3 = 5 ∧ catalan 4 = 14 ∧ catalan 5 = 42 ∧
    catalan 6 = 132 ∧ catalan 7 = 429 := by
  simp only [catalan_eq_centralBinom_div]; decide

/-- Completeness for n = 5, 6, 7: `tris n` is a permutation of the subset enumeration `Assoc.triangulations n`. -/
theorem tris_complete_5 : (tris 5).isPerm (triangulations 5) = true := by decide +kernel
theorem tris_complete_6 : (tris 6).isPerm (triangulations 6) = true := by decide +kernel
theorem tris_complete_7 : (tris 7).isPerm (triangulations 7) = true := by decide +kernel

theorem check_5 : checkAll 5 = true := by decide +kernel
theorem check_6 : checkAll 6 = true := by decide +kernel
theorem check_7 : checkAll 7 = true := by decide +kernel
theorem check_8 : checkAll 8 = true := by decide +kernel
/-- Numeric key of a diagonal list (used only to certify duplicate-freeness via `List.Nodup.of_map`). -/
def key (n : ℕ) (s : List (ℕ × ℕ)) : ℕ := (s.map fun d => 2 ^ (d.1 * n + d.2)).sum
theorem nodup_8 : (tris 8).Nodup := List.Nodup.of_map (key 8) (by decide +kernel)

/-- Sizes, ear sums Σ_T e(T) = n C_{n−3} and pair sums Σ_{(T,d)} p for n = 5..8 (n = 9 in `HgDim1Mean9`). -/
theorem counts_5 : (tris 5).length = 5 ∧ ((tris 5).map (ears 5)).sum = 5 * 2 ∧ ((tris 5).map (sumPT 5)).sum = 10 := by
  decide +kernel
theorem counts_6 : (tris 6).length = 14 ∧ ((tris 6).map (ears 6)).sum = 6 * 5 ∧ ((tris 6).map (sumPT 6)).sum = 60 := by
  decide +kernel
theorem counts_7 : (tris 7).length = 42 ∧ ((tris 7).map (ears 7)).sum = 7 * 14 ∧ ((tris 7).map (sumPT 7)).sum = 280 := by
  decide +kernel
theorem counts_8 : (tris 8).length = 132 ∧ ((tris 8).map (ears 8)).sum = 8 * 42 ∧
    ((tris 8).map (sumPT 8)).sum = 1200 := by
  decide +kernel

/-- The general expression at n = 5..9. -/
theorem sumP_instances : sumP 1 = 10 ∧ sumP 2 = 60 ∧ sumP 3 = 280 ∧ sumP 4 = 1200 ∧ sumP 5 = 4950 := by
  obtain ⟨-, c2, c3, c4, c5, c6, c7⟩ := catalan_vals
  simp only [sumP, c2, c3, c4, c5, c6, c7]; norm_num

/-- Enumerated Σ_{(T,d)} p equals (2n − 12)C_{n−2} + 2nC_{n−3} for n = 5..8. -/
theorem enum_eq_sumP :
    ((((tris 5).map (sumPT 5)).sum : ℕ) : ℤ) = sumP 1 ∧ ((((tris 6).map (sumPT 6)).sum : ℕ) : ℤ) = sumP 2 ∧
    ((((tris 7).map (sumPT 7)).sum : ℕ) : ℤ) = sumP 3 ∧ ((((tris 8).map (sumPT 8)).sum : ℕ) : ℤ) = sumP 4 := by
  obtain ⟨s1, s2, s3, s4, -⟩ := sumP_instances
  rw [counts_5.2.2, counts_6.2.2, counts_7.2.2, counts_8.2.2, s1, s2, s3, s4]; norm_num

/-- Mean κ on K_5..K_9 from the enumerated Σ p (via κ = (2 − p)/(n − 2) per pair): 1/3, 1/7, 1/15, 1/33, 1/91. -/
theorem mean_kappa_instance :
    ((2 : ℚ) - 10 / (2 * 5)) / 3 = 1 / 3 ∧ ((2 : ℚ) - 60 / (3 * 14)) / 4 = 1 / 7 ∧
    ((2 : ℚ) - 280 / (4 * 42)) / 5 = 1 / 15 ∧ ((2 : ℚ) - 1200 / (5 * 132)) / 6 = 1 / 33 ∧
    ((2 : ℚ) - 4950 / (6 * 429)) / 7 = 1 / 91 := by norm_num

/-- Witness (nonvacuity): the heptagon has a triangulation with an internal triangle, e(T) = 3 ≠ 2. -/
theorem witness_internal : ∃ s ∈ tris 7, ears 7 s = 3 := ⟨[(0, 2), (0, 4), (2, 4), (4, 6)], by decide +kernel, by decide +kernel⟩

end PositiveGeometryEmergentSpaceTime.HgDim1Mean
