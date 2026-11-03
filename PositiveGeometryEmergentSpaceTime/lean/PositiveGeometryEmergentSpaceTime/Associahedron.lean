/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
M2c / P-Pole: the n = 5 kinematic associahedron of Arkani-Hamed, Bai, He, Yan
(arXiv:1711.09102, eqs. 3.5, 3.10–3.14, 3.24, 4.3, 4.11, 5.13).

On the subspace H_5 (c13, c14, c24 constants) we use coordinates x = X13, y = X14.
The other planar variables are affine (ABHY eqs. 3.11–3.13, re-derived from eq. 3.5):
  X24 = y − x + c13,  X25 = c13 + c14 − x,  X35 = c14 + c24 − y.
Facets are indexed by `Fin 5` in counter-clockwise order (X14, X24, X25, X35, X13);
vertex `k` is where facets `k` and `k+1` meet.

PROVED here: pentagon combinatorics, canonical form (fan triangulation, independent formula)
= bi-adjoint amplitude m5, residues on every facet, a genuine limit for one facet, positivity
counterexamples, the soft limit, and Catalan counts by `decide`.
CITED (not proved): that pulling back the planar scattering form gives the canonical form
(ABHY §3.3), and the general-n associahedron theorem.
-/
import Mathlib

open Filter Topology

namespace PositiveGeometryEmergentSpaceTime.Assoc

/-! ## (a) The five planar variables and the pentagon -/

/-- Planar variables on H_5, facet order: 0 ↦ X14, 1 ↦ X24, 2 ↦ X25, 3 ↦ X35, 4 ↦ X13. -/
def X (c13 c14 c24 x y : ℝ) : Fin 5 → ℝ :=
  ![y, y - x + c13, c13 + c14 - x, c14 + c24 - y, x]

/-- The positive region `A_5 = H_5 ∩ {X ≥ 0}`. -/
def region (c13 c14 c24 x y : ℝ) : Prop := ∀ k, 0 ≤ X c13 c14 c24 x y k

/-- Vertex `k` = meeting point of facets `k` and `k+1`, i.e. the planar cubic diagram with
propagators {X_k, X_{k+1}}. -/
def vertex (c13 c14 c24 : ℝ) : Fin 5 → ℝ × ℝ :=
  ![(c13, 0), (c13 + c14, c14), (c13 + c14, c14 + c24), (0, c14 + c24), (0, 0)]

variable {c13 c14 c24 : ℝ}

/-- Unfolded form of `region`: `(x, y)` lies in the n = 5 region iff the five planar variables X14 =
  y, X24 = y − x + c13, X25 = c13 + c14 − x, X35 = c14 + c24 − y, X13 = x are all ≥ 0. -/
theorem region_iff (x y : ℝ) : region c13 c14 c24 x y ↔
    0 ≤ y ∧ 0 ≤ y - x + c13 ∧ 0 ≤ c13 + c14 - x ∧ 0 ≤ c14 + c24 - y ∧ 0 ≤ x := by
  simp [region, X, Fin.forall_fin_succ]

/-- Each vertex lies in the region, has exactly its two (compatible) X's zero, and all the
other three strictly positive. -/
theorem vertex_spec (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) (k : Fin 5) :
    region c13 c14 c24 (vertex c13 c14 c24 k).1 (vertex c13 c14 c24 k).2 ∧
    X c13 c14 c24 (vertex c13 c14 c24 k).1 (vertex c13 c14 c24 k).2 k = 0 ∧
    X c13 c14 c24 (vertex c13 c14 c24 k).1 (vertex c13 c14 c24 k).2 (k + 1) = 0 ∧
    ∀ j, j ≠ k → j ≠ k + 1 → 0 < X c13 c14 c24 (vertex c13 c14 c24 k).1 (vertex c13 c14 c24 k).2 j := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [region_iff]; fin_cases k <;> refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp [vertex] <;> linarith
  · fin_cases k <;> simp [vertex, X]
  · fin_cases k <;> simp [vertex, X]
  · intro j hj hj'
    fin_cases k <;> fin_cases j <;> simp_all [vertex, X] <;> linarith

