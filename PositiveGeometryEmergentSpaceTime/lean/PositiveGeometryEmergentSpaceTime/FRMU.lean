/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT2
import PositiveGeometryEmergentSpaceTime.Separation

/-!
# FR-MU (frontier rung 1) — `μ_n/μ_p` from a spin-flavour-symmetric `N_c`-quark construction

Also known as: magnetic-moment ratio, SU(6) quark-model ratio, Beg–Lee–Pais −2/3.

FRONTIER-CONSTRUCTION. Colour is antisymmetric, so the spin×flavour wavefunction is totally symmetric. The
symmetric-irrep matrix elements enter as **explicit hypotheses** (`SymIrrepME`, no `axiom`). The locked checker
`sims/frmu/frmu_checker.py` verifies them by brute force for `N_c = 1, 3, 5, 7`. The charges are those of the
STRUCT-2 anomaly branch (`Separation.chargeUp/chargeDown`, lepton doublet `yL = −1/2`).
Verdict of the rung: NUMEROLOGY (in band, not significant after trials).
-/

namespace PositiveGeometryEmergentSpaceTime.FRMU

open PositiveGeometryEmergentSpaceTime.Separation

/-- Symmetric-irrep nucleon matrix elements (hypotheses of the construction).
`sigP`, `sigN` = ⟨Σ σ_z⟩ in p↑, n↑; `gtP`, `gtN` = ⟨Σ σ_z τ_3⟩.
Also known as: ⟨2S_z⟩, ⟨4G^{33}⟩ (contracted SU(4) / large-N_c spin-flavour). -/
structure SymIrrepME (_N_c : ℚ) where
  /-- ⟨Σσ_z⟩ in the proton. -/
  sigP : ℚ
  /-- ⟨Σσ_z⟩ in the neutron. -/
  sigN : ℚ
  /-- ⟨Σσ_zτ_3⟩ in the proton. -/
  gtP : ℚ
  /-- ⟨Σσ_zτ_3⟩ in the neutron. -/
  gtN : ℚ

/-- The construction's hypotheses: symmetric-irrep values (explicit hypothesis, not an axiom; checked by brute force
in `sims/frmu`). -/
def SymIrrepME.Valid {N_c : ℚ} (M : SymIrrepME N_c) : Prop :=
  M.sigP = 1 ∧ M.sigN = 1 ∧ M.gtP = (N_c + 2) / 3 ∧ M.gtN = -(N_c + 2) / 3

/-- Proton magnetic moment in quark magnetons: `Q̄ ⟨Σσ⟩ + (ΔQ/2) ⟨Σστ_3⟩`. Also known as: μ_p. -/
def muProton {N_c : ℚ} (M : SymIrrepME N_c) (Qu Qd : ℚ) : ℚ := (Qu + Qd) / 2 * M.sigP + (Qu - Qd) / 2 * M.gtP

/-- Neutron magnetic moment in quark magnetons. Also known as: μ_n. -/
def muNeutron {N_c : ℚ} (M : SymIrrepME N_c) (Qu Qd : ℚ) : ℚ := (Qu + Qd) / 2 * M.sigN + (Qu - Qd) / 2 * M.gtN

/-- Planted: `N_c = 3`, SM charges ⇒ `μ_p = 1`, `μ_n = −2/3` (textbook SU(6)). -/
theorem planted_sm (M : SymIrrepME 3) (hM : M.Valid) :
    muProton M (2 / 3) (-1 / 3) = 1 ∧ muNeutron M (2 / 3) (-1 / 3) = -2 / 3 := by
  unfold muProton muNeutron; obtain ⟨h1, h2', h3', h4'⟩ := hM; rw [h1, h2', h3',
      h4']; constructor <;> norm_num

