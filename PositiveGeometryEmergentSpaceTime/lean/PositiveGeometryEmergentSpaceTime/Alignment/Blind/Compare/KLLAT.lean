/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.UnequalLS
import PositiveGeometryEmergentSpaceTime.KLPhi
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.KlLatBlind

/-!
# ALIGNMENT BLIND-3 (2026-11-03) — Compare + sanity: KL-LAT / KL-LAT2 / KS-1 trajectory algebra

Blind prereg: e6e1666 (pushed before `PositiveGeometryEmergentSpaceTime.UnequalLS` / `PositiveGeometryEmergentSpaceTime.KLPhi` were opened).

VERDICTS:
* `UnequalLS.zero_line` + `zero_line_conv` vs blind `zero_line` (an iff): **EQUIV** (both directions).
* **Intercept derivation: OVERSTATED in the prose, not in the Lean.** The records say the intercepts
  "are fixed by demanding that the dual zero line … be exactly the hidden-zero line". Both original
  theorems *assume* the ½ intercepts and prove consistency. The blind `zero_line_conv` shows that the
  πK line alone fixes only the **sum** a + b = 1 − α'(mπ² + m_K²). The split is forced once the ρ
  trajectory is fixed, and the ρ intercept is itself forced by the equal-mass ππ hidden zero:
  `rho_intercept_from_pipi`, `k_intercept_from_rho` (new, below). So the claimed derivation is
  correct but needs the ππ step, which no original Lean theorem states. **MISSING-LEAN, now supplied.**
* `mass_formula`: **ORIG-STRONGER** (any slope a ≠ 0); the blind is the a = 1/(2(mρ² − mπ²)) instance
  (`blind_mass_of_orig`).
* `kstar_relation`, `spacing`, `KLPhi.phi_relation`, `equal_spacing`, `phi_from_kstar`: **EQUIV**
  (the original hypothesis forms follow from the blind mass formula; the identities match).
* `poch3`: not blinded (Γ recursion; independent of the hidden-zero content).
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.KLLAT
open PositiveGeometryEmergentSpaceTime.HadronKinematics

/-! ## Compare -/

theorem orig_zero_line_of_blind (a m_pi2 m_K2 s t u : ℝ) (ha : a ≠ 0)
    (hstu : s + t + u = stuSumPiK m_pi2 m_K2)
    (hz : (1/2 + a * (t - m_pi2)) + (1/2 + a * (u - m_K2)) = 1) : s = sigmaPiK m_pi2 m_K2 := by
  have := (KlLatBlind.zero_line a m_pi2 m_K2 s t u ha (by simpa [stuSumPiK, sigmaPiK] using hstu)).mp
    (by unfold KlLatBlind.aRho KlLatBlind.aK; exact hz)
  simpa [sigmaPiK] using this

theorem orig_zero_line_conv_of_blind (a m_pi2 m_K2 s t u : ℝ) (ha : a ≠ 0)
    (hstu : s + t + u = stuSumPiK m_pi2 m_K2) (hs : s = sigmaPiK m_pi2 m_K2) :
    (1/2 + a * (t - m_pi2)) + (1/2 + a * (u - m_K2)) = 1 := by
  have := (KlLatBlind.zero_line a m_pi2 m_K2 s t u ha (by simpa [stuSumPiK, sigmaPiK] using hstu)).mpr
    (by simpa [sigmaPiK] using hs)
  unfold KlLatBlind.aRho KlLatBlind.aK at this; exact this

theorem blind_zero_line_of_orig (ap pi2 K2 s t u : ℝ) (hap : ap ≠ 0) (hon : s + t + u = 2 * (pi2 + K2)) :
    KlLatBlind.aRho ap pi2 t + KlLatBlind.aK ap K2 u = 1 ↔ s = pi2 + K2 := by
  unfold KlLatBlind.aRho KlLatBlind.aK
  have hon' : s + t + u = stuSumPiK pi2 K2 := by simpa [stuSumPiK, sigmaPiK] using hon
  constructor
  · intro h; simpa [sigmaPiK] using UnequalLS.zero_line ap pi2 K2 s t u hap hon' h
  · intro h; exact UnequalLS.zero_line_conv ap pi2 K2 s t u hon' (by simpa [sigmaPiK] using h)

