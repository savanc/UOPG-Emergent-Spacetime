/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.Legendre

/-!
# F-DIM — tree-level unitarity of the trunk pion amplitude bounds, but does not force, the spacetime dimension

Also known as: F-DIM, critical dimension of the Lovelace–Shapiro amplitude.
Amplitude: `A = Γ(1−α(s))Γ(1−α(t))/Γ(1−α(s)−α(t))`, `α(s) = α₀ + s`, `α′ = 1`, Adler zero `m_π² = ½ − α₀`
(Bianchi–Consoli–Di Vecchia 2021, CITED). Partial waves are SO(D−1) Gegenbauer polynomials `C_j^λ`, `λ = (D−3)/2`
(Arkani-Hamed–Eberhardt–Huang–Mizera arXiv:2201.11575, CITED). Here:
* `quadratic_gegenbauer`: exact spin decomposition of a quadratic residue; the spin-0 coefficient is `a/(D−1) + c`;
* `lsLevel1_eq`: the level-1 residue polynomial;
* `ls_spin0_nonneg_iff`: spin-0 positivity at level 1 ⇔ `D ≤ lsCritDim α₀ = 2(1+4α₀)/(2−α₀)`;
* `lsCritDim_half = 4`, `lsCritDim_one = 10`, `bos_spin0_nonneg_iff` (`D ≤ 26`);
* `lsCritDim_surj`: every real bound `> 1` occurs for some intercept, so the integer 4 is inherited from the
  Adler-zero value `α₀ = ½`, not produced by positivity;
* `trunk_bound_not_forced`: at `α₀ = ½`, both `D = 3` and `D = 4` pass and every named candidate
  `8, 10, 11, 16, 24, 26` fails: a bound, not an equality.
No axioms; no FRONTIER-AXIOM.
-/

namespace PositiveGeometryEmergentSpaceTime.FDim

/-- Gegenbauer `C₁^λ(x) = 2λx`. Also known as: `G₁(x, D)`. -/
def gegen1 (lam x : ℝ) : ℝ := 2 * lam * x

/-- Gegenbauer `C₂^λ(x) = 2λ(λ+1)x² − λ`. Also known as: `G₂(x, D)`. -/
def gegen2 (lam x : ℝ) : ℝ := 2 * lam * (lam + 1) * x ^ 2 - lam

/-- Spin decomposition of a quadratic residue `a x² + b x + c` in `D = 2λ + 3` dimensions. -/
theorem quadratic_gegenbauer {lam : ℝ} (hl : 0 < lam) (a b c x : ℝ) :
    a * x ^ 2 + b * x + c =
      (a / (2 * (lam + 1)) + c) + (b / (2 * lam)) * gegen1 lam x
        + (a / (2 * lam * (lam + 1))) * gegen2 lam x := by
  unfold gegen1 gegen2
  field_simp
  ring

/-- Level-1 residue of the LS amplitude (up to the free overall sign): `(α(t) − 1 + 1)(α(t) − 1 + 2)` with
`t = −(3α₀/2)(1−x)` at `s₁ = 2 − α₀`, `m² = ½ − α₀`. Also known as: `R₁(x)`. -/
noncomputable def lsLevel1 (alpha0 x : ℝ) : ℝ :=
  (alpha0 - 3 * alpha0 / 2 * (1 - x)) * (alpha0 + 1 - 3 * alpha0 / 2 * (1 - x))

/-- Closed form of the level-1 residue polynomial: `lsLevel1 α₀ x = α₀/4 · (9α₀x² + (6 − 6α₀)x − (2
  − α₀))`. -/
theorem lsLevel1_eq (alpha0 x : ℝ) :
    lsLevel1 alpha0 x = alpha0 / 4 * (9 * alpha0 * x ^ 2 + (6 - 6 * alpha0) * x - (2 - alpha0)) := by
  unfold lsLevel1; ring

/-- Critical dimension of the LS family. Also known as: `D_c(α₀)`. -/
noncomputable def lsCritDim (alpha0 : ℝ) : ℝ := 2 * (1 + 4 * alpha0) / (2 - alpha0)

/-- Spin-0 coefficient (divided by `α₀/4 > 0`) of the level-1 residue in `D` dimensions. -/
noncomputable def lsSpin0 (alpha0 D : ℝ) : ℝ := 9 * alpha0 / (D - 1) - (2 - alpha0)

