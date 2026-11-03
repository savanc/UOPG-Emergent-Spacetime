/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
SURF-1′ (prereg/SURF-1-colour-sign-coherence-2026-10-28.md, run SURF1-2026-10-28-r1).
Kernel-checked double-line colour-weight enumerator, independent of the Python checker.
Model (prereg §2): cubic vertex Tr φ³ summed over both cyclic orientations (weight 1 each);
propagator δ_il δ_jk − (c/N) δ_ij δ_kl; each closed index loop gives N.
A closed graph = list of vertices (lists of half-edge ids, cyclic order) + list of edges (pairs of
half-edge ids). Half-edge `h` has index slots `2h` (in) and `2h+1` (out). A vertex joins out(h) to
in(next h). A propagator either exchanges indices (in h – out h', out h – in h') or, for the ghost
term, contracts each end on itself (in h – out h). Every slot meets one vertex link and one edge link,
so index loops are the cycles of the alternating walk; loops are counted by marking each cycle in a\nbitmask from its first unvisited slot.
Configuration `(o, m)`: bit `j` of `o` flips the cyclic order of cubic vertex `j`; bit `i` of `m`
puts edge `i` in the ghost subset (k = popcount m). Term: `(−c)^k N^(loops − k)`.
No `sorry`, no `native_decide`.
-/
set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Surf1

/-- A graph given by vertex half-edge lists `V` and edges `E` as half-edge pairs. -/
structure G where
  V : List (List Nat)
  E : List (Nat × Nat)

/-- Slot index `2h`, the first of the two slots of half-edge `h`. -/
def inS (h : Nat) : Nat := 2 * h
/-- Slot index `2h + 1`, the second of the two slots of half-edge `h`. -/
def outS (h : Nat) : Nat := 2 * h + 1

/-- Cyclic order of vertex `j` under orientation bits `o` (cubic vertices flip `[a,b,c] ↦ [a,c,b]`). -/
def oriented (o : Nat) (j : Nat) (v : List Nat) : List Nat :=
  match v with
  | [a, b, c] => if o.testBit j then [a, c, b] else [a, b, c]
  | _ => v

/-- Successor / predecessor of half-edge `h` in a cyclic list `c` (if `h ∈ c`). -/
def nextIn (c : List Nat) (h : Nat) : Option Nat :=
  match c.idxOf? h with
  | some t => some (c.getD ((t + 1) % c.length) 0)
  | none => none

/-- The half-edge before `h` in the cyclic list `c`, if `h` occurs in `c`. -/
def prevIn (c : List Nat) (h : Nat) : Option Nat :=
  match c.idxOf? h with
  | some t => some (c.getD ((t + c.length - 1) % c.length) 0)
  | none => none

/-- First result of `f j v` over the indexed vertex list, if any. -/
def findSome (f : Nat → List Nat → Option Nat) : Nat → List (List Nat) → Option Nat
  | _, [] => none
  | j, v :: vs => match f j v with
    | some r => some r
    | none => findSome f (j + 1) vs

/-- Vertex link of slot `s`. -/
def vlink (g : G) (o s : Nat) : Nat :=
  let h := s / 2
  if s % 2 == 1 then
    inS ((findSome (fun j v => nextIn (oriented o j v) h) 0 g.V).getD 0)
  else
    outS ((findSome (fun j v => prevIn (oriented o j v) h) 0 g.V).getD 0)

/-- Find the edge containing half-edge `h`, returning its index and both endpoints. -/
def findEdge : Nat → List (Nat × Nat) → Nat → Option (Nat × Nat × Nat)
  | _, [], _ => none
  | i, e :: es, h =>
    if e.1 == h then some (i, e.1, e.2) else if e.2 == h then some (i, e.2,
        e.1) else findEdge (i + 1) es h

