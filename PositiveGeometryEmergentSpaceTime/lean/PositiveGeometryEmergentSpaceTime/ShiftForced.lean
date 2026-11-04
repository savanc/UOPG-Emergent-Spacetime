/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
M2e — the algebraic core of "the δ-shift is forced at n = 6".

Shift X_ij ↦ X_ij + δ·a_ij on the 9 hexagon chords. The conditions are C1(4) (δ⁴·A6 has a finite, nonzero
limit), C2 (no poles at the (e,e)/(o,o) chords) and C3 (Adler zero on all six legs).

**Split between script and Lean.**
* Script-verified (`scripts/m2e_shift_scan.py`, exact sympy + Singular; `scripts/m2e_certificates.py`):
  the reduction "C1–C3 ⇒ these coefficient equations", and the elimination of 503 of the 511 non-empty
  supports by a nonzero constant/monomial coefficient. Every survivor shifts all six (e,e)/(o,o) chords.
* Lean-proved here: for each of the 8 surviving supports, the listed equations (with all a ≠ 0) force either
  a = λ·(a_oo = 1, a_ee = −1, a_oe = 0) (support = the six chords; λ = a13) or a contradiction (any (o,e)
  chord shifted). Each hypothesis is tagged with its origin, C1 or C3.
-/

namespace PositiveGeometryEmergentSpaceTime.ShiftForced

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords. Hypotheses: 5 script-derived coefficient equations (in a =
  1/b), from C1. -/
@[nolint unusedArguments]
theorem forced_main {a13 a15 a24 a26 a35 a46 : ℝ} (h13 : a13 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a13 + a24 = 0)  -- from C1
    (e1 : a13 + a26 = 0)  -- from C1
    (e4 : a15 + a26 = 0)  -- from C1
    (e5 : a15 + a46 = 0)  -- from C1
    (e7 : a24 + a35 = 0)  -- from C1
    : a15 = a13 ∧ a24 = -a13 ∧ a26 = -a13 ∧ a35 = a13 ∧ a46 = -a13 := by
  have d1 : (a13 + a24) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h46] at d1
  have l2 : a24 = -a13 := by linarith
  have d3 : (a13 + a26) = 0 := by linear_combination (1 / (1)) * (e1)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h46] at d3
  have l4 : a26 = -a13 := by linarith
  have d5 : (a13 - a15) = 0 := by linear_combination (1 / (-1)) * (e4 - (1) * l4)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h46] at d5
  have l6 : a15 = a13 := by linarith
  have d7 : (a13 + a46) = 0 := by linear_combination (1 / (1)) * (e5 - (1) * l6)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h46] at d7
  have l8 : a46 = -a13 := by linarith
  have d9 : (a13 - a35) = 0 := by linear_combination (1 / (-1)) * (e7 - (1) * l2)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h46] at d9
  have l10 : a35 = a13 := by linarith
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · linear_combination (1) * l6
  · linear_combination (1) * l2
  · linear_combination (1) * l4
  · linear_combination (1) * l10
  · linear_combination (1) * l8


set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords + X14. Hypotheses: 6 script-derived coefficient equations
  (in a = 1/b), from C1+C3. -/
