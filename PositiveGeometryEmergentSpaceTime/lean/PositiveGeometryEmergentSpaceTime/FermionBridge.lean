/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-! FZ-0 T1: the Zhang–Zhu fermion–fermion bridge (ū₃γ^μu₁ = 0) trivialises any
2-fermion + 2-scalar amplitude ū₃(A + B Q̸)u₁ for equal-mass Dirac fermions.
Spinor bilinears are abstracted: `b1 = ū₃u₁`, `bv μ = ū₃γ^μu₁`.
Dirac equations enter only through the Gordon contraction
`Σ_μ P_μ bv μ = 2M b1` (P = p₁+p₃, from ū₃p̸₃ = Mū₃ and p̸₁u₁ = Mu₁). -/

namespace PositiveGeometryEmergentSpaceTime.FermionBridge

open BigOperators

/-- invariant decomposition of a πN-type amplitude -/
def amp (A B : ℂ) (Q : Fin 4 → ℂ) (b1 : ℂ) (bv : Fin 4 → ℂ) : ℂ :=
  A * b1 + B * ∑ μ, Q μ * bv μ

/-- If every vector bilinear `ū₃γ^μu₁` vanishes, the amplitude `ū₃(A + B Q̸)u₁` reduces to `A ·
  ū₃u₁`. -/
theorem bridge_reduces (A B : ℂ) (Q : Fin 4 → ℂ) (b1 : ℂ) (bv : Fin 4 → ℂ)
    (hbr : ∀ μ, bv μ = 0) : amp A B Q b1 bv = A * b1 := by
  simp [amp, hbr]

/-- With the Gordon contraction `Σ_μ P_μ bv_μ = 2M b1`, `M ≠ 0` and all `bv_μ = 0`, the scalar
  bilinear `b1` also vanishes. -/
theorem bridge_kills_scalar (M b1 : ℂ) (P bv : Fin 4 → ℂ) (hM : M ≠ 0)
    (hG : ∑ μ, P μ * bv μ = 2 * M * b1) (hbr : ∀ μ, bv μ = 0) : b1 = 0 := by
  simp [hbr] at hG
  rcases hG with h | h
  · exact absurd h hM
  · exact h

/-- Main T1 statement: on the bridge the amplitude vanishes for every A, B (any dynamics,
any s,t), so the "zero" carries no dynamical information. -/
theorem bridge_trivial_zero (A B M b1 : ℂ) (P Q bv : Fin 4 → ℂ) (hM : M ≠ 0)
    (hG : ∑ μ, P μ * bv μ = 2 * M * b1) (hbr : ∀ μ, bv μ = 0) :
    amp A B Q b1 bv = 0 := by
  rw [bridge_reduces A B Q b1 bv hbr, bridge_kills_scalar M b1 P bv hM hG hbr, mul_zero]

/-- T3 remark: with only the vector bridge and the scalar bilinear free, a zero needs A = 0;
LO A^{3/2} = g²/M ≠ 0 (MR-7, `PiNGate.D_at_t0`). -/
theorem needs_A_zero (A b1 : ℂ) (hb : b1 ≠ 0) (h : A * b1 = 0) : A = 0 := by
  rcases mul_eq_zero.mp h with h | h
  · exact h
  · exact absurd h hb

end PositiveGeometryEmergentSpaceTime.FermionBridge
