/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31): split the BLIND SURF-1′ enumerator `coeffs` into one chunk per
orientation pattern, so that each chunk can be kernel-checked separately (a single
`decide +kernel` on `coeffs K4` exceeds 12 GB).
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Surf1Blind

namespace PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
open Surf1Blind

/-- Ghost-mask sum for one orientation pattern, starting from `acc` (the inner fold of `coeffs`). -/
def inner (G : CGraph) (ori : Nat) (acc : List Int) : List Int :=
  (List.range (2 ^ G.edges.length)).foldl (fun acc gh =>
      let k := (List.range G.edges.length).countP gh.testBit
      let j := loops G ori gh + G.edges.length - k
      acc.modify j (· + (-1) ^ k)) acc

/-- Zero vector of `coeffs`. -/
def zeros (G : CGraph) : List Int := List.replicate (3 * G.edges.length + 1) 0

/-- Per-orientation chunk. -/
def chunk (G : CGraph) (ori : Nat) : List Int := inner G ori (zeros G)

theorem coeffs_eq_foldl (G : CGraph) :
    coeffs G = (List.range (2 ^ G.nv)).foldl (fun acc ori => inner G ori acc) (zeros G) := rfl

theorem modify_zipWith (a b : List Int) (h : a.length = b.length) (j : Nat) (c : Int) :
    (List.zipWith (· + ·) a b).modify j (· + c) = List.zipWith (· + ·) a (b.modify j (· + c)) := by
  apply List.ext_getElem
  · simp [h]
  · intro i h1 h2
    simp only [List.getElem_modify, List.getElem_zipWith]
    split <;> ring

theorem foldl_modify_zipWith (L : List Nat) (f : Nat → Nat) (g : Nat → Int) :
    ∀ (a b : List Int), a.length = b.length →
    L.foldl (fun acc x => acc.modify (f x) (· + g x)) (List.zipWith (· + ·) a b) =
      List.zipWith (· + ·) a (L.foldl (fun acc x => acc.modify (f x) (· + g x)) b) := by
  induction L with
  | nil => intro a b _; rfl
  | cons x L ih =>
    intro a b h
    simp only [List.foldl_cons]
    rw [modify_zipWith a b h]
    exact ih a _ (by simp [h])

theorem zipWith_zeros (b : List Int) (n : Nat) (h : b.length = n) :
    List.zipWith (· + ·) (List.replicate n 0) b = b := by
  subst h
  apply List.ext_getElem <;> simp

theorem length_inner (G : CGraph) (ori : Nat) (acc : List Int) :
    (inner G ori acc).length = acc.length := by
  unfold inner
  generalize List.range (2 ^ G.edges.length) = L
  induction L generalizing acc with
  | nil => rfl
  | cons x L ih => simp only [List.foldl_cons]; rw [ih]; simp

theorem inner_add (G : CGraph) (ori : Nat) (a : List Int) (ha : a.length = (zeros G).length) :
    inner G ori a = List.zipWith (· + ·) a (chunk G ori) := by
  have h0 : List.zipWith (· + ·) a (zeros G) = a := by
    apply List.ext_getElem
    · simp [ha]
    · intro i h1 h2; simp [zeros]
  conv_lhs => rw [← h0]
  exact foldl_modify_zipWith _ _ _ a (zeros G) ha

/-- Sum of the first `n` orientation chunks. -/
def csum (G : CGraph) : Nat → List Int
  | 0 => zeros G
  | n + 1 => List.zipWith (· + ·) (csum G n) (chunk G n)

theorem length_csum (G : CGraph) (n : Nat) : (csum G n).length = (zeros G).length := by
  induction n with
  | zero => rfl
  | succ n ih => simp [csum, ih, chunk, length_inner]

theorem foldl_eq_csum (G : CGraph) (n : Nat) :
    (List.range n).foldl (fun acc ori => inner G ori acc) (zeros G) = csum G n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [List.range_succ, List.foldl_append, ih]
    simp only [List.foldl_cons, List.foldl_nil, csum]
    exact inner_add G n _ (length_csum G n)

theorem coeffs_eq_csum (G : CGraph) : coeffs G = csum G (2 ^ G.nv) := by
  rw [coeffs_eq_foldl, foldl_eq_csum]

end PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