@[nolint unusedArguments]
theorem no_solution_14 {a13 a14 a15 a24 a26 a35 a46 : ℝ} (h13 : a13 ≠ 0) (h14 : a14 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a13 + a26 = 0)  -- from C1
    (e2 : a15 + a26 = 0)  -- from C1
    (e3 : a24 + a35 = 0)  -- from C1
    (e5 : a35 + a46 = 0)  -- from C1
    (e6 : a13*a14 + a13*a26 + a24*a26 = 0)  -- from C3
    (e10 : a13*a15 + a13*a46 + a15*a24 + a24*a46 = 0)  -- from C3
    : False := by
  have d1 : (a13 + a26) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h26, h35, h46] at d1
  have l2 : a26 = -a13 := by linarith
  have d3 : (a13 - a15) = 0 := by linear_combination (1 / (-1)) * (e2 - (1) * l2)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h26, h35, h46] at d3
  have l4 : a15 = a13 := by linarith
  have d5 : (a24 + a35) = 0 := by linear_combination (1 / (1)) * (e3)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h26, h35, h46] at d5
  have l6 : a35 = -a24 := by linarith
  have d7 : (a24 - a46) = 0 := by linear_combination (1 / (-1)) * (e5 - (1) * l6)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h26, h35, h46] at d7
  have l8 : a46 = a24 := by linarith
  have d9 : (a13) * (a13 - a14 + a24) = 0 := by linear_combination (1 / (-1)) * (e6 - (a13 + a24) * l2)
  try simp only [mul_eq_zero, false_or, h13] at d9
  have l10 : a24 = -a13 + a14 := by linarith
  have d11 : (a14)^2 = 0 := by linear_combination (1 / (1)) * (e10 - (a13 + a24) * l4 - (a13 + a24) * l8 - (a13 + a14 + a24) * l10)
  simp [h14] at d11


set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords + X25. Hypotheses: 6 script-derived coefficient equations
  (in a = 1/b), from C1+C3. -/
@[nolint unusedArguments]
theorem no_solution_25 {a13 a15 a24 a25 a26 a35 a46 : ℝ} (h13 : a13 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h25 : a25 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a13 + a24 = 0)  -- from C1
    (e1 : a13 + a26 = 0)  -- from C1
    (e2 : a15 + a46 = 0)  -- from C1
    (e5 : a35 + a46 = 0)  -- from C1
    (e6 : a13*a15 + a13*a26 + a25*a26 = 0)  -- from C3
    (e12 : a15*a24 + a15*a35 + a24*a26 + a26*a35 = 0)  -- from C3
    : False := by
  have d1 : (a13 + a24) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h25, h26, h35, h46] at d1
  have l2 : a24 = -a13 := by linarith
  have d3 : (a13 + a26) = 0 := by linear_combination (1 / (1)) * (e1)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h25, h26, h35, h46] at d3
  have l4 : a26 = -a13 := by linarith
  have d5 : (a15 + a46) = 0 := by linear_combination (1 / (1)) * (e2)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h25, h26, h35, h46] at d5
  have l6 : a46 = -a15 := by linarith
  have d7 : (a15 - a35) = 0 := by linear_combination (1 / (-1)) * (e5 - (1) * l6)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h25, h26, h35, h46] at d7
  have l8 : a35 = a15 := by linarith
  have d9 : (a13) * (a13 - a15 + a25) = 0 := by linear_combination (1 / (-1)) * (e6 - (a13 + a25) * l4)
  try simp only [mul_eq_zero, false_or, h13] at d9
  have l10 : a25 = -a13 + a15 := by linarith
  have d11 : (a13 - a15)^2 = 0 := by linear_combination (1 / (1)) * (e12 - (a15 + a26) * l2 - (-a13 + a35) * l4 - (-a13 + a15) * l8)
  try simp only [pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true] at d11
  have l12 : a15 = a13 := by linarith
  exact absurd (by linarith) h25


set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords + X36. Hypotheses: 6 script-derived coefficient equations
  (in a = 1/b), from C1+C3. -/
