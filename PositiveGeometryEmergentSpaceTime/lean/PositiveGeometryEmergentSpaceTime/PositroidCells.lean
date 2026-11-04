/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Network

/-!
# H-T2: electrical networks → positroid cells → canonical forms

Prereg: `prereg/H-T2-positroid-cells-2026-10-11.md`. Builds on H-T1's `PositiveGeometryEmergentSpaceTime.Network` (Lam's map, the Y network).

* **Cell identification (b).** The n = 3 facet network (terminal 1 joined to 2 and 3, conductances `b, c`) has Lam
  point `MF b c ∈ Gr(2,6)≥0`. Its zero pattern is `Δ₂₃ = Δ₅₆ = 0`, all others are positive. Its Grassmann necklace and
  bounded affine permutation `f = [4,3,5,7,6,8]` equal Lam's `f_τ` for `τ = (15)(24)(36)`. The same pipeline sends the Y
  network to the top cell `f = [3,…,8]`.
* **Dimension.** `dim Π_{f_τ} = n − 1 + 2 c(τ)` for all 15 matchings of `[6]` (decidable check). The electroid top cell
  is 3-dimensional = 3 edges: Y ↔ Δ (star–triangle) is a bijection `ℝ³_{>0} → ℝ³_{>0}`.
* **Canonical form (c).** The star–triangle map has log-Jacobian determinant `−1`:
  `dlog x₁₂ ∧ dlog x₁₃ ∧ dlog x₂₃ = −dlog a ∧ dlog b ∧ dlog c`. The dlog form of conductances is therefore independent
  of the critical network (up to orientation).
* **Fusions (d).** For the Y and facet networks, the terminal-column minors all equal `L₁₂₃`. Their cell in `Gr(2,3)` is
  the top cell, which equals *Fusions* Def. 2 applied to an irreducible 3-state chain.

All combinatorics is `decide` (kernel reduction), not `native_decide`.
-/

namespace PositiveGeometryEmergentSpaceTime.PositroidCells
open PositiveGeometryEmergentSpaceTime.Network

/-! ## Combinatorics: Grassmann necklaces and bounded affine permutations (k = 2, columns `0 … N-1`) -/

/-- All 2-subsets `(i, j)`, `i < j < N`. -/
def pairs (N : ℕ) : List (ℕ × ℕ) :=
  (List.range N).flatMap fun i => ((List.range N).filter (fun j => i < j)).map fun j => (i, j)

/-- Lexicographic key of a pair in the cyclic order starting at `a`. -/
def key (N a : ℕ) (p : ℕ × ℕ) : ℕ :=
  let u := (p.1 + N - a) % N; let v := (p.2 + N - a) % N; min u v * N + max u v

/-- The Grassmann necklace entry `I_a`: the `≤_a`-lex-minimal pair with nonzero Plücker coordinate. -/
def neck (N : ℕ) (nz : ℕ → ℕ → Bool) (a : ℕ) : Option (ℕ × ℕ) :=
  ((pairs N).filter (fun p => nz p.1 p.2)).foldl
    (fun best p => match best with
      | none => some p
      | some q => if key N a p < key N a q then some p else some q) none

/-- Boolean test that `x` is one of the two endpoints of the pair `p`. -/
def mem (p : ℕ × ℕ) (x : ℕ) : Bool := p.1 == x || p.2 == x

/-- Bounded affine permutation (1-based values, as in Lam and Knutson–Lam–Speyer) read off from the necklace:
`f(a) = a` for a loop, `a + N` for a coloop, otherwise the element entering `I_{a+1}`, lifted above `a`. -/
def fperm (N : ℕ) (nz : ℕ → ℕ → Bool) (a : ℕ) : ℕ :=
  match neck N nz a, neck N nz ((a + 1) % N) with
  | some I, some J =>
    if !(mem I a) then a + 1
    else
      let other := if I.1 == a then I.2 else I.1
      let j := if J.1 == other then J.2 else J.1
      if j == a then a + 1 + N else if j > a then j + 1 else j + 1 + N
  | _, _ => 0

/-- Lam's `f_τ(i) = g_τ(i) − 1`, `g_τ(i) = τ(i)` or `τ(i) + 2n` (τ given 1-based as a list). -/
def ftau (tau : List ℕ) (i : ℕ) : ℕ :=
  let N := tau.length; let t := tau.getD (i - 1) 0
  (if i < t then t else t + N) - 1

/-- Affine length `ℓ(f) = #{(i, j) : 1 ≤ i ≤ N, i < j, f(i) > f(j)}` (periodic extension; `j < i +
  N` suffices). -/
