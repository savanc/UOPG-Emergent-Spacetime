/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.LECRatio
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.M3Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: M3 (BE14 L3/L2 vs the zero-parameter band)

Blind: inputs are the paper's rounded numbers, central `-3.79`, `σ = 0.31`, band `[-2.6, -1.4]`;
proves the gap is exactly `119/31 ≈ 3.839σ` and rounds to 3.84.
Original (`LECRatio.be14_*`): inputs are the raw BE14 values `L3/L2 = -3.07/0.81 = -307/81` with
first-order propagated `σ² = R²((0.20/3.07)² + (0.04/0.81)²)`; proves only `gap > 3.8σ`.

VERDICT: **DIFFERENT** (different inputs; neither statement implies the other formally).
Reconciliation proved here: the original's `R` and `σ` round to the blind's `-3.79` and `0.31`;
the original's exact gap lies in `[3.835σ, 3.845σ)`, so the paper's "3.84σ" is true under both
input conventions; and the blind's numbers also give the original's `> 3.8σ` form.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.M3

open PositiveGeometryEmergentSpaceTime.Alignment

/-- The original central value rounds to the blind's `-3.79`. -/
theorem orig_central_rounds : (-3795 / 1000 : ℚ) < -307 / 81 ∧ (-307 / 81 : ℚ) ≤ -3785 / 1000 := by
  norm_num

/-- The original propagated σ rounds to the blind's `0.31`: `0.305² ≤ σ² < 0.315²`. -/
theorem orig_sigma_rounds :
    let R : ℚ := -307 / 81
    let σ2 : ℚ := R ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2)
    (305 / 1000) ^ 2 ≤ σ2 ∧ σ2 < (315 / 1000) ^ 2 := by
  norm_num

/-- The original data's exact n-σ lies in `[3.835, 3.845)` (squared form), i.e. rounds to 3.84. -/
theorem orig_nsigma_rounds :
    let R : ℚ := -307 / 81
    let σ2 : ℚ := R ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2)
    (3835 / 1000) ^ 2 * σ2 ≤ (-13 / 5 - R) ^ 2 ∧ (-13 / 5 - R) ^ 2 < (3845 / 1000) ^ 2 * σ2 := by
  norm_num

/-- Blind numbers ⇒ the original's `> 3.8σ` statement shape. -/
theorem blind_gives_orig_shape :
    (19 / 5 : ℚ) ^ 2 * M3Blind.sigma ^ 2 < (M3Blind.bandLo - M3Blind.central) ^ 2 := by
  unfold M3Blind.sigma M3Blind.bandLo M3Blind.central; norm_num

/-- Both readings agree on the headline: original `be14_gap` and blind `nsigma_rounds`. -/
theorem both_headlines :
    ((let R : ℚ := -307 / 81
      let σ2 : ℚ := R ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2)
      (19 / 5) ^ 2 * σ2 < (-13 / 5 - R) ^ 2)) ∧
    (3835 / 1000 ≤ M3Blind.nsigma ∧ M3Blind.nsigma < 3845 / 1000) :=
  ⟨PositiveGeometryEmergentSpaceTime.LECRatio.be14_gap, M3Blind.nsigma_rounds⟩

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.M3