/-- Vertex 0 (facets X14 and X24 meet) is `(c13, 0)`. -/
@[simp] theorem vertex_0 : vertex c13 c14 c24 0 = (c13, 0) := rfl
/-- Vertex 1 (facets X24 and X25 meet) is `(c13 + c14, c14)`. -/
@[simp] theorem vertex_1 : vertex c13 c14 c24 1 = (c13 + c14, c14) := rfl
/-- Vertex 2 (facets X25 and X35 meet) is `(c13 + c14, c14 + c24)`. -/
@[simp] theorem vertex_2 : vertex c13 c14 c24 2 = (c13 + c14, c14 + c24) := rfl
/-- Vertex 3 (facets X35 and X13 meet) is `(0, c14 + c24)`. -/
@[simp] theorem vertex_3 : vertex c13 c14 c24 3 = (0, c14 + c24) := rfl
/-- Vertex 4 (facets X13 and X14 meet) is `(0, 0)`. -/
@[simp] theorem vertex_4 : vertex c13 c14 c24 4 = (0, 0) := rfl

/-- The five vertices are distinct. -/
theorem vertex_injective (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) :
    Function.Injective (vertex c13 c14 c24) := by
  intro k l h
  fin_cases k <;> fin_cases l <;> first
    | rfl
    | (exfalso; simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, vertex_0, vertex_1, vertex_2,
        vertex_3, vertex_4, Prod.mk.injEq] at h; obtain ⟨a, b⟩ := h; linarith)

/-- **Vertices = compatible pairs.** If two distinct facets vanish at a point of the region,
they are cyclically adjacent (non-crossing chords) and the point is their vertex. In particular
the five crossing pairs (X13,X24), (X13,X25), (X14,X25), (X14,X35), (X24,X35) never vanish
together, and the region has exactly five vertices. -/
theorem two_zero (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) {x y : ℝ}
    (hr : region c13 c14 c24 x y) {i j : Fin 5} (hij : i ≠ j)
    (hi : X c13 c14 c24 x y i = 0) (hj : X c13 c14 c24 x y j = 0) :
    ∃ k, ({i, j} : Finset (Fin 5)) = {k, k + 1} ∧ (x, y) = vertex c13 c14 c24 k := by
  rw [region_iff] at hr
  obtain ⟨r0, r1, r2, r3, r4⟩ := hr
  fin_cases i <;> fin_cases j <;> simp [X] at hi hj hij <;>
    first
    | (exfalso; linarith)
    | (refine ⟨0, by decide, ?_⟩; simp only [vertex, Prod.ext_iff]; simp; constructor <;> linarith)
    | (refine ⟨1, by decide, ?_⟩; simp only [vertex, Prod.ext_iff]; simp; constructor <;> linarith)
    | (refine ⟨2, by decide, ?_⟩; simp only [vertex, Prod.ext_iff]; simp; constructor <;> linarith)
    | (refine ⟨3, by decide, ?_⟩; simp only [vertex, Prod.ext_iff]; simp; constructor <;> linarith)
    | (refine ⟨4, by decide, ?_⟩; simp only [vertex, Prod.ext_iff]; simp; constructor <;> linarith)

set_option linter.unusedVariables false in
set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- **Edges.** On each facet `X_F = 0` the region is the closed segment between the two
vertices of that facet: only the two neighbouring inequalities survive, and they cut out an
interval of positive length. -/
@[nolint unusedArguments]
theorem facet_X13 (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) {x y : ℝ} (hk : x = 0) :
    region c13 c14 c24 x y ↔ 0 ≤ y ∧ y ≤ c14 + c24 := by
  rw [region_iff]; constructor
  · rintro ⟨h0, -, -, h3, -⟩; exact ⟨h0, by linarith⟩
  · rintro ⟨a, b⟩; subst hk; exact ⟨a, by linarith, by linarith, by linarith, le_rfl⟩

