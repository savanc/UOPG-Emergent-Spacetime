/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — SURF-1′: sanity theorems and blind-vs-original comparison.
Original: `PositiveGeometryEmergentSpaceTime.Surf1` (lean/PositiveGeometryEmergentSpaceTime/Surf1/*.lean). Blind: `PositiveGeometryEmergentSpaceTime.Alignment.Surf1Blind`.
Nothing in the original is edited.
-/
import PositiveGeometryEmergentSpaceTime.Surf1
import PositiveGeometryEmergentSpaceTime.Alignment.Surf1Kernel.Theta
import PositiveGeometryEmergentSpaceTime.Alignment.Surf1Kernel.K4
import PositiveGeometryEmergentSpaceTime.Alignment.Surf1Kernel.Dsq

namespace PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
open PositiveGeometryEmergentSpaceTime.Surf1

/-! ## 1. Blind enumerator reproduces the original's certified Laurent data (kernel) -/

/-- Laurent evaluation agrees: blind `evalW theta = ev thetaL` for `N ≠ 0`. -/
theorem evalW_theta (N : ℚ) (hN : N ≠ 0) : Surf1Blind.evalW Surf1Blind.theta N = ev thetaL N := by
  unfold Surf1Blind.evalW
  rw [blind_theta]
  simp [ev, thetaL, Surf1Blind.theta, List.zipIdx, zpow_neg, zpow_natCast]
  field_simp
  ring

theorem evalW_K4 (N : ℚ) (hN : N ≠ 0) : Surf1Blind.evalW Surf1Blind.K4 N = ev tetraL N := by
  unfold Surf1Blind.evalW
  rw [blind_K4]
  simp [ev, tetraL, Surf1Blind.K4, List.zipIdx, zpow_neg, zpow_natCast]
  field_simp
  ring

theorem evalW_dsq (N : ℚ) (hN : N ≠ 0) : Surf1Blind.evalW Surf1Blind.dsq N = ev ttUL N := by
  unfold Surf1Blind.evalW
  rw [blind_dsq]
  simp [ev, ttUL, Surf1Blind.dsq, List.zipIdx, zpow_neg, zpow_natCast]
  field_simp
  ring

/-- Blind K_tri equals the original K_tri for N ≥ 3. -/
theorem Ktri_eq (N : ℚ) (h : 3 ≤ N) : Surf1Blind.Ktri N = K (W1 tetra) (W1 theta) N := by
  have hN : N ≠ 0 := by intro h0; rw [h0] at h; norm_num at h
  rw [tetra_c1, theta_c1]
  simp only [Surf1Blind.Ktri, K]
  rw [evalW_K4 N hN, evalW_theta N hN]; rfl

/-- Blind claim, triangle half, PROVED via the original's sign facts: K_tri(3) = −1. -/
theorem blind_Ktri_three : Surf1Blind.Ktri 3 = -1 := by
  rw [Ktri_eq 3 (by norm_num), tetra_c1, theta_c1]; exact K_tri_three

/-- The blind closed-form claim holds (pure ℚ algebra). -/
theorem blind_closed_form : Surf1Blind.ClaimClosedForm := by
  intro N hN
  rcases Nat.eq_or_lt_of_le hN with h | h
  · left; subst h; norm_num
  · right
    have h4 : (4 : ℚ) ≤ N := by exact_mod_cast h
    have a : 0 < (N : ℚ) ^ 2 - 10 := by nlinarith
    have b : 0 < (N : ℚ) * ((N : ℚ) ^ 2 - 4) := by
      have : 0 < (N : ℚ) ^ 2 - 4 := by nlinarith
      positivity
    exact div_neg_of_neg_of_pos (by linarith) b

/-- Original closed form ⇔ blind closed form of the box ratio on the original's data. -/
theorem original_box_matches_prose (N : ℚ) (h : 3 ≤ N) :
    K (W1 boxU) (W1 ttU) N = -8 * (N ^ 2 - 10) / (N * (N ^ 2 - 4)) := by
  rw [boxU_c1, ttU_c1]; exact K_boxU_closed N h

/-! ## 2. Sanity: non-vacuity and planted wrong cases -/

/-- Neither disjunct of `no_sign_coherent_N` is redundant: at N = 3 the box is positive
(so the triangle is needed) … -/
theorem box_pos_at_3 : 0 < K (W1 boxU) (W1 ttU) 3 := by
  rw [boxU_c1, ttU_c1]; show 0 < K boxUL ttUL 3; rw [K_boxU_three]; norm_num

/-- … and at every N ≥ 4 the triangle is positive (so the box is needed). -/
theorem tri_pos_ge_4 (N : ℚ) (h : 4 ≤ N) : 0 < K (W1 tetra) (W1 theta) N := by
  rw [tetra_c1, theta_c1]; show 0 < K tetraL thetaL N; rw [K_tri_closed N (by linarith)]
  have : 0 < N ^ 2 - 12 := by nlinarith
  positivity

/-- Planted wrong reading: "the triangle alone is negative for all N ≥ 3" is FALSE. -/
theorem planted_tri_alone_false : ¬ ∀ N : ℕ, 3 ≤ N → K (W1 tetra) (W1 theta) N < 0 := by
  intro h
  have := h 4 (by norm_num)
  have := tri_pos_ge_4 4 (by norm_num)
  push_cast at *
  linarith

/-- Planted wrong reading: "the crossed box alone is negative for all N ≥ 3" is FALSE. -/
theorem planted_box_alone_false : ¬ ∀ N : ℕ, 3 ≤ N → K (W1 boxU) (W1 ttU) N < 0 := by
  intro h
  have := h 3 (by norm_num)
  have := box_pos_at_3
  push_cast at *
  linarith

/-- Textbook value (P1, U(N) → SU(N)): the single propagator loop is N² − 1 = dim SU(N). -/
theorem single_loop_is_dim : ∀ N : ℚ, N ≠ 0 → ev (W1 single) N = N ^ 2 - 1 := by
  intro N _; rw [single_c1]; simp [ev]; ring

/-- Textbook value (Haber 1912.13302 as quoted in the prereg, not refetched): K_tri = (N²−12)/N,
so at SU(3) the d-symmetric triangle interference is −1, while SU(4) gives +1. -/
theorem Ktri_values : K (W1 tetra) (W1 theta) 3 = -1 ∧ K (W1 tetra) (W1 theta) 4 = 1 := by
  refine ⟨by rw [tetra_c1, theta_c1]; exact K_tri_three, ?_⟩
  rw [tetra_c1, theta_c1]; show K tetraL thetaL 4 = 1; rw [K_tri_closed 4 (by norm_num)]; norm_num

/-! ## 4. K₃,₃ (crossed box), conditional

The blind K₃,₃ coefficient vector below was obtained by interpreter `#eval` only
(SIMULATED, ~37 s); a kernel `decide` on it exceeds the 12 GB box limit even per orientation
chunk. Conditional on that vector, the full blind enumerated claim follows from the original. -/

/-- The `#eval` value of `Surf1Blind.coeffs Surf1Blind.K33` (index j ↔ N^(j−9)). -/
def K33vec : List ℤ := [0,0,0,0,0,0,1280,0,-1728,0,480,0,-32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

theorem evalW_K33_of (h : Surf1Blind.coeffs Surf1Blind.K33 = K33vec) (N : ℚ) (hN : N ≠ 0) :
    Surf1Blind.evalW Surf1Blind.K33 N = ev boxUL N := by
  unfold Surf1Blind.evalW
  rw [h]
  simp [ev, boxUL, K33vec, Surf1Blind.K33, List.zipIdx, zpow_neg, zpow_natCast]
  field_simp
  ring

theorem KboxX_eq_of (h : Surf1Blind.coeffs Surf1Blind.K33 = K33vec) (N : ℚ) (h3 : 3 ≤ N) :
    Surf1Blind.KboxX N = K (W1 boxU) (W1 ttU) N := by
  have hN : N ≠ 0 := by intro h0; rw [h0] at h3; norm_num at h3
  rw [boxU_c1, ttU_c1]
  simp only [Surf1Blind.KboxX, K]
  rw [evalW_K33_of h N hN, evalW_dsq N hN]; rfl

/-- Blind derivation-level claim, conditional only on the (SIMULATED) K₃,₃ vector. -/
theorem claimEnumerated_of_K33 (h : Surf1Blind.coeffs Surf1Blind.K33 = K33vec) :
    Surf1Blind.ClaimEnumerated := by
  refine ⟨blind_Ktri_three, fun N hN => ?_, fun N hN => ?_⟩
  · rw [KboxX_eq_of h N (by exact_mod_cast (show 3 ≤ N by omega))]
    exact K_boxU_neg_enum N (by exact_mod_cast hN)
  · rw [Ktri_eq N (by exact_mod_cast hN), KboxX_eq_of h N (by exact_mod_cast hN)]
    exact no_sign_coherent_N N hN

end PositiveGeometryEmergentSpaceTime.Alignment.Surf1Sanity
