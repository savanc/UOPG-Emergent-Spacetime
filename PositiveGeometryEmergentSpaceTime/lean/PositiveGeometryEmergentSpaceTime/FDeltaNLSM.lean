/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# F-POSGEOM-DAUGHTER — the δ-shifted stringy Tr(Φ³) four-point amplitude (geometry-native stringy NLSM)

Also known as: F-POSGEOM-DAUGHTER, δ-deformation (Arkani-Hamed–Cao–Dong–Figueiredo–He, arXiv:2312.16282 §7,
arXiv:2401.05483). Four-point member: `I₄^δ = Γ(α′(X₁₃ − δ)) Γ(α′(X₂₄ + δ)) / Γ(α′(X₁₃ + X₂₄))` (their eq. 7.10).
* `shift_preserves_c_iff`: a shift `(X₁₃, X₂₄) → (X₁₃ + e₁, X₂₄ + e₂)` preserves `c₁₃ = X₁₃ + X₂₄` iff `e₂ = −e₁`
  (four-point instance of their uniqueness of the c-preserving shift).
* `deltaAmp4_stripped`, `deltaAmp4_tachyon_residue`: the pole at `X₁₃ = δ` has pole-stripped value exactly 1 (for every
  `δ`, whenever `Γ(α′(X₂₄+δ)) ≠ 0`): in their propagator convention `1/(X + m²)` this is a state with `m² = −δ`.
* `nlsm_mass_condition_tachyon`: the full-U(N) non-linear realisation needs `m_φ² + m_φ̃² = 0` (CITED, 2401.05483 §III);
  with `m_φ² ≠ 0` one of the two is negative — a tachyon for every NLSM member (`δ ≠ 0`).
No axioms; amplitudes and the U(N) condition CITED.
-/

namespace PositiveGeometryEmergentSpaceTime.FDeltaNLSM

/-- Four-point δ-shifted stringy Tr(Φ³) amplitude. Also known as: `I₄^δ` (2312.16282 eq. 7.10). -/
noncomputable def deltaAmp4 (ap d X Y : ℝ) : ℝ :=
  Real.Gamma (ap * (X - d)) * Real.Gamma (ap * (Y + d)) * (Real.Gamma (ap * (X + Y)))⁻¹

/-- A shift `(X, Y) ↦ (X + e₁, Y + e₂)` preserves `X + Y` iff `e₂ = −e₁`. -/
theorem shift_preserves_c_iff (X Y e1 e2 : ℝ) : (X + e1) + (Y + e2) = X + Y ↔ e2 = -e1 := by
  constructor <;> intro h <;> linarith

/-- The δ-shift preserves `c₁₃ = X₁₃ + X₂₄`. -/
theorem delta_shift_preserves_c (X Y d : ℝ) : (X - d) + (Y + d) = X + Y := by ring

/-- Pole-stripped amplitude: `α′(X − δ)·I₄^δ = Γ(α′(X−δ)+1)Γ(α′(Y+δ))/Γ(α′(X+Y))` for `α′(X − δ) ≠
  0`. -/
theorem deltaAmp4_stripped {ap d X Y : ℝ} (h : ap * (X - d) ≠ 0) :
    ap * (X - d) * deltaAmp4 ap d X Y
      = Real.Gamma (ap * (X - d) + 1) * Real.Gamma (ap * (Y + d)) * (Real.Gamma (ap * (X + Y)))⁻¹ := by
  unfold deltaAmp4; rw [Real.Gamma_add_one h]; ring

/-- At the pole `X = δ` the pole-stripped value is exactly 1: a state of mass² `−δ` with unit
  residue, for every `δ`. -/
theorem deltaAmp4_tachyon_residue {ap d Y : ℝ} (hG : Real.Gamma (ap * (Y + d)) ≠ 0) :
    Real.Gamma (ap * (d - d) + 1) * Real.Gamma (ap * (Y + d)) * (Real.Gamma (ap * (d + Y)))⁻¹ = 1 := by
  rw [show ap * (d - d) + 1 = 1 by ring, Real.Gamma_one, one_mul, show d + Y = Y + d by ring]
  exact mul_inv_cancel₀ hG

/-- NLSM condition `m_φ² + m_φ̃² = 0` with `m_φ² ≠ 0` forces one negative mass² (a tachyon). -/
theorem nlsm_mass_condition_tachyon {m1 m2 : ℝ} (h : m1 + m2 = 0) (hne : m1 ≠ 0) : m1 < 0 ∨ m2 < 0 := by
  rcases lt_or_gt_of_ne hne with h1 | h1
  · exact Or.inl h1
  · exact Or.inr (by linarith)

/-- In the δ-family the two shifted channels carry mass² `−δ` and `+δ`: for `δ ≠ 0` one is
  tachyonic. -/
theorem delta_family_tachyon {d : ℝ} (hd : d ≠ 0) : -d < 0 ∨ d < 0 :=
  nlsm_mass_condition_tachyon (by ring) (neg_ne_zero.mpr hd)

/-- Bundle (F-POSGEOM-DAUGHTER): unique c-preserving 4-pt shift; unit-residue pole at `X₁₃ = δ`;
  tachyon for `δ ≠ 0`. -/
theorem fdelta_obstruction {ap d Y : ℝ} (hd : d ≠ 0) (hG : Real.Gamma (ap * (Y + d)) ≠ 0) :
    (∀ X Y e1 e2 : ℝ, (X + e1) + (Y + e2) = X + Y ↔ e2 = -e1) ∧
    Real.Gamma (ap * (d - d) + 1) * Real.Gamma (ap * (Y + d)) * (Real.Gamma (ap * (d + Y)))⁻¹ = 1 ∧
    (-d < 0 ∨ d < 0) :=
  ⟨shift_preserves_c_iff, deltaAmp4_tachyon_residue hG, delta_family_tachyon hd⟩

end PositiveGeometryEmergentSpaceTime.FDeltaNLSM
