/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
M3: the O(p⁴) ratio fixed by the 4-point hidden zero, and its map to the chiral LECs.
Pre-registration: `prereg/M3-lec-ratio-2026-10-10.md`. Conventions: Albert–Rastelli arXiv:2203.11950,
eqs. (3.4), (4.21), (4.26), (4.27), (4.35). Reuses `PositiveGeometryEmergentSpaceTime.Hankel` (moments, 2×2 Hankel) and
`PositiveGeometryEmergentSpaceTime.NLSM` (`A4`).
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Hankel
import PositiveGeometryEmergentSpaceTime.NLSM

open Finset

namespace PositiveGeometryEmergentSpaceTime.LECRatio

/-! ## L1. Hidden zero at O(p⁴) ⇔ g₂,₁ = g₂,₀ -/

/-- O(p⁴) part of the ordered large-N amplitude, `g20 (s²+u²) + 2 g21 s u` (AR 3.4).

Also known as: LECRatio.P4, LEC quartic polynomial in s and u.
-/
def lecP4 (g20 g21 s u : ℝ) : ℝ := g20 * (s ^ 2 + u ^ 2) + 2 * g21 * s * u

/-- The 4-point hidden zero `s + u = 0` (t = 0; `X13 + X24 = 0`) holds at O(p⁴) iff `g21 = g20`. -/
theorem hidden_zero_iff (g20 g21 : ℝ) : (∀ s, lecP4 g20 g21 s (-s) = 0) ↔ g21 = g20 := by
  constructor
  · intro h
    have := h 1
    simp [lecP4] at this
    linarith
  · rintro rfl s
    simp [lecP4]; ring

/-- On the hidden-zero ray the O(p⁴) amplitude is `g20 (s+u)²`. -/
theorem hidden_zero_form (g20 s u : ℝ) : lecP4 g20 g20 s u = g20 * (s + u) ^ 2 := by
  simp [lecP4]; ring

/-! ## L2. Any completion with an overall (X13 + X24) factor -/

/-- If the quadratic Taylor term `A x² + B x y + C y²` vanishes on `y = -x` (true whenever the amplitude
is `(x+y)·G` with `G` regular), its `x ↔ y` symmetrisation (the cyclic, C-even part) is
`((A+C)/2)(x+y)²`, i.e. `g20 = g21 = (A+C)/2`. -/
theorem sym_part_of_zero (A B C : ℝ) (h : ∀ x : ℝ, A * x ^ 2 + B * x * (-x) + C * (-x) ^ 2 = 0)
    (x y : ℝ) :
    ((A * x ^ 2 + B * x * y + C * y ^ 2) + (A * y ^ 2 + B * y * x + C * x ^ 2)) / 2
      = (A + C) / 2 * (x + y) ^ 2 := by
  have h1 := h 1
  have hB : B = A + C := by linarith
  subst hB; ring

/-- Product form: `(x+y)(c1 x + c2 y)` splits into the C-even piece `((c1+c2)/2)(x+y)²` and the
C-odd piece `((c1-c2)/2)(x²-y²)`. For [H]'s stringy δ-family `c1 - c2 = ψ(-a) - ψ(a)` (script). -/
theorem product_split (c1 c2 x y : ℝ) :
    (x + y) * (c1 * x + c2 * y) = (c1 + c2) / 2 * (x + y) ^ 2 + (c1 - c2) / 2 * (x ^ 2 - y ^ 2) := by
  ring

/-- Field-theory δ-shift (M2d, `NLSM.A4`): the shifted 4-point amplitude carries the exact factor
`X13 + X24` for every δ, so the hidden zero holds to all orders in `1/δ`. -/
theorem shift4_factor (δ X13 X24 : ℝ) (h1 : X13 - δ ≠ 0) (h2 : X24 + δ ≠ 0) :
    δ ^ 2 * PositiveGeometryEmergentSpaceTime.NLSM.A4 (X13 - δ) (X24 + δ)
      = (X13 + X24) * (δ ^ 2 / ((X13 - δ) * (X24 + δ))) := by
  unfold PositiveGeometryEmergentSpaceTime.NLSM.A4
  field_simp
  ring

