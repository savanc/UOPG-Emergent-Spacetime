/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — H-T5 tie theorems for the NAME-ONLY definition `IsingTiling.C` (D161).
Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.IsingTiling
import PositiveGeometryEmergentSpaceTime.IsingOG

/-!
# H-T5 ties: `IsingTiling.C` is the GP matrix of the star Ising network

* Star Gibbs sum (known value): for the 3-leaf star with the centre spin summed out, high-temperature
  weights `∏ᵢ (1 + tᵢ σ₀ σᵢ)` over the 16 spin configurations give `Z = 16` and `⟨σᵢσⱼ⟩ = tᵢ tⱼ` for all t.
  `exp_spin`: `exp (J s) = cosh J (1 + s tanh J)` for `s = ±1`, so these are the Boltzmann weights up to
  the constant `∏ cosh Jᵢ`, with `tᵢ = tanh Jᵢ`.
* GP sign rule (GP arXiv:1807.03282 eq. 2.4 as transcribed in `IsingOG`; 0-indexed):
  row i, column pair (2j, 2j+1), i ≠ j: `(s, −s)·mᵢⱼ` with `s = (−1)^{i+j+1}` if `i < j`, `(−1)^{i+j}` if `i > j`;
  diagonal pair `(1, 1)`.
* Tie (D161): `gpRule` of the star correlations at `t = (1/2, 1/3, 1/4)` is exactly `IsingTiling.C`,
  and its real cast is `IsingOG.gpY (1/2) (1/3) (1/4)` (whose 20 minors are positive, `gpY_pos_sample`).
* Planted: a wrong `t` gives a different matrix; dropping the GP signs leaves OG(3,6).
* Non-vacuity: `C` is in OG(3,6) and has a positive maximal minor.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.IsingStar
open PositiveGeometryEmergentSpaceTime.IsingTiling

/-! ## Star Gibbs sum -/

/-- The 16 configurations `(σ₀, σ₁, σ₂, σ₃) ∈ {±1}⁴`. -/
def cfgs : List (ℚ × ℚ × ℚ × ℚ) :=
  [1, -1].flatMap fun a => [1, -1].flatMap fun b => [1, -1].flatMap fun c => [1, -1].map fun d => (a, b, c, d)

/-- High-temperature weight of a configuration. -/
def wt (t₁ t₂ t₃ : ℚ) (s : ℚ × ℚ × ℚ × ℚ) : ℚ :=
  (1 + t₁ * s.1 * s.2.1) * (1 + t₂ * s.1 * s.2.2.1) * (1 + t₃ * s.1 * s.2.2.2)

def Z (t₁ t₂ t₃ : ℚ) : ℚ := (cfgs.map (wt t₁ t₂ t₃)).sum
def N12 (t₁ t₂ t₃ : ℚ) : ℚ := (cfgs.map fun s => wt t₁ t₂ t₃ s * s.2.1 * s.2.2.1).sum
def N13 (t₁ t₂ t₃ : ℚ) : ℚ := (cfgs.map fun s => wt t₁ t₂ t₃ s * s.2.1 * s.2.2.2).sum
def N23 (t₁ t₂ t₃ : ℚ) : ℚ := (cfgs.map fun s => wt t₁ t₂ t₃ s * s.2.2.1 * s.2.2.2).sum

theorem Z_eq (t₁ t₂ t₃ : ℚ) : Z t₁ t₂ t₃ = 16 := by
  simp [Z, cfgs, wt]; ring

/-- Known value: boundary correlations of the star are `tᵢ tⱼ` (for every t). -/
theorem star_corr (t₁ t₂ t₃ : ℚ) :
    N12 t₁ t₂ t₃ / Z t₁ t₂ t₃ = t₁ * t₂ ∧ N13 t₁ t₂ t₃ / Z t₁ t₂ t₃ = t₁ * t₃ ∧
    N23 t₁ t₂ t₃ / Z t₁ t₂ t₃ = t₂ * t₃ := by
  rw [Z_eq]
  refine ⟨?_, ?_, ?_⟩ <;> simp [N12, N13, N23, cfgs, wt] <;> ring

/-- Boltzmann weight of one edge in high-temperature form. -/
theorem exp_spin (J s : ℝ) (hs : s = 1 ∨ s = -1) :
    Real.exp (J * s) = Real.cosh J * (1 + s * Real.tanh J) := by
  have hc : Real.cosh J ≠ 0 := (Real.cosh_pos J).ne'
  rw [Real.tanh_eq_sinh_div_cosh]
  rcases hs with rfl | rfl
  · rw [mul_one, ← Real.cosh_add_sinh]; field_simp
  · rw [mul_neg_one, ← Real.cosh_sub_sinh]; field_simp; ring

