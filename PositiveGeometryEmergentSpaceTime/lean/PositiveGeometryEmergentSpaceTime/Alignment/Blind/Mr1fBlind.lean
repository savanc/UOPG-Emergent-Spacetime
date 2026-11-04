/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-4 (2026-11-03) — BLIND formalisation of the MR-1f width formula.
Written ONLY from the prose of prereg/KL-1-MR-1f-KS-1-prereg-2026-10-13.md (Theory; Predictions;
"Width formula") and reviews/KL-1-MR-1f-KS-1-result-2026-10-13.md, BEFORE opening
lean/PositiveGeometryEmergentSpaceTime/UnequalLS.lean, lean/PositiveGeometryEmergentSpaceTime/DecayZeroNoGo.lean, scripts/kl1_theory.py or any MR-1f
blueprint row. (UnequalLS.poch3 had been read in BLIND-3 Phase 2; it is not used here.)
Prose: A = β Γ(1−α_ρ(t)) Γ(1−α_K(u)) / Γ(1−α_ρ(t)−α_K(u)); α_ρ(t) = ½ + α'(t − mπ²),
α_K(u) = ½ + α'(u − mK²); "Γ_J ∝ G_J q_J / ((2J+1) m_J²), G_J = P_J-Legendre coefficient of the
u-pole residue, t = −2q²(1−cos θ)"; R_J = Γ_J/Γ_1; V2 (LS masses): R2 = 0.8949, R3 = 0.5776,
R4 = 0.3649.
Readings chosen here (blind):
* u-pole at α_K(u) = J; residue in α_K of Γ(1−α_K) is (−1)^J/(J−1)! (standard, NOT formalised),
  and Γ(1−a)/Γ(1−a−J) = (−1)^J (a)_J (`gamma_ratio`, PROVED), so the residue is (a)_J/(J−1)!
  with a = α_ρ(t) (`res`); the overall α' and sign are common to all J and drop out of R_J.
