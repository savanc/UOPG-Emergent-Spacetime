/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Klein
import PositiveGeometryEmergentSpaceTime.Spinor

/-!
# M1b: the Hermitian ↔ split slice bridge

Pre-registration: `prereg/M1b-slice-bridge-2026-10-11.md`. Review: `reviews/M1b-result-2026-10-11.md`.

* **B1 (no-go).** Hermitian (real Minkowski) X never has a positive chart Plücker vector (`herm_not_pos`). The
  projective form, for any τ-fixed Plücker vector, is `tau_fixed_not_pos`. The nonnegative closure meets Minkowski
  space in exactly two null half-rays (`herm_nonneg_iff`).
* **B2 (continuation).** In the family `X_w = [[t+z, x − w i],[x + w i, t − z]]`, `det` is the holomorphic η
  (`det_Xw`). Positivity forces `w ∈ iℝ` with `Im w < −|x|` (`Xw_pos_forces_split`), so only the split end of a
  Wick rotation is positive. An explicit split point lies in Gr⁺ (`split_point_pos`).
* **B3 (kinematics).** In real (1,3) kinematics: same-sign null vectors have p·q ≥ 0 (`null_dot_nonneg`).
  At n = 4, s, t > 0 is impossible (`no_pos4`). At n = 5, neither all five planar invariants < 0 (`no_euclid5`)
  nor all > 0 (`no_pos5`) is possible. Explicit exact Euclidean points exist at n = 4 and n = 6 (`cfg4_*`,
  `cfg6_*`), and both n = 5 patterns exist in (2,2) (`splitPos_*`, `splitNeg_*`).
-/

open Matrix Complex

namespace PositiveGeometryEmergentSpaceTime.SliceBridge

/-- `z` is a (strictly) positive real. -/
def posR (z : ℂ) : Prop := 0 < z.re ∧ z.im = 0
/-- `z` is a nonnegative real. -/
def nnR (z : ℂ) : Prop := 0 ≤ z.re ∧ z.im = 0

/-! ## B1 -/

/-- **B1, chart form.** If `X` is Hermitian, then for no rescaling `λ` are `λ p₀₁`, `λ p₀₂`, `λ p₁₃` all positive
reals. In particular no Hermitian `X` lies in Gr⁺(2,4) through the chart. This holds pointwise, not just for open
sets. -/
theorem herm_not_pos (X : Matrix (Fin 2) (Fin 2) ℂ) (hX : X.IsHermitian) (l : ℂ) :
    ¬ (posR (l * pl (chart X) 0 1) ∧ posR (l * pl (chart X) 0 2) ∧ posR (l * pl (chart X) 1 3)) := by
  obtain ⟨h01, h02, -, -, h13, -⟩ := chart_pl X
  rw [h01, h02, h13]
  rintro ⟨⟨a1, a2⟩, ⟨b1, b2⟩, ⟨c1, c2⟩⟩
  have hx : X 0 1 = star (X 1 0) := (hX.apply 0 1).symm
  rw [hx] at c1 c2
  simp only [mul_one] at a1 a2
  simp only [mul_re, mul_im, neg_re, neg_im, star_def, conj_re, conj_im, a2] at b1 b2 c1 c2
  nlinarith

/-- The antilinear involution on Plücker space `(p01,p02,p03,p12,p13,p23)` (indices 0..5) whose fixed points
in the chart are exactly the Hermitian X. -/
def tau (p : Fin 6 → ℂ) : Fin 6 → ℂ :=
  ![star (p 0), -star (p 4), star (p 2), star (p 3), -star (p 1), star (p 5)]

