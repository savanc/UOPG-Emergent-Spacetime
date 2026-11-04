/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-4 Phase 2 (2026-11-03): MR-1f width formula — Compare + sanity.
Originals opened AFTER the prereg push d8004bd: lean/PositiveGeometryEmergentSpaceTime/UnequalLS.lean (`poch3`),
scripts/kl1_theory.py (`resid`, `width`, `pred`), scripts/kl1_theory_output.txt.
Original Lean coverage of the width formula: only `UnequalLS.poch3` (the J = 3 Gamma-ratio instance).
The Legendre projection, G_J, the kinematics and the ratios exist only in the script (SIMULATED).
NOT imported by `PositiveGeometryEmergentSpaceTime`.
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.UnequalLS
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Mr1fBlind

set_option linter.unusedSectionVars false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR1F

open Real PositiveGeometryEmergentSpaceTime.Alignment.Mr1fBlind

noncomputable section

/-! ## Compare: Gamma-ratio step -/

/-- Minimal-hypothesis Gamma ratio: only a + k ≠ 0 for k < J is needed. -/
theorem gamma_ratio_min (a : ℝ) (J : ℕ) (ha : ∀ k < J, a + k ≠ 0) :
    Gamma (1 - a) = (-1) ^ J * (∏ k ∈ Finset.range J, (a + k)) * Gamma (1 - a - J) := by
  induction J with
  | zero => simp
  | succ J ih =>
    have hs : Gamma (1 - a - J) = (-a - J) * Gamma (1 - a - ((J : ℝ) + 1)) := by
      rw [show 1 - a - (J : ℝ) = (1 - a - ((J : ℝ) + 1)) + 1 by ring,
        Real.Gamma_add_one (by intro h; apply ha J (Nat.lt_succ_self J); linarith)]
      ring_nf
    rw [ih (fun k hk => ha k (Nat.lt_succ_of_lt hk)), hs, Finset.prod_range_succ]; push_cast; ring

/-- The blind statement follows from the minimal one. -/
theorem blind_of_min (a : ℝ) (ha : ∀ n : ℕ, a + n ≠ 0) (J : ℕ) :
    Gamma (1 - a) = (-1) ^ J * (∏ k ∈ Finset.range J, (a + k)) * Gamma (1 - a - J) :=
  gamma_ratio_min a J (fun k _ => ha k)

/-- The ORIGINAL `UnequalLS.poch3` is the J = 3 instance of the minimal blind statement
(z = 1 − a), under the original's own hypothesis. -/
theorem orig_poch3_of_blind (z : ℝ) (hz : ∀ n : ℕ, z - 3 ≠ -n) :
    Real.Gamma z = (z - 1) * (z - 2) * (z - 3) * Real.Gamma (z - 3) := by
  have h := gamma_ratio_min (1 - z) 3 (by
    intro k hk
    interval_cases k
    · intro h; exact hz 2 (by push_cast at h ⊢; linarith)
    · intro h; exact hz 1 (by push_cast at h ⊢; linarith)
    · intro h; exact hz 0 (by push_cast at h ⊢; linarith))
  simp only [Finset.prod_range_succ, Finset.prod_range_zero] at h
  rw [show (1 : ℝ) - (1 - z) = z by ring] at h
  push_cast at h
  rw [h]; ring

/-- And conversely the original gives the blind J = 3 instance (same core). -/
theorem blind3_of_orig (a : ℝ) (ha : ∀ n : ℕ, (1 - a) - 3 ≠ -n) :
    Gamma (1 - a) = (-1) ^ 3 * (∏ k ∈ Finset.range 3, (a + k)) * Gamma (1 - a - (3 : ℕ)) := by
  rw [PositiveGeometryEmergentSpaceTime.UnequalLS.poch3 (1 - a) ha]
  simp only [Finset.prod_range_succ, Finset.prod_range_zero]; push_cast; ring

/-! ## Compare: script residue sign (finding) -/

