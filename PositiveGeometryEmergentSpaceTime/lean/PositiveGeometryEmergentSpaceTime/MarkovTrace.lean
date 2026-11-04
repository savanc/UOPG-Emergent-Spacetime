/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# H-T1: trace chains, entropy rate, and Kac's factor

Pre-registration: `prereg/H-T1-trace-network-2026-10-11.md`. Review: `reviews/H-T1-result-2026-10-11.md`.

* **(a)** `conjecture_false`: an exact 3-state chain whose trace on two states has a *larger* entropy rate. This
  refutes the conjecture in the trace-order preprint (doi:10.20944/preprints202410.1305.v1) §3 as stated: "if P ≤t Q then the entropy rate of P is less
  than or equal to the entropy rate of Q".
* **(b)** For general finite blocks: the trace `A + B N C` is row-stochastic (`trace_mem_rowStochastic`), `π_S` is
  stationary for it (`trace_stationary`), and the Kac excursion identity gives a mean return time of `1/π(S)`
  (`kac`). Exact commute times for the *Traces* §7 example are in `commute_*`.
* **(c)** The corrected bound `π(S)·h(Tr) ≤ h(P)` for one eliminated state and any number of kept states
  (`one_state_elimination`). The counterexample attains equality (`corrected_equality`).

Entropy is in nats (`Real.negMulLog`); bits = nats / log 2.
-/

open Matrix Real Finset

namespace PositiveGeometryEmergentSpaceTime.MarkovTrace

/-- Entropy rate of a chain `P` in its stationary law `π` (nats): `Σᵢ πᵢ Σⱼ −Pᵢⱼ log Pᵢⱼ` (*Traces*
  eq. 47, natural log). -/
noncomputable def entRate {n : Type*} [Fintype n] (pr : n → ℝ) (P : Matrix n n ℝ) : ℝ :=
  ∑ i, pr i * ∑ j, negMulLog (P i j)

/-! ## (a) The counterexample -/

/-- States 0, 1 → 2; state 2 → 0 or 1 with probability ½.

Also known as: three-state P3, path-graph stochastic matrix counterexample.
-/
noncomputable def traceP3 : Matrix (Fin 3) (Fin 3) ℝ := !![0, 0, 1; 0, 0, 1; 1/2, 1/2, 0]
/-- Stationary distribution `(1/4, 1/4, 1/2)` of `traceP3`. -/
noncomputable def pi3 : Fin 3 → ℝ := ![1/4, 1/4, 1/2]

/-- The 3-state chain `traceP3` is row-stochastic. -/
theorem traceP3_stochastic : traceP3 ∈ rowStochastic ℝ (Fin 3) := by
  rw [mem_rowStochastic_iff_sum]; constructor
  · intro i j; fin_cases i <;> fin_cases j <;> norm_num [traceP3]
  · intro i; fin_cases i <;> simp [traceP3, Fin.sum_univ_three] <;> norm_num

/-- `pi3 = (1/4, 1/4, 1/2)` is stationary for `traceP3`. -/
theorem pi3_stationary : pi3 ᵥ* traceP3 = pi3 := by
  ext j; fin_cases j <;> simp [pi3, traceP3, vecMul, dotProduct, Fin.sum_univ_three] <;> norm_num

/-- The trace on `S = {0,1}` (eliminate state 2): `Tr i j = P i j + P i 2 · P 2 j / (1 − P 2 2)`. -/
noncomputable def Tr3 : Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => traceP3 i.castSucc j.castSucc + traceP3 i.castSucc 2 * traceP3 2 j.castSucc / (1 - traceP3 2 2)

/-- The trace of `traceP3` on the first two states is the 2×2 matrix with all entries 1/2. -/
theorem Tr3_eq : Tr3 = !![1/2, 1/2; 1/2, 1/2] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Tr3, traceP3]

/-- `negMulLog (1/2) = log 2 / 2`. -/
lemma negMulLog_half : negMulLog (2⁻¹ : ℝ) = log 2 / 2 := by
  simp [negMulLog, Real.log_inv]; ring

