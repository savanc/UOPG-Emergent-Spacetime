/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.FT2Mesh
import PositiveGeometryEmergentSpaceTime.MassShift
/-!
# BR-2: FT2Mesh spurion shifts ↔ MassShift offset reparametrisation (2026-10-14)
Spurion (unequal quark-line mass) shifts X_ij ↦ X_ij + ν_i + ν_j leave every mesh combination invariant
(FT2Mesh). Keeping the 6-pt poles X14, X25, X36 fixed needs ν4 = −ν1, ν5 = −ν2, ν6 = −ν3. A6N is NOT invariant
under this whole family; MassShift's `a6n_reparam` is exactly its one-parameter member ν = (−l/2, l/2, −l/2).
-/
namespace PositiveGeometryEmergentSpaceTime.BR2
open PositiveGeometryEmergentSpaceTime.NLSM

/-- (a) Spurion shifts cancel in the mesh combination (instance of FT2Mesh.mesh_shift_cancels). -/
theorem spurion_shift_mesh (Y11 Y22 Y12 Y21 νa νa1 νb νb1 : ℝ) :
    ((Y11 + (νa + νb)) + (Y22 + (νa1 + νb1)) - (Y12 + (νa + νb1)) - (Y21 + (νa1 + νb)))
      = Y11 + Y22 - Y12 - Y21 := by
  have := PositiveGeometryEmergentSpaceTime.FT2Mesh.mesh_shift_cancels Y11 Y22 Y12 Y21 (-νa) (-νa1) (-νb) (-νb1)
  linarith

/-- Pole-preserving spurion shift of the nine 6-pt planar variables. -/
noncomputable def A6Nsp (n1 n2 n3 X13 X14 X15 X24 X25 X26 X35 X36 X46 : ℝ) : ℝ :=
  A6N (X13 + (n1 + n3)) X14 (X15 + (n1 - n2)) (X24 + (n2 - n1)) X25 (X26 + (n2 - n3))
    (X35 + (n3 - n2)) X36 (X46 + (-n1 - n3))

/-- (b) `a6n_reparam` is the spurion shift with ν = (−l/2, l/2, −l/2). -/
theorem a6n_reparam_is_spurion (l X13 X14 X15 X24 X25 X26 X35 X36 X46 : ℝ) :
    A6Nsp (-l/2) (l/2) (-l/2) X13 X14 X15 X24 X25 X26 X35 X36 X46 =
      A6N X13 X14 X15 X24 X25 X26 X35 X36 X46 := by
  have h := PositiveGeometryEmergentSpaceTime.MassShift.a6n_reparam X13 X14 X15 X24 X25 X26 X35 X36 X46 l
  simp only [A6Nsp]
  convert h using 2 <;> ring

/-- (c) General spurion shifts do change A6N (ν = (1,0,0), poles 1, other variables 0). -/
theorem a6n_not_spurion_invariant :
    A6Nsp 1 0 0 0 1 0 0 1 0 0 1 0 ≠ A6N 0 1 0 0 1 0 0 1 0 := by
  simp only [A6Nsp, A6N]; norm_num

/-- (d) Non-vacuity witness: the reparam instance holds at an explicit point with nonzero poles. -/
theorem br2_witness : A6Nsp (-1/2) (1/2) (-1/2) 1 1 1 1 1 1 1 1 1 = A6N 1 1 1 1 1 1 1 1 1 :=
  a6n_reparam_is_spurion 1 1 1 1 1 1 1 1 1 1

end PositiveGeometryEmergentSpaceTime.BR2
