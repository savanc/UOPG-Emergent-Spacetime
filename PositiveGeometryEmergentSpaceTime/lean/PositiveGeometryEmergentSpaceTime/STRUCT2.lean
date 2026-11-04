/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT1
/-!
# STRUCT-2: does anomaly consistency fix the number of colours? (2026-10-15)
One generation with N_c colours: Q (N_c,2,yQ), uᶜ (N_c̄,1,yu), dᶜ (N_c̄,1,yd), L (1,2,yL), eᶜ (1,1,ye), no νᶜ.
Perturbative anomaly conditions `ACCN` (CITED coefficients) and the SU(2) Witten condition (CITED: the number
N_c + 1 of doublets is even). Results: for N_c ≠ 0, yQ ≠ 0 the charges are yQ·(N_c−1, −N_c−1, −N_c, 2N_c) or with uᶜ↔dᶜ;
a solution exists for every N_c; Witten ⇔ N_c odd; N_c = 3 and N_c = 5 both pass, so consistency does not single out 3.
No positive-geometry input.
-/
namespace PositiveGeometryEmergentSpaceTime.STRUCT2

/-- Perturbative anomaly conditions with `N_c` colours.
Also known as: Nc (number of colours), STRUCT2.N. -/
def ACCN (N_c yQ yu yd yL ye : ℚ) : Prop :=
  2 * yQ + yu + yd = 0 ∧ N_c * yQ + yL = 0 ∧
  2 * N_c * yQ + N_c * yu + N_c * yd + 2 * yL + ye = 0 ∧
  2 * N_c * yQ ^ 3 + N_c * yu ^ 3 + N_c * yd ^ 3 + 2 * yL ^ 3 + ye ^ 3 = 0

/-- Witten SU(2) global-anomaly condition (CITED): even number of doublets (N_c colour doublets + 1
  lepton doublet). -/
def Witten (N_c : ℕ) : Prop := Even (N_c + 1)

/-- Cubic condition on the linear solution space. -/
theorem cubicN_factor (N_c yQ yu : ℚ) :
    2 * N_c * yQ ^ 3 + N_c * yu ^ 3 + N_c * (-2 * yQ - yu) ^ 3 + 2 * (-N_c * yQ) ^ 3 + (2 * N_c * yQ) ^ 3
      = -6 * N_c * yQ * (yQ + yu - N_c * yQ) * (yQ + yu + N_c * yQ) := by ring

/-- N1: for N_c ≠ 0 and yQ ≠ 0 the hypercharges are fixed up to normalisation and uᶜ↔dᶜ. -/
theorem accN_unique {N_c yQ yu yd yL ye : ℚ} (h : ACCN N_c yQ yu yd yL ye) (hN : N_c ≠ 0) (hQ : yQ ≠ 0) :
    (yu = (N_c - 1) * yQ ∧ yd = -(N_c + 1) * yQ ∧ yL = -N_c * yQ ∧ ye = 2 * N_c * yQ) ∨
    (yu = -(N_c + 1) * yQ ∧ yd = (N_c - 1) * yQ ∧ yL = -N_c * yQ ∧ ye = 2 * N_c * yQ) := by
  obtain ⟨h3, h2, hg, hc⟩ := h
  have hd : yd = -2 * yQ - yu := by linarith
  have hL : yL = -N_c * yQ := by linarith
  have he : ye = 2 * N_c * yQ := by
    have : N_c * (2 * yQ + yu + yd) = 0 := by rw [h3]; ring
    nlinarith [this]
  subst hd hL he
  have hf := cubicN_factor N_c yQ yu
  rw [hc] at hf
  have h6 : -6 * N_c * yQ ≠ 0 := by
    have : (-6 : ℚ) ≠ 0 := by norm_num
    exact mul_ne_zero (mul_ne_zero this hN) hQ
  have hp : (yQ + yu - N_c * yQ) * (yQ + yu + N_c * yQ) = 0 := by
    have : -6 * N_c * yQ * ((yQ + yu - N_c * yQ) * (yQ + yu + N_c * yQ)) = 0 := by linarith [hf]
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h h6
    · exact h
  rcases mul_eq_zero.mp hp with h | h
  · left; refine ⟨by linarith, by linarith, rfl, rfl⟩
  · right; refine ⟨by linarith, by linarith, rfl, rfl⟩

/-- N2 (exclusion): for every N_c there is an anomaly-free assignment, so the ACC do not fix N_c. -/
theorem accN_solution (N_c : ℚ) : ACCN N_c 1 (N_c - 1) (-(N_c + 1)) (-N_c) (2 * N_c) := by
  refine ⟨by ring, by ring, by ring, by ring⟩

/-- At N_c = 3 this is STRUCT-1's SM branch (consistency with `STRUCT1.ACC`). -/
theorem accN_three_eq_struct1 {yQ yu yd yL ye : ℚ} :
    ACCN 3 yQ yu yd yL ye ↔ PositiveGeometryEmergentSpaceTime.STRUCT1.ACC yQ yu yd yL ye := by
  unfold ACCN PositiveGeometryEmergentSpaceTime.STRUCT1.ACC
  constructor <;> rintro ⟨a, b, c, d⟩ <;> refine ⟨by linarith, by linarith, by linarith,
      by linarith⟩

/-- N3: Witten ⇔ N_c odd. -/
theorem witten_iff_odd (N_c : ℕ) : Witten N_c ↔ Odd N_c := by
  unfold Witten; rw [Nat.even_add_one, Nat.not_even_iff_odd]

/-- N4 (exclusion): N_c = 3 and N_c = 5 both satisfy ACC + Witten — consistency does not single out N_c =
  3. -/
theorem three_not_selected :
    (ACCN 3 1 2 (-4) (-3) 6 ∧ Witten 3) ∧ (ACCN 5 1 4 (-6) (-5) 10 ∧ Witten 5) := by
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · have := accN_solution 3; norm_num at this ⊢; exact this
  · exact ⟨2, rfl⟩
  · have := accN_solution 5; norm_num at this ⊢; exact this
  · exact ⟨3, rfl⟩

/-- Witness that Witten is a real constraint: N_c = 2 fails it. -/
theorem witten_excludes_two : ¬ Witten 2 := by
  rw [witten_iff_odd]; decide

end PositiveGeometryEmergentSpaceTime.STRUCT2
