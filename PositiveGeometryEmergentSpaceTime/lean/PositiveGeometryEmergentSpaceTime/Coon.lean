/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
M3c: the Coon q-deformation of the Lovelace–Shapiro pion amplitude and the even/odd balance ε.
Pre-registration: `prereg/M3c-coon-2026-10-11.md`. Numbers: `scripts/m3c_coon.py` (script, not Lean).
Conventions: α′ = 1, `r = √q`, `c = 1 - r²`. Family F_B (α0 = [1/2]_q = 1/(1+√q)):
`σ = r - c s`, `τ = r - c u`. Low-energy jet `M = g10 (s+u) + g20 (s²+u²) + 2 g21 su + O(3)`, ε = 1 - g21/g20.
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.LECRatio

namespace PositiveGeometryEmergentSpaceTime.Coon

/-! ## C1. Zero-curve lemma: ε is the curvature of the amplitude's zero set at the Adler point -/

/-- The O(p²)+O(p⁴) jet restricted to the curve `u = -s + k s²` equals
`(g10 k + 2 g20 - 2 g21) s²` plus an explicit `s³` remainder. -/
theorem jet_on_curve (g10 g20 g21 k s : ℝ) :
    g10 * (s + (-s + k * s ^ 2)) + g20 * (s ^ 2 + (-s + k * s ^ 2) ^ 2) + 2 * g21 * s * (-s + k * s ^ 2)
      = (g10 * k + 2 * g20 - 2 * g21) * s ^ 2 + s ^ 3 * (g20 * (-2 * k + k ^ 2 * s) + 2 * g21 * k) := by
  ring

/-- If the jet vanishes to order s² along `u = -s + k s²`, then `ε = 1 - g21/g20 = -k g10 / (2 g20)`.
The hidden zero is `k = 0` (ε = 0); the ρ side ε < 0 needs `k > 0` when `g10, g20 > 0`. -/
theorem eps_of_curvature (g10 g20 g21 k : ℝ) (hg : g20 ≠ 0) (h : g10 * k + 2 * g20 - 2 * g21 = 0) :
    1 - g21 / g20 = -k * g10 / (2 * g20) := by
  field_simp; linarith

/-- Sign rule: with `g10, g20 > 0`, the zero curve bends toward `su > 0`-side (`k < 0`) iff ε > 0
  (scalar side). -/
