/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
M2f — a mass shift for Weinberg's s − M².
Pre-registration: prereg/M2f-mass-shift-2026-10-10.md. Script: scripts/m2f_mass_shift.py.
Sources: [N] arXiv:2401.05483 eqs. 1–2, 8 (δ-shift; general mass deformation of the shift);
[CGW] Carrillo González & Ward, arXiv:2601.16860 eqs. 10–13, 26–35 (massive NLSM = NLSM at X̃ = X − M²);
[KMS] Knecht, Moussallam, Stern, hep-ph/9411259 eq. 1 (O(p²) ππ amplitude, generalised ChPT).
Conventions (mostly-minus, as [CGW]): X_ij = (p_i + … + p_{j−1})², p_i² = M², X̃ = X − M².
Ansatz: Y = X + μ + δ·a* with constant offsets μ; a* the M2d δ-shift (a_oo = −1, a_ee = +1, a_oe = 0).
Every LIMIT is a genuine `Filter.Tendsto … atTop`, obtained from the M2d limits (`PositiveGeometryEmergentSpaceTime.NLSM`)
evaluated at shifted arguments: the δ-limit depends on X only through X + μ. That reuse is the point:
the new content here is the identification, the dressing, the soft values and the offset uniqueness.
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.NLSM

open Filter Topology

namespace PositiveGeometryEmergentSpaceTime.MassShift
open PositiveGeometryEmergentSpaceTime.NLSM

/-! ## n = 4 -/

/-- LIMIT (any constant offsets): δ²·A4(X13 + μ13 − δ, X24 + μ24 + δ) → −(X13 + X24 + μ13 + μ24). -/
theorem mshift4_limit (X13 X24 μ13 μ24 : ℝ) :
    Tendsto (fun δ : ℝ => δ ^ 2 * A4 (X13 + μ13 - δ) (X24 + μ24 + δ)) atTop
      (𝓝 (-(X13 + X24 + μ13 + μ24))) := by
  have h := shift4_limit (X13 := X13 + μ13) (X24 := X24 + μ24)
  convert h using 2; ring

/-- LIMIT (uniform mass, μ = −M²): δ²·A4 → −(X13 + X24 − 2M²) = −(X̃13 + X̃24). -/
theorem mshift4_uniform (X13 X24 M2 : ℝ) :
    Tendsto (fun δ : ℝ => δ ^ 2 * A4 (X13 - M2 - δ) (X24 - M2 + δ)) atTop
      (𝓝 (-(X13 + X24 - 2 * M2))) := by
  have h := mshift4_limit X13 X24 (-M2) (-M2)
  convert h using 3; ring

/-- Massive non-planar variable c13 = −2 p1·p3 = X13 + X24 − X14 − X23 with the on-shell boundary
values X14 = X23 = M² ([CGW] eq. 11–12). -/
def c13m (X13 X24 M2 : ℝ) : ℝ := X13 + X24 - M2 - M2

/-- IDENTITY: the uniform-mass limit is −c13 (massive), i.e. the [CGW] eq. 28 structure. -/
theorem mshift4_eq_neg_c13 (X13 X24 M2 : ℝ) : -(X13 + X24 - 2 * M2) = -c13m X13 X24 M2 := by
  simp only [c13m]; ring

/-- IDENTITY (SU(2) dressing). With the ordered amplitude f(x,y) = κ(x + y − 2c) and the trace coefficients
of Tr(σ_aσ_bσ_cσ_d) = 2(δ_abδ_cd − δ_acδ_bd + δ_adδ_bc) over the six orderings (1,σ(2),σ(3),σ(4))
(coefficients +2,+2,−2,+2,−2,+2 for δ_12δ_34; computed in the script), the δ_12δ_34 coefficient is
8κ(s − c). Here s = s12, t = s23, u = s13, on shell s + t + u = 4M². -/
theorem dressing_coeff (κ c s t u : ℝ) :
    let f := fun x y : ℝ => κ * (x + y - 2 * c)
    2 * (f s t + f s u - f u t + f u s - f t u + f t s) = 8 * κ * (s - c) := by
  intro f; simp only [f]; ring

