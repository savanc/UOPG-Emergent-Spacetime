/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-! TP-1b (2026-10-13, AutoResearch): E8 Perron–Frobenius eigenvector/eigenvalue.
Graph: chain 0–1–2–3–4–5–6, node 7 on node 2. Eigenvalue c = 2cos(π/30). -/
namespace PositiveGeometryEmergentSpaceTime.TP1b
open Real

/-- Characteristic polynomial of the E₈ adjacency matrix.

Also known as: TP1b.P, E₈ adjacency characteristic polynomial.
-/
noncomputable def charPolyE8 (c : ℝ) : ℝ := c ^ 8 - 7 * c ^ 6 + 14 * c ^ 4 - 8 * c ^ 2 + 1
/-- E₈ Perron–Frobenius eigenvector components (recursion from node 6, scaled).

Also known as: v, TP-1b eigenvector.
-/
noncomputable def e8Eigenvector (c : ℝ) : Fin 8 → ℝ := ![c ^ 7 - 6 * c ^ 5 + 9 * c ^ 3 - 2 * c,
  c ^ 6 - 5 * c ^ 4 + 6 * c ^ 2 - 1, c ^ 5 - 3 * c ^ 3 + c, c ^ 4 - 2 * c ^ 2, c ^ 3 - c,
  c ^ 2, c, c ^ 4 - 3 * c ^ 2 + 1]

/-- (A) all 8 node equations of A e8Eigenvector = c e8Eigenvector, given charPolyE8 c = 0. -/
theorem eigen (c : ℝ) (h : charPolyE8 c = 0) :
    e8Eigenvector c 1 = c * e8Eigenvector c 0 ∧ e8Eigenvector c 0 + e8Eigenvector c 2 = c * e8Eigenvector c 1 ∧ e8Eigenvector c 1 + e8Eigenvector c 3 + e8Eigenvector c 7 = c * e8Eigenvector c 2 ∧
    e8Eigenvector c 2 + e8Eigenvector c 4 = c * e8Eigenvector c 3 ∧ e8Eigenvector c 3 + e8Eigenvector c 5 = c * e8Eigenvector c 4 ∧ e8Eigenvector c 4 + e8Eigenvector c 6 = c * e8Eigenvector c 5 ∧
    e8Eigenvector c 5 = c * e8Eigenvector c 6 ∧ e8Eigenvector c 2 = c * e8Eigenvector c 7 := by
  unfold charPolyE8 at h
  simp only [e8Eigenvector, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val]
  refine ⟨by linear_combination -h, by ring, by ring, by ring, by ring, by ring, by ring, by ring⟩

/-- trig identity: charPolyE8(2cos t) = 2cos 8t + 2cos 6t − 2cos 2t − 1. -/
theorem charPolyE8_two_cos (t : ℝ) :
    charPolyE8 (2 * cos t) = 2 * cos (8 * t) + 2 * cos (6 * t) - 2 * cos (2 * t) - 1 := by
  have h2 : cos (2 * t) = 2 * cos t ^ 2 - 1 := cos_two_mul t
  have h4 : cos (4 * t) = 2 * cos (2 * t) ^ 2 - 1 := by rw [← cos_two_mul]; ring_nf
  have h8 : cos (8 * t) = 2 * cos (4 * t) ^ 2 - 1 := by rw [← cos_two_mul]; ring_nf
  have h6 : cos (6 * t) = 4 * cos (2 * t) ^ 3 - 3 * cos (2 * t) := by
    rw [← cos_three_mul]; ring_nf
  rw [h8, h6, h4, h2]; unfold charPolyE8; ring

/-- (C) 2cos(π/30) is a root of charPolyE8. -/
theorem charPolyE8_root : charPolyE8 (2 * cos (π / 30)) = 0 := by
  rw [charPolyE8_two_cos]
  have e8 : 8 * (π / 30) = 4 * π / 15 := by ring
  have e6 : 6 * (π / 30) = π / 5 := by ring
  have e2 : 2 * (π / 30) = π / 15 := by ring
  rw [e8, e6, e2]
  have hsub : cos (4 * π / 15) - cos (π / 15) = -2 * sin (π / 6) * sin (π / 10) := by
    rw [cos_sub_cos]; congr 2 <;> ring_nf
  have hs10 : sin (π / 10) = 2 * cos (π / 5) ^ 2 - 1 := by
    rw [← cos_two_mul, ← cos_pi_div_two_sub]; congr 1; ring
  have h5 : cos (π / 5) = (1 + √5) / 4 := cos_pi_div_five
  have hsq : √5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  rw [sin_pi_div_six] at hsub
  have : 2 * cos (4 * π / 15) + 2 * cos (π / 5) - 2 * cos (π / 15) - 1
      = 2 * (cos (4 * π / 15) - cos (π / 15)) + 2 * cos (π / 5) - 1 := by ring
  rw [this, hsub, hs10, h5]; nlinarith [hsq]

/-- bounds: 1.988 ≤ 2cos(π/30) ≤ 2. -/
theorem c_bounds : 1.988 ≤ 2 * cos (π / 30) ∧ 2 * cos (π / 30) ≤ 2 := by
  constructor
  · have := one_sub_sq_div_two_le_cos (x := π / 30)
    have hp := pi_lt_d2; have hp0 := pi_pos
    have : (π / 30) ^ 2 < (3.15 / 30) ^ 2 := by
      apply pow_lt_pow_left₀ (by linarith) (by positivity) (by norm_num)
    nlinarith
  · linarith [cos_le_one (π / 30)]

/-- (B) strictly positive eigenvector at c* = 2cos(π/30). -/
theorem e8Eigenvector_pos : ∀ i, 0 < e8Eigenvector (2 * cos (π / 30)) i := by
  obtain ⟨hl, hu⟩ := c_bounds
  set c := 2 * cos (π / 30)
  have hc : 0 < c := by linarith
  have hu2 : 3.952 ≤ c ^ 2 := by nlinarith
  have hu3 : c ^ 2 ≤ 4 := by nlinarith
  intro i; fin_cases i <;> simp [e8Eigenvector]
  · have h1 : 0 < c * (c ^ 2 * (c ^ 2 - 3) ^ 2 - 2) := by
      apply mul_pos hc; nlinarith [sq_nonneg (c ^ 2 - 3),
          mul_le_mul_of_nonneg_left (show (0.952:ℝ)^2 ≤ (c^2-3)^2 by nlinarith) (show (0:ℝ) ≤ c^2 by positivity)]
    nlinarith [h1]
  · nlinarith [mul_pos (by nlinarith : (0:ℝ) < c ^ 2 - 2) (by nlinarith : (0:ℝ) < c ^ 2 - 3)]
  · have h1 : 0 < c * (c ^ 4 - 3 * c ^ 2 + 1) := mul_pos hc (by nlinarith)
    nlinarith [h1]
  · nlinarith
  · have h1 : 0 < c * (c ^ 2 - 1) := mul_pos hc (by nlinarith)
    nlinarith [h1]
  · positivity
  · exact hc
  · nlinarith
end PositiveGeometryEmergentSpaceTime.TP1b