@[nolint unusedArguments]
theorem no_solution_36 {a13 a15 a24 a26 a35 a36 a46 : ℝ} (h13 : a13 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h36 : a36 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a13 + a24 = 0)  -- from C1
    (e2 : a15 + a26 = 0)  -- from C1
    (e3 : a15 + a46 = 0)  -- from C1
    (e4 : a24 + a35 = 0)  -- from C1
    (e6 : a13*a15 + a15*a26 + a26*a36 = 0)  -- from C3
    (e11 : a13*a35 + a13*a46 + a26*a35 + a26*a46 = 0)  -- from C3
    : False := by
  have d1 : (a13 + a24) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h36, h46] at d1
  have l2 : a24 = -a13 := by linarith
  have d3 : (a15 + a26) = 0 := by linear_combination (1 / (1)) * (e2)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h36, h46] at d3
  have l4 : a26 = -a15 := by linarith
  have d5 : (a15 + a46) = 0 := by linear_combination (1 / (1)) * (e3)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h36, h46] at d5
  have l6 : a46 = -a15 := by linarith
  have d7 : (a13 - a35) = 0 := by linear_combination (1 / (-1)) * (e4 - (1) * l2)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h26, h35, h36, h46] at d7
  have l8 : a35 = a13 := by linarith
  have d9 : (a15) * (a13 - a15 - a36) = 0 := by linear_combination (1 / (1)) * (e6 - (a15 + a36) * l4)
  try simp only [mul_eq_zero, false_or, h15] at d9
  have l10 : a36 = a13 - a15 := by linarith
  have d11 : (a13 - a15)^2 = 0 := by linear_combination (1 / (1)) * (e11 - (a35 + a46) * l4 - (a13 - a15) * l6 - (a13 - a15) * l8)
  try simp only [pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true] at d11
  have l12 : a15 = a13 := by linarith
  exact absurd (by linarith) h36


set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords + X14, X25. Hypotheses: 6 script-derived coefficient
  equations (in a = 1/b), from C1+C3. -/
@[nolint unusedArguments]
theorem no_solution_14_25 {a13 a14 a15 a24 a25 a26 a35 a46 : ℝ} (h13 : a13 ≠ 0) (h14 : a14 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h25 : a25 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a13 + a26 = 0)  -- from C1
    (e1 : a35 + a46 = 0)  -- from C1
    (e2 : a13*a14 + a13*a26 + a24*a26 = 0)  -- from C3
    (e3 : a13*a15 + a13*a26 + a25*a26 = 0)  -- from C3
    (e4 : a14*a46 + a15*a35 + a35*a46 = 0)  -- from C3
    (e6 : a13*a15 + a13*a46 + a15*a24 + a24*a46 = 0)  -- from C3
    : False := by
  have d1 : (a13 + a26) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h25, h26, h35, h46] at d1
  have l2 : a26 = -a13 := by linarith
  have d3 : (a35 + a46) = 0 := by linear_combination (1 / (1)) * (e1)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h25, h26, h35, h46] at d3
  have l4 : a46 = -a35 := by linarith
  have d5 : (a13) * (a13 - a14 + a24) = 0 := by linear_combination (1 / (-1)) * (e2 - (a13 + a24) * l2)
  try simp only [mul_eq_zero, false_or, h13] at d5
  have l6 : a24 = -a13 + a14 := by linarith
  have d7 : (a13) * (a13 - a15 + a25) = 0 := by linear_combination (1 / (-1)) * (e3 - (a13 + a25) * l2)
  try simp only [mul_eq_zero, false_or, h13] at d7
  have l8 : a25 = -a13 + a15 := by linarith
  have d9 : (a35) * (a14 - a15 + a35) = 0 := by linear_combination (1 / (-1)) * (e4 - (a14 + a35) * l4)
  try simp only [mul_eq_zero, false_or, h35] at d9
  have l10 : a35 = -a14 + a15 := by linarith
  have d11 : (a14)^2 = 0 := by linear_combination (1 / (1)) * (e6 - (a13 + a24) * l4 - (a15 - a35) * l6 - (-a14) * l10)
  simp [h14] at d11


set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords + X14, X36. Hypotheses: 6 script-derived coefficient
  equations (in a = 1/b), from C1+C3. -/