/-- Main: with STRUCT-2 ACC (`yL = −1/2`) and `N_c > 0`,
`μ_n/μ_p = (3 − N_c(N_c+2)) / (3 + N_c(N_c+2))`. -/
theorem ratio_acc {N_c yQ yu yd ye : ℚ} (hN : 0 < N_c) (h : STRUCT2.ACCN N_c yQ yu yd (-1 / 2) ye)
    (M : SymIrrepME N_c) (hM : M.Valid) :
    muNeutron M (chargeUp yQ) (chargeDown yQ) / muProton M (chargeUp yQ) (chargeDown yQ) =
      (3 - N_c * (N_c + 2)) / (3 + N_c * (N_c + 2)) := by
  obtain ⟨_, h2, _, _⟩ := h
  have hy : yQ = 1 / (2 * N_c) := by field_simp; linarith
  unfold muProton muNeutron chargeUp chargeDown
  obtain ⟨h1, h2', h3', h4'⟩ := hM; rw [h1, h2', h3', h4', hy]
  have hN0 : N_c ≠ 0 := hN.ne'
  have hp : ((1 / (2 * N_c) + 1 / 2) + (1 / (2 * N_c) - 1 / 2)) / 2 * 1 +
      ((1 / (2 * N_c) + 1 / 2) - (1 / (2 * N_c) - 1 / 2)) / 2 * ((N_c + 2) / 3) =
      (3 + N_c * (N_c + 2)) / (6 * N_c) := by field_simp; ring
  have hn : ((1 / (2 * N_c) + 1 / 2) + (1 / (2 * N_c) - 1 / 2)) / 2 * 1 +
      ((1 / (2 * N_c) + 1 / 2) - (1 / (2 * N_c) - 1 / 2)) / 2 * (-(N_c + 2) / 3) =
      (3 - N_c * (N_c + 2)) / (6 * N_c) := by field_simp; ring
  rw [hp, hn]
  have h3 : (0 : ℚ) < 3 + N_c * (N_c + 2) := by positivity
  field_simp

/-- Prediction at `N_c = 3`: `μ_n/μ_p = −2/3`. -/
theorem ratio_three : ((3 : ℚ) - 3 * (3 + 2)) / (3 + 3 * (3 + 2)) = -2 / 3 := by norm_num

/-- Large-`N_c` structure: `R(N_c) + 1 = 6 / (3 + N_c(N_c+2))`, so `R → −1` and `R > −1`. -/
theorem ratio_plus_one {N_c : ℚ} (hN : 0 < N_c) :
    (3 - N_c * (N_c + 2)) / (3 + N_c * (N_c + 2)) + 1 = 6 / (3 + N_c * (N_c + 2)) := by
  have h3 : (0 : ℚ) < 3 + N_c * (N_c + 2) := by positivity
  field_simp; ring

/-- With N_c-independent SM charges (2/3, −1/3) the same construction gives `−(N_c+1)/(N_c+3)`. -/
theorem ratio_fixed_charges {N_c : ℚ} (hN : 0 < N_c) (M : SymIrrepME N_c) (hM : M.Valid) :
    muNeutron M (2 / 3) (-1 / 3) / muProton M (2 / 3) (-1 / 3) = -(N_c + 1) / (N_c + 3) := by
  unfold muProton muNeutron; obtain ⟨h1, h2', h3', h4'⟩ := hM; rw [h1, h2', h3', h4']
  have h3 : (0 : ℚ) < N_c + 3 := by linarith
  field_simp; ring

/-- The anomaly-consistent and the fixed-charge constructions agree (for `N_c > 0`) **only at `N_c =
  3`**. -/
theorem acc_fixed_agree_iff {N_c : ℚ} (hN : 0 < N_c) :
    (3 - N_c * (N_c + 2)) / (3 + N_c * (N_c + 2)) = -(N_c + 1) / (N_c + 3) ↔ N_c = 3 := by
  have h3 : (0 : ℚ) < 3 + N_c * (N_c + 2) := by positivity
  have h4 : (0 : ℚ) < N_c + 3 := by linarith
  rw [div_eq_div_iff h3.ne' h4.ne']
  constructor
  · intro h
    have hq : (N_c - 3) * (N_c + 2) = 0 := by nlinarith
    rcases mul_eq_zero.1 hq with h5 | h5
    · linarith
    · linarith
  · rintro rfl; norm_num

end PositiveGeometryEmergentSpaceTime.FRMU
