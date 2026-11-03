/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.MassiveZero
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Mr2Blind

/-!
# ALIGNMENT BLIND-3 (2026-11-03) — Compare + sanity: MR-2 (massive hidden zero ⇒ A(P) = 0)

Blind prereg: e6e1666 (pushed before `PositiveGeometryEmergentSpaceTime.MassiveZero` was opened).

VERDICTS:
* `dress`: **DIFFERENT definition, tied**. The original uses the six-term SU(2) trace sum
  `2(f s t + f s u − f u t + f u s − f t u + f t s)`; the blind uses three terms `f s t + f s u − f t u`.
  Exactly: orig `dress f = 2·(blind f + blind fᵀ)` (`dress_tie`); for symmetric f, orig = 4·blind.
* `dress_zero_at_P` vs blind `dress_zero_P_nosym`: **BLIND-STRONGER**. The original's `hsym`
  hypothesis is not needed: `orig_dress_zero_nosym` proves the original conclusion without it.
* `poly_zero_iff`: **DIFFERENT generality, core EQUIV**. Original: units M² = 1, with an extra LO
  term κ(x+y−2). Blind: any M² ≠ 0, no κ. Each implies the other at M² = 1 (below).
* `dress_poly_at_P`: **EQUIV** after the ×4 tie (`dress_poly_tie`).
* `lo_zero_at_P` (`(1:ℝ) − 1 = 0`), `su2_poly_at_P`, `g1_poly_vanishes`, `g1_poly_at_11`,
  `f1_poly_at_1`: **NAME-ONLY** (closed numerals; no amplitude in the statement). The ties below
  show what they stand for: `lo_tie` (the LO ordered amplitude dresses to 8κ(s − 1), so vanishes at P)
  and `G1`/`F1` evaluations. The BCEGS one-loop polynomials themselves stay CITED.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR2

/-! ## Compare -/

theorem dress_tie (f : ℝ → ℝ → ℝ) (s t u : ℝ) :
    MassiveZero.dress f s t u = 2 * (Mr2Blind.dress f s t u + Mr2Blind.dress (fun x y => f y x) s t u) := by
  unfold MassiveZero.dress Mr2Blind.dress; ring

theorem dress_tie_symm (f : ℝ → ℝ → ℝ) (hsym : ∀ x y, f x y = f y x) (s t u : ℝ) :
    MassiveZero.dress f s t u = 4 * Mr2Blind.dress f s t u := by
  rw [dress_tie]; unfold Mr2Blind.dress; simp only [hsym t s, hsym u s, hsym u t]; ring

/-- The original conclusion holds without the symmetry hypothesis (via the blind). -/
theorem orig_dress_zero_nosym (f : ℝ → ℝ → ℝ) (hz : ∀ x y, x + y = 2 → f x y = 0) :
    MassiveZero.dress f 1 1 2 = 0 := by
  rw [dress_tie]
  have h1 := Mr2Blind.dress_zero_P_nosym f 1 (fun s t h => hz s t (by linarith))
  have h2 := Mr2Blind.dress_zero_P_nosym (fun x y => f y x) 1 (fun s t h => hz t s (by linarith))
  norm_num at h1 h2 ⊢; rw [h1, h2]; ring

theorem orig_dress_zero_of_blind (f : ℝ → ℝ → ℝ) (_hsym : ∀ x y, f x y = f y x)
    (hz : ∀ x y, x + y = 2 → f x y = 0) : MassiveZero.dress f 1 1 2 = 0 :=
  orig_dress_zero_nosym f hz

theorem fpoly_tie (κ a1 a2 a3 a4 x y : ℝ) :
    MassiveZero.fpoly κ a1 a2 a3 a4 x y = κ * (x + y - 2) + Mr2Blind.fpoly a1 a2 a3 a4 1 x y := by
  unfold MassiveZero.fpoly Mr2Blind.fpoly; ring

theorem orig_poly_zero_iff_of_blind (κ a1 a2 a3 a4 : ℝ) :
    (∀ x y, x + y = 2 → MassiveZero.fpoly κ a1 a2 a3 a4 x y = 0) ↔ (a2 = 2 * a1 ∧ 4 * a1 + 2 * a3 + a4 = 0) := by
  rw [← Mr2Blind.poly_zero_iff a1 a2 a3 a4 1 one_ne_zero]
  constructor
  · intro h s t hst; have := h s t (by linarith); rw [fpoly_tie] at this
    have e : s + t - 2 = 0 := by linarith
    rw [e] at this; simpa using this
  · intro h x y hxy; rw [fpoly_tie, h x y (by linarith)]
    have e : x + y - 2 = 0 := by linarith
    rw [e]; ring