/-- NEW (the step the prose relies on): the equal-mass ππ hidden zero (line s = 2mπ²) with dual zero
α_ρ(t) + α_ρ(u) = 1 forces the ρ intercept: α_ρ(mπ²) = ½. -/
theorem rho_intercept_from_pipi (ap a pi2 : ℝ) (hap : ap ≠ 0)
    (h : ∀ s t u : ℝ, s + t + u = 2 * (pi2 + pi2) → (a + ap * t + (a + ap * u) = 1 ↔ s = pi2 + pi2)) :
    a + ap * pi2 = 1 / 2 := by
  have := (KlLatBlind.zero_line_conv ap a a pi2 pi2 hap).mp h
  linarith

/-- NEW: given the ρ trajectory (intercept from ππ), the πK hidden zero forces α_K(m_K²) = ½. -/
theorem k_intercept_from_rho (ap a b pi2 K2 : ℝ) (hap : ap ≠ 0) (hrho : a + ap * pi2 = 1 / 2)
    (h : ∀ s t u : ℝ, s + t + u = 2 * (pi2 + K2) → (a + ap * t + (b + ap * u) = 1 ↔ s = pi2 + K2)) :
    b + ap * K2 = 1 / 2 := by
  have := (KlLatBlind.zero_line_conv ap a b pi2 K2 hap).mp h
  linarith

/-- The original intercepts are exactly the ones these two steps force. -/
theorem orig_intercepts_forced (ap pi2 K2 : ℝ) :
    (1/2 - ap * pi2) + ap * pi2 = 1/2 ∧ (1/2 - ap * K2) + ap * K2 = 1/2 := by constructor <;> ring

theorem blind_mass_of_orig (pi2 rho2 K2 m2 J : ℝ) (h : rho2 - pi2 ≠ 0) :
    KlLatBlind.aK (1 / (2 * (rho2 - pi2))) K2 m2 = J ↔ m2 = K2 + (2 * J - 1) * (rho2 - pi2) := by
  have ha : (1 / (2 * (rho2 - pi2)) : ℝ) ≠ 0 := by simpa using h
  unfold KlLatBlind.aK
  rw [UnequalLS.mass_formula _ _ _ _ ha]
  have : (2 * J - 1) / (2 * (1 / (2 * (rho2 - pi2)))) = (2 * J - 1) * (rho2 - pi2) := by
    field_simp
  rw [this]

theorem orig_kstar_of_blind (m_pi2 m_rho2 m_K2 m2 : ℝ) (hne : m_rho2 - m_pi2 ≠ 0)
    (h : 1/2 + (1 / (2*(m_rho2 - m_pi2))) * (m2 - m_K2) = 1) : m2 - m_K2 = m_rho2 - m_pi2 := by
  have := (KlLatBlind.mass_formula m_pi2 m_rho2 m_K2 m2 1 hne).mp (by unfold KlLatBlind.aK; exact h)
  rw [this]; ring

theorem orig_spacing_tie (pi2 rho2 : ℝ) (h : rho2 - pi2 ≠ 0) :
    1 / (1 / (2 * (rho2 - pi2))) = 2 * (rho2 - pi2) := by field_simp

theorem orig_phi_of_blind (m_pi2 m_rho2 m_K2 m2 : ℝ) (hne : m_rho2 - m_pi2 ≠ 0)
    (h : 1/2 + (1 / (2*(m_rho2 - m_pi2))) * (m2 - (2*m_K2 - m_pi2)) = 1) :
    m2 = 2*m_K2 + m_rho2 - 2*m_pi2 := by
  have := (KlLatBlind.mass_formula m_pi2 m_rho2 (2*m_K2 - m_pi2) m2 1 hne).mp
    (by unfold KlLatBlind.aK; exact h)
  rw [this, ← KlLatBlind.phi_relation]

theorem equal_spacing_tie (m_pi2 m_rho2 m_K2 : ℝ) :
    (2*m_K2 + m_rho2 - 2*m_pi2) - (m_K2 + m_rho2 - m_pi2) = (m_K2 + m_rho2 - m_pi2) - m_rho2 :=
  KLPhi.equal_spacing m_pi2 m_rho2 m_K2 _ _ rfl rfl

/-! ## Sanity -/

