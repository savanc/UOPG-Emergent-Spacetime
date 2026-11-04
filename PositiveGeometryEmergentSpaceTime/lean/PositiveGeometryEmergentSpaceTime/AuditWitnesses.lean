/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.EWZ1b
import PositiveGeometryEmergentSpaceTime.FT2Mesh
import PositiveGeometryEmergentSpaceTime.KEtaGate
import PositiveGeometryEmergentSpaceTime.UnequalLS
import PositiveGeometryEmergentSpaceTime.RelEntropy
import PositiveGeometryEmergentSpaceTime.TP1b
import PositiveGeometryEmergentSpaceTime.MassiveZero
import PositiveGeometryEmergentSpaceTime.SubthresholdGate

/-!
# Lean audit 2026-10-13: non-vacuity witnesses

Each theorem below exhibits a concrete point satisfying the full hypothesis bundle of a theorem cited
as PROVED in a review, so that theorem is not vacuously true. No existing statement is changed.
See `notes/LEAN-AUDIT-2026-10-13.md`.

Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/

namespace PositiveGeometryEmergentSpaceTime.AuditWitnesses

/-- `EWZ1b.forced`: its two hypotheses are jointly satisfiable (SM point a = lam3 = lam4 = 1). -/
theorem ewz1b_forced_hyps_sat :
    EWZ1b.N 1 (-3) (4) (-4) (-1) (-4) (2) (2) (2) (5) (1) (-2) (-4) (2) (-5) 1 1 (1) = 0 ∧
    EWZ1b.N 1 (1) (4) (-5) (2) (-1) (-2) (4) (-4) (0) (-5) (-5) (-5) (5) (3) 1 1 (-5) = 0 :=
  ⟨EWZ1b.zero_of_gauge _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ rfl (by norm_num),
   EWZ1b.zero_of_gauge _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ rfl (by norm_num)⟩

/-- `EWZ1b.forced` is not trivial: off the SM couplings the residual is nonzero at its first point. -/
theorem ewz1b_forced_discriminates :
    EWZ1b.N 2 (-3) (4) (-4) (-1) (-4) (2) (2) (2) (5) (1) (-2) (-4) (2) (-5) 1 1 (1) ≠ 0 := by
  rw [EWZ1b.N_decomp]; simp only [EWZ1b.Q1, EWZ1b.Q2]; norm_num

/-- `FT2Mesh.zero_unphysical` / `DecayZeroNoGo.no_zero`: hypothesis bundle satisfiable
(two particles of unit mass at rest, d = 0). -/
theorem ft2_unphysical_hyps_sat :
    ∃ m1 m2 a1 a2 E1 E2 d : ℝ, 0 < m1 ∧ 0 < m2 ∧ 0 ≤ a1 ∧ 0 ≤ a2 ∧ 0 ≤ E1 ∧ 0 ≤ E2 ∧
      E1^2 = m1^2 + a1^2 ∧ E2^2 = m2^2 + a2^2 ∧ d ≤ a1*a2 :=
  ⟨1, 1, 0, 0, 1, 1, 0, by norm_num⟩

/-- `KEtaGate.dual_ne_chiral`: satisfiable (m_π² = 1, m_η² = 2). -/
theorem keta_hyps_sat : ∃ m_eta2 m_pi2 : ℝ, 0 < m_pi2 ∧ m_pi2 < m_eta2 := ⟨2, 1, by norm_num⟩

/-- `UnequalLS.zero_line`: hypothesis bundle satisfiable (a = 1, m_π² = 1, m_K² = 3, s = 4, t = 2, u
  = 2). -/
theorem unequalLS_zero_line_hyps_sat :
    ∃ a m_pi2 m_K2 s t u : ℝ, a ≠ 0 ∧ s + t + u = 2 * (m_pi2 + m_K2) ∧
      (1/2 + a * (t - m_pi2)) + (1/2 + a * (u - m_K2)) = 1 :=
  ⟨1, 1, 3, 4, 2, 2, by norm_num⟩

/-- `RelEntropy.relEnt_nonneg`: satisfiable (two uniform distributions on `Fin 2`). -/
theorem relEnt_hyps_sat : ∃ p q : Fin 2 → ℝ, (∀ i, 0 < p i) ∧ (∀ i, 0 < q i) ∧
    ∑ i, p i = ∑ i, q i :=
  ⟨fun _ => 1/2, fun _ => 1/2, fun _ => by norm_num, fun _ => by norm_num, rfl⟩

/-- `TP1b.eigen`: its hypothesis `P c = 0` is satisfied at the claimed E8 eigenvalue. -/
theorem tp1b_eigen_hyp_sat : ∃ c : ℝ, TP1b.charPolyE8 c = 0 ∧ 1.988 ≤ c :=
  ⟨_, TP1b.charPolyE8_root, TP1b.c_bounds.1⟩

/-- `MassiveZero.dress_zero_at_P`: satisfiable by the LO ordered amplitude f(x,y) = x + y − 2. -/
theorem massiveZero_hyps_sat : ∃ f : ℝ → ℝ → ℝ, (∀ x y, f x y = f y x) ∧
    (∀ x y, x + y = 2 → f x y = 0) ∧ f 0 0 ≠ 0 :=
  ⟨fun x y => x + y - 2, fun x y => by ring, fun x y h => by linarith, by norm_num⟩

end PositiveGeometryEmergentSpaceTime.AuditWitnesses