/-- Weinberg's form A(s,t,u) ∝ (s − M²) holds for all s iff c = M² (κ ≠ 0). -/
theorem weinberg_iff (κ c M2 : ℝ) (hκ : κ ≠ 0) :
    (∀ s : ℝ, 8 * κ * (s - c) = 8 * κ * (s - M2)) ↔ c = M2 := by
  constructor
  · intro h
    have h0 := h 0
    have : 8 * κ * (M2 - c) = 0 := by linarith
    rcases mul_eq_zero.mp this with h1 | h1
    · exact absurd (by linarith : κ = 0) hκ
    · linarith
  · rintro rfl s; rfl

/-- With uniform offsets, the shift constant is c = −(μ13 + μ24)/2 = M². -/
theorem uniform_c (M2 : ℝ) : -((-M2) + (-M2)) / 2 = M2 := by ring

/-- (d2) at n = 4: if the limit −(X13 + X24 + μ13 + μ24) has the massive hidden zero (it vanishes whenever
c13 = 0), then μ13 + μ24 = −2M², i.e. c = M². -/
theorem hidden_zero4_forces (μ13 μ24 M2 : ℝ)
    (h : ∀ X13 X24 : ℝ, c13m X13 X24 M2 = 0 → -(X13 + X24 + μ13 + μ24) = 0) :
    μ13 + μ24 = -2 * M2 := by
  have := h (2 * M2) 0 (by simp only [c13m]; ring)
  linarith

/-- (b1) n = 4: at the formal soft point of leg 1 (X̃13 = X̃24 = 0, i.e. X13 = X24 = M²) the uniform-mass
limit vanishes. -/
theorem msoft4_zero (M2 : ℝ) : -(M2 + M2 - 2 * M2) = 0 := by ring

/-- (b2) n = 4: at the naive massless soft point X13 = X24 = 0 (s = t = 0) the value is +2M² ≠ 0
(for M ≠ 0): the Adler zero is broken by exactly O(M²). -/
theorem msoft4_naive (M2 : ℝ) : -((0 : ℝ) + 0 - 2 * M2) = 2 * M2 := by ring

/-! ## Scattering lengths (LO, threshold s = 4M², t = u = 0) -/

/-- Isospin-0 threshold amplitude for A(s,t,u) = (s − c)/F²: 3A(s,t,u) + A(t,s,u) + A(u,t,s). -/
theorem T0_threshold (M2 c F : ℝ) :
    3 * ((4 * M2 - c) / F ^ 2) + (0 - c) / F ^ 2 + (0 - c) / F ^ 2 = (12 * M2 - 5 * c) / F ^ 2 := by ring

/-- Isospin-2 threshold amplitude: A(t,s,u) + A(u,t,s). -/
theorem T2_threshold (c F : ℝ) : (0 - c) / F ^ 2 + (0 - c) / F ^ 2 = -2 * c / F ^ 2 := by ring

/-- a0⁰ = T0/(32π) for general c. -/
noncomputable def a00 (M2 c F : ℝ) : ℝ := (12 * M2 - 5 * c) / (32 * Real.pi * F ^ 2)
/-- a0² = T2/(32π) for general c. -/
noncomputable def a20 (c F : ℝ) : ℝ := -2 * c / (32 * Real.pi * F ^ 2)

/-- At c = M²: Weinberg's a0⁰ = 7M²/(32πF²), a0² = −M²/(16πF²). -/
theorem weinberg_lengths (M2 F : ℝ) :
    a00 M2 M2 F = 7 * M2 / (32 * Real.pi * F ^ 2) ∧ a20 M2 F = -M2 / (16 * Real.pi * F ^ 2) := by
  constructor
  · simp only [a00]; ring
  · simp only [a20]
    rw [show (16 : ℝ) * Real.pi * F ^ 2 = (32 * Real.pi * F ^ 2) / 2 by ring, div_div_eq_mul_div]
    ring

/-- The dimensionless LO ratio a0⁰/a0² equals −7/2 iff c = M² (for c ≠ 0, F ≠ 0). M and F drop out. -/
theorem ratio_iff (M2 c F : ℝ) (hc : c ≠ 0) (hF : F ≠ 0) :
    a00 M2 c F / a20 c F = -7 / 2 ↔ c = M2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hD : (32 * Real.pi * F ^ 2) ≠ 0 := by positivity
  have key : a00 M2 c F / a20 c F = (12 * M2 - 5 * c) / (-2 * c) := by
    simp only [a00, a20]; field_simp
  rw [key, div_eq_iff (by simpa using hc)]
  constructor <;> intro h <;> linarith

/-! ## n = 6 -/

