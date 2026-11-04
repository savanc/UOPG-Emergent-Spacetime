/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — EW-Z1b sanity theorems for the script-generated residual `EWZ1b.N` (D170).
Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.EWZ1b

/-!
# EW-Z1b sanity

* Known values: at the gauge point (a = lam3 = 1, lam4 = 1) the residual vanishes at both forcing points;
  `N` is even in the VVS coupling `a` (the Higgs-coupling sign is unobservable).
* Planted: a = 2·lam3 (VVS off by 2) and lam4 = 2·lam3² (contact off by 2) give nonzero residuals.
* Non-vacuity: the hypotheses of `EWZ1b.forced` are satisfiable (gauge point), and both signs a = ±lam3 pass.
* Tie to the Feynman rules: `N` is script data; the regeneration check is recorded in
  notes/alignment/SANITY-2026-11-03.md (script-level, not a Lean proof).
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.EWZ1bSanity
open PositiveGeometryEmergentSpaceTime.EWZ1b

/-- Residual at forcing point 1 as a function of the couplings. -/
def N1 (a lam3 lam4 : ℚ) : ℚ := N a (-3) (4) (-4) (-1) (-4) (2) (2) (2) (5) (1) (-2) (-4) (2) (-5) lam3 lam4 (1)
/-- Residual at forcing point 2. -/
def N2 (a lam3 lam4 : ℚ) : ℚ := N a (1) (4) (-5) (2) (-1) (-2) (4) (-4) (0) (-5) (-5) (-5) (5) (3) lam3 lam4 (-5)

/-- Known value / non-vacuity: the gauge point satisfies both hypotheses of `forced`. -/
theorem gauge_point : N1 1 1 1 = 0 ∧ N2 1 1 1 = 0 := by
  unfold N1 N2 N; norm_num

/-- Non-vacuity: the opposite VVS sign also passes (a = −lam3). -/
theorem gauge_point_neg : N1 (-1) 1 1 = 0 ∧ N2 (-1) 1 1 = 0 := by
  unfold N1 N2 N; norm_num

/-- Known value: `N` is even in `a`. -/
theorem N_even_a (a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s : ℚ) :
    N a e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s
      = N (-a) e1p2 e2p1 e2p3 e3p2 e4p1 e4p2 ee12 ee14 ee23 ee24 ee34 k1 k2 k3 lam3 lam4 s := by
  unfold N; ring

/-- Planted: VVS coupling off by a factor 2 (a = 2·lam3) breaks the zero at point 1 or 2. -/
theorem planted_a2 : N1 2 1 1 ≠ 0 ∨ N2 2 1 1 ≠ 0 := by
  unfold N1 N2 N; norm_num

/-- Planted: quartic contact off by a factor 2 (lam4 = 2·lam3²) breaks the zero at point 1 or 2. -/
theorem planted_lam4 : N1 1 1 2 ≠ 0 ∨ N2 1 1 2 ≠ 0 := by
  unfold N1 N2 N; norm_num

/-- Non-vacuity of the forcing conclusion: `forced` applied at the gauge point returns the gauge relations. -/
theorem forced_nonvacuous : (1:ℚ) ^ 2 = 1 ^ 2 ∧ (1:ℚ) = 1 ^ 2 :=
  forced 1 1 1 gauge_point.1 gauge_point.2

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.EWZ1bSanity
