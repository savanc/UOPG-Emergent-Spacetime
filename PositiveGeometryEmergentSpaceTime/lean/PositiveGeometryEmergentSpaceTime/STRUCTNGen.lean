/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT3

/-!
# STRUCT-NGEN sharpen (2026-10-20): which consistency conditions bound `N_gen`, and do any force 3?

Also known as: STRUCT-NGEN, N_gen sharpen. Builds on `PositiveGeometryEmergentSpaceTime.STRUCT3` (`b0SU3`, `b0SU2`, `af_SU3_iff`, `af_SU2_iff`).
* `sm_core_window`, `sm_core_not_forced`: unconditional SM consistency (anomalies blind; AF of SU(3) and SU(2)) with
  `N ≥ 1` gives `1 ≤ N ≤ 5`; `N = 1, 2, 4, 5` pass, so 3 is not forced.
* `bz_two_loop_iff`: no two-loop Banks–Zaks zero in QCD (`b₁ = 102 − 38/3·n_f > 0`, `n_f = 2N`) iff `N ≤ 4`.
* `triality_sum`, `triality_iff`, `triality_window`, `triality_su3_only_not_forced`: baryon-triality Z₉ condition
  (García-Etxebarria–Montero 1808.00009 §4.2, CITED): per-generation residue −3, so `9 ∣ 3N ↔ 3 ∣ N`; with AF of SU(2)
  this gives exactly `N = 3`, with AF of SU(3) only `{3, 6}` (CONDITIONAL on gauging baryon triality).
* `z16_no_nuc_iff`, `z16_no_nuc_window_empty`: Spin-Z₄ (1808.00009 §4.3, CITED) without νᶜ needs `16 ∣ 15N ↔ 16 ∣ N`.
* `rival331_anomaly_iff`, `rival331_window`: rival SU(3)_c×SU(3)_L×U(1)_X (Pisano–Pleitez hep-ph/9206242; Frampton
  1992, CITED): `#3 = #3̄` gives `3 ∣ N`; AF of QCD with `n_f = 3N` gives `N ≤ 5`; together exactly `N = 3`.
No axioms.
-/

namespace PositiveGeometryEmergentSpaceTime.STRUCTNGen

open PositiveGeometryEmergentSpaceTime.STRUCT3

/-- Unconditional SM consistency window (anomalies are `N`-blind, `STRUCT3.acc_ngen_blind`,
  `witten_ngen_blind`). -/
theorem sm_core_window (N : ℕ) :
    (1 ≤ N ∧ 0 < b0SU3 N ∧ 0 < b0SU2 N) ↔ (1 ≤ N ∧ N ≤ 5) := by
  rw [af_SU3_iff, af_SU2_iff]; omega

/-- 3 is not forced: 1, 2, 4 and 5 pass the same unconditional set. -/
theorem sm_core_not_forced :
    ∀ N ∈ ({1, 2, 4, 5} : Finset ℕ), 1 ≤ N ∧ 0 < b0SU3 N ∧ 0 < b0SU2 N := by
  intro N hN
  rw [sm_core_window]
  simp only [Finset.mem_insert, Finset.mem_singleton] at hN
  omega

/-- Two-loop QCD coefficient with `n_f = 2N` Dirac flavours. Also known as: b1 QCD, β₁. -/
def b1QCD (N : ℕ) : ℚ := 102 - 38 / 3 * (2 * N)

/-- `b₁QCD N > 0` iff `N ≤ 4`. -/
theorem bz_two_loop_iff (N : ℕ) : 0 < b1QCD N ↔ N ≤ 4 := by
  unfold b1QCD
  constructor
  · intro h
    by_contra hc
    push Not at hc
    have : (5 : ℚ) ≤ N := by exact_mod_cast hc
    linarith
  · intro h
    have : (N : ℚ) ≤ 4 := by exact_mod_cast h
    linarith

/-- Baryon-triality residues (1808.00009 Table 1, row "Triality") weighted by SU(3)×SU(2) multiplicity:
`Ū`: −1 × 3, `Q`: 0 × 6, `D̄`: 1 × 3, `L`: −1 × 2, `Ē`: −1 × 1. -/
theorem triality_sum : (-1 : ℤ) * 3 + 0 * 6 + 1 * 3 + (-1) * 2 + (-1) * 1 = -3 := by norm_num

