/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of HG-DIM-2 (permutohedra).
Written ONLY from the curvature paper v4 prose (§"Contrast: the permutohedron", Thm perm,
the HG-DIM-2 rung card and the Lean table row "HgDim2P4/P5/P6: coupling cost, inversion
potential, matching lower bound"), BEFORE opening the original HgDim2* modules or the blueprint.

Blind modelling choices:
 * vertices of Perm_n are one-line permutations (lists of 0..n-1); right multiplication by the
   adjacent transposition s_i swaps POSITIONS i, i+1;
 * graph distance is taken to be the Kendall-tau distance (number of value pairs whose relative
   order differs). That this equals the Cayley-graph distance is the classical inversion-count
   fact; it is CITED here, not proved (gap vs a BFS-distance formalisation);
 * Ollivier κ with idleness 1/(D+1): uniform measure on the closed ball (n points), so
   κ = 1 − W₁ and W₁ = cost / n where cost = min over BIJECTIONS of the two closed balls of the
   summed distance. Restricting to bijections (perfect matchings) is exact by Birkhoff; that step
   is CITED, not proved. So the theorems below certify the MATCHING cost, and κ via Birkhoff.
 * by vertex-transitivity (cited in the paper) it suffices to take w = id.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.HgDim2Blind

/-- swap positions k, k+1 (right multiplication by s_{k+1} in 1-based labels) -/
def swapAt : ℕ → List ℕ → List ℕ
  | 0, a :: b :: t => b :: a :: t
  | k + 1, a :: t => a :: swapAt k t
  | _, l => l

def idxOf (a : ℕ) : List ℕ → ℕ
  | [] => 0
  | x :: t => if x = a then 0 else idxOf a t + 1

/-- Kendall-tau distance between two one-line permutations of 0..n-1 -/
def kdist (n : ℕ) (x y : List ℕ) : ℕ :=
  ((List.range n).flatMap fun a => (List.range n).filterMap fun b =>
    if a < b ∧ (decide (idxOf a x < idxOf b x) ≠ decide (idxOf a y < idxOf b y)) then some ()
    else none).length

def idPerm (n : ℕ) : List ℕ := List.range n

/-- closed ball of w: w and w s_j for j = 0..n-2 -/
def ball (n : ℕ) (w : List ℕ) : List (List ℕ) := w :: (List.range (n - 1)).map (swapAt · w)

def insertAll (x : ℕ) : List ℕ → List (List ℕ)
  | [] => [[x]]
  | y :: ys => (x :: y :: ys) :: (insertAll x ys).map (y :: ·)

def perms : List ℕ → List (List ℕ)
  | [] => [[]]
  | x :: xs => (perms xs).flatMap (insertAll x)

def listMin (l : List ℕ) : ℕ := l.foldl min 1000000

/-- matching cost between the closed balls of u and v -/
def cost (n : ℕ) (u v : List ℕ) : ℕ :=
  let bu := ball n u
  let bv := ball n v
  let M := bu.map fun x => bv.map fun y => kdist n x y
  listMin ((perms (List.range n)).map fun σ =>
    ((List.range n).zip σ).foldl (fun acc ij => acc + (M.getD ij.1 []).getD ij.2 0) 0)

/-- label i (0-based position) edge cost at w = id -/
def labelCost (n i : ℕ) : ℕ := cost n (idPerm n) (swapAt i (idPerm n))

/-- per-label κ = 1 − cost/n -/
def kappa (n i : ℕ) : ℚ := 1 - (labelCost n i : ℚ) / n

/-! ### Perm_4 (S_4): end labels cost 4 (κ=0), interior label cost 6 (κ=−1/2) -/
theorem p4_costs : labelCost 4 0 = 4 ∧ labelCost 4 1 = 6 ∧ labelCost 4 2 = 4 := by decide

/-! ### Perm_5 -/
theorem p5_costs : labelCost 5 0 = 5 ∧ labelCost 5 1 = 7 ∧ labelCost 5 2 = 7 ∧
    labelCost 5 3 = 5 := by decide +kernel

/-! ### Perm_6 -/
theorem p6_costs : labelCost 6 0 = 6 ∧ labelCost 6 1 = 8 ∧ labelCost 6 2 = 8 ∧
    labelCost 6 3 = 8 ∧ labelCost 6 4 = 6 := by decide +kernel

theorem kappa_formula_6 :
    kappa 6 0 = (2 - 2 * 1) / 6 ∧ kappa 6 1 = (2 - 2 * 2) / 6 ∧ kappa 6 2 = (2 - 2 * 2) / 6 ∧
    kappa 6 3 = (2 - 2 * 2) / 6 ∧ kappa 6 4 = (2 - 2 * 1) / 6 := by
  obtain ⟨a, b, c, d, e⟩ := p6_costs
  simp only [kappa, a, b, c, d, e]; norm_num

/-- hexagon transport cost 3: d(s_j, s_i s_j) = 3 for |i−j| = 1 (n = 4, i = 1, j = 2). -/
theorem hexagon_cost3 :
    kdist 4 (swapAt 1 (idPerm 4)) (swapAt 1 (swapAt 0 (idPerm 4))) = 3 := by decide

/-- BLIND CLAIM (n = 4, 5): κ = (2 − 2h)/n per label, h = 1 at the ends, 2 inside. -/
theorem kappa_formula_45 :
    kappa 4 0 = (2 - 2 * 1) / 4 ∧ kappa 4 1 = (2 - 2 * 2) / 4 ∧ kappa 4 2 = (2 - 2 * 1) / 4 ∧
    kappa 5 0 = (2 - 2 * 1) / 5 ∧ kappa 5 1 = (2 - 2 * 2) / 5 ∧ kappa 5 2 = (2 - 2 * 2) / 5 ∧
    kappa 5 3 = (2 - 2 * 1) / 5 := by
  obtain ⟨a, b, c⟩ := p4_costs
  obtain ⟨d, e, f, g⟩ := p5_costs
  simp only [kappa, a, b, c, d, e, f, g]; norm_num

/-- Forman count: h hexagons and n−2−h squares give κ_F = 2 − 2h (paper eq.). -/
theorem forman_count (n h : ℤ) : n - (n - 2 - h) - 3 * h = 2 - 2 * h := by ring

/-- link: (2−2h)/n = κ_F/(D+1) with D+1 = n. -/
theorem link (n h : ℚ) : (2 - 2 * h) / n = (n - (n - 2 - h) - 3 * h) / n := by ring_nf

/-- BLIND CLAIM (mean): two end labels with κ = 0 and n−3 interior labels with κ = −2/n
average to −2(n−3)/(n(n−1)). -/
theorem mean_kappa (n : ℚ) (hn : 4 ≤ n) :
    (2 * 0 + (n - 3) * (-2 / n)) / (n - 1) = -2 * (n - 3) / (n * (n - 1)) := by
  have h1 : n ≠ 0 := by linarith
  have h2 : n - 1 ≠ 0 := by linarith
  field_simp
  ring

theorem mean_never_positive (n : ℚ) (hn : 4 ≤ n) : -2 * (n - 3) / (n * (n - 1)) < 0 := by
  apply div_neg_of_neg_of_pos <;> nlinarith

end PositiveGeometryEmergentSpaceTime.Alignment.HgDim2Blind
