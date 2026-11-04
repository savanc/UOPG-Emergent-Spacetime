/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.SG1
/-! TP-1a (2026-10-13, AutoResearch): A_n Perron–Frobenius eigenvector x_k = sin(kπ/(n+1)),
eigenvalue 2cos(π/h) with Coxeter number h = n+1. -/
namespace PositiveGeometryEmergentSpaceTime.TP1a
open Real
/-- Perron–Frobenius eigenvector entry `x n k = sin(kπ/(n + 1))` of the Aₙ path graph. -/
noncomputable def x (n k : ℕ) : ℝ := Real.sin (k * (π / (n + 1)))

/-- (a) positivity on 1 ≤ k ≤ n. -/
theorem x_pos {n k : ℕ} (h1 : 1 ≤ k) (h2 : k ≤ n) : 0 < x n k := by
  unfold x
  have hn : (0 : ℝ) < n + 1 := by positivity
  apply Real.sin_pos_of_pos_of_lt_pi
  · have : (1 : ℝ) ≤ k := by exact_mod_cast h1
    have := Real.pi_pos; positivity
  · have hk : (k : ℝ) < n + 1 := by exact_mod_cast Nat.lt_succ_of_le h2
    rw [mul_div_assoc', div_lt_iff₀ hn]; nlinarith [Real.pi_pos]

/-- boundary values vanish: x₀ = x_{n+1} = 0. -/
theorem x_zero (n : ℕ) : x n 0 = 0 := by simp [x]
/-- `x n (n + 1) = sin π = 0`. -/
theorem x_end (n : ℕ) : x n (n + 1) = 0 := by
  unfold x; push_cast
  have hn : (n : ℝ) + 1 ≠ 0 := by positivity
  rw [mul_div_cancel₀ _ hn, Real.sin_pi]

/-- (b) eigen-equation of the path adjacency at every interior index (ends via x_zero/x_end). -/
theorem eigen (n k : ℕ) :
    x n k + x n (k + 2) = 2 * Real.cos (π / (n + 1)) * x n (k + 1) := by
  unfold x; push_cast
  set θ := π / (n + 1)
  have e1 : (k : ℝ) * θ = (k + 1) * θ - θ := by ring
  have e2 : ((k : ℝ) + 2) * θ = (k + 1) * θ + θ := by ring
  rw [e1, e2, Real.sin_sub, Real.sin_add]; ring

/-- (c) eigenvalue 2cos(π/h), h = n+1, as a statement about the Coxeter number. -/
theorem eigenvalue_coxeter (n : ℕ) : 2 * Real.cos (π / ((n + 1 : ℕ) : ℝ)) = 2 * Real.cos (π / (n + 1)) := by
  push_cast; rfl

/-- (d) ratio x₂/x₁ = 2cos θ; for n = 4 it is the golden ratio (links SG-1). -/
theorem ratio21 {n : ℕ} (hn : 1 ≤ n) : x n 2 / x n 1 = 2 * Real.cos (π / (n + 1)) := by
  have h := eigen n 0
  rw [x_zero, zero_add] at h
  have hp : 0 < x n 1 := x_pos le_rfl hn
  rw [div_eq_iff hp.ne', h]
/-- For A₄ (`n = 4`): `x 4 2 / x 4 1 = φ` (the golden ratio). -/
theorem golden_A4 : x 4 2 / x 4 1 = goldenRatio := by
  rw [ratio21 (by norm_num)]; norm_num; rw [goldenRatio]; ring
end PositiveGeometryEmergentSpaceTime.TP1a