/-- LIMIT (any constant offsets μ on the nine chords): δ⁴·A6(X + μ + δa*) → A6N(X + μ),
provided the three (o,e) propagators X_oe + μ_oe are nonzero. -/
theorem mshift6_limit {X13 X14 X15 X24 X25 X26 X35 X36 X46 m13 m14 m15 m24 m25 m26 m35 m36 m46 : ℝ}
    (h14 : X14 + m14 ≠ 0) (h25 : X25 + m25 ≠ 0) (h36 : X36 + m36 ≠ 0) :
    Tendsto (fun δ : ℝ => δ ^ 4 * A6 (X13 + m13 - δ) (X14 + m14) (X15 + m15 - δ) (X24 + m24 + δ) (X25 + m25)
        (X26 + m26 + δ) (X35 + m35 - δ) (X36 + m36) (X46 + m46 + δ)) atTop
      (𝓝 (A6N (X13 + m13) (X14 + m14) (X15 + m15) (X24 + m24) (X25 + m25) (X26 + m26) (X35 + m35)
        (X36 + m36) (X46 + m46))) :=
  shift6_limit h14 h25 h36

/-- LIMIT (uniform mass): δ⁴·A6(X − M² + δa*) → A6N(X̃), the massive 6-pion amplitude of [CGW]
(checked independently in the Cayley parametrisation by the script: A6_FR = −A6N(X̃), A4_FR = X̃13 + X̃24). -/
theorem mshift6_uniform {X13 X14 X15 X24 X25 X26 X35 X36 X46 M2 : ℝ}
    (h14 : X14 - M2 ≠ 0) (h25 : X25 - M2 ≠ 0) (h36 : X36 - M2 ≠ 0) :
    Tendsto (fun δ : ℝ => δ ^ 4 * A6 (X13 - M2 - δ) (X14 - M2) (X15 - M2 - δ) (X24 - M2 + δ) (X25 - M2)
        (X26 - M2 + δ) (X35 - M2 - δ) (X36 - M2) (X46 - M2 + δ)) atTop
      (𝓝 (A6N (X13 - M2) (X14 - M2) (X15 - M2) (X24 - M2) (X25 - M2) (X26 - M2) (X35 - M2)
        (X36 - M2) (X46 - M2))) :=
  shift6_limit h14 h25 h36

/-- (b1) n = 6: formal soft p1 with the other legs on shell (X13, X26 → M², X14 → X24, X15 → X25) sends the
massive amplitude A6N(X̃) to 0. -/
theorem msoft6_leg1 {X24 X25 X35 X36 X46 M2 : ℝ} (h24 : X24 - M2 ≠ 0) (h25 : X25 - M2 ≠ 0) (h36 : X36 - M2 ≠ 0) :
    A6N (M2 - M2) (X24 - M2) (X25 - M2) (X24 - M2) (X25 - M2) (M2 - M2) (X35 - M2) (X36 - M2) (X46 - M2) = 0 := by
  simpa using nlsm6_adler (X35 := X35 - M2) (X46 := X46 - M2) h24 h25 h36

/-! ## (d) Offsets: what is forced -/

/-- (d0) IDENTITY: moving the offsets along a* (μ ↦ μ + λa*, i.e. δ ↦ δ + λ) does not change A6N. -/
theorem a6n_reparam (Z13 Z14 Z15 Z24 Z25 Z26 Z35 Z36 Z46 l : ℝ) :
    A6N (Z13 - l) Z14 (Z15 - l) (Z24 + l) Z25 (Z26 + l) (Z35 - l) Z36 (Z46 + l) =
      A6N Z13 Z14 Z15 Z24 Z25 Z26 Z35 Z36 Z46 := by
  simp only [A6N]; ring

/-- (d0) at n = 4. -/
theorem a4n_reparam (Z13 Z24 l : ℝ) : A4N (Z13 - l) (Z24 + l) = A4N Z13 Z24 := by simp only [A4N]; ring

