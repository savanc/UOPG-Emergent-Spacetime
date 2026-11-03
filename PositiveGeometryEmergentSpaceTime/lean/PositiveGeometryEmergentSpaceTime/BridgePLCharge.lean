/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.BridgePLAssoc

/-!
# BRIDGE-PL-ASSOC (charge rung, 2026-10-20): can the Plücker → torus → hypersimplex → associahedron chain see a U(1) charge?

Also known as: BRIDGE-PL-ASSOC mission rung, BRIDGE-PL-CHARGE. Standard maps CITED (GGMS 1987; Speyer–Williams
math/0312297; Arkani-Hamed–Bai–Lam 1703.04541; ABHY 1711.09102; Arkani-Hamed–He–Lam 1912.08707; Lukowski–Parisi–Williams
2002.06164). A U(1) charge vector `λ` enters `Gr(2,n)` only as a cocharacter of the column torus: `P ↦ P · diag(t)`,
`tᵢ = exp(τ λᵢ)`.
* M1 (quotient level): `pl5_torus` (Plücker weights `tᵢ tⱼ`), `uCR_torus_invariant` (every cross-ratio / u-variable is
  torus-invariant for EVERY `t`), `pos_torus` (positivity preserved for `t > 0`), `X13mono_torus` (chart monomials only
  pick up a common weight). Hence associahedron data are charge-blind: SM and rival charges are indistinguishable.
* M2 (equivariant level): `sym_cubic_reduction` — for any `Sₙ`-symmetric measure the cubic moment of `⟨λ, μ⟩` on
  `Tr λ = 0` is `κ · Tr λ³` with `κ = E₃ − 3E₂₁ + 2E₁₁₁`; `cube_kappa_zero`, `simplex_kappa_pos` (rivals; moments CITED).
No axioms.
-/

open Matrix

namespace PositiveGeometryEmergentSpaceTime.BridgePLCharge

open PositiveGeometryEmergentSpaceTime.BridgePLAssoc

/-- Column-torus action `P ↦ P · diag(t)` (charge cocharacter). -/
def torusAct (P : Matrix (Fin 2) (Fin 5) ℝ) (t : Fin 5 → ℝ) : Matrix (Fin 2) (Fin 5) ℝ :=
  P * Matrix.diagonal t

/-- Under the column-torus action `P ↦ P · diag(t)`, each Plücker coordinate scales by `tᵢ tⱼ`. -/
theorem pl5_torus (P : Matrix (Fin 2) (Fin 5) ℝ) (t : Fin 5 → ℝ) (i j : Fin 5) :
    pl5 (torusAct P t) i j = t i * t j * pl5 P i j := by
  simp only [pl5_eq, torusAct, Matrix.mul_diagonal]; ring

/-- Plücker cross-ratio `⟨ab⟩⟨cd⟩/(⟨ac⟩⟨bd⟩)` (the u-variables of `M₀,ₙ⁺ = Gr₊(2,n)/T` are of this
  form). -/
noncomputable def uCR (P : Matrix (Fin 2) (Fin 5) ℝ) (a b c d : Fin 5) : ℝ :=
  pl5 P a b * pl5 P c d / (pl5 P a c * pl5 P b d)

/-- M1: every cross-ratio is invariant under every nonvanishing torus element (any charge vector). -/
theorem uCR_torus_invariant (P : Matrix (Fin 2) (Fin 5) ℝ) (t : Fin 5 → ℝ) (ht : ∀ i, t i ≠ 0)
    (a b c d : Fin 5) : uCR (torusAct P t) a b c d = uCR P a b c d := by
  unfold uCR
  simp only [pl5_torus]
  have hk : t a * t b * t c * t d ≠ 0 := by
    have := ht a; have := ht b; have := ht c; have := ht d; positivity
  rw [show t a * t b * pl5 P a b * (t c * t d * pl5 P c d)
      = (t a * t b * t c * t d) * (pl5 P a b * pl5 P c d) by ring,
    show t a * t c * pl5 P a c * (t b * t d * pl5 P b d)
      = (t a * t b * t c * t d) * (pl5 P a c * pl5 P b d) by ring]
  exact mul_div_mul_left _ _ hk

