/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — HG-DIM-1 tie theorems for the NAME-ONLY definitions
`HgDim1.NA_neg`, `NB_neg`, `NA_pos`, `NB_pos` (D177). Not part of `import PositiveGeometryEmergentSpaceTime`.
-/
import PositiveGeometryEmergentSpaceTime.HgDim1

/-!
# HG-DIM-1 ties: hand-listed neighbourhoods = computed closed flip neighbourhoods

* Tie (D177): each of the four hand-listed lists is exactly the closed neighbourhood `{v} ∪ N(v)` of
  the edge endpoint in the flip graph `adj`, listed in index order.
* Completeness (known value): the 42 masks in `tris` are *all* the 4-diagonal noncrossing subsets of the
  14 diagonals of the 7-gon (Catalan C₅ = 42); 84 edges (f₁ of the 4-dim associahedron).
* Planted: swapping one vertex of a neighbourhood list, or an edge that is not a flip, is rejected.
* Non-vacuity: both edges are genuine flips with distinct endpoints.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.HgDim1Nbhd
open PositiveGeometryEmergentSpaceTime.HgDim1

/-- Closed neighbourhood of `v` in the flip graph, in index order. -/
def closedNbhd (v : V) : List V := (List.finRange 42).filter (fun w => w == v || adj v w)

theorem NA_neg_tie : NA_neg = closedNbhd 2 := by decide +kernel
theorem NB_neg_tie : NB_neg = closedNbhd 8 := by decide +kernel
theorem NA_pos_tie : NA_pos = closedNbhd 0 := by decide +kernel
theorem NB_pos_tie : NB_pos = closedNbhd 1 := by decide +kernel

/-- All 4-subsets `a<b<c<d` of the 14 diagonals that are pairwise noncrossing, as masks. -/
def allTriMasks : List Nat :=
  (List.range 14).flatMap fun a => (List.range 14).flatMap fun b => (List.range 14).flatMap fun c =>
    ((List.range 14).filter fun d =>
      decide (a < b) && decide (b < c) && decide (c < d) &&
      !crosses a b && !crosses a c && !crosses a d && !crosses b c && !crosses b d && !crosses c d).map
      fun d => 2 ^ a + 2 ^ b + 2 ^ c + 2 ^ d

/-- Known value: there are exactly 42 = C₅ triangulations of the 7-gon. -/
theorem allTriMasks_length : allTriMasks.length = 42 := by decide +kernel

/-- Completeness: every noncrossing 4-subset is one of the 42 listed masks (and conversely, by
`tris_valid`, `tris_distinct` and the count). -/
theorem tris_complete : allTriMasks.all (fun m => tris.contains m) = true := by decide +kernel

/-- Known value: 84 flip edges (4-regular on 42 vertices). -/
theorem edge_count :
    ((List.finRange 42).flatMap fun i => (List.finRange 42).filter fun j => decide (i < j) && adj i j).length
      = 84 := by decide +kernel

/-- Planted: replacing the last vertex `16` of `NA_neg` by the non-neighbour `17` is rejected. -/
theorem planted_nbhd : ([0, 2, 3, 8, 17] : List V) ≠ closedNbhd 2 ∧ adj 2 17 = false := by decide +kernel

/-- Planted: `(0, 3)` is not a flip edge, so it cannot serve as a curvature edge. -/
theorem planted_edge : adj 0 3 = false := by decide +kernel

/-- Non-vacuity: both certificate edges are flips with distinct endpoints, closed neighbourhoods of size 5. -/
theorem nonvacuous : adj 2 8 = true ∧ adj 0 1 = true ∧ (2 : V) ≠ 8 ∧ (closedNbhd 2).length = 5 ∧
    (closedNbhd 8).length = 5 := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.HgDim1Nbhd
