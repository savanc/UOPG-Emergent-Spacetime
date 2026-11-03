/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.BridgePLCharge

/-!
# GRADED-POSITROID (2026-10-22): Cartan-weight-graded positroid moments vs the anomaly polynomial

Continuous-mode own pick (author approved 2026-10-22).

Each of the 15 SM Weyl states carries a Cartan weight `w = (H3, H8', T3, Y)` with
`H3, H8' ∈ {(1,1), (-1,1), (0,-2)}` (antitriplets negated), `T3 = ±1/2`.
The exchangeable-moment reduction (`polarized_cubic_reduction`) shows that the graded third moment of a positroid
slice is `κ · Σᵢ wᵢᵃ wᵢᵇ wᵢᶜ` once every first moment vanishes, i.e. the Cartan-restricted anomaly polynomial
times a geometry-only constant. Results:
* `graded_cubic_iff_acc`: all graded first/third moments vanish ⇔ the four perturbative ACC (rival-equivalent:
  the graded condition is literally the anomaly polynomial, nothing beyond it).
* `sm_graded_quintic_ne`: the quintic moment along `Y` is nonzero for the SM, so imposing it would exclude the SM.
* `no_proper_anomaly_free_union`: no proper nonempty union of SM multiplets has `Tr Y = Tr Y³ = 0`.
* `graded_charge_blind`: the cross-ratio (u-variable) layer is blind to any Cartan grading.
-/

namespace PositiveGeometryEmergentSpaceTime.GradedPositroid

open PositiveGeometryEmergentSpaceTime.BridgePLAssoc PositiveGeometryEmergentSpaceTime.BridgePLCharge

/-- Polarized exchangeable cubic reduction: with all three first moments zero, an exchangeable third-moment
tensor `(E3, E21, E111)` contracts to `κ · T`, `κ = E3 - 3 E21 + 2 E111`. Here `A, B, C` are the component sums,
`Pab` etc. the pairwise sums, `T` the triple sum. -/
theorem polarized_cubic_reduction (E3 E21 E111 A B C Pab Pac Pbc T : ℝ)
    (hA : A = 0) (hB : B = 0) (hC : C = 0) :
    E3 * T + E21 * (A * Pbc + B * Pac + C * Pab - 3 * T)
      + E111 * (A * B * C - A * Pbc - B * Pac - C * Pab + 2 * T)
      = (E3 - 3 * E21 + 2 * E111) * T := by
  subst hA hB hC; ring

/-- Ordered-triple expansion behind `polarized_cubic_reduction`, on five columns with three
  different gradings. -/
theorem triple_sum_general (a b c : Fin 5 → ℝ) (E3 E21 E111 : ℝ) :
    (∑ i, ∑ j, ∑ k, a i * b j * c k *
        (if i = j ∧ j = k then E3 else if i = j ∨ j = k ∨ i = k then E21 else E111))
      = E3 * (∑ i, a i * b i * c i)
        + E21 * ((∑ i, a i) * (∑ i, b i * c i) + (∑ i, b i) * (∑ i, a i * c i)
            + (∑ i, c i) * (∑ i, a i * b i) - 3 * ∑ i, a i * b i * c i)
        + E111 * ((∑ i, a i) * (∑ i, b i) * (∑ i, c i) - (∑ i, a i) * (∑ i, b i * c i)
            - (∑ i, b i) * (∑ i, a i * c i) - (∑ i, c i) * (∑ i, a i * b i)
            + 2 * ∑ i, a i * b i * c i) := by
  simp only [Fin.sum_univ_five]
  simp (config := { decide := true })
  ring

/-- Cartan weights `(H3, H8', T3, Y)` of the 15 states for hypercharges `(yQ, yu, yd, yL, ye)`
(order: Q r↑ r↓ g↑ g↓ b↑ b↓, uᶜ r̄ ḡ b̄, dᶜ r̄ ḡ b̄, L ↑ ↓, eᶜ). -/
def genW (yQ yu yd yL ye : ℚ) : Fin 15 → Fin 4 → ℚ :=
  ![![1, 1, 1/2, yQ], ![1, 1, -1/2, yQ], ![-1, 1, 1/2, yQ], ![-1, 1, -1/2, yQ],
    ![0, -2, 1/2, yQ], ![0, -2, -1/2, yQ],
    ![-1, -1, 0, yu], ![1, -1, 0, yu], ![0, 2, 0, yu],
    ![-1, -1, 0, yd], ![1, -1, 0, yd], ![0, 2, 0, yd],
    ![0, 0, 1/2, yL], ![0, 0, -1/2, yL], ![0, 0, 0, ye]]

/-- SM weights (`Y`: Q 1/6, uᶜ −2/3, dᶜ 1/3, L −1/2, eᶜ 1). -/
def smW : Fin 15 → Fin 4 → ℚ := genW (1/6) (-2/3) (1/3) (-1/2) 1

/-- Graded first moment (up to the geometric factor `k/n`). -/
def m1 (w : Fin 15 → Fin 4 → ℚ) (a : Fin 4) : ℚ := ∑ i, w i a

/-- Graded cubic tensor `Σᵢ wᵢᵃ wᵢᵇ wᵢᶜ` (the Cartan-restricted anomaly polynomial). -/
def cub (w : Fin 15 → Fin 4 → ℚ) (a b c : Fin 4) : ℚ := ∑ i, w i a * w i b * w i c

/-- The four perturbative ACC (grav, SU(3)²Y, SU(2)²Y, Y³) with SM multiplicities. -/
def ACC (yQ yu yd yL ye : ℚ) : Prop :=
  6 * yQ + 3 * yu + 3 * yd + 2 * yL + ye = 0 ∧ 2 * yQ + yu + yd = 0 ∧ 3 * yQ + yL = 0 ∧
    6 * yQ ^ 3 + 3 * yu ^ 3 + 3 * yd ^ 3 + 2 * yL ^ 3 + ye ^ 3 = 0