/-- Charge form: `tᵢ = exp(τ λᵢ)`; the u-variables do not depend on `λ` at all. -/
theorem uCR_charge_blind (P : Matrix (Fin 2) (Fin 5) ℝ) (lam : Fin 5 → ℝ) (τ : ℝ) (a b c d : Fin 5) :
    uCR (torusAct P fun i => Real.exp (τ * lam i)) a b c d = uCR P a b c d :=
  uCR_torus_invariant P _ (fun _ => (Real.exp_pos _).ne') a b c d

/-- Two charge vectors (e.g. SM hypercharge vs any rival) give identical u-variables. -/
theorem uCR_rival_indistinguishable (P : Matrix (Fin 2) (Fin 5) ℝ) (lam lam' : Fin 5 → ℝ) (τ : ℝ)
    (a b c d : Fin 5) :
    uCR (torusAct P fun i => Real.exp (τ * lam i)) a b c d
      = uCR (torusAct P fun i => Real.exp (τ * lam' i)) a b c d := by
  rw [uCR_charge_blind, uCR_charge_blind]

/-- Positive torus elements preserve the sign of every Plücker coordinate (`Gr₊` is torus-stable). -/
theorem pos_torus (P : Matrix (Fin 2) (Fin 5) ℝ) (t : Fin 5 → ℝ) (ht : ∀ i, 0 < t i) (i j : Fin 5) :
    0 < pl5 (torusAct P t) i j ↔ 0 < pl5 P i j := by
  rw [pl5_torus]
  have h : 0 < t i * t j := mul_pos (ht i) (ht j)
  constructor
  · intro hp; exact (pos_iff_pos_of_mul_pos hp).mp h
  · intro hp; positivity

/-- The chart monomial `X13mono` only picks up the common weight `t₀t₁t₂t₃`. -/
theorem X13mono_torus (P : Matrix (Fin 2) (Fin 5) ℝ) (t : Fin 5 → ℝ) :
    X13mono (torusAct P t) = (t 0 * t 1 * t 2 * t 3) * X13mono P := by
  simp only [X13mono, pl5_torus]; ring

/-- M2: cubic moment of an `Sₙ`-symmetric measure, written in power sums, reduces on `p₁ = 0` to `κ
  p₃`. -/
theorem sym_cubic_reduction (E3 E21 E111 p1 p2 p3 : ℝ) (h1 : p1 = 0) :
    E3 * p3 + 3 * E21 * (p1 * p2 - p3) + E111 * (p1 ^ 3 - 3 * p1 * p2 + 2 * p3)
      = (E3 - 3 * E21 + 2 * E111) * p3 := by
  subst h1; ring

/-- Ordered-triple expansion behind `sym_cubic_reduction`, checked on five columns. -/
theorem triple_sum_five (l : Fin 5 → ℝ) (E3 E21 E111 : ℝ) :
    (∑ i, ∑ j, ∑ k, l i * l j * l k *
        (if i = j ∧ j = k then E3 else if i = j ∨ j = k ∨ i = k then E21 else E111))
      = E3 * (∑ i, l i ^ 3) + 3 * E21 * ((∑ i, l i) * (∑ i, l i ^ 2) - ∑ i, l i ^ 3)
        + E111 * ((∑ i, l i) ^ 3 - 3 * (∑ i, l i) * (∑ i, l i ^ 2) + 2 * ∑ i, l i ^ 3) := by
  simp only [Fin.sum_univ_five]
  simp (config := { decide := true })
  ring

/-- Rival cube `[0,1]ⁿ` (independent uniforms, CITED moments 1/4, 1/6, 1/8): `κ = 0`, no cubic
  constraint. -/
theorem cube_kappa_zero : (1 / 4 : ℝ) - 3 * (1 / 6) + 2 * (1 / 8) = 0 := by norm_num

/-- Rival simplex `Δ(1,n)` (Dirichlet(1,…,1), CITED moments 6/D, 2/D, 1/D, `D = n(n+1)(n+2)`): `κ =
  2/D > 0`. -/
theorem simplex_kappa_pos (n : ℕ) (hn : 0 < n) :
    0 < (6 : ℝ) / (n * (n + 1) * (n + 2)) - 3 * (2 / (n * (n + 1) * (n + 2)))
      + 2 * (1 / (n * (n + 1) * (n + 2))) := by
  have hD : (0 : ℝ) < n * (n + 1) * (n + 2) := by
    have : (0 : ℝ) < n := by exact_mod_cast hn
    positivity
  have : (6 : ℝ) / (n * (n + 1) * (n + 2)) - 3 * (2 / (n * (n + 1) * (n + 2)))
      + 2 * (1 / (n * (n + 1) * (n + 2))) = 2 / (n * (n + 1) * (n + 2)) := by ring
  rw [this]; positivity

/-- M2 does not discriminate: `(yQ,yu,yd,yL,ye) = (1,−7,0,8,−1)` (found by the checker) satisfies the two trace
conditions `Tr Y = 0`, `Tr Y³ = 0` (SM multiplicities 6,3,3,2,1) but violates SU(3)²U(1) (`2yQ+yu+yd = −5`), so it is
not an STRUCT-1 ACC solution (conditions restated inline; no import of `PositiveGeometryEmergentSpaceTime.STRUCT1`). -/
theorem trace_conditions_not_acc :
    (6 * (1 : ℚ) + 3 * (-7) + 3 * 0 + 2 * 8 + (-1) = 0) ∧
    (6 * (1 : ℚ) ^ 3 + 3 * (-7) ^ 3 + 3 * 0 ^ 3 + 2 * 8 ^ 3 + (-1) ^ 3 = 0) ∧
    (2 * (1 : ℚ) + (-7) + 0 ≠ 0) := by
  norm_num

/-- Bundle (BRIDGE-PL-ASSOC mission rung): M1 charge-blind; M2 reproduced by the simplex rival and
  non-discriminating. -/
theorem bridge_charge_nolink (P : Matrix (Fin 2) (Fin 5) ℝ) (lam lam' : Fin 5 → ℝ) (τ : ℝ) (a b c d : Fin 5) :
    uCR (torusAct P fun i => Real.exp (τ * lam i)) a b c d
      = uCR (torusAct P fun i => Real.exp (τ * lam' i)) a b c d ∧
    (0 < (6 : ℝ) / (15 * (15 + 1) * (15 + 2)) - 3 * (2 / (15 * (15 + 1) * (15 + 2)))
      + 2 * (1 / (15 * (15 + 1) * (15 + 2)))) ∧
    (2 * (1 : ℚ) + (-7) + 0 ≠ 0) := by
  refine ⟨uCR_rival_indistinguishable P lam lam' τ a b c d, ?_, by norm_num⟩
  have := simplex_kappa_pos 15 (by norm_num)
  push_cast at this
  exact this

end PositiveGeometryEmergentSpaceTime.BridgePLCharge
