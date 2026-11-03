/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-! FZ-1 algebra: Pauli vertex keeps the Ward identity; locus-universal zero forces κ = 0. -/
namespace PositiveGeometryEmergentSpaceTime.PauliZero
open BigOperators

/-- antisymmetric tensor contracted twice with the same vector vanishes (σ^{μν}k_μk_ν = 0). -/
theorem antisym_contract (S : Fin 4 → Fin 4 → ℂ) (k : Fin 4 → ℂ) (hS : ∀ μ ν, S μ ν = - S ν μ) :
    ∑ μ, ∑ ν, S μ ν * k μ * k ν = 0 := by
  have h : ∑ μ, ∑ ν, S μ ν * k μ * k ν = - ∑ μ, ∑ ν, S μ ν * k μ * k ν := by
    conv_rhs => rw [Finset.sum_comm]
    rw [← Finset.sum_neg_distrib]; congr 1; ext μ; rw [← Finset.sum_neg_distrib]; congr 1; ext ν
    rw [hS ν μ]; ring
  linear_combination h / 2

/-- If A(κ) = a₁κ + a₂κ² vanishes at two locus points whose coefficient vectors are independent,
then κ = 0: the hidden zero holds on the whole locus only at g = 2. -/
theorem universal_zero_forces_kappa (a1 a2 b1 b2 κ : ℂ) (hdet : a1 * b2 - a2 * b1 ≠ 0)
    (ha : a1 * κ + a2 * κ ^ 2 = 0) (hb : b1 * κ + b2 * κ ^ 2 = 0) : κ = 0 := by
  by_contra hk
  have h1 : a1 + a2 * κ = 0 := by
    have : κ * (a1 + a2 * κ) = 0 := by linear_combination ha
    exact (mul_eq_zero.mp this).resolve_left hk
  have h2 : b1 + b2 * κ = 0 := by
    have : κ * (b1 + b2 * κ) = 0 := by linear_combination hb
    exact (mul_eq_zero.mp this).resolve_left hk
  exact hdet (by linear_combination b2 * h1 - a2 * h2)

/-- real forward locus: A = a₂κ², zero iff κ = 0 when a₂ ≠ 0. -/
theorem forward_quadratic (a2 κ : ℂ) (h : a2 ≠ 0) : a2 * κ ^ 2 = 0 ↔ κ = 0 := by
  constructor
  · intro hz; exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp ((mul_eq_zero.mp hz).resolve_left h)
  · intro hk; simp [hk]

end PositiveGeometryEmergentSpaceTime.PauliZero
