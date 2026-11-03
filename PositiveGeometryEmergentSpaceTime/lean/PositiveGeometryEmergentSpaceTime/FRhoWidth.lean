/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.FScatLen

/-!
# F-RHOWIDTH — the ρ coupling of the Lovelace–Shapiro amplitude with Weinberg normalisation vs KSRF

Also known as: F-RHOWIDTH, LS ρ-residue vs Kawarabayashi–Suzuki–Riazuddin–Fayyazuddin (KSRF).
* `isoT1`: `T¹ = A(t,s,u) − A(u,t,s)`; for a dual amplitude with symmetric `V`, `T¹ = 2λ(V(s,t) − V(s,u))`.
* Residue: `(1 − α_s)·V(s,t) = Γ(2 − α_s)Γ(1−α_t)/Γ(1−α_s−α_t)`, whose value at `α_s = 1` is `−α_t`
  (the limit/continuity step is CITED, not proved here). Hence near the ρ pole `T¹ ≈ 2g²(t−u)/(m_ρ² − s)` with
  `g² = −λ = 1/(2πα′F²)` (N1 normalisation, F-SCATLEN).
* P_a (`α′ = 1/(2(m_ρ² − m_π²))`): `g²_LS = (m_ρ² − m_π²)/(πF²)`; KSRF `g² = m_ρ²/(2F²)`;
  `g²_LS / g²_KSRF = (2/π)(1 − m_π²/m_ρ²) < 2/π < 1`: **the LS residue does NOT reproduce KSRF**.
No axioms.
-/

namespace PositiveGeometryEmergentSpaceTime.FRhoWidth

open PositiveGeometryEmergentSpaceTime.FScatLen

/-- Isospin-1 combination `T¹ = A(t,s,u) − A(u,t,s)`. -/
def isoT1 (A : ℝ → ℝ → ℝ → ℝ) (s t u : ℝ) : ℝ := A t s u - A u t s

/-- For a dual amplitude with symmetric `V`, the isospin-1 combination is `T¹ = 2λ (V(s,t) −
  V(s,u))`. -/
theorem dual_T1 (V : ℝ → ℝ → ℝ) (hV : ∀ a b, V a b = V b a) (lam s t u : ℝ) :
    isoT1 (dualAmp V lam) s t u = 2 * lam * (V s t - V s u) := by
  unfold isoT1 dualAmp; rw [hV t s, hV u t, hV u s]; ring

/-- Pole-stripped LS block: `(1 − a)·Γ(1−a)Γ(1−b)/Γ(1−a−b) = Γ(2−a)Γ(1−b)/Γ(1−a−b)` for `a ≠ 1`. -/
theorem stripped_block {a b : ℝ} (ha : 1 - a ≠ 0) :
    (1 - a) * (Real.Gamma (1 - a) * Real.Gamma (1 - b) * (Real.Gamma (1 - a - b))⁻¹)
      = Real.Gamma (2 - a) * Real.Gamma (1 - b) * (Real.Gamma (1 - a - b))⁻¹ := by
  have h : Real.Gamma (2 - a) = (1 - a) * Real.Gamma (1 - a) := by
    rw [show (2 : ℝ) - a = (1 - a) + 1 by ring, Real.Gamma_add_one ha]
  rw [h]; ring

/-- Value of the pole-stripped block at `a = 1`: `Γ(1)Γ(1−b)/Γ(−b) = −b` (for `b ≠ 0` and `Γ(−b) ≠
  0`). -/
theorem stripped_at_pole {b : ℝ} (hb : -b ≠ 0) (hG : Real.Gamma (-b) ≠ 0) :
    Real.Gamma (2 - 1) * Real.Gamma (1 - b) * (Real.Gamma (1 - 1 - b))⁻¹ = -b := by
  have h1 : Real.Gamma (1 - b) = (-b) * Real.Gamma (-b) := by
    rw [show (1 : ℝ) - b = -b + 1 by ring, Real.Gamma_add_one hb]
  rw [show (2 : ℝ) - 1 = 1 by norm_num, Real.Gamma_one, show (1 : ℝ) - 1 - b = -b by ring, h1]
  field_simp

/-- ρ-pole residue of `T¹`: with `V ≈ −α_t/(α′(m_ρ²−s))`, `2λ(V(s,t)−V(s,u)) = 2(−λ)(t−u)/(m_ρ²−s)`,
  i.e. `g² = −λ`. -/
theorem T1_pole_form {ap lam mr2 s t u a0 : ℝ} (hap : ap ≠ 0) (hs : mr2 - s ≠ 0) :
    2 * lam * (-(a0 + ap * t) / (ap * (mr2 - s)) - -(a0 + ap * u) / (ap * (mr2 - s)))
      = 2 * (-lam) * (t - u) / (mr2 - s) := by
  field_simp; ring

