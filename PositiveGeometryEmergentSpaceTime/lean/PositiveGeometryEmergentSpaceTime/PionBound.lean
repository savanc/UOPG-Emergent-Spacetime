/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Dispersion

/-!
M2 / P-EFT, Lean part 2: the algebraic map from "d²T/ds² ≥ 0" to bounds on the chiral
low-energy constants l̄₁, l̄₂ (Manohar-Mateu 2008, Table 1, first two rows).

Conventions (all CITED, see prereg/M2-positivity-2026-10-10.md):
  * pion mass M_π = 1; the overall positive factor x₂²/(16π²), x₂ = M_π²/F_π², is divided out;
  * O(p⁴) amplitude A(s,t,u) in the form of Bijnens et al. 1997 (hep-ph/9707291) eq. (4.14):
    only the s-dependent part matters (b₁, b₂ and the O(p²) term are at most linear in s and
    drop out of the second derivative);
  * 16π² b₃ = l̄₁/3 + l̄₂/6 − 7/12, 16π² b₄ = l̄₂/6 − 5/36 (ibid. eqs. (D.1)–(D.3));
  * 16π² J̄(z) = z/6 + z²/60 + O(z³) (Taylor series at z = 0; checked numerically in
    scripts/m2_pipi_bound.py). Second derivatives at s = 0 of J̄(±s)·(polynomial) only see
    these two coefficients, so the truncation is exact for the quantity we need;
  * J̄ at the fixed point t = 4 is an s-independent constant `Jt` (kept symbolic).
-/

namespace PositiveGeometryEmergentSpaceTime.PionBound

noncomputable section

/-- Truncated `16π² J̄`. -/
def J2 (z : ℝ) : ℝ := z / 6 + z ^ 2 / 60

/-- `16π² b₃`, `16π² b₄` at leading order. -/
def b3 (l1 l2 : ℝ) : ℝ := l1 / 3 + l2 / 6 - 7 / 12
/-- Coefficient `b₄(l₂) = l₂/6 − 5/36`. -/
def b4 (l2 : ℝ) : ℝ := l2 / 6 - 5 / 36

/-- s-relevant part of `(16π²/x₂²)·A(S,T,U)` at O(p⁴); `JS, JT, JU` are the values of
`16π² J̄` at `S, T, U`. -/
def A (l1 l2 JS JT JU S T U : ℝ) : ℝ :=
  b3 l1 l2 * S ^ 2 + b4 l2 * (T - U) ^ 2 + JS * (S ^ 2 - 1) / 2
    + JT * (14 - 4 * S - 10 * T + S * T + 2 * T ^ 2) / 6
    + JU * (14 - 4 * S - 10 * U + S * U + 2 * U ^ 2) / 6

/-- π⁺π⁰ → π⁺π⁰ = A(t,s,u), at t = 4 (so u = −s). -/
def Tpm (l1 l2 Jt s : ℝ) : ℝ := A l1 l2 Jt (J2 s) (J2 (-s)) 4 s (-s)

/-- π⁰π⁰ → π⁰π⁰ = A(s,t,u) + A(t,s,u) + A(u,t,s), at t = 4. -/
def T00 (l1 l2 Jt s : ℝ) : ℝ :=
  A l1 l2 (J2 s) Jt (J2 (-s)) s 4 (-s) + A l1 l2 Jt (J2 s) (J2 (-s)) 4 s (-s)
    + A l1 l2 (J2 (-s)) Jt (J2 s) (-s) 4 s

/-- Exact polynomial form of the π⁺π⁰ amplitude: the s² coefficient is (2/3)(l̄₂ − 27/20). -/
theorem Tpm_poly (l1 l2 Jt s : ℝ) :
    Tpm l1 l2 Jt s = (45 * Jt + 32 * l1 + 16 * l2 - 56) / 6
      + (2 / 3) * (l2 - 27 / 20) * s ^ 2 + (1 / 90) * s ^ 4 := by
  unfold Tpm A J2 b3 b4; ring

/-- Exact polynomial form of the π⁰π⁰ amplitude: the s² coefficient is
(2/3)(l̄₁ + 2 l̄₂ − 157/40). -/
theorem T00_poly (l1 l2 Jt s : ℝ) :
    T00 l1 l2 Jt s = (171 * Jt + 96 * l1 + 144 * l2 - 248) / 18
      + (2 / 3) * (l1 + 2 * l2 - 157 / 40) * s ^ 2 + (1 / 30) * s ^ 4 := by
  unfold T00 A J2 b3 b4; ring

