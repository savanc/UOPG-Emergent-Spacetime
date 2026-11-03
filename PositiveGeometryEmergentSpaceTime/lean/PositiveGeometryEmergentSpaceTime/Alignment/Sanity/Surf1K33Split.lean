/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE C (2026-11-03) — SURF-1′: split the blind colour enumerator `coeffs` into
(orientation, ghost-block) pieces, so that the K₃,₃ vector can be kernel-checked piece by piece
(a whole-orientation `decide +kernel` exceeds 12 GB). Not part of `import PositiveGeometryEmergentSpaceTime`.
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Surf1Kernel.Split

/-!
# SURF-1′: ghost-block split of `coeffs`

`blk G ori lo n` is the inner ghost-mask fold of `coeffs` restricted to the masks `lo, …, lo+n−1`.
`chunk_eq_blocks`: one orientation chunk is the sum of its `nb` blocks of size `B` when `nb·B = 2^E`.
`coeffs_eq_blocks`: hence `coeffs` is the double sum over orientations and blocks.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
open Surf1Blind

/-- Step of the inner fold (one ghost mask). -/
def gstep (G : CGraph) (ori : Nat) (acc : List Int) (gh : Nat) : List Int :=
  let k := (List.range G.edges.length).countP gh.testBit
  let j := loops G ori gh + G.edges.length - k
  acc.modify j (· + (-1) ^ k)

/-- Ghost block `lo, …, lo+n−1` of the inner fold, from zero. -/
def blk (G : CGraph) (ori lo n : Nat) : List Int := (List.range' lo n).foldl (gstep G ori) (zeros G)

/-- Sum of the first `m` blocks of size `B`. -/
def bsum (G : CGraph) (ori B : Nat) : Nat → List Int
  | 0 => zeros G
  | m + 1 => List.zipWith (· + ·) (bsum G ori B m) (blk G ori (m * B) B)

theorem gfold_add (G : CGraph) (ori : Nat) (L : List Nat) (a b : List Int) (h : a.length = b.length) :
    L.foldl (gstep G ori) (List.zipWith (· + ·) a b) = List.zipWith (· + ·) a (L.foldl (gstep G ori) b) :=
  foldl_modify_zipWith L (fun gh => loops G ori gh + G.edges.length - (List.range G.edges.length).countP gh.testBit)
    (fun gh => (-1) ^ (List.range G.edges.length).countP gh.testBit) a b h

theorem length_gfold (G : CGraph) (ori : Nat) (L : List Nat) (acc : List Int) :
    (L.foldl (gstep G ori) acc).length = acc.length := by
  induction L generalizing acc with
  | nil => rfl
  | cons x L ih => simp only [List.foldl_cons]; rw [ih]; simp [gstep]

theorem length_bsum (G : CGraph) (ori B m : Nat) : (bsum G ori B m).length = (zeros G).length := by
  induction m with
  | zero => rfl
  | succ m ih => simp [bsum, ih, blk, length_gfold]

theorem gfold_eq_bsum (G : CGraph) (ori B m : Nat) :
    (List.range' 0 (m * B)).foldl (gstep G ori) (zeros G) = bsum G ori B m := by
  induction m with
  | zero => simp [bsum]
  | succ m ih =>
    have hr : List.range' 0 ((m + 1) * B) = List.range' 0 (m * B) ++ List.range' (m * B) B := by
      rw [show (m + 1) * B = m * B + B by ring, ← List.range'_append]; simp
    rw [hr, List.foldl_append, ih, bsum]
    have h0 : List.zipWith (· + ·) (bsum G ori B m) (zeros G) = bsum G ori B m := by
      apply List.ext_getElem
      · simp [length_bsum]
      · intro i h1 h2; simp [zeros]
    conv_lhs => rw [← h0]
    rw [gfold_add G ori _ _ _ (length_bsum G ori B m)]; rfl

theorem chunk_eq_blocks (G : CGraph) (ori B nb : Nat) (h : nb * B = 2 ^ G.edges.length) :
    chunk G ori = bsum G ori B nb := by
  rw [← gfold_eq_bsum, h, ← List.range_eq_range']; rfl

end PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
