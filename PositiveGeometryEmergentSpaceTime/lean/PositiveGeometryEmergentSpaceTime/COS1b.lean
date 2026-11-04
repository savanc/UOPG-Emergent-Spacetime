/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-! COS-1b (2026-10-13, AutoResearch): for null boundary momenta p = (|k|, k) (mostly plus),
p_i·p_j = -|k_i||k_j| + ⟪k_i,k_j⟫ ≤ 0, so the c = 0 NLSM wavefunction numerator p₁·p₃+p₂·p₄ has no
zero in the open physical region; any zero there needs the basis-dependent c E² term. -/
namespace PositiveGeometryEmergentSpaceTime.COS1b

variable {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
/-- Minkowski product of two null boundary momenta.

Also known as: COS1b.mdot, Minkowski product of null boundary momenta p=(|k|,k).
-/
noncomputable def nullBoundaryDot (a b : V) : ℝ := -(‖a‖ * ‖b‖) + inner ℝ a b
/-- The Minkowski product of two null boundary momenta `(|a|, a)`, `(|b|, b)` is ≤ 0
  (Cauchy–Schwarz). -/
theorem nullBoundaryDot_nonpos (a b : V) : nullBoundaryDot a b ≤ 0 := by
  unfold nullBoundaryDot; have := real_inner_le_norm a b; linarith
/-- The c = 0 numerator `p₁·p₃ + p₂·p₄` built from null boundary momenta is ≤ 0, so it can vanish
  only when both terms vanish. -/
theorem numerator_nonpos (k1 k2 k3 k4 : V) : nullBoundaryDot k1 k3 + nullBoundaryDot k2 k4 ≤ 0 :=
  add_nonpos (nullBoundaryDot_nonpos k1 k3) (nullBoundaryDot_nonpos k2 k4)
/-- A zero of N_c = N₀ + c E² with E > 0 forces c = -N₀/E² ≥ 0. -/
theorem zero_forces_c_nonneg {N0 c E : ℝ} (hN : N0 ≤ 0) (hE : 0 < E) (hz : N0 + c * E ^ 2 = 0) :
    0 ≤ c := by
  have hE2 : 0 < E ^ 2 := by positivity
  by_contra h; push Not at h; nlinarith
end PositiveGeometryEmergentSpaceTime.COS1b
