/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.PiKZero
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Mr4Blind

/-!
# ALIGNMENT BLIND-3 (2026-11-03) — Compare + sanity: MR-4 (πK hidden-zero line algebra)

Blind prereg: e6e1666 (pushed before `PositiveGeometryEmergentSpaceTime.PiKZero` was opened).

VERDICTS (per original declaration):
* `line_su`, `line_su_piK` vs blind `line_s_sub_u`: **EQUIV** (both directions below).
* `line_poly` vs blind `line_restriction`: **EQUIV** (definitions tie after an argument permutation).
* `lo_zero_on_line(_piK)`: **BLIND-STRONGER**. The original is the arithmetic fact `(S − S)/(2F²) = 0`;
  it never states that the LO amplitude `F⁺ − F⁻` *equals* `(Σ − s)/(2F²)`. The blind `lo_closed`
  does, and it implies the original (`orig_lo_of_blind`).
* `line_is_orthogonal` vs blind `line_iff_dot_zero`: **BLIND-STRONGER** (vector/bilinear form, any
  masses; original is the scalar shadow `m1²+m2²+2d = m1²+m2² ↔ d = 0`, implied below). The
  original docstring says "equal-mass limit", but its statement holds for any masses.
* ν = t/(4 m_K) and κ = mπ/(4 m_K): **MISSING-LEAN** in the original (docstring only); the blind
  `line_nu` and `kappa_line` now cover them.
* `bdm_g0/g1/g2`: not blinded (BDM formulas CITED); sanity below checks they are not vacuous.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR4
open PositiveGeometryEmergentSpaceTime.HadronKinematics

/-! ## Compare -/

theorem orig_line_su_of_blind (m_pi2 m_K2 s t u : ℝ)
    (hst : s + t + u = stuSumPiK m_pi2 m_K2) (hs : s = sigmaPiK m_pi2 m_K2) : s - u = t :=
  Mr4Blind.line_s_sub_u m_pi2 m_K2 s t u (by simpa [stuSumPiK, sigmaPiK] using hst)
    (by simpa [sigmaPiK] using hs)

theorem blind_line_of_orig (Mpi2 MK2 s t u : ℝ) (hon : s + t + u = 2 * (Mpi2 + MK2))
    (hline : s = Mpi2 + MK2) : s - u = t :=
  PiKZero.line_su_piK Mpi2 MK2 s t u (by simpa [stuSumPiK, sigmaPiK] using hon)
    (by simpa [sigmaPiK] using hline)

theorem Fp_tie (C00 C10 C20 C01 C11 C30 τ x : ℝ) :
    PiKZero.Fp C00 C10 C20 C01 C11 C30 τ x = Mr4Blind.Fplus C00 C10 C20 C30 C01 C11 τ x := by
  unfold PiKZero.Fp Mr4Blind.Fplus; ring

theorem Fm_tie (D00 D10 D20 D01 τ x : ℝ) :
    PiKZero.Fm D00 D10 D20 D01 τ x = Mr4Blind.Fminus D00 D10 D20 D01 τ x := rfl

theorem orig_line_poly_of_blind (C00 C10 C20 C01 C11 C30 D00 D10 D20 D01 κ τ : ℝ) :
    PiKZero.Fp C00 C10 C20 C01 C11 C30 τ (κ*τ) - PiKZero.Fm D00 D10 D20 D01 τ (κ*τ)
      = C00 + (C10 - κ*D00)*τ + (C20 + κ^2*C01 - κ*D10)*τ^2
        + (C30 + κ^2*C11 - κ*D20 - κ^3*D01)*τ^3 := by
  rw [Fp_tie, Fm_tie]; exact Mr4Blind.line_restriction _ _ _ _ _ _ _ _ _ _ _ _

theorem blind_line_restriction_of_orig (Cp00 Cp10 Cp20 Cp30 Cp01 Cp11 Cm00 Cm10 Cm20 Cm01 κ τ : ℝ) :
    Mr4Blind.Fplus Cp00 Cp10 Cp20 Cp30 Cp01 Cp11 τ (κ * τ) - Mr4Blind.Fminus Cm00 Cm10 Cm20 Cm01 τ (κ * τ)
      = Cp00 + (Cp10 - κ * Cm00) * τ + (Cp20 + κ ^ 2 * Cp01 - κ * Cm10) * τ ^ 2
        + (Cp30 + κ ^ 2 * Cp11 - κ * Cm20 - κ ^ 3 * Cm01) * τ ^ 3 := by
  rw [← Fp_tie, ← Fm_tie]; exact PiKZero.line_poly _ _ _ _ _ _ _ _ _ _ _ _

