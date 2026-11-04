/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT1
/-!
# STRUCT-1b: restoring hypercharge uniqueness with νᶜ (2026-10-15)
With νᶜ, perturbative anomaly cancellation leaves a B−L family (STRUCT1.not_unique_with_nu).
(M) a Majorana mass for νᶜ (yn = 0) restores uniqueness: SM up to normalisation and uᶜ↔dᶜ;
(D) Dirac Yukawas with one Higgs doublet do NOT: a one-parameter family (containing SM and B−L) survives;
(MY) Yukawas + Majorana alone (no cubic condition needed) give the SM with yH = 3yQ.
Charge conditions are CITED conventions (definitions). No positive-geometry input.
-/
namespace PositiveGeometryEmergentSpaceTime.STRUCT1b
open PositiveGeometryEmergentSpaceTime.STRUCT1

/-- Gauge invariance of the four Yukawa couplings Q H uᶜ, Q H* dᶜ, L H* eᶜ, L H νᶜ. -/
def Yuk (yQ yu yd yL ye yn yH : ℚ) : Prop :=
  yQ + yH + yu = 0 ∧ yQ - yH + yd = 0 ∧ yL - yH + ye = 0 ∧ yL + yH + yn = 0

/-- M: anomaly-free with νᶜ, Majorana-allowed (yn = 0), yQ ≠ 0 ⇒ SM up to normalisation and uᶜ↔dᶜ. -/
theorem majorana_unique {yQ yu yd yL ye yn : ℚ} (h : ACCnu yQ yu yd yL ye yn) (hn : yn = 0)
    (hQ : yQ ≠ 0) :
    (yu = -4 * yQ ∧ yd = 2 * yQ ∧ yL = -3 * yQ ∧ ye = 6 * yQ) ∨
    (yu = 2 * yQ ∧ yd = -4 * yQ ∧ yL = -3 * yQ ∧ ye = 6 * yQ) := by
  subst hn
  obtain ⟨h1, h2, h3, h4⟩ := h
  exact hypercharge_unique ⟨h1, h2, by linarith, by linarith⟩ hQ

/-- D: for every t the family (1, t, −t−2, −3, 2−t, t+4; yH = −1−t) is anomaly-free with all Dirac
  Yukawas. -/
theorem dirac_family (t : ℚ) :
    ACCnu 1 t (-t - 2) (-3) (2 - t) (t + 4) ∧ Yuk 1 t (-t - 2) (-3) (2 - t) (t + 4) (-1 - t) := by
  refine ⟨⟨by ring, by ring, by ring, by ring⟩, by ring, by ring, by ring, by ring⟩

/-- D (exclusion): the Dirac family contains both the SM (t = −4) and B−L (t = −1, scaled by 3), so ACC + Dirac
Yukawas do not fix hypercharge. -/
theorem dirac_not_unique :
    (ACCnu 1 (-4) 2 (-3) 6 0 ∧ Yuk 1 (-4) 2 (-3) 6 0 3) ∧
    (ACCnu 1 (-1) (-1) (-3) 3 3 ∧ Yuk 1 (-1) (-1) (-3) 3 3 0) ∧ ((-4 : ℚ) ≠ -1) := by
  refine ⟨?_, ?_, by norm_num⟩
  · have := dirac_family (-4); norm_num at this ⊢; exact this
  · have := dirac_family (-1); norm_num at this ⊢; exact this

/-- MY: the four Yukawa conditions + Majorana (yn = 0) + the linear SU(2)²U(1) condition alone (no SU(3)²U(1),
gravitational or cubic condition) ⇒ SM charges relative to yQ, with yH = 3yQ. -/
theorem yukawa_majorana {yQ yu yd yL ye yn yH : ℚ} (hy : Yuk yQ yu yd yL ye yn yH) (hn : yn = 0)
    (hL : 3 * yQ + yL = 0) :
    yH = 3 * yQ ∧ yu = -4 * yQ ∧ yd = 2 * yQ ∧ ye = 6 * yQ := by
  obtain ⟨a, b, c, d⟩ := hy
  subst hn
  refine ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- Witness (non-vacuity of M's hypotheses): the SM with a neutral νᶜ satisfies them. -/
theorem witness_majorana : ACCnu (1/6) (-2/3) (1/3) (-1/2) 1 0 := sm_nu_anomaly_free

end PositiveGeometryEmergentSpaceTime.STRUCT1b