/-- The script's residue is the coefficient of 1/(J − α_K): lead = (−1)^(J−1)/(J−1)!, times
∏(−a−k) = (−1)^J (a)_J, i.e. −(a)_J/(J−1)! = −res J a. Uniform in J, so every R_J is unchanged;
the residue in (u − m_J²) is +res J a / α′ > 0. -/
theorem script_residue_eq (J : ℕ) (a : ℝ) :
    ((-1) ^ (J + 1) / ((J - 1).factorial : ℝ)) * (∏ k ∈ Finset.range J, (-a - k)) = -res J a := by
  unfold res
  have : (∏ k ∈ Finset.range J, (-a - (k : ℝ))) = (-1) ^ J * ∏ k ∈ Finset.range J, (a + k) := by
    rw [← Finset.card_range J, ← Finset.prod_const, Finset.card_range, ← Finset.prod_mul_distrib]
    exact Finset.prod_congr rfl (fun k _ => by ring)
  rw [this, pow_succ]
  have h1 : ((-1 : ℝ) ^ J) * (-1) ^ J = 1 := by rw [← mul_pow]; norm_num
  calc (-1 : ℝ) ^ J * -1 / ((J - 1).factorial : ℝ) * ((-1) ^ J * ∏ k ∈ Finset.range J, (a + k))
      = -(((-1 : ℝ) ^ J * (-1) ^ J) * (∏ k ∈ Finset.range J, (a + k)) / ((J - 1).factorial : ℝ)) := by
        ring
    _ = _ := by rw [h1, one_mul]

/-! ## Sanity -/

/-- Width squared removes the square root. -/
theorem width_sq (ap mK mpi : ℝ) (J : ℕ) (hQ : 0 ≤ q2 (m2J ap (mK ^ 2) J) mK mpi) :
    width ap mK mpi J ^ 2 =
      Gtop J (2 * ap * q2 (m2J ap (mK ^ 2) J) mK mpi) ^ 2 * q2 (m2J ap (mK ^ 2) J) mK mpi
        / ((2 * (J : ℝ) + 1) * m2J ap (mK ^ 2) J) ^ 2 := by
  unfold width; rw [div_pow, mul_pow, Real.sq_sqrt hQ]

theorem width_pos (ap mK mpi : ℝ) (J : ℕ) (hap : 0 < ap) (hQ : 0 < q2 (m2J ap (mK ^ 2) J) mK mpi)
    (hm : 0 < m2J ap (mK ^ 2) J) : 0 < width ap mK mpi J := by
  unfold width Gtop
  have hs := Real.sqrt_pos.mpr hQ
  have hB : 0 < 2 * ap * q2 (m2J ap (mK ^ 2) J) mK mpi := by positivity
  positivity

/-- Blind numerical inputs (GeV): mπ, mρ, mK. -/
def mpi0 : ℝ := 13957 / 100000
def mrho0 : ℝ := 77526 / 100000
def mK0 : ℝ := 4957 / 10000
def ap0 : ℝ := apOf mpi0 mrho0

theorem ap0_pos : 0 < ap0 := by norm_num [ap0, apOf, mpi0, mrho0]

/-- NON-VACUITY: all four poles lie above the Kπ threshold (q² > 0, m² > 0). -/
theorem q2_pos (J : ℕ) (hJ : 1 ≤ J ∧ J ≤ 4) :
    0 < q2 (m2J ap0 (mK0 ^ 2) J) mK0 mpi0 ∧ 0 < m2J ap0 (mK0 ^ 2) J := by
  obtain ⟨h1, h4⟩ := hJ
  interval_cases J <;> norm_num [q2, m2J, ap0, apOf, mpi0, mrho0, mK0]

theorem sq_bounds {R lo hi : ℝ} (hR : 0 < R) (hlo : 0 ≤ lo) (hhi : 0 < hi)
    (h1 : lo ^ 2 < R ^ 2) (h2 : R ^ 2 < hi ^ 2) : lo < R ∧ R < hi := by
  constructor <;> nlinarith

theorem ratio_sq (J : ℕ) (hJ : 1 ≤ J ∧ J ≤ 4) :
    ratio ap0 mK0 mpi0 J ^ 2 =
      (Gtop J (2 * ap0 * q2 (m2J ap0 (mK0 ^ 2) J) mK0 mpi0) ^ 2 * q2 (m2J ap0 (mK0 ^ 2) J) mK0 mpi0
        / ((2 * (J : ℝ) + 1) * m2J ap0 (mK0 ^ 2) J) ^ 2) /
      (Gtop 1 (2 * ap0 * q2 (m2J ap0 (mK0 ^ 2) 1) mK0 mpi0) ^ 2 * q2 (m2J ap0 (mK0 ^ 2) 1) mK0 mpi0
        / ((2 * ((1 : ℕ) : ℝ) + 1) * m2J ap0 (mK0 ^ 2) 1) ^ 2) := by
  unfold ratio
  rw [div_pow, width_sq _ _ _ _ (q2_pos J hJ).1.le,
    width_sq _ _ _ _ (q2_pos 1 ⟨le_refl _, by norm_num⟩).1.le]

