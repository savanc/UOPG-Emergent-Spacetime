/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — BLIND second formalisation of RG-IR-1 (Lean part).
Written from Paper II §"RG-IR-1" ("Lean proves the affine structure of the flow in seven
theorems (u_flow_affine, affine_width, qcd_sensitivity_exponent and four more); this certifies
the algebra, not a physics claim") and the prereg's physics set-up, BEFORE reading
lean/PositiveGeometryEmergentSpaceTime/RgIr1.lean. Partly NOT blind: the prereg's Lean plan (§5) names the targets and
two numeric values (−8/(−7) − 1 = 1/7; −c3/b3 = 8/7, …), which were read.

Physics reading of "affine structure of the flow": at one loop
  dy/dt = y (a y² − G(t)) / k,  k = 16π²,  G = Σ cᵢ gᵢ²(t),
and u = 1/y² obeys the LINEAR equation du/dt = (2 G(t) u − 2a)/k, so u(t) is affine in u(0).
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.RgIr1Blind

/-- BLIND CLAIM C1 (calculus form): the substitution u = 1/y² linearises the one-loop
top-Yukawa flow. -/
def ClaimLinearises : Prop :=
  ∀ (y G : ℝ → ℝ) (a k t : ℝ), k ≠ 0 → y t ≠ 0 →
    HasDerivAt y (y t * (a * y t ^ 2 - G t) / k) t →
    HasDerivAt (fun s => 1 / y s ^ 2) ((2 * G t * (1 / y t ^ 2) - 2 * a) / k) t

/-- BLIND CLAIM C2 (affine dependence): two solutions of the same linear flow differ by a
solution of the homogeneous flow (so the time-t map u(0) ↦ u(t) is affine). -/
def ClaimAffine : Prop :=
  ∀ (u₁ u₂ α β : ℝ → ℝ) (t : ℝ) (d₁ d₂ : ℝ),
    HasDerivAt u₁ d₁ t → HasDerivAt u₂ d₂ t →
    d₁ = α t * u₁ t + β t → d₂ = α t * u₂ t + β t →
    HasDerivAt (fun s => u₁ s - u₂ s) (α t * (u₁ t - u₂ t)) t

/-- BLIND CLAIM C3 (width): an affine map with slope A > 0 sends an interval of width w to
one of width A·w. -/
def ClaimWidth : Prop :=
  ∀ A B lo hi : ℝ, 0 < A → lo ≤ hi → (A * hi + B) - (A * lo + B) = A * (hi - lo)

/-- BLIND CLAIM C4 (QCD sensitivity exponent, SM one-loop c₃ = 8, b₃ = −7): positive. -/
def ClaimQcdExponent : Prop := (-(8 : ℚ) / (-7)) - 1 = 1 / 7 ∧ 0 < (-(8 : ℚ) / (-7)) - 1

end PositiveGeometryEmergentSpaceTime.Alignment.RgIr1Blind
