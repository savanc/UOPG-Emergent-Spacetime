/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
/-! COS-1 gate (2026-10-13, AutoResearch): tree Tr φ³ wavefunction coefficients of conformally
coupled scalars are strictly positive on the physical region, so no hidden zero lies there. -/
namespace PositiveGeometryEmergentSpaceTime.COS1
/-- Two-site (4-pt exchange) wavefunction coefficient. -/
noncomputable def psi2 (x1 x2 y : ℝ) : ℝ := 1 / ((x1 + x2) * (x1 + y) * (x2 + y))
/-- The two-site wavefunction coefficient `psi2` is strictly positive when all three energies are
  positive. -/
theorem psi2_pos {x1 x2 y : ℝ} (h1 : 0 < x1) (h2 : 0 < x2) (hy : 0 < y) : 0 < psi2 x1 x2 y := by
  unfold psi2; positivity
/-- Recursion check: (x1+x2) ψ₂ = ψ₁(x1+y) ψ₁(x2+y). -/
theorem psi2_recursion {x1 x2 y : ℝ} (h1 : 0 < x1) (h2 : 0 < x2) (hy : 0 < y) :
    (x1 + x2) * psi2 x1 x2 y = 1 / (x1 + y) * (1 / (x2 + y)) := by
  unfold psi2; field_simp
/-- Ordered 4-pt: s + t channel sum is positive, hence never zero, on the physical region. -/
theorem four_pt_no_zero {a b c d ys yt : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (hs : 0 < ys) (ht : 0 < yt) : psi2 a b ys + psi2 c d yt ≠ 0 :=
  (add_pos (psi2_pos ha hb hs) (psi2_pos hc hd ht)).ne'
/-- Any finite sum of positive channel terms is nonzero (n-point ordered sums). -/
theorem sum_pos_ne_zero {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (f : ι → ℝ)
    (h : ∀ i ∈ s, 0 < f i) : ∑ i ∈ s, f i ≠ 0 :=
  (Finset.sum_pos h hs).ne'
end PositiveGeometryEmergentSpaceTime.COS1
