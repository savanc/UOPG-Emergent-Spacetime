/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Klein
import PositiveGeometryEmergentSpaceTime.Associahedron

/-!
# BRIDGE-PL-ASSOC (XD-1): Plücker → hypersimplex moment map → planar X (n = 4, 5)

Partial formalisation of CROSS-DOMAIN X1 / systems-review BRIDGE-PL-ASSOC
(arXiv:0708.3431, 1703.04541, 1711.09102). Real proofs only; **no sorry**; no new axioms.

**Proved**
* (a) Pairwise Plücker-square moment map lands in Δ(2,4) and Δ(2,5) (∑μ = 2, each μ ∈ [0,1]).
* (b) n = 4: Klein `plucker_rel` = planar three-channel identity on Plücker monomials
  `⟨01⟩⟨23⟩ + ⟨03⟩⟨12⟩ = ⟨02⟩⟨13⟩`.
* (c) n = 5: `pl5` minors; a Plücker relation on columns {0,1,2,3}; five planar monomials;
  the Assoc affine identity `X24 = X14 − X13 + c13` holds when those symbols are read as
  the monomials below (algebraic skeleton of the kinematic chart).

**Gap (not proved — documented)**
* Toric homeomorphism Gr₊(2,n) ≃→ Δ(2,n) (Birch / AHBL) and the positroid subdivision whose
  kinematic slice is the full ABHY associahedron; matching `Assoc.m5` to a pushforward form.

Credit 0. Moves no SM ledger line.
-/

open Matrix

namespace PositiveGeometryEmergentSpaceTime.BridgePLAssoc

/-! ## (a) Hypersimplex and moment map, n = 4 -/

/-- Hypersimplex Δ(2,4). -/
def hypersimplex24 (x : Fin 4 → ℝ) : Prop :=
  (∀ i, 0 ≤ x i ∧ x i ≤ 1) ∧ x 0 + x 1 + x 2 + x 3 = 2

/-- Pair-norm² of the six Plücker coordinates of a 2×4 matrix. -/
noncomputable def pairNorm4 (P : Matrix (Fin 2) (Fin 4) ℝ) : ℝ :=
  (pl P 0 1) ^ 2 + (pl P 0 2) ^ 2 + (pl P 0 3) ^ 2 +
    (pl P 1 2) ^ 2 + (pl P 1 3) ^ 2 + (pl P 2 3) ^ 2

/-- Moment-map coordinate μᵢ (torus weight on column i). -/
noncomputable def mu4 (P : Matrix (Fin 2) (Fin 4) ℝ) : Fin 4 → ℝ := fun
  | 0 => ((pl P 0 1) ^ 2 + (pl P 0 2) ^ 2 + (pl P 0 3) ^ 2) / pairNorm4 P
  | 1 => ((pl P 0 1) ^ 2 + (pl P 1 2) ^ 2 + (pl P 1 3) ^ 2) / pairNorm4 P
  | 2 => ((pl P 0 2) ^ 2 + (pl P 1 2) ^ 2 + (pl P 2 3) ^ 2) / pairNorm4 P
  | 3 => ((pl P 0 3) ^ 2 + (pl P 1 3) ^ 2 + (pl P 2 3) ^ 2) / pairNorm4 P

/-- The n = 4 Plücker-square moment map sums to 2 whenever the Plücker norm is nonzero (the
  hypersimplex Δ(2,4) level). -/
theorem mu4_sum (P : Matrix (Fin 2) (Fin 4) ℝ) (hN : pairNorm4 P ≠ 0) :
    mu4 P 0 + mu4 P 1 + mu4 P 2 + mu4 P 3 = 2 := by
  have hnums :
      ((pl P 0 1) ^ 2 + (pl P 0 2) ^ 2 + (pl P 0 3) ^ 2) +
        ((pl P 0 1) ^ 2 + (pl P 1 2) ^ 2 + (pl P 1 3) ^ 2) +
        ((pl P 0 2) ^ 2 + (pl P 1 2) ^ 2 + (pl P 2 3) ^ 2) +
        ((pl P 0 3) ^ 2 + (pl P 1 3) ^ 2 + (pl P 2 3) ^ 2) =
        pairNorm4 P * 2 := by
    simp only [pairNorm4]; ring
  simp only [mu4]
  field_simp [hN]
  exact hnums

