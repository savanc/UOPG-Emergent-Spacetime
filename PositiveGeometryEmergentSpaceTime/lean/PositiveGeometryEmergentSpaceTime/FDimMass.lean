/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.FDim

/-!
# F-DIM-MASS — the trunk LS amplitude with a massive pion fails D = 4 unitarity at level 1

Also known as: F-DIM-MASS, physical-mass gate check of the Lovelace–Shapiro trunk amplitude.
Units `α′ = 1`; `m2` is the external pion mass² in these units (`α′ m_π²`), `alpha0` the intercept.
Level-1 residue `(α₀ − k + kx)(α₀ + 1 − k + kx)`, `k = (2 − α₀ − 4m²)/2` (amplitude CITED, Bianchi–Consoli–Di Vecchia 2021);
its spin-0 coefficient in `D` dimensions is `k²/(D−1) + (α₀−k)(α₀+1−k)` (`FDim.quadratic_gegenbauer`).
* `weinberg_line_iff`: the LS zero line `α(s)+α(t)=1` equals the LO current-algebra line `s+t=2m²` iff `α₀ = ½ − m²`
  (the baseline P_a);
* `baseline_spin0_D4`: on that line the D = 4 spin-0 coefficient is `m²(m² − ½) < 0` for `0 < m² < ½` (GATE-FAIL of the
  trunk model at any non-zero pion mass);
* `lsCritDim_lt_four_iff`: `D_c(α₀) < 4 ↔ α₀ < ½`;
* `adlerZero_spin0_D4` (P_b, `α₀ = ½`): `16 m⁴/3 ≥ 0` (level 1 passes); `symmetric_spin0_D4` (P_c): negative for small m².
No axioms; no FRONTIER-AXIOM.
-/

namespace PositiveGeometryEmergentSpaceTime.FDimMass

/-- Level-1 kinematic shift `k = (2 − α₀ − 4m²)/2`. Also known as: `K/2`. -/
noncomputable def level1K (alpha0 m2 : ℝ) : ℝ := (2 - alpha0 - 4 * m2) / 2

/-- Level-1 spin-0 coefficient (σ-normalised) in `D` dimensions. Also known as: `B_{1,0}(α₀, m²,
  D)`. -/
noncomputable def level1Spin0 (alpha0 m2 D : ℝ) : ℝ :=
  level1K alpha0 m2 ^ 2 / (D - 1) + (alpha0 - level1K alpha0 m2) * (alpha0 + 1 - level1K alpha0 m2)

/-- The level-1 residue as a quadratic in `x` (feeds `FDim.quadratic_gegenbauer`). -/
theorem level1_residue_quadratic (alpha0 m2 x : ℝ) :
    (alpha0 - level1K alpha0 m2 + level1K alpha0 m2 * x) * (alpha0 + 1 - level1K alpha0 m2 + level1K alpha0 m2 * x)
      = level1K alpha0 m2 ^ 2 * x ^ 2
        + level1K alpha0 m2 * (2 * alpha0 + 1 - 2 * level1K alpha0 m2) * x
        + (alpha0 - level1K alpha0 m2) * (alpha0 + 1 - level1K alpha0 m2) := by ring

/-- The LS zero set `α(s) + α(t) = 1` coincides with the LO current-algebra zero line `s + t = 2m²`
  iff `α₀ = ½ − m²`. -/
theorem weinberg_line_iff (alpha0 m2 : ℝ) :
    (∀ s t : ℝ, (alpha0 + s) + (alpha0 + t) = 1 ↔ s + t = 2 * m2) ↔ alpha0 = 1 / 2 - m2 := by
  constructor
  · intro h
    have := (h m2 m2).2 (by ring)
    linarith
  · rintro rfl s t
    constructor <;> intro h <;> linarith

/-- Baseline (P_a): on the Adler line the D = 4 spin-0 coefficient equals `m²(m² − ½)`. -/
theorem baseline_spin0_D4 (m2 : ℝ) : level1Spin0 (1 / 2 - m2) m2 4 = m2 * (m2 - 1 / 2) := by
  unfold level1Spin0 level1K; ring

