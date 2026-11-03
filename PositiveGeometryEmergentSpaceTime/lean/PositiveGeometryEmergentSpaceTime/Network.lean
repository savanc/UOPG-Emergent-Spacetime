/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.MarkovTrace

/-!
# H-T1 (e): trace = Kron reduction = response matrix, and Lam's map to Gr≥0

* (e1) `schur_trace`: for any chain with blocks `A, B, C, D` and stationary weights, the trace generator scaled by
  `diag(π_S)` is the Schur complement of `L = diag(π)(1 − P)`: `diag(π_S)(1 − Tr) = L_SS − L_SB L_BB⁻¹ L_BS`. For a
  reversible chain `L` is the conductance Laplacian (`c_xy = π_x P_xy`), so this is Kron reduction (the response
  matrix). The identity itself needs no reversibility.
* (e2) The 2-boundary path network `1 — 0 — 2` (conductances `a, c`) as a chain. At `a = c` it is *exactly* the
  counterexample `P3` of (a) (`path_eq_traceP3`). Its Lam point in Gr(1,4) is `[ac : a+c : ac : a+c]`, all coordinates
  > 0 (`lam2_pos`), and `Δ₁/Δ₂` is the effective conductance read off the trace (`lam2_response`).
* (e3) The Y (star) network: an explicit 2×6 matrix whose 15 Plücker coordinates are Lam's `Δ_I = Σ L_σ`
  (computed from his §5.2 concordance rule in `scripts/ht1_lam_concordance.py`), all > 0 for positive conductances
  (`Y_pluecker`, `Y_pos`). The star chain's trace gives the response matrix, which the Plücker ratios recover
  (`star_response`).

Lam, *Electroid varieties and a compactification of the space of electrical networks*, arXiv:1402.6261.
-/

open Matrix

namespace PositiveGeometryEmergentSpaceTime.Network

variable {S B : Type*} [Fintype S] [Fintype B] [DecidableEq S] [DecidableEq B]

