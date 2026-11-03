/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Klein
import PositiveGeometryEmergentSpaceTime.Network
/-!
# BR-3: Klein-quadric Plücker coordinates (M1 spinor cluster) ↔ Network 2×6 minors (H-T cluster) (2026-10-14)
The 2×6 minors of `Network` are the Klein `pl` of the 2×4 column restriction, so the Plücker relation
transfers to any four columns, in particular to Lam's Y-network point `MY`. Classical; structural join only.
-/
namespace PositiveGeometryEmergentSpaceTime.BR3
open Matrix

/-- Network minors are Klein Plücker coordinates of a column restriction. -/
theorem mn_eq_pl (M : Matrix (Fin 2) (Fin 6) ℝ) (e : Fin 4 → Fin 6) (i j : Fin 4) :
    PositiveGeometryEmergentSpaceTime.Network.mn M (e i) (e j) = PositiveGeometryEmergentSpaceTime.pl (M.submatrix id e) i j := by
  rw [PositiveGeometryEmergentSpaceTime.pl_eq]; simp [PositiveGeometryEmergentSpaceTime.Network.mn]

/-- Three-term Plücker relation for any four columns `e` of a 2×6 matrix. -/
theorem plucker_any4 (M : Matrix (Fin 2) (Fin 6) ℝ) (e : Fin 4 → Fin 6) :
    PositiveGeometryEmergentSpaceTime.Network.mn M (e 0) (e 1) * PositiveGeometryEmergentSpaceTime.Network.mn M (e 2) (e 3)
      - PositiveGeometryEmergentSpaceTime.Network.mn M (e 0) (e 2) * PositiveGeometryEmergentSpaceTime.Network.mn M (e 1) (e 3)
      + PositiveGeometryEmergentSpaceTime.Network.mn M (e 0) (e 3) * PositiveGeometryEmergentSpaceTime.Network.mn M (e 1) (e 2) = 0 := by
  simp only [mn_eq_pl]; exact PositiveGeometryEmergentSpaceTime.plucker_rel _

/-- Instance: Lam's Y-network point satisfies the Plücker relation on columns 0,1,2,3. -/
theorem MY_plucker (a b c : ℝ) :
    PositiveGeometryEmergentSpaceTime.Network.mn (PositiveGeometryEmergentSpaceTime.Network.MY a b c) 0 1 * PositiveGeometryEmergentSpaceTime.Network.mn (PositiveGeometryEmergentSpaceTime.Network.MY a b c) 2 3
      - PositiveGeometryEmergentSpaceTime.Network.mn (PositiveGeometryEmergentSpaceTime.Network.MY a b c) 0 2 * PositiveGeometryEmergentSpaceTime.Network.mn (PositiveGeometryEmergentSpaceTime.Network.MY a b c) 1 3
      + PositiveGeometryEmergentSpaceTime.Network.mn (PositiveGeometryEmergentSpaceTime.Network.MY a b c) 0 3 * PositiveGeometryEmergentSpaceTime.Network.mn (PositiveGeometryEmergentSpaceTime.Network.MY a b c) 1 2 = 0 :=
  plucker_any4 _ ![0, 1, 2, 3]

/-- Non-vacuity witness: a 2×6 matrix with a nonzero minor (so the relation is not 0 = 0 trivially
  everywhere). -/
theorem br3_witness : PositiveGeometryEmergentSpaceTime.Network.mn !![1, 0, 0, 0, 0, 0; 0, 1, 0, 0, 0, 0] 0 1 = 1 := by
  simp [PositiveGeometryEmergentSpaceTime.Network.mn]

end PositiveGeometryEmergentSpaceTime.BR3
