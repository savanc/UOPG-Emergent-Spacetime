/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-3 (2026-11-03) — BLIND second formalisation of MR-4 (πK unequal-mass hidden-zero line).
Written ONLY from the prose of reviews/MR-4-result-2026-10-13.md (Claims, Addendum A) and
reviews/MR-4-prereg-2026-10-13.md (Theory, Observable), BEFORE opening lean/PositiveGeometryEmergentSpaceTime/PiKZero.lean
or its blueprint row. Prose claims: "On s = Σ, s − u = t (so ν = t/4mK)"; "The LO term vanishes on
the line" (Addendum A: F⁺ = t/(4F²), F⁻ = ν mK/F²); "In the equal-mass limit the line is p_π·p_K = 0";
"F^{3/2}(κτ) = g0 + g1τ + g2τ² + g3τ³ with the stated coefficients" (prereg list g0..g3).
Readings chosen here (blind): Σ = Mπ² + MK²; on-shell s + t + u = 2Σ; ν = (s − u)/(4 mK);
F^{3/2} = F⁺ − F⁻, truncated at total degree 3 in τ after x = ν/mπ = κτ.
Not blinded: `bdm_g0/g1/g2` (needs the BDM NLO formulas, not in the prose).
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Mr4Blind

variable {K : Type*} [Field K] [CharZero K]

/-- On the line s = Σ (with s + t + u = 2Σ), s − u = t. -/
theorem line_s_sub_u (Mpi2 MK2 s t u : K) (hon : s + t + u = 2 * (Mpi2 + MK2))
    (hline : s = Mpi2 + MK2) : s - u = t := by
  subst hline; linear_combination -hon

/-- Hence ν = (s − u)/(4 mK) = t/(4 mK) on the line. -/
theorem line_nu (Mpi2 MK2 mK s t u : K) (hon : s + t + u = 2 * (Mpi2 + MK2))
    (hline : s = Mpi2 + MK2) : (s - u) / (4 * mK) = t / (4 * mK) := by
  rw [line_s_sub_u Mpi2 MK2 s t u hon hline]

/-- LO: with F⁺ = t/(4F²), F⁻ = ν mK/F², ν = (s−u)/(4mK), mK ≠ 0, on shell,
F^{3/2} = F⁺ − F⁻ = (Σ − s)/(2F²). -/
theorem lo_closed (Mpi2 MK2 mK F s t u : K) (hmK : mK ≠ 0) (hF : F ≠ 0)
    (hon : s + t + u = 2 * (Mpi2 + MK2)) :
    t / (4 * F ^ 2) - ((s - u) / (4 * mK)) * mK / F ^ 2 = (Mpi2 + MK2 - s) / (2 * F ^ 2) := by
  have hu : u = 2 * (Mpi2 + MK2) - s - t := by linear_combination hon
  subst hu; field_simp; ring

/-- BLIND CLAIM: the LO F^{3/2} vanishes on the whole line s = Σ. -/
theorem lo_zero_on_line (Mpi2 MK2 mK F s t u : K) (hmK : mK ≠ 0) (hF : F ≠ 0)
    (hon : s + t + u = 2 * (Mpi2 + MK2)) (hline : s = Mpi2 + MK2) :
    t / (4 * F ^ 2) - ((s - u) / (4 * mK)) * mK / F ^ 2 = 0 := by
  rw [lo_closed Mpi2 MK2 mK F s t u hmK hF hon, hline]; simp

/-- Converse (blind extra): off the line the LO F^{3/2} is nonzero (char ≠ 2). -/
theorem lo_ne_zero_off_line (Mpi2 MK2 mK F s t u : K) (hmK : mK ≠ 0) (hF : F ≠ 0)
    (hon : s + t + u = 2 * (Mpi2 + MK2)) (hoff : s ≠ Mpi2 + MK2) :
    t / (4 * F ^ 2) - ((s - u) / (4 * mK)) * mK / F ^ 2 ≠ 0 := by
  rw [lo_closed Mpi2 MK2 mK F s t u hmK hF hon]
  have : Mpi2 + MK2 - s ≠ 0 := sub_ne_zero.mpr (Ne.symm hoff)
  exact div_ne_zero this (mul_ne_zero two_ne_zero (pow_ne_zero 2 hF))

/-- Kinematics: for any symmetric bilinear "Minkowski" form B, s = B(p+q,p+q) with
B(p,p) = Mπ², B(q,q) = MK² gives s = Σ + 2 B(p,q). So s = Σ ⇔ p_π·p_K = 0
(for every mass pair, in particular the equal-mass limit). -/
theorem line_iff_dot_zero {V : Type*} [AddCommGroup V] [Module K V]
    (B : LinearMap.BilinForm K V) (hB : B.IsSymm) (p q : V) :
    B (p + q) (p + q) = B p p + B q q ↔ B p q = 0 := by
  have h : B (p + q) (p + q) = B p p + B q q + 2 * B p q := by
    simp only [map_add, LinearMap.add_apply]
    rw [show B q p = B p q from hB.eq q p]; ring
  rw [h]; constructor
  · intro h2; have : (2 : K) * B p q = 0 := by linear_combination h2
    simpa using this
  · intro h0; rw [h0]; ring

/-- Truncated subthreshold expansion (prereg): F⁺ = Σ_{i+2j≤3} C⁺ij τ^i x^{2j},
F⁻ = x Σ_{1+i+2j≤3} C⁻ij τ^i x^{2j}. -/
def Fplus (Cp00 Cp10 Cp20 Cp30 Cp01 Cp11 τ x : K) : K :=
  Cp00 + Cp10 * τ + Cp20 * τ ^ 2 + Cp30 * τ ^ 3 + Cp01 * x ^ 2 + Cp11 * τ * x ^ 2
def Fminus (Cm00 Cm10 Cm20 Cm01 τ x : K) : K :=
  x * (Cm00 + Cm10 * τ + Cm20 * τ ^ 2 + Cm01 * x ^ 2)

/-- BLIND CLAIM: restricted to the line (x = κτ), F⁺ − F⁻ = g0 + g1τ + g2τ² + g3τ³ with
g0 = C⁺00, g1 = C⁺10 − κC⁻00, g2 = C⁺20 + κ²C⁺01 − κC⁻10, g3 = C⁺30 + κ²C⁺11 − κC⁻20 − κ³C⁻01. -/
theorem line_restriction (Cp00 Cp10 Cp20 Cp30 Cp01 Cp11 Cm00 Cm10 Cm20 Cm01 κ τ : K) :
    Fplus Cp00 Cp10 Cp20 Cp30 Cp01 Cp11 τ (κ * τ) - Fminus Cm00 Cm10 Cm20 Cm01 τ (κ * τ)
      = Cp00 + (Cp10 - κ * Cm00) * τ + (Cp20 + κ ^ 2 * Cp01 - κ * Cm10) * τ ^ 2
        + (Cp30 + κ ^ 2 * Cp11 - κ * Cm20 - κ ^ 3 * Cm01) * τ ^ 3 := by
  unfold Fplus Fminus; ring

/-- κ: on the line x = ν/mπ = t/(4 mK mπ) = κ τ with τ = t/mπ², κ = mπ/(4mK). -/
theorem kappa_line (mpi mK t : K) (hpi : mpi ≠ 0) (hK : mK ≠ 0) :
    (t / (4 * mK)) / mpi = (mpi / (4 * mK)) * (t / mpi ^ 2) := by
  field_simp

end PositiveGeometryEmergentSpaceTime.Alignment.Mr4Blind
