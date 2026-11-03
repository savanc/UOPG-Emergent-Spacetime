/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of MR-1b (Legendre arithmetic).
Written ONLY from Paper II v8 §"MR-1b" prose (LS amplitude A(s,t) = Γ(1−α(s))Γ(1−α(t))/
Γ(1−α(s)−α(t)), α(s) = α₀ + α′s, α₀ = 1/2, α′ = 1/(2m_ρ²); "the Legendre decompositions of the
two residues and the arithmetic that gives 5/16 and 49/240 are PROVED"; convention
"c_J = −g²m² … with m² = 5 and 7 in units m_ρ² = 1 and ratios taken relative to g_ρ² = 1/2")
and Paper I v9 §MR-1b, BEFORE opening lean/…/LSResidue*, the blueprint row or generated/lean.

Blind set-up (units m_ρ² = 1, massless pions): α(x) = 1/2 + x/2, level N at m_N² = 2N − 1,
t = −(s/2)(1 − z). Residue in s of A at α(s) = N:
  Res = (2(−1)^N/(N−1)!) · Γ(1−α(t))/Γ(1−N−α(t)) = (2(−1)^N/(N−1)!) · ∏_{j=1}^{N}(j − N − α(t)).
(The Γ-ratio step is proved below as `gamma_ratio`.) The literal residue has POSITIVE leading
Legendre coefficients (1/2, 25/32, 343/480 at N = 1, 3, 4), so g² = c_J/m² (not −c_J/m²) is the
reading that gives g_ρ² = +1/2 and the ratios +5/16, +49/240.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.Mr1bBlind

open Finset

def P0 (_z : ℚ) : ℚ := 1
def P1 (z : ℚ) : ℚ := z
def P2 (z : ℚ) : ℚ := (3 * z ^ 2 - 1) / 2
def P3 (z : ℚ) : ℚ := (5 * z ^ 3 - 3 * z) / 2
def P4 (z : ℚ) : ℚ := (35 * z ^ 4 - 30 * z ^ 2 + 3) / 8

def alpha (x : ℚ) : ℚ := 1 / 2 + x / 2
def mSq (N : ℕ) : ℚ := 2 * N - 1
def tOf (s z : ℚ) : ℚ := -(s / 2) * (1 - z)

theorem level (N : ℕ) : alpha (mSq N) = N := by unfold alpha mSq; ring

/-- The residue of the LS amplitude at α(s) = N (as a function of z = cos θ). -/
def residue (N : ℕ) (z : ℚ) : ℚ :=
  2 * (-1) ^ N / (Nat.factorial (N - 1) : ℚ) *
    ∏ i ∈ range N, ((i : ℚ) + 1 - N - alpha (tOf (mSq N) z))

/-- Γ-ratio identity behind `residue`: Γ(x + N) = Γ(x) ∏_{i<N} (x + i) away from poles. -/
theorem gamma_ratio (x : ℝ) (N : ℕ) (h : ∀ i < N, x + i ≠ 0) :
    Real.Gamma (x + N) = Real.Gamma x * ∏ i ∈ range N, (x + i) := by
  induction N with
  | zero => simp
  | succ n ih =>
    rw [prod_range_succ, ← mul_assoc, ← ih (fun i hi => h i (by omega))]
    have : x + ((n + 1 : ℕ) : ℝ) = (x + n) + 1 := by push_cast; ring
    rw [this, Real.Gamma_add_one (h n (by omega))]; ring

theorem rho_residue (z : ℚ) : residue 1 z = 1/2 * P1 z + 1/2 * P0 z := by
  simp [residue, alpha, tOf, mSq, P0, P1]; ring

theorem f2_residue (z : ℚ) : residue 2 z = 3/4 * P2 z + 3/4 * P1 z + 0 * P0 z := by
  simp [residue, prod_range_succ, alpha, tOf, mSq, P0, P1, P2]; ring

/-- BLIND CLAIM (ρ₃ level, N = 3, m² = 5). -/
theorem rho3_residue (z : ℚ) :
    residue 3 z = 25/32 * P3 z + 25/32 * P2 z + 5/32 * P1 z + 5/32 * P0 z := by
  simp [residue, prod_range_succ, alpha, tOf, mSq, P0, P1, P2, P3]; ring

/-- BLIND CLAIM (f₄ level, N = 4, m² = 7). -/
theorem f4_residue (z : ℚ) :
    residue 4 z = 343/480 * P4 z + 343/480 * P3 z + 49/144 * P2 z + 91/240 * P1 z
      + 7/180 * P0 z := by
  simp [residue, prod_range_succ, alpha, tOf, mSq, P0, P1, P2, P3, P4, Nat.factorial]; ring

/-- Uniqueness of the leading coefficient: if a degree-≤4 Legendre combination vanishes
identically, all coefficients vanish (so "the" Legendre coefficients above are well defined). -/
theorem legendre_indep (a b c d e : ℚ)
    (h : ∀ z, a * P4 z + b * P3 z + c * P2 z + d * P1 z + e * P0 z = 0) :
    a = 0 ∧ b = 0 ∧ c = 0 ∧ d = 0 ∧ e = 0 := by
  have h0 := h 0; have h1 := h 1; have h2 := h (-1); have h3 := h 2; have h4 := h (-2)
  simp only [P0, P1, P2, P3, P4] at h0 h1 h2 h3 h4
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> linarith

/-- coupling convention read from the prose, with the sign that makes g_ρ² = +1/2. -/
def gSq (cLead m2 : ℚ) : ℚ := cLead / m2

theorem g_rho : gSq (1/2) (mSq 1) = 1/2 := by unfold gSq mSq; norm_num

/-- BLIND CLAIM: g²_{ρ₃ππ}/g²_{ρππ} = 5/16. -/
theorem rho3_ratio : gSq (25/32) (mSq 3) / gSq (1/2) (mSq 1) = 5/16 := by
  unfold gSq mSq; norm_num

/-- BLIND CLAIM: g²_{f₄ππ}/g²_{ρππ} = 49/240. -/
theorem f4_ratio : gSq (343/480) (mSq 4) / gSq (1/2) (mSq 1) = 49/240 := by
  unfold gSq mSq; norm_num

/-- Literal "c_J = −g²m²" with g_ρ² = +1/2 held fixed gives −5/16 and −49/240. -/
theorem literal_sign_ratios :
    (-(25/32) / mSq 3) / (1/2 : ℚ) = -5/16 ∧ (-(343/480) / mSq 4) / (1/2 : ℚ) = -49/240 := by
  unfold mSq; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Mr1bBlind
