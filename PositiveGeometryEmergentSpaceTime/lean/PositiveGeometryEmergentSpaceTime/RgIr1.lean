import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# RgIr1 — algebra behind RG-IR-1 (top-Yukawa IR quasi-fixed point vs UV memory), 2026-10-30

One-loop SM: `dy/dt = κ y (a y² − G)`, `G = Σ cᵢ gᵢ²`, `κ = 1/16π²`. For `u = 1/y²` the flow is affine
(`u_flow_affine`), so `u_IR = S u_UV + A` and widths contract by `S` (`affine_width`, `affine_contracts`):
the flow narrows a UV prior but never selects a point. QCD-only: `R = y²/g₃²` has the unique positive
fixed point `2/9` and sensitivity exponent `8/7 − 1 = 1/7 > 0`. `exp_ratio_invariant`: the exponents
`−cᵢ/bᵢ` are unchanged by coupling renormalisations `g² ↦ k g²` (GUT vs SM hypercharge normalisation)
and by `ln μ` vs `ln μ²` (all coefficients × k).
-/

namespace PositiveGeometryEmergentSpaceTime.RgIr1

/-- Chain rule for `u = 1/y²`: `du/dt = −2 y⁻³ dy/dt` turns the cubic Yukawa flow into an affine one. -/
theorem u_flow_affine (y G κ a : ℝ) (hy : y ≠ 0) :
    (-2 / y ^ 3) * (y * κ * (a * y ^ 2 - G)) = 2 * κ * (G / y ^ 2 - a) := by
  field_simp
  ring

/-- QCD-only ratio `R = y²/g₃²`: `d ln R ∝ (9/2) R − 1`, unique positive fixed point `R* = 2/9`. -/
theorem qcd_ratio_fixed (R : ℚ) : 9 / 2 * R - 1 = 0 ↔ R = 2 / 9 := by
  constructor <;> intro h <;> linarith

/-- Sensitivity exponent of `1/R` to its UV value in the QCD-only flow: `−c₃/b₃ − 1 = 8/7 − 1 = 1/7 > 0`. -/
theorem qcd_sensitivity_exponent : (-(8 : ℚ) / (-7)) - 1 = 1 / 7 ∧ (0 : ℚ) < 1 / 7 := by
  norm_num

/-- Convention screening: rescaling both a beta coefficient and a Yukawa coefficient by `k ≠ 0` leaves `c/b`. -/
theorem exp_ratio_invariant (b c k : ℚ) (hk : k ≠ 0) : (c * k) / (b * k) = c / b :=
  mul_div_mul_right c b hk

/-- An affine map `u ↦ S u + A` multiplies interval widths by `S`. -/
theorem affine_width (S A u0 u1 : ℝ) : (S * u1 + A) - (S * u0 + A) = S * (u1 - u0) := by
  ring

/-- For `0 < S < 1` a nonzero width strictly shrinks but never reaches zero: narrowing, not selection. -/
theorem affine_contracts (S u0 u1 : ℝ) (hS0 : 0 < S) (hS1 : S < 1) (h : u0 < u1) :
    0 < S * (u1 - u0) ∧ S * (u1 - u0) < u1 - u0 := by
  have hd : 0 < u1 - u0 := by linarith
  exact ⟨mul_pos hS0 hd, by nlinarith⟩

/-- SM one-loop exponents `−cᵢ/bᵢ` for `b = (41/6, −19/6, −7)`, `c = (17/12, 9/4, 8)`. -/
theorem sm_exponent_signs :
    -(8 : ℚ) / (-7) = 8 / 7 ∧ -(9 / 4 : ℚ) / (-19 / 6) = 27 / 38 ∧ -(17 / 12 : ℚ) / (41 / 6) = -17 / 82 := by
  norm_num

end PositiveGeometryEmergentSpaceTime.RgIr1