theorem eps_pos_iff (g10 g20 g21 k : ℝ) (h10 : 0 < g10) (h20 : 0 < g20)
    (h : g10 * k + 2 * g20 - 2 * g21 = 0) : 0 < 1 - g21 / g20 ↔ k < 0 := by
  rw [eps_of_curvature g10 g20 g21 k h20.ne' h, neg_mul, neg_div, neg_pos]
  constructor
  · intro hk; by_contra hk'; push Not at hk'
    have : 0 ≤ k * g10 / (2 * g20) := div_nonneg (mul_nonneg hk' h10.le) (by linarith)
    linarith
  · intro hk; exact div_neg_of_neg_of_pos (mul_neg_of_neg_of_pos hk h10) (by linarith)

/-! ## C2. Family F_B: the n = 0 numerator `στ - q` and its jet -/

/-- Exact: with `σ = r - c s`, `τ = r - c u`, `c = 1 - r²`, `q = r²`:
`στ - q = -c (r (s+u) - c su)`. It vanishes at the origin (no constant term: Adler-type zero). -/
theorem stau_sub_q (r s u : ℝ) :
    (r - (1 - r ^ 2) * s) * (r - (1 - r ^ 2) * u) - r ^ 2
      = -(1 - r ^ 2) * (r * (s + u) - (1 - r ^ 2) * (s * u)) := by ring

/-- `στ − q` vanishes at the origin `s = u = 0` (no constant term). -/
theorem stau_origin (r : ℝ) : (r - (1 - r ^ 2) * 0) * (r - (1 - r ^ 2) * 0) - r ^ 2 = 0 := by ring

/-- On the old hidden-zero line `u = -s`, `στ - q = -c² s²`, nonzero for `s ≠ 0`, `r² ≠ 1`:
the q-deformation breaks the exact hidden zero (it moves to the curve `r(s+u) = c su`). -/
theorem stau_on_line (r s : ℝ) :
    (r - (1 - r ^ 2) * s) * (r - (1 - r ^ 2) * (-s)) - r ^ 2 = -((1 - r ^ 2) ^ 2 * s ^ 2) := by ring

/-- On the line `u = −s`, `στ − q ≠ 0` whenever `s ≠ 0` and `r² ≠ 1`: the exact hidden zero is not
  preserved by the q-deformation. -/
theorem stau_on_line_ne (r s : ℝ) (hr : r ^ 2 ≠ 1) (hs : s ≠ 0) :
    (r - (1 - r ^ 2) * s) * (r - (1 - r ^ 2) * (-s)) - r ^ 2 ≠ 0 := by
  rw [stau_on_line]
  have h1 : (1 - r ^ 2) ≠ 0 := sub_ne_zero.mpr (Ne.symm hr)
  exact neg_ne_zero.mpr (mul_ne_zero (pow_ne_zero 2 h1) (pow_ne_zero 2 hs))

/-- Jet of `K · (στ - q)` for any symmetric prefactor `K = K0 + K1 (s+u) + O(2)` (this covers C = 1 and FPRS's
polynomial-residue C alike): `g10 = -c r K0`, `g20 = -c r K1`, `g21 = -c r K1 + c² K0 / 2`. Stated as the exact
quadratic identity. -/
theorem jetB (r K0 K1 s u : ℝ) :
    (K0 + K1 * (s + u)) * (-(1 - r ^ 2) * (r * (s + u) - (1 - r ^ 2) * (s * u)))
      = (-(1 - r ^ 2) * r * K0) * (s + u) + (-(1 - r ^ 2) * r * K1) * (s ^ 2 + u ^ 2)
        + 2 * (-(1 - r ^ 2) * r * K1 + (1 - r ^ 2) ^ 2 * K0 / 2) * (s * u)
        + (1 - r ^ 2) ^ 2 * K1 * (s + u) * (s * u) := by ring

/-- Hence, exactly, `g21 = g20 - c g10 / (2r)` and `ε = c g10 / (2 r g20)`. -/
theorem epsB (r K0 K1 : ℝ) (hr : r ≠ 0) (h20 : -(1 - r ^ 2) * r * K1 ≠ 0) :
    1 - (-(1 - r ^ 2) * r * K1 + (1 - r ^ 2) ^ 2 * K0 / 2) / (-(1 - r ^ 2) * r * K1)
      = (1 - r ^ 2) * (-(1 - r ^ 2) * r * K0) / (2 * r * (-(1 - r ^ 2) * r * K1)) := by
  have hc : (1 - r ^ 2) ≠ 0 := by intro h; apply h20; rw [h]; ring
  have hK : K1 ≠ 0 := by intro h; apply h20; rw [h]; ring
  have hd : 2 * r * (-(1 - r ^ 2) * r * K1) ≠ 0 := mul_ne_zero (mul_ne_zero two_ne_zero hr) h20
  rw [one_sub_div h20, div_eq_div_iff h20 hd]
  ring

/-- **Wrong side.** For `0 < r < 1` (`0 < q < 1`) and positive `g10, g20` (as unitarity requires),
F_B has ε > 0: the Adler-compatible Coon deformation moves the spin balance toward scalars, never toward ρ. -/
theorem epsB_pos (r g10 g20 : ℝ) (hr0 : 0 < r) (hr1 : r < 1) (h10 : 0 < g10) (h20 : 0 < g20) :
    0 < (1 - r ^ 2) * g10 / (2 * r * g20) := by
  have : 0 < 1 - r ^ 2 := by nlinarith
  positivity

/-- Derivative at q = 1: `f(q) = (1-q)/(2√q)` has `f(1) = 0`, `f'(1) = -1/2`; so for ANY differentiable `h`
(here `h = g10/g20`), `(f h)'(1) = -h(1)/2`. With the LS value `h(1) = 1/(2 ln 2)` (M3/AR) this is
`dε/dq|_{q=1} = -1/(4 ln 2) < 0`. -/
theorem f_hasDerivAt : HasDerivAt (fun q : ℝ => (1 - q) / (2 * Real.sqrt q)) (-1 / 2) 1 := by
  have hs : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt 1)) 1 := Real.hasDerivAt_sqrt (by norm_num)
  have h2 : HasDerivAt (fun q : ℝ => 2 * Real.sqrt q) (2 * (1 / (2 * Real.sqrt 1))) 1 := hs.const_mul 2
  have h1 : HasDerivAt (fun q : ℝ => 1 - q) (-1) 1 := by
    simpa using (hasDerivAt_id (1 : ℝ)).const_sub 1
  have hne : 2 * Real.sqrt 1 ≠ 0 := by simp
  have := h1.div h2 hne
  convert this using 1
  simp [Real.sqrt_one]; norm_num