/-- **(e1)** Trace generator = Schur complement of `L = diag(π)(1 − P)` (Kron reduction). `K` is the explicit inverse
of `L_BB`. -/
theorem schur_trace (pS : S → ℝ) (pB : B → ℝ) (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ)
    (D N : Matrix B B ℝ) (hpB : ∀ b, pB b ≠ 0) (hN : (1 - D) * N = 1) (hN' : N * (1 - D) = 1) :
    let LSS := diagonal pS * (1 - A)
    let LSB := -(diagonal pS * Bm)
    let LBS := -(diagonal pB * C)
    let LBB := diagonal pB * (1 - D)
    let K := N * diagonal (fun b => (pB b)⁻¹)
    K * LBB = 1 ∧ LBB * K = 1 ∧ LSS - LSB * K * LBS = diagonal pS * (1 - PositiveGeometryEmergentSpaceTime.MarkovTrace.trace A Bm C N) := by
  intro LSS LSB LBS LBB K
  have hd1 : diagonal (fun b => (pB b)⁻¹) * diagonal pB = 1 := by
    rw [diagonal_mul_diagonal, ← diagonal_one]; congr 1; ext b; exact inv_mul_cancel₀ (hpB b)
  have hd2 : diagonal pB * diagonal (fun b => (pB b)⁻¹) = 1 := by
    rw [diagonal_mul_diagonal, ← diagonal_one]; congr 1; ext b; exact mul_inv_cancel₀ (hpB b)
  refine ⟨?_, ?_, ?_⟩
  · simp only [K, LBB]; rw [Matrix.mul_assoc, ← Matrix.mul_assoc (diagonal _), hd1, Matrix.one_mul,
      hN']
  · simp only [K, LBB]; rw [Matrix.mul_assoc, ← Matrix.mul_assoc (1 - D), hN, Matrix.one_mul, hd2]
  · simp only [LSS, LSB, LBS, K, PositiveGeometryEmergentSpaceTime.MarkovTrace.trace]
    have : diagonal pS * Bm * (N * diagonal (fun b => (pB b)⁻¹)) * (diagonal pB * C) = diagonal pS * (Bm * N * C) := by
      simp only [Matrix.mul_assoc]; rw [← Matrix.mul_assoc (diagonal _) (diagonal pB), hd1,
          Matrix.one_mul]
    simp only [Matrix.neg_mul, Matrix.mul_neg, neg_neg]
    rw [this, Matrix.mul_sub, Matrix.mul_sub, Matrix.mul_add]
    abel

/-! ## (e2) Two boundary nodes: the path network -/

/-- Random walk on the path `0 — 2 — 1` (boundary 0, 1; interior 2) with conductances `a` (edge
  0–2), `c` (1–2). -/
noncomputable def Ppath (a c : ℝ) : Matrix (Fin 3) (Fin 3) ℝ := !![0, 0, 1; 0, 0, 1; a / (a + c),
    c / (a + c), 0]
/-- Stationary distribution `(a/(2(a+c)), c/(2(a+c)), 1/2)` of the path-network walk. -/
noncomputable def pipath (a c : ℝ) : Fin 3 → ℝ := ![a / (2 * (a + c)), c / (2 * (a + c)), 1 / 2]

/-- For positive conductances, `pipath a c` is stationary for the path-network walk `Ppath a c`. -/
theorem path_stationary (a c : ℝ) (ha : 0 < a) (hc : 0 < c) : pipath a c ᵥ* Ppath a c = pipath a c := by
  have : a + c ≠ 0 := by positivity
  ext j; fin_cases j <;> simp [pipath, Ppath, vecMul, dotProduct, Fin.sum_univ_three] <;> field_simp

/-- Reversible (detailed balance), so it is an electrical network with `c_xy = π_x P_xy`. -/
theorem path_reversible (a c : ℝ) (ha : 0 < a) (hc : 0 < c) :
    ∀ i j, pipath a c i * Ppath a c i j = pipath a c j * Ppath a c j i := by
  have : a + c ≠ 0 := by positivity
  intro i j; fin_cases i <;> fin_cases j <;> simp [pipath, Ppath] <;> field_simp

/-- At `a = c` the path network *is* the counterexample chain of (a). -/
theorem path_eq_traceP3 : Ppath 1 1 = PositiveGeometryEmergentSpaceTime.MarkovTrace.traceP3 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Ppath, PositiveGeometryEmergentSpaceTime.MarkovTrace.traceP3] <;> norm_num

/-- Trace on the boundary {0, 1}: every row is `(a, c)/(a + c)`. -/
theorem path_trace (a c : ℝ) (i j : Fin 2) :
    Ppath a c i.castSucc j.castSucc + Ppath a c i.castSucc 2 * Ppath a c 2 j.castSucc / (1 - Ppath a c 2 2)
      = ![a / (a + c), c / (a + c)] j := by
  fin_cases i <;> fin_cases j <;> simp [Ppath]

/-- Lam's point of Gr(1,4) for the path network: `Δ = (L₁₂, L₁|₂, L₁₂, L₁|₂) = (ac, a+c, ac, a+c)` (grove
measurements; concordance in `scripts/ht1_lam_concordance.py`). For `k = 1` the Plücker coordinates are the entries. -/
def lam2 (a c : ℝ) : Fin 4 → ℝ := ![a * c, a + c, a * c, a + c]

/-- For positive conductances every coordinate of `lam2 a c` is positive. -/
theorem lam2_pos (a c : ℝ) (ha : 0 < a) (hc : 0 < c) : ∀ k, 0 < lam2 a c k := by
  intro k; fin_cases k <;> simp [lam2] <;> positivity

/-- The observer window determines the Lam point: with the chain's own conductances, the response entry
`−Λ₀₁ = π₀ Tr₀₁` equals `(Δ₁/Δ₂) / (2(a+c))`. `Δ₁/Δ₂ = ac/(a+c)` is the effective conductance of the grove-normalised
network. -/
theorem lam2_response (a c : ℝ) (ha : 0 < a) (hc : 0 < c) :
    pipath a c 0 * (c / (a + c)) = (lam2 a c 0 / lam2 a c 1) / (2 * (a + c)) := by
  have : a + c ≠ 0 := by positivity
  simp [pipath, lam2]; field_simp

/-! ## (e3) Three boundary nodes: the Y network -/

/-- 2×2 minor on columns `i, j`. -/
def mn (M : Matrix (Fin 2) (Fin 6) ℝ) (i j : Fin 6) : ℝ := M 0 i * M 1 j - M 0 j * M 1 i