/-- Each coordinate of the n = 4 Plücker-square moment map is ≥ 0 when the Plücker norm is positive. -/
theorem mu4_nonneg (P : Matrix (Fin 2) (Fin 4) ℝ) (hN : 0 < pairNorm4 P) (i : Fin 4) :
    0 ≤ mu4 P i := by
  fin_cases i <;> simp only [mu4] <;> positivity

/-- Each coordinate of the n = 4 Plücker-square moment map is ≤ 1 when the Plücker norm is positive. -/
theorem mu4_le_one (P : Matrix (Fin 2) (Fin 4) ℝ) (hN : 0 < pairNorm4 P) (i : Fin 4) :
    mu4 P i ≤ 1 := by
  fin_cases i <;>
    · simp only [mu4]
      refine (div_le_one hN).2 ?_
      simp only [pairNorm4]
      nlinarith [sq_nonneg (pl P 0 1), sq_nonneg (pl P 0 2), sq_nonneg (pl P 0 3),
        sq_nonneg (pl P 1 2), sq_nonneg (pl P 1 3), sq_nonneg (pl P 2 3)]

/-- **(a₄)** Moment map of any nonzero Plücker vector of a 2×4 matrix lands in Δ(2,4). -/
theorem moment_in_hypersimplex24 (P : Matrix (Fin 2) (Fin 4) ℝ) (hN : 0 < pairNorm4 P) :
    hypersimplex24 (mu4 P) := by
  refine ⟨fun i => ⟨mu4_nonneg P hN i, mu4_le_one P hN i⟩, ?_⟩
  simpa using mu4_sum P (ne_of_gt hN)

/-! ## (a₅) n = 5 -/

/-- Plücker minor on columns `i, j` of a 2×5 matrix. -/
def pl5 (P : Matrix (Fin 2) (Fin 5) ℝ) (i j : Fin 5) : ℝ :=
  (P.submatrix id ![i, j]).det

/-- Unfolded form of the 2×5 Plücker coordinate: `pl5 P i j = P₀ᵢ P₁ⱼ − P₀ⱼ P₁ᵢ`. -/
lemma pl5_eq (P : Matrix (Fin 2) (Fin 5) ℝ) (i j : Fin 5) :
    pl5 P i j = P 0 i * P 1 j - P 0 j * P 1 i := by
  simp [pl5, det_fin_two]

/-- One Plücker relation on columns {0,1,2,3} (same as Klein, via the 2×4 submatrix). -/
theorem pl5_rel_0123 (P : Matrix (Fin 2) (Fin 5) ℝ) :
    pl5 P 0 1 * pl5 P 2 3 - pl5 P 0 2 * pl5 P 1 3 + pl5 P 0 3 * pl5 P 1 2 = 0 := by
  simp only [pl5_eq]; ring

/-- The hypersimplex Δ(2,5): points of ℝ⁵ with every coordinate in `[0, 1]` and coordinate sum 2. -/
def hypersimplex25 (x : Fin 5 → ℝ) : Prop :=
  (∀ i, 0 ≤ x i ∧ x i ≤ 1) ∧ x 0 + x 1 + x 2 + x 3 + x 4 = 2

/-- Sum of the squares of the ten Plücker coordinates of a 2×5 matrix. -/
noncomputable def pairNorm5 (P : Matrix (Fin 2) (Fin 5) ℝ) : ℝ :=
  (pl5 P 0 1) ^ 2 + (pl5 P 0 2) ^ 2 + (pl5 P 0 3) ^ 2 + (pl5 P 0 4) ^ 2 +
    (pl5 P 1 2) ^ 2 + (pl5 P 1 3) ^ 2 + (pl5 P 1 4) ^ 2 +
    (pl5 P 2 3) ^ 2 + (pl5 P 2 4) ^ 2 + (pl5 P 3 4) ^ 2

/-- μᵢ for n = 5: sum of p² over the four pairs containing i, over ‖p‖². -/
noncomputable def mu5 (P : Matrix (Fin 2) (Fin 5) ℝ) : Fin 5 → ℝ := fun
  | 0 => ((pl5 P 0 1) ^ 2 + (pl5 P 0 2) ^ 2 + (pl5 P 0 3) ^ 2 + (pl5 P 0 4) ^ 2) / pairNorm5 P
  | 1 => ((pl5 P 0 1) ^ 2 + (pl5 P 1 2) ^ 2 + (pl5 P 1 3) ^ 2 + (pl5 P 1 4) ^ 2) / pairNorm5 P
  | 2 => ((pl5 P 0 2) ^ 2 + (pl5 P 1 2) ^ 2 + (pl5 P 2 3) ^ 2 + (pl5 P 2 4) ^ 2) / pairNorm5 P
  | 3 => ((pl5 P 0 3) ^ 2 + (pl5 P 1 3) ^ 2 + (pl5 P 2 3) ^ 2 + (pl5 P 3 4) ^ 2) / pairNorm5 P
  | 4 => ((pl5 P 0 4) ^ 2 + (pl5 P 1 4) ^ 2 + (pl5 P 2 4) ^ 2 + (pl5 P 3 4) ^ 2) / pairNorm5 P

