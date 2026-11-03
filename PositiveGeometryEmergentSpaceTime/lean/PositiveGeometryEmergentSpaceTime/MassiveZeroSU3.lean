/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-2c Gate 1: SU(3)/U(N) single-trace massive hidden zero at P = (M²,M²,2M²), units M = 1.
Degenerate-mass ordered 4-pt amplitude, s + t + u = 4. On shell p_i² = 1:
  p1·p2 = (s-2)/2, p2·p3 = (t-2)/2, p1·p3 = (u-2)/2.
Single-trace O(p⁴) kinematic structures (L0/L3-type operators, CONJECTURE that these are the only two
independent ones after on-shell reduction):
  SA = (p1·p2)(p3·p4) + (p2·p3)(p4·p1) = ((s-2)² + (t-2)²)/4,   SB = (p1·p3)(p2·p4) = (u-2)²/4.
Mass operators (L5, L8 single trace) give terms c5·(s+t)·… and constants; we keep them as free
linear coefficients. Result: the zero condition at P carries SA(P) = 1/2 ≠ 0, so it cannot be
evaluated from L5, L8 alone (needs kinematic LECs L0..L3, absent from FLAG 2019 Table 25).
-/

namespace PositiveGeometryEmergentSpaceTime.MassiveZeroSU3

/-- Polynomial `SA(s, t) = ((s − 2)² + (t − 2)²)/4`. -/
noncomputable def SA (s t : ℝ) : ℝ := ((s - 2) ^ 2 + (t - 2) ^ 2) / 4
/-- Polynomial `SB(s, t) = (u − 2)²/4` with `u = 4 − s − t`. -/
noncomputable def SB (s t : ℝ) : ℝ := ((4 - s - t) - 2) ^ 2 / 4

/-- Dot products at P = (1,1,2): p1·p2 = p2·p3 = -1/2, p1·p3 = 0. -/
theorem dots_at_P : ((1:ℝ) - 2) / 2 = -1/2 ∧ ((4 - 1 - 1 : ℝ) - 2) / 2 = 0 := by norm_num

/-- `SA 1 1 = 1/2`. -/
theorem SA_at_P : SA 1 1 = 1 / 2 := by unfold SA; norm_num
/-- `SB 1 1 = 0`. -/
theorem SB_at_P : SB 1 1 = 0 := by unfold SB; norm_num

/-- NLO ordered amplitude: kinematic (αA, αB) + mass-operator part (linear in s+t with c5, constant
  c8). -/
noncomputable def fNLO (αA αB c5 c8 : ℝ) (s t : ℝ) : ℝ := αA * SA s t + αB * SB s t + c5 * (s + t) + c8

/-- Hidden-zero value at P: the kinematic coefficient αA enters with weight 1/2. -/
theorem fNLO_at_P (αA αB c5 c8 : ℝ) : fNLO αA αB c5 c8 1 1 = αA / 2 + 2 * c5 + c8 := by
  unfold fNLO; rw [SA_at_P, SB_at_P]; ring

/-- Non-determination: the mass coefficients (c5, c8) alone never decide the zero condition. -/
theorem not_determined_by_mass (αB c5 c8 : ℝ) :
    ∃ αA αA' : ℝ, fNLO αA αB c5 c8 1 1 = 0 ∧ fNLO αA' αB c5 c8 1 1 ≠ 0 := by
  refine ⟨-2 * (2 * c5 + c8), -2 * (2 * c5 + c8) + 2, ?_, ?_⟩ <;>
    rw [fNLO_at_P] <;> norm_num <;> ring_nf <;> norm_num

/-- Only if αA = 0 (kinematic single-trace LEC combination vanishes) is it an L5/L8 relation. -/
theorem mass_only_iff (αB c5 c8 : ℝ) : fNLO 0 αB c5 c8 1 1 = 0 ↔ c8 = -2 * c5 := by
  rw [fNLO_at_P]; constructor <;> intro h <;> linarith

end PositiveGeometryEmergentSpaceTime.MassiveZeroSU3