/-- Second derivative at 0 of `c + k s² + q s⁴` is `2k`. -/
theorem deriv2_even_quartic (c k q : ℝ) :
    deriv (deriv fun s : ℝ => c + k * s ^ 2 + q * s ^ 4) 0 = 2 * k := by
  have h1 : ∀ x : ℝ, HasDerivAt (fun s : ℝ => c + k * s ^ 2 + q * s ^ 4)
      (k * (2 * x) + q * (4 * x ^ 3)) x := by
    intro x
    have a := ((hasDerivAt_pow 2 x).const_mul k).const_add c
    have b := (hasDerivAt_pow 4 x).const_mul q
    convert a.add b using 1
    all_goals first | rfl | ring
  have hd : deriv (fun s : ℝ => c + k * s ^ 2 + q * s ^ 4) =
      fun x => k * (2 * x) + q * (4 * x ^ 3) := funext fun x => (h1 x).deriv
  rw [hd]
  have h2 : HasDerivAt (fun x : ℝ => k * (2 * x) + q * (4 * x ^ 3))
      (k * 2 + q * (4 * (3 * 0 ^ 2))) 0 := by
    have a := ((hasDerivAt_id (0:ℝ)).const_mul 2).const_mul k
    have b := (((hasDerivAt_pow 3 (0:ℝ))).const_mul 4).const_mul q
    convert a.add b using 1
    all_goals first | rfl | simp
  rw [h2.deriv]; ring

/-- d²/ds² of the π⁺π⁰ one-loop amplitude at (s = 0, t = 4m²), in units x₂²/(16π²). -/
theorem deriv2_Tpm (l1 l2 Jt : ℝ) :
    deriv (deriv fun s => Tpm l1 l2 Jt s) 0 = (4 / 3) * (l2 - 27 / 20) := by
  have : (fun s => Tpm l1 l2 Jt s) = fun s => (45 * Jt + 32 * l1 + 16 * l2 - 56) / 6
      + (2 / 3) * (l2 - 27 / 20) * s ^ 2 + (1 / 90) * s ^ 4 := funext (Tpm_poly l1 l2 Jt)
  rw [this, deriv2_even_quartic]; ring

/-- Second `s`-derivative of `T00` at `s = 0` is `4/3 · (l₁ + 2l₂ − 157/40)`. -/
theorem deriv2_T00 (l1 l2 Jt : ℝ) :
    deriv (deriv fun s => T00 l1 l2 Jt s) 0 = (4 / 3) * (l1 + 2 * l2 - 157 / 40) := by
  have : (fun s => T00 l1 l2 Jt s) = fun s => (171 * Jt + 96 * l1 + 144 * l2 - 248) / 18
      + (2 / 3) * (l1 + 2 * l2 - 157 / 40) * s ^ 2 + (1 / 30) * s ^ 4 :=
    funext (T00_poly l1 l2 Jt)
  rw [this, deriv2_even_quartic]; ring

/-- L4 (P1). Positivity of the curvature (from `Dispersion.secondDeriv_nonneg_of_dispersion`
or its measure version) applied to the π⁺π⁰ amplitude at O(p⁴) gives **l̄₂ ≥ 27/20**.
Hypothesis `hpos`: the O(p⁴) chiral amplitude obeys the axiomatic bound at this point
(this is where the CITED ChPT-validity assumption enters). -/
theorem lbar2_ge (l1 l2 Jt : ℝ) (hpos : 0 ≤ deriv (deriv fun s => Tpm l1 l2 Jt s) 0) :
    27 / 20 ≤ l2 := by
  rw [deriv2_Tpm] at hpos; linarith

/-- L4 (S1). Same for π⁰π⁰: **l̄₁ + 2 l̄₂ ≥ 157/40**. -/
theorem lbar1_2lbar2_ge (l1 l2 Jt : ℝ) (hpos : 0 ≤ deriv (deriv fun s => T00 l1 l2 Jt s) 0) :
    157 / 40 ≤ l1 + 2 * l2 := by
  rw [deriv2_T00] at hpos; linarith

/-- And the converse direction: the bound is sharp at this order (the curvature is exactly
proportional to the margin), so a violation of the inequality would mean a negative
curvature, i.e. the pre-registered FAIL condition. -/
theorem Tpm_curvature_neg_iff (l1 l2 Jt : ℝ) :
    deriv (deriv fun s => Tpm l1 l2 Jt s) 0 < 0 ↔ l2 < 27 / 20 := by
  rw [deriv2_Tpm]; constructor <;> intro h <;> linarith

/-- Chained statement: dispersion hypotheses (CITED) + matching of the true curvature with
the O(p⁴) amplitude (CITED: ChPT validity at (s,t) = (0,4m²), error O(p⁶)) ⇒ l̄₂ ≥ 27/20. -/
theorem lbar2_ge_of_dispersion
    (l1 l2 Jt s₀ u : ℝ) (imS imU : ℝ → ℝ) (A2 : ℝ)
    (hs : (0:ℝ) < s₀) (hu : u < s₀)
    (himS : ∀ x, s₀ ≤ x → 0 ≤ imS x) (himU : ∀ x, s₀ ≤ x → 0 ≤ imU x)
    (hdisp : A2 = (2 / Real.pi) *
      ∫ x in Set.Ici s₀, (imS x / (x - 0) ^ 3 + imU x / (x - u) ^ 3))
    (hmatch : A2 = deriv (deriv fun s => Tpm l1 l2 Jt s) 0) :
    27 / 20 ≤ l2 := by
  apply lbar2_ge l1 l2 Jt
  rw [← hmatch]
  exact PositiveGeometryEmergentSpaceTime.Dispersion.secondDeriv_nonneg_of_dispersion s₀ 0 u A2 imS imU hs hu himS himU hdisp

end

end PositiveGeometryEmergentSpaceTime.PionBound
