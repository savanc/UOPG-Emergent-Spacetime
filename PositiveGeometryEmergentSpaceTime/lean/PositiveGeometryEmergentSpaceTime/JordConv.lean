import Mathlib.Algebra.Field.Basic
import Mathlib.Algebra.Module.LinearMap.Defs
import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Algebra.NoZeroSMulDivisors.Basic

/-!
# JORD-1 convention-invariance re-check (2026-10-30, the author)

The physics-preserving equivalence used by `sims/convcheck/jord1_conv.py`: uniform rescaling
`v ↦ c • v` (`c ≠ 0`) of idempotent representatives.
* `der_smul_eq_zero_iff`: a linear map kills `c • v` iff it kills `v`, so stabilisers
  (`stab S = {D | D s = 0 ∀ s ∈ S}`) do not depend on the scale of the representatives.
* `idem_scale_iff`: for a bilinear product `B`, `B (c•x) (c•x) = c • (c•x) ↔ B x x = x` (`c ≠ 0`):
  "P is idempotent at unit scale" and "2P passes the 2P-scale test" are the same statement.
Glossary: `c` = scale factor λ; `B` = Jordan product (any bilinear map); `D` = derivation (any linear map).
PROVED, 0 sorry, no native_decide.
-/

namespace PositiveGeometryEmergentSpaceTime.JordConv

variable {K V W : Type*} [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]

theorem der_smul_eq_zero_iff (D : V →ₗ[K] W) {c : K} (hc : c ≠ 0) (v : V) :
    D (c • v) = 0 ↔ D v = 0 := by
  rw [map_smul, smul_eq_zero]; simp [hc]

theorem stab_smul_eq (D : V →ₗ[K] W) {c : K} (hc : c ≠ 0) (S : Set V) :
    (∀ s ∈ S, D (c • s) = 0) ↔ (∀ s ∈ S, D s = 0) := by
  simp only [der_smul_eq_zero_iff D hc]

theorem idem_scale_iff (B : V →ₗ[K] V →ₗ[K] V) {c : K} (hc : c ≠ 0) (x : V) :
    B (c • x) (c • x) = c • (c • x) ↔ B x x = x := by
  simp only [map_smul, LinearMap.smul_apply]
  constructor
  · intro h
    have h2 : (c * c) • (B x x) = (c * c) • x := by rw [mul_smul, mul_smul]; exact h
    exact smul_right_injective V (mul_ne_zero hc hc) h2
  · intro h; rw [h]

end PositiveGeometryEmergentSpaceTime.JordConv