/-- The blind closed form implies the original arithmetic statement: on the line the LO amplitude
is literally the original's `(Σ − Σ)/(2F²)`. -/
theorem orig_lo_of_blind (m_pi2 m_K2 mK F s t u : ℝ) (hmK : mK ≠ 0) (hF : F ≠ 0)
    (hon : s + t + u = 2 * (m_pi2 + m_K2)) (hs : s = sigmaPiK m_pi2 m_K2) :
    t / (4 * F ^ 2) - ((s - u) / (4 * mK)) * mK / F ^ 2
      = (sigmaPiK m_pi2 m_K2 - sigmaPiK m_pi2 m_K2) / (2 * F ^ 2) := by
  rw [Mr4Blind.lo_closed m_pi2 m_K2 mK F s t u hmK hF hon, hs]; simp [sigmaPiK]

/-- The blind bilinear statement follows from the original scalar lemma (take m1 = m2 = 0, d = B p q),
so the two carry the same algebra; the blind adds the bilinear-form setting. -/
theorem blind_dot_of_orig {V : Type*} [AddCommGroup V] [Module ℝ V]
    (B : LinearMap.BilinForm ℝ V) (hB : B.IsSymm) (p q : V) :
    B (p + q) (p + q) = B p p + B q q ↔ B p q = 0 := by
  have h : B (p + q) (p + q) = B p p + B q q + 2 * B p q := by
    simp only [map_add, LinearMap.add_apply]
    rw [show B q p = B p q from hB.eq q p]; ring
  have ho := PiKZero.line_is_orthogonal 0 0 (B p q)
  rw [h]; constructor
  · intro h2; exact ho.mp (by linarith)
  · intro h0; rw [h0]; ring

/-- Conversely the original scalar lemma follows from the blind one (V = ℝ): it is pure
linear arithmetic; derived here from the blind on `B := LinearMap.mul ℝ ℝ`, p = 1, q = d. -/
theorem orig_orth_of_blind (m1 m2 d : ℝ) : m1^2 + m2^2 + 2*d = m1^2 + m2^2 ↔ d = 0 := by
  have hB : LinearMap.BilinForm.IsSymm (LinearMap.mul ℝ ℝ) := ⟨fun x y => by simp [mul_comm]⟩
  have hb := Mr4Blind.line_iff_dot_zero (LinearMap.mul ℝ ℝ) hB 1 d
  simp only [LinearMap.mul_apply'] at hb
  constructor
  · intro h; simpa using hb.mp (by linear_combination h)
  · intro h; have := hb.mpr (by simpa using h); linear_combination this

/-! ## Sanity -/

/-- Known value: κ = mπ/(4 m_K) with the PDG-like inputs used in the MR-4 record is ≈ 0.0704. -/
theorem kappa_value : (0.0703 : ℝ) < 0.13957 / (4 * 0.4957) ∧ 0.13957 / (4 * 0.4957) < (0.0705 : ℝ) := by
  constructor <;> norm_num

/-- Non-vacuity: an on-shell point on the line with t ≠ 0 exists, and the LO amplitude vanishes there. -/
theorem line_point_exists : ∃ s t u : ℝ, s + t + u = 2 * (1 + 2) ∧ s = 1 + 2 ∧ t ≠ 0 ∧
    t / (4 * 1 ^ 2) - ((s - u) / (4 * 1)) * 1 / 1 ^ 2 = 0 :=
  ⟨3, 1, 2, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- Planted wrong case: off the line `s − u = t` fails (s = Σ + 1). -/
theorem planted_off_line : ¬ (∀ s t u : ℝ, s + t + u = 2 * (1 + 2) → s - u = t) := by
  intro h; have := h 4 1 1 (by norm_num); norm_num at this

/-- Planted wrong case: the LO amplitude is nonzero off the line (instance of the blind converse). -/
theorem planted_lo_off_line : (1 : ℝ) / (4 * 1 ^ 2) - ((4 - 1) / (4 * 1)) * 1 / 1 ^ 2 ≠ 0 := by norm_num

/-- `bdm_g1` is not vacuous: at mπ = 1, mK = 2, L's = 1 both sides equal −20. -/
theorem bdm_g1_value :
    (4 * sigmaPiK ((1:ℝ)^2) (2^2) * 1^2 * (-(4*1+1)+2*1) + 2*1^4*1) - ((1:ℝ)/(4*2))*(8*2*1^3*1) = -60 ∧
    4*(1:ℝ)^2*(-(sigmaPiK (1^2) (2^2))*(4*1+1-2*1)) = -60 := by
  simp only [sigmaPiK]; constructor <;> norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR4