/-- The entropy rate of `traceP3` at `pi3` is `log 2 / 2`. -/
theorem entRate_traceP3 : entRate pi3 traceP3 = log 2 / 2 := by
  simp [entRate, pi3, traceP3, Fin.sum_univ_three]; rw [negMulLog_half]; ring

/-- The entropy rate of the trace chain `Tr3` at `(1/2, 1/2)` is `log 2`, larger than that of
  `traceP3`. -/
theorem entRate_Tr3 : entRate ![1/2, 1/2] Tr3 = log 2 := by
  rw [Tr3_eq]; simp [entRate, Fin.sum_univ_two]; rw [negMulLog_half]; ring

/-- In bits: `h(P) = ½`, `h(Tr) = 1`. -/
theorem bits : entRate pi3 traceP3 / log 2 = 1/2 ∧ entRate ![1/2, 1/2] Tr3 / log 2 = 1 := by
  have h := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  rw [entRate_traceP3, entRate_Tr3]; constructor <;> field_simp

/-- **(a)** The *Traces* §3 conjecture is false as stated: the trace (the observer, `Tr3 ≤t traceP3`) has a strictly larger
entropy rate than the chain it traces. -/
theorem conjecture_false : entRate pi3 traceP3 < entRate ![1/2, 1/2] Tr3 := by
  rw [entRate_traceP3, entRate_Tr3]; have := Real.log_pos (by norm_num : (1 : ℝ) < 2); linarith

/-- The corrected per-original-step statement holds with equality here: `π(S)·h(Tr) = h(P)`, with
  `π(S) = ½`. -/
theorem corrected_equality : (pi3 0 + pi3 1) * entRate ![1/2, 1/2] Tr3 = entRate pi3 traceP3 := by
  rw [entRate_traceP3, entRate_Tr3]; simp [pi3]; ring

/-! ## (b) General trace algebra (any finite S, B) -/

variable {S B : Type*} [Fintype S] [Fintype B] [DecidableEq S] [DecidableEq B]

/-- The trace (stochastic complement) `A + B N C`, with `N = (1 − D)⁻¹` supplied as data. -/
def trace (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ) (N : Matrix B B ℝ) : Matrix S S ℝ :=
  A + Bm * N * C

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- If the block chain has row sums 1 and `N (1 − D) = 1`, the trace `A + B N C` has row sums 1. -/
@[nolint unusedArguments]
theorem trace_rowsum (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ) (D N : Matrix B B ℝ)
    (hS : A *ᵥ 1 + Bm *ᵥ 1 = 1) (hB : C *ᵥ 1 + D *ᵥ 1 = 1) (hN : N * (1 - D) = 1) :
    trace A Bm C N *ᵥ 1 = 1 := by
  have hC : C *ᵥ 1 = (1 - D) *ᵥ 1 := by
    rw [sub_mulVec, one_mulVec]; exact eq_sub_of_add_eq hB
  have : N *ᵥ (C *ᵥ 1) = 1 := by rw [hC, mulVec_mulVec, hN, one_mulVec]
  rw [trace, add_mulVec, ← mulVec_mulVec, ← mulVec_mulVec, this, hS]

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- If `A, B, C, N` are entrywise nonnegative, the trace `A + B N C` is entrywise nonnegative. -/
@[nolint unusedArguments]
theorem trace_nonneg (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ) (N : Matrix B B ℝ)
    (hA : ∀ i j, 0 ≤ A i j) (hBm : ∀ i j, 0 ≤ Bm i j) (hC : ∀ i j, 0 ≤ C i j) (hN : ∀ i j, 0 ≤ N i j) :
    ∀ i j, 0 ≤ trace A Bm C N i j := by
  intro i j
  simp only [trace, Matrix.add_apply, mul_apply]
  refine add_nonneg (hA i j) (sum_nonneg fun k _ => mul_nonneg (sum_nonneg fun l _ => mul_nonneg (hBm _ _) (hN _ _))
    (hC _ _))