/-- Its O(p⁴) term is purely C-odd. Exact identity:
`δ² A4 = -(X13+X24) - (X13²-X24²)/δ + R`, with
`R = (X13+X24)(X13²X24 + X13²δ - X13X24² - X13X24δ + X24²δ) / (δ (X13-δ)(X24+δ)) = O(1/δ²)`,
and `R` again carries the factor `X13 + X24`. -/
theorem shift4_expansion (δ X13 X24 : ℝ) (hδ : δ ≠ 0) (h1 : X13 - δ ≠ 0) (h2 : X24 + δ ≠ 0) :
    δ ^ 2 * PositiveGeometryEmergentSpaceTime.NLSM.A4 (X13 - δ) (X24 + δ)
      = -(X13 + X24) - (X13 ^ 2 - X24 ^ 2) / δ
        + (X13 + X24) * (X13 ^ 2 * X24 + X13 ^ 2 * δ - X13 * X24 ^ 2 - X13 * X24 * δ + X24 ^ 2 * δ)
          / (δ * (X13 - δ) * (X24 + δ)) := by
  unfold PositiveGeometryEmergentSpaceTime.NLSM.A4
  field_simp
  ring

/-! ## L3. Map to the chiral LECs (AR 4.21, 4.26, 4.27) -/

/-- SU(N) single-trace couplings (L1' = L2' = 0 at large N): `g20 = g21 ⇔ L3' = 0`. -/
theorem su3_iff (L3p L4p f : ℝ) (hf : f ≠ 0) :
    (2 * L3p + 4 * L4p) / f ^ 4 = 4 * L4p / f ^ 4 ↔ L3p = 0 := by
  have hf4 : f ^ 4 ≠ 0 := pow_ne_zero 4 hf
  constructor
  · intro h
    have := (div_left_inj' hf4).1 h
    linarith
  · rintro rfl; ring_nf

/-- After the N_f = 3 renaming (AR 4.21) with `L1' = L2' = 0`: `2L1 = L2` always (large N_c, not
geometry), and `L3 = -2 L2 ⇔ L3' = 0` (the hidden-zero ray). -/
theorem su3_rename (L3p L4p : ℝ) :
    let L1 := 0 + L4p / 2
    let L2 := 0 + L4p
    let L3 := L3p - 2 * L4p
    2 * L1 = L2 ∧ (L3 = -2 * L2 ↔ L3p = 0) := by
  simp only
  refine ⟨by ring, ?_⟩
  constructor <;> intro h <;> linarith

/-- SU(2) (AR 4.27): `g20 = (2ℓ1+3ℓ2)/(2f⁴)`, `g21 = ℓ2/f⁴`; hidden zero ⇔ `2ℓ1 + ℓ2 = 0`. -/
theorem su2_iff (l1 l2 f : ℝ) (hf : f ≠ 0) :
    (2 * l1 + 3 * l2) / (2 * f ^ 4) = l2 / f ^ 4 ↔ 2 * l1 + l2 = 0 := by
  have hf4 : f ^ 4 ≠ 0 := pow_ne_zero 4 hf
  rw [div_eq_div_iff (mul_ne_zero two_ne_zero hf4) hf4]
  constructor
  · intro h
    have : (2 * l1 + l2) * f ^ 4 = 0 := by linarith
    rcases mul_eq_zero.1 this with h' | h'
    · exact h'
    · exact absurd h' hf4
  · intro h
    have : l2 = -2 * l1 := by linarith
    subst this; ring

/-! ## L4. Consistency with positivity (sum rules AR 4.35, reusing `Hankel.moment`) -/

variable {ι : Type*}

/-- `g20 = Σ w/m⁴` with `x = 1/m²`: the second moment of `Σ w δ_x`. -/
def g20 (S : Finset ι) (w x : ι → ℝ) : ℝ := PositiveGeometryEmergentSpaceTime.Hankel.moment S w x 2

/-- `g21 = g20 - Σ w (-1)^J/m⁴ = Σ w (1 - (-1)^J)/m⁴` (AR 4.35). -/
def g21 (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ) : ℝ :=
  ∑ l ∈ S, w l * (1 - (-1) ^ J l) * x l ^ 2

/-- AR's linear O(p⁴) bounds from positive spectral weight: `0 ≤ g21 ≤ 2 g20`
(ℓ2 ≥ 0 and ℓ1 + ℓ2 ≥ 0). -/
theorem linear_bounds (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ) (hw : ∀ l ∈ S, 0 ≤ w l) :
    0 ≤ g21 S w x J ∧ g21 S w x J ≤ 2 * g20 S w x := by
  unfold g21 g20 PositiveGeometryEmergentSpaceTime.Hankel.moment
  rw [Finset.mul_sum]
  constructor
  · refine Finset.sum_nonneg fun l hl => ?_
    rcases neg_one_pow_eq_or ℝ (J l) with h | h <;> rw [h] <;> nlinarith [hw l hl, sq_nonneg (x l)]
  · refine Finset.sum_le_sum fun l hl => ?_
    rcases neg_one_pow_eq_or ℝ (J l) with h | h <;> rw [h] <;> nlinarith [hw l hl, sq_nonneg (x l)]

/-- The hidden-zero ray `g21 = g20` holds iff the even-spin and odd-spin weights balance,
`Σ w (-1)^J / m⁴ = 0`. -/
theorem hidden_zero_iff_balance (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ) :
    g21 S w x J = g20 S w x ↔ ∑ l ∈ S, w l * (-1) ^ J l * x l ^ 2 = 0 := by
  unfold g21 g20 PositiveGeometryEmergentSpaceTime.Hankel.moment
  have : ∑ l ∈ S, w l * (1 - (-1) ^ J l) * x l ^ 2
      = ∑ l ∈ S, w l * x l ^ 2 - ∑ l ∈ S, w l * (-1) ^ J l * x l ^ 2 := by
    rw [← Finset.sum_sub_distrib]; exact Finset.sum_congr rfl fun l _ => by ring
  rw [this]; constructor <;> intro h <;> linarith

/-- Consistency theorem: a hidden-zero completion with positive spectral weight satisfies all of AR's
linear O(p⁴) bounds, and sits strictly between the scalar edge (`g21 = 0`) and the Skyrme/vector edge
(`g21 = 2 g20`) whenever `g20 > 0`. -/
theorem hidden_zero_consistent (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ)
    (hz : g21 S w x J = g20 S w x) (hpos : 0 < g20 S w x) :
    0 < g21 S w x J ∧ g21 S w x J < 2 * g20 S w x := by
  rw [hz]; constructor <;> linarith

/-- Odd spins only (vector dominance) put the theory on the Skyrme line `g21 = 2 g20`. -/
theorem odd_only_skyrme (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ) (hJ : ∀ l ∈ S, Odd (J l)) :
    g21 S w x J = 2 * g20 S w x := by
  unfold g21 g20 PositiveGeometryEmergentSpaceTime.Hankel.moment
  rw [Finset.mul_sum]
  exact Finset.sum_congr rfl fun l hl => by rw [(hJ l hl).neg_one_pow]; ring

/-- Even spins only give `g21 = 0` (the scalar edge). -/
theorem even_only_zero (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ) (hJ : ∀ l ∈ S, Even (J l)) :
    g21 S w x J = 0 := by
  unfold g21
  exact Finset.sum_eq_zero fun l hl => by rw [(hJ l hl).neg_one_pow]; ring

/-- Forward Hankel bound `g20² ≤ g10 g30` (moments 1, 2, 3 of `Σ w δ_x`, `x = 1/m² ≥ 0`), from M2b's
`moment_sq_le_discrete` applied to the weights `w x`. -/
theorem forward_hankel (S : Finset ι) (w x : ι → ℝ) (hw : ∀ l ∈ S, 0 ≤ w l) (hx : ∀ l ∈ S,
    0 ≤ x l) :
    PositiveGeometryEmergentSpaceTime.Hankel.moment S w x 2 ^ 2
      ≤ PositiveGeometryEmergentSpaceTime.Hankel.moment S w x 1 * PositiveGeometryEmergentSpaceTime.Hankel.moment S w x 3 := by
  have h := PositiveGeometryEmergentSpaceTime.Hankel.moment_sq_le_discrete S (fun l => w l * x l) x
    (fun l hl => mul_nonneg (hw l hl) (hx l hl))
  have e : ∀ k, PositiveGeometryEmergentSpaceTime.Hankel.moment S (fun l => w l * x l) x k = PositiveGeometryEmergentSpaceTime.Hankel.moment S w x (k + 1) :=
    fun k => Finset.sum_congr rfl fun l _ => by ring
  simpa [e] using h

/-! ## L5. Lovelace–Shapiro numbers (closed forms from `scripts/m3_lec_ratio.py`, α′ = 1) -/

/-- LS: `g10 = π`, `g20 = g21 = 2π ln 2`, `g30 = π(12 ln²2 + π²)/6`. The forward Hankel inequality
holds: `g10 g30 - g20² = π²(π² - 12 ln²2)/6 > 0`. -/
theorem ls_hankel :
    (2 * Real.pi * Real.log 2) ^ 2 < Real.pi * (Real.pi * (12 * Real.log 2 ^ 2 + Real.pi ^ 2) / 6) := by
  have hp := Real.pi_gt_three
  have hl := Real.log_two_lt_d9
  have hl0 : 0 < Real.log 2 := Real.log_pos one_lt_two
  have : 12 * Real.log 2 ^ 2 < Real.pi ^ 2 := by nlinarith
  nlinarith [Real.pi_pos, sq_nonneg Real.pi]

/-- LS normalised coupling `g̃2 = ln 2` is below the cutoff bound `g̃2 ≤ 1` (AR 4.10) at `M = m_ρ`,
and `g̃2' = 2 g̃2` (the hidden-zero ray). -/
theorem ls_gt2 : 0 < Real.log 2 ∧ Real.log 2 < 1 := by
  refine ⟨Real.log_pos one_lt_two, ?_⟩
  have := Real.log_two_lt_d9; linarith

/-! ## L6. Data arithmetic (pre-registered rule; BE14 Table 3, uncorrelated errors) -/

/-- Central BE14 ratio `L3/L2 = -3.07/0.81 = -307/81`. -/
theorem be14_central : (-307 / 100 : ℚ) / (81 / 100) = -307 / 81 := by norm_num

/-- FAIL condition, squared form: with `R = -307/81` and
`σ² = R²((0.20/3.07)² + (0.04/0.81)²)`, the 2σ interval lies below the band edge `-2.6`:
`R < -13/5` and `(2σ)² < (-13/5 - R)²`. -/
theorem be14_fail :
    let R : ℚ := -307 / 81
    let σ2 : ℚ := R ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2)
    R < -13 / 5 ∧ 4 * σ2 < (-13 / 5 - R) ^ 2 := by
  norm_num