set_option linter.unusedVariables false in
set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- For positive constants, the facet X14 = 0 (y = 0) of the region is the segment `0 ≤ x ≤ c13`. -/
@[nolint unusedArguments]
theorem facet_X14 (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) {x y : ℝ} (hk : y = 0) :
    region c13 c14 c24 x y ↔ 0 ≤ x ∧ x ≤ c13 := by
  rw [region_iff]; constructor
  · rintro ⟨-, h1, -, -, h4⟩; exact ⟨h4, by linarith⟩
  · rintro ⟨a, b⟩; subst hk; exact ⟨le_rfl, by linarith, by linarith, by linarith, a⟩

set_option linter.unusedVariables false in
set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- For positive constants, on the facet X24 = 0 the region is cut out by `X14 ≥ 0` and `X25 ≥ 0`
  (its two neighbouring facets). -/
@[nolint unusedArguments]
theorem facet_X24 (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) {x y : ℝ}
    (hk : y - x + c13 = 0) :
    region c13 c14 c24 x y ↔ 0 ≤ y ∧ 0 ≤ c13 + c14 - x := by
  rw [region_iff]; constructor
  · rintro ⟨h0, -, h2, -, -⟩; exact ⟨h0, h2⟩
  · rintro ⟨a, b⟩; exact ⟨a, by linarith, b, by linarith, by linarith⟩

set_option linter.unusedVariables false in
set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- For positive constants, on the facet X25 = 0 the region is cut out by `X24 ≥ 0` and `X35 ≥ 0`
  (its two neighbouring facets). -/
@[nolint unusedArguments]
theorem facet_X25 (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) {x y : ℝ}
    (hk : c13 + c14 - x = 0) :
    region c13 c14 c24 x y ↔ 0 ≤ y - x + c13 ∧ 0 ≤ c14 + c24 - y := by
  rw [region_iff]; constructor
  · rintro ⟨-, h1, -, h3, -⟩; exact ⟨h1, h3⟩
  · rintro ⟨a, b⟩; exact ⟨by linarith, a, by linarith, b, by linarith⟩

set_option linter.unusedVariables false in
set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- For positive constants, on the facet X35 = 0 the region is cut out by `X25 ≥ 0` and `X13 ≥ 0`
  (its two neighbouring facets). -/
@[nolint unusedArguments]
theorem facet_X35 (h13 : 0 < c13) (h14 : 0 < c14) (h24 : 0 < c24) {x y : ℝ}
    (hk : c14 + c24 - y = 0) :
    region c13 c14 c24 x y ↔ 0 ≤ c13 + c14 - x ∧ 0 ≤ x := by
  rw [region_iff]; constructor
  · rintro ⟨-, -, h2, -, h4⟩; exact ⟨h2, h4⟩
  · rintro ⟨a, b⟩; exact ⟨by linarith, by linarith, a, by linarith, b⟩

/-! ## (b) Amplitude and canonical form -/

/-- Tree-level bi-adjoint φ³ amplitude m(I5|I5) (ABHY eq. 3.24), one term per vertex. -/
noncomputable def m5 (c13 c14 c24 x y : ℝ) : ℝ :=
  let X14 := y; let X24 := y - x + c13; let X25 := c13 + c14 - x
  let X35 := c14 + c24 - y; let X13 := x
  1 / (X13 * X14) + 1 / (X14 * X24) + 1 / (X24 * X25) + 1 / (X25 * X35) + 1 / (X35 * X13)

/-- Affine bracket `⟨Y Z1 Z2⟩ = det[[1,x,y],[1,a1,b1],[1,a2,b2]]`.

Also known as: Assoc.br, ⟨Y Z₁ Z₂⟩ affine bracket.
-/
def affineBracket (x y : ℝ) (Z1 Z2 : ℝ × ℝ) : ℝ :=
  (Z1.1 * Z2.2 - Z2.1 * Z1.2) - x * (Z2.2 - Z1.2) + y * (Z2.1 - Z1.1)

