/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.LeanCert
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.LeanCert1Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: LEAN-CERT-1 (N_ACC and ABHY counts)

Blind: (A) ABHY count `dim ker C_n = n(n−3)/2` for **all** `n ≥ 3` (rank–nullity + surjectivity of the
row-sum map), instantiated at n = 5, 6, 7; (B) N_ACC with normalisation `Y_Q = 1/6`: exactly 2 solutions.
Original: (A) kernel certificates at n = 5, 6, 7 for `eq5` (`abhy*_finrank` = 5, 9, 14) **and** the explicit
planar-basis identification `ker = range eq10`; (B) `ACC` with `Y_Q = 1` (charges ×6), `acc_iff`, and
`accSet.card = 2` over a finite grid; planted wrong answers rejected.

VERDICT: **DIFFERENT** — (B) N_ACC is EQUIV (`acc_scale`, `solutions_correspond`); (A) is
BLIND-STRONGER on the count (all n) and ORIG-STRONGER on the basis (`eq10`, which the blind lacks).
GAP: the blind `C n` and the original `eq5 n N` are both "sum over pairs containing a vertex"
maps but are not formally identified; only their kernel dimensions are proved equal.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.LeanCert1

open PositiveGeometryEmergentSpaceTime.Alignment.LeanCert1Blind

/-- ACC under the normalisation change `Y_Q = 1/6` (blind) ↔ `Y_Q = 1` (original), charges ×6. -/
theorem acc_scale (u d l e : ℚ) :
    LeanCert1Blind.ACC ⟨1/6, u, d, l, e⟩ ↔ PositiveGeometryEmergentSpaceTime.LeanCert.ACC (6 * u) (6 * d) (6 * l) (6 * e) := by
  simp only [LeanCert1Blind.ACC, PositiveGeometryEmergentSpaceTime.LeanCert.ACC]
  constructor
  · rintro ⟨b1, b2, b3, b4⟩
    exact ⟨by linear_combination 6 * b1, by linear_combination 6 * b3,
      by linear_combination 6 * b2, by linear_combination 216 * b4⟩
  · rintro ⟨o1, o2, o3, o4⟩
    exact ⟨by linear_combination o1 / 6, by linear_combination o3 / 6,
      by linear_combination o2 / 6, by linear_combination o4 / 216⟩

/-- The two solution sets correspond under ×6. -/
theorem solutions_correspond :
    (fun y : Hyp => (6 * y.yu, 6 * y.yd, 6 * y.yL, 6 * y.ye)) '' solSet = ↑PositiveGeometryEmergentSpaceTime.LeanCert.accSet := by
  rw [solSet_eq, PositiveGeometryEmergentSpaceTime.LeanCert.nacc_set_eq, Set.image_pair]
  simp only [Finset.coe_insert, Finset.coe_singleton]
  norm_num

/-- Headline counts agree. -/
theorem nacc_agree : solSet.ncard = PositiveGeometryEmergentSpaceTime.LeanCert.accSet.card := by
  rw [nacc_eq_two_blind, PositiveGeometryEmergentSpaceTime.LeanCert.nacc_eq_two]

/-- ABHY: the blind general count equals the original certified dimension at n = 5, 6, 7. -/
theorem abhy_agree :
    Module.finrank ℚ (LinearMap.ker (C 5)) =
      Module.finrank ℚ (LinearMap.ker (PositiveGeometryEmergentSpaceTime.LeanCert.cq (PositiveGeometryEmergentSpaceTime.LeanCert.eq5 5 10)).mulVecLin) ∧
    Module.finrank ℚ (LinearMap.ker (C 6)) =
      Module.finrank ℚ (LinearMap.ker (PositiveGeometryEmergentSpaceTime.LeanCert.cq (PositiveGeometryEmergentSpaceTime.LeanCert.eq5 6 15)).mulVecLin) ∧
    Module.finrank ℚ (LinearMap.ker (C 7)) =
      Module.finrank ℚ (LinearMap.ker (PositiveGeometryEmergentSpaceTime.LeanCert.cq (PositiveGeometryEmergentSpaceTime.LeanCert.eq5 7 21)).mulVecLin) := by
  rw [abhy_count_5, abhy_count_6, abhy_count_7, PositiveGeometryEmergentSpaceTime.LeanCert.abhy5_finrank,
    PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_finrank, PositiveGeometryEmergentSpaceTime.LeanCert.abhy7_finrank]
  norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.LeanCert1
