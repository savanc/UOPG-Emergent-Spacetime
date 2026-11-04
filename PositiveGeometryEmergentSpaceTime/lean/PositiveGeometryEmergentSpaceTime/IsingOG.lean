/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.PositroidCells

/-!
# H-T3: planar Ising networks → the positive orthogonal Grassmannian OG≥0(n, 2n)

Prereg: `prereg/H-T3-ising-OG-2026-10-11.md`. Galashin–Pylyavskyy (GP, arXiv:1807.03282) map M ↦ M̃ (eq. 2.4).

* n = 2 (one edge, σ = ⟨σ₁σ₂⟩): the six minors, the OG relations Δ_I = Δ_{Iᶜ}, positivity, the inverse formula
  (GP eq. 2.7), and the three cells via the Grassmann-necklace machinery of `PositroidCells` (reused).
* The carrier variable: σ = tanh J ⇒ Δ₂₃/Δ₁₂ = 1/sinh 2J. For GP's plabic weights s = sech 2J, c = tanh 2J we have
  s² + c² = 1 and c/s = sinh 2J. So HW's ABJM 4-pt measure dθ/(sc) = dlog tan θ equals dlog sinh 2J.
* n = 3 (Y network, m_ij = t_i t_j): the ten OG relations hold identically.
No `sorry`, no `native_decide`, no custom axioms.
-/

namespace PositiveGeometryEmergentSpaceTime.IsingOG
open PositiveGeometryEmergentSpaceTime.PositroidCells

/-! ## n = 2 -/

/-- GP's `M̃` for `M = [[1, σ], [σ, 1]]` (GP eq. 2.6). -/
def gp2 (σ : ℝ) : Matrix (Fin 2) (Fin 4) ℝ := !![1, 1, σ, -σ; -σ, σ, 1, 1]

/-- 2×2 minor on columns `i, j`. -/
def m2 (A : Matrix (Fin 2) (Fin 4) ℝ) (i j : Fin 4) : ℝ := A 0 i * A 1 j - A 0 j * A 1 i

/-- Explicit 2×2 minors of the one-parameter matrix `gp2 σ`: `Δ₀₁ = Δ₂₃ = 2σ`, `Δ₀₃ = Δ₁₂ = 1 − σ²`,
  `Δ₀₂ = 1 + σ²`, … (exact polynomial identities). -/
theorem gp2_minors (σ : ℝ) :
    m2 (gp2 σ) 0 1 = 2 * σ ∧ m2 (gp2 σ) 2 3 = 2 * σ ∧
    m2 (gp2 σ) 0 3 = 1 - σ ^ 2 ∧ m2 (gp2 σ) 1 2 = 1 - σ ^ 2 ∧
    m2 (gp2 σ) 0 2 = 1 + σ ^ 2 ∧ m2 (gp2 σ) 1 3 = 1 + σ ^ 2 := by
  simp only [m2, gp2, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.head_cons,
    Matrix.tail_cons]
  refine ⟨by ring, by ring, by ring, by ring, by ring, by ring⟩

/-- The OG relations `Δ_I = Δ_{[4]∖I}` hold for every real σ (GP Def. 2.1, Ex. 2.5). -/
theorem gp2_orthogonal (σ : ℝ) :
    m2 (gp2 σ) 0 1 = m2 (gp2 σ) 2 3 ∧ m2 (gp2 σ) 0 2 = m2 (gp2 σ) 1 3 ∧ m2 (gp2 σ) 0 3 = m2 (gp2 σ) 1 2 := by
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := gp2_minors σ
  exact ⟨by rw [h1, h2], by rw [h5, h6], by rw [h3, h4]⟩

/-- Positivity: for `0 < σ < 1` all six minors are strictly positive (top cell of OG≥0(2,4)). -/
theorem gp2_pos {σ : ℝ} (h0 : 0 < σ) (h1 : σ < 1) :
    0 < m2 (gp2 σ) 0 1 ∧ 0 < m2 (gp2 σ) 2 3 ∧ 0 < m2 (gp2 σ) 0 3 ∧ 0 < m2 (gp2 σ) 1 2 ∧
    0 < m2 (gp2 σ) 0 2 ∧ 0 < m2 (gp2 σ) 1 3 := by
  obtain ⟨e1, e2, e3, e4, e5, e6⟩ := gp2_minors σ
  have hs : σ ^ 2 < 1 := by nlinarith
  rw [e1, e2, e3, e4, e5, e6]
  refine ⟨by linarith, by linarith, by linarith, by linarith, by positivity, by positivity⟩

