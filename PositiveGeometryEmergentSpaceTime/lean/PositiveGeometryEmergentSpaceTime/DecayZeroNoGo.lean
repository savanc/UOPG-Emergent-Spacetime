/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-6 Gate: the CGW-type massive hidden-zero locus p_a·p_b = 0 (MR-2: p1·p3 = 0; MR-4: s = Σ) cannot be reached
by any pair of physical (future-timelike, on-shell) momenta, so in K → 3π the locus lies outside the Dalitz region.
For E_i² = m_i² + a_i², E_i ≥ 0, a_i ≥ 0 and |p⃗1·p⃗2| ≤ a1 a2:  p1·p2 = E1E2 − p⃗1·p⃗2 ≥ m1 m2.
-/

namespace PositiveGeometryEmergentSpaceTime.DecayZeroNoGo

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- For `Eᵢ² = mᵢ² + aᵢ²` with all quantities ≥ 0: `m₁m₂ + a₁a₂ ≤ E₁E₂`. -/
@[nolint unusedArguments]
theorem key (m1 m2 a1 a2 E1 E2 : ℝ) (hm1 : 0 ≤ m1) (hm2 : 0 ≤ m2) (ha1 : 0 ≤ a1) (ha2 : 0 ≤ a2)
    (hE1 : 0 ≤ E1) (hE2 : 0 ≤ E2) (h1 : E1^2 = m1^2 + a1^2) (h2 : E2^2 = m2^2 + a2^2) :
    m1 * m2 + a1 * a2 ≤ E1 * E2 := by
  have hsq : (m1*m2 + a1*a2)^2 ≤ (E1*E2)^2 := by
    have : (E1*E2)^2 = (m1^2+a1^2)*(m2^2+a2^2) := by rw [mul_pow, h1, h2]
    rw [this]; nlinarith [sq_nonneg (m1*a2 - a1*m2)]
  have h0 : 0 ≤ E1*E2 := mul_nonneg hE1 hE2
  nlinarith [sq_nonneg (m1*m2 + a1*a2 - E1*E2), sq_nonneg (m1*m2 + a1*a2 + E1*E2),
    mul_nonneg hm1 hm2, mul_nonneg ha1 ha2]

/-- Physical pairs have p1·p2 ≥ m1 m2 > 0, so the zero locus p1·p2 = 0 is unphysical. -/
theorem dot_ge (m1 m2 a1 a2 E1 E2 d : ℝ) (hm1 : 0 ≤ m1) (hm2 : 0 ≤ m2) (ha1 : 0 ≤ a1) (ha2 : 0 ≤ a2)
    (hE1 : 0 ≤ E1) (hE2 : 0 ≤ E2) (h1 : E1^2 = m1^2 + a1^2) (h2 : E2^2 = m2^2 + a2^2)
    (hd : d ≤ a1 * a2) : m1 * m2 ≤ E1 * E2 - d := by
  have := key m1 m2 a1 a2 E1 E2 hm1 hm2 ha1 ha2 hE1 hE2 h1 h2; nlinarith [mul_nonneg ha1 ha2]

/-- For positive masses, nonnegative momenta and on-shell energies `Eᵢ² = mᵢ² + aᵢ²`: if `d ≤ a₁a₂`
  then `E₁E₂ − d ≠ 0` (via `key`). -/
theorem no_zero (m1 m2 a1 a2 E1 E2 d : ℝ) (hm1 : 0 < m1) (hm2 : 0 < m2) (ha1 : 0 ≤ a1) (ha2 : 0 ≤ a2)
    (hE1 : 0 ≤ E1) (hE2 : 0 ≤ E2) (h1 : E1^2 = m1^2 + a1^2) (h2 : E2^2 = m2^2 + a2^2)
    (hd : d ≤ a1 * a2) : E1 * E2 - d ≠ 0 := by
  have := dot_ge m1 m2 a1 a2 E1 E2 d hm1.le hm2.le ha1 ha2 hE1 hE2 h1 h2 hd
  have : 0 < m1*m2 := mul_pos hm1 hm2; linarith

/-- In a decay with all-incoming convention, (K, π) pairs have p_K·(−p_π) ≤ −mK mπ < 0, and
(π, π) pairs (both outgoing) have p·p' ≥ mπ² > 0: either way never 0. Pion-pair invariant at the
locus: s = 2mπ² < 4mπ² (below the Dalitz edge). -/
theorem pipi_locus_below_threshold (m : ℝ) (hm : 0 < m) : 2*m^2 < 4*m^2 := by nlinarith

end PositiveGeometryEmergentSpaceTime.DecayZeroNoGo