/-- Canonical rational function of the triangle `Z1 Z2 Z3` (counter-clockwise):
`⟨Z1Z2Z3⟩² / (⟨Y Z1 Z2⟩⟨Y Z2 Z3⟩⟨Y Z3 Z1⟩)` (projective simplex formula, ABHY App. A). -/
noncomputable def tri (x y : ℝ) (Z1 Z2 Z3 : ℝ × ℝ) : ℝ :=
  affineBracket Z1.1 Z1.2 Z2 Z3 ^ 2 / (affineBracket x y Z1 Z2 * affineBracket x y Z2 Z3 * affineBracket x y Z3 Z1)

/-- Canonical form of the pentagon by the fan triangulation from the origin vertex. This
definition uses only the vertices, not the Feynman-diagram sum. -/
noncomputable def omegaFan (c13 c14 c24 x y : ℝ) : ℝ :=
  tri x y (vertex c13 c14 c24 4) (vertex c13 c14 c24 0) (vertex c13 c14 c24 1) +
  tri x y (vertex c13 c14 c24 4) (vertex c13 c14 c24 1) (vertex c13 c14 c24 2) +
  tri x y (vertex c13 c14 c24 4) (vertex c13 c14 c24 2) (vertex c13 c14 c24 3)

/-- **Canonical form = amplitude.** Away from the five facets and the two spurious diagonals of
the fan, the triangulated canonical form equals m5. The spurious poles cancel. -/
theorem omegaFan_eq_m5 (h13 : c13 ≠ 0) (h14 : c14 ≠ 0) (h24 : c24 ≠ 0) (h1314 : c13 + c14 ≠ 0)
    (h1424 : c14 + c24 ≠ 0) {x y : ℝ}
    (hx : x ≠ 0) (hy : y ≠ 0) (hX24 : y - x + c13 ≠ 0) (hX25 : c13 + c14 - x ≠ 0)
    (hX35 : c14 + c24 - y ≠ 0)
    (hd1 : -(x * c14) + y * (c13 + c14) ≠ 0) (hd2 : -(x * (c14 + c24)) + y * (c13 + c14) ≠ 0) :
    omegaFan c13 c14 c24 x y = m5 c13 c14 c24 x y := by
  simp only [omegaFan, tri, affineBracket, m5, vertex_0, vertex_1, vertex_2, vertex_3, vertex_4]
  have b1 : (0:ℝ) * 0 - c13 * 0 - x * (0 - 0) + y * (c13 - 0) = c13 * y := by ring
  have b2 : c13 * c14 - (c13 + c14) * 0 - x * (c14 - 0) + y * (c13 + c14 - c13)
      = c14 * (y - x + c13) := by ring
  have b3 : (c13 + c14) * (c14 + c24) - (c13 + c14) * c14 - x * (c14 + c24 - c14)
      + y * (c13 + c14 - (c13 + c14)) = c24 * (c13 + c14 - x) := by ring
  have b4 : (c13 + c14) * (c14 + c24) - 0 * (c14 + c24) - x * (c14 + c24 - (c14 + c24))
      + y * (0 - (c13 + c14)) = (c13 + c14) * (c14 + c24 - y) := by ring
  have b5 : (0:ℝ) * 0 - 0 * (c14 + c24) - x * (0 - (c14 + c24)) + y * (0 - 0)
      = (c14 + c24) * x := by ring
  have d1 : (c13 + c14) * 0 - 0 * c14 - x * (0 - c14) + y * (0 - (c13 + c14))
      = -(-(x * c14) + y * (c13 + c14)) := by ring
  have d1' : (0:ℝ) * c14 - (c13 + c14) * 0 - x * (c14 - 0) + y * (c13 + c14 - 0)
      = -(x * c14) + y * (c13 + c14) := by ring
  have d2 : (c13 + c14) * 0 - 0 * (c14 + c24) - x * (0 - (c14 + c24)) + y * (0 - (c13 + c14))
      = -(-(x * (c14 + c24)) + y * (c13 + c14)) := by ring
  have d2' : (0:ℝ) * (c14 + c24) - (c13 + c14) * 0 - x * (c14 + c24 - 0) + y * (c13 + c14 - 0)
      = -(x * (c14 + c24)) + y * (c13 + c14) := by ring
  rw [b1, b2, b3, b4, b5, d1, d1', d2, d2']
  have e1 : -(c14 * x) + (c13 + c14) * y ≠ 0 := by
    intro h; apply hd1; linarith
  have e2 : -(x * (c14 + c24)) + (c13 + c14) * y ≠ 0 := by
    intro h; apply hd2; linarith
  field_simp
  ring

