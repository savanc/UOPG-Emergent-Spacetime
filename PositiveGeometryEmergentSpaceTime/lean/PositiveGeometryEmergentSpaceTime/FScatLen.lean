/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# F-SCATLEN — S-wave ππ scattering lengths of linear (Adler-zero) and Lovelace–Shapiro amplitudes

Also known as: F-SCATLEN, threshold isospin projections T⁰, T² of an `A(s,t,u)` pion amplitude.
`T⁰ = 3A(s,t,u) + A(t,s,u) + A(u,t,s)`, `T² = A(t,s,u) + A(u,t,s)`, at threshold `s = 4m², t = u = 0`;
`a₀^I = T^I/(32π)`.
* Linear amplitude `A = (s − s_A)/F²` (Adler point `s_A`): `T⁰ = (12m² − 5s_A)/F²`, `T² = −2s_A/F²`;
  Weinberg (`s_A = m²`): 7, −2; Adler-at-zero (`s_A = 0`, the F-DIM-MASS repair P_b): 12, 0;
  `2T⁰ − 5T² = 24m²/F²` for every `s_A`.
* Dual (LS-type) amplitude `λ[V(s,t) + V(s,u) − V(t,u)]` with symmetric `V`: `T² = 2λV(0,0)` at threshold;
  for LS with `α₀ = ½` this is exactly 0 (`1/Γ(0) = 0`; Lean's `0⁻¹ = 0` coincides with the entire `1/Γ`).
* Normalisation N1: `λ = −1/(2πα′F²)` turns the soft LS limit `π(1 − 2α(s))` on the Adler line into `(s − m²)/F²`.
No axioms; amplitudes CITED (Weinberg 1966; Lovelace 1968).
-/

namespace PositiveGeometryEmergentSpaceTime.FScatLen

/-- Threshold isospin-0 combination. Also known as: `T⁰`. -/
def isoT0 (A : ℝ → ℝ → ℝ → ℝ) (s t u : ℝ) : ℝ := 3 * A s t u + A t s u + A u t s

/-- Threshold isospin-2 combination. Also known as: `T²`. -/
def isoT2 (A : ℝ → ℝ → ℝ → ℝ) (s t u : ℝ) : ℝ := A t s u + A u t s

/-- Linear Adler-zero amplitude `(s − s_A)/F²`. Also known as: current-algebra amplitude; Weinberg
  at `s_A = m²`. -/
noncomputable def linAmp (sA F2 : ℝ) (s _t _u : ℝ) : ℝ := (s - sA) / F2

/-- Dual (Lovelace-type) crossing combination `λ[V(s,t) + V(s,u) − V(t,u)]`. -/
def dualAmp (V : ℝ → ℝ → ℝ) (lam : ℝ) (s t u : ℝ) : ℝ := lam * (V s t + V s u - V t u)

/-- Lovelace–Shapiro building block `Γ(1−α(s))Γ(1−α(t))/Γ(1−α(s)−α(t))`, `α(s) = α₀ + α′s`. Also
  known as: `V(s,t)`. -/
noncomputable def lsV (alpha0 ap : ℝ) (s t : ℝ) : ℝ :=
  Real.Gamma (1 - (alpha0 + ap * s)) * Real.Gamma (1 - (alpha0 + ap * t)) *
    (Real.Gamma (1 - (alpha0 + ap * s) - (alpha0 + ap * t)))⁻¹

/-- Isospin-0 threshold value of the linear amplitude `(s − s_A)/F²`: `T⁰ = (12m² − 5s_A)/F²`. -/
theorem lin_T0 (sA F2 m2 : ℝ) : isoT0 (linAmp sA F2) (4 * m2) 0 0 = (12 * m2 - 5 * sA) / F2 := by
  unfold isoT0 linAmp; ring

/-- Isospin-2 threshold value of the linear amplitude `(s − s_A)/F²`: `T² = −2s_A/F²`. -/
theorem lin_T2 (sA F2 m2 : ℝ) : isoT2 (linAmp sA F2) (4 * m2) 0 0 = -2 * sA / F2 := by
  unfold isoT2 linAmp; ring

/-- Weinberg LO: `32π a₀⁰ = 7m²/F²`. -/
theorem lin_weinberg_T0 (F2 m2 : ℝ) : isoT0 (linAmp m2 F2) (4 * m2) 0 0 = 7 * m2 / F2 := by
  rw [lin_T0]; ring

/-- Weinberg LO: `32π a₀² = −2m²/F²`. -/
theorem lin_weinberg_T2 (F2 m2 : ℝ) : isoT2 (linAmp m2 F2) (4 * m2) 0 0 = -2 * m2 / F2 := lin_T2 _ _ _

/-- Adler zero at `s = 0` (P_b, linearised): `32π a₀⁰ = 12m²/F²`. -/
theorem lin_adlerZero_T0 (F2 m2 : ℝ) : isoT0 (linAmp 0 F2) (4 * m2) 0 0 = 12 * m2 / F2 := by
  rw [lin_T0]; ring

/-- Adler zero at `s = 0` (P_b, linearised): `a₀² = 0`. -/
theorem lin_adlerZero_T2 (F2 m2 : ℝ) : isoT2 (linAmp 0 F2) (4 * m2) 0 0 = 0 := by
  rw [lin_T2]; ring

/-- The broken claim "P_b reproduces Weinberg's a₀²" is false for `m² ≠ 0`, `F² ≠ 0`. -/
theorem lin_adlerZero_T2_ne_weinberg {F2 m2 : ℝ} (hF : F2 ≠ 0) (hm : m2 ≠ 0) :
    isoT2 (linAmp 0 F2) (4 * m2) 0 0 ≠ isoT2 (linAmp m2 F2) (4 * m2) 0 0 := by
  rw [lin_adlerZero_T2, lin_weinberg_T2]
  intro h
  have : -2 * m2 = 0 := by
    have := congrArg (· * F2) h; field_simp at this; linarith
  exact hm (by linarith)

/-- Ratio of the linearised P_b and Weinberg isospin-0 scattering lengths: 12/7. -/
theorem lin_adlerZero_ratio {F2 m2 : ℝ} (hF : F2 ≠ 0) (hm : m2 ≠ 0) :
    isoT0 (linAmp 0 F2) (4 * m2) 0 0 / isoT0 (linAmp m2 F2) (4 * m2) 0 0 = 12 / 7 := by
  rw [lin_adlerZero_T0, lin_weinberg_T0]; field_simp

/-- `2T⁰ − 5T² = 24m²/F²` for every Adler point `s_A`: the combination cannot see where the Adler
  zero sits. -/
theorem lin_combination_invariant (sA F2 m2 : ℝ) :
    2 * isoT0 (linAmp sA F2) (4 * m2) 0 0 - 5 * isoT2 (linAmp sA F2) (4 * m2) 0 0 = 24 * m2 / F2 := by
  rw [lin_T0, lin_T2]; ring

/-- Dual amplitude with symmetric `V`: threshold `T² = 2λV(0,0)`. -/
theorem dual_T2_threshold (V : ℝ → ℝ → ℝ) (hV : ∀ a b, V a b = V b a) (lam S : ℝ) :
    isoT2 (dualAmp V lam) S 0 0 = 2 * lam * V 0 0 := by
  unfold isoT2 dualAmp; rw [hV 0 S]; ring

/-- The Lovelace–Shapiro building block `lsV` is symmetric in its two arguments. -/
theorem lsV_symm (alpha0 ap : ℝ) (a b : ℝ) : lsV alpha0 ap a b = lsV alpha0 ap b a := by
  unfold lsV; rw [mul_comm (Real.Gamma _) (Real.Gamma _)]; ring_nf

/-- LS at `α₀ = ½` (P_b): `V(0,0) = Γ(½)²/Γ(0) = 0` (`1/Γ` vanishes at 0). -/
theorem lsV_half_zero (ap : ℝ) : lsV (1 / 2) ap 0 0 = 0 := by
  unfold lsV
  have : (1 : ℝ) - (1 / 2 + ap * 0) - (1 / 2 + ap * 0) = 0 := by ring
  rw [this, Real.Gamma_zero, inv_zero, mul_zero]

/-- P_b, exact (all orders in α′): the LS amplitude with `α₀ = ½` has `a₀² = 0` at threshold. -/
theorem ls_adlerZero_a02_exact (ap lam S : ℝ) : isoT2 (dualAmp (lsV (1 / 2) ap) lam) S 0 0 = 0 := by
  rw [dual_T2_threshold _ (lsV_symm _ _) lam S, lsV_half_zero]; ring

/-- Crossing combination of the soft LS limit: `(1−x−y) + (1−x−z) − (1−y−z) = 1 − 2x`. -/
theorem soft_crossing (x y z : ℝ) : (1 - x - y) + (1 - x - z) - (1 - y - z) = 1 - 2 * x := by ring

/-- `Γ(½)² = π` (the soft-limit constant of `V`). -/
theorem gamma_half_sq : Real.Gamma (1 / 2) ^ 2 = Real.pi := by
  rw [Real.Gamma_one_half_eq, Real.sq_sqrt Real.pi_pos.le]

/-- Normalisation N1: `λ = −1/(2πα′F²)` maps the soft LS limit `λπ(1 − 2α(s))` on the Adler line
`α₀ = ½ − α′m²` to Weinberg's `(s − m²)/F²`. -/
theorem ls_soft_normalisation {ap F2 : ℝ} (hap : ap ≠ 0) (hF : F2 ≠ 0) (m2 s : ℝ) :
    (-1 / (2 * Real.pi * ap * F2)) * Real.pi * (1 - 2 * ((1 / 2 - ap * m2) + ap * s)) = (s - m2) / F2 := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp; ring

/-- Bundle (F-SCATLEN): Weinberg (7, −2); P_b linear (12, 0); P_b exact `a₀² = 0`; N1 normalisation. -/
theorem fscatlen_threshold (F2 m2 ap lam S : ℝ) :
    isoT0 (linAmp m2 F2) (4 * m2) 0 0 = 7 * m2 / F2 ∧ isoT2 (linAmp m2 F2) (4 * m2) 0 0 = -2 * m2 / F2 ∧
    isoT0 (linAmp 0 F2) (4 * m2) 0 0 = 12 * m2 / F2 ∧ isoT2 (linAmp 0 F2) (4 * m2) 0 0 = 0 ∧
    isoT2 (dualAmp (lsV (1 / 2) ap) lam) S 0 0 = 0 :=
  ⟨lin_weinberg_T0 _ _, lin_weinberg_T2 _ _, lin_adlerZero_T0 _ _, lin_adlerZero_T2 _ _,
    ls_adlerZero_a02_exact _ _ _⟩

end PositiveGeometryEmergentSpaceTime.FScatLen
