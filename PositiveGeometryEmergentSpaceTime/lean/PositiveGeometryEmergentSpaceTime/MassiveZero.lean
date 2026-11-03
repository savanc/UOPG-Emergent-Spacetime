/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-2: algebraic content of the massive 4-point hidden zero (units M_π² = 1).
Ordered amplitude f(x,y) (x = s12, y = s23), symmetric under x ↔ y.
Massive hidden zero (M2f / Carrillo González–Ward 2601.16860): f vanishes on the line x + y = 2.
SU(2) dressing (M2f `dressing_coeff`): A(s,t,u) = 2(f s t + f s u - f u t + f u s - f t u + f t s).
-/

namespace PositiveGeometryEmergentSpaceTime.MassiveZero

/-- SU(2) dressing of an ordered amplitude (same trace coefficients as M2f `dressing_coeff`). -/
def dress (f : ℝ → ℝ → ℝ) (s t u : ℝ) : ℝ :=
  2 * (f s t + f s u - f u t + f u s - f t u + f t s)

/-- Any symmetric ordered amplitude with the massive hidden zero gives A(1,1,2) = 0:
the full isospin amplitude vanishes at the Mandelstam-triangle point P = (M², M², 2M²). -/
theorem dress_zero_at_P (f : ℝ → ℝ → ℝ) (hsym : ∀ x y, f x y = f y x)
    (hz : ∀ x y, x + y = 2 → f x y = 0) : dress f 1 1 2 = 0 := by
  unfold dress
  have h11 : f 1 1 = 0 := hz 1 1 (by norm_num)
  rw [hsym 2 1, h11]
  ring

/-- General O(p⁴) symmetric ordered polynomial plus the LO term κ(x+y-2). -/
def fpoly (κ a1 a2 a3 a4 : ℝ) (x y : ℝ) : ℝ :=
  κ * (x + y - 2) + a1 * (x ^ 2 + y ^ 2) + a2 * (x * y) + a3 * (x + y) + a4

/-- The massive hidden zero holds for the polynomial iff a2 = 2 a1 (the massless/M3 condition)
and 4 a1 + 2 a3 + a4 = 0 (the new mass-dependent condition). -/
theorem poly_zero_iff (κ a1 a2 a3 a4 : ℝ) :
    (∀ x y,
        x + y = 2 → fpoly κ a1 a2 a3 a4 x y = 0) ↔ (a2 = 2 * a1 ∧ 4 * a1 + 2 * a3 + a4 = 0) := by
  constructor
  · intro h
    have h0 := h 1 1 (by norm_num)
    have h1 := h 0 2 (by norm_num)
    unfold fpoly at h0 h1
    constructor <;> nlinarith
  · rintro ⟨ha, hb⟩ x y hxy
    unfold fpoly
    have hy : y = 2 - x := by linarith
    subst hy; subst ha
    nlinarith [hb]

/-- At P the dressed polynomial equals 4·f(1,1) = 4(2a1 + a2 + 2a3 + a4) (LO term drops out). -/
theorem dress_poly_at_P (κ a1 a2 a3 a4 : ℝ) :
    dress (fpoly κ a1 a2 a3 a4) 1 1 2 = 4 * (2 * a1 + a2 + 2 * a3 + a4) := by
  unfold dress fpoly; ring

/-- LO alone (Weinberg) vanishes at P: A_LO = s - 1 at s = 1. -/
theorem lo_zero_at_P : (1 : ℝ) - 1 = 0 := by norm_num

/-- Tree-level SU(2) polynomial c0 + c1 s + c2 s² + c3 (t-u)² evaluated at P = (1,1,2). -/
theorem su2_poly_at_P (c0 c1 c2 c3 : ℝ) :
    c0 + c1 * 1 + c2 * 1 ^ 2 + c3 * (1 - 2) ^ 2 = c0 + c1 + c2 + c3 := by ring

/-- One-loop G¹(s,t) polynomial (BCEGS eq. 4.15) vanishes at (s,t) = (1,2): only G¹(1,1) survives at P,
and F¹(1) = 0. -/
theorem g1_poly_vanishes : (14 : ℝ) - 4 * 1 - 10 * 2 + 1 * 2 + 2 * 2 ^ 2 = 0 := by norm_num
/-- Arithmetic: the one-loop polynomial `14 − 4s − 10t + st + 2t²` equals 3 at `(s, t) = (1, 1)`. -/
theorem g1_poly_at_11 : (14 : ℝ) - 4 * 1 - 10 * 1 + 1 * 1 + 2 * 1 ^ 2 = 3 := by norm_num
/-- Arithmetic: `1² − 1 = 0`. -/
theorem f1_poly_at_1 : (1 : ℝ) ^ 2 - 1 = 0 := by norm_num

end PositiveGeometryEmergentSpaceTime.MassiveZero