/-! ### Residues (factorisation). Multiplied-out identities, all five facets. -/

/-- Residue structure on the facet X13 = x: `x · m5` equals the two-term residue `1/X14 + 1/X35`
  plus `x` times the terms regular at `x = 0` (exact identity for `x ≠ 0`). -/
theorem res_X13 (x y : ℝ) (hx : x ≠ 0) :
    x * m5 c13 c14 c24 x y = (1 / y + 1 / (c14 + c24 - y)) +
      x * (1 / (y * (y - x + c13)) + 1 / ((y - x + c13) * (c13 + c14 - x))
        + 1 / ((c13 + c14 - x) * (c14 + c24 - y))) := by
  simp only [m5]
  have a : x * (1 / (x * y)) = 1 / y := by
    rw [mul_one_div, div_mul_eq_div_div, div_self hx]
  have b : x * (1 / ((c14 + c24 - y) * x)) = 1 / (c14 + c24 - y) := by
    rw [mul_one_div, mul_comm (c14 + c24 - y), div_mul_eq_div_div, div_self hx]
  rw [mul_add, mul_add, mul_add, mul_add, a, b]; ring

/-- The other four facets, as coefficient identities: `X_F · m5 = (1/X_prev + 1/X_next) +
  X_F·(regular)`. -/
theorem res_X14 (x y : ℝ) (hy : y ≠ 0) :
    y * m5 c13 c14 c24 x y = (1 / x + 1 / (y - x + c13)) +
      y * (1 / ((y - x + c13) * (c13 + c14 - x)) + 1 / ((c13 + c14 - x) * (c14 + c24 - y))
        + 1 / ((c14 + c24 - y) * x)) := by
  simp only [m5]
  have a : y * (1 / (x * y)) = 1 / x := by
    rw [mul_one_div, mul_comm x, div_mul_eq_div_div, div_self hy]
  have b : y * (1 / (y * (y - x + c13))) = 1 / (y - x + c13) := by
    rw [mul_one_div, div_mul_eq_div_div, div_self hy]
  rw [mul_add, mul_add, mul_add, mul_add, a, b]; ring

/-- Residue structure on the facet X24: `X24 · m5` equals `1/X14 + 1/X25` plus `X24` times the terms
  regular at X24 = 0 (exact identity for X24 ≠ 0). -/
theorem res_X24 (x y : ℝ) (h : y - x + c13 ≠ 0) :
    (y - x + c13) * m5 c13 c14 c24 x y = (1 / y + 1 / (c13 + c14 - x)) +
      (y - x + c13) * (1 / (x * y) + 1 / ((c13 + c14 - x) * (c14 + c24 - y))
        + 1 / ((c14 + c24 - y) * x)) := by
  simp only [m5]
  have a : (y - x + c13) * (1 / (y * (y - x + c13))) = 1 / y := by
    rw [mul_one_div, mul_comm y, div_mul_eq_div_div, div_self h]
  have b : (y - x + c13) * (1 / ((y - x + c13) * (c13 + c14 - x))) = 1 / (c13 + c14 - x) := by
    rw [mul_one_div, div_mul_eq_div_div, div_self h]
  rw [mul_add, mul_add, mul_add, mul_add, a, b]; ring

/-- Residue structure on the facet X25: `X25 · m5` equals `1/X24 + 1/X35` plus `X25` times the terms
  regular at X25 = 0 (exact identity for X25 ≠ 0). -/