@[nolint unusedArguments]
theorem no_solution_14_36 {a13 a14 a15 a24 a26 a35 a36 a46 : ℝ} (h13 : a13 ≠ 0) (h14 : a14 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h36 : a36 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a15 + a26 = 0)  -- from C1
    (e1 : a24 + a35 = 0)  -- from C1
    (e2 : a13*a15 + a15*a26 + a26*a36 = 0)  -- from C3
    (e3 : a13*a35 + a14*a24 + a24*a35 = 0)  -- from C3
    (e4 : a14*a15 + a15*a26 + a26*a46 = 0)  -- from C3
    (e6 : a13*a15 + a13*a46 + a15*a24 + a24*a46 = 0)  -- from C3
    : False := by
  have d1 : (a15 + a26) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h26, h35, h36, h46] at d1
  have l2 : a26 = -a15 := by linarith
  have d3 : (a24 + a35) = 0 := by linear_combination (1 / (1)) * (e1)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h14, h15, h24, h26, h35, h36, h46] at d3
  have l4 : a35 = -a24 := by linarith
  have d5 : (a15) * (a13 - a15 - a36) = 0 := by linear_combination (1 / (1)) * (e2 - (a15 + a36) * l2)
  try simp only [mul_eq_zero, false_or, h15] at d5
  have l6 : a36 = a13 - a15 := by linarith
  have d7 : (a24) * (a13 - a14 + a24) = 0 := by linear_combination (1 / (-1)) * (e3 - (a13 + a24) * l4)
  try simp only [mul_eq_zero, false_or, h24] at d7
  have l8 : a24 = -a13 + a14 := by linarith
  have d9 : (a15) * (a14 - a15 - a46) = 0 := by linear_combination (1 / (1)) * (e4 - (a15 + a46) * l2)
  try simp only [mul_eq_zero, false_or, h15] at d9
  have l10 : a46 = a14 - a15 := by linarith
  have d11 : (a14)^2 = 0 := by linear_combination (1 / (1)) * (e6 - (a15 + a46) * l8 - (a14) * l10)
  simp [h14] at d11


set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Support: the six (e,e)/(o,o) chords + X25, X36. Hypotheses: 6 script-derived coefficient
  equations (in a = 1/b), from C1+C3. -/
@[nolint unusedArguments]
theorem no_solution_25_36 {a13 a15 a24 a25 a26 a35 a36 a46 : ℝ} (h13 : a13 ≠ 0) (h15 : a15 ≠ 0) (h24 : a24 ≠ 0) (h25 : a25 ≠ 0) (h26 : a26 ≠ 0) (h35 : a35 ≠ 0) (h36 : a36 ≠ 0) (h46 : a46 ≠ 0)
    (e0 : a13 + a24 = 0)  -- from C1
    (e1 : a15 + a46 = 0)  -- from C1
    (e2 : a13*a24 + a13*a35 + a24*a25 = 0)  -- from C3
    (e3 : a13*a24 + a13*a36 + a24*a26 = 0)  -- from C3
    (e4 : a15*a25 + a15*a46 + a26*a46 = 0)  -- from C3
    (e8 : a15*a24 + a15*a35 + a24*a26 + a26*a35 = 0)  -- from C3
    : False := by
  have d1 : (a13 + a24) = 0 := by linear_combination (1 / (1)) * (e0)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h25, h26, h35, h36, h46] at d1
  have l2 : a24 = -a13 := by linarith
  have d3 : (a15 + a46) = 0 := by linear_combination (1 / (1)) * (e1)
  try simp only [mul_eq_zero, pow_eq_zero_iff, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      false_or, or_false, or_assoc, h13, h15, h24, h25, h26, h35, h36, h46] at d3
  have l4 : a46 = -a15 := by linarith
  have d5 : (a13) * (a13 + a25 - a35) = 0 := by linear_combination (1 / (-1)) * (e2 - (a13 + a25) * l2)
  try simp only [mul_eq_zero, false_or, h13] at d5
  have l6 : a35 = a13 + a25 := by linarith
  have d7 : (a13) * (a13 + a26 - a36) = 0 := by linear_combination (1 / (-1)) * (e3 - (a13 + a26) * l2)
  try simp only [mul_eq_zero, false_or, h13] at d7
  have l8 : a36 = a13 + a26 := by linarith
  have d9 : (a15) * (a15 - a25 + a26) = 0 := by linear_combination (1 / (-1)) * (e4 - (a15 + a26) * l4)
  try simp only [mul_eq_zero, false_or, h15] at d9
  have l10 : a26 = -a15 + a25 := by linarith
  have d11 : (a25)^2 = 0 := by linear_combination (1 / (1)) * (e8 - (a15 + a26) * l2 - (a15 + a26) * l6 - (a25) * l10)
  simp [h25] at d11