/-- Explicit 2×6 representative of Lam's point for the Y network (conductances `a, b, c` to boundary 1̄, 2̄, 3̄;
columns 1̄, 1̃, 2̄, 2̃, 3̄, 3̃). -/
noncomputable def MY (a b c : ℝ) : Matrix (Fin 2) (Fin 6) ℝ :=
  !![1, 0, -b / a, -(a + b + c) / (a * c), -(a + b) / a, -(a + b + c) / (a * c);
     0, a * c, a * b * c, a * (b + c), a * b * c, a * b]

/-- The 15 Plücker coordinates are Lam's grove sums: `Δ₁₃ = L₁₂₃ = abc`, `Δ₂₄ = L₁|₂|₃ = a+b+c`,
`Δ₃₄ = L₁₂|₃ = ab`, and so on. -/
theorem Y_pluecker (a b c : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    mn (MY a b c) 0 1 = a*c ∧
    mn (MY a b c) 0 2 = a*b*c ∧
    mn (MY a b c) 0 3 = a*b + a*c ∧
    mn (MY a b c) 0 4 = a*b*c ∧
    mn (MY a b c) 0 5 = a*b ∧
    mn (MY a b c) 1 2 = b*c ∧
    mn (MY a b c) 1 3 = a + b + c ∧
    mn (MY a b c) 1 4 = a*c + b*c ∧
    mn (MY a b c) 1 5 = a + b + c ∧
    mn (MY a b c) 2 3 = a*b ∧
    mn (MY a b c) 2 4 = a*b*c ∧
    mn (MY a b c) 2 5 = a*b + b*c ∧
    mn (MY a b c) 3 4 = a*c ∧
    mn (MY a b c) 3 5 = a + b + c ∧
    mn (MY a b c) 4 5 = b*c := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [mn, MY] <;> field_simp <;> ring

/-- **(e3) Strict positivity.** For positive conductances all 15 Plücker coordinates are > 0, so the network's
point lies in the totally positive part of Gr(2,6) (the top cell of Lam's slice X₃). -/
theorem Y_pos (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    0 < mn (MY a b c) 0 1 ∧
    0 < mn (MY a b c) 0 2 ∧
    0 < mn (MY a b c) 0 3 ∧
    0 < mn (MY a b c) 0 4 ∧
    0 < mn (MY a b c) 0 5 ∧
    0 < mn (MY a b c) 1 2 ∧
    0 < mn (MY a b c) 1 3 ∧
    0 < mn (MY a b c) 1 4 ∧
    0 < mn (MY a b c) 1 5 ∧
    0 < mn (MY a b c) 2 3 ∧
    0 < mn (MY a b c) 2 4 ∧
    0 < mn (MY a b c) 2 5 ∧
    0 < mn (MY a b c) 3 4 ∧
    0 < mn (MY a b c) 3 5 ∧
    0 < mn (MY a b c) 4 5 := by
  obtain ⟨h01, h02, h03, h04, h05, h12, h13, h14, h15, h23, h24, h25, h34, h35, h45⟩ :=
    Y_pluecker a b c ha.ne' hc.ne'
  refine ⟨by rw [h01]; positivity, by rw [h02]; positivity, by rw [h03]; positivity,
      by rw [h04]; positivity, by rw [h05]; positivity, by rw [h12]; positivity,
      by rw [h13]; positivity, by rw [h14]; positivity, by rw [h15]; positivity,
      by rw [h23]; positivity, by rw [h24]; positivity, by rw [h25]; positivity,
      by rw [h34]; positivity, by rw [h35]; positivity, by rw [h45]; positivity⟩

/-- The star chain (leaves 0,1,2 with conductances a,b,c to a centre) has trace `Tr_ij = a_j/Σ` on the leaves and
stationary leaf weights `a_i/(2Σ)`. Its response entry `Λ₀₁ = −π₀ Tr₀₁` satisfies
`−2Σ·Λ₀₁ = ab/Σ = Δ₃₄/Δ₂₄ = L₁₂|₃ / L₁|₂|₃`. The observer's response matrix is read off Lam's Plücker coordinates. -/
theorem star_response (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    2 * (a + b + c) * ((a / (2 * (a + b + c))) * (b / (a + b + c))) = mn (MY a b c) 2 3 / mn (MY a b c) 1 3 := by
  obtain ⟨-, -, -, -, -, -, h13, -, -, h23, -⟩ := Y_pluecker a b c ha.ne' hc.ne'
  rw [h13, h23]; have : a + b + c ≠ 0 := by positivity
  field_simp

end PositiveGeometryEmergentSpaceTime.Network