/-- Known values (record inputs, GeV²): mρ² − mπ² = 1/(2·0.8598), m_K = 0.4957.
m_K*² ≈ 0.82725 (m ≈ 0.9095 GeV) and m_K2*² ≈ 1.99031 (m ≈ 1.4108 GeV). -/
theorem kstar_values :
    let d : ℝ := 1 / (2 * 0.8598); let K2 : ℝ := 0.4957 ^ 2
    (0.8272 < K2 + (2*1-1) * d ∧ K2 + (2*1-1) * d < 0.8273) ∧
    (1.9902 < K2 + (2*2-1) * d ∧ K2 + (2*2-1) * d < 1.9904) := by
  norm_num

/-- The masses quoted (0.9095, 1.4108 GeV) are the 4-d.p. square roots of those values. -/
theorem kstar_mass_values :
    let d : ℝ := 1 / (2 * 0.8598); let K2 : ℝ := 0.4957 ^ 2
    ((0.9095 : ℝ) ^ 2 < K2 + d ∧ K2 + d < 0.9096 ^ 2) ∧
    ((1.4107 : ℝ) ^ 2 < K2 + 3 * d ∧ K2 + 3 * d < 1.4108 ^ 2) := by norm_num

/-- Known values: the record's intercepts α_ρ(0) ≈ 0.483 and α_K(0) ≈ 0.289 (prereg line 9) follow
from α' = 0.8598 GeV⁻², mπ = 0.13957, m_K = 0.4957. -/
theorem intercept_values :
    (0.4832 : ℝ) < 1/2 - 0.8598 * 0.13957 ^ 2 ∧ 1/2 - 0.8598 * 0.13957 ^ 2 < (0.4834 : ℝ) ∧
    (0.2886 : ℝ) < 1/2 - 0.8598 * 0.4957 ^ 2 ∧ 1/2 - 0.8598 * 0.4957 ^ 2 < (0.2888 : ℝ) := by norm_num

/-- Planted wrong case: with the intercept sum but a *different split* the K* lands elsewhere
(a = 0.4, b chosen to keep the sum; ap = 1, mπ² = 0, m_K² = 1, so α_K(m²) = 1 at m² ≠ m_K² + (mρ² − mπ²)). -/
theorem planted_split : let ap : ℝ := 1; let a : ℝ := 0.4; let b : ℝ := 1 - ap * (0 + 1) - a
    a + b = 1 - ap * (0 + 1) ∧ b + ap * 1 ≠ 1 / 2 := by norm_num

/-- Planted wrong case: the zero line fails off-shell-line (s ≠ mπ² + m_K²). -/
theorem planted_off_line : KlLatBlind.aRho (1:ℝ) 0 0 + KlLatBlind.aK (1:ℝ) 1 (2 * (0 + 1) - 3 - 0) ≠ 1 := by
  unfold KlLatBlind.aRho KlLatBlind.aK; norm_num

/-- Non-vacuity: the hypothesis of `rho_intercept_from_pipi` is satisfiable (a = ½ − ap mπ²). -/
theorem nonvacuous_pipi : ∀ s t u : ℝ, s + t + u = 2 * (1 + 1) →
    ((1/2 - 1 * 1) + 1 * t + ((1/2 - 1 * 1) + 1 * u) = 1 ↔ s = 1 + 1) := by
  intro s t u h; constructor <;> intro h' <;> linarith

/-- Sanity for `poch3` (NOT blind: read in Phase 2): hypothesis satisfiable at z = 5, and the
identity reproduces Γ(5) = 4·3·2·Γ(2) = 24 (a known value). -/
theorem poch3_value : Real.Gamma 5 = 24 := by
  have hz : ∀ n : ℕ, (5:ℝ) - 3 ≠ -n := by
    intro n h; have : (0:ℝ) ≤ n := Nat.cast_nonneg n; linarith
  rw [UnequalLS.poch3 5 hz]
  have : (5:ℝ) - 3 = (1:ℕ) + 1 := by norm_num
  rw [this, Real.Gamma_nat_eq_factorial]; norm_num

/-- Planted wrong case: the Pochhammer factor with a sign error does not give Γ(5). -/
theorem poch3_planted : (5 - 1) * (5 - 2) * (5 + 3) * Real.Gamma ((1:ℕ) + 1) ≠ (24 : ℝ) := by
  rw [Real.Gamma_nat_eq_factorial]; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.KLLAT