/-- Rival equivalence: the graded positroid conditions (all first moments and all third-moment components vanish)
are exactly the four ACC. The graded object adds no condition beyond the anomaly polynomial. -/
theorem graded_cubic_iff_acc (yQ yu yd yL ye : ℚ) :
    ((∀ a, m1 (genW yQ yu yd yL ye) a = 0) ∧ (∀ a b c, cub (genW yQ yu yd yL ye) a b c = 0))
      ↔ ACC yQ yu yd yL ye := by
  constructor
  · rintro ⟨h1, h3⟩
    have g := h1 3
    have c0 := h3 0 0 3
    have c2 := h3 2 2 3
    have c3 := h3 3 3 3
    simp [m1, cub, genW, Fin.sum_univ_succ] at g c0 c2 c3
    refine ⟨by linarith, by linarith, by linarith, by linear_combination c3⟩
  · rintro ⟨h1, h2, h3, h4⟩
    have hd : yd = -2 * yQ - yu := by linarith
    have hL : yL = -3 * yQ := by linarith
    subst hd hL
    have he : ye = 6 * yQ := by linarith
    subst he
    refine ⟨fun a => ?_, fun a b c => ?_⟩
    · fin_cases a <;> simp [m1, genW, Fin.sum_univ_succ] <;> ring
    · fin_cases a <;> fin_cases b <;> fin_cases c <;>
        simp [cub, genW, Fin.sum_univ_succ] <;> first | ring1 | linear_combination h4

/-- The SM satisfies all graded first and third moment conditions. -/
theorem sm_graded_cubic_zero : (∀ a, m1 smW a = 0) ∧ (∀ a b c, cub smW a b c = 0) :=
  (graded_cubic_iff_acc _ _ _ _ _).2 (by unfold ACC; norm_num)

/-- SM weights sum to zero on every Cartan axis. -/
theorem sm_weights_sum_zero (a : Fin 4) : m1 smW a = 0 := sm_graded_cubic_zero.1 a

/-- Quintic moment along `Y` (on `p1 = 0`, `m5 ∝ p5` once `p3 = 0`): `Σ Y⁵ = 5/9 ≠ 0` for the SM, so a
graded quintic-moment condition would EXCLUDE the SM. -/
theorem sm_graded_quintic_ne : (∑ i, smW i 3 ^ 5) = 5 / 9 ∧ (∑ i, smW i 3 ^ 5) ≠ 0 := by
  have h : (∑ i, smW i 3 ^ 5) = 5 / 9 := by
    simp [smW, genW, Fin.sum_univ_succ]; norm_num
  exact ⟨h, by rw [h]; norm_num⟩

/-- G3: no proper nonempty union of whole SM multiplets (6Y = 1, −4, 2, −3, 6; multiplicities 6, 3, 3, 2, 1) has
`Tr Y = 0` and `Tr Y³ = 0` (hence no anomaly-free proper sub-union under any stronger graded condition). -/
theorem no_proper_anomaly_free_union :
    ∀ s : Fin 5 → Bool, (∃ i, s i = true) → (∃ i, s i = false) →
      ¬ ((((if s 0 then 6 * 1 else 0) + (if s 1 then 3 * (-4) else 0) + (if s 2 then 3 * 2 else 0)
            + (if s 3 then 2 * (-3) else 0) + (if s 4 then 6 else 0) : ℤ) = 0) ∧
         (((if s 0 then 6 * 1 else 0) + (if s 1 then 3 * (-64) else 0) + (if s 2 then 3 * 8 else 0)
            + (if s 3 then 2 * (-27) else 0) + (if s 4 then 216 else 0) : ℤ) = 0)) := by
  decide

/-- The cross-ratio (u-variable) layer is blind to any Cartan grading: torus `tᵢ = exp(τ ⟨θ, wᵢ⟩)`. -/
theorem graded_charge_blind (P : Matrix (Fin 2) (Fin 5) ℝ) (w : Fin 5 → Fin 4 → ℝ) (θ : Fin 4 → ℝ) (τ : ℝ)
    (a b c d : Fin 5) :
    uCR (torusAct P fun i => Real.exp (τ * ∑ j, θ j * w i j)) a b c d = uCR P a b c d :=
  uCR_charge_blind P (fun i => ∑ j, θ j * w i j) τ a b c d

/-- Bundle (GRADED-POSITROID): graded conditions ⇔ ACC (rival-equivalent, nothing new); quintic excludes the SM;
no proper anomaly-free union; u-variables grading-blind. -/
theorem graded_positroid_nolink (P : Matrix (Fin 2) (Fin 5) ℝ) (w : Fin 5 → Fin 4 → ℝ) (θ : Fin 4 → ℝ)
    (τ : ℝ) (a b c d : Fin 5) :
    (∀ yQ yu yd yL ye : ℚ, ((∀ a, m1 (genW yQ yu yd yL ye) a = 0) ∧
        (∀ a b c, cub (genW yQ yu yd yL ye) a b c = 0)) ↔ ACC yQ yu yd yL ye) ∧
    (∑ i, smW i 3 ^ 5) ≠ 0 ∧
    uCR (torusAct P fun i => Real.exp (τ * ∑ j, θ j * w i j)) a b c d = uCR P a b c d :=
  ⟨graded_cubic_iff_acc, sm_graded_quintic_ne.2, graded_charge_blind P w θ τ a b c d⟩

end PositiveGeometryEmergentSpaceTime.GradedPositroid