/-- The n = 5 Plücker-square moment map sums to 2 whenever the Plücker norm is nonzero. -/
theorem mu5_sum (P : Matrix (Fin 2) (Fin 5) ℝ) (hN : pairNorm5 P ≠ 0) :
    mu5 P 0 + mu5 P 1 + mu5 P 2 + mu5 P 3 + mu5 P 4 = 2 := by
  have hnums :
      ((pl5 P 0 1) ^ 2 + (pl5 P 0 2) ^ 2 + (pl5 P 0 3) ^ 2 + (pl5 P 0 4) ^ 2) +
        ((pl5 P 0 1) ^ 2 + (pl5 P 1 2) ^ 2 + (pl5 P 1 3) ^ 2 + (pl5 P 1 4) ^ 2) +
        ((pl5 P 0 2) ^ 2 + (pl5 P 1 2) ^ 2 + (pl5 P 2 3) ^ 2 + (pl5 P 2 4) ^ 2) +
        ((pl5 P 0 3) ^ 2 + (pl5 P 1 3) ^ 2 + (pl5 P 2 3) ^ 2 + (pl5 P 3 4) ^ 2) +
        ((pl5 P 0 4) ^ 2 + (pl5 P 1 4) ^ 2 + (pl5 P 2 4) ^ 2 + (pl5 P 3 4) ^ 2) =
        pairNorm5 P * 2 := by
    simp only [pairNorm5]; ring
  simp only [mu5]
  field_simp [hN]
  exact hnums

/-- Each coordinate of the n = 5 Plücker-square moment map is ≥ 0 when the Plücker norm is positive. -/
theorem mu5_nonneg (P : Matrix (Fin 2) (Fin 5) ℝ) (hN : 0 < pairNorm5 P) (i : Fin 5) :
    0 ≤ mu5 P i := by
  fin_cases i <;> simp only [mu5] <;> positivity

/-- Each coordinate of the n = 5 Plücker-square moment map is ≤ 1 when the Plücker norm is positive. -/
theorem mu5_le_one (P : Matrix (Fin 2) (Fin 5) ℝ) (hN : 0 < pairNorm5 P) (i : Fin 5) :
    mu5 P i ≤ 1 := by
  fin_cases i <;>
    · simp only [mu5]
      refine (div_le_one hN).2 ?_
      simp only [pairNorm5]
      nlinarith [sq_nonneg (pl5 P 0 1), sq_nonneg (pl5 P 0 2), sq_nonneg (pl5 P 0 3),
        sq_nonneg (pl5 P 0 4), sq_nonneg (pl5 P 1 2), sq_nonneg (pl5 P 1 3),
        sq_nonneg (pl5 P 1 4), sq_nonneg (pl5 P 2 3), sq_nonneg (pl5 P 2 4),
        sq_nonneg (pl5 P 3 4)]

/-- For a 2×5 matrix with positive Plücker norm, the Plücker-square moment map lands in the
  hypersimplex Δ(2,5). -/
theorem moment_in_hypersimplex25 (P : Matrix (Fin 2) (Fin 5) ℝ) (hN : 0 < pairNorm5 P) :
    hypersimplex25 (mu5 P) := by
  refine ⟨fun i => ⟨mu5_nonneg P hN i, mu5_le_one P hN i⟩, ?_⟩
  simpa using mu5_sum P (ne_of_gt hN)

/-! ## (b) n = 4 planar three-channel identity -/

/-- Planar / dual-channel monomials from Plücker (n = 4). -/
def channel01_23 (P : Matrix (Fin 2) (Fin 4) ℝ) : ℝ := pl P 0 1 * pl P 2 3
/-- The n = 4 Plücker monomial `⟨03⟩⟨12⟩` (one of the three channel monomials in the Klein
  relation). -/
def channel03_12 (P : Matrix (Fin 2) (Fin 4) ℝ) : ℝ := pl P 0 3 * pl P 1 2
/-- The n = 4 Plücker monomial `⟨02⟩⟨13⟩` (one of the three channel monomials in the Klein
  relation). -/
