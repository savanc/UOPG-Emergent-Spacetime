/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-!
# STRUCT-1: SM hypercharges as the unique anomaly-free assignment (2026-10-15)
One generation of left-handed Weyl fields Q (3,2,yQ), uᶜ (3̄,1,yu), dᶜ (3̄,1,yd), L (1,2,yL), eᶜ (1,1,ye),
optionally νᶜ (1,1,yn). Perturbative anomaly conditions over ℚ: SU(3)²U(1), SU(2)²U(1), grav²U(1), U(1)³.
Results: (C1) without νᶜ and with yQ ≠ 0 the charges are yQ·(−4,2,−3,6) or yQ·(2,−4,−3,6) (uᶜ↔dᶜ), i.e. the SM
up to normalisation; (C2) yQ = 0 admits the extra family yL = ye = 0, yd = −yu; (C3) with νᶜ, B−L is an extra
solution, so the anomaly conditions alone do not fix hypercharge. Known results (Geng–Marshak, Minahan–Ramond–Warner).
No positive-geometry input is used.
-/
namespace PositiveGeometryEmergentSpaceTime.STRUCT1

/-- Anomaly conditions without νᶜ. -/
def ACC (yQ yu yd yL ye : ℚ) : Prop :=
  2 * yQ + yu + yd = 0 ∧ 3 * yQ + yL = 0 ∧
  6 * yQ + 3 * yu + 3 * yd + 2 * yL + ye = 0 ∧
  6 * yQ ^ 3 + 3 * yu ^ 3 + 3 * yd ^ 3 + 2 * yL ^ 3 + ye ^ 3 = 0

/-- Anomaly conditions with a right-handed neutrino νᶜ (charge yn). -/
def ACCnu (yQ yu yd yL ye yn : ℚ) : Prop :=
  2 * yQ + yu + yd = 0 ∧ 3 * yQ + yL = 0 ∧
  6 * yQ + 3 * yu + 3 * yd + 2 * yL + ye + yn = 0 ∧
  6 * yQ ^ 3 + 3 * yu ^ 3 + 3 * yd ^ 3 + 2 * yL ^ 3 + ye ^ 3 + yn ^ 3 = 0

/-- The cubic condition factorises on the linear solution space: −18·yQ·(yu + 4yQ)(yu − 2yQ). -/
theorem cubic_factor (yQ yu : ℚ) :
    6 * yQ ^ 3 + 3 * yu ^ 3 + 3 * (-2 * yQ - yu) ^ 3 + 2 * (-3 * yQ) ^ 3 + (6 * yQ) ^ 3
      = -18 * yQ * (yu + 4 * yQ) * (yu - 2 * yQ) := by ring

/-- C1: uniqueness up to normalisation and uᶜ↔dᶜ (no νᶜ, yQ ≠ 0). -/
theorem hypercharge_unique {yQ yu yd yL ye : ℚ} (h : ACC yQ yu yd yL ye) (hQ : yQ ≠ 0) :
    (yu = -4 * yQ ∧ yd = 2 * yQ ∧ yL = -3 * yQ ∧ ye = 6 * yQ) ∨
    (yu = 2 * yQ ∧ yd = -4 * yQ ∧ yL = -3 * yQ ∧ ye = 6 * yQ) := by
  obtain ⟨h3, h2, hg, hc⟩ := h
  have hd : yd = -2 * yQ - yu := by linarith
  have hL : yL = -3 * yQ := by linarith
  have he : ye = 6 * yQ := by subst hd; subst hL; linarith
  subst hd hL he
  have hf := cubic_factor yQ yu
  rw [hc] at hf
  have : (yu + 4 * yQ) * (yu - 2 * yQ) = 0 := by
    have h18 : (-18 * yQ) ≠ 0 := by intro h; apply hQ; linarith
    have : -18 * yQ * ((yu + 4 * yQ) * (yu - 2 * yQ)) = 0 := by linarith [hf]
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h h18
    · exact h
  rcases mul_eq_zero.mp this with h | h
  · left; refine ⟨by linarith, by linarith, rfl, rfl⟩
  · right; refine ⟨by linarith, by linarith, rfl, rfl⟩

/-- The SM assignment (yQ = 1/6 normalisation) is anomaly-free (non-vacuity witness for C1). -/
theorem sm_is_anomaly_free : ACC (1/6) (-2/3) (1/3) (-1/2) 1 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- C2: without the hypothesis yQ ≠ 0 there is an extra family (yQ = yL = ye = 0, yd = −yu). -/
theorem yQ_zero_family (t : ℚ) : ACC 0 t (-t) 0 0 := by
  refine ⟨by ring, by ring, by ring, by ring⟩

/-- C2': that family is not of SM form for t ≠ 0 (so `hQ` is genuinely needed). -/
theorem yQ_zero_family_not_sm {t : ℚ} (ht : t ≠ 0) :
    ¬ ((t = -4 * 0 ∧ -t = 2 * 0) ∨ (t = 2 * 0 ∧ -t = -4 * 0)) := by
  rintro (⟨h, _⟩ | ⟨h, _⟩) <;> exact ht (by linarith)

/-- C3: with νᶜ, B−L is anomaly-free. -/
theorem bminusl_anomaly_free : ACCnu (1/3) (-1/3) (-1/3) (-1) 1 1 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- The SM with neutral νᶜ is also anomaly-free. -/
theorem sm_nu_anomaly_free : ACCnu (1/6) (-2/3) (1/3) (-1/2) 1 0 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- C3 (exclusion): with νᶜ the conditions do not fix hypercharge — B−L is not proportional to the SM charges
(in either uᶜ↔dᶜ labelling). -/
theorem not_unique_with_nu :
    ¬ ∃ c : ℚ, ((1:ℚ)/3 = c * (1/6) ∧ (-1:ℚ)/3 = c * (-2/3) ∧ (-1:ℚ)/3 = c * (1/3)) ∨
              ((1:ℚ)/3 = c * (1/6) ∧ (-1:ℚ)/3 = c * (1/3) ∧ (-1:ℚ)/3 = c * (-2/3)) := by
  rintro ⟨c, ⟨h1, h2, _⟩ | ⟨h1, _, h3⟩⟩ <;> linarith

end PositiveGeometryEmergentSpaceTime.STRUCT1