/-- Product rule at `q = 1`: for any `h` differentiable at 1, `(1 − q)/(2√q) · h(q)` has derivative
  `−h(1)/2` at `q = 1`. -/
theorem eps_slope (h : ℝ → ℝ) (h' : ℝ) (hh : HasDerivAt h h' 1) :
    HasDerivAt (fun q => (1 - q) / (2 * Real.sqrt q) * h q) (-1 / 2 * h 1) 1 := by
  have := f_hasDerivAt.mul hh
  convert this using 1
  simp

/-- Sign check: `−½ · 1/(2 ln 2) < 0` (the LS value plugged into `eps_slope`). -/
theorem ls_slope_neg : -1 / 2 * (1 / (2 * Real.log 2)) < 0 := by
  have := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  have : 0 < 1 / (2 * Real.log 2) := by positivity
  linarith

/-! ## C3. Region facts for the computed (rounded) values — exact ℚ arithmetic, not physics -/

/-- F_B at q = 1/2 (script): g20/g10 = 1.949654, g21/g10 = 1.596101. Inside AR's wedge (R_full), outside
the M3b family (g21 < g20, scalar side); ε = 0.181342 matches `c/(2r) · g10/g20` to 6 digits. -/
theorem fB_half_regions :
    (0 : ℚ) ≤ 1596101 / 10 ^ 6 ∧ (1596101 / 10 ^ 6 : ℚ) ≤ 2 * (1949654 / 10 ^ 6) ∧
      (1596101 / 10 ^ 6 : ℚ) < 1949654 / 10 ^ 6 := by norm_num

/-- F_B at q = 0.02 (largest ε on the grid): ε = 0.436 < 1, still inside R_full, far from the ρ
  side. -/
theorem fB_002_regions : (0 : ℚ) ≤ 4482049 / 10 ^ 6 ∧ (4482049 / 10 ^ 6 : ℚ) ≤ 2 * (7946873 / 10 ^ 6) ∧
    (4482049 / 10 ^ 6 : ℚ) < 7946873 / 10 ^ 6 := by norm_num

/-- F_A (FPRS Coon, α0 = 1/2): the most negative ε on the grid is ≈ -0.0230 (q = 0.5), far above -1/2; at q = 1/2
(g20/g10 = 1.640640, g21/g10 = 1.678260) it is inside the M3b family interval g20 ≤ g21 ≤ 2 g20 (ρ side, barely). -/
theorem fA_min_far_from_rho : (-1 / 2 : ℚ) < -230 / 10 ^ 4 ∧
    (1678260 / 10 ^ 6 : ℚ) ≤ 2 * (1640640 / 10 ^ 6) ∧ (1640640 / 10 ^ 6 : ℚ) ≤ 1678260 / 10 ^ 6 := by norm_num

end PositiveGeometryEmergentSpaceTime.Coon
