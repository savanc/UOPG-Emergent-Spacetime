/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# EW-Z1b — hidden zeros of massive W amplitudes force the gauge/Higgs couplings (CGW 2601.16860 setup)

`N` = numerator × both propagators of the colour-ordered 4-vector amplitude A[1234] in the U(N)→U(1)^N
adjoint-Higgs (Coulomb-branch) theory of Carrillo González–Ward (arXiv 2601.16860, §VI.2), with *adjustable*
couplings `lam3` (VVV), `a` (VVS: Higgs/Goldstone–W–W per unit mass), `lam4` (VVVV)
Also known as: `lam3` = g (VVV); `lam4` = g² VVVV contact (NOT the Higgs quartic λ_H); `a` = VVS coupling per unit mass., already restricted to the
hidden-zero locus c̃₁₃ = 0, ε₁·ε₃ = ε₁·p₃ = ε₃·p₁ = 0, with `t` eliminated. `k1 k2 k3` are vev differences
(masses; k4 = −k1−k2−k3), `s` the s-channel invariant, `eeij = εᵢ·εⱼ`, `eipj = εᵢ·pⱼ`. The expression is
generated verbatim from the Feynman rules by `sims/ewz1b/mklean.py` (cross-checked there against the full
amplitude). Claim tag of this file: PROVED (0 sorry).
-/

namespace PositiveGeometryEmergentSpaceTime.EWZ1b

/-- Hidden-zero residual: numerator × both propagators of the colour-ordered massive 4-vector
amplitude A[1234] restricted to the CGW zero locus (script-generated, `sims/ewz1b/mklean.py`). -/
def N (a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s : ℚ) : ℚ :=
  (s - (k1 + k2)^2)*(-ee12*ee34*lam4 - ee14*ee23*lam4)*(-2*k1*k3 + k2^2 - s - (k2 + k3)^2 + (k1 + k2 + k3)^2) + (s - (k1 + k2)^2)*(-a^2*ee14*ee23*(k2 - k3)*(-2*k1 - k2 - k3) + 4*e1p2*e2p3*ee34*lam3^2 - 4*e1p2*e3p2*ee24*lam3^2 + 4*e1p2*e4p1*ee23*lam3^2 + 4*e1p2*e4p2*ee23*lam3^2 + 4*e2p1*e3p2*ee14*lam3^2 - 4*e3p2*e4p1*ee12*lam3^2 + 2*ee14*ee23*k1^2*lam3^2 + 2*ee14*ee23*k1*k2*lam3^2 + 2*ee14*ee23*k1*k3*lam3^2 + 2*ee14*ee23*k2^2*lam3^2 + 2*ee14*ee23*k2*k3*lam3^2 + 2*ee14*ee23*k3^2*lam3^2 - 2*ee14*ee23*lam3^2*s - ee14*ee23*lam3^2*(-2*k1*k3 + k2^2 - s + (k1 + k2 + k3)^2)) + (-2*k1*k3 + k2^2 - s - (k2 + k3)^2 + (k1 + k2 + k3)^2)*(-a^2*ee12*ee34*(k1 - k2)*(k1 + k2 + 2*k3) + 4*e1p2*e2p3*ee34*lam3^2 - 4*e1p2*e3p2*ee24*lam3^2 + 4*e1p2*e4p1*ee23*lam3^2 + 4*e1p2*e4p2*ee23*lam3^2 + 4*e2p1*e3p2*ee14*lam3^2 - 4*e3p2*e4p1*ee12*lam3^2 + 2*ee12*ee34*k1^2*lam3^2 + 2*ee12*ee34*k1*k2*lam3^2 + 2*ee12*ee34*k1*k3*lam3^2 + 2*ee12*ee34*k2^2*lam3^2 + 2*ee12*ee34*k2*k3*lam3^2 + 2*ee12*ee34*k3^2*lam3^2 - ee12*ee34*lam3^2*s - 2*ee12*ee34*lam3^2*(-2*k1*k3 + k2^2 - s + (k1 + k2 + k3)^2))

