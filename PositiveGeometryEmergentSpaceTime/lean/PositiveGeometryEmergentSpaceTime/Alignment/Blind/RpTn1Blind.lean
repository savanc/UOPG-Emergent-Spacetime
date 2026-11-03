/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of RP-TN-1 (Lean part).
Written ONLY from Paper II v8 §"RP-TN-1" prose and glossary ("the reflected (Hankel) 2×2 minor
C(a+c)C(a+k+c+l) − C(a+c+l)C(a+k+c) is nonnegative for a two-term correlator
C(t) = w₁x₁ᵗ + w₂x₂ᵗ with nonnegative weights and nodes, and the unreflected (Toeplitz) minor
C(a)C(b) − C(0)C(a+b) is negative for positive weights, distinct nonnegative nodes and
a, b ≥ 1"), BEFORE opening the original Lean module or the blueprint row.
Blind derivation: Hankel minor = w₁w₂(x₁x₂)^{a+c}(x₁ᵏ−x₂ᵏ)(x₁ˡ−x₂ˡ);
Toeplitz minor = −w₁w₂(x₁ᵃ−x₂ᵃ)(x₁ᵇ−x₂ᵇ).
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.RpTn1Blind

def C (w₁ w₂ x₁ x₂ : ℝ) (t : ℕ) : ℝ := w₁ * x₁ ^ t + w₂ * x₂ ^ t

theorem hankel_identity (w₁ w₂ x₁ x₂ : ℝ) (a c k l : ℕ) :
    C w₁ w₂ x₁ x₂ (a + c) * C w₁ w₂ x₁ x₂ (a + k + c + l)
      - C w₁ w₂ x₁ x₂ (a + c + l) * C w₁ w₂ x₁ x₂ (a + k + c)
    = w₁ * w₂ * (x₁ * x₂) ^ (a + c) * (x₁ ^ k - x₂ ^ k) * (x₁ ^ l - x₂ ^ l) := by
  unfold C; simp only [pow_add, mul_pow]; ring

theorem toeplitz_identity (w₁ w₂ x₁ x₂ : ℝ) (a b : ℕ) :
    C w₁ w₂ x₁ x₂ a * C w₁ w₂ x₁ x₂ b - C w₁ w₂ x₁ x₂ 0 * C w₁ w₂ x₁ x₂ (a + b)
    = -(w₁ * w₂ * (x₁ ^ a - x₂ ^ a) * (x₁ ^ b - x₂ ^ b)) := by
  unfold C; simp only [pow_add, pow_zero]; ring

/-- same-sign lemma: for nonnegative nodes, (x₁ᵏ − x₂ᵏ)(x₁ˡ − x₂ˡ) ≥ 0. -/
lemma same_sign (x₁ x₂ : ℝ) (h₁ : 0 ≤ x₁) (h₂ : 0 ≤ x₂) (k l : ℕ) :
    0 ≤ (x₁ ^ k - x₂ ^ k) * (x₁ ^ l - x₂ ^ l) := by
  rcases le_total x₁ x₂ with h | h
  · have hk : x₁ ^ k ≤ x₂ ^ k := pow_le_pow_left₀ h₁ h k
    have hl : x₁ ^ l ≤ x₂ ^ l := pow_le_pow_left₀ h₁ h l
    exact mul_nonneg_of_nonpos_of_nonpos (by linarith) (by linarith)
  · have hk : x₂ ^ k ≤ x₁ ^ k := pow_le_pow_left₀ h₂ h k
    have hl : x₂ ^ l ≤ x₁ ^ l := pow_le_pow_left₀ h₂ h l
    exact mul_nonneg (by linarith) (by linarith)

/-- BLIND CLAIM (Hankel/reflected minor ≥ 0). -/
theorem hankel_minor_nonneg (w₁ w₂ x₁ x₂ : ℝ) (hw₁ : 0 ≤ w₁) (hw₂ : 0 ≤ w₂)
    (h₁ : 0 ≤ x₁) (h₂ : 0 ≤ x₂) (a c k l : ℕ) :
    0 ≤ C w₁ w₂ x₁ x₂ (a + c) * C w₁ w₂ x₁ x₂ (a + k + c + l)
      - C w₁ w₂ x₁ x₂ (a + c + l) * C w₁ w₂ x₁ x₂ (a + k + c) := by
  rw [hankel_identity, mul_assoc]
  exact mul_nonneg (mul_nonneg (mul_nonneg hw₁ hw₂) (pow_nonneg (mul_nonneg h₁ h₂) _))
    (same_sign x₁ x₂ h₁ h₂ k l)

/-- BLIND CLAIM (Toeplitz/unreflected minor < 0). -/
theorem toeplitz_minor_neg (w₁ w₂ x₁ x₂ : ℝ) (hw₁ : 0 < w₁) (hw₂ : 0 < w₂)
    (h₁ : 0 ≤ x₁) (h₂ : 0 ≤ x₂) (hne : x₁ ≠ x₂) (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    C w₁ w₂ x₁ x₂ a * C w₁ w₂ x₁ x₂ b - C w₁ w₂ x₁ x₂ 0 * C w₁ w₂ x₁ x₂ (a + b) < 0 := by
  rw [toeplitz_identity, neg_lt_zero, mul_assoc]
  apply mul_pos (mul_pos hw₁ hw₂)
  rcases lt_or_gt_of_ne hne with h | h
  · have hA : x₁ ^ a < x₂ ^ a := pow_lt_pow_left₀ h h₁ (by omega)
    have hB : x₁ ^ b < x₂ ^ b := pow_lt_pow_left₀ h h₁ (by omega)
    exact mul_pos_of_neg_of_neg (by linarith) (by linarith)
  · have hA : x₂ ^ a < x₁ ^ a := pow_lt_pow_left₀ h h₂ (by omega)
    have hB : x₂ ^ b < x₁ ^ b := pow_lt_pow_left₀ h h₂ (by omega)
    exact mul_pos (by linarith) (by linarith)

/-- Sharpness controls: the Toeplitz minor vanishes at equal nodes or at a = 0. -/
theorem toeplitz_zero_equal_nodes (w₁ w₂ x : ℝ) (a b : ℕ) :
    C w₁ w₂ x x a * C w₁ w₂ x x b - C w₁ w₂ x x 0 * C w₁ w₂ x x (a + b) = 0 := by
  rw [toeplitz_identity]; ring

theorem toeplitz_zero_a0 (w₁ w₂ x₁ x₂ : ℝ) (b : ℕ) :
    C w₁ w₂ x₁ x₂ 0 * C w₁ w₂ x₁ x₂ b - C w₁ w₂ x₁ x₂ 0 * C w₁ w₂ x₁ x₂ (0 + b) = 0 := by
  simp

/-- Control: with a negative node the Hankel minor can be negative (so nonnegativity of nodes
is needed): x = (1, −2), w = (1, 1), a = c = 0, k = 1, l = 2 gives −9. -/
theorem hankel_negative_node_control :
    C 1 1 1 (-2) (0 + 0) * C 1 1 1 (-2) (0 + 1 + 0 + 2)
      - C 1 1 1 (-2) (0 + 0 + 2) * C 1 1 1 (-2) (0 + 1 + 0) = -9 := by
  unfold C; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.RpTn1Blind