/-- Edge link of slot `s` (ghost if bit `i` of `m` is set for its edge `i`). -/
def elink (g : G) (m s : Nat) : Nat :=
  let h := s / 2
  match findEdge 0 g.E h with
  | some (i, _, h') =>
    if m.testBit i then (if s % 2 == 0 then outS h else inS h)
    else (if s % 2 == 0 then outS h' else inS h')
  | none => s

/-- Number of slots: twice the total number of half-edges of `g`. -/
def nSlots (g : G) : Nat := 2 * (g.V.map List.length).sum

/-- Link tables, computed once per orientation pattern / ghost mask. -/
def vtab (g : G) (o : Nat) : List Nat := (List.range (nSlots g)).map (vlink g o)
/-- Edge-link table for ghost mask `m`, one entry per slot. -/
def etab (g : G) (m : Nat) : List Nat := (List.range (nSlots g)).map (elink g m)

/-- Mark the loop through `s` (alternating vertex link, edge link) in the bitmask `vis`. -/
def markLoop (vt et : List Nat) (s : Nat) : Nat → Nat → Nat → Nat
  | 0, _, vis => vis
  | f + 1, x, vis =>
    let y := vt.getD x 0
    let vis' := vis ||| (1 <<< x) ||| (1 <<< y)
    let z := et.getD y 0
    if z == s then vis' else markLoop vt et s f z vis'

/-- Number of index loops: each unvisited slot starts a new loop. -/
def loopsT (vt et : List Nat) (n : Nat) : Nat :=
  ((List.range n).foldl (fun (st : Nat × Nat) s =>
    if st.1.testBit s then st else (markLoop vt et s n s st.1, st.2 + 1)) (0, 0)).2

/-- Number of loops of `g` for orientation pattern `o` and ghost mask `m`. -/
def loops (g : G) (o m : Nat) : Nat := loopsT (vtab g o) (etab g m) (nSlots g)

/-- Number of set bits of `m` among the lowest `n` bits. -/
def popc (m : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => (if m.testBit n then 1 else 0) + popc m n

/-- Number of cubic (three-valent) vertices of `g`. -/
def nCubic (g : G) : Nat := (g.V.filter (fun v => v.length == 3)).length

/-- Orientation patterns: cubic vertices are numbered by their position in `V`; bits only matter on
cubic vertices, so we enumerate `o < 2 ^ |V|` and divide out the 2-valent duplicates by restricting to
patterns with zero bits on 2-valent positions. -/
def oValid (g : G) (o : Nat) : Bool :=
  (List.range g.V.length).all (fun j => (g.V.getD j []).length == 3 || !o.testBit j)

/-- Orientation `o` contribution to the Laurent coefficient of `N^e` at `c = 1`:
`Σ_m (−1)^k [loops(o, m) − k = e]` over ghost masks `m < 2^|E|`. -/
def coefO (g : G) (o : Nat) (e : Int) : Int :=
  (List.range (2 ^ g.E.length)).foldr (fun m acc =>
    let k := popc m g.E.length
    if ((loops g o m : Nat) : Int) - k == e then acc + (if k % 2 == 0 then 1 else -1) else acc) 0

/-- Coefficient vector of orientation `o` over exponents `hi, hi−1, …, hi−len+1` (zero if `o` sets a bit
on a 2-valent vertex). -/
def ovec (g : G) (o : Nat) (hi : Int) (len : Nat) : List Int :=
  if oValid g o then (List.range len).map (fun i : Nat => coefO g o (hi - (i : Int)))
  else List.replicate len 0

/-- Sum of the orientation vectors for `o < j`. -/
def vsum (g : G) (hi : Int) (len : Nat) : Nat → List Int
  | 0 => List.replicate len 0
  | j + 1 => List.zipWith (· + ·) (vsum g hi len j) (ovec g j hi len)

/-- Window of exponents that contains every term: `loops ≤ nSlots` (each loop is started at a distinct
slot) and `0 ≤ k ≤ |E|`, so `−|E| ≤ loops − k ≤ nSlots`. -/
def hiW (g : G) : Int := nSlots g
/-- Length of the coefficient window of the colour weight of `g`. -/
def lenW (g : G) : Nat := nSlots g + g.E.length + 1

/-- Colour weight `W(g)` at `c = 1`: coefficients of `N^hiW, N^(hiW−1), …, N^(−|E|)`
(sum over all orientations `o < 2^|V|` and ghost masks `m < 2^|E|`). -/
def coefs (g : G) : List Int := vsum g (hiW g) (lenW g) (2 ^ g.V.length)

/-- U(N) part (`c = 0`): number of configurations with no ghost and `loops = e`. -/
def coefU (g : G) (e : Nat) : Nat :=
  ((List.range (2 ^ g.V.length)).filter (oValid g)).foldr (fun o acc =>
    if loops g o 0 == e then acc + 1 else acc) 0

/-- Laurent data `(exponent, coefficient)` (nonzero entries, decreasing exponent) of a window
  vector. -/
def nz (hi : Int) (v : List Int) : List (Int × Int) :=
  ((List.range v.length).map (fun i : Nat => (hi - (i : Int),
      v.getD i 0))).filter (fun p => p.2 != 0)

/-- `W(g)` at `c = 1` as nonzero Laurent terms. -/
def W1 (g : G) : List (Int × Int) := nz (hiW g) (coefs g)

/-! ### Graphs (prereg §2) -/

/-- P1: one propagator closed on itself through a 2-valent vertex. -/
def single : G := ⟨[[0, 1]], [(0, 1)]⟩
/-- theta = tree3 ∘ tree3. -/
def theta : G := ⟨[[0, 1, 2], [3, 4, 5]], [(0, 3), (1, 4), (2, 5)]⟩
/-- tree3 ∘ triangle (tetrahedron): tree vertex (0,1,2); triangle (3,p=4,q=5), (6,q2=7,r=8),
  (9,r2=10,p2=11). -/
def tetra : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]],
  [(4, 11), (5, 7), (8, 10), (0, 3), (1, 6), (2, 9)]⟩

/-! ### Kernel-checked colour weights at c = 1 (full exponent window) -/

/-- P1: W(single loop) = N² − 1. -/
theorem single_c1 : W1 single = [(2, 1), (0, -1)] := by decide +kernel

/-- P2: W(theta) = 2N³ − 10N + 8/N = 2(N²−1)(N²−4)/N. -/
theorem theta_c1 : W1 theta = [(3, 2), (1, -10), (-1, 8)] := by decide +kernel

/-- Triangle numerator: W(tree3 ∘ triangle) = 2N⁴ − 34N² + 128 − 96/N² = 2(N²−1)(N²−4)(N²−12)/N². -/
theorem tetra_c1 : W1 tetra = [(4, 2), (2, -34), (0, 128), (-2, -96)] := by decide +kernel

/-- Null N1 (U(N), c = 0): theta = 2N³ + 2N (only positive coefficients). -/
theorem theta_u : (List.range 5).map (coefU theta) = [0, 2, 0, 2, 0] := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Surf1
