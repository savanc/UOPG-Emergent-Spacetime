/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of MR-3.
Written ONLY from Paper II v8 §"MR-3" prose and Fig. caption ("minimal massive LS family fixed by
an Adler zero and the ρ on the leading trajectory, r = m_π²/m_ρ²; the J = 0 coefficient at the
f₂ level is r(2r−1)/(4(r−1)²) < 0 for 0 < r < 1/2, so positivity forces r = 0"), BEFORE opening
lean/PGEST/MassiveLS.lean, the blueprint row or the generated/lean listing.

Blind reconstruction of the family (units m_ρ² = 1):
  A(s,t) = Γ(1−α(s))Γ(1−α(t))/Γ(1−α(s)−α(t)), α(x) = α₀ + α′x,
  Adler zero at s = t = m_π² = r  ⇔  α(r) = 1/2;   ρ on the trajectory ⇔ α(1) = 1,
  so α′ = 1/(2(1−r)), α₀ = 1 − α′.  f₂ level: α(s) = 2.  Kinematics: s + t + u = 4r,
  t = −(s − 4r)(1 − z)/2.  Residue in s at α(s) = 2 is (2/α′)·α(t)(1+α(t)) (positive prefactor),
  and we decompose R(z) = α(t)(1+α(t)) in Legendre polynomials.
The blind derivation REPRODUCES c₀ = r(2r−1)/(4(r−1)²) with this normalisation, and also finds
c₁ = −3(2r−1)/(8(r−1)²), c₂ = 3(2r−1)²/(8(r−1)²).
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.Mr3Blind

def P0 (_z : ℚ) : ℚ := 1
def P1 (z : ℚ) : ℚ := z
def P2 (z : ℚ) : ℚ := (3 * z ^ 2 - 1) / 2

def alphaP (r : ℚ) : ℚ := 1 / (2 * (1 - r))
def alpha0 (r : ℚ) : ℚ := 1 - alphaP r
def alpha (r x : ℚ) : ℚ := alpha0 r + alphaP r * x
/-- the f₂ mass², α(s) = 2 -/
def sF2 (r : ℚ) : ℚ := (2 - alpha0 r) / alphaP r
def tOf (r z : ℚ) : ℚ := -(sF2 r - 4 * r) * (1 - z) / 2
/-- reduced f₂-level residue Γ(1−α_t)/Γ(−1−α_t) = α_t(1+α_t) -/
def R (r z : ℚ) : ℚ := alpha r (tOf r z) * (1 + alpha r (tOf r z))

def c0 (r : ℚ) : ℚ := r * (2 * r - 1) / (4 * (r - 1) ^ 2)
def c1 (r : ℚ) : ℚ := -3 * (2 * r - 1) / (8 * (r - 1) ^ 2)
def c2 (r : ℚ) : ℚ := 3 * (2 * r - 1) ^ 2 / (8 * (r - 1) ^ 2)

/-- family checks: Adler zero (1 − α(r) − α(r) = 0) and α(m_ρ²) = 1. -/
theorem adler_zero (r : ℚ) (hr : r ≠ 1) : 1 - alpha r r - alpha r r = 0 := by
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  unfold alpha alpha0 alphaP; field_simp; ring

theorem rho_on_trajectory (r : ℚ) : alpha r 1 = 1 := by
  unfold alpha alpha0; ring

theorem f2_level (r : ℚ) (hr : r ≠ 1) : alpha r (sF2 r) = 2 := by
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  unfold alpha sF2 alpha0 alphaP; field_simp; ring

/-- BLIND CLAIM (Legendre decomposition at the f₂ level). -/
theorem legendre_decomp (r z : ℚ) (hr : r ≠ 1) :
    R r z = c2 r * P2 z + c1 r * P1 z + c0 r * P0 z := by
  have h : (1 - r) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  have h' : (r - 1) ≠ 0 := sub_ne_zero.mpr hr
  unfold R alpha tOf sF2 alpha0 alphaP c0 c1 c2 P0 P1 P2
  field_simp; ring

private lemma den_pos (r : ℚ) (hr : r ≠ 1) (m : ℚ) (hm : 0 < m) : 0 < m * (r - 1) ^ 2 := by
  have : 0 < (r - 1) ^ 2 := by positivity
  positivity

/-- BLIND CLAIM (paper's stated sign): c₀ < 0 on 0 < r < 1/2. -/
theorem c0_neg (r : ℚ) (h0 : 0 < r) (h1 : r < 1/2) : c0 r < 0 := by
  unfold c0
  apply div_neg_of_neg_of_pos
  · nlinarith
  · exact den_pos r (by linarith) 4 (by norm_num)

/-- BLIND CLAIM (paper's headline, on the stated range): for 0 ≤ r < 1/2,
c₀ ≥ 0 ⇔ r = 0. -/
theorem positivity_forces_zero (r : ℚ) (h0 : 0 ≤ r) (h1 : r < 1/2) : 0 ≤ c0 r ↔ r = 0 := by
  constructor
  · intro h
    rcases h0.lt_or_eq with h0 | h0
    · exact absurd h (not_le.mpr (c0_neg r h0 h1))
    · exact h0.symm
  · rintro rfl; unfold c0; norm_num

/-- BLIND-STRONGER reading: over all r ≥ 0, r ≠ 1, non-negativity of ALL three f₂-level
coefficients holds iff r = 0 or r = 1/2. (So "only c₀ can fail positivity" is false for
r > 1/2, where c₁ < 0; and r = 1/2 is a degenerate point where the whole residue vanishes.) -/
theorem all_coeffs_nonneg_iff (r : ℚ) (h0 : 0 ≤ r) (hr : r ≠ 1) :
    (0 ≤ c0 r ∧ 0 ≤ c1 r ∧ 0 ≤ c2 r) ↔ (r = 0 ∨ r = 1/2) := by
  have hd4 := den_pos r hr 4 (by norm_num)
  have hd8 := den_pos r hr 8 (by norm_num)
  unfold c0 c1 c2
  rw [div_nonneg_iff, div_nonneg_iff, div_nonneg_iff]
  constructor
  · rintro ⟨h0', h1', _⟩
    rcases h0' with ⟨a, _⟩ | ⟨_, b⟩
    · rcases h1' with ⟨c, _⟩ | ⟨_, d⟩
      · have hc : 2 * r - 1 ≤ 0 := by linarith
        rcases hc.lt_or_eq with hc | hc
        · left; nlinarith
        · right; linarith
      · linarith
    · linarith
  · rintro (rfl | rfl)
    · refine ⟨Or.inl ⟨by norm_num, by norm_num⟩, Or.inl ⟨by norm_num, by norm_num⟩,
        Or.inl ⟨by norm_num, by norm_num⟩⟩
    · refine ⟨Or.inl ⟨by norm_num, by norm_num⟩, Or.inl ⟨by norm_num, by norm_num⟩,
        Or.inl ⟨by norm_num, by norm_num⟩⟩

theorem c1_neg_above_half (r : ℚ) (h1 : 1/2 < r) (hr : r ≠ 1) : c1 r < 0 := by
  unfold c1
  apply div_neg_of_neg_of_pos
  · linarith
  · exact den_pos r hr 8 (by norm_num)

theorem residue_vanishes_at_half (z : ℚ) : R (1/2) z = 0 := by
  rw [legendre_decomp _ _ (by norm_num)]; unfold c0 c1 c2; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Mr3Blind
