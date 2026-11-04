/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
  PositiveGeometryEmergentSpaceTime/ScaleNoGo.lean — rung OP-2.
  No-go: data that sees only orbit/stabiliser structure (OP-1 pattern) is invariant under
  v ↦ c • v (c ≠ 0, action commuting with scalars), so it cannot fix a magnitude, nor a ratio
  of magnitudes of independent sectors. Amplitude side: the LS family written in units m_ρ² is
  invariant under the overall rescaling (s,u,m²) ↦ (λs,λu,λm²), so it never selects m_ρ.
  Prior art: Buckingham 1914 (π theorem); Landau theory (magnitude set by potential coefficients).
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.OrderParameter

namespace PositiveGeometryEmergentSpaceTime.ScaleNoGo

open MulAction

section Linear
variable {G K V : Type*} [Group G] [Field K] [AddCommGroup V] [Module K V]
  [MulAction G V] [SMulCommClass G K V]

/-- (a) Stabiliser is scale-invariant. -/
theorem stabilizer_smul_eq (v : V) {c : K} (hc : c ≠ 0) :
    stabilizer G (c • v) = stabilizer G v := by
  ext g
  simp only [mem_stabilizer_iff]
  constructor
  · intro h
    rw [smul_comm] at h
    have := congrArg (fun x => c⁻¹ • x) h
    simpa [inv_smul_smul₀ hc] using this
  · intro h; rw [smul_comm, h]

/-- (b) Orbit of c•v is the c-image of the orbit of v. -/
theorem orbit_smul (v : V) (c : K) :
    orbit G (c • v) = (fun x => c • x) '' orbit G v := by
  ext x
  constructor
  · rintro ⟨g, rfl⟩; exact ⟨g • v, ⟨g, rfl⟩, by simp [smul_comm]⟩
  · rintro ⟨_, ⟨g, rfl⟩, rfl⟩; exact ⟨g, by simp [smul_comm]⟩

/-- Broken-ness is scale invariant. -/
theorem broken_smul_iff (v : V) {c : K} (hc : c ≠ 0) :
    stabilizer G (c • v) ≠ ⊤ ↔ stabilizer G v ≠ ⊤ := by
  rw [stabilizer_smul_eq v hc]

/-- (c) Any function of the stabiliser data is scale invariant. -/
theorem opData_scale_invariant {α : Type*} (F : Subgroup G → α) (v : V) {c : K} (hc : c ≠ 0) :
    F (stabilizer G (c • v)) = F (stabilizer G v) := by
  rw [stabilizer_smul_eq v hc]

end Linear

section Real
variable {G V : Type*} [Group G] [AddCommGroup V] [Module ℝ V]
  [MulAction G V] [SMulCommClass G ℝ V]