set_option linter.unusedVariables false in
/-- Coefficient of the VVS defect `a² − lam3²` in `N` (script-generated). -/
@[nolint unusedArguments]
def Q1 (a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s : ℚ) : ℚ := -ee12*ee34*k1^4 - 2*ee12*ee34*k1^3*k2 - 2*ee12*ee34*k1^3*k3 - 2*ee12*ee34*k1^2*k2*k3 + ee12*ee34*k1^2*s + 2*ee12*ee34*k1*k2^3 + 2*ee12*ee34*k1*k2^2*k3 + 2*ee12*ee34*k1*k3*s + ee12*ee34*k2^4 + 2*ee12*ee34*k2^3*k3 - ee12*ee34*k2^2*s - 2*ee12*ee34*k2*k3*s - 2*ee14*ee23*k1^3*k2 + 2*ee14*ee23*k1^3*k3 - 5*ee14*ee23*k1^2*k2^2 + 4*ee14*ee23*k1^2*k2*k3 + ee14*ee23*k1^2*k3^2 - 4*ee14*ee23*k1*k2^3 + 2*ee14*ee23*k1*k2^2*k3 + 2*ee14*ee23*k1*k2*k3^2 + 2*ee14*ee23*k1*k2*s - 2*ee14*ee23*k1*k3*s - ee14*ee23*k2^4 + ee14*ee23*k2^2*k3^2 + ee14*ee23*k2^2*s - ee14*ee23*k3^2*s
set_option linter.unusedVariables false in
/-- Coefficient of the quartic defect `lam4 − lam3²` in `N` (script-generated). -/
@[nolint unusedArguments]
def Q2 (a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s : ℚ) : ℚ := ee12*ee34*k1^4 + 4*ee12*ee34*k1^3*k2 + 6*ee12*ee34*k1^2*k2^2 - 2*ee12*ee34*k1^2*s + 4*ee12*ee34*k1*k2^3 - 4*ee12*ee34*k1*k2*s + ee12*ee34*k2^4 - 2*ee12*ee34*k2^2*s + ee12*ee34*s^2 + ee14*ee23*k1^4 + 4*ee14*ee23*k1^3*k2 + 6*ee14*ee23*k1^2*k2^2 - 2*ee14*ee23*k1^2*s + 4*ee14*ee23*k1*k2^3 - 4*ee14*ee23*k1*k2*s + ee14*ee23*k2^4 - 2*ee14*ee23*k2^2*s + ee14*ee23*s^2

/-- The hidden-zero residual is a combination of the two coupling defects only. -/
theorem N_decomp (a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s : ℚ) :
    N a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s = Q1 a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s * (a^2 - lam3^2) + Q2 a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s * (lam4 - lam3^2) := by
  unfold N Q1 Q2; ring

/-- CGW: in the spontaneously broken theory (a = ±lam3, lam4 = lam3², e.g. all = 1) the hidden zero holds
for all masses, polarisations and `s`. -/
theorem zero_of_gauge (a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s : ℚ) (ha : a^2 = lam3^2) (h4 : lam4 = lam3^2) :
    N a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s = 0 := by
  rw [N_decomp, ha, h4]; ring

/-- Forcing: if the zero holds at two explicit kinematic points (hence a fortiori if it holds on the
whole locus), then a² = lam3² and lam4 = lam3². -/
theorem forced (a lam3 lam4 : ℚ)
    (h1 : N a (-3) (4) (-4) (-1) (-4) (2) (2) (2) (5) (1) (-2) (-4) (2) (-5) lam3 lam4 (1) = 0)
    (h2 : N a (1) (4) (-5) (2) (-1) (-2) (4) (-4) (0) (-5) (-5) (-5) (5) (3) lam3 lam4 (-5) = 0) :
    a^2 = lam3^2 ∧ lam4 = lam3^2 := by
  rw [N_decomp] at h1 h2
  simp only [Q1, Q2] at h1 h2
  norm_num at h1 h2
  have hx : a^2 - lam3^2 = 0 := by linarith
  have hy : lam4 - lam3^2 = 0 := by linarith
  exact ⟨by linarith, by linarith⟩

/-- Audit note (2026-10-13): all couplings here are rational (`ℚ`); the real-coupling version is
not stated (see notes/LEAN-AUDIT-2026-10-13.md, item A-5). -/
theorem forced_iff (a lam3 lam4 : ℚ) :
    (a^2 = lam3^2 ∧ lam4 = lam3^2) ↔ ((a = lam3 ∨ a = -lam3) ∧ lam4 = lam3^2) := by
  rw [sq_eq_sq_iff_eq_or_eq_neg]

/-- Control (CGW eq. 53–54): naive Proca YM on the zero leaves m²(P/X + Q/Y) with X + Y = 0,
i.e. a scalar-exchange-shaped residue m²(P − Q)/X, nonzero unless m = 0 or P = Q. -/
theorem proca_control (m P Q X Y : ℚ) (hX : X ≠ 0) (hXY : X + Y = 0) :
    m^2 * (P / X + Q / Y) = m^2 * (P - Q) / X := by
  have : Y = -X := by linarith
  subst this; field_simp; ring

/-- The Proca control residue `m²(P − Q)/X` is nonzero when `X ≠ 0`, `m ≠ 0` and `P ≠ Q`. -/
theorem proca_nonzero (m P Q X : ℚ) (hX : X ≠ 0) (hm : m ≠ 0) (hPQ : P ≠ Q) :
    m^2 * (P - Q) / X ≠ 0 := by
  exact div_ne_zero (mul_ne_zero (pow_ne_zero 2 hm) (sub_ne_zero.mpr hPQ)) hX

end PositiveGeometryEmergentSpaceTime.EWZ1b