/-- The trace of a stochastic chain is stochastic (Mathlib's `rowStochastic`), given `N ≥ 0`. -/
theorem trace_mem_rowStochastic (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ) (D N : Matrix B B ℝ)
    (hA : ∀ i j, 0 ≤ A i j) (hBm : ∀ i j, 0 ≤ Bm i j) (hC : ∀ i j, 0 ≤ C i j) (hNn : ∀ i j, 0 ≤ N i j)
    (hS : A *ᵥ 1 + Bm *ᵥ 1 = 1) (hB : C *ᵥ 1 + D *ᵥ 1 = 1) (hN : N * (1 - D) = 1) :
    trace A Bm C N ∈ rowStochastic ℝ S :=
  ⟨trace_nonneg A Bm C N hA hBm hC hNn, trace_rowsum A Bm C D N hS hB hN⟩

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Stationarity of `π` on `S ⊔ B` gives `π_B = π_S B N`. -/
@[nolint unusedArguments]
theorem piB_eq (Bm : Matrix S B ℝ) (D N : Matrix B B ℝ) (pS : S → ℝ) (pB : B → ℝ)
    (h2 : pS ᵥ* Bm + pB ᵥ* D = pB) (hN : (1 - D) * N = 1) : pB = (pS ᵥ* Bm) ᵥ* N := by
  have : pB ᵥ* (1 - D) = pS ᵥ* Bm := by rw [vecMul_sub, vecMul_one]; exact (eq_sub_of_add_eq h2).symm
  calc pB = pB ᵥ* ((1 - D) * N) := by rw [hN, vecMul_one]
    _ = (pS ᵥ* Bm) ᵥ* N := by rw [← vecMul_vecMul, this]

/-- **(b) Stationary law of the trace.** `π_S` is stationary for `Tr`, hence so is `π_S / π(S)`. -/
theorem trace_stationary (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ) (D N : Matrix B B ℝ)
    (pS : S → ℝ) (pB : B → ℝ) (h1 : pS ᵥ* A + pB ᵥ* C = pS) (h2 : pS ᵥ* Bm + pB ᵥ* D = pB)
    (hN : (1 - D) * N = 1) : pS ᵥ* trace A Bm C N = pS := by
  rw [trace, vecMul_add, ← vecMul_vecMul, ← vecMul_vecMul, ← piB_eq Bm D N pS pB h2 hN, h1]

/-- If `(π_S, π_B)` is stationary for the block chain and `(1 − D) N = 1`, then every rescaling `Z⁻¹
  π_S` is stationary for the trace `A + B N C`. -/
theorem trace_stationary_normalised (A : Matrix S S ℝ) (Bm : Matrix S B ℝ) (C : Matrix B S ℝ) (D N : Matrix B B ℝ)
    (pS : S → ℝ) (pB : B → ℝ) (h1 : pS ᵥ* A + pB ᵥ* C = pS) (h2 : pS ᵥ* Bm + pB ᵥ* D = pB)
    (hN : (1 - D) * N = 1) (Z : ℝ) : (Z⁻¹ • pS) ᵥ* trace A Bm C N = Z⁻¹ • pS := by
  rw [smul_vecMul, trace_stationary A Bm C D N pS pB h1 h2 hN]

/-- **(b) Kac.** With `π` a probability vector, the excursion sum `Σ_{i∈S} πᵢ (1 + (B N 𝟙)ᵢ)` equals 1. The expected
return time to `S` from `π_S/π(S)` (1 step plus the expected time in `B`, the Kemeny–Snell fundamental-matrix
identification, CITED) is therefore `1/π(S)`. -/
theorem kac_sum (Bm : Matrix S B ℝ) (D N : Matrix B B ℝ) (pS : S → ℝ) (pB : B → ℝ)
    (h2 : pS ᵥ* Bm + pB ᵥ* D = pB) (hN : (1 - D) * N = 1) (hprob : ∑ i, pS i + ∑ b, pB b = 1) :
    ∑ i, pS i * (1 + (Bm *ᵥ (N *ᵥ 1)) i) = 1 := by
  have e0 : pS ⬝ᵥ (Bm *ᵥ (N *ᵥ 1)) = pB ⬝ᵥ 1 := by
    rw [dotProduct_mulVec, dotProduct_mulVec, ← piB_eq Bm D N pS pB h2 hN]
  have e : ∑ i, pS i * (Bm *ᵥ (N *ᵥ 1)) i = ∑ b, pB b := by
    simpa [dotProduct] using e0
  simp only [mul_add, mul_one, sum_add_distrib, e, hprob]

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Kac-type identity: under the stated block stationarity, `(1 − D) N = 1`, total mass 1 and `π(S)
  > 0`, the `π_S/π(S)`-average of `1 + (B N 𝟙)ᵢ` equals `1/π(S)`. (Reading this as the mean return
  time uses the CITED Kemeny–Snell identification; see `kac_sum`.) -/
@[nolint unusedArguments]
theorem kac (Bm : Matrix S B ℝ) (D N : Matrix B B ℝ) (pS : S → ℝ) (pB : B → ℝ)
    (h2 : pS ᵥ* Bm + pB ᵥ* D = pB) (hN : (1 - D) * N = 1) (hprob : ∑ i, pS i + ∑ b, pB b = 1)
    (hpos : 0 < ∑ i, pS i) :
    ∑ i, (pS i / ∑ k, pS k) * (1 + (Bm *ᵥ (N *ᵥ 1)) i) = 1 / ∑ k, pS k := by
  have := kac_sum Bm D N pS pB h2 hN hprob
  calc _ = (∑ i, pS i * (1 + (Bm *ᵥ (N *ᵥ 1)) i)) / ∑ k, pS k := by
          rw [sum_div]; exact sum_congr rfl fun i _ => by ring
    _ = 1 / ∑ k, pS k := by rw [this]

/-! ### Commute times for the *Traces* §7 example (uniform 3 colours; trace on {r, g}) -/

/-- Original chain, all transitions 1/3. The hitting-time equations for target `g` (unknowns `hr`, `hb`) force
`hr = 3`, so the commute time r ↔ g is 6 (by symmetry). -/
theorem commute_original (hr hb : ℝ) (e1 : hr = 1 + (1/3) * hr + (1/3) * hb) (e2 : hb = 1 + (1/3) * hr + (1/3) * hb) :
    hr = 3 ∧ hr + hr = 6 := by constructor <;> linarith

/-- The trace on {r, g} has all transitions 1/2 (`Tr = 1/3 + (1/3)(3/2)(1/3)`), so the hitting time is 2 and the
commute time is 4. Ratio 4/6 = 2/3 = π(S): one Kac factor (*Traces*' "dilation" and "contraction" alike). -/
theorem commute_trace (h : ℝ) (e : h = 1 + (1/3 + (1/3) * (1 - 1/3)⁻¹ * (1/3)) * h) :
    (1/3 + (1/3) * (1 - 1/3)⁻¹ * (1/3) : ℝ) = 1/2 ∧ h = 2 ∧ (h + h) / 6 = 2/3 := by
  norm_num at e ⊢; refine ⟨by linarith, by linarith⟩

/-! ## (c) The corrected bound, one eliminated state -/

/-- Subadditivity of `−x log x` on `[0, ∞)`. -/
lemma negMulLog_add_le {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) :
    negMulLog (x + y) ≤ negMulLog x + negMulLog y := by
  rcases hx.eq_or_lt with rfl | hx'
  · simp
  rcases hy.eq_or_lt with rfl | hy'
  · simp
  simp only [negMulLog]
  have h1 : log x ≤ log (x + y) := Real.log_le_log hx' (by linarith)
  have h2 : log y ≤ log (x + y) := Real.log_le_log hy' (by linarith)
  nlinarith [mul_le_mul_of_nonneg_left h1 hx, mul_le_mul_of_nonneg_left h2 hy]

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- Grouping: `Σⱼ η(u qⱼ) = η(u) + u Σⱼ η(qⱼ)` when `Σ q = 1`. -/
@[nolint unusedArguments]
lemma sum_negMulLog_mul (u : ℝ) (q : S → ℝ) (hq : ∑ j, q j = 1) :
    ∑ j, negMulLog (u * q j) = negMulLog u + u * ∑ j, negMulLog (q j) := by
  simp only [negMulLog_mul, sum_add_distrib, ← sum_mul, ← mul_sum, hq, one_mul]

/-- **(c) One-state elimination.** For a chain on `S ⊔ {b}` with rows `(A i ·, u i)` and `(w, d)` and stationary
weights `π`, `pb` (only the b-balance `Σ πᵢ uᵢ + pb d = pb` is needed), the trace `Tr = A + u wᵀ/(1 − d)` satisfies
`Σ_{i∈S} πᵢ H(Trᵢ) ≤ h(P)`, i.e. **π(S)·h(Tr) ≤ h(P)**. This is the per-original-step correction of the *Traces*
conjecture. -/
theorem one_state_elimination (A : S → S → ℝ) (u w : S → ℝ) (d : ℝ) (pr : S → ℝ) (pb : ℝ)
    (hA : ∀ i j, 0 ≤ A i j) (hu : ∀ i, 0 ≤ u i) (hw : ∀ j, 0 ≤ w j) (hd0 : 0 ≤ d) (hd1 : d < 1)
    (hpr : ∀ i, 0 ≤ pr i) (hpb : 0 ≤ pb) (hwsum : ∑ j, w j + d = 1)
    (hbal : ∑ i, pr i * u i + pb * d = pb) :
    ∑ i, pr i * ∑ j, negMulLog (A i j + u i * (w j / (1 - d)))
      ≤ ∑ i, pr i * (∑ j, negMulLog (A i j) + negMulLog (u i)) + pb * (∑ j, negMulLog (w j) + negMulLog d) := by
  set q : S → ℝ := fun j => w j / (1 - d) with hqdef
  have h1d : 0 < 1 - d := by linarith
  have hq0 : ∀ j, 0 ≤ q j := fun j => div_nonneg (hw j) h1d.le
  have hq : ∑ j, q j = 1 := by
    simp only [hqdef, ← sum_div]; rw [div_eq_one_iff_eq h1d.ne']; linarith
  set H := ∑ j, negMulLog (q j)
  -- row bound
  have hrow : ∀ i, ∑ j, negMulLog (A i j + u i * q j) ≤ ∑ j, negMulLog (A i j) + negMulLog (u i) + u i * H := by
    intro i
    calc ∑ j, negMulLog (A i j + u i * q j) ≤ ∑ j, (negMulLog (A i j) + negMulLog (u i * q j)) :=
          sum_le_sum fun j _ => negMulLog_add_le (hA i j) (mul_nonneg (hu i) (hq0 j))
      _ = ∑ j, negMulLog (A i j) + negMulLog (u i) + u i * H := by
          rw [sum_add_distrib, sum_negMulLog_mul (u i) q hq]; ring
  have hsum : ∑ i, pr i * ∑ j, negMulLog (A i j + u i * q j)
      ≤ ∑ i, pr i * (∑ j, negMulLog (A i j) + negMulLog (u i)) + (∑ i, pr i * u i) * H := by
    rw [sum_mul, ← sum_add_distrib]
    exact sum_le_sum fun i _ => by nlinarith [mul_le_mul_of_nonneg_left (hrow i) (hpr i)]
  -- b-row entropy dominates pb (1 − d) H
  have hw' : ∀ j, w j = (1 - d) * q j := fun j => by simp [hqdef]; field_simp
  have hbrow : ∑ j, negMulLog (w j) = negMulLog (1 - d) + (1 - d) * H := by
    simp only [hw']; exact sum_negMulLog_mul (1 - d) q hq
  have hn1 : 0 ≤ negMulLog (1 - d) := negMulLog_nonneg h1d.le (by linarith)
  have hn2 : 0 ≤ negMulLog d := negMulLog_nonneg hd0 hd1.le
  have hbalu : ∑ i, pr i * u i = pb * (1 - d) := by linarith
  have hH : 0 ≤ H := sum_nonneg fun j _ => negMulLog_nonneg (hq0 j)
      (by have := single_le_sum (fun k _ => hq0 k) (mem_univ j); linarith)
  calc _ = ∑ i, pr i * ∑ j, negMulLog (A i j + u i * q j) := rfl
    _ ≤ _ := hsum
    _ ≤ _ := by
        rw [hbalu, hbrow]
        nlinarith [mul_nonneg hpb hn1, mul_nonneg hpb hn2]

end PositiveGeometryEmergentSpaceTime.MarkovTrace