/-- GP eq. 2.7: σ is recovered from the minors. -/
theorem gp2_inverse (σ : ℝ) : m2 (gp2 σ) 0 1 / (m2 (gp2 σ) 0 2 + m2 (gp2 σ) 0 3) = σ := by
  obtain ⟨e1, -, e3, -, e5, -⟩ := gp2_minors σ
  rw [e1, e3, e5]; field_simp; ring

/-- The three cells of OG≥0(2,4), via `PositroidCells.fperm` (reused):
* top (0 < σ < 1, all minors ≠ 0): f = [3,4,5,6], τ = (13)(24), one crossing (dim 1);
* σ = 0 (Δ₁₂ = Δ₃₄ = 0): τ = (12)(34);
* σ = 1 (Δ₁₄ = Δ₂₃ = 0): τ = (14)(23)  (GP Ex. 2.5). -/
theorem gp2_cells :
    (List.range 4).map (fperm 4 (fun _ _ => true)) = [3, 4, 5, 6] ∧ crossings [3, 4, 1, 2] = 1 ∧
    (List.range 4).map (fperm 4 (fun i j => !((i == 0 && j == 1) || (i == 2 && j == 3)))) = [2, 5,
        4, 7] ∧
    (List.range 4).map (fperm 4 (fun i j => !((i == 0 && j == 3) || (i == 1 && j == 2)))) = [4, 3,
        6, 5] ∧
    crossings [2, 1, 4, 3] = 0 ∧ crossings [4, 3, 2, 1] = 0 := by decide

/-! ## The carrier variable sinh 2J -/

/-- With σ = tanh J (one Ising edge), `Δ₂₃/Δ₁₂ = (1 − σ²)/(2σ) = 1/sinh 2J`. -/
theorem ratio_eq_inv_sinh {J : ℝ} (hJ : 0 < J) :
    m2 (gp2 (Real.tanh J)) 1 2 / m2 (gp2 (Real.tanh J)) 0 1 = 1 / Real.sinh (2 * J) := by
  obtain ⟨e1, -, -, e4, -, -⟩ := gp2_minors (Real.tanh J)
  rw [e4, e1, Real.tanh_eq_sinh_div_cosh, Real.sinh_two_mul]
  have hc : 0 < Real.cosh J := Real.cosh_pos J
  have hs : 0 < Real.sinh J := Real.sinh_pos_iff.mpr hJ
  have hid : Real.cosh J ^ 2 - Real.sinh J ^ 2 = 1 := Real.cosh_sq_sub_sinh_sq J
  field_simp
  nlinarith [hid]

/-- GP's medial weights `s = sech 2J`, `c = tanh 2J` (GP eq. 5.1) lie on the unit circle (HW's vertex angle θ with
`c = sin θ`, `s = cos θ`), and `c/s = sinh 2J`; hence `dlog tan θ = dlog (c/s) = dlog sinh 2J`. -/
theorem medial_weights (J : ℝ) :
    (1 / Real.cosh (2 * J)) ^ 2 + Real.tanh (2 * J) ^ 2 = 1 ∧
    Real.tanh (2 * J) / (1 / Real.cosh (2 * J)) = Real.sinh (2 * J) := by
  have hc : 0 < Real.cosh (2 * J) := Real.cosh_pos _
  have hid : Real.cosh (2 * J) ^ 2 - Real.sinh (2 * J) ^ 2 = 1 := Real.cosh_sq_sub_sinh_sq _
  rw [Real.tanh_eq_sinh_div_cosh]
  constructor
  · field_simp; linarith
  · field_simp

/-- Kramers–Wannier covariance of the carrier: if `sinh 2J* = 1/sinh 2J` (GP eq. 3.4), the carrier variable is
inverted, so `dlog sinh 2J* = − dlog sinh 2J`. -/
theorem kw_inverts {a b : ℝ} (ha : a ≠ 0) (h : b = 1 / a) : Real.log |b| = - Real.log |a| := by
  rw [h, abs_div, abs_one, Real.log_div one_ne_zero (abs_ne_zero.mpr ha), Real.log_one, zero_sub]

/-! ## n = 3: the Y network -/

