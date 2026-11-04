/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — BLIND second formalisation of SURF-1'.
Written from the prose only (Paper II §no-go paragraph "SURF-1'" and the model text of
prereg/SURF-1-colour-sign-coherence-2026-10-28.md §2), BEFORE reading any file under
lean/PositiveGeometryEmergentSpaceTime/Surf1/ or SurfConv.lean. Nothing here imports the original formalisation.

Independent model (prereg §2): field φ = φ^a T^a, cubic vertex Tr(φφφ) summed over both
cyclic orientations, propagator ⟨φ_ij φ_kl⟩ = δ_il δ_jk − (c/N) δ_ij δ_kl (c = 1: SU(N)),
each closed index loop gives N. Colour weight of a closed cubic graph Γ:
  W(Γ) = Σ_orientations Σ_ghost-subsets (−c)^k N^(loops − k).
Observable K_G = W(tree ∘ G) / W(tree ∘ tree).

Prose claim (Paper II): "for N ≥ 3 either the triangle-type or the crossed-box coefficient
is negative; explicitly K_tri(3) = −1 and K_box^×(N) = −8(N²−10)/(N(N²−4)) < 0 for N ≥ 4."
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.Surf1Blind

/-- A closed cubic multigraph: edge `i` joins `edges[i].1` and `edges[i].2`;
half-edge `2*i + j` is end `j` of edge `i`. -/
structure CGraph where
  nv : Nat
  edges : List (Nat × Nat)

/-- Vertex at the end of half-edge `h`. -/
def CGraph.vtx (G : CGraph) (h : Nat) : Nat :=
  let e := G.edges.getD (h / 2) (0, 0)
  if h % 2 = 0 then e.1 else e.2

/-- Half-edges at vertex `v`, in edge-list order (the "standard" cyclic order). -/
def CGraph.hes (G : CGraph) (v : Nat) : List Nat :=
  (List.range (2 * G.edges.length)).filter (fun h => G.vtx h = v)

/-- Cyclic successor of half-edge `h` at its vertex; orientation bit `o` reverses the order. -/
def CGraph.next (G : CGraph) (o : Bool) (h : Nat) : Nat :=
  let L := G.hes (G.vtx h)
  let L := if o then L.reverse else L
  let i := L.idxOf h
  L.getD ((i + 1) % L.length) 0

/-- Cyclic predecessor (successor in the reversed order). -/
def CGraph.prev (G : CGraph) (o : Bool) (h : Nat) : Nat := G.next (!o) h

/-- Slots: `2*h` is the first (row) index of the field at half-edge `h`, `2*h+1` the second.
Vertex Tr(φ_a φ_b φ_c): second index of a ↔ first index of the next field. -/
def vlink (G : CGraph) (ori : Nat) (s : Nat) : Nat :=
  let h := s / 2
  let o := ori.testBit (G.vtx h)
  if s % 2 = 1 then 2 * G.next o h else 2 * G.prev o h + 1

/-- Propagator: normal term δ_il δ_jk (i↔l, j↔k); ghost term δ_ij δ_kl ties the two slots
of each half-edge together. -/
def plink (gh : Nat) (s : Nat) : Nat :=
  let h := s / 2
  if gh.testBit (h / 2) then 2 * h + (1 - s % 2) else 2 * (h ^^^ 1) + (1 - s % 2)

/-- `σ = plink ∘ vlink`; every index loop is exactly two σ-orbits. -/
def sigma (G : CGraph) (ori gh : Nat) (s : Nat) : Nat := plink gh (vlink G ori s)

/-- `s` is the least slot of its σ-orbit (orbit length ≤ number of slots). -/
def orbitMinAux (G : CGraph) (ori gh s : Nat) : Nat → Nat → Bool
  | 0, _ => true
  | fuel + 1, x => let y := sigma G ori gh x; if y = s then true else s ≤ y && orbitMinAux G ori gh s fuel y

def isOrbitMin (G : CGraph) (ori gh : Nat) (s : Nat) : Bool :=
  orbitMinAux G ori gh s (4 * G.edges.length) s

/-- Number of closed index loops for given orientation and ghost masks. -/
def loops (G : CGraph) (ori gh : Nat) : Nat :=
  ((List.range (4 * G.edges.length)).countP (fun s => isOrbitMin G ori gh s)) / 2

/-- `W(Γ)·N^E` at c = 1 as a coefficient list: entry `j` is the coefficient of `N^(j − E)`. -/
def coeffs (G : CGraph) : List Int :=
  let E := G.edges.length
  (List.range (2 ^ G.nv)).foldl (fun acc ori =>
    (List.range (2 ^ E)).foldl (fun acc gh =>
      let k := (List.range E).countP gh.testBit
      let j := loops G ori gh + E - k
      acc.modify j (· + (-1) ^ k)) acc) (List.replicate (3 * E + 1) 0)

/-- Laurent evaluation at `N`. -/
def evalW (G : CGraph) (N : ℚ) : ℚ :=
  let E := G.edges.length
  ((coeffs G).zipIdx.map (fun p => (p.1 : ℚ) * N ^ (p.2 : ℤ) / N ^ (E : ℤ))).sum

/-- n = 3: tree ∘ tree is the theta graph; tree ∘ triangle is the tetrahedron K₄. -/
def theta : CGraph := ⟨2, [(0,1),(0,1),(0,1)]⟩
def K4 : CGraph := ⟨4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]⟩
/-- n = 4, s-channel tree glued to itself: two double edges plus two singles. -/
def dsq : CGraph := ⟨4, [(0,2),(0,2),(1,3),(1,3),(0,1),(2,3)]⟩
/-- s-channel tree glued to the crossed box: the graph is K₃,₃ (hand derivation, see note). -/
def K33 : CGraph := ⟨6, [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]⟩

/-- Blind observables. -/
noncomputable def Ktri (N : ℚ) : ℚ := evalW K4 N / evalW theta N
noncomputable def KboxX (N : ℚ) : ℚ := evalW K33 N / evalW dsq N

/-- BLIND CLAIM (prose, closed-form level). -/
def ClaimClosedForm : Prop :=
  (∀ N : ℕ, 3 ≤ N → ((N:ℚ)^2 - 12) / N < 0 ∨ -8 * ((N:ℚ)^2 - 10) / (N * ((N:ℚ)^2 - 4)) < 0)

/-- BLIND CLAIM (prose, derivation level): from the colour enumerator. -/
def ClaimEnumerated : Prop :=
  Ktri 3 = -1 ∧ (∀ N : ℕ, 4 ≤ N → KboxX N < 0) ∧ (∀ N : ℕ, 3 ≤ N → Ktri N < 0 ∨ KboxX N < 0)

end PositiveGeometryEmergentSpaceTime.Alignment.Surf1Blind
