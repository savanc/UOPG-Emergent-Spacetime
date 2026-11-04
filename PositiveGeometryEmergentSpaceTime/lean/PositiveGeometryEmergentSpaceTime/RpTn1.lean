import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity



/-!
# RpTn1 — algebra behind RP-TN-1 (reflection positivity vs total nonnegativity), 2026-10-30

Two-state OS correlator `f t = w₁ x₁^t + w₂ x₂^t`. The reflected (Hankel) 2×2 minor
`f(a+c) f(a+k+c+l) − f(a+c+l) f(a+k+c)` factors as `w₁w₂(x₁x₂)^{a+c}(x₂^k − x₁^k)(x₂^l − x₁^l)`, which is
`≥ 0` for nonnegative nodes and weights (`hankel2_minor_nonneg`). The unreflected (Toeplitz) minor
`f a f b − f 0 f (a+b) = −w₁w₂(x₁^a − x₂^a)(x₁^b − x₂^b)` is `< 0` for distinct nonnegative nodes,
positive weights and `a, b ≥ 1` (`toeplitz2_minor_neg`), and `= 0` for one state. A negative node makes
`f 1 < 0` (a diagonal entry of `H1`, so transfer positivity fails in the window) while the rank-one `H0`
principal minor vanishes (`neg_node_witness`). Statements do not depend on checker gates.
-/

namespace PositiveGeometryEmergentSpaceTime.RpTn1

/-- Two-state correlator. -/
def corr2 (w₁ w₂ x₁ x₂ : ℝ) (t : ℕ) : ℝ := w₁ * x₁ ^ t + w₂ * x₂ ^ t

theorem hankel2_minor_identity (w₁ w₂ x₁ x₂ : ℝ) (a c k l : ℕ) :
    corr2 w₁ w₂ x₁ x₂ (a + c) * corr2 w₁ w₂ x₁ x₂ (a + k + (c + l))
      - corr2 w₁ w₂ x₁ x₂ (a + (c + l)) * corr2 w₁ w₂ x₁ x₂ (a + k + c)
      = w₁ * w₂ * (x₁ * x₂) ^ (a + c) * ((x₂ ^ k - x₁ ^ k) * (x₂ ^ l - x₁ ^ l)) := by
  unfold corr2; ring

theorem pow_diff_mul_nonneg (x₁ x₂ : ℝ) (h₁ : 0 ≤ x₁) (h₂ : 0 ≤ x₂) (k l : ℕ) :
    0 ≤ (x₂ ^ k - x₁ ^ k) * (x₂ ^ l - x₁ ^ l) := by
  rcases le_total x₁ x₂ with h | h
  · have hk := pow_le_pow_left₀ h₁ h k
    have hl := pow_le_pow_left₀ h₁ h l
    exact mul_nonneg (by linarith) (by linarith)
  · have hk := pow_le_pow_left₀ h₂ h k
    have hl := pow_le_pow_left₀ h₂ h l
    exact mul_nonneg_of_nonpos_of_nonpos (by linarith) (by linarith)

theorem hankel2_minor_nonneg (w₁ w₂ x₁ x₂ : ℝ) (hw₁ : 0 ≤ w₁) (hw₂ : 0 ≤ w₂) (h₁ : 0 ≤ x₁) (h₂ : 0 ≤ x₂)
    (a c k l : ℕ) :
    0 ≤ corr2 w₁ w₂ x₁ x₂ (a + c) * corr2 w₁ w₂ x₁ x₂ (a + k + (c + l))
      - corr2 w₁ w₂ x₁ x₂ (a + (c + l)) * corr2 w₁ w₂ x₁ x₂ (a + k + c) := by
  rw [hankel2_minor_identity]
  have := pow_diff_mul_nonneg x₁ x₂ h₁ h₂ k l
  have : 0 ≤ (x₁ * x₂) ^ (a + c) := pow_nonneg (mul_nonneg h₁ h₂) _
  positivity

theorem toeplitz2_minor_identity (w₁ w₂ x₁ x₂ : ℝ) (a b : ℕ) :
    corr2 w₁ w₂ x₁ x₂ a * corr2 w₁ w₂ x₁ x₂ b - corr2 w₁ w₂ x₁ x₂ 0 * corr2 w₁ w₂ x₁ x₂ (a + b)
      = -(w₁ * w₂ * ((x₁ ^ a - x₂ ^ a) * (x₁ ^ b - x₂ ^ b))) := by
  unfold corr2; ring

theorem toeplitz2_minor_neg (w₁ w₂ x₁ x₂ : ℝ) (hw₁ : 0 < w₁) (hw₂ : 0 < w₂) (h₁ : 0 ≤ x₁) (h₂ : 0 ≤ x₂)
    (hne : x₁ ≠ x₂) (a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0) :
    corr2 w₁ w₂ x₁ x₂ a * corr2 w₁ w₂ x₁ x₂ b - corr2 w₁ w₂ x₁ x₂ 0 * corr2 w₁ w₂ x₁ x₂ (a + b) < 0 := by
  rw [toeplitz2_minor_identity]
  have hp : 0 < (x₁ ^ a - x₂ ^ a) * (x₁ ^ b - x₂ ^ b) := by
    rcases lt_or_gt_of_ne hne with h | h
    · have ha' := pow_lt_pow_left₀ h h₁ ha
      have hb' := pow_lt_pow_left₀ h h₁ hb
      exact mul_pos_of_neg_of_neg (by linarith) (by linarith)
    · have ha' := pow_lt_pow_left₀ h h₂ ha
      have hb' := pow_lt_pow_left₀ h h₂ hb
      exact mul_pos (by linarith) (by linarith)
  have : 0 < w₁ * w₂ * ((x₁ ^ a - x₂ ^ a) * (x₁ ^ b - x₂ ^ b)) := by positivity
  linarith

theorem toeplitz1_minor_zero (w x : ℝ) (a b : ℕ) :
    corr2 w 0 x 0 a * corr2 w 0 x 0 b - corr2 w 0 x 0 0 * corr2 w 0 x 0 (a + b) = 0 := by
  unfold corr2; ring

theorem neg_node_witness :
    corr2 1 0 (-1 / 2) 0 1 < 0 ∧
      corr2 1 0 (-1 / 2) 0 0 * corr2 1 0 (-1 / 2) 0 2 - corr2 1 0 (-1 / 2) 0 1 ^ 2 = 0 := by
  unfold corr2; norm_num

/-- Non-vacuity: the hypotheses of `toeplitz2_minor_neg` are satisfiable (nodes 1/3, 2/3, a = b = 1). -/
theorem toeplitz2_witness :
    corr2 1 1 (1 / 3) (2 / 3) 1 * corr2 1 1 (1 / 3) (2 / 3) 1
      - corr2 1 1 (1 / 3) (2 / 3) 0 * corr2 1 1 (1 / 3) (2 / 3) (1 + 1) < 0 :=
  toeplitz2_minor_neg 1 1 (1 / 3) (2 / 3) one_pos one_pos (by norm_num) (by norm_num) (by norm_num) 1 1
    one_ne_zero one_ne_zero

end PositiveGeometryEmergentSpaceTime.RpTn1