/-- For `α₀ < 2` and `D > 1`, the level-1 spin-0 coefficient is ≥ 0 iff `D ≤ lsCritDim α₀`. -/
theorem ls_spin0_nonneg_iff {alpha0 D : ℝ} (h2 : alpha0 < 2) (hD : 1 < D) :
    0 ≤ lsSpin0 alpha0 D ↔ D ≤ lsCritDim alpha0 := by
  unfold lsSpin0 lsCritDim
  have hD1 : 0 < D - 1 := by linarith
  have h2' : 0 < 2 - alpha0 := by linarith
  rw [sub_nonneg, le_div_iff₀ hD1, le_div_iff₀ h2']
  constructor <;> intro h <;> nlinarith

/-- `lsCritDim (1/2) = 4`. -/
theorem lsCritDim_half : lsCritDim (1 / 2) = 4 := by unfold lsCritDim; norm_num

/-- `lsCritDim 1 = 10`. -/
theorem lsCritDim_one : lsCritDim 1 = 10 := by unfold lsCritDim; norm_num

/-- Bosonic open string, first massive level: spin-0 coefficient `∝ 25/(D−1) − 1`; positive iff `D ≤
  26`. -/
theorem bos_spin0_nonneg_iff {D : ℝ} (hD : 1 < D) : 0 ≤ 25 / (D - 1) - 1 ↔ D ≤ 26 := by
  have hD1 : 0 < D - 1 := by linarith
  rw [sub_nonneg, le_div_iff₀ hD1]
  constructor <;> intro h <;> linarith

/-- The bound is continuous in the intercept: every real `d > 1` is `lsCritDim α₀` for some `α₀ ∈
  (0, 2)`. -/
theorem lsCritDim_surj {d : ℝ} (hd : 1 < d) :
    ∃ alpha0, 0 < alpha0 ∧ alpha0 < 2 ∧ lsCritDim alpha0 = d := by
  refine ⟨2 * (d - 1) / (8 + d), by apply div_pos <;> linarith, ?_, ?_⟩
  · rw [div_lt_iff₀ (by linarith)]; linarith
  · unfold lsCritDim
    have h8 : (8 + d) ≠ 0 := by linarith
    have hden : 2 - 2 * (d - 1) / (8 + d) = 18 / (8 + d) := by field_simp; ring
    rw [hden]
    field_simp
    ring

/-- At the trunk intercept `α₀ = ½` the level-1 condition allows both `D = 3` and `D = 4` (a bound, not an
equality) and excludes every named candidate `8, 10, 11, 16, 24, 26`. -/
theorem trunk_bound_not_forced :
    0 ≤ lsSpin0 (1 / 2) 3 ∧ 0 ≤ lsSpin0 (1 / 2) 4 ∧
    ∀ D ∈ ({8, 10, 11, 16, 24, 26} : Set ℝ), lsSpin0 (1 / 2) D < 0 := by
  refine ⟨by unfold lsSpin0; norm_num, by unfold lsSpin0; norm_num, ?_⟩
  intro D hD
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hD
  rcases hD with rfl | rfl | rfl | rfl | rfl | rfl <;> unfold lsSpin0 <;> norm_num

/-- Bundle (F-DIM): level-1 positivity ⇔ `D ≤ D_c(α₀)`; `D_c(½) = 4`; `D_c` takes every real value
  `> 1`. -/
theorem fdim_bound_not_forced :
    (∀ alpha0 D : ℝ, alpha0 < 2 → 1 < D → (0 ≤ lsSpin0 alpha0 D ↔ D ≤ lsCritDim alpha0)) ∧
    lsCritDim (1 / 2) = 4 ∧ (∀ d : ℝ, 1 < d → ∃ alpha0,
        0 < alpha0 ∧ alpha0 < 2 ∧ lsCritDim alpha0 = d) :=
  ⟨fun _ _ h2 hD => ls_spin0_nonneg_iff h2 hD, lsCritDim_half, fun _ hd => lsCritDim_surj hd⟩

/-- F-DIM′: level-2 trunk residue at `α₀ = ½` (`σ`-normalised, ×128): `(5x−3)(5x+1)(5x+5)`. Also
  known as: `R₂(x)`. -/
def lsLevel2Half (x : ℝ) : ℝ := (5 * x - 3) * (5 * x + 1) * (5 * x + 5)

open PositiveGeometryEmergentSpaceTime.Legendre in
/-- F-DIM′: in `D = 4` the level-2 trunk residue has partial-wave coefficients `10, 10, 50, 50 ≥ 0`
  (spins 0..3). -/
theorem lsLevel2Half_legendre (x : ℝ) :
    lsLevel2Half x = 10 + 10 * legendreP1 x + 50 * legendreP2 x + 50 * legendreP3 x := by
  unfold lsLevel2Half legendreP1 legendreP2 legendreP3; ring

end PositiveGeometryEmergentSpaceTime.FDim