theorem res_X25 (x y : ℝ) (h : c13 + c14 - x ≠ 0) :
    (c13 + c14 - x) * m5 c13 c14 c24 x y = (1 / (y - x + c13) + 1 / (c14 + c24 - y)) +
      (c13 + c14 - x) * (1 / (x * y) + 1 / (y * (y - x + c13)) + 1 / ((c14 + c24 - y) * x)) := by
  simp only [m5]
  have a : (c13 + c14 - x) * (1 / ((y - x + c13) * (c13 + c14 - x))) = 1 / (y - x + c13) := by
    rw [mul_one_div, mul_comm (y - x + c13), div_mul_eq_div_div, div_self h]
  have b : (c13 + c14 - x) * (1 / ((c13 + c14 - x) * (c14 + c24 - y))) = 1 / (c14 + c24 - y) := by
    rw [mul_one_div, div_mul_eq_div_div, div_self h]
  rw [mul_add, mul_add, mul_add, mul_add, a, b]; ring

/-- Residue structure on the facet X35: `X35 · m5` equals `1/X25 + 1/X13` plus `X35` times the terms
  regular at X35 = 0 (exact identity for X35 ≠ 0). -/
theorem res_X35 (x y : ℝ) (h : c14 + c24 - y ≠ 0) :
    (c14 + c24 - y) * m5 c13 c14 c24 x y = (1 / (c13 + c14 - x) + 1 / x) +
      (c14 + c24 - y) * (1 / (x * y) + 1 / (y * (y - x + c13))
        + 1 / ((y - x + c13) * (c13 + c14 - x))) := by
  simp only [m5]
  have a : (c14 + c24 - y) * (1 / ((c13 + c14 - x) * (c14 + c24 - y))) = 1 / (c13 + c14 - x) := by
    rw [mul_one_div, mul_comm (c13 + c14 - x), div_mul_eq_div_div, div_self h]
  have b : (c14 + c24 - y) * (1 / ((c14 + c24 - y) * x)) = 1 / x := by
    rw [mul_one_div, div_mul_eq_div_div, div_self h]
  rw [mul_add, mul_add, mul_add, mul_add, a, b]; ring