theorem ratio_pos (J : ℕ) (hJ : 1 ≤ J ∧ J ≤ 4) : 0 < ratio ap0 mK0 mpi0 J := by
  unfold ratio
  exact div_pos (width_pos _ _ _ _ ap0_pos (q2_pos J hJ).1 (q2_pos J hJ).2)
    (width_pos _ _ _ _ ap0_pos (q2_pos 1 ⟨le_refl _, by norm_num⟩).1
      (q2_pos 1 ⟨le_refl _, by norm_num⟩).2)

/-- KNOWN VALUE / TIE to SIMULATED V2 (prereg table 0.8949; kl1_theory_output.txt 0.89489):
R2 ∈ (0.89485, 0.89495). -/
theorem R2_val : 0.89485 < ratio ap0 mK0 mpi0 2 ∧ ratio ap0 mK0 mpi0 2 < 0.89495 := by
  apply sq_bounds (ratio_pos 2 ⟨by norm_num, by norm_num⟩) (by norm_num) (by norm_num) <;>
  · rw [ratio_sq 2 ⟨by norm_num, by norm_num⟩]
    simp only [Gtop, Nat.factorial]
    norm_num [q2, m2J, ap0, apOf, mpi0, mrho0, mK0]

/-- TIE: R3 ∈ (0.57755, 0.57765) (prose 0.5776; script 0.57764). -/
theorem R3_val : 0.57755 < ratio ap0 mK0 mpi0 3 ∧ ratio ap0 mK0 mpi0 3 < 0.57765 := by
  apply sq_bounds (ratio_pos 3 ⟨by norm_num, by norm_num⟩) (by norm_num) (by norm_num) <;>
  · rw [ratio_sq 3 ⟨by norm_num, by norm_num⟩]
    simp only [Gtop, Nat.factorial]
    norm_num [q2, m2J, ap0, apOf, mpi0, mrho0, mK0]

/-- TIE: R4 ∈ (0.36485, 0.36495) (prose 0.3649; script 0.36488). -/
theorem R4_val : 0.36485 < ratio ap0 mK0 mpi0 4 ∧ ratio ap0 mK0 mpi0 4 < 0.36495 := by
  apply sq_bounds (ratio_pos 4 ⟨by norm_num, by norm_num⟩) (by norm_num) (by norm_num) <;>
  · rw [ratio_sq 4 ⟨by norm_num, by norm_num⟩]
    simp only [Gtop, Nat.factorial]
    norm_num [q2, m2J, ap0, apOf, mpi0, mrho0, mK0]

/-- PLANTED WRONG READING: G_J := x^J coefficient B^J/(J−1)! (instead of the P_J coefficient).
Its R2² exceeds 1.3², far outside the V2 band (the planted case is rejected, as it should be). -/
def Glead (J : ℕ) (B : ℝ) : ℝ := B ^ J / ((J - 1).factorial : ℝ)

theorem planted_xJ_R2 :
    (1.3 : ℝ) ^ 2 <
      (Glead 2 (2 * ap0 * q2 (m2J ap0 (mK0 ^ 2) 2) mK0 mpi0) ^ 2 * q2 (m2J ap0 (mK0 ^ 2) 2) mK0 mpi0
        / ((2 * (2 : ℝ) + 1) * m2J ap0 (mK0 ^ 2) 2) ^ 2) /
      (Glead 1 (2 * ap0 * q2 (m2J ap0 (mK0 ^ 2) 1) mK0 mpi0) ^ 2 * q2 (m2J ap0 (mK0 ^ 2) 1) mK0 mpi0
        / ((2 * (1 : ℝ) + 1) * m2J ap0 (mK0 ^ 2) 1) ^ 2) := by
  simp only [Glead, Nat.factorial]
  norm_num [q2, m2J, ap0, apOf, mpi0, mrho0, mK0]

/-- PLANTED: dropping 1/(J−1)! doubles R3 (2! = 2), and the band (0.57755, 0.57765) rejects it. -/
theorem planted_nofact_R3 (r : ℝ) (hr : 0.57755 < r ∧ r < 0.57765) :
    ¬ (0.57755 < 2 * r ∧ 2 * r < 0.57765) := by
  intro h; linarith [h.2, hr.1]

/-- NON-VACUITY of `gamma_ratio`: its hypothesis holds at a = ½ (the ρ intercept at mπ²). -/
theorem gamma_hyp_nonvacuous : ∀ n : ℕ, (1 / 2 : ℝ) + n ≠ 0 := by
  intro n; positivity

/-- TIE to the KS-1 mass algebra: the K* pole sits at α_K = 1. -/
theorem pole_J1 : alphaK ap0 (mK0 ^ 2) (m2J ap0 (mK0 ^ 2) 1) = 1 := by
  have := alphaK_m2J ap0 (mK0 ^ 2) ap0_pos.ne' 1; simpa using this

end

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR1F
