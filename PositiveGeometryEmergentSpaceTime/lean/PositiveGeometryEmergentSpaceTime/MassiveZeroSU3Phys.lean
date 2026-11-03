/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-2d: SU(3) ππ tree O(p⁴) amplitude at the massive hidden-zero point P = (M²,M²,2M²), M = 1.
The polynomial form A·F⁴ = F²(s-1) + 4(2L1+L3)(s-2)² + 4L2((t-2)²+(u-2)²) + c0 + c1 s with
c0 = -8(2L4 - L4 ms + L5 - 4L6 - 2L8), c1 = -8 L4 ms is SIMULATED (sims/mr2d/tree.py);
this file proves the algebra from that form to the hidden-zero condition and its running.
-/

namespace PositiveGeometryEmergentSpaceTime.MassiveZeroSU3Phys

/-- Explicit polynomial amplitude in `s, t` (with `u = 4 − s − t`), quadratic order `F²(s − 1)` plus
  LEC terms in `L₁…L₆, L₈` and `ms`. -/
noncomputable def AF4 (F L1 L2 L3 L4 L5 L6 L8 ms s t : ℝ) : ℝ :=
  let u := 4 - s - t
  F ^ 2 * (s - 1) + 4 * (2 * L1 + L3) * (s - 2) ^ 2 + 4 * L2 * ((t - 2) ^ 2 + (u - 2) ^ 2)
    - 8 * (2 * L4 - L4 * ms + L5 - 4 * L6 - 2 * L8) - 8 * L4 * ms * s

/-- Hidden-zero value: m_s and F drop out at P. -/
theorem AF4_at_P (F L1 L2 L3 L4 L5 L6 L8 ms : ℝ) :
    AF4 F L1 L2 L3 L4 L5 L6 L8 ms 1 1 =
      4 * (2 * L1 + L2 + L3) + 16 * (2 * L6 - L4) + 8 * (2 * L8 - L5) := by
  unfold AF4; ring

/-- Same value in the raw L-basis. -/
theorem Z_raw (L1 L2 L3 L4 L5 L6 L8 : ℝ) :
    4 * (2 * L1 + L2 + L3) + 16 * (2 * L6 - L4) + 8 * (2 * L8 - L5) =
      8 * L1 + 4 * L2 + 4 * L3 - 16 * L4 - 8 * L5 + 32 * L6 + 16 * L8 := by ring

/-- Running coefficient of Z with GL85 Γ_i (CITED): Γ_Z = 11/18 ≠ 0, so Z is scale dependent. -/
theorem GammaZ :
    8 * (3 / 32 : ℝ) + 4 * (3 / 16) + 4 * 0 - 16 * (1 / 8) - 8 * (3 / 8) + 32 * (11 / 144)
      + 16 * (5 / 48) = 11 / 18 := by norm_num

/-- Zero iff the L5/L8 combination is fixed by the others (no pure L5/L8 relation). -/
theorem zero_iff (L1 L2 L3 L4 L5 L6 L8 : ℝ) :
    4 * (2 * L1 + L2 + L3) + 16 * (2 * L6 - L4) + 8 * (2 * L8 - L5) = 0 ↔
      2 * L8 - L5 = -(2 * L1 + L2 + L3) / 2 - 2 * (2 * L6 - L4) := by
  constructor <;> intro h <;> linarith

end PositiveGeometryEmergentSpaceTime.MassiveZeroSU3Phys