/-- (d1) UNIQUENESS. With the internal pion poles at the physical mass (v_oe = 0, condition (P)), if the limit
A6N(X̃ + v) equals the massive amplitude A6N(X̃) for every X̃ with nonzero poles, then v = λ·a*-pattern:
v13 = v15 = v35 = −v46 and v24 = v26 = v46. Proof: evaluation at ten explicit points. -/
theorem offsets_forced6 (v13 v15 v24 v26 v35 v46 : ℝ)
    (h : ∀ Z13 Z14 Z15 Z24 Z25 Z26 Z35 Z36 Z46 : ℝ, Z14 ≠ 0 → Z25 ≠ 0 → Z36 ≠ 0 →
      A6N (Z13 + v13) Z14 (Z15 + v15) (Z24 + v24) Z25 (Z26 + v26) (Z35 + v35) Z36 (Z46 + v46) =
        A6N Z13 Z14 Z15 Z24 Z25 Z26 Z35 Z36 Z46) :
    v13 = -v46 ∧ v15 = -v46 ∧ v35 = -v46 ∧ v24 = v46 ∧ v26 = v46 := by
  have e0 := h 0 1 0 0 1 0 0 1 0 one_ne_zero one_ne_zero one_ne_zero
  have e1 := h 0 2 0 0 1 0 0 1 0 two_ne_zero one_ne_zero one_ne_zero
  have e3 := h 0 1 0 0 1 0 0 2 0 one_ne_zero one_ne_zero two_ne_zero
  have f13 := h 1 1 0 0 1 0 0 1 0 one_ne_zero one_ne_zero one_ne_zero
  have g13 := h 1 2 0 0 1 0 0 1 0 two_ne_zero one_ne_zero one_ne_zero
  have f15 := h 0 1 1 0 1 0 0 1 0 one_ne_zero one_ne_zero one_ne_zero
  have g15 := h 0 2 1 0 1 0 0 1 0 two_ne_zero one_ne_zero one_ne_zero
  have f35 := h 0 1 0 0 1 0 1 1 0 one_ne_zero one_ne_zero one_ne_zero
  have g35 := h 0 1 0 0 1 0 1 2 0 one_ne_zero one_ne_zero two_ne_zero
  simp only [A6N] at e0 e1 e3 f13 g13 f15 g15 f35 g35
  norm_num at e0 e1 e3 f13 g13 f15 g15 f35 g35
  -- β1 = v15 + v46, α2 = v35 + v46 from (f13 − e0) and (g13 − e1)
  have hb1 : v15 + v46 = 0 := by linear_combination (2 : ℝ) * (f13 - e0) - 2 * (g13 - e1)
  have ha2 : v35 + v46 = 0 := by linear_combination (-1 : ℝ) * (f13 - e0) + 2 * (g13 - e1)
  -- α1 = v13 + v24, β3 = v35 + v24 from Z15
  have ha1 : v13 + v24 = 0 := by linear_combination (2 : ℝ) * (f15 - e0) - 2 * (g15 - e1)
  have hb3 : v35 + v24 = 0 := by linear_combination (-1 : ℝ) * (f15 - e0) + 2 * (g15 - e1)
  -- β2 = v13 + v26, α3 = v15 + v26 from Z35
  have hb2 : v13 + v26 = 0 := by linear_combination (2 : ℝ) * (f35 - e0) - 2 * (g35 - e3)
  have ha3 : v15 + v26 = 0 := by linear_combination (-1 : ℝ) * (f35 - e0) + 2 * (g35 - e3)
  refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith⟩

/-- (d1) CONVERSE: every such v (uniform mass up to δ-reparametrisation) does give the massive
  amplitude. -/
theorem offsets_forced6_converse (Z13 Z14 Z15 Z24 Z25 Z26 Z35 Z36 Z46 l : ℝ) :
    A6N (Z13 + -l) Z14 (Z15 + -l) (Z24 + l) Z25 (Z26 + l) (Z35 + -l) Z36 (Z46 + l) =
      A6N Z13 Z14 Z15 Z24 Z25 Z26 Z35 Z36 Z46 := by
  simp only [A6N]; ring