def flen (N : ℕ) (f : ℕ → ℕ) : ℕ :=
  let F : ℕ → ℕ := fun j => f ((j - 1) % N + 1) + N * ((j - 1) / N)
  ((List.range N).map fun i0 => ((List.range (N - 1)).filter fun d => F (i0 + 1 + d + 1) < F (i0 + 1))).map
    List.length |>.sum

/-- Number of crossing chord pairs of a matching (1-based list). -/
def crossings (tau : List ℕ) : ℕ :=
  let N := tau.length
  let ch := (List.range N).filterMap fun i => let t := tau.getD i 0; if i + 1 < t then some (i + 1,
      t) else none
  (ch.flatMap fun p => ch.filter fun q => p.1 < q.1 ∧ q.1 < p.2 ∧ p.2 < q.2).length

/-- The 15 matchings of `[6]`, as involutions. -/
def matchings6 : List (List ℕ) :=
  [[2,1,4,3,6,5], [2,1,5,6,3,4], [2,1,6,5,4,3], [3,4,1,2,6,5], [3,5,1,6,2,4], [3,6,1,5,4,2],
      [4,3,2,1,6,5],
   [4,5,6,1,2,3], [4,6,5,1,3,2], [5,3,2,6,1,4], [5,4,6,2,1,3], [5,6,4,3,1,2], [6,3,2,5,4,1], [6,4,5,2,3,1],
   [6,5,4,3,2,1]]

/-- **Dimension count, n = 3.** For every matching τ of `[6]`, `dim Π_{f_τ} = k(N−k) − ℓ(f_τ) = 8 − ℓ(f_τ)` equals
`n − 1 + 2 c(τ) = 2 + 2 c(τ)`. Equivalently (Lam, Thm 4.16) `ℓ(f_τ) = 2(3 − c(τ))`. -/
theorem dim_formula_n3 :
    matchings6.all (fun t => 8 - flen 6 (ftau t) == 2 + 2 * crossings t) = true := by decide

/-- Crossing numbers of the 15 matchings: `0:5, 1:6, 2:3, 3:1`, giving the stratum counts of `E₃` (1 top cell,
3 facets, 6 codim-2, 5 vertices). -/
theorem crossing_census_n3 :
    matchings6.map crossings = [0, 1, 0, 1, 2, 1, 0, 3, 2, 1, 2, 1, 0, 1, 0] := by decide

/-! ## The facet network: exact Plücker data -/

/-- Lam point of the facet network: terminal 1̄ joined to 2̄ (conductance `b`) and to 3̄ (conductance `c`); columns
`1̄, 1̃, 2̄, 2̃, 3̄, 3̃`. It is the `a → ∞` limit of `MY a b c` (the spoke at 1 contracted). -/
noncomputable def MF (b c : ℝ) : Matrix (Fin 2) (Fin 6) ℝ :=
  !![1, 0, 0, -1 / c, -1, -1 / c;
     0, c, b * c, b + c, b * c, b]

/-- The 15 Plücker coordinates are Lam's concordance sums of the groves `L₁₂₃ = bc`, `L₁|₂|₃ = 1`, `L₁₂|₃ = b`,
`L₁₃|₂ = c`, `L₂₃|₁ = 0`. -/
theorem F_pluecker (b c : ℝ) (hc : c ≠ 0) :
    mn (MF b c) 0 1 = c ∧ mn (MF b c) 0 2 = b*c ∧ mn (MF b c) 0 3 = b + c ∧ mn (MF b c) 0 4 = b*c ∧
    mn (MF b c) 0 5 = b ∧ mn (MF b c) 1 2 = 0 ∧ mn (MF b c) 1 3 = 1 ∧ mn (MF b c) 1 4 = c ∧
    mn (MF b c) 1 5 = 1 ∧ mn (MF b c) 2 3 = b ∧ mn (MF b c) 2 4 = b*c ∧ mn (MF b c) 2 5 = b ∧
    mn (MF b c) 3 4 = c ∧ mn (MF b c) 3 5 = 1 ∧ mn (MF b c) 4 5 = 0 := by
  simp only [mn, MF, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.cons_val]
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> field_simp <;> ring

/-- Zero pattern of the facet point (0-based columns). -/
def nzF (i j : ℕ) : Bool := !((i == 1 && j == 2) || (i == 4 && j == 5))

