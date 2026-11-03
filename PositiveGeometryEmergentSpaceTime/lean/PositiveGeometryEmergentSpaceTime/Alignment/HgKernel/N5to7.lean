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

theorem len_5 : (HgDim1Blind.tris 5).length = 5 := by decide +kernel
theorem alllen_5 : ∀ T ∈ HgDim1Blind.tris 5, T.length = 2 := by
  have h : (HgDim1Blind.tris 5).all (fun T => T.length == 2) = true := by decide +kernel
  simpa using h

theorem sumP_5 : HgDim1Blind.sumP 5 = 10 := by decide +kernel

/-- Same set of triangulations as the original enumerator (via the original's numeric key). -/
theorem same_set_5 : ((HgDim1Blind.tris 5).map (HgDim1Mean.key 5)).isPerm
    ((HgDim1Mean.tris 5).map (HgDim1Mean.key 5)) = true := by decide +kernel

/-- Same p on every (T,d) of the blind enumeration: blind `pval` = original `pOf`. -/
theorem same_p_5 : (HgDim1Blind.tris 5).all (fun T =>
    T.map (HgDim1Blind.pval 5 T) == T.map (HgDim1Mean.pOf 5 T)) = true := by decide +kernel

theorem len_6 : (HgDim1Blind.tris 6).length = 14 := by decide +kernel
theorem alllen_6 : ∀ T ∈ HgDim1Blind.tris 6, T.length = 3 := by
  have h : (HgDim1Blind.tris 6).all (fun T => T.length == 3) = true := by decide +kernel
  simpa using h

theorem sumP_6 : HgDim1Blind.sumP 6 = 60 := by decide +kernel

/-- Same set of triangulations as the original enumerator (via the original's numeric key). -/
theorem same_set_6 : ((HgDim1Blind.tris 6).map (HgDim1Mean.key 6)).isPerm
    ((HgDim1Mean.tris 6).map (HgDim1Mean.key 6)) = true := by decide +kernel

/-- Same p on every (T,d) of the blind enumeration: blind `pval` = original `pOf`. -/
theorem same_p_6 : (HgDim1Blind.tris 6).all (fun T =>
    T.map (HgDim1Blind.pval 6 T) == T.map (HgDim1Mean.pOf 6 T)) = true := by decide +kernel

theorem len_7 : (HgDim1Blind.tris 7).length = 42 := by decide +kernel
theorem alllen_7 : ∀ T ∈ HgDim1Blind.tris 7, T.length = 4 := by
  have h : (HgDim1Blind.tris 7).all (fun T => T.length == 4) = true := by decide +kernel
  simpa using h

theorem sumP_7 : HgDim1Blind.sumP 7 = 280 := by decide +kernel

/-- Same set of triangulations as the original enumerator (via the original's numeric key). -/
theorem same_set_7 : ((HgDim1Blind.tris 7).map (HgDim1Mean.key 7)).isPerm
    ((HgDim1Mean.tris 7).map (HgDim1Mean.key 7)) = true := by decide +kernel

/-- Same p on every (T,d) of the blind enumeration: blind `pval` = original `pOf`. -/
theorem same_p_7 : (HgDim1Blind.tris 7).all (fun T =>
    T.map (HgDim1Blind.pval 7 T) == T.map (HgDim1Mean.pOf 7 T)) = true := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Sanity