/-- (d2) UNIQUENESS from hidden zeros. With (P) (v_oe = 0), if A6N(X̃ + v) vanishes on the massive
skinny-rectangle loci c = 0 with indices [1, 3] (the M2d loci, in X̃), then v lies on the a* line: uniform mass up to
δ-reparametrisation. Proof: evaluation at explicit points on the loci; the rational combinations were
found by `scripts/m2f_d2_cert.py` and are re-checked here by `linear_combination`. -/
theorem hidden_zeros_force6 (v13 v15 v24 v26 v35 v46 : ℝ)
    (z1 : ∀ Z14 Z25 Z26 Z35 Z36 Z46 : ℝ, Z14 ≠ 0 → Z25 ≠ 0 → Z36 ≠ 0 →
      A6N (-Z26 + v13) (Z14) (Z25 - Z26 + v15) (Z14 + Z26 + v24) (Z25) (Z26 + v26) (Z35 + v35) (Z36) (Z46 + v46) = 0)
    (z3 : ∀ Z14 Z15 Z25 Z26 Z36 Z46 : ℝ, Z14 ≠ 0 → Z25 ≠ 0 → Z36 ≠ 0 →
      A6N (Z14 + Z36 - Z46 + v13) (Z14) (Z15 + v15) (-Z36 + Z46 + v24) (Z25) (Z26 + v26) (Z36 - Z46 + v35) (Z36) (Z46 + v46) = 0)
    : v13 = -v46 ∧ v15 = -v46 ∧ v35 = -v46 ∧ v24 = v46 ∧ v26 = v46 := by
  have e0 := z1 (-1) (-2) (0) (2) (-3) (-3) (by norm_num) (by norm_num) (by norm_num)
  have e1 := z1 (3) (1) (-3) (-1) (1) (-3) (by norm_num) (by norm_num) (by norm_num)
  have e2 := z1 (1) (-2) (-3) (-3) (1) (0) (by norm_num) (by norm_num) (by norm_num)
  have e3 := z1 (-2) (-3) (1) (0) (-3) (3) (by norm_num) (by norm_num) (by norm_num)
  have e4 := z1 (1) (-3) (-2) (2) (2) (1) (by norm_num) (by norm_num) (by norm_num)
  have e5 := z1 (-3) (1) (1) (0) (-3) (-2) (by norm_num) (by norm_num) (by norm_num)
  have e12 := z3 (1) (0) (-1) (-1) (-2) (3) (by norm_num) (by norm_num) (by norm_num)
  have e13 := z3 (-2) (2) (3) (-2) (-3) (1) (by norm_num) (by norm_num) (by norm_num)
  simp only [A6N] at e0 e1 e2 e3 e4 e5 e12 e13
  have h1 : v13 + v46 = 0 := by linear_combination (16940/34941 : ℝ) * e0 + (-76345/69882 : ℝ) * e1 + (116807/104823 : ℝ) * e2 + (5742/11647 : ℝ) * e3 + (58961/34941 : ℝ) * e4 + (18855/11647 : ℝ) * e5 + (-2/3 : ℝ) * e12 + (1 : ℝ) * e13
  have h2 : v15 + v46 = 0 := by linear_combination (13259/34941 : ℝ) * e0 + (-44837/34941 : ℝ) * e1 + (162023/104823 : ℝ) * e2 + (5901/11647 : ℝ) * e3 + (45326/34941 : ℝ) * e4 + (21513/11647 : ℝ) * e5 + (-2/3 : ℝ) * e12 + (1 : ℝ) * e13
  have h3 : v35 + v46 = 0 := by linear_combination (-1952/58235 : ℝ) * e0 + (63127/116470 : ℝ) * e1 + (-76403/174705 : ℝ) * e2 + (-29847/58235 : ℝ) * e3 + (-40349/58235 : ℝ) * e4 + (-45378/58235 : ℝ) * e5 + (2/5 : ℝ) * e12
  have h4 : v24 - v46 = 0 := by linear_combination (-11453/34941 : ℝ) * e0 + (68107/69882 : ℝ) * e1 + (-96812/104823 : ℝ) * e2 + (-7830/11647 : ℝ) * e3 + (-59225/34941 : ℝ) * e4 + (-16182/11647 : ℝ) * e5 + (2/3 : ℝ) * e12 + (-1 : ℝ) * e13
  have h5 : v26 - v46 = 0 := by linear_combination (-14888/34941 : ℝ) * e0 + (36890/34941 : ℝ) * e1 + (-121766/104823 : ℝ) * e2 + (-9675/11647 : ℝ) * e3 + (-61868/34941 : ℝ) * e4 + (-19995/11647 : ℝ) * e5 + (2/3 : ℝ) * e12 + (-1 : ℝ) * e13
  refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith⟩
