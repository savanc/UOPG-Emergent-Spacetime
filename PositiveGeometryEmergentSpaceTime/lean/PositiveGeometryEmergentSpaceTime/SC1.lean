/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.MassiveLS
/-!
# SC-1: Regge slope → string tension (2026-10-15)
MassiveLS (MR-3) gives the chiral-limit slope `ap 0 = 1/2` in units m_ρ² = 1. With the Nambu–Goto
relation σ = 1/(2π α′) (CITED, encoded as a definition) this fixes m_ρ²/σ = π and m_ρ/√σ = √π.
Comparison with large-N lattice data (1304.4437, 2011.13061) is in reviews/SC-1-result-2026-10-15.md (PARTIAL).
-/
namespace PositiveGeometryEmergentSpaceTime.SC1
open PositiveGeometryEmergentSpaceTime.MassiveLS

/-- Nambu–Goto string tension from a Regge slope (CITED relation, as a definition).
Also known as: σ, σ_NG, string tension; argument `ap` is the Regge slope α′ (also known as: ap', alpha_prime). -/
noncomputable def sigmaNG (ap : ℝ) : ℝ := 1 / (2 * Real.pi * ap)

/-- Chiral-limit LS slope is 1/2 (units m_ρ² = 1). -/
theorem ap_chiral : ap 0 = 1 / 2 := by norm_num [ap]

/-- m_ρ²/σ = π for the chiral-limit LS slope. -/
theorem mrho_sq_over_sigma : 1 / sigmaNG (ap 0) = Real.pi := by
  rw [ap_chiral, sigmaNG]; field_simp

/-- m_ρ/√σ = √π. -/
theorem mrho_over_sqrt_sigma : 1 / Real.sqrt (sigmaNG (ap 0)) = Real.sqrt Real.pi := by
  rw [one_div, ← Real.sqrt_inv, ← one_div, mrho_sq_over_sigma]

/-- Same π as the KSRF gap of MassiveLS: m_ρ²/σ equals `(1/2)/(1/(2π))`. -/
theorem sigma_matches_ksrf_gap : 1 / sigmaNG (ap 0) = (1 / 2 : ℝ) / (1 / (2 * Real.pi)) := by
  rw [mrho_sq_over_sigma, ksrf_gap]

/-- Non-vacuity witness: the slope convention matters — α′ = 1 (rival R1) gives m_ρ²/σ = 2π ≠ π. -/
theorem witness_rival_slope : 1 / sigmaNG 1 = 2 * Real.pi ∧ 1 / sigmaNG 1 ≠ Real.pi := by
  have hp := Real.pi_pos
  refine ⟨by rw [sigmaNG]; field_simp, ?_⟩
  rw [sigmaNG]; field_simp; intro h; linarith

end PositiveGeometryEmergentSpaceTime.SC1