/-- **Totally nonnegative, with exactly the pattern `nzF`.** For `b, c > 0` every Plücker coordinate `Δ_{ij}` (i < j)
is `≥ 0`, and it is nonzero iff `nzF i j`. -/
theorem F_pattern (b c : ℝ) (hb : 0 < b) (hc : 0 < c) :
    (0 < mn (MF b c) 0 1 ∧ 0 < mn (MF b c) 0 2 ∧ 0 < mn (MF b c) 0 3 ∧ 0 < mn (MF b c) 0 4 ∧
     0 < mn (MF b c) 0 5 ∧ 0 < mn (MF b c) 1 3 ∧ 0 < mn (MF b c) 1 4 ∧ 0 < mn (MF b c) 1 5 ∧
     0 < mn (MF b c) 2 3 ∧ 0 < mn (MF b c) 2 4 ∧ 0 < mn (MF b c) 2 5 ∧ 0 < mn (MF b c) 3 4 ∧
     0 < mn (MF b c) 3 5) ∧ mn (MF b c) 1 2 = 0 ∧ mn (MF b c) 4 5 = 0 := by
  obtain ⟨h01, h02, h03, h04, h05, h12, h13, h14, h15, h23, h24, h25, h34, h35,
      h45⟩ := F_pluecker b c hc.ne'
  rw [h01, h02, h03, h04, h05, h13, h14, h15, h23, h24, h25, h34, h35]
  exact ⟨⟨hc, by positivity, by positivity, by positivity, hb, one_pos, hc, one_pos, hb,
      by positivity, hb, hc,
    one_pos⟩, h12, h45⟩

/-- **Cell identification (facet).** The necklace of the facet pattern is `(1,2),(2,4),(3,4),(4,5),(1,5),(1,6)`
(1-based), its bounded affine permutation is `[4,3,5,7,6,8]`, and this is Lam's `f_τ` for the medial pairing
`τ = (15)(24)(36)`, which has `c(τ) = 2` crossings = 2 edges. Its positroid cell has dimension `8 − ℓ = 6 = 2 + 2·2`. -/
theorem facet_cell :
    (List.range 6).map (neck 6 nzF) = [some (0,1), some (1,3), some (2,3), some (3,4), some (0,4),
        some (0,5)] ∧
    (List.range 6).map (fperm 6 nzF) = [4, 3, 5, 7, 6, 8] ∧
    (List.range 6).map (fun i => ftau [5,4,6,2,1,3] (i + 1)) = [4, 3, 5, 7, 6, 8] ∧
    crossings [5,4,6,2,1,3] = 2 ∧ 8 - flen 6 (fun i => fperm 6 nzF (i - 1)) = 6 := by decide

/-- **Cell identification (top).** All 15 coordinates nonzero (the Y network, `PositiveGeometryEmergentSpaceTime.Network.Y_pos`) give
`f = [3,4,5,6,7,8]`, which is Lam's `f_{τ_top}` with `τ_top(i) = i + 3`, 3 crossings = 3 edges, and dimension 8. -/
theorem top_cell :
    (List.range 6).map (fperm 6 (fun _ _ => true)) = [3, 4, 5, 6, 7, 8] ∧
    (List.range 6).map (fun i => ftau [4,5,6,1,2,3] (i + 1)) = [3, 4, 5, 6, 7, 8] ∧
    crossings [4,5,6,1,2,3] = 3 ∧ 8 - flen 6 (fun i => fperm 6 (fun _ _ => true) (i - 1)) = 8 := by decide

/-! ## Dimension = edges: star–triangle is a bijection of positive orthants -/

/-- Response (Δ-network) conductances of the Y network (H-T1 `star_response`): `x₁₂ = ab/S` etc. -/
noncomputable def yd (a b c : ℝ) : ℝ × ℝ × ℝ := (a*b/(a+b+c), a*c/(a+b+c), b*c/(a+b+c))

/-- Inverse map (Δ → Y): `a = P/x₂₃`, `b = P/x₁₃`, `c = P/x₁₂`, `P = x₁₂x₁₃ + x₁₂x₂₃ + x₁₃x₂₃`. -/
noncomputable def dy (x y z : ℝ) : ℝ × ℝ × ℝ :=
  let P := x*y + x*z + y*z; (P/z, P/y, P/x)