/-- **Residue as a limit** on the facet X13 = 0: `X13 · m5 → 1/X14 + 1/X35`, the 4-point
amplitude `1/s + 1/t` of the facet segment (ABHY eqs. 3.22, 4.3). -/
theorem tendsto_res_X13 (y : ℝ) (hc : y + c13 ≠ 0) (hc' : c13 + c14 ≠ 0) :
    Tendsto (fun x => x * m5 c13 c14 c24 x y) (𝓝[≠] 0)
      (𝓝 (1 / y + 1 / (c14 + c24 - y))) := by
  set g : ℝ → ℝ := fun x => (1 / y + 1 / (c14 + c24 - y)) +
      x * (1 / (y * (y - x + c13)) + 1 / ((y - x + c13) * (c13 + c14 - x))
        + 1 / ((c13 + c14 - x) * (c14 + c24 - y))) with hg
  have hcont : ContinuousAt g 0 := by
    have d1 : ContinuousAt (fun x : ℝ => 1 / (y * (y - x + c13))) 0 := by
      by_cases hy : y = 0
      · simp [hy]; exact continuousAt_const
      · exact continuousAt_const.div (by fun_prop) (by simpa using mul_ne_zero hy (by simpa using hc))
    have d2 : ContinuousAt (fun x : ℝ => 1 / ((y - x + c13) * (c13 + c14 - x))) 0 :=
      continuousAt_const.div (by fun_prop) (by simpa using mul_ne_zero (by simpa using hc) hc')
    have d3 : ContinuousAt (fun x : ℝ => 1 / ((c13 + c14 - x) * (c14 + c24 - y))) 0 := by
      by_cases hz : c14 + c24 - y = 0
      · simp [hz]; exact continuousAt_const
      · exact continuousAt_const.div (by fun_prop) (by simpa using mul_ne_zero hc' hz)
    exact continuousAt_const.add (continuousAt_id.mul ((d1.add d2).add d3))
  have h0 : g 0 = 1 / y + 1 / (c14 + c24 - y) := by simp [hg]
  rw [← h0]
  refine (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with x hx
  exact (res_X13 x y hx).symm

/-! ## (c) Positivity doing work -/

/-- If `c14 + c24 < 0` the region is empty (X14 ≥ 0 and X35 ≥ 0 cannot both hold). -/
theorem empty_of_c14c24_neg (h : c14 + c24 < 0) (x y : ℝ) : ¬ region c13 c14 c24 x y := by
  rw [region_iff]; rintro ⟨h0, -, -, h3, -⟩; linarith

/-- If `c13 + c14 < 0` the region is empty (X13 ≥ 0 and X25 ≥ 0 cannot both hold). -/
theorem empty_of_c13c14_neg (h : c13 + c14 < 0) (x y : ℝ) : ¬ region c13 c14 c24 x y := by
  rw [region_iff]; rintro ⟨-, -, h2, -, h4⟩; linarith

/-- All constants zero: the "pentagon" collapses to one point. -/
theorem region_zero (x y : ℝ) : region 0 0 0 x y ↔ x = 0 ∧ y = 0 := by
  rw [region_iff]; constructor
  · rintro ⟨h0, h1, h2, h3, h4⟩; constructor <;> linarith
  · rintro ⟨rfl, rfl⟩; norm_num

/-- `c13 < 0`: X14 is strictly positive on the region, so the facet X14 = 0 (and with it the
pole 1/X14 of m5) is not a boundary. The polytope is no longer a pentagon (see script: it is a
quadrilateral whose canonical form differs from m5). -/
theorem X14_pos_of_c13_neg (h : c13 < 0) {x y : ℝ} (hr : region c13 c14 c24 x y) : 0 < y := by
  rw [region_iff] at hr; obtain ⟨-, h1, -, -, h4⟩ := hr; linarith

/-- Soft limit (ABHY eq. 4.11 and text below it): with `c13 = c14 = 0`, m5 vanishes on H. -/
theorem soft_limit {x y : ℝ} (hx : x ≠ 0) (hy : y ≠ 0) (hxy : y - x ≠ 0) (h35 : c24 - y ≠ 0) :
    m5 0 0 c24 x y = 0 := by
  simp only [m5]
  have : (0:ℝ) + 0 - x = -x := by ring
  rw [this]
  simp only [add_zero, zero_add]
  field_simp
  ring

/-! ## (d) Catalan counts by `decide` (triangulations ↔ vertices of A_n, CITED correspondence) -/

/-- Diagonals of a convex n-gon with vertices 0..n-1. -/
def diags (n : ℕ) : List (ℕ × ℕ) :=
  (List.range n).flatMap fun i => (List.range n).filterMap fun j =>
    if i + 1 < j ∧ ¬ (i = 0 ∧ j = n - 1) then some (i, j) else none

/-- Two diagonals `p = (i, j)` and `q` of the polygon cross iff their endpoints strictly interleave. -/
def crosses (p q : ℕ × ℕ) : Bool :=
  (p.1 < q.1 && q.1 < p.2 && p.2 < q.2) || (q.1 < p.1 && p.1 < q.2 && q.2 < p.2)

/-- Boolean test that no two diagonals in the list cross (`crosses` is false for every pair). -/
def noncrossing (s : List (ℕ × ℕ)) : Bool :=
  s.all fun p => s.all fun q => !crosses p q

/-- Sets of `n-3` pairwise non-crossing diagonals (= triangulations = vertices of A_n). -/
def triangulations (n : ℕ) : List (List (ℕ × ℕ)) :=
  (diags n).sublists.filter fun s => s.length == n - 3 && noncrossing s

/-- A convex pentagon has 5 diagonals (checked by `decide`). -/
theorem diags_five : (diags 5).length = 5 := by decide
/-- A convex hexagon has 9 diagonals (checked by `decide`). -/
theorem diags_six : (diags 6).length = 9 := by decide
/-- The pentagon has 5 triangulations, the Catalan number C₃ (checked by `decide`). -/
theorem catalan_five : (triangulations 5).length = 5 := by decide
/-- The hexagon has 14 triangulations, the Catalan number C₄ (checked by `decide`). -/
theorem catalan_six : (triangulations 6).length = 14 := by decide

end PositiveGeometryEmergentSpaceTime.Assoc
