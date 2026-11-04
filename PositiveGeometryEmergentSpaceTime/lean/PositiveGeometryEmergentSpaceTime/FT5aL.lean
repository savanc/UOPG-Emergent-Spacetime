/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-!
# FT-5a-L: 4-point O(p^4) single-trace contact terms at the hidden-zero locus
Contact amplitudes (derived by sims/ft5/ft5aL_sym.py, exp parametrisation; SIMULATED derivation, see review):
T_L0 = 4 (p0·p2)(p1·p3),  T_B = 2 (p0·p1)(p2·p3) + 2 (p0·p3)(p1·p2), in Gram variables x_ij = p_i·p_j.
At four points the one-insertion amplitude is the contact term alone (O(p^4) vertices have ≥ 4 legs),
for any LO masses, which enter only through the on-shell Gram entries.
-/
namespace PositiveGeometryEmergentSpaceTime.FT5aL

/-- Gram data: off-diagonal dot products and on-shell masses squared. -/
structure Gram4 where
  /-- Dot product `p₀ · p₁`. -/
  x01 : ℝ
  /-- Dot product `p₀ · p₂`. -/
  x02 : ℝ
  /-- Dot product `p₀ · p₃`. -/
  x03 : ℝ
  /-- Dot product `p₁ · p₂`. -/
  x12 : ℝ
  /-- Dot product `p₁ · p₃`. -/
  x13 : ℝ
  /-- Dot product `p₂ · p₃`. -/
  x23 : ℝ
  /-- Squared mass `p₀ · p₀`. -/
  m0 : ℝ
  /-- Squared mass `p₁ · p₁`. -/
  m1 : ℝ
  /-- Squared mass `p₂ · p₂`. -/
  m2 : ℝ
  /-- Squared mass `p₃ · p₃`. -/
  m3 : ℝ

/-- Momentum conservation: each row of the Gram matrix sums to zero. -/
def Conserved (g : Gram4) : Prop :=
  g.m0 + g.x01 + g.x02 + g.x03 = 0 ∧ g.x01 + g.m1 + g.x12 + g.x13 = 0 ∧
  g.x02 + g.x12 + g.m2 + g.x23 = 0 ∧ g.x03 + g.x13 + g.x23 + g.m3 = 0

/-- L0 contact amplitude 4(p0·p2)(p1·p3) (script-derived, SIMULATED). -/
def TL0 (g : Gram4) : ℝ := 4 * g.x02 * g.x13
/-- O_B contact amplitude 2(p0·p1)(p2·p3) + 2(p0·p3)(p1·p2) (script-derived, SIMULATED). -/
def TB (g : Gram4) : ℝ := 2 * g.x01 * g.x23 + 2 * g.x03 * g.x12

/-- The L0 contact term vanishes on the hidden-zero locus p0·p2 = 0, for any masses. -/
theorem L0_zero (g : Gram4) (h : g.x02 = 0) : TL0 g = 0 := by
  simp [TL0, h]

/-- O_B does not: a massless, momentum-conserving point on the locus with T_B ≠ 0. -/
theorem B_not_zero : ∃ g : Gram4, Conserved g ∧ g.x02 = 0 ∧ TB g ≠ 0 := by
  refine ⟨⟨1, 0, -1, -1, 0, 1, 0, 0, 0, 0⟩, ?_, rfl, ?_⟩
  · refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num
  · norm_num [TB]

/-- O_B also fails with unequal masses (m² = 3, 5, 9, 7 assigned to legs; an explicit conserved
  point). -/
theorem B_not_zero_massive : ∃ g : Gram4, Conserved g ∧ g.x02 = 0 ∧ g.m0 ≠ g.m2 ∧ TB g ≠ 0 := by
  refine ⟨⟨-1, 0, -2, -4, 0, -5, 3, 5, 9, 7⟩, ?_, rfl, by norm_num, ?_⟩
  · refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num
  · norm_num [TB]

/-- Uniqueness within the span: a·T_L0 + b·T_B vanishes on all conserved locus points only if b = 0. -/
theorem only_L0 (a b : ℝ)
    (h : ∀ g : Gram4, Conserved g → g.x02 = 0 → a * TL0 g + b * TB g = 0) : b = 0 := by
  have := h ⟨1, 0, -1, -1, 0, 1, 0, 0, 0, 0⟩ (by refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num) rfl
  simp [TL0, TB] at this; linarith

end PositiveGeometryEmergentSpaceTime.FT5aL
