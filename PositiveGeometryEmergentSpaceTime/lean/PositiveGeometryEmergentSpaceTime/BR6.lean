/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Spinor
import PositiveGeometryEmergentSpaceTime.LightCone
import PositiveGeometryEmergentSpaceTime.MassiveSpinor
/-!
# BR-6: M1 spinor/kinematics cluster ↔ MassiveSpinor (BH-2) (2026-10-14)
MassiveSpinor restated M1's σ-map locally (`sig`) to avoid import coupling. Here: `sig = sigma`, so the
Minkowski determinant identity of M1 transfers, and the mass shell splits cleanly: massive (η ≠ 0) momenta
have rank 2 (MassiveSpinor), massless ones are characterised in LightCone. Classical; structural join.
-/
namespace PositiveGeometryEmergentSpaceTime.BR6

/-- MassiveSpinor's local σ-map is M1's `sigma`. -/
theorem sig_eq_sigma (v : Fin 4 → ℝ) : PositiveGeometryEmergentSpaceTime.MassiveSpinor.sig v = PositiveGeometryEmergentSpaceTime.sigma v := rfl

/-- det σ(v) = η(v) for MassiveSpinor's map (M1's `det_sigma` transferred). -/
theorem det_sig (v : Fin 4 → ℝ) : (PositiveGeometryEmergentSpaceTime.MassiveSpinor.sig v).det = (PositiveGeometryEmergentSpaceTime.minkowskiQuad v : ℂ) := by
  rw [sig_eq_sigma]; exact PositiveGeometryEmergentSpaceTime.det_sigma v

/-- Massive (η ≠ 0) Minkowski momenta give rank-2 matrices (MassiveSpinor.massive_rank_two via M1's
  det). -/
theorem massive_sigma_rank_two (v : Fin 4 → ℝ) (hv : PositiveGeometryEmergentSpaceTime.minkowskiQuad v ≠ 0) : (PositiveGeometryEmergentSpaceTime.sigma v).rank = 2 := by
  rw [← sig_eq_sigma]
  apply PositiveGeometryEmergentSpaceTime.MassiveSpinor.massive_rank_two
  rw [det_sig]; exact_mod_cast hv

/-- Massive decomposition for an on-shell Minkowski momentum: η(v) = m², m ≠ 0 ⇒ σ(v) = Λ Λ̃ᵀ, det Λ
  = det Λ̃ = m. -/
theorem minkowski_massive_decomp (v : Fin 4 → ℝ) {m : ℂ} (hm : m ≠ 0) (hv : (PositiveGeometryEmergentSpaceTime.minkowskiQuad v : ℂ) = m ^ 2) :
    ∃ L Lt : Matrix (Fin 2) (Fin 2) ℂ, PositiveGeometryEmergentSpaceTime.sigma v = L * Lt.transpose ∧ L.det = m ∧ Lt.det = m := by
  rw [← sig_eq_sigma]
  exact PositiveGeometryEmergentSpaceTime.MassiveSpinor.exists_massive_decomp _ hm (by rw [det_sig]; exact hv)

/-- Massive momenta are never a single spinor pair (the m → 0 form): σ(v) ≠ a bᵀ. -/
theorem massive_not_single_pair (v : Fin 4 → ℝ) (hv : PositiveGeometryEmergentSpaceTime.minkowskiQuad v ≠ 0) (a b : Fin 2 → ℂ) :
    PositiveGeometryEmergentSpaceTime.sigma v ≠ Matrix.vecMulVec a b := by
  intro h
  have hd := PositiveGeometryEmergentSpaceTime.det_sigma v
  rw [h, Matrix.det_fin_two] at hd
  simp [Matrix.vecMulVec_apply] at hd
  apply hv; exact_mod_cast (by rw [← hd]; ring : (PositiveGeometryEmergentSpaceTime.minkowskiQuad v : ℂ) = 0)

/-- Non-vacuity witness: the rest-frame momentum (1,0,0,0) is massive (η = 1). -/
theorem br6_witness : PositiveGeometryEmergentSpaceTime.minkowskiQuad ![1, 0, 0, 0] = 1 := by
  simp [PositiveGeometryEmergentSpaceTime.minkowskiQuad]

end PositiveGeometryEmergentSpaceTime.BR6