/-- The band edge is more than 3.8σ away: `(3.8 σ)² < (-13/5 - R)²`. -/
theorem be14_gap :
    let R : ℚ := -307 / 81
    let σ2 : ℚ := R ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2)
    (19 / 5) ^ 2 * σ2 < (-13 / 5 - R) ^ 2 := by
  norm_num


/-! ## L7. Well-posedness check (added in the ladder review, 2026-10-10)

AR's linear bounds `0 ≤ g21 ≤ 2 g20` translate, through the large-N map, into `L3 ≥ -3 L2` (the
Skyrme/vector edge; `ℓ1 + ℓ2 ≥ 0` in SU(2)). So *every* unitary large-N tree completion has
`L3/L2 ≥ -3`; the BE14 NNLO central value `-307/81 < -3` lies outside that region. -/

/-- Linear algebra step: for `f ≠ 0`, `4L₄'/f⁴ ≤ 2(2L₃' + 4L₄')/f⁴` implies `L₃' − 2L₄' ≥ −3L₄'`. -/
theorem l3_ge_neg3_l2 (L3p L4p f : ℝ) (hf : f ≠ 0)
    (hb : 4 * L4p / f ^ 4 ≤ 2 * ((2 * L3p + 4 * L4p) / f ^ 4)) :
    (L3p - 2 * L4p) ≥ -3 * L4p := by
  have hf4 : 0 < f ^ 4 := by positivity
  rw [mul_div_assoc', div_le_div_iff_of_pos_right hf4] at hb
  linarith

/-- `−307/81 < −3` (the BE14 central value of `L₃/L₂` lies below −3). -/
theorem be14_outside_wedge : (-307 / 81 : ℚ) < -3 := by norm_num

/-! ## L8. M3w: reachable region of the M3b family vs the full large-N region (2026-10-11)

Pre-registration `prereg/M3w-wellposedness-2026-10-11.md`. The planned M3b family is the positive
combination of a hidden-zero theory A (`g21 = g20`, ε = 0) and an odd-spin-only theory B
(`g21 = 2 g20`, ρ dominance, ε = -1). Its reachable O(p⁴) ratio interval is `g20 ≤ g21 ≤ 2 g20`
(ρ = g21/g20 ∈ [1, 2]), i.e. `-3 ≤ L3/L2 ≤ -2` and `-1 ≤ ℓ1/ℓ2 ≤ -1/2`; it is exactly the half of
AR's linear wedge `0 ≤ g21 ≤ 2 g20` in which odd spins outweigh even spins at moment 2. -/

/-- The mixture `a·A + b·B` (a, b ≥ 0) of a hidden-zero and an odd-only theory has `g20 ≤ g21 ≤ 2
  g20`. -/
theorem family_interval (a b gA gB : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hA : 0 ≤ gA) (hB : 0 ≤ gB) :
    a * gA + b * gB ≤ a * gA + b * (2 * gB) ∧ a * gA + b * (2 * gB) ≤ 2 * (a * gA + b * gB) := by
  constructor <;> nlinarith [mul_nonneg ha hA, mul_nonneg hb hB]

/-- Every ratio `ρ ∈ [1, 2]` is reached by the family (normalised `g20 = 1`), with nonnegative
  weights. -/
theorem family_surj (gA gB ρ : ℝ) (hA : 0 < gA) (hB : 0 < gB) (h1 : 1 ≤ ρ) (h2 : ρ ≤ 2) :
    ∃ a b : ℝ, 0 ≤ a ∧ 0 ≤ b ∧ a * gA + b * gB = 1 ∧ a * gA + b * (2 * gB) = ρ := by
  refine ⟨(2 - ρ) / gA, (ρ - 1) / gB, div_nonneg (by linarith) hA.le,
      div_nonneg (by linarith) hB.le, ?_, ?_⟩
  · field_simp; ring
  · field_simp; ring

/-- Spectral form: for positive spectral weight, `g21 ≥ g20` (the family's lower edge) iff the
odd spins outweigh the even ones, `Σ w (-1)^J / m⁴ ≤ 0` (ε ≤ 0). -/
theorem family_iff_odd_excess (S : Finset ι) (w x : ι → ℝ) (J : ι → ℕ) :
    g20 S w x ≤ g21 S w x J ↔ ∑ l ∈ S, w l * (-1) ^ J l * x l ^ 2 ≤ 0 := by
  unfold g21 g20 PositiveGeometryEmergentSpaceTime.Hankel.moment
  have : ∑ l ∈ S, w l * (1 - (-1) ^ J l) * x l ^ 2
      = ∑ l ∈ S, w l * x l ^ 2 - ∑ l ∈ S, w l * (-1) ^ J l * x l ^ 2 := by
    rw [← Finset.sum_sub_distrib]; exact Finset.sum_congr rfl fun l _ => by ring
  rw [this]; constructor <;> intro h <;> linarith

/-- R_fam ⊂ R_full: the family's interval lies inside AR's linear wedge. -/
theorem family_sub_full (g20 g21 : ℝ) (h0 : 0 ≤ g20) (h1 : g20 ≤ g21) (h2 : g21 ≤ 2 * g20) :
    0 ≤ g21 ∧ g21 ≤ 2 * g20 := ⟨by linarith, h2⟩

/-- SU(3) form of R_fam (large-N map, `2L1 = L2`, `L2 > 0`): `g20 ≤ g21 ≤ 2 g20` with
`g20 = 2(L3 + 4L2)`, `g21 = 4 L2` iff `-3 L2 ≤ L3 ≤ -2 L2`. -/
theorem family_su3 (L2 L3 : ℝ) :
    (2 * (L3 + 4 * L2) ≤ 4 * L2 ∧ 4 * L2 ≤ 2 * (2 * (L3 + 4 * L2))) ↔ (-3 * L2 ≤ L3 ∧ L3 ≤ -2 * L2) := by
  constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> linarith

/-- SU(2) form of R_fam: `g20 = (2ℓ1 + 3ℓ2)/2`, `g21 = ℓ2`: iff `-ℓ2 ≤ ℓ1 ≤ -ℓ2/2`. -/
theorem family_su2 (l1 l2 : ℝ) :
    ((2 * l1 + 3 * l2) / 2 ≤ l2 ∧ l2 ≤ 2 * ((2 * l1 + 3 * l2) / 2)) ↔ (-l2 ≤ l1 ∧ 2 * l1 ≤ -l2) := by
  constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> linarith

/-- ε-parametrisation: ρ = 1 - ε and `L3/L2 = 2/(1-ε) - 4` interpolate -2 (ε = 0) and -3 (ε = -1). -/
theorem family_eps_endpoints : (2 / (1 - 0 : ℝ) - 4 = -2) ∧ (2 / (1 - (-1)) - 4 : ℝ) = -3 := by
  constructor <;> norm_num

/-- Gap ⇒ normalised bound: if all masses are ≥ M (`0 ≤ x ≤ c = 1/M²`) and weights are positive,
the second moment is ≤ `c` times the first (`g̃2 ≤ 1` in AR's normalisation). -/
theorem moment_two_le_gap (S : Finset ι) (w x : ι → ℝ) (c : ℝ) (hw : ∀ l ∈ S, 0 ≤ w l)
    (hx0 : ∀ l ∈ S, 0 ≤ x l) (hxc : ∀ l ∈ S, x l ≤ c) :
    PositiveGeometryEmergentSpaceTime.Hankel.moment S w x 2 ≤ c * PositiveGeometryEmergentSpaceTime.Hankel.moment S w x 1 := by
  unfold PositiveGeometryEmergentSpaceTime.Hankel.moment
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum fun l hl => ?_
  have := mul_le_mul_of_nonneg_left (hxc l hl) (mul_nonneg (hw l hl) (hx0 l hl))
  nlinarith [this]

/-! ### Data facts (exact ℚ on the quoted rounded numbers; pulls compared via squares)

`σ_r² = r²((σ3/L3)² + (σ2/L2)²)`. "Outside at > 2σ" is `gap² > 4σ²`; with the 30 % large-N_c band
`σ_N = 0.3|r|`, "inside 2σ" is `gap² < 4(σ² + σ_N²)`. -/

/-- D1 (BE14 NNLO preferred): r = -307/81 is outside R_full (hence R_fam) by more than 2σ_exp. -/
theorem d1_outside_2sigma :
    (-3 - (-307 / 81 : ℚ)) ^ 2 > 4 * ((307 / 81) ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2)) := by norm_num

/-- D1 with the 30 % band is within 2σ of R_full (and of R_fam's ρ-edge). -/
theorem d1_inside_with_band :
    (-3 - (-307 / 81 : ℚ)) ^ 2 < 4 * ((307 / 81) ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2) + (3 / 10 * (307 / 81)) ^ 2) := by
  norm_num

/-- D1 with a band of only 7 % already suffices (threshold f* ≈ 0.065). -/
theorem d1_inside_with_7pct :
    (-3 - (-307 / 81 : ℚ)) ^ 2 < 4 * ((307 / 81) ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2) + (7 / 100 * (307 / 81)) ^ 2) := by
  norm_num

/-- D1 linear check: Δ_L = 3L2 + L3 = -0.64 with σ² = 0.2² + 9·0.04²; outside `Δ_L ≥ 0` by > 2σ. -/
theorem d1_deltaL_outside : (3 * (81 / 100) + (-307 / 100) : ℚ) < 0 ∧
    (3 * (81 / 100) + (-307 / 100) : ℚ) ^ 2 > 4 * ((20 / 100) ^ 2 + 9 * (4 / 100) ^ 2) := by norm_num

/-- The 30 % band on r = -307/81 (σ_N ≈ 1.14) is wider than the whole family interval [-3, -2]. -/
theorem band_wider_than_family : (3 / 10 * (307 / 81) : ℚ) > (-2) - (-3) := by norm_num

/-- D2 (BE14 p⁴ fit, NLO): r = -3.8/1.6 = -19/8 lies inside R_fam = [-3, -2]. -/
theorem d2_inside_family : (-3 : ℚ) ≤ (-38 / 10) / (16 / 10) ∧ (-38 / 10) / (16 / 10) ≤ (-2 : ℚ) := by norm_num

/-- D3 (BE14 NNLO free fit): r = -280/59 is outside R_full by more than 2σ_exp. -/
theorem d3_outside_2sigma : (-280 / 59 : ℚ) < -3 ∧
    (-3 - (-280 / 59 : ℚ)) ^ 2 > 4 * ((280 / 59) ^ 2 * ((20 / 280) ^ 2 + (4 / 59) ^ 2)) := by norm_num

/-- D8 (large-N_c lattice, FPRS quote): Δ_L = -0.12(22) is within 1σ of the edge Δ_L = 0
(the ρ-dominance edge ε = -1 of the family and of R_full). -/
theorem d8_within_1sigma : (12 / 100 : ℚ) ^ 2 ≤ (22 / 100) ^ 2 := by norm_num

/-- SU(2), CGL 2001 at μ = 0.77 GeV: the large-N bound ℓ1 + ℓ2 ≥ 0 reads ℓ̄1 + 2ℓ̄2 ≥ 3 ln(μ²/Mπ²)
(AR eq. 79). With ℓ̄1 + 2ℓ̄2 = 8.2, σ² = 0.6² + 4·0.1² = 0.4, the gap exceeds 2σ. -/
theorem cgl_outside_2sigma :
    (3 * Real.log ((77000 / 13957 : ℝ) ^ 2) - 82 / 10) ^ 2 > 4 * (4 / 10) ∧
      82 / 10 < 3 * Real.log ((77000 / 13957 : ℝ) ^ 2) := by
  have hl2 := Real.log_two_gt_d9
  have h19 : 1 - (19 / 10 : ℝ)⁻¹ ≤ Real.log (19 / 10) := Real.one_sub_inv_le_log_of_pos (by norm_num)
  have hmono : Real.log (2 ^ 4 * (19 / 10) : ℝ) ≤ Real.log ((77000 / 13957 : ℝ) ^ 2) :=
    Real.log_le_log (by norm_num) (by norm_num)
  have hsplit : Real.log (2 ^ 4 * (19 / 10) : ℝ) = 4 * Real.log 2 + Real.log (19 / 10) := by
    rw [Real.log_mul (by norm_num) (by norm_num), Real.log_pow]; push_cast; ring
  have h19' : (9 / 19 : ℝ) ≤ Real.log (19 / 10) := by norm_num at h19; exact h19
  set L := Real.log ((77000 / 13957 : ℝ) ^ 2) with hL
  have key : (15 / 10 : ℝ) ≤ 3 * L - 82 / 10 := by linarith
  constructor <;> nlinarith

/-- Correction to the ladder-review caveat: under M3's own rule (±30 % band on the *theory* value,
PASS if the band meets I₁ = [r̂ - σ, r̂ + σ]), the ρ-dominance edge r = -3 has band [-3.9, -2.1], which meets I₁
for D1 because `r̂ + σ ≥ -3.9` (`σ² > (3.9 + r̂)²`). So the vector edge would *pass* the M3 comparison. -/
theorem vmd_edge_passes_m3_rule :
    (39 / 10 + (-307 / 81 : ℚ)) ^ 2 < (307 / 81) ^ 2 * ((20 / 307) ^ 2 + (4 / 81) ^ 2) ∧
      (-307 / 81 : ℚ) < -39 / 10 + 1 := by norm_num

end PositiveGeometryEmergentSpaceTime.LECRatio