/-- (d2) UNIQUENESS from hidden zeros. With (P) (v_oe = 0), if A6N(X̃ + v) vanishes on the massive
skinny-rectangle loci c = 0 with indices [1, 4] (the M2d loci, in X̃), then v lies on the a* line: uniform mass up to
δ-reparametrisation. Proof: evaluation at explicit points on the loci; the rational combinations were
found by `scripts/m2f_d2_cert.py` and are re-checked here by `linear_combination`. -/
theorem hidden_zeros_force6_opp (v13 v15 v24 v26 v35 v46 : ℝ)
    (z1 : ∀ Z14 Z25 Z26 Z35 Z36 Z46 : ℝ, Z14 ≠ 0 → Z25 ≠ 0 → Z36 ≠ 0 →
      A6N (-Z26 + v13) (Z14) (Z25 - Z26 + v15) (Z14 + Z26 + v24) (Z25) (Z26 + v26) (Z35 + v35) (Z36) (Z46 + v46) = 0)
    (z4 : ∀ Z13 Z14 Z25 Z26 Z36 Z46 : ℝ, Z14 ≠ 0 → Z25 ≠ 0 → Z36 ≠ 0 →
      A6N (Z13 + v13) (Z14) (Z14 - Z46 + v15) (Z25 + Z46 + v24) (Z25) (Z26 + v26) (-Z46 + v35) (Z36) (Z46 + v46) = 0)
    : v13 = -v46 ∧ v15 = -v46 ∧ v35 = -v46 ∧ v24 = v46 ∧ v26 = v46 := by
  have e0 := z1 (-1) (-2) (0) (2) (-3) (-3) (by norm_num) (by norm_num) (by norm_num)
  have e1 := z1 (3) (1) (-3) (-1) (1) (-3) (by norm_num) (by norm_num) (by norm_num)
  have e2 := z1 (1) (-2) (-3) (-3) (1) (0) (by norm_num) (by norm_num) (by norm_num)
  have e3 := z1 (-2) (-3) (1) (0) (-3) (3) (by norm_num) (by norm_num) (by norm_num)
  have e4 := z1 (1) (-3) (-2) (2) (2) (1) (by norm_num) (by norm_num) (by norm_num)
  have e5 := z1 (-3) (1) (1) (0) (-3) (-2) (by norm_num) (by norm_num) (by norm_num)
  have e12 := z4 (1) (1) (-1) (-1) (-2) (3) (by norm_num) (by norm_num) (by norm_num)
  have e13 := z4 (2) (3) (-2) (-3) (1) (-1) (by norm_num) (by norm_num) (by norm_num)
  simp only [A6N] at e0 e1 e2 e3 e4 e5 e12 e13
  have h1 : v13 + v46 = 0 := by linear_combination (-9133/23294 : ℝ) * e0 + (717055/93176 : ℝ) * e1 + (-1599821/139764 : ℝ) * e2 + (-323151/46588 : ℝ) * e3 + (-329561/46588 : ℝ) * e4 + (-181347/23294 : ℝ) * e5 + (15/2 : ℝ) * e12 + (6 : ℝ) * e13
  have h2 : v15 + v46 = 0 := by linear_combination (-11587/23294 : ℝ) * e0 + (699283/93176 : ℝ) * e1 + (-1539533/139764 : ℝ) * e2 + (-322515/46588 : ℝ) * e3 + (-347741/46588 : ℝ) * e4 + (-176031/23294 : ℝ) * e5 + (15/2 : ℝ) * e12 + (6 : ℝ) * e13
  have h3 : v35 + v46 = 0 := by linear_combination (2705/23294 : ℝ) * e0 + (89785/93176 : ℝ) * e1 + (-166835/139764 : ℝ) * e2 + (-30801/46588 : ℝ) * e3 + (-13079/46588 : ℝ) * e4 + (-30663/23294 : ℝ) * e5 + (1/2 : ℝ) * e12
  have h4 : v24 - v46 = 0 := by linear_combination (12791/23294 : ℝ) * e0 + (-728039/93176 : ℝ) * e1 + (1626481/139764 : ℝ) * e2 + (314799/46588 : ℝ) * e3 + (329209/46588 : ℝ) * e4 + (186693/23294 : ℝ) * e5 + (-15/2 : ℝ) * e12 + (-6 : ℝ) * e13
  have h5 : v26 - v46 = 0 := by linear_combination (10501/23294 : ℝ) * e0 + (-720475/93176 : ℝ) * e1 + (1593209/139764 : ℝ) * e2 + (307419/46588 : ℝ) * e3 + (325685/46588 : ℝ) * e4 + (179067/23294 : ℝ) * e5 + (-15/2 : ℝ) * e12 + (-6 : ℝ) * e13
  refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith⟩

end PositiveGeometryEmergentSpaceTime.MassShift