* q_J² = Källén(m_J², mK², mπ²)/(4 m_J²); m_J² from α_K(m_J²) = J.
* G_J = coefficient of P_J (the top Legendre coefficient) of the degree-J residue polynomial in cos θ.
* Numerical inputs (not stated in the prose, chosen blind as standard values): mπ = 0.13957,
  mρ = 0.77526 (α' = 1/(2(mρ²−mπ²)) = 0.8598), mK = 0.4957 GeV (prose).
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Mr1fBlind

open Real

noncomputable section

/-- ρ trajectory with the hidden-zero intercept. -/
def alphaRho (ap mpi2 t : ℝ) : ℝ := 1 / 2 + ap * (t - mpi2)
/-- K* trajectory with the hidden-zero intercept. -/
def alphaK (ap mK2 u : ℝ) : ℝ := 1 / 2 + ap * (u - mK2)

/-- The Gamma-ratio step of the residue: Γ(1−a) = (−1)^J (a)_J Γ(1−a−J) for a not a non-positive
integer. -/
theorem gamma_ratio (a : ℝ) (ha : ∀ n : ℕ, a + n ≠ 0) (J : ℕ) :
    Gamma (1 - a) = (-1) ^ J * (∏ k ∈ Finset.range J, (a + k)) * Gamma (1 - a - J) := by
  induction J with
  | zero => simp
  | succ J ih =>
    have hs : Gamma (1 - a - J) = (-a - J) * Gamma (1 - a - ((J : ℝ) + 1)) := by
      rw [show 1 - a - (J : ℝ) = (1 - a - ((J : ℝ) + 1)) + 1 by ring,
        Real.Gamma_add_one (by intro h; apply ha J; linarith)]
      ring_nf
    rw [ih, hs, Finset.prod_range_succ]; push_cast; ring

/-- u-pole residue at α_K = J as a function of a = α_ρ(t): (a)_J / (J−1)!. -/
noncomputable def res (J : ℕ) (a : ℝ) : ℝ := (∏ k ∈ Finset.range J, (a + k)) / ((J - 1).factorial : ℝ)

/-- Kinematics: t = −2q²(1 − x), x = cos θ. -/
def tOf (q2 x : ℝ) : ℝ := -2 * q2 * (1 - x)

/-- α_ρ(t) is affine in x = cos θ with slope B = 2α'q². -/
theorem alphaRho_tOf (ap mpi2 q2 x : ℝ) :
    alphaRho ap mpi2 (tOf q2 x) = (1 / 2 - ap * mpi2 - 2 * ap * q2) + (2 * ap * q2) * x := by
  unfold alphaRho tOf; ring

/-- Legendre polynomials P_0..P_4. -/
def P : ℕ → ℝ → ℝ
  | 0, _ => 1
  | 1, x => x
  | 2, x => (3 * x ^ 2 - 1) / 2
  | 3, x => (5 * x ^ 3 - 3 * x) / 2
  | 4, x => (35 * x ^ 4 - 30 * x ^ 2 + 3) / 8
  | _, _ => 0

/-- Closed form of the top Legendre coefficient: G_J = B^J 2^J (J!)² / ((J−1)! (2J)!). -/
noncomputable def Gtop (J : ℕ) (B : ℝ) : ℝ :=
  B ^ J * 2 ^ J * ((J.factorial : ℝ)) ^ 2 / (((J - 1).factorial : ℝ) * ((2 * J).factorial : ℝ))

theorem Gtop_vals (B : ℝ) : Gtop 1 B = B ∧ Gtop 2 B = 2 * B ^ 2 / 3 ∧ Gtop 3 B = B ^ 3 / 5 ∧
    Gtop 4 B = 4 * B ^ 4 / 105 := by
  simp only [Gtop, Nat.factorial]; norm_num; refine ⟨?_, ?_, ?_⟩ <;> ring

/-- BLIND CLAIM (J = 1): Legendre decomposition of the residue; G_1 = Gtop 1 B. -/
theorem legendre_J1 (A B x : ℝ) : res 1 (A + B * x) = A * P 0 x + Gtop 1 B * P 1 x := by
  rw [(Gtop_vals B).1]; simp [res, P]

/-- BLIND CLAIM (J = 2). -/
theorem legendre_J2 (A B x : ℝ) :
    res 2 (A + B * x) = (3 * A ^ 2 + 3 * A + B ^ 2) / 3 * P 0 x + B * (2 * A + 1) * P 1 x
      + Gtop 2 B * P 2 x := by
  rw [(Gtop_vals B).2.1]; simp [res, P, Finset.prod_range_succ]; ring

/-- BLIND CLAIM (J = 3). -/
theorem legendre_J3 (A B x : ℝ) :
    res 3 (A + B * x) = (A + 1) * (A ^ 2 + 2 * A + B ^ 2) / 2 * P 0 x
      + B * (15 * A ^ 2 + 30 * A + 3 * B ^ 2 + 10) / 10 * P 1 x + B ^ 2 * (A + 1) * P 2 x
      + Gtop 3 B * P 3 x := by
  rw [(Gtop_vals B).2.2.1]; simp [res, P, Finset.prod_range_succ]; ring

/-- BLIND CLAIM (J = 4). -/
theorem legendre_J4 (A B x : ℝ) :
    res 4 (A + B * x) =
      (15 * A ^ 4 + 90 * A ^ 3 + 30 * A ^ 2 * B ^ 2 + 165 * A ^ 2 + 90 * A * B ^ 2 + 90 * A
        + 3 * B ^ 4 + 55 * B ^ 2) / 90 * P 0 x
      + B * (2 * A + 3) * (5 * A ^ 2 + 15 * A + 3 * B ^ 2 + 5) / 15 * P 1 x
      + B ^ 2 * (42 * A ^ 2 + 126 * A + 6 * B ^ 2 + 77) / 63 * P 2 x
      + 2 * B ^ 3 * (2 * A + 3) / 15 * P 3 x + Gtop 4 B * P 4 x := by
  rw [(Gtop_vals B).2.2.2]; simp [res, P, Finset.prod_range_succ]; ring

/-- Pole position: α_K(m_J²) = J. -/
noncomputable def m2J (ap mK2 : ℝ) (J : ℕ) : ℝ := mK2 + ((J : ℝ) - 1 / 2) / ap

theorem alphaK_m2J (ap mK2 : ℝ) (hap : ap ≠ 0) (J : ℕ) : alphaK ap mK2 (m2J ap mK2 J) = J := by
  unfold alphaK m2J; field_simp; ring

/-- CM momentum squared in the Kπ channel. -/
def q2 (m2 mK mpi : ℝ) : ℝ := (m2 - (mK + mpi) ^ 2) * (m2 - (mK - mpi) ^ 2) / (4 * m2)

/-- Width (up to a J-independent constant): Γ_J = G_J q_J / ((2J+1) m_J²), with B = 2α'q_J². -/
noncomputable def width (ap mK mpi : ℝ) (J : ℕ) : ℝ :=
  Gtop J (2 * ap * q2 (m2J ap (mK ^ 2) J) mK mpi) * Real.sqrt (q2 (m2J ap (mK ^ 2) J) mK mpi)
    / ((2 * (J : ℝ) + 1) * m2J ap (mK ^ 2) J)

/-- Width ratio R_J = Γ_J / Γ_1. -/
noncomputable def ratio (ap mK mpi : ℝ) (J : ℕ) : ℝ := width ap mK mpi J / width ap mK mpi 1

/-- Universal slope from the ρ: α' = 1/(2(mρ² − mπ²)). -/
noncomputable def apOf (mpi mrho : ℝ) : ℝ := 1 / (2 * (mrho ^ 2 - mpi ^ 2))

end

end PositiveGeometryEmergentSpaceTime.Alignment.Mr1fBlind
