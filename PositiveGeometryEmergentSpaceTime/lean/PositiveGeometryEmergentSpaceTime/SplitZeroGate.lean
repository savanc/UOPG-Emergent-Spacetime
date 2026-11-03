/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
FT-1 gate. Rodina 2610.01775 exact splitting: A = Σ R_α J J J. At n = 4 there is one cell,
so the only linear zero is the ordinary one, X13 + X24 = 0 (new families start at n = 6,
continuous families at n = 5). With unequal-mass shifts X13 = s - μ1, X24 = u - μ2 the
zero is the single line t = Sm² - μ1 - μ2; matching the LO chiral Kη zero fixes μ1 + μ2,
which the mechanism does not determine (a fitted input). πη LO is constant: no line.

Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/

namespace PositiveGeometryEmergentSpaceTime.SplitZeroGate

/-- Four-point: the cubic amplitude 1/X13 + 1/X24 vanishes iff X13 + X24 = 0 (unique zero). -/
theorem four_point_unique (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
    1 / a + 1 / b = 0 ↔ a + b = 0 := by
  rw [div_add_div _ _ ha hb, div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · linarith
    · exact absurd h (mul_ne_zero ha hb)
  · intro h; left; linarith

/-- Unequal-mass shifted four-point zero is a single t-line set by μ1 + μ2. -/
theorem shifted_zero_line (s t u Sm μ1 μ2 : ℝ) (hstu : s + t + u = Sm)
    (hz : (s - μ1) + (u - μ2) = 0) : t = Sm - μ1 - μ2 := by linarith

/-- Matching the LO chiral zero t0 forces μ1 + μ2 = Sm - t0: one free parameter fixed by the target. -/
theorem chiral_match_iff (Sm μ1 μ2 t0 : ℝ) :
    Sm - μ1 - μ2 = t0 ↔ μ1 + μ2 = Sm - t0 := by constructor <;> intro h <;> linarith

/-- With the geometry-fixed K* shift μ1 = μ2 = m_K² (Kη: Sm = 2mK² + 2mη²) the line is t = 2mη²,
    the KEtaGate line, which misses the chiral zero (PositiveGeometryEmergentSpaceTime.KEtaGate.dual_ne_chiral). -/
theorem kstar_shift_line (s t u m_K2 m_eta2 : ℝ) (hstu : s + t + u = 2 * m_K2 + 2 * m_eta2)
    (hz : (s - m_K2) + (u - m_K2) = 0) : t = 2 * m_eta2 := by linarith

/-- πη LO amplitude is a nonzero constant: no zero line at all. -/
theorem pieta_no_zero (c : ℝ) (hc : c ≠ 0) : ¬ ∃ s t : ℝ, (fun _ _ => c) s t = (0:ℝ) := by
  rintro ⟨_, _, h⟩; exact hc h

end PositiveGeometryEmergentSpaceTime.SplitZeroGate