/-- (c') No magnitude: if f is homogeneous of degree 1 (e.g. a norm, a vev, a mass) and f v ≠ 0,
no function of the stabiliser data reproduces f on the whole ray through v. -/
theorem no_magnitude (f : V → ℝ) (hf : ∀ (c : ℝ) (x : V), f (c • x) = |c| * f x)
    (v : V) (hv : f v ≠ 0) :
    ¬ ∃ F : Subgroup G → ℝ, ∀ c : ℝ, c ≠ 0 → F (stabilizer G (c • v)) = f (c • v) := by
  rintro ⟨F, hF⟩
  have h1 := hF 1 one_ne_zero
  have h2 := hF 2 two_ne_zero
  rw [opData_scale_invariant F v (two_ne_zero : (2:ℝ) ≠ 0), hf] at h2
  rw [one_smul] at h1
  rw [h1] at h2
  norm_num at h2
  exact hv (by linarith)

end Real

section Cross
variable {G₁ G₂ V₁ V₂ : Type*} [Group G₁] [Group G₂]
  [AddCommGroup V₁] [Module ℝ V₁] [MulAction G₁ V₁] [SMulCommClass G₁ ℝ V₁]
  [AddCommGroup V₂] [Module ℝ V₂] [MulAction G₂ V₂] [SMulCommClass G₂ ℝ V₂]

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- (d) No cross-sector ratio: independent rescalings of two sectors leave the joint stabiliser
data unchanged but change f₁/f₂, so no function of that data fixes the ratio. -/
@[nolint unusedArguments]
theorem no_cross_ratio (f₁ : V₁ → ℝ) (f₂ : V₂ → ℝ)
    (hf₁ : ∀ (c : ℝ) (x : V₁), f₁ (c • x) = |c| * f₁ x)
    (v₁ : V₁) (v₂ : V₂) (h₁ : f₁ v₁ ≠ 0) (h₂ : f₂ v₂ ≠ 0) :
    ¬ ∃ F : Subgroup G₁ × Subgroup G₂ → ℝ, ∀ c₁ c₂ : ℝ, c₁ ≠ 0 → c₂ ≠ 0 →
      F (stabilizer G₁ (c₁ • v₁), stabilizer G₂ (c₂ • v₂)) = f₁ (c₁ • v₁) / f₂ (c₂ • v₂) := by
  rintro ⟨F, hF⟩
  have a := hF 1 1 one_ne_zero one_ne_zero
  have b := hF 2 1 two_ne_zero one_ne_zero
  rw [stabilizer_smul_eq v₁ (two_ne_zero : (2:ℝ) ≠ 0), hf₁] at b
  simp only [one_smul] at a b
  rw [a] at b
  field_simp at b
  norm_num at b

end Cross

/-! ## (e) Amplitude side: Lovelace–Shapiro with dimensionful arguments -/

/-- Dimensionful LS amplitude: trajectory α(x) = α₀ + x/(2 m²) (α' = 1/(2m_ρ²) chiral case). -/
noncomputable def LS (a0 : ℝ) (s u m2 : ℝ) : ℝ :=
  -(Real.Gamma (1 - (a0 + s / (2*m2))) * Real.Gamma (1 - (a0 + u / (2*m2)))) /
    Real.Gamma (1 - (a0 + s / (2*m2)) - (a0 + u / (2*m2)))

/-- Overall rescaling invariance (dimensional analysis). -/
theorem LS_scale (a0 s u m2 lam : ℝ) (hl : lam ≠ 0) (hm : m2 ≠ 0) :
    LS a0 (lam * s) (lam * u) (lam * m2) = LS a0 s u m2 := by
  have e1 : lam * s / (2 * (lam * m2)) = s / (2 * m2) := by field_simp
  have e2 : lam * u / (2 * (lam * m2)) = u / (2 * m2) := by field_simp
  simp only [LS, e1, e2]

/-- LS depends only on the dimensionless pair (s/m², u/m²). -/
theorem LS_dimensionless (a0 s u m2 : ℝ) (hm : m2 ≠ 0) :
    LS a0 s u m2 = LS a0 (s / m2) (u / m2) 1 := by
  rw [← LS_scale a0 (s/m2) (u/m2) 1 m2 hm one_ne_zero]
  congr 1 <;> field_simp
/-- Hence no property of the amplitude *as a function* selects m²: the family at m² and at λm²
are related by the rescaling of the kinematics. One dimensionful input is always needed. -/
theorem LS_no_scale (a0 m2 lam : ℝ) (hl : lam ≠ 0) (hm : m2 ≠ 0) (P : (ℝ → ℝ → ℝ) → Prop)
    (hP : ∀ A : ℝ → ℝ → ℝ, P A ↔ P (fun s u => A (lam * s) (lam * u))) :
    P (fun s u => LS a0 s u m2) ↔ P (fun s u => LS a0 s u (lam * m2)) := by
  rw [hP (fun s u => LS a0 s u (lam * m2))]
  simp only [LS_scale a0 _ _ m2 lam hl hm]

end PositiveGeometryEmergentSpaceTime.ScaleNoGo
