/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — SURF-1′ tie theorems for the NAME-ONLY definitions
`Surf1.boxU` (D174) and `Surf1.ttU` (D175). Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.Surf1.Box.Graph
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Data.Fintype.Sum

/-!
# SURF-1′ ties: `boxU ≅ K₃,₃`, `ttU` = double square

The half-edge data of `boxU` / `ttU` is read back into a vertex graph (`vEdges`: the vertex pair of
each edge). We prove
* `boxU`: 6 vertices, 9 edges, no loops, no multi-edges, and under the bipartition
  `{v0,v3,v5} | {v1,v2,v4}` (explicit relabelling `relab`) the edge set is exactly the 9 cross pairs of
  `K₃,₃`; as a Mathlib statement, the vertex adjacency is isomorphic to `completeBipartiteGraph`;
* planted: the triangular prism (6 vertices, 9 edges, cubic) is rejected (it has a triangle; `boxU` does not);
* `ttU`: the vertex multigraph is `v0v1, v2v3, v0v2², v1v3²` (the double square), with exactly two
  doubled pairs; planted: a simple 4-cycle and `K₄` are rejected.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Surf1Ties
open PositiveGeometryEmergentSpaceTime.Surf1

/-- Vertex index of half-edge `h` (position of the list containing it; `V.length` if absent). -/
def vOf (g : G) (h : Nat) : Nat := g.V.findIdx (fun l => l.contains h)

/-- Unordered vertex pair of every edge, normalised `(min, max)`. -/
def vEdges (g : G) : List (Nat × Nat) :=
  g.E.map (fun e => (min (vOf g e.1) (vOf g e.2), max (vOf g e.1) (vOf g e.2)))

/-- Every half-edge `0 … 3|V|-1` appears exactly once across vertices and once across edges. -/
def halfEdgesOK (g : G) : Bool :=
  g.V.flatten.length == 3 * g.V.length && 2 * g.E.length == 3 * g.V.length &&
  (List.range (3 * g.V.length)).all (fun h =>
    g.V.flatten.count h == 1 && (g.E.flatMap (fun e => [e.1, e.2])).count h == 1) &&
  g.V.all (fun l => l.length == 3)

/-- Bool adjacency on vertex indices. -/
def adjB (g : G) (i j : Nat) : Bool := (vEdges g).contains (min i j, max i j)

/-! ## boxU -/

theorem boxU_halfEdges : halfEdgesOK boxU = true := by decide +kernel

/-- Known value: the vertex pairs of `boxU`, read off the half-edge data. -/
theorem boxU_vEdges :
    vEdges boxU = [(0, 1), (2, 3), (3, 4), (4, 5), (2, 5), (0, 2), (1, 3), (0, 4), (1, 5)] := by decide +kernel

/-- Simple: no loops, 9 distinct pairs. -/
theorem boxU_simple : (vEdges boxU).all (fun p => p.1 != p.2) = true ∧ (vEdges boxU).Nodup := by decide +kernel

/-- Side of each vertex under the bipartition `{0,3,5} | {1,2,4}`. -/
def sideBox (i : Nat) : Bool := [1, 2, 4].contains i

/-- `boxU` is exactly `K₃,₃`: two vertices are adjacent iff they lie on opposite sides. -/
theorem boxU_eq_K33 : ∀ i j : Fin 6, adjB boxU i j = (sideBox i != sideBox j) := by decide +kernel

/-- Relabelling `relab : Fin 6 → Fin 3 ⊕ Fin 3` (side A: 0,3,5; side B: 1,2,4). -/
def relab : Fin 6 ≃ Fin 3 ⊕ Fin 3 where
  toFun := fun i => match i with
    | 0 => Sum.inl 0 | 1 => Sum.inr 0 | 2 => Sum.inr 1
    | 3 => Sum.inl 1 | 4 => Sum.inr 2 | 5 => Sum.inl 2
  invFun := fun s => match s with
    | Sum.inl 0 => 0 | Sum.inl 1 => 3 | Sum.inl 2 => 5
    | Sum.inr 0 => 1 | Sum.inr 1 => 2 | Sum.inr 2 => 4
  left_inv := by decide +kernel
  right_inv := by decide +kernel