/-- For Hermitian `X`, the Plücker vector of the chart `[1 | X]` is fixed by `tau`. -/
theorem tau_chart_herm (X : Matrix (Fin 2) (Fin 2) ℂ) (hX : X.IsHermitian) :
    tau ![pl (chart X) 0 1, pl (chart X) 0 2, pl (chart X) 0 3, pl (chart X) 1 2, pl (chart X) 1 3,
      pl (chart X) 2 3] =
    ![pl (chart X) 0 1, pl (chart X) 0 2, pl (chart X) 0 3, pl (chart X) 1 2, pl (chart X) 1 3,
      pl (chart X) 2 3] := by
  obtain ⟨h01, h02, h03, h12, h13, h23⟩ := chart_pl X
  have e : ∀ i j, star (X i j) = X j i := fun i j => hX.apply j i
  ext k; fin_cases k <;>
    simp [tau, h01, h02, h03, h12, h13, h23, e, det_fin_two, star_sub, star_mul', mul_comm]

/-- A positive real complex number equals its conjugate. -/
lemma real_of_posR {z : ℂ} (h : posR z) : star z = z := by
  apply Complex.ext <;> simp [h.2]

/-- **B1, projective form.** If `τ p = μ • p` for some `μ` (a τ-fixed point of projective space; this covers
Hermitian points at infinity too), then no rescaling makes `p₀₁, p₀₂, p₁₃` all positive reals. -/
theorem tau_fixed_not_pos (p : Fin 6 → ℂ) (μ : ℂ) (hτ : tau p = μ • p) (l : ℂ) :
    ¬ (posR (l * p 0) ∧ posR (l * p 1) ∧ posR (l * p 4)) := by
  rintro ⟨ha, hb, hc⟩
  have h0 : star (p 0) = μ * p 0 := by simpa [tau] using congrFun hτ 0
  have h1 : -star (p 4) = μ * p 1 := by simpa [tau] using congrFun hτ 1
  have ra := real_of_posR ha; have rc := real_of_posR hc
  rw [star_mul', h0] at ra
  rw [star_mul'] at rc
  have hp0 : p 0 ≠ 0 := by rintro h; simp [h, posR] at ha
  have key : star l * μ = l := by
    apply mul_right_cancel₀ hp0; linear_combination ra
  have hfin : -(l * p 1) = l * p 4 := by linear_combination (star l) * h1 + (p 1) * key + rc
  have hb1 := hb.1; have hc1 := hc.1
  have := congrArg Complex.re hfin
  rw [Complex.neg_re] at this; linarith

/-- **B1, closure.** A Hermitian `X = σ(t,x,y,z)` has all chart Plücker coordinates nonnegative reals iff
`x = y = 0` and either `t = z ≤ 0` or `t = −z ≥ 0`: two null half-rays in the (t, z) plane, a set of dimension 1. -/
theorem herm_nonneg_iff (t x y z : ℝ) :
    (nnR (pl (chart (sigma ![t, x, y, z])) 0 2) ∧ nnR (pl (chart (sigma ![t, x, y, z])) 0 3) ∧
      nnR (pl (chart (sigma ![t, x, y, z])) 1 2) ∧ nnR (pl (chart (sigma ![t, x, y, z])) 1 3) ∧
      nnR (pl (chart (sigma ![t, x, y, z])) 2 3)) ↔
    x = 0 ∧ y = 0 ∧ ((t = z ∧ t ≤ 0) ∨ (t = -z ∧ 0 ≤ t)) := by
  obtain ⟨-, h02, h03, h12, h13, h23⟩ := chart_pl (sigma ![t, x, y, z])
  rw [h02, h03, h12, h13, h23, det_fin_two]
  simp only [nnR, sigma, of_apply, cons_val', cons_val_zero, cons_val_one, empty_val',
      cons_val_fin_one,
    head_cons, cons_val_two, cons_val_three, tail_cons]
  simp only [add_re, add_im, sub_re, sub_im, mul_re, mul_im, neg_re, neg_im, ofReal_re, ofReal_im,
      I_re, I_im]
  constructor
  · rintro ⟨⟨a1, a2⟩, ⟨b1, -⟩, ⟨c1, -⟩, ⟨d1, d2⟩, ⟨e1, -⟩⟩
    have hy : y = 0 := by linarith
    have hx : x = 0 := by subst hy; linarith
    subst hx hy
    refine ⟨rfl, rfl, ?_⟩
    have hprod : (t + z) * (t - z) = 0 := by nlinarith
    rcases mul_eq_zero.mp hprod with h | h
    · right; constructor <;> linarith
    · left; constructor <;> linarith
  · rintro ⟨rfl, rfl, h⟩
    rcases h with ⟨rfl, ht⟩ | ⟨rfl, ht⟩ <;> refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_,
        ?_⟩⟩ <;>
      norm_num <;> nlinarith

/-- Corollary: those Hermitian points are null (det = η = 0): positivity touches Minkowski space
  only on light rays. -/
theorem herm_nonneg_null (t z : ℝ) (h : (t = z) ∨ (t = -z)) : minkowskiQuad ![t, 0, 0, z] = 0 := by
  rcases h with rfl | rfl <;> simp [minkowskiQuad]

/-! ## B2 -/

/-- The common complexification: `w` real gives Hermitian X (Minkowski), `w = i y'` gives a real
  matrix (split). -/
def Xw (t x z : ℝ) (w : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![((t + z : ℝ) : ℂ), (x : ℂ) - w * I; (x : ℂ) + w * I, ((t - z : ℝ) : ℂ)]

/-- `det` is the holomorphic η: `t² − x² − w² − z²`. It is (1,3) for real `w` and (2,2) for `w = i
  y'`. -/
theorem det_Xw (t x z : ℝ) (w : ℂ) : (Xw t x z w).det = (t : ℂ) ^ 2 - (x : ℂ) ^ 2 - w ^ 2 - (z : ℂ) ^ 2 := by
  rw [det_fin_two]; simp [Xw]; ring_nf; rw [I_sq]; ring

/-- For real `w = y`, `Xw t x z y = σ(t, x, y, z)` (the Hermitian/Minkowski slice). -/
theorem Xw_real_herm (t x z y : ℝ) : Xw t x z (y : ℂ) = sigma ![t, x, y, z] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Xw, sigma]

/-- For `w = i y'`, `det Xw = t² − x² + y'² − z²` (signature (2,2)). -/
theorem det_Xw_split (t x z y' : ℝ) : (Xw t x z ((y' : ℂ) * I)).det = ((t ^ 2 - x ^ 2 + y' ^ 2 - z ^ 2 : ℝ) : ℂ) := by
  rw [det_Xw]; push_cast; ring_nf; rw [I_sq]; ring

/-- **B2.** If the two off-diagonal Plücker coordinates of `[I | X_w]` are positive reals, then `w` is purely
imaginary with `Im w < x` and `Im w < −x`. So the Hermitian slice (`Im w = 0`, which includes the common (1,2)
slice `w = 0`) is excluded, and positivity is reached only on the split end of the rotation `w ↦ i w`. -/
theorem Xw_pos_forces_split (t x z : ℝ) (w : ℂ)
    (h : posR (pl (chart (Xw t x z w)) 0 2) ∧ posR (pl (chart (Xw t x z w)) 1 3)) :
    w.re = 0 ∧ w.im < x ∧ w.im < -x := by
  obtain ⟨-, h02, -, -, h13, -⟩ := chart_pl (Xw t x z w)
  rw [h02, h13] at h
  obtain ⟨⟨a1, a2⟩, ⟨b1, -⟩⟩ := h
  simp [Xw] at a1 a2 b1
  exact ⟨a2, by linarith, by linarith⟩

/-- On the Hermitian slice, `p₀₂` and `p₁₃` of the chart cannot both be positive reals. -/
theorem herm_slice_excluded (t x z y : ℝ) :
    ¬ (posR (pl (chart (Xw t x z (y : ℂ))) 0 2) ∧ posR (pl (chart (Xw t x z (y : ℂ))) 1 3)) := by
  intro h; have := Xw_pos_forces_split t x z _ h; simp at this; linarith [this.1, this.2]

/-- An explicit split point in Gr⁺: `(t, x, y', z) = (0, 0, −2, −1)`, i.e. `X = [[−1, −2],[2, 1]]`, with
det = t² − x² + y'² − z² = 3 > 0. All six chart Plücker coordinates are positive reals. -/
theorem split_point_pos :
    ∀ ij : Fin 4 × Fin 4, ij ∈ [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)] →
      posR (pl (chart (Xw 0 0 (-1) ((-2 : ℝ) * I))) ij.1 ij.2) := by
  intro ij hij
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hij
  rcases hij with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [pl_eq, chart, Xw, posR] <;> norm_num


/-! ### B1/B2 robustness under column orders and sign twists (prereg addendum)

Gr⁺ depends on the column order and on column signs. `scripts/m1b_orders.py` finds that 192 of the 384
(order, twist) choices contain Hermitian points, all with `y = 0`. The convention-free statement: *any* positivity
notion needs every minor to be a real multiple of one `λ`. Since `p₀₁ = 1`, `λ` is real, and then `p₀₂` real forces
`y = 0`. So positive Hermitian points lie in the hyperplane `y = 0` (the common (1,2) slice) and never fill an open
set of ℝ^{1,3}. -/

/-- Convention-free B1: if `λ p₀₁` and `λ p₀₂` are real with `λ ≠ 0`, the Hermitian point has `y =
  0`. -/
theorem herm_real_minors_y0 (t x y z : ℝ) (l : ℂ) (hl : l ≠ 0) (h1 : (l * pl (chart (sigma ![t, x,
    y, z])) 0 1).im = 0)
    (h2 : (l * pl (chart (sigma ![t, x, y, z])) 0 2).im = 0) : y = 0 := by
  obtain ⟨h01, h02, -⟩ := chart_pl (sigma ![t, x, y, z])
  rw [h01] at h1; rw [h02] at h2
  simp [sigma] at h1 h2
  have hre : l.re ≠ 0 := by
    intro h; apply hl; exact Complex.ext h h1
  rw [h1] at h2; simp at h2
  rcases h2 with h | h
  · exact absurd h hre
  · exact h

/-- Hence no open set: from any such point, moving off `y = 0` leaves the set. -/
theorem herm_real_minors_no_open (t x y z ε : ℝ) (hε : ε ≠ 0) (hy : y = 0) (l : ℂ) (hl : l ≠ 0)
    (h1 : (l * pl (chart (sigma ![t, x, y + ε, z])) 0 1).im = 0) :
    (l * pl (chart (sigma ![t, x, y + ε, z])) 0 2).im ≠ 0 := by
  intro h2; have := herm_real_minors_y0 t x (y + ε) z l hl h1 h2; subst hy; simp at this; exact hε this

/-- Convention-free B2: real `p₀₂` on the Wick family forces `Re w = 0` (the split slice). Its only contact with
the Hermitian slice is `w = 0`, the common (1,2) slice. -/
theorem Xw_real_forces_split (t x z : ℝ) (w : ℂ) (h : (pl (chart (Xw t x z w)) 0 2).im = 0) : w.re = 0 := by
  obtain ⟨-, h02, -⟩ := chart_pl (Xw t x z w); rw [h02] at h; simpa [Xw] using h

/-- The twist is real: with column 3 negated (order 0123), the spacelike point `(t,x,y,z) = (−2, 2, 0, 1)` on the
common slice has all six twisted minors positive. -/
theorem twisted_example :
    let P := chart (sigma ![-2, 2, 0, 1])
    0 < (pl P 0 1).re ∧ 0 < (pl P 0 2).re ∧ 0 < (-pl P 0 3).re ∧ 0 < (pl P 1 2).re ∧ 0 < (-pl P 1 3).re ∧
      0 < (-pl P 2 3).re ∧ (pl P 0 2).im = 0 ∧ (pl P 1 3).im = 0 := by
  simp [pl_eq, chart, sigma]; norm_num

/-! ## B3: real (1,3) kinematics (mostly minus) -/

/-- Minkowski product (mostly minus) on real 4-vectors.

Also known as: SliceBridge.mdot, Minkowski product p·η·q.
-/
def minkowskiDot (p q : Fin 4 → ℝ) : ℝ := p 0 * q 0 - p 1 * q 1 - p 2 * q 2 - p 3 * q 3
/-- `p` is null: `p · p = 0` for the Minkowski product. -/
def Null (p : Fin 4 → ℝ) : Prop := minkowskiDot p p = 0

/-- Same-sign (future or past) null vectors have nonnegative Minkowski product (Cauchy–Schwarz). -/
theorem null_dot_nonneg {p q : Fin 4 → ℝ} (hp : Null p) (hq : Null q) (hp0 : 0 ≤ p 0) (hq0 : 0 ≤ q 0) :
    0 ≤ minkowskiDot p q := by
  unfold Null minkowskiDot at *
  nlinarith [sq_nonneg (p 1 * q 2 - p 2 * q 1), sq_nonneg (p 1 * q 3 - p 3 * q 1),
      sq_nonneg (p 2 * q 3 - p 3 * q 2),
    mul_nonneg hp0 hq0, sq_nonneg (p 1 * q 1 + p 2 * q 2 + p 3 * q 3 - p 0 * q 0),
    sq_nonneg (p 1 * q 1 + p 2 * q 2 + p 3 * q 3 + p 0 * q 0)]

/-- A null real 4-vector with zero energy component is zero. -/
lemma null_zero_energy {p : Fin 4 → ℝ} (hp : Null p) (h : p 0 = 0) : p 1 = 0 ∧ p 2 = 0 ∧ p 3 = 0 := by
  unfold Null minkowskiDot at hp; rw [h] at hp
  refine ⟨?_, ?_, ?_⟩ <;> nlinarith [sq_nonneg (p 1), sq_nonneg (p 2), sq_nonneg (p 3)]

/-- A strictly negative product of null vectors forces strictly opposite energies. -/
theorem neg_dot_opposite {p q : Fin 4 → ℝ} (hp : Null p) (hq : Null q) (h : minkowskiDot p q < 0) :
    (0 < p 0 ∧ q 0 < 0) ∨ (p 0 < 0 ∧ 0 < q 0) := by
  have hn : ∀ v : Fin 4 → ℝ, Null v → Null (-v) := fun v hv => by unfold Null minkowskiDot at *; simp; linarith
  have e1 : minkowskiDot (-p) (-q) = minkowskiDot p q := by unfold minkowskiDot; simp only [Pi.neg_apply]; ring
  have e2 : minkowskiDot p (-q) = -minkowskiDot p q := by unfold minkowskiDot; simp only [Pi.neg_apply]; ring
  have e3 : minkowskiDot (-p) q = -minkowskiDot p q := by unfold minkowskiDot; simp only [Pi.neg_apply]; ring
  rcases lt_trichotomy (p 0) 0 with hp0 | hp0 | hp0 <;> rcases lt_trichotomy (q 0) 0 with hq0 | hq0 | hq0
  · have := null_dot_nonneg (hn p hp) (hn q hq) (by simp; linarith) (by simp; linarith); linarith
  · obtain ⟨a, b, c⟩ := null_zero_energy hq hq0; unfold minkowskiDot at h; rw [hq0, a, b,
      c] at h; simp at h
  · exact Or.inr ⟨hp0, hq0⟩
  · obtain ⟨a, b, c⟩ := null_zero_energy hp hp0; unfold minkowskiDot at h; rw [hp0, a, b,
      c] at h; simp at h
  · obtain ⟨a, b, c⟩ := null_zero_energy hp hp0; unfold minkowskiDot at h; rw [hp0, a, b,
      c] at h; simp at h
  · obtain ⟨a, b, c⟩ := null_zero_energy hp hp0; unfold minkowskiDot at h; rw [hp0, a, b,
      c] at h; simp at h
  · exact Or.inl ⟨hp0, hq0⟩
  · obtain ⟨a, b, c⟩ := null_zero_energy hq hq0; unfold minkowskiDot at h; rw [hq0, a, b,
      c] at h; simp at h
  · have := null_dot_nonneg hp hq hp0.le hq0.le; linarith

/-- A strictly positive product of null vectors forces strictly equal energy signs. -/
theorem pos_dot_same {p q : Fin 4 → ℝ} (hp : Null p) (hq : Null q) (h : 0 < minkowskiDot p q) :
    (0 < p 0 ∧ 0 < q 0) ∨ (p 0 < 0 ∧ q 0 < 0) := by
  have hnq : Null (-q) := by unfold Null minkowskiDot at *; simp; linarith
  have e2 : minkowskiDot p (-q) = -minkowskiDot p q := by unfold minkowskiDot; simp only [Pi.neg_apply]; ring
  rcases neg_dot_opposite hp hnq (by rw [e2]; linarith) with ⟨a, b⟩ | ⟨a, b⟩
  · left; simp at b; exact ⟨a, by linarith⟩
  · right; simp at b; exact ⟨a, by linarith⟩

/-- For null `p, q`, the two-particle invariant is `(p+q)² = 2 p·q`. -/
theorem s_eq_two_dot {p q : Fin 4 → ℝ} (hp : Null p) (hq : Null q) : minkowskiDot (p + q) (p + q) = 2 * minkowskiDot p q := by
  unfold Null minkowskiDot at *; simp; linarith

/-- **B3, n = 5, Euclidean pattern.** For any five real null vectors (in cyclic order), the five adjacent products
cannot all be negative. An odd cycle cannot alternate energy signs. No momentum conservation is needed. -/
theorem no_euclid5 (p : Fin 5 → Fin 4 → ℝ) (hn : ∀ i, Null (p i))
    (h : ∀ i : Fin 5, minkowskiDot (p i) (p (i + 1)) < 0) : False := by
  have := fun i => neg_dot_opposite (hn i) (hn (i + 1)) (h i)
  have h0 := this 0; have h1 := this 1; have h2 := this 2; have h3 := this 3; have h4 := this 4
  simp only [show (0 : Fin 5) + 1 = 1 from rfl, show (1 : Fin 5) + 1 = 2 from rfl,
      show (2 : Fin 5) + 1 = 3 from rfl,
    show (3 : Fin 5) + 1 = 4 from rfl, show (4 : Fin 5) + 1 = 0 from rfl] at h0 h1 h2 h3 h4
  rcases h0 with ⟨a, b⟩ | ⟨a, b⟩ <;> rcases h1 with ⟨c, d⟩ | ⟨c, d⟩ <;> rcases h2 with ⟨e, f⟩ | ⟨e,
      f⟩ <;>
    rcases h3 with ⟨g, k⟩ | ⟨g, k⟩ <;> rcases h4 with ⟨m, o⟩ | ⟨m, o⟩ <;> linarith

/-- **B3, n = 5, positive pattern.** With momentum conservation, the five adjacent products cannot all be positive
(all energies would share a sign). -/
theorem no_pos5 (p : Fin 5 → Fin 4 → ℝ) (hn : ∀ i, Null (p i)) (hc : ∑ i, p i 0 = 0)
    (h : ∀ i : Fin 5, 0 < minkowskiDot (p i) (p (i + 1))) : False := by
  have := fun i => pos_dot_same (hn i) (hn (i + 1)) (h i)
  have h0 := this 0; have h1 := this 1; have h2 := this 2; have h3 := this 3
  simp only [show (0 : Fin 5) + 1 = 1 from rfl, show (1 : Fin 5) + 1 = 2 from rfl,
      show (2 : Fin 5) + 1 = 3 from rfl,
    show (3 : Fin 5) + 1 = 4 from rfl] at h0 h1 h2 h3
  simp [Fin.sum_univ_succ] at hc
  rcases h0 with ⟨a, b⟩ | ⟨a, b⟩ <;> rcases h1 with ⟨c, d⟩ | ⟨c, d⟩ <;> rcases h2 with ⟨e, f⟩ | ⟨e,
      f⟩ <;>
    rcases h3 with ⟨g, k⟩ | ⟨g, k⟩ <;> linarith

/-- At n = 5 the planar variables are the adjacent invariants: `X₁₄ = s₁₂₃ = s₄₅` by momentum
  conservation. -/
theorem planar5_eq (p : Fin 5 → Fin 4 → ℝ) (hc : p 0 + p 1 + p 2 + p 3 + p 4 = 0) :
    minkowskiDot (p 0 + p 1 + p 2) (p 0 + p 1 + p 2) = minkowskiDot (p 3 + p 4) (p 3 + p 4) := by
  have : p 0 + p 1 + p 2 = -(p 3 + p 4) := by rw [eq_neg_iff_add_eq_zero, ← hc]; abel
  rw [this]; unfold minkowskiDot; simp only [Pi.neg_apply, Pi.add_apply]; ring

/-- **B3, n = 4.** With momentum conservation, s = (p1+p2)² and t = (p2+p3)² cannot both be
  positive. -/
theorem no_pos4 (p : Fin 4 → Fin 4 → ℝ) (hn : ∀ i, Null (p i)) (hc : p 0 + p 1 + p 2 + p 3 = 0)
    (hs : 0 < minkowskiDot (p 0) (p 1)) (ht : 0 < minkowskiDot (p 1) (p 2)) : False := by
  have h3 : p 3 = -(p 0 + p 1 + p 2) := by rw [eq_neg_iff_add_eq_zero, ← hc]; abel
  have hsum : minkowskiDot (p 0) (p 1) + minkowskiDot (p 1) (p 2) + minkowskiDot (p 0) (p 2) = 0 := by
    have := hn 3; rw [h3] at this
    have a := hn 0; have b := hn 1; have c := hn 2
    unfold Null minkowskiDot at *; simp at this; nlinarith
  rcases pos_dot_same (hn 0) (hn 1) hs with ⟨a, b⟩ | ⟨a, b⟩ <;>
    rcases pos_dot_same (hn 1) (hn 2) ht with ⟨c, d⟩ | ⟨c, d⟩
  · have := null_dot_nonneg (hn 0) (hn 2) a.le d.le; linarith
  · linarith
  · linarith
  · have hn' : ∀ v : Fin 4 → ℝ, Null v → Null (-v) := fun v hv => by unfold Null minkowskiDot at *; simp; linarith
    have := null_dot_nonneg (hn' _ (hn 0)) (hn' _ (hn 2)) (by simp; linarith) (by simp; linarith)
    have e : minkowskiDot (-p 0) (-p 2) = minkowskiDot (p 0) (p 2) := by unfold minkowskiDot; simp only [Pi.neg_apply]; ring
    linarith

/-! ## B3: exact configurations (generated by `scripts/m1b_gen_lean.py`) -/

/-- Minkowski product (mostly minus) on rational 4-vectors. -/
def mdotQ (p q : Fin 4 → ℚ) : ℚ := p 0 * q 0 - p 1 * q 1 - p 2 * q 2 - p 3 * q 3
/-- 2×2 bracket `⟨ab⟩`. -/
def br2 (a b : Fin 2 → ℚ) : ℚ := a 0 * b 1 - a 1 * b 0

/-- In (2,2), `p = λ λ̃ᵀ` and `det(p_i + p_j) = ⟨ij⟩[ij]`. -/
theorem det_two_spinor (a b c d : Fin 2 → ℚ) :
    (a 0 * b 0 + c 0 * d 0) * (a 1 * b 1 + c 1 * d 1) - (a 0 * b 1 + c 0 * d 1) * (a 1 * b 0 + c 1 * d 0)
      = br2 a c * br2 b d := by unfold br2; ring

/-- cfg4: real (1,3) null momenta (mostly minus, all incoming), exact. -/

def cfg4 : Fin 4 → Fin 4 → ℚ := ![![(5 : ℚ), (0 : ℚ), (0 : ℚ), (5 : ℚ)], ![(-5 : ℚ), (-3 : ℚ),
    (0 : ℚ), (-4 : ℚ)], ![(5 : ℚ), (0 : ℚ), (0 : ℚ), (-5 : ℚ)], ![(-5 : ℚ), (3 : ℚ), (0 : ℚ),
    (4 : ℚ)]]

/-- Each momentum of `cfg4` is null. -/
theorem cfg4_null : ∀ i, mdotQ (cfg4 i) (cfg4 i) = 0 := by
  intro i; fin_cases i <;> norm_num [cfg4, mdotQ]

/-- The momenta of `cfg4` sum to zero. -/
theorem cfg4_cons : ∀ μ, ∑ i, cfg4 i μ = 0 := by
  intro μ; fin_cases μ <;> norm_num [cfg4, Fin.sum_univ_succ]

/-- Two planar invariants of `cfg4` are negative (`(p₀ + p₁)² < 0`, `(p₁ + p₂)² < 0`). -/
theorem cfg4_euclidean :
    mdotQ (cfg4 0 + cfg4 1) (cfg4 0 + cfg4 1) < 0 ∧
    mdotQ (cfg4 1 + cfg4 2) (cfg4 1 + cfg4 2) < 0 := by
  norm_num [cfg4, mdotQ]

/-- cfg6: real (1,3) null momenta (mostly minus, all incoming), exact. -/

def cfg6 : Fin 6 → Fin 4 → ℚ := ![![(5 : ℚ), (5 : ℚ), (0 : ℚ), (0 : ℚ)], ![(-5 : ℚ), (50 / 51 : ℚ),
    (50 / 51 : ℚ), (-245 / 51 : ℚ)], ![(3 : ℚ), (0 : ℚ), (0 : ℚ), (-3 : ℚ)], ![(-4 : ℚ),
    (-4 / 3 : ℚ), (-8 / 3 : ℚ), (-8 / 3 : ℚ)], ![(2036 / 295 : ℚ), (-4072 / 885 : ℚ),
    (2036 / 885 : ℚ), (4072 / 885 : ℚ)], ![(-1741 / 295 : ℚ), (-691 / 15045 : ℚ),
    (-9242 / 15045 : ℚ), (88306 / 15045 : ℚ)]]

/-- Each momentum of `cfg6` is null. -/
theorem cfg6_null : ∀ i, mdotQ (cfg6 i) (cfg6 i) = 0 := by
  intro i; fin_cases i <;> norm_num [cfg6, mdotQ]

/-- The momenta of `cfg6` sum to zero. -/
theorem cfg6_cons : ∀ μ, ∑ i, cfg6 i μ = 0 := by
  intro μ; fin_cases μ <;> norm_num [cfg6, Fin.sum_univ_succ]

/-- The listed planar invariants `(pᵢ + pᵢ₊₁)²` of `cfg6` are all negative. -/
theorem cfg6_euclidean :
    mdotQ (cfg6 0 + cfg6 1) (cfg6 0 + cfg6 1) < 0 ∧
    mdotQ (cfg6 1 + cfg6 2) (cfg6 1 + cfg6 2) < 0 ∧
    mdotQ (cfg6 2 + cfg6 3) (cfg6 2 + cfg6 3) < 0 ∧
    mdotQ (cfg6 3 + cfg6 4) (cfg6 3 + cfg6 4) < 0 ∧
    mdotQ (cfg6 4 + cfg6 5) (cfg6 4 + cfg6 5) < 0 ∧
    mdotQ (cfg6 5 + cfg6 0) (cfg6 5 + cfg6 0) < 0 ∧
    mdotQ (cfg6 0 + cfg6 1 + cfg6 2) (cfg6 0 + cfg6 1 + cfg6 2) < 0 ∧
    mdotQ (cfg6 1 + cfg6 2 + cfg6 3) (cfg6 1 + cfg6 2 + cfg6 3) < 0 ∧
    mdotQ (cfg6 2 + cfg6 3 + cfg6 4) (cfg6 2 + cfg6 3 + cfg6 4) < 0 := by
  norm_num [cfg6, mdotQ]

/-- splitPos: real (2,2) spinors, n = 5, `p_i = λ_i λ̃_iᵀ`, exact. -/

def splitPosL : Fin 5 → Fin 2 → ℚ := ![![(1 : ℚ), (-3 : ℚ)], ![(-1 : ℚ), (-3 : ℚ)], ![(-4 : ℚ),
    (4 : ℚ)], ![(-1 : ℚ), (-1 : ℚ)], ![(4 : ℚ), (3 : ℚ)]]

/-- Second spinors `λ̃ᵢ` of the five-point (2,2) configuration `splitPos`. -/
def splitPosT : Fin 5 → Fin 2 → ℚ := ![![(-19 / 3 : ℚ), (7 / 2 : ℚ)], ![(14 / 3 : ℚ), (-5 / 2 : ℚ)],
    ![(-2 : ℚ), (1 : ℚ)], ![(-3 : ℚ), (-2 : ℚ)], ![(0 : ℚ), (-1 : ℚ)]]

/-- Momentum conservation for the (2,2) spinor data: `Σᵢ λᵢ λ̃ᵢᵀ = 0` (entrywise). -/
theorem splitPos_cons : ∀ a b : Fin 2, ∑ i, splitPosL i a * splitPosT i b = 0 := by
  intro a b; fin_cases a <;> fin_cases b <;> norm_num [splitPosL, splitPosT, Fin.sum_univ_succ]

/-- All listed adjacent products `⟨i i+1⟩[i i+1]` are positive for `splitPos`. -/
theorem splitPos_planar :
    0 < br2 (splitPosL 0) (splitPosL 1) * br2 (splitPosT 0) (splitPosT 1) ∧
    0 < br2 (splitPosL 1) (splitPosL 2) * br2 (splitPosT 1) (splitPosT 2) ∧
    0 < br2 (splitPosL 2) (splitPosL 3) * br2 (splitPosT 2) (splitPosT 3) ∧
    0 < br2 (splitPosL 3) (splitPosL 4) * br2 (splitPosT 3) (splitPosT 4) ∧
    0 < br2 (splitPosL 4) (splitPosL 0) * br2 (splitPosT 4) (splitPosT 0) := by
  norm_num [splitPosL, splitPosT, br2]

/-- splitNeg: real (2,2) spinors, n = 5, `p_i = λ_i λ̃_iᵀ`, exact. -/

def splitNegL : Fin 5 → Fin 2 → ℚ := ![![(-2 : ℚ), (1 : ℚ)], ![(0 : ℚ), (-3 : ℚ)], ![(-2 : ℚ),
    (1 : ℚ)], ![(1 : ℚ), (-4 : ℚ)], ![(-3 : ℚ), (4 : ℚ)]]

/-- Second spinors `λ̃ᵢ` of the five-point (2,2) configuration `splitNeg`. -/
def splitNegT : Fin 5 → Fin 2 → ℚ := ![![(4 : ℚ), (-11 / 2 : ℚ)], ![(-7 / 3 : ℚ), (5 / 2 : ℚ)],
    ![(-3 : ℚ), (1 : ℚ)], ![(2 : ℚ), (0 : ℚ)], ![(0 : ℚ), (3 : ℚ)]]

/-- Momentum conservation for the (2,2) spinor data `splitNeg`. -/
theorem splitNeg_cons : ∀ a b : Fin 2, ∑ i, splitNegL i a * splitNegT i b = 0 := by
  intro a b; fin_cases a <;> fin_cases b <;> norm_num [splitNegL, splitNegT, Fin.sum_univ_succ]

/-- All listed adjacent products `⟨i i+1⟩[i i+1]` are negative for `splitNeg`. -/
theorem splitNeg_planar :
    0 > br2 (splitNegL 0) (splitNegL 1) * br2 (splitNegT 0) (splitNegT 1) ∧
    0 > br2 (splitNegL 1) (splitNegL 2) * br2 (splitNegT 1) (splitNegT 2) ∧
    0 > br2 (splitNegL 2) (splitNegL 3) * br2 (splitNegT 2) (splitNegT 3) ∧
    0 > br2 (splitNegL 3) (splitNegL 4) * br2 (splitNegT 3) (splitNegT 4) ∧
    0 > br2 (splitNegL 4) (splitNegL 0) * br2 (splitNegT 4) (splitNegT 0) := by
  norm_num [splitNegL, splitNegT, br2]

end PositiveGeometryEmergentSpaceTime.SliceBridge