/-- LS ρ coupling with N1: `g² = −λ = 1/(2πα′F²)`. Also known as: `g²_{ρππ}` (LS). -/
noncomputable def gLS2 (ap F2 : ℝ) : ℝ := 1 / (2 * Real.pi * ap * F2)

/-- KSRF coupling `g² = m_ρ²/(2F²)`. Also known as: KSRF relation. -/
noncomputable def gKSRF2 (mr2 F2 : ℝ) : ℝ := mr2 / (2 * F2)

/-- Unfolded form: `gLS2 α' F² = −(−1/(2π α' F²))`, i.e. `g² = −λ` with the N1 normalisation. -/
theorem gLS2_eq_neg_lambda (ap F2 : ℝ) : gLS2 ap F2 = -(-1 / (2 * Real.pi * ap * F2)) := by
  unfold gLS2; ring

/-- P_a: `g²_LS = (m_ρ² − m_π²)/(πF²)`. -/
theorem gLS2_Pa {mr2 mp2 F2 : ℝ} (h : mr2 - mp2 ≠ 0) :
    gLS2 (1 / (2 * (mr2 - mp2))) F2 = (mr2 - mp2) / (Real.pi * F2) := by
  unfold gLS2; field_simp

/-- `g²_LS / g²_KSRF = (2/π)(1 − m_π²/m_ρ²)` for P_a. -/
theorem ls_ksrf_ratio {mr2 mp2 F2 : ℝ} (h : mr2 - mp2 ≠ 0) (hr : mr2 ≠ 0) (hF : F2 ≠ 0) :
    gLS2 (1 / (2 * (mr2 - mp2))) F2 / gKSRF2 mr2 F2 = 2 / Real.pi * (1 - mp2 / mr2) := by
  rw [gLS2_Pa h]; unfold gKSRF2
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp

/-- The LS residue with Weinberg normalisation is strictly below KSRF: ratio `< 2/π < 1`. -/
theorem ls_below_ksrf {mr2 mp2 F2 : ℝ} (h0 : 0 < mp2) (h1 : mp2 < mr2) (hF : 0 < F2) :
    gLS2 (1 / (2 * (mr2 - mp2))) F2 / gKSRF2 mr2 F2 < 2 / Real.pi ∧ 2 / Real.pi < 1 := by
  have hr : mr2 ≠ 0 := by linarith
  rw [ls_ksrf_ratio (by linarith) hr hF.ne']
  have hpi := Real.pi_gt_three
  refine ⟨?_, ?_⟩
  · have : 0 < mp2 / mr2 := div_pos h0 (by linarith)
    have h2 : 0 < 2 / Real.pi := by positivity
    nlinarith
  · rw [div_lt_one (by linarith)]; linarith

/-- Broken claim refuted: the LS residue never equals KSRF for `0 < m_π² < m_ρ²`. -/
theorem ls_ne_ksrf {mr2 mp2 F2 : ℝ} (h0 : 0 < mp2) (h1 : mp2 < mr2) (hF : 0 < F2) :
    gLS2 (1 / (2 * (mr2 - mp2))) F2 ≠ gKSRF2 mr2 F2 := by
  intro h
  have hK : 0 < gKSRF2 mr2 F2 := by unfold gKSRF2; exact div_pos (by linarith) (by linarith)
  have := (ls_below_ksrf h0 h1 hF)
  rw [h, div_self hK.ne'] at this
  linarith [this.1, this.2]

/-- Massless limit / P_b (`α′ = 1/(2m_ρ²)`): ratio exactly `2/π`. -/
theorem ls_ksrf_ratio_Pb {mr2 F2 : ℝ} (hr : mr2 ≠ 0) (hF : F2 ≠ 0) :
    gLS2 (1 / (2 * mr2)) F2 / gKSRF2 mr2 F2 = 2 / Real.pi := by
  unfold gLS2 gKSRF2
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp

/-- Bundle (F-RHOWIDTH): T¹ dual form; residue identities; LS/KSRF ratio `(2/π)(1 − m_π²/m_ρ²) < 1`. -/
theorem frhowidth_ratio {mr2 mp2 F2 : ℝ} (h0 : 0 < mp2) (h1 : mp2 < mr2) (hF : 0 < F2) :
    gLS2 (1 / (2 * (mr2 - mp2))) F2 / gKSRF2 mr2 F2 = 2 / Real.pi * (1 - mp2 / mr2) ∧
    gLS2 (1 / (2 * (mr2 - mp2))) F2 ≠ gKSRF2 mr2 F2 :=
  ⟨ls_ksrf_ratio (by linarith) (by linarith) hF.ne', ls_ne_ksrf h0 h1 hF⟩

end PositiveGeometryEmergentSpaceTime.FRhoWidth