/-- Full support (all nine chords shifted). There are no unshifted denominators, so the would-be limit
L is a linear form Σ c_f X_f (its coefficients c_f are polynomials in a; script). If L has the Adler zero on all
six legs, then L ≡ 0, and the nonzero clause of C1(4) fails. This needs no input about a. -/
def Llin (c13 c14 c15 c24 c25 c26 c35 c36 c46 X13 X14 X15 X24 X25 X26 X35 X36 X46 : ℝ) : ℝ :=
  c13*X13 + c14*X14 + c15*X15 + c24*X24 + c25*X25 + c26*X26 + c35*X35 + c36*X36 + c46*X46

/-- If the linear form `Llin` vanishes on each of the six stated Adler-zero substitutions, all nine
  coefficients are 0 (so `Llin ≡ 0`). -/
theorem full_support_L_vanishes {c13 c14 c15 c24 c25 c26 c35 c36 c46 : ℝ}
    (h1 : ∀ X24 X25 X35 X36 X46 : ℝ,
        Llin c13 c14 c15 c24 c25 c26 c35 c36 c46 (0) (X24) (X25) (X24) (X25) (0) (X35) (X36) (X46) = 0)
    (h2 : ∀ X14 X15 X35 X36 X46 : ℝ,
        Llin c13 c14 c15 c24 c25 c26 c35 c36 c46 (0) (X14) (X15) (0) (X35) (X36) (X35) (X36) (X46) = 0)
    (h3 : ∀ X14 X15 X25 X26 X46 : ℝ,
        Llin c13 c14 c15 c24 c25 c26 c35 c36 c46 (X14) (X14) (X15) (0) (X25) (X26) (0) (X46) (X46) = 0)
    (h4 : ∀ X13 X15 X25 X26 X36 : ℝ,
        Llin c13 c14 c15 c24 c25 c26 c35 c36 c46 (X13) (X15) (X15) (X25) (X25) (X26) (0) (X36) (0) = 0)
    (h5 : ∀ X13 X14 X24 X26 X36 : ℝ,
        Llin c13 c14 c15 c24 c25 c26 c35 c36 c46 (X13) (X14) (0) (X24) (X26) (X26) (X36) (X36) (0) = 0)
    (h6 : ∀ X13 X14 X24 X25 X35 : ℝ,
        Llin c13 c14 c15 c24 c25 c26 c35 c36 c46 (X13) (X14) (0) (X24) (X25) (0) (X35) (X13) (X14) = 0) :
    c13 = 0 ∧ c14 = 0 ∧ c15 = 0 ∧ c24 = 0 ∧ c25 = 0 ∧ c26 = 0 ∧ c35 = 0 ∧ c36 = 0 ∧ c46 = 0 := by
  simp only [Llin] at *
  have := h1 1 0 0 0 0
  have := h1 0 1 0 0 0
  have := h1 0 0 1 0 0
  have := h1 0 0 0 1 0
  have := h1 0 0 0 0 1
  have := h2 1 0 0 0 0
  have := h2 0 1 0 0 0
  have := h2 0 0 1 0 0
  have := h2 0 0 0 1 0
  have := h2 0 0 0 0 1
  have := h3 1 0 0 0 0
  have := h3 0 1 0 0 0
  have := h3 0 0 1 0 0
  have := h3 0 0 0 1 0
  have := h3 0 0 0 0 1
  have := h4 1 0 0 0 0
  have := h4 0 1 0 0 0
  have := h4 0 0 1 0 0
  have := h4 0 0 0 1 0
  have := h4 0 0 0 0 1
  have := h5 1 0 0 0 0
  have := h5 0 1 0 0 0
  have := h5 0 0 1 0 0
  have := h5 0 0 0 1 0
  have := h5 0 0 0 0 1
  have := h6 1 0 0 0 0
  have := h6 0 1 0 0 0
  have := h6 0 0 1 0 0
  have := h6 0 0 0 1 0
  have := h6 0 0 0 0 1
  norm_num at *
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> linarith

end PositiveGeometryEmergentSpaceTime.ShiftForced
