/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-2e: lattice-only consequence of the MR-4 πK hidden-zero line at tree NLO.
Line coefficients (SIMULATED, matched to BDM/BKM in `PositiveGeometryEmergentSpaceTime.PiKZero`):
 c0 = 2 MK² Mp² (4L1+L3-4L4-L5+4L6+2L8),  c1 = -(MK²+Mp²)(4L1+L3-2L4).
If both vanish, the kinematic LECs drop out: R := 2(2L6-L4) + (2L8-L5) = 0.
-/

namespace PositiveGeometryEmergentSpaceTime.FlagRelation

/-- Exact identity: `c0/(2MK²Mp²) + c1/(MK² + Mp²) = 2(2L6 − L4) + (2L8 − L5)` for the two πK line
  coefficients (nonzero masses). -/
theorem R_identity (Mp MK L1 L3 L4 L5 L6 L8 : ℝ) (hp : Mp ≠ 0) (hK : MK ≠ 0) (hs : MK^2 + Mp^2 ≠ 0) :
    (2*MK^2*Mp^2*(4*L1+L3-4*L4-L5+4*L6+2*L8)) / (2*MK^2*Mp^2)
      + (-(MK^2+Mp^2)*(4*L1+L3-2*L4)) / (MK^2+Mp^2)
    = 2*(2*L6 - L4) + (2*L8 - L5) := by
  field_simp; ring

/-- If both πK line coefficients `c0` and `c1` vanish, then `R = 2(2L6 − L4) + (2L8 − L5) = 0`. -/
theorem zero_implies_R (Mp MK L1 L3 L4 L5 L6 L8 : ℝ) (hp : Mp ≠ 0) (hK : MK ≠ 0)
    (hs : MK^2 + Mp^2 ≠ 0)
    (h0 : 2*MK^2*Mp^2*(4*L1+L3-4*L4-L5+4*L6+2*L8) = 0)
    (h1 : -(MK^2+Mp^2)*(4*L1+L3-2*L4) = 0) :
    2*(2*L6 - L4) + (2*L8 - L5) = 0 := by
  have := R_identity Mp MK L1 L3 L4 L5 L6 L8 hp hK hs
  rw [h0, h1, zero_div, zero_div, add_zero] at this; linarith

/-- Running coefficient with GL85 Γ_i (CITED): Γ_R = -1/9 ≠ 0, so R is scale dependent. -/
theorem GammaR : 2*(2*(11/144:ℝ) - 1/8) + (2*(5/48) - 3/8) = -1/9 := by norm_num

end PositiveGeometryEmergentSpaceTime.FlagRelation
