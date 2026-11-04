/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — HG-DIM-1 kernel facts about the BLIND enumerator and its
agreement with the original (`PositiveGeometryEmergentSpaceTime.HgDim1Mean`). Split into small files because the kernel
does not release memory between `decide +kernel` proofs in one file (12 GB OOM otherwise).
-/
import PositiveGeometryEmergentSpaceTime.HgDim1Mean
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.HgDim1Blind

namespace PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Sanity

open PositiveGeometryEmergentSpaceTime

theorem len_8 : (HgDim1Blind.tris 8).length = 132 := by decide +kernel
theorem alllen_8 : ∀ T ∈ HgDim1Blind.tris 8, T.length = 5 := by
  have h : (HgDim1Blind.tris 8).all (fun T => T.length == 5) = true := by decide +kernel
  simpa using h

theorem sumP_8 : HgDim1Blind.sumP 8 = 1200 := by decide +kernel

/-- Same set of triangulations as the original enumerator (via the original's numeric key). -/
theorem same_set_8 : ((HgDim1Blind.tris 8).map (HgDim1Mean.key 8)).isPerm
    ((HgDim1Mean.tris 8).map (HgDim1Mean.key 8)) = true := by decide +kernel

/-- Same p on every (T,d) of the blind enumeration: blind `pval` = original `pOf`. -/
theorem same_p_8 : (HgDim1Blind.tris 8).all (fun T =>
    T.map (HgDim1Blind.pval 8 T) == T.map (HgDim1Mean.pOf 8 T)) = true := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Sanity