/-- For positive `a, b, c`, `dy ∘ yd` is the identity (Y → Δ → Y). -/
theorem dy_yd (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    dy (yd a b c).1 (yd a b c).2.1 (yd a b c).2.2 = (a, b, c) := by
  simp only [dy, yd, Prod.mk.injEq]
  have hS : 0 < a + b + c := by positivity
  refine ⟨?_, ?_, ?_⟩ <;> field_simp

/-- For positive `x, y, z`, `yd ∘ dy` is the identity (Δ → Y → Δ). -/
theorem yd_dy (x y z : ℝ) (hx : 0 < x) (hy : 0 < y) (hz : 0 < z) :
    yd (dy x y z).1 (dy x y z).2.1 (dy x y z).2.2 = (x, y, z) := by
  simp only [dy, yd, Prod.mk.injEq]
  have hP : 0 < x*y + x*z + y*z := by positivity
  refine ⟨?_, ?_, ?_⟩ <;> field_simp

/-- **Top electroid cell `≅ ℝ³_{>0}` in either chart.** `yd` maps the positive orthant to itself bijectively, so the
cell has dimension 3 = the number of edges of either critical network (Y or Δ). -/
theorem yd_bijOn : Set.BijOn (fun p : ℝ × ℝ × ℝ => yd p.1 p.2.1 p.2.2)
    {p | 0 < p.1 ∧ 0 < p.2.1 ∧ 0 < p.2.2} {p | 0 < p.1 ∧ 0 < p.2.1 ∧ 0 < p.2.2} := by
  refine ⟨?_, ?_, ?_⟩
  · rintro ⟨a, b, c⟩ ⟨ha, hb, hc⟩; simp only [yd, Set.mem_ofPred_eq]; exact ⟨by positivity,
      by positivity, by positivity⟩
  · rintro ⟨a, b, c⟩ ⟨ha, hb, hc⟩ ⟨a', b', c'⟩ ⟨ha', hb', hc'⟩ h
    have h1 := dy_yd a b c ha hb hc; have h2 := dy_yd a' b' c' ha' hb' hc'
    simp only at h; rw [h] at h1; rw [h1] at h2; exact h2
  · rintro ⟨x, y, z⟩ ⟨hx, hy, hz⟩
    have hP : 0 < x*y + x*z + y*z := by positivity
    refine ⟨dy x y z, ?_, yd_dy x y z hx hy hz⟩
    simp only [dy, Set.mem_ofPred_eq]; exact ⟨by positivity, by positivity, by positivity⟩

/-! ## Canonical form: the star–triangle map preserves the dlog form up to sign -/

/-- Derivative of `t ↦ t q/(t + r)` at `a` (with `a + r ≠ 0`) is `q r/(a + r)²`. -/
theorem hasDerivAt_lin_div (q r a : ℝ) (h : a + r ≠ 0) :
    HasDerivAt (fun t => t * q / (t + r)) (q * r / (a + r)^2) a := by
  have h1 : HasDerivAt (fun t => t * q) q a := by simpa using (hasDerivAt_id a).mul_const q
  have h2 : HasDerivAt (fun t => t + r) 1 a := by simpa using (hasDerivAt_id a).add_const r
  convert h1.div h2 h using 1; field_simp; ring

/-- Derivative of `t ↦ p/(t + r)` at `a` (with `a + r ≠ 0`) is `−p/(a + r)²`. -/
theorem hasDerivAt_const_div (p r a : ℝ) (h : a + r ≠ 0) :
    HasDerivAt (fun t => p / (t + r)) (-p / (a + r)^2) a := by
  have h2 : HasDerivAt (fun t => t + r) 1 a := by simpa using (hasDerivAt_id a).add_const r
  convert (hasDerivAt_const a p).div h2 h using 1; ring

/-- Logarithmic Jacobian `∂ log x_{ij} / ∂ log (a, b, c)` of the star–triangle map. Each entry is
`t · ∂x/∂t / x`, with derivatives from `hasDerivAt_lin_div` / `hasDerivAt_const_div`. -/
noncomputable def logJac (a b c : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  let S := a + b + c
  !![(b+c)/S, (a+c)/S, -c/S; (b+c)/S, -b/S, (a+b)/S; -a/S, (a+c)/S, (a+b)/S]

/-- The `(x₁₂, ∂/∂a)` entry, checked against the actual derivative: `a · ∂ₐ(ab/S) / (ab/S) =
  (b+c)/S`. -/
theorem logJac_entry00 (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    HasDerivAt (fun t => t * b / (t + (b + c))) (b * (b + c) / (a + (b + c))^2) a ∧
    a * (b * (b + c) / (a + (b + c))^2) / (a * b / (a + b + c)) = logJac a b c 0 0 := by
  refine ⟨hasDerivAt_lin_div b (b + c) a (by positivity), ?_⟩
  simp only [logJac, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.empty_val',
    Matrix.cons_val_fin_one]
  have hS : 0 < a + b + c := by positivity
  field_simp; ring

/-- The `(x₂₃, ∂/∂a)` entry: `a · ∂ₐ(bc/S) / (bc/S) = −a/S`. -/
theorem logJac_entry20 (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    HasDerivAt (fun t => b * c / (t + (b + c))) (-(b * c) / (a + (b + c))^2) a ∧
    a * (-(b * c) / (a + (b + c))^2) / (b * c / (a + b + c)) = logJac a b c 2 0 := by
  refine ⟨hasDerivAt_const_div (b * c) (b + c) a (by positivity), ?_⟩
  simp [logJac]
  have hS : 0 < a + b + c := by positivity
  field_simp; ring

/-- **Star–triangle preserves the dlog form (up to sign).** `det ∂log x / ∂log(a,b,c) = −1`, i.e.
`dlog x₁₂ ∧ dlog x₁₃ ∧ dlog x₂₃ = −dlog a ∧ dlog b ∧ dlog c`. (The other entries follow from the same two derivative
lemmas by the `a ↔ b ↔ c` symmetry; `logJac_entry00/20` check the two shapes.) -/
theorem star_triangle_dlog (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    (logJac a b c).det = -1 := by
  have hS : 0 < a + b + c := by positivity
  simp [logJac, Matrix.det_fin_three]
  field_simp; ring

/-- **n = 3 grove quadric** (Lam Prop. 5.35 at n = 3) on the Y chart: `L₁₂₃ · L₁|₂|₃ = e₂(L₁₂|₃, L₁₃|₂, L₂₃|₁)`. It cuts
out the 3-fold `Q ⊂ ℙ⁴` that carries `E₃`; the candidate canonical form is `Res_Q ⟨L d⁴L⟩ / (Q · L₁₂|₃ L₁₃|₂ L₂₃|₁)`. -/
theorem grove_quadric (a b c : ℝ) :
    (a*b*c) * (a+b+c) = (a*b)*(a*c) + (a*b)*(b*c) + (a*c)*(b*c) := by ring

/-! ## Fusions comparison (d) -/

/-- *Fusions* Def. 2 for a chain whose classes are given by labels `cls` (all classes recurrent, as for a reversible
chain): `σ(a) = a + max cyclic distance to a class-mate`, or `a + n` for a singleton (absorbing). 1-based output. -/
def fusions (n : ℕ) (cls : ℕ → ℕ) (a : ℕ) : ℕ :=
  let ds := ((List.range n).filter fun b => b != a && cls b == cls a).map fun b => (b + n - a) % n
  a + 1 + (if ds = [] then n else ds.foldl max 0)

/-- Terminal-column minors (`1̄, 2̄, 3̄` = columns 0, 2, 4) of the Y and facet points are all equal
  to `L₁₂₃`. -/
theorem terminal_minors (a b c : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    (mn (MY a b c) 0 2 = a*b*c ∧ mn (MY a b c) 0 4 = a*b*c ∧ mn (MY a b c) 2 4 = a*b*c) ∧
    (mn (MF b c) 0 2 = b*c ∧ mn (MF b c) 0 4 = b*c ∧ mn (MF b c) 2 4 = b*c) := by
  obtain ⟨-, h02, -, h04, -, -, -, -, -, -, -, -, -, -, -⟩ := F_pluecker b c hc
  obtain ⟨_, h02', h03', h04', _⟩ := Y_pluecker a b c ha hc
  refine ⟨⟨h02', h04', ?_⟩, ⟨h02, h04, ?_⟩⟩
  · simp only [mn, MY, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.cons_val]; field_simp; ring
  · simp only [mn, MF, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.cons_val]; ring

/-- **(d) at n = 3.** The terminal projection (all three minors equal and nonzero) sits in the top cell of `Gr(2,3)`,
`f = [3,4,5]`. That is exactly *Fusions*' σ for an irreducible 3-state chain (one class). But two different network
cells (top `[3,…,8]` and facet `[4,3,5,7,6,8]`) both map to this one Fusions label: Fusions forgets `τ`. -/
theorem fusions_matches_projection :
    (List.range 3).map (fperm 3 (fun _ _ => true)) = [3, 4, 5] ∧
    (List.range 3).map (fusions 3 (fun _ => 0)) = [3, 4, 5] ∧
    (List.range 6).map (fperm 6 (fun _ _ => true)) ≠ (List.range 6).map (fperm 6 nzF) := by decide

end PositiveGeometryEmergentSpaceTime.PositroidCells
