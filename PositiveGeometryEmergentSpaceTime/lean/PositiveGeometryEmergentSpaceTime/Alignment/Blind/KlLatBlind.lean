/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-3 (2026-11-03) — BLIND second formalisation of KL-LAT / KL-LAT2 / KS-1 (algebra).
Written ONLY from the prose of prereg/KL-1-MR-1f-KS-1-prereg-2026-10-13.md (Theory),
prereg/KL-LAT-prereg-2026-10-13.md (Prediction), reviews/KL-LAT2-gate-2026-10-13.md (Theory gate),
reviews/KL-LAT-result-2026-10-13.md and reviews/KL-1-MR-1f-KS-1-result-2026-10-13.md, BEFORE opening
lean/PositiveGeometryEmergentSpaceTime/UnequalLS.lean, lean/PositiveGeometryEmergentSpaceTime/KLPhi.lean or their blueprint rows.
Prose claims: α_ρ(t) = ½ + α'(t − mπ²), α_K(u) = ½ + α'(u − mK²); "the dual zero line α_ρ(t)+α_K(u)=1
be exactly the hidden-zero line s = mπ²+mK²"; α' = 1/(2(mρ²−mπ²)); J=1: m_K*² = m_K² + (m_ρ² − m_π²);
J=2: m_K2*² = m_K² + 3(m_ρ² − m_π²); spacing; φ: m_φ² = 2m_K² + m_ρ² − 2m_π² ⇔ m_φ² − m_K*² = m_K*² − m_ρ².
Readings chosen here (blind): masses squared as field elements; πK on-shell s + t + u = 2(mπ² + mK²);
K*_J is the J-th recurrence: α_K(m_J²) = J. Not blinded: `poch3` (Pochhammer residue, form not in prose).
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace PositiveGeometryEmergentSpaceTime.Alignment.KlLatBlind

variable {K : Type*} [Field K] [CharZero K]

def aRho (ap pi2 t : K) : K := 1 / 2 + ap * (t - pi2)
def aK (ap K2 u : K) : K := 1 / 2 + ap * (u - K2)

/-- BLIND CLAIM (zero line): on shell, α_ρ(t) + α_K(u) = 1 ⇔ s = mπ² + mK² (α' ≠ 0). -/
theorem zero_line (ap pi2 K2 s t u : K) (hap : ap ≠ 0) (hon : s + t + u = 2 * (pi2 + K2)) :
    aRho ap pi2 t + aK ap K2 u = 1 ↔ s = pi2 + K2 := by
  unfold aRho aK
  have : 1 / 2 + ap * (t - pi2) + (1 / 2 + ap * (u - K2)) = 1 + ap * (pi2 + K2 - s) := by
    linear_combination ap * hon
  rw [this]; constructor
  · intro h; have : ap * (pi2 + K2 - s) = 0 := by linear_combination h
    have := (mul_eq_zero.mp this).resolve_left hap; linear_combination -this
  · intro h; rw [h]; ring

/-- BLIND FINDING (converse): for general linear trajectories a + α' t, b + α' u with common slope
α' ≠ 0, "dual zero line = hidden-zero line" on shell fixes ONLY the sum a + b = 1 − α'(mπ² + mK²);
the split between a and b is extra input (the ½-at-pseudoscalar rule). -/
theorem zero_line_conv (ap a b pi2 K2 : K) (hap : ap ≠ 0) :
    (∀ s t u : K, s + t + u = 2 * (pi2 + K2) → (a + ap * t + (b + ap * u) = 1 ↔ s = pi2 + K2))
      ↔ a + b = 1 - ap * (pi2 + K2) := by
  constructor
  · intro h
    have := (h (pi2 + K2) 0 (pi2 + K2) (by ring)).mpr rfl
    linear_combination this
  · intro hab s t u hon
    have : a + ap * t + (b + ap * u) = 1 + ap * (pi2 + K2 - s) := by
      linear_combination hab + ap * hon
    rw [this]; constructor
    · intro h; have : ap * (pi2 + K2 - s) = 0 := by linear_combination h
      have := (mul_eq_zero.mp this).resolve_left hap; linear_combination -this
    · intro h; rw [h]; ring

/-- Witness that the split is free: two different splits with the same sum both satisfy it. -/
theorem split_not_forced : ∃ a a' b b' : ℚ, a ≠ a' ∧ a + b = a' + b' := ⟨0, 1, 1, 0, by norm_num, by norm_num⟩

/-- The stated intercepts satisfy the sum rule. -/
theorem stated_sum (ap pi2 K2 : K) :
    (1 / 2 - ap * pi2) + (1 / 2 - ap * K2) = 1 - ap * (pi2 + K2) := by ring

/-- Slope from the ρ (α_ρ(mρ²) = 1). -/
theorem slope (pi2 rho2 : K) (h : rho2 - pi2 ≠ 0) : aRho (1 / (2 * (rho2 - pi2))) pi2 rho2 = 1 := by
  unfold aRho; field_simp; ring

/-- BLIND CLAIM (mass formula): α_K(m²) = J with α' = 1/(2(mρ²−mπ²)) ⇔ m² = mK² + (2J − 1)(mρ² − mπ²). -/
theorem mass_formula (pi2 rho2 K2 m2 J : K) (h : rho2 - pi2 ≠ 0) :
    aK (1 / (2 * (rho2 - pi2))) K2 m2 = J ↔ m2 = K2 + (2 * J - 1) * (rho2 - pi2) := by
  unfold aK; constructor
  · intro hJ; field_simp at hJ; linear_combination hJ
  · intro hm; rw [hm]; field_simp; ring

/-- J = 1 (AVW / kstar relation) and J = 2. -/
theorem kstar_relation (pi2 rho2 K2 : K) : K2 + (2 * 1 - 1) * (rho2 - pi2) = K2 + (rho2 - pi2) := by ring
theorem k2star (pi2 rho2 K2 : K) : K2 + (2 * 2 - 1) * (rho2 - pi2) = K2 + 3 * (rho2 - pi2) := by ring

/-- Spacing: m_{J+1}² − m_J² = 2(mρ² − mπ²) = 1/α'. -/
theorem spacing (pi2 rho2 K2 J : K) :
    (K2 + (2 * (J + 1) - 1) * (rho2 - pi2)) - (K2 + (2 * J - 1) * (rho2 - pi2)) = 2 * (rho2 - pi2) := by ring

/-- KL-LAT2 φ: α_φ(m_ηs²) = ½ with universal slope, at J = 1: m_φ² = m_ηs² + (mρ² − mπ²);
with GMOR m_ηs² = 2mK² − mπ²: m_φ² = 2mK² + mρ² − 2mπ². -/
theorem phi_relation (pi2 rho2 K2 : K) :
    (2 * K2 - pi2) + (2 * 1 - 1) * (rho2 - pi2) = 2 * K2 + rho2 - 2 * pi2 := by ring

/-- Equal spacing in squares: m_φ² − m_K*² = m_K*² − m_ρ². -/
theorem equal_spacing (pi2 rho2 K2 : K) :
    (2 * K2 + rho2 - 2 * pi2) - (K2 + (rho2 - pi2)) = (K2 + (rho2 - pi2)) - rho2 := by ring

/-- φ from K*: m_φ² = 2 m_K*² − m_ρ². -/
theorem phi_from_kstar (pi2 rho2 K2 : K) :
    2 * K2 + rho2 - 2 * pi2 = 2 * (K2 + (rho2 - pi2)) - rho2 := by ring

end PositiveGeometryEmergentSpaceTime.Alignment.KlLatBlind