/-- The vertex graph of `boxU` as a Mathlib `SimpleGraph`. -/
def boxGraph : SimpleGraph (Fin 6) := SimpleGraph.fromRel (fun i j => adjB boxU i j = true)

/-- **Tie (D174).** `boxU`'s vertex graph is isomorphic to `K₃,₃ = completeBipartiteGraph (Fin 3) (Fin 3)`. -/
def boxU_iso_K33 : boxGraph ≃g completeBipartiteGraph (Fin 3) (Fin 3) where
  toEquiv := relab
  map_rel_iff' := by
    intro a b
    simp only [boxGraph, completeBipartiteGraph_adj, SimpleGraph.fromRel_adj]
    revert a b
    decide +kernel

/-- No triangles in `boxU` (bipartite). -/
def triFree (g : G) (n : Nat) : Bool :=
  (List.range n).all fun a => (List.range n).all fun b => (List.range n).all fun c =>
    !(adjB g a b && adjB g b c && adjB g a c && a != b && b != c && a != c)

theorem boxU_triFree : triFree boxU 6 = true := by decide +kernel

/-! ## Planted: the triangular prism (also cubic, 6 vertices, 9 edges) -/

/-- Prism: triangles 0-1-2 and 3-4-5, rungs 0-3, 1-4, 2-5, as half-edge data. -/
def prism : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17]],
  [(0, 3), (4, 6), (7, 1), (9, 12), (13, 15), (16, 10), (2, 11), (5, 14), (8, 17)]⟩

theorem prism_wellformed : halfEdgesOK prism = true ∧ (vEdges prism).length = 9 ∧ (vEdges prism).Nodup := by
  decide +kernel

/-- The planted prism fails the K₃,₃ statement: it has a triangle, so no bipartition works. -/
theorem prism_rejected : triFree prism 6 = false ∧
    ¬ (∀ i j : Fin 6, adjB prism i j = (sideBox i != sideBox j)) := by decide +kernel

/-! ## ttU -/

theorem ttU_halfEdges : halfEdgesOK ttU = true := by decide +kernel

/-- **Tie (D175).** `ttU`'s vertex multigraph is the double square `v0v1, v2v3, v0v2 ×2, v1v3 ×2`. -/
theorem ttU_vEdges : vEdges ttU = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 2), (1, 3)] := by decide +kernel

/-- Multiplicity of each vertex pair in `ttU`: two pairs doubled, two single, the diagonals absent. -/
theorem ttU_mult :
    (vEdges ttU).count (0, 2) = 2 ∧ (vEdges ttU).count (1, 3) = 2 ∧
    (vEdges ttU).count (0, 1) = 1 ∧ (vEdges ttU).count (2, 3) = 1 ∧
    (vEdges ttU).count (0, 3) = 0 ∧ (vEdges ttU).count (1, 2) = 0 := by decide +kernel

/-- Planted: `K₄` (cubic, simple, 4 vertices) as half-edge data; it is not the double square. -/
def k4 : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]],
  [(0, 3), (1, 6), (2, 9), (4, 7), (5, 10), (8, 11)]⟩

theorem k4_rejected : halfEdgesOK k4 = true ∧ (vEdges k4).Nodup ∧
    vEdges k4 ≠ [(0, 1), (2, 3), (0, 2), (1, 3), (0, 2), (1, 3)] := by decide +kernel

/-- Non-vacuity: the statements are about well-formed cubic graphs with the expected sizes. -/
theorem nonvacuous : boxU.V.length = 6 ∧ boxU.E.length = 9 ∧ ttU.V.length = 4 ∧ ttU.E.length = 6 := by
  decide +kernel

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Surf1Ties
