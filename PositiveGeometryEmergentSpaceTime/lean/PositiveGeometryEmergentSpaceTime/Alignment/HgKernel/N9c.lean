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

/-- Same p on every (T,d) of the blind enumeration: blind `pval` = original `pOf`. -/
theorem same_p_9 : (HgDim1Blind.tris 9).all (fun T =>
    T.map (HgDim1Blind.pval 9 T) == T.map (HgDim1Mean.pOf 9 T)) = true := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Sanity