/-! ## GP sign rule -/

/-- Sign of the odd column of pair `j` in row `i` (0-indexed). -/
def gpSign (i j : ℕ) : ℚ := if i < j then (-1) ^ (i + j + 1) else (-1) ^ (i + j)

/-- GP's `M̃` for an `n = 3` correlation function `m`. -/
def gpRule (m : ℕ → ℕ → ℚ) : Matrix (Fin 3) (Fin 6) ℚ := Matrix.of fun i c =>
  if c.val / 2 = i.val then 1
  else gpSign i (c.val / 2) * m i (c.val / 2) * (if c.val % 2 = 0 then 1 else -1)

/-- Star correlations at `t`. -/
def starM (t : ℕ → ℚ) : ℕ → ℕ → ℚ := fun i j => t i * t j

def t0 : ℕ → ℚ := fun i => if i = 0 then 1/2 else if i = 1 then 1/3 else 1/4

/-- **Tie (D161).** `IsingTiling.C` is GP's matrix of the star correlations at `t = (1/2, 1/3, 1/4)`. -/
theorem C_eq_gpRule : C = gpRule (starM t0) := by
  ext i c; fin_cases i <;> fin_cases c <;> simp [C, gpRule, gpSign, starM, t0] <;> norm_num

/-- The real cast of `C` is `IsingOG.gpY (1/2) (1/3) (1/4)`, the point whose twenty minors are positive. -/
theorem C_cast_eq_gpY : C.map (Rat.cast : ℚ → ℝ) = PositiveGeometryEmergentSpaceTime.IsingOG.gpY (1/2) (1/3) (1/4) := by
  ext i c; fin_cases i <;> fin_cases c <;> simp [C, PositiveGeometryEmergentSpaceTime.IsingOG.gpY] <;> norm_num

/-- `C` lies in the positive part: every maximal minor is positive (via `IsingOG.gpY_pos_sample`). -/
theorem C_positive : 0 < PositiveGeometryEmergentSpaceTime.IsingOG.m3 (C.map (Rat.cast : ℚ → ℝ)) 0 1 2 ∧
    0 < PositiveGeometryEmergentSpaceTime.IsingOG.m3 (C.map (Rat.cast : ℚ → ℝ)) 3 4 5 := by
  rw [C_cast_eq_gpY]
  exact ⟨PositiveGeometryEmergentSpaceTime.IsingOG.gpY_pos_sample.1, (PositiveGeometryEmergentSpaceTime.IsingOG.gpY_pos_sample).2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2⟩

/-! ## Planted cases -/

def t1 : ℕ → ℚ := fun i => if i = 0 then 1/2 else if i = 1 then 1/3 else 1/5

/-- Planted: wrong couplings `t = (1/2, 1/3, 1/5)` do not reproduce `C`. -/
theorem planted_t : C ≠ gpRule (starM t1) := by
  intro h
  have := congrFun (congrFun h 0) 4
  simp [C, gpRule, gpSign, starM, t1] at this; norm_num at this

/-- Planted: the unsigned rule (all off-diagonal entries `(+m, −m)`) leaves OG(3,6). -/
def plainRule (m : ℕ → ℕ → ℚ) : Matrix (Fin 3) (Fin 6) ℚ := Matrix.of fun i c =>
  if c.val / 2 = i.val then 1 else m i (c.val / 2) * (if c.val % 2 = 0 then 1 else -1)

theorem planted_sign : ∑ m, plainRule (starM t0) 0 m * ogSignature m * plainRule (starM t0) 1 m ≠ 0 := by
  simp [plainRule, starM, t0, ogSignature, Fin.sum_univ_succ]; norm_num

/-- The GP-signed matrix of the star satisfies the OG relations for every `t` (not just `t0`). -/
theorem gpRule_orth (t : ℕ → ℚ) (i j : Fin 3) :
    ∑ m, gpRule (starM t) i m * ogSignature m * gpRule (starM t) j m = 0 := by
  fin_cases i <;> fin_cases j <;> simp [gpRule, gpSign, starM, ogSignature, Fin.sum_univ_succ] <;> ring

/-- Non-vacuity: `C` itself satisfies the OG relation and its correlation entries are nonzero. -/
theorem nonvacuous : (∑ m, C 0 m * ogSignature m * C 1 m = 0) ∧ C 0 2 ≠ 0 ∧ C 1 4 ≠ 0 ∧ C 2 0 ≠ 0 := by
  refine ⟨C_orth 0 1, ?_, ?_, ?_⟩ <;> simp [C]

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.IsingStar
