/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — BLIND second formalisation of HG-DIM-1 (mean curvature).
Written from the prose only (Paper II §"HG-DIM-1: associahedra"; curvature paper Def. "flip
quadrilateral and p" and the statement of Thm "mean curvature of K_n"), BEFORE reading
lean/PositiveGeometryEmergentSpaceTime/HgDim1*.lean. Nothing here imports the original formalisation.

Prose claim (Paper II): on K_n, κ(e) = (2 − p(e))/(D+1), D = n − 3, and
  mean κ̄(K_n) = (10 − n)/((n − 2)(2n − 5)),
"proved on paper for all n ≥ 4, with the general algebra and kernel-checked instances
n = 5,…,9 in Lean".
Curvature paper: Σ_{(T,d)} p(T,d) = (2n − 12) Cat_{n−2} + 2n Cat_{n−3}, E[p] = 5(n−4)/(2n−5).

Blind design: our own triangulation enumerator (recursive, apex of the side (i,j)), our own
p(T,d); κ itself (Ollivier, idleness 1/(D+1)) is NOT formalised here — the full claim is
stated conditionally on an abstract curvature function satisfying the per-edge formula.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Blind

/-- Triangulations of the sub-polygon on consecutive vertices `i, i+1, …, j` (side (i,j)),
as lists of diagonals `(a,b)` with `a < b`. `fuel` bounds the recursion. -/
def triAux : Nat → Nat → Nat → List (List (Nat × Nat))
  | 0, _, _ => [[]]
  | fuel + 1, i, j =>
    if j < i + 2 then [[]] else
    (List.range (j - i - 1)).flatMap fun t =>
      let k := i + 1 + t
      (triAux fuel i k).flatMap fun A => (triAux fuel k j).map fun B =>
        (if k - i ≥ 2 then [(i, k)] else []) ++ (if j - k ≥ 2 then [(k, j)] else []) ++ A ++ B

/-- All triangulations of the convex `n`-gon with vertices `0,…,n−1`. -/
def tris (n : Nat) : List (List (Nat × Nat)) := triAux n 0 (n - 1)

/-- `{x,y}` is a side of the polygon. -/
def isSide (n x y : Nat) : Bool :=
  x + 1 = y || y + 1 = x || (x = 0 && y + 1 = n) || (y = 0 && x + 1 = n)

/-- `x,y` adjacent in the triangulation (side or diagonal of `T`). -/
def adj (n : Nat) (T : List (Nat × Nat)) (x y : Nat) : Bool :=
  isSide n x y || T.contains (min x y, max x y)

/-- p(T,d): the two triangles of `T` on `d = (a,b)` have apexes c₁ ∈ (a,b), c₂ ∉ [a,b];
count the four sides of the flip quadrilateral that are diagonals (not polygon sides). -/
def pval (n : Nat) (T : List (Nat × Nat)) (d : Nat × Nat) : Nat :=
  let a := d.1
  let b := d.2
  let apex := (List.range n).filter fun c => c ≠ a && c ≠ b && adj n T a c && adj n T b c
  let sides := apex.flatMap fun c => [(a, c), (c, b)]
  sides.countP fun s => !isSide n s.1 s.2

/-- Σ_{(T,d)} p(T,d). -/
def sumP (n : Nat) : Nat := ((tris n).map fun T => (T.map (pval n T)).sum).sum

/-- Mean of (2 − p)/(n − 2) over all (T,d) pairs (= mean over edges, since p(T,d) = p(T',d')). -/
def meanKappaLocal (n : Nat) : ℚ :=
  (((tris n).map fun T => (T.map fun d => ((2 : ℚ) - pval n T d) / (n - 2))).map List.sum).sum
    / ((tris n).length * (n - 3))

/-- BLIND CLAIM (counting layer, instances). -/
def ClaimSumP : Prop :=
  ∀ n ∈ ({5, 6, 7, 8, 9} : Finset ℕ),
    (sumP n : ℤ) = (2 * n - 12) * (catalan (n - 2) : ℤ) + 2 * n * catalan (n - 3)

/-- BLIND CLAIM (mean of the local formula, instances). -/
def ClaimMeanLocal : Prop :=
  ∀ n ∈ ({5, 6, 7, 8, 9} : Finset ℕ),
    meanKappaLocal n = (10 - (n : ℚ)) / ((n - 2) * (2 * n - 5))

/-- BLIND CLAIM (full, conditional form): for any edge-curvature function on (T,d) pairs that
obeys the per-edge formula, the mean is the closed form. The per-edge formula itself
(Ollivier curvature = (2−p)/(D+1)) is the paper-proved input. -/
def ClaimMeanConditional : Prop :=
  ∀ n ∈ ({5, 6, 7, 8, 9} : Finset ℕ), ∀ κ : List (Nat × Nat) → Nat × Nat → ℚ,
    (∀ T ∈ tris n, ∀ d ∈ T, κ T d = (2 - (pval n T d : ℚ)) / (n - 2)) →
    (((tris n).map fun T => (T.map (κ T)).sum).sum) / ((tris n).length * (n - 3))
      = (10 - (n : ℚ)) / ((n - 2) * (2 * n - 5))

end PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Blind