/-- GP's `M̃` (3×6) for the Y network with `m_ij = t_i t_j` (`t = tanh L`; star with centre summed
  out). -/
def gpY (t₁ t₂ t₃ : ℝ) : Matrix (Fin 3) (Fin 6) ℝ :=
  !![1, 1, t₁ * t₂, -(t₁ * t₂), -(t₁ * t₃), t₁ * t₃;
     -(t₁ * t₂), t₁ * t₂, 1, 1, t₂ * t₃, -(t₂ * t₃);
     t₁ * t₃, -(t₁ * t₃), -(t₂ * t₃), t₂ * t₃, 1, 1]

/-- 3×3 minor on columns `a, b, c` (Laplace expansion along row 0). -/
def m3 (A : Matrix (Fin 3) (Fin 6) ℝ) (a b c : Fin 6) : ℝ :=
  A 0 a * (A 1 b * A 2 c - A 1 c * A 2 b) - A 0 b * (A 1 a * A 2 c - A 1 c * A 2 a) +
    A 0 c * (A 1 a * A 2 b - A 1 b * A 2 a)

/-- The ten OG relations `Δ_I = Δ_{[6]∖I}` hold identically for the Y network (GP Cor. 5.6,
  instance). -/
theorem gpY_orthogonal (t₁ t₂ t₃ : ℝ) :
    m3 (gpY t₁ t₂ t₃) 0 1 2 = m3 (gpY t₁ t₂ t₃) 3 4 5 ∧ m3 (gpY t₁ t₂ t₃) 0 1 3 = m3 (gpY t₁ t₂ t₃) 2 4 5 ∧
    m3 (gpY t₁ t₂ t₃) 0 1 4 = m3 (gpY t₁ t₂ t₃) 2 3 5 ∧ m3 (gpY t₁ t₂ t₃) 0 1 5 = m3 (gpY t₁ t₂ t₃) 2 3 4 ∧
    m3 (gpY t₁ t₂ t₃) 0 2 3 = m3 (gpY t₁ t₂ t₃) 1 4 5 ∧ m3 (gpY t₁ t₂ t₃) 0 2 4 = m3 (gpY t₁ t₂ t₃) 1 3 5 ∧
    m3 (gpY t₁ t₂ t₃) 0 2 5 = m3 (gpY t₁ t₂ t₃) 1 3 4 ∧ m3 (gpY t₁ t₂ t₃) 0 3 4 = m3 (gpY t₁ t₂ t₃) 1 2 5 ∧
    m3 (gpY t₁ t₂ t₃) 0 3 5 = m3 (gpY t₁ t₂ t₃) 1 2 4 ∧ m3 (gpY t₁ t₂ t₃) 0 4 5 = m3 (gpY t₁ t₂ t₃) 1 2 3 := by
  simp [m3, gpY]
  refine ⟨by ring, by ring, by ring, by ring, by ring, by ring, by ring, by ring, by ring, by ring⟩

/-- Positivity at an exact rational Y point (t = 1/2, 1/3, 1/4): all twenty minors are > 0, so the point lies in
OG>0(3,6), the top cell (τ = (14)(25)(36), three crossings = three edges; see `PositroidCells.top_cell`). -/
theorem gpY_pos_sample :
    let A := gpY (1/2) (1/3) (1/4)
    0 < m3 A 0 1 2 ∧ 0 < m3 A 0 1 3 ∧ 0 < m3 A 0 1 4 ∧ 0 < m3 A 0 1 5 ∧ 0 < m3 A 0 2 3 ∧
    0 < m3 A 0 2 4 ∧ 0 < m3 A 0 2 5 ∧ 0 < m3 A 0 3 4 ∧ 0 < m3 A 0 3 5 ∧ 0 < m3 A 0 4 5 ∧
    0 < m3 A 1 2 3 ∧ 0 < m3 A 1 2 4 ∧ 0 < m3 A 1 2 5 ∧ 0 < m3 A 1 3 4 ∧ 0 < m3 A 1 3 5 ∧
    0 < m3 A 1 4 5 ∧ 0 < m3 A 2 3 4 ∧ 0 < m3 A 2 3 5 ∧ 0 < m3 A 2 4 5 ∧ 0 < m3 A 3 4 5 := by
  simp [m3, gpY]
  norm_num

end PositiveGeometryEmergentSpaceTime.IsingOG