theorem blind_poly_zero_iff_of_orig (a1 a2 a3 a4 : ℝ) :
    (∀ s t, s + t = 2 * 1 → Mr2Blind.fpoly a1 a2 a3 a4 1 s t = 0) ↔ (a2 = 2 * a1 ∧ 4 * a1 + 2 * a3 + a4 = 0) := by
  rw [← MassiveZero.poly_zero_iff 0 a1 a2 a3 a4]
  constructor
  · intro h x y hxy; rw [fpoly_tie, h x y (by linarith)]; ring
  · intro h s t hst; have := h s t (by linarith); rw [fpoly_tie] at this; simpa using this

theorem dress_poly_tie (κ a1 a2 a3 a4 : ℝ) :
    MassiveZero.dress (MassiveZero.fpoly κ a1 a2 a3 a4) 1 1 2
      = 4 * Mr2Blind.dress (Mr2Blind.fpoly a1 a2 a3 a4 1) 1 1 (2 * 1) := by
  rw [MassiveZero.dress_poly_at_P, Mr2Blind.dress_poly_P]; ring

/-- What `lo_zero_at_P` stands for: the LO ordered amplitude κ(x+y−2) dresses to 8κ(s − 1). -/
theorem lo_tie (κ s t u : ℝ) : MassiveZero.dress (fun x y => κ * (x + y - 2)) s t u = 8 * κ * (s - 1) := by
  unfold MassiveZero.dress; ring

theorem lo_tie_at_P (κ : ℝ) : MassiveZero.dress (fun x y => κ * (x + y - 2)) 1 1 2 = 0 := by
  rw [lo_tie]; ring

/-- Named one-loop polynomials behind the NAME-ONLY numerals (as written in the MR-2 record). -/
def G1 (s t : ℝ) : ℝ := 14 - 4 * s - 10 * t + s * t + 2 * t ^ 2
def F1 (s : ℝ) : ℝ := s ^ 2 - 1

theorem g1_tie : G1 1 2 = 0 ∧ G1 1 1 = 3 ∧ F1 1 = 0 := by
  unfold G1 F1; norm_num

/-! ## Sanity -/

/-- Non-vacuity: `poly_zero_iff`'s right side holds for nonzero coefficients, and the hidden-zero
hypothesis of `dress_zero_at_P` is met by a nonzero symmetric f. -/
theorem nonvacuous :
    (∃ a1 a2 a3 a4 : ℝ, a1 ≠ 0 ∧ a2 = 2 * a1 ∧ 4 * a1 + 2 * a3 + a4 = 0) ∧
    (∃ f : ℝ → ℝ → ℝ, (∀ x y, f x y = f y x) ∧ (∀ x y, x + y = 2 → f x y = 0) ∧ f 0 0 ≠ 0) :=
  ⟨⟨1, 2, -2, 0, by norm_num, by norm_num, by norm_num⟩,
   ⟨fun x y => x + y - 2, fun x y => by ring, fun x y h => by linarith, by norm_num⟩⟩

/-- Planted wrong case: with a2 ≠ 2a1 the polynomial does not vanish on the line, and A(P) ≠ 0. -/
theorem planted_wrong :
    ¬ (∀ x y, x + y = 2 → MassiveZero.fpoly 0 1 0 (-2) 0 x y = 0) ∧
    MassiveZero.dress (MassiveZero.fpoly 0 1 0 (-2) 0) 1 1 2 ≠ 0 := by
  constructor
  · rw [MassiveZero.poly_zero_iff]; norm_num
  · rw [MassiveZero.dress_poly_at_P]; norm_num

/-- Planted wrong case for the dressing: a symmetric f WITHOUT the zero can have A(P) ≠ 0. -/
theorem planted_no_zero : MassiveZero.dress (fun _ _ => (1 : ℝ)) 1 1 2 ≠ 0 := by
  unfold MassiveZero.dress; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR2
