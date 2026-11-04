/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
SURF-1′ sign facts over ℚ (prereg §4). Pure polynomial facts about the literal Laurent lists that
`Enum.lean` / `Box.lean` certify by kernel enumeration; tied together in `Main.lean`.
-/
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-!
# PositiveGeometryEmergentSpaceTime.Surf1.Signs

Supporting module of the `PositiveGeometryEmergentSpaceTime` Lean library. See the declarations below for
the statements; each theorem is checked by the Lean kernel.
-/


set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Surf1

/-- Evaluate Laurent data `(exponent, coefficient)` at `N`. -/
def ev (p : List (Int × Int)) (N : ℚ) : ℚ := (p.map (fun t => (t.2 : ℚ) * N ^ t.1)).sum

/-- `K = W(numerator)/W(denominator)` at `N`. -/
def K (num den : List (Int × Int)) (N : ℚ) : ℚ := ev num N / ev den N

/-- Laurent data certified in `Enum.lean` / `Box/Graph.lean` / `Box.lean`. -/
def thetaL : List (Int × Int) := [(3, 2), (1, -10), (-1, 8)]
/-- Laurent coefficients `(exponent, coefficient)` of the tetrahedron weight. -/
def tetraL : List (Int × Int) := [(4, 2), (2, -34), (0, 128), (-2, -96)]
/-- Laurent coefficients `(exponent, coefficient)` of the `ttU` weight. -/
def ttUL : List (Int × Int) := [(4, 4), (2, -36), (0, 96), (-2, -64)]
/-- Laurent coefficients `(exponent, coefficient)` of the `boxU` weight. -/
def boxUL : List (Int × Int) := [(3, -32), (1, 480), (-1, -1728), (-3, 1280)]

/-- Closed form: `ev thetaL N = 2(N²−1)(N²−4)/N` for `N ≠ 0`. -/
theorem ev_theta (N : ℚ) (h : N ≠ 0) : ev thetaL N = 2 * (N ^ 2 - 1) * (N ^ 2 - 4) / N := by
  simp [ev, thetaL, zpow_neg, zpow_ofNat]
  field_simp
  ring

/-- Closed form: `ev tetraL N = 2(N²−1)(N²−4)(N²−12)/N²` for `N ≠ 0`. -/
theorem ev_tetra (N : ℚ) (h : N ≠ 0) :
    ev tetraL N = 2 * (N ^ 2 - 1) * (N ^ 2 - 4) * (N ^ 2 - 12) / N ^ 2 := by
  simp [ev, tetraL, zpow_neg, zpow_ofNat]
  field_simp
  ring

/-- Closed form: `ev ttUL N = 4(N²−1)(N²−4)²/N²` for `N ≠ 0`. -/
theorem ev_ttU (N : ℚ) (h : N ≠ 0) : ev ttUL N = 4 * (N ^ 2 - 1) * (N ^ 2 - 4) ^ 2 / N ^ 2 := by
  simp [ev, ttUL, zpow_neg, zpow_ofNat]
  field_simp
  ring

/-- Closed form: `ev boxUL N = −32(N²−1)(N²−4)(N²−10)/N³` for `N ≠ 0`. -/
theorem ev_boxU (N : ℚ) (h : N ≠ 0) :
    ev boxUL N = -32 * (N ^ 2 - 1) * (N ^ 2 - 4) * (N ^ 2 - 10) / N ^ 3 := by
  simp [ev, boxUL, zpow_neg, zpow_ofNat]
  field_simp
  ring

/-- P3: K_triangle = (N²−12)/N. -/
theorem K_tri_closed (N : ℚ) (h3 : 3 ≤ N) : K tetraL thetaL N = (N ^ 2 - 12) / N := by
  have hN : N ≠ 0 := by intro h; rw [h] at h3; norm_num at h3
  have h1 : N ^ 2 - 1 ≠ 0 := by nlinarith
  have h4 : N ^ 2 - 4 ≠ 0 := by nlinarith
  rw [K, ev_tetra N hN, ev_theta N hN]
  field_simp

/-- P3 at N = 3: the triangle interference is −1 (cited (N²−12)/N). -/
theorem K_tri_three : K tetraL thetaL 3 = -1 := by
  simp [K, ev, tetraL, thetaL]
  norm_num

/-- `K tetraL thetaL 3` is negative. -/
theorem K_tri_three_neg : K tetraL thetaL 3 < 0 := by
  rw [K_tri_three]; norm_num

/-- Crossed box, u-channel: K = −8(N²−10)/(N(N²−4)). -/
theorem K_boxU_closed (N : ℚ) (h3 : 3 ≤ N) :
    K boxUL ttUL N = -8 * (N ^ 2 - 10) / (N * (N ^ 2 - 4)) := by
  have hN : N ≠ 0 := by intro h; rw [h] at h3; norm_num at h3
  have h1 : N ^ 2 - 1 ≠ 0 := by nlinarith
  have h4 : N ^ 2 - 4 ≠ 0 := by nlinarith
  rw [K, ev_boxU N hN, ev_ttU N hN]
  field_simp
  ring

/-- `K boxUL ttUL N` is negative for every rational `N ≥ 4`. -/
theorem K_boxU_neg (N : ℚ) (h4 : 4 ≤ N) : K boxUL ttUL N < 0 := by
  rw [K_boxU_closed N (by linarith)]
  have a : 0 < N ^ 2 - 10 := by nlinarith
  have b : 0 < N * (N ^ 2 - 4) := by
    have : 0 < N ^ 2 - 4 := by nlinarith
    positivity
  apply div_neg_of_neg_of_pos _ b
  linarith

/-- Post-hoc (not verdict-bearing): the crossed box is positive at N = 3 (8/15). -/
theorem K_boxU_three : K boxUL ttUL 3 = 8 / 15 := by
  simp [K, ev, boxUL, ttUL]
  norm_num

/-- Denominators are positive for every N ≥ 3 (gate DEN_POSITIVE, for these two graphs). -/
theorem ev_theta_pos (N : ℚ) (h3 : 3 ≤ N) : 0 < ev thetaL N := by
  have hN : 0 < N := by linarith
  rw [ev_theta N hN.ne']
  have : 0 < N ^ 2 - 1 := by nlinarith
  have : 0 < N ^ 2 - 4 := by nlinarith
  positivity

/-- `ev ttUL N` is positive for every rational `N ≥ 3`. -/
theorem ev_ttU_pos (N : ℚ) (h3 : 3 ≤ N) : 0 < ev ttUL N := by
  have hN : 0 < N := by linarith
  rw [ev_ttU N hN.ne']
  have : 0 < N ^ 2 - 1 := by nlinarith
  have : 0 < N ^ 2 - 4 := by nlinarith
  positivity

/-- S = ∅ on the polynomial level: for every integer N ≥ 3, the triangle (N = 3) or the crossed
u-channel box (N ≥ 4) has negative interference. -/
theorem no_coherent_poly (N : ℕ) (h : 3 ≤ N) :
    K tetraL thetaL N < 0 ∨ K boxUL ttUL N < 0 := by
  rcases Nat.eq_or_lt_of_le h with h' | h'
  · left; subst h'; exact_mod_cast K_tri_three_neg
  · right; apply K_boxU_neg; exact_mod_cast h'

end PositiveGeometryEmergentSpaceTime.Surf1
