/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
SUB-1 gate: the MR-2 massive hidden zero at P = (M², M², 2M²) in terms of the ππ
subthreshold parameters (Knecht–Moussallam–Stern–Fuchs / CGL form), units M_π² = 1, x = M²/F².
A(s,t,u) = x(α/3 + β(s-4/3)) + x²(λ1(s-2)² + λ2((t-2)²+(u-2)²))
         + x³(λ3(s-2)³ + λ4((t-2)³+(u-2)³)) + O(p⁸).
-/

namespace PositiveGeometryEmergentSpaceTime.SubthresholdGate

/-- Polynomial `x(α/3 + β(s − 4/3)) + x²(l₁(s − 2)² + l₂((t − 2)² + (u − 2)²)) + x³(l₃(s − 2)³ +
  l₄((t − 2)³ + (u − 2)³))` (subthreshold expansion through order `x³`). -/
noncomputable def Asub (x α β l1 l2 l3 l4 s t u : ℝ) : ℝ :=
  x * (α / 3 + β * (s - 4 / 3)) + x ^ 2 * (l1 * (s - 2) ^ 2 + l2 * ((t - 2) ^ 2 + (u - 2) ^ 2))
  + x ^ 3 * (l3 * (s - 2) ^ 3 + l4 * ((t - 2) ^ 3 + (u - 2) ^ 3))

/-- Value at P: one linear combination of the subthreshold parameters. -/
theorem Asub_at_P (x α β l1 l2 l3 l4 : ℝ) :
    Asub x α β l1 l2 l3 l4 1 1 2 = x * (α - β) / 3 + x ^ 2 * (l1 + l2) - x ^ 3 * (l3 + l4) := by
  unfold Asub; ring

/-- LO (α = β = 1, λi = 0) vanishes at P: the condition is empty at leading order. -/
theorem lo_trivial (x : ℝ) : Asub x 1 1 0 0 0 0 1 1 2 = 0 := by
  rw [Asub_at_P]; ring

/-- The zero is equivalent to a single relation α - β = -3x(λ1+λ2) + 3x²(λ3+λ4) (x ≠ 0). -/
theorem zero_iff (x α β l1 l2 l3 l4 : ℝ) (hx : x ≠ 0) :
    Asub x α β l1 l2 l3 l4 1 1 2 = 0 ↔ α - β = -3 * x * (l1 + l2) + 3 * x ^ 2 * (l3 + l4) := by
  rw [Asub_at_P]
  constructor
  · intro h
    have : x * ((α - β) + 3 * x * (l1 + l2) - 3 * x ^ 2 * (l3 + l4)) = 0 := by linarith
    rcases mul_eq_zero.mp this with h0 | h0
    · exact absurd h0 hx
    · linarith
  · intro h; rw [h]; ring

/-- Not a kinematic identity: a parameter point violating it exists. -/
theorem nontrivial : Asub 1 1 0 0 0 0 0 1 1 2 ≠ 0 := by
  rw [Asub_at_P]; norm_num

end PositiveGeometryEmergentSpaceTime.SubthresholdGate