/-- GATE-FAIL of the trunk model: any pion mass `0 < m² < ½` makes the D = 4 level-1 spin-0
  coefficient negative. -/
theorem baseline_gate_fail {m2 : ℝ} (h0 : 0 < m2) (h1 : m2 < 1 / 2) : level1Spin0 (1 / 2 - m2) m2 4 < 0 := by
  rw [baseline_spin0_D4]; nlinarith

/-- Consistency with F-DIM: on the Adler line the level-1 spin-0 coefficient is `FDim.lsSpin0` up to the factor
`α₀/4·(…)` normalisation; here directly: `D_c(α₀) < 4 ↔ α₀ < ½` for `0 < α₀ < 2`. -/
theorem lsCritDim_lt_four_iff {alpha0 : ℝ} (h2 : alpha0 < 2) :
    PositiveGeometryEmergentSpaceTime.FDim.lsCritDim alpha0 < 4 ↔ alpha0 < 1 / 2 := by
  unfold PositiveGeometryEmergentSpaceTime.FDim.lsCritDim
  have h : 0 < 2 - alpha0 := by linarith
  rw [div_lt_iff₀ h]
  constructor <;> intro h' <;> linarith

/-- Fix P_b (Adler point at s = t = 0, `α₀ = ½`): the D = 4 level-1 spin-0 coefficient is `16 m⁴/3 ≥
  0`. -/
theorem adlerZero_spin0_D4 (m2 : ℝ) : level1Spin0 (1 / 2) m2 4 = 16 * m2 ^ 2 / 3 := by
  unfold level1Spin0 level1K; ring

/-- With the Adler point at `s = t = 0` (`α₀ = ½`), the D = 4 level-1 spin-0 coefficient is ≥ 0 for
  every `m²`. -/
theorem adlerZero_level1_pass (m2 : ℝ) : 0 ≤ level1Spin0 (1 / 2) m2 4 := by
  rw [adlerZero_spin0_D4]; positivity

/-- Fix P_c (Adler point at the symmetric point, `α₀ = ½ − 4m²/3`): D = 4 coefficient `(16m⁴/9 −
  2m²)/3`. -/
theorem symmetric_spin0_D4 (m2 : ℝ) :
    level1Spin0 (1 / 2 - 4 * m2 / 3) m2 4 = (16 * m2 ^ 2 / 9 - 2 * m2) / 3 := by
  unfold level1Spin0 level1K; ring

/-- With the Adler point at the symmetric point (`α₀ = ½ − 4m²/3`), the D = 4 level-1 spin-0
  coefficient is < 0 for `0 < m² < 9/8`. -/
theorem symmetric_level1_fail {m2 : ℝ} (h0 : 0 < m2) (h1 : m2 < 9 / 8) :
    level1Spin0 (1 / 2 - 4 * m2 / 3) m2 4 < 0 := by
  rw [symmetric_spin0_D4]; nlinarith

/-- Bundle (F-DIM-MASS): Weinberg-line uniqueness of the baseline; baseline fails D = 4 at any `0 < m² < ½`;
P_b passes level 1; P_c fails level 1. -/
theorem fdimmass_gate :
    (∀ alpha0 m2 : ℝ, (∀ s t : ℝ,
        (alpha0 + s) + (alpha0 + t) = 1 ↔ s + t = 2 * m2) ↔ alpha0 = 1 / 2 - m2) ∧
    (∀ m2 : ℝ, 0 < m2 → m2 < 1 / 2 → level1Spin0 (1 / 2 - m2) m2 4 < 0) ∧
    (∀ m2 : ℝ, 0 ≤ level1Spin0 (1 / 2) m2 4) ∧
    (∀ m2 : ℝ, 0 < m2 → m2 < 9 / 8 → level1Spin0 (1 / 2 - 4 * m2 / 3) m2 4 < 0) :=
  ⟨weinberg_line_iff, fun _ h0 h1 => baseline_gate_fail h0 h1, adlerZero_level1_pass,
    fun _ h0 h1 => symmetric_level1_fail h0 h1⟩

end PositiveGeometryEmergentSpaceTime.FDimMass
