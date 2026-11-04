/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PILOT (2026-10-31) — HG-DIM-1 mean curvature: sanity theorems and
blind-vs-original comparison. Original: `PositiveGeometryEmergentSpaceTime.HgDim1Mean`, `PositiveGeometryEmergentSpaceTime.HgDim1Mean9`.
Blind: `PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Blind`. The original is not edited.
-/
import PositiveGeometryEmergentSpaceTime.HgDim1Mean9
import PositiveGeometryEmergentSpaceTime.Alignment.HgKernel.N5to7
import PositiveGeometryEmergentSpaceTime.Alignment.HgKernel.N8
import PositiveGeometryEmergentSpaceTime.Alignment.HgKernel.N9a
import PositiveGeometryEmergentSpaceTime.Alignment.HgKernel.N9b
import PositiveGeometryEmergentSpaceTime.Alignment.HgKernel.N9c

namespace PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Sanity

open PositiveGeometryEmergentSpaceTime

/-! ## 1. Kernel facts: see `PositiveGeometryEmergentSpaceTime.Alignment.HgKernel.*` (len_n, alllen_n, sumP_n,
same_set_n, same_p_n for n = 5..9). -/

/-! ## 2. Generic algebra: mean of (2 − p)/c over pairs -/

theorem sum_inner (T : List (ℕ × ℕ)) (f : ℕ × ℕ → ℕ) (c : ℚ) :
    (T.map fun d => ((2 : ℚ) - f d) / c).sum = (2 * T.length - ((T.map f).sum : ℕ)) / c := by
  induction T with
  | nil => simp
  | cons x T ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons, ih]; push_cast; ring

theorem sum_outer (L : List (List (ℕ × ℕ))) (g : List (ℕ × ℕ) → ℕ × ℕ → ℕ) (c : ℚ) (m : ℕ)
    (hL : ∀ T ∈ L, T.length = m) :
    (L.map fun T => (T.map fun d => ((2 : ℚ) - g T d) / c).sum).sum
      = (2 * L.length * m - ((L.map fun T => (T.map (g T)).sum).sum : ℕ)) / c := by
  induction L with
  | nil => simp
  | cons T L ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    rw [sum_inner, ih (fun T' h => hL T' (List.mem_cons_of_mem _ h)), hL T List.mem_cons_self]
    push_cast; ring

/-- Mean over the blind enumeration under the per-edge hypothesis, in terms of Σp. -/
theorem mean_of_formula (n : ℕ) (κ : List (ℕ × ℕ) → ℕ × ℕ → ℚ)
    (hκ : ∀ T ∈ HgDim1Blind.tris n, ∀ d ∈ T, κ T d = (2 - (HgDim1Blind.pval n T d : ℚ)) / (n - 2))
    (hlen : ∀ T ∈ HgDim1Blind.tris n, T.length = n - 3) :
    ((HgDim1Blind.tris n).map fun T => (T.map (κ T)).sum).sum
      = (2 * (HgDim1Blind.tris n).length * (n - 3 : ℕ) - (HgDim1Blind.sumP n : ℚ)) / (n - 2) := by
  have hc : ((HgDim1Blind.tris n).map fun T => (T.map (κ T)).sum) =
      ((HgDim1Blind.tris n).map fun T =>
        (T.map fun d => ((2 : ℚ) - HgDim1Blind.pval n T d) / (n - 2)).sum) := by
    apply List.map_congr_left
    intro T hT
    congr 1
    exact List.map_congr_left (fun d hd => hκ T hT d hd)
  rw [hc, sum_outer _ (fun T d => HgDim1Blind.pval n T d) _ (n - 3) hlen]
  simp [HgDim1Blind.sumP]

/-! ## 3. Blind claims, proved -/

theorem claim_sumP : HgDim1Blind.ClaimSumP := by
  obtain ⟨-, c2, c3, c4, c5, c6, c7⟩ := HgDim1Mean.catalan_vals
  intro n hn
  simp only [Finset.mem_insert, Finset.mem_singleton] at hn
  rcases hn with rfl | rfl | rfl | rfl | rfl
  · rw [sumP_5, c3, c2]; norm_num
  · rw [sumP_6, c4, c3]; norm_num
  · rw [sumP_7, c5, c4]; norm_num
  · rw [sumP_8, c6, c5]; norm_num
  · rw [sumP_9, c7, c6]; norm_num