/-- `9 ∣ −3N` iff `3 ∣ N`. -/
theorem triality_iff (N : ℕ) : (9 : ℤ) ∣ (-3) * N ↔ 3 ∣ N := by
  constructor
  · intro h
    have h' : (9 : ℤ) ∣ 3 * N := by
      rw [show (3 : ℤ) * N = -((-3) * N) by ring]; exact dvd_neg.mpr h
    obtain ⟨k, hk⟩ := h'
    have : (N : ℤ) = 3 * k := by linarith
    exact_mod_cast (show (3 : ℤ) ∣ N from ⟨k, this⟩)
  · rintro ⟨k, rfl⟩
    exact ⟨-k, by push_cast; ring⟩

/-- Conditional forcing: gauged baryon triality + AF of SU(2) + `N ≥ 1` ⇒ `N = 3`. -/
theorem triality_window (N : ℕ) : (1 ≤ N ∧ N ≤ 5 ∧ 3 ∣ N) ↔ N = 3 := by
  constructor
  · rintro ⟨h1, h5, ⟨k, rfl⟩⟩; omega
  · rintro rfl; exact ⟨by norm_num, by norm_num, ⟨1, rfl⟩⟩

/-- With AF of SU(3) only (`N ≤ 8`) baryon triality allows `N = 6` too. -/
theorem triality_su3_only_not_forced : 1 ≤ 6 ∧ 0 < b0SU3 6 ∧ 3 ∣ 6 :=
  ⟨by norm_num, (af_SU3_iff 6).mpr (by norm_num), ⟨2, rfl⟩⟩

/-- Spin-Z₄ condition without νᶜ (15 Weyl fermions per generation). -/
theorem z16_no_nuc_iff (N : ℕ) : 16 ∣ 15 * N ↔ 16 ∣ N := by
  constructor
  · intro h
    have hc : Nat.Coprime 16 15 := by norm_num
    exact hc.dvd_of_dvd_mul_left h
  · intro h; exact Dvd.dvd.mul_left h 15

/-- For `1 ≤ N ≤ 5`, `16 ∤ 15N`. -/
theorem z16_no_nuc_window_empty (N : ℕ) (h1 : 1 ≤ N) (h5 : N ≤ 5) : ¬ 16 ∣ 15 * N := by
  rw [z16_no_nuc_iff]
  rintro ⟨k, rfl⟩
  omega

/-- Rival 3-3-1 SU(3)_L anomaly: `N` lepton triplets + `3a` quark triplets = `3(N − a)`
  antitriplets. -/
def anomaly331 (N : ℕ) : Prop := ∃ a, a ≤ N ∧ N + 3 * a = 3 * (N - a)

/-- The 3-3-1 SU(3)_L anomaly condition `anomaly331 N` holds iff `3 ∣ N`. -/
theorem rival331_anomaly_iff (N : ℕ) : anomaly331 N ↔ 3 ∣ N := by
  constructor
  · rintro ⟨a, ha, h⟩; exact ⟨a, by omega⟩
  · rintro ⟨k, rfl⟩; exact ⟨k, by omega, by omega⟩

/-- QCD one-loop coefficient in the rival with `n_f = 3N`. -/
def b0QCD331 (N : ℕ) : ℚ := 11 - 2 / 3 * (3 * N)

/-- Rival 3-3-1: consistency (SU(3)_L anomaly + QCD AF + `N ≥ 1`) singles out exactly `N = 3`. -/
theorem rival331_window (N : ℕ) : (1 ≤ N ∧ anomaly331 N ∧ 0 < b0QCD331 N) ↔ N = 3 := by
  rw [rival331_anomaly_iff]
  have hAF : 0 < b0QCD331 N ↔ N ≤ 5 := by
    unfold b0QCD331
    constructor
    · intro h; by_contra hc; push Not at hc
      have : (6 : ℚ) ≤ N := by exact_mod_cast hc
      linarith
    · intro h; have : (N : ℚ) ≤ 5 := by exact_mod_cast h
      linarith
  rw [hAF]
  constructor
  · rintro ⟨h1, ⟨k, rfl⟩, h5⟩; omega
  · rintro rfl; exact ⟨by norm_num, ⟨1, rfl⟩, by norm_num⟩

/-- Bundle (STRUCT-NGEN): SM unconditional set does not force 3 (1 passes); conditional triality and the 3-3-1 rival
each single out 3. -/
theorem structngen_summary :
    (1 ≤ 1 ∧ 0 < b0SU3 1 ∧ 0 < b0SU2 1) ∧ (∀ N : ℕ, (1 ≤ N ∧ N ≤ 5 ∧ 3 ∣ N) ↔ N = 3) ∧
    (∀ N : ℕ, (1 ≤ N ∧ anomaly331 N ∧ 0 < b0QCD331 N) ↔ N = 3) :=
  ⟨sm_core_not_forced 1 (by simp), triality_window, rival331_window⟩

end PositiveGeometryEmergentSpaceTime.STRUCTNGen
