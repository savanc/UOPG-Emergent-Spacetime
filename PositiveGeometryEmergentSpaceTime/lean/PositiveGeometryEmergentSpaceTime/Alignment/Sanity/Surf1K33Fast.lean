/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE C (2026-11-03) — SURF-1′: a table form of the blind enumerator on `K33`, proved equal
to the original `blk`, so that the kernel pieces evaluate cheaper. Not part of `import PositiveGeometryEmergentSpaceTime`.
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Surf1K33Split

/-!
# SURF-1′: table form of the K₃,₃ enumerator

`vT`, `nT` tabulate `K33.vtx` and `K33.next` on the 18 half-edges (each checked by `decide`). `blkT`
is `blk K33` with `σ` computed from these tables; `blk_eq_blkT` proves the two folds equal for every
orientation, ghost range and length. The orbit counter is rewritten through a `σ`-generic `orbF`.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
open Surf1Blind

/-- Orbit-minimum test for an arbitrary successor function. -/
def orbF (σ : Nat → Nat) (s : Nat) : Nat → Nat → Bool
  | 0, _ => true
  | fuel + 1, x => let y := σ x; if y = s then true else s ≤ y && orbF σ s fuel y

theorem orbitMinAux_eq (G : CGraph) (ori gh s : Nat) :
    ∀ fuel x, orbitMinAux G ori gh s fuel x = orbF (sigma G ori gh) s fuel x
  | 0, _ => rfl
  | fuel + 1, x => by simp only [orbitMinAux, orbF, orbitMinAux_eq G ori gh s fuel]

/-- Loop count for an arbitrary successor function on `n` slots. -/
def loopsF (σ : Nat → Nat) (n : Nat) : Nat := ((List.range n).countP (fun s => orbF σ s n s)) / 2

theorem loops_eq (G : CGraph) (ori gh : Nat) :
    loops G ori gh = loopsF (sigma G ori gh) (4 * G.edges.length) := by
  unfold loops isOrbitMin loopsF; simp only [orbitMinAux_eq]

/-- Vertex of each half-edge of `K33`. -/
def vT : List Nat := [0, 3, 0, 4, 0, 5, 1, 3, 1, 4, 1, 5, 2, 3, 2, 4, 2, 5]
/-- Cyclic successor of each half-edge of `K33`, standard (`false`) and reversed (`true`) order. -/
def nT : Bool → List Nat
  | false => [2, 7, 4, 9, 0, 11, 8, 13, 10, 15, 6, 17, 14, 1, 16, 3, 12, 5]
  | true => [4, 13, 0, 15, 2, 17, 10, 1, 6, 3, 8, 5, 16, 7, 12, 9, 14, 11]

theorem vtx_T : ∀ h : Fin 18, K33.vtx h = vT.getD h 0 := by decide
theorem next_T : ∀ (o : Bool) (h : Fin 18), K33.next o h = (nT o).getD h 0 := by decide

/-- Table form of `vlink K33`. -/
def vlinkT (ori s : Nat) : Nat :=
  if s < 36 then
    let h := s / 2
    let o := ori.testBit (vT.getD h 0)
    if s % 2 = 1 then 2 * (nT o).getD h 0 else 2 * (nT (!o)).getD h 0 + 1
  else vlink K33 ori s

theorem vlink_eq (ori s : Nat) : vlink K33 ori s = vlinkT ori s := by
  unfold vlinkT
  split
  · rename_i hs
    have hh : s / 2 < 18 := by omega
    have e1 := vtx_T ⟨s / 2, hh⟩
    have e2 := next_T true ⟨s / 2, hh⟩
    have e3 := next_T false ⟨s / 2, hh⟩
    simp only at e1 e2 e3
    simp only [vlink, CGraph.prev, e1]
    cases ori.testBit (vT.getD (s / 2) 0) <;> simp [e2, e3]
  · rfl

/-- Table form of `σ` on `K33`. -/
def sigmaT (ori gh s : Nat) : Nat := plink gh (vlinkT ori s)

theorem sigma_eq (ori gh : Nat) : sigma K33 ori gh = sigmaT ori gh := by
  funext s; simp only [sigma, sigmaT, vlink_eq]

/-- Table form of one ghost step. -/
def gstepT (ori : Nat) (acc : List Int) (gh : Nat) : List Int :=
  let k := (List.range 9).countP gh.testBit
  acc.modify (loopsF (sigmaT ori gh) 36 + 9 - k) (· + (-1) ^ k)

/-- Table form of a ghost block. -/
def blkT (ori lo n : Nat) : List Int := (List.range' lo n).foldl (gstepT ori) (List.replicate 28 0)

theorem blk_eq_blkT (ori lo n : Nat) : blk K33 ori lo n = blkT ori lo n := by
  have : gstep K33 ori = gstepT ori := by
    funext acc gh; simp only [gstep, gstepT, loops_eq, sigma_eq]; rfl
  simp only [blk, blkT, this]; rfl

end PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