theorem claim_mean_conditional : HgDim1Blind.ClaimMeanConditional := by
  intro n hn κ hκ
  simp only [Finset.mem_insert, Finset.mem_singleton] at hn
  rcases hn with rfl | rfl | rfl | rfl | rfl
  · rw [mean_of_formula 5 κ hκ alllen_5, len_5, sumP_5]; norm_num
  · rw [mean_of_formula 6 κ hκ alllen_6, len_6, sumP_6]; norm_num
  · rw [mean_of_formula 7 κ hκ alllen_7, len_7, sumP_7]; norm_num
  · rw [mean_of_formula 8 κ hκ alllen_8, len_8, sumP_8]; norm_num
  · rw [mean_of_formula 9 κ hκ alllen_9, len_9, sumP_9]; norm_num

/-- Non-vacuity of the conditional claim: the local formula itself satisfies the hypothesis,
which gives the unconditional `ClaimMeanLocal`. -/
theorem claim_mean_local : HgDim1Blind.ClaimMeanLocal := by
  intro n hn
  have h := claim_mean_conditional n hn (fun T d => (2 - (HgDim1Blind.pval n T d : ℚ)) / (n - 2))
    (fun _ _ _ _ => rfl)
  rw [← h, HgDim1Blind.meanKappaLocal, List.map_map]
  rfl

/-! ## 4. Comparison with the original statements -/

/-- Blind Σp = original closed-form `sumP (n − 4)` for n = 5..9. -/
theorem sumP_matches_original :
    (HgDim1Blind.sumP 5 : ℤ) = HgDim1Mean.sumP 1 ∧ (HgDim1Blind.sumP 6 : ℤ) = HgDim1Mean.sumP 2 ∧
    (HgDim1Blind.sumP 7 : ℤ) = HgDim1Mean.sumP 3 ∧ (HgDim1Blind.sumP 8 : ℤ) = HgDim1Mean.sumP 4 ∧
    (HgDim1Blind.sumP 9 : ℤ) = HgDim1Mean.sumP 5 := by
  obtain ⟨s1, s2, s3, s4, s5⟩ := HgDim1Mean.sumP_instances
  rw [sumP_5, sumP_6, sumP_7, sumP_8, sumP_9, s1, s2, s3, s4, s5]; norm_num

/-- The blind mean target and the original `mean_kappa_closed` target agree (n = m + 4). -/
theorem mean_targets_agree (m : ℕ) :
    (10 - ((m + 4 : ℕ) : ℚ)) / ((((m + 4 : ℕ) : ℚ) - 2) * (2 * ((m + 4 : ℕ) : ℚ) - 5))
      = (6 - (m : ℚ)) / (((m : ℚ) + 2) * (2 * m + 3)) := by
  push_cast; ring_nf

/-! ## 5. Sanity: known values, planted wrong cases, sign change -/

/-- Known value: the pentagon has 5 triangulations and every flip quadrilateral has exactly
one diagonal side (p = 1, so κ = 1/3 on the 5-cycle K_5). -/
theorem pentagon_p_one : (HgDim1Blind.tris 5).all (fun T => T.all (fun d => HgDim1Blind.pval 5 T d == 1)) = true := by
  decide +kernel

/-- Prose "negative edges exist exactly for n ≥ 7" at n = 6, 7: p ≤ 2 everywhere on K_6 … -/
theorem no_negative_6 : (HgDim1Blind.tris 6).all (fun T => T.all (fun d => HgDim1Blind.pval 6 T d ≤ 2)) = true := by
  decide +kernel

/-- … and some pair on K_7 has p = 3 (κ = −1/5, the prose minimum at n = 7). -/
theorem negative_7 : (HgDim1Blind.tris 7).any (fun T => T.any (fun d => HgDim1Blind.pval 7 T d == 3)) = true := by
  decide +kernel

/-- Planted wrong formula (2n − 6 instead of 2n − 5) is rejected at n = 5. -/
theorem planted_wrong_mean : HgDim1Blind.meanKappaLocal 5 ≠ (10 - 5) / ((5 - 2) * (2 * 5 - 6)) := by
  rw [claim_mean_local 5 (by simp)]; norm_num

/-- Prose "the mean changes sign at the decagon", from the original general closed form. -/
theorem sign_change (m : ℕ) :
    (0 < (6 - (m : ℚ)) / (((m : ℚ) + 2) * (2 * m + 3)) ↔ m < 6) ∧
    ((6 - (m : ℚ)) / (((m : ℚ) + 2) * (2 * m + 3)) = 0 ↔ m = 6) := by
  have hd : (0 : ℚ) < ((m : ℚ) + 2) * (2 * m + 3) := by positivity
  constructor
  · rw [div_pos_iff_of_pos_right hd]
    constructor <;> intro h
    · exact_mod_cast (show (m : ℚ) < 6 by linarith)
    · have : (m : ℚ) < 6 := by exact_mod_cast h
      linarith
  · rw [div_eq_zero_iff, or_iff_left hd.ne']
    constructor <;> intro h
    · exact_mod_cast (show (m : ℚ) = 6 by linarith)
    · subst h; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.HgDim1Sanity