def channel02_13 (P : Matrix (Fin 2) (Fin 4) ℝ) : ℝ := pl P 0 2 * pl P 1 3

/-- **(b)** Klein Plücker relation = planar three-channel identity. -/
theorem planar_three_channel (P : Matrix (Fin 2) (Fin 4) ℝ) :
    channel01_23 P + channel03_12 P = channel02_13 P := by
  have h := plucker_rel (R := ℝ) P
  simp only [channel01_23, channel03_12, channel02_13] at *
  linarith

/-! ## (c) n = 5 planar Plücker monomials on the Assoc chart -/

/-- X13 ~ ⟨0 2⟩⟨1 3⟩. -/
def X13mono (P : Matrix (Fin 2) (Fin 5) ℝ) : ℝ := pl5 P 0 2 * pl5 P 1 3
/-- X14 ~ ⟨0 3⟩⟨1 4⟩. -/
def X14mono (P : Matrix (Fin 2) (Fin 5) ℝ) : ℝ := pl5 P 0 3 * pl5 P 1 4
/-- X24 ~ ⟨1 3⟩⟨2 4⟩. -/
def X24mono (P : Matrix (Fin 2) (Fin 5) ℝ) : ℝ := pl5 P 1 3 * pl5 P 2 4

/-- Chart offset c13 chosen so the ABHY affine relation holds on these monomials
(same move as restricting to H_5 in `Assoc`). -/
def c13Mono (P : Matrix (Fin 2) (Fin 5) ℝ) : ℝ :=
  X24mono P - X14mono P + X13mono P

/-- **(c₁)** Assoc affine relation `X24 = X14 − X13 + c13` on the Plücker monomials. -/
theorem assoc_affine_X24 (P : Matrix (Fin 2) (Fin 5) ℝ) :
    X24mono P = X14mono P - X13mono P + c13Mono P := by
  simp [c13Mono]

/-- **(c₂)** Evaluating `Assoc.X` at `(c13, x, y) = (c13Mono, X13mono, X14mono)` recovers `X24mono`.
This is the Lean edge Klein/`pl5` → `Assoc.X`. -/
theorem assoc_X24_matches (P : Matrix (Fin 2) (Fin 5) ℝ) (c14 c24 : ℝ) :
    PositiveGeometryEmergentSpaceTime.Assoc.X (c13Mono P) c14 c24 (X13mono P) (X14mono P) 1 = X24mono P := by
  simp [PositiveGeometryEmergentSpaceTime.Assoc.X, c13Mono]

/-- Witness: a concrete 2×4 matrix with nonzero Plücker norm has moment map in Δ(2,4). -/
theorem moment24_witness :
    0 < pairNorm4 (!![1, 0, 1, 0; 0, 1, 0, 1] : Matrix (Fin 2) (Fin 4) ℝ) ∧
      hypersimplex24 (mu4 !![1, 0, 1, 0; 0, 1, 0, 1]) := by
  have hN : 0 < pairNorm4 (!![1, 0, 1, 0; 0, 1, 0, 1] : Matrix (Fin 2) (Fin 4) ℝ) := by
    simp [pairNorm4, pl_eq]; norm_num
  exact ⟨hN, moment_in_hypersimplex24 _ hN⟩

/-- Witness: three-channel identity on the chart `[I|X]`. -/
theorem planar_channel_witness :
    channel01_23 (chart (R := ℝ) !![1, 2; 3, 4]) +
        channel03_12 (chart (R := ℝ) !![1, 2; 3, 4]) =
      channel02_13 (chart (R := ℝ) !![1, 2; 3, 4]) :=
  planar_three_channel _


/-- **Graph bridge.** One theorem whose type uses both the n=4 Klein/`pl` moment map
and the n=5 `Assoc.X` chart skeleton — a real Lean edge between the two trunks. -/
theorem pl_assoc_bridge :
    (∀ P : Matrix (Fin 2) (Fin 4) ℝ, 0 < pairNorm4 P → hypersimplex24 (mu4 P)) ∧
      (∀ P : Matrix (Fin 2) (Fin 5) ℝ, ∀ c14 c24 : ℝ,
        PositiveGeometryEmergentSpaceTime.Assoc.X (c13Mono P) c14 c24 (X13mono P) (X14mono P) 1 = X24mono P) :=
  ⟨moment_in_hypersimplex24, fun P c14 c24 => assoc_X24_matches P c14 c24⟩

end PositiveGeometryEmergentSpaceTime.BridgePLAssoc
