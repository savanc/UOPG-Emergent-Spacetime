/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
LEAN-CERT-1 (prereg/LEAN-CERT-1-certificate-upgrade-2026-10-23.md; run LEANCERT1-2026-10-23-r1).
Sketch-and-verify certificate checker: integer certificates (P, Q, d) computed outside Lean by exact
rref after a mod-p rank sketch (sims/leancert1/leancert1_checker.py), CHECKED here by kernel `decide`
(no native_decide) on structurally recursive Bool folds, and turned into statements over ℚ by the
once-proved soundness theorems `kernel_char`, `leftInv_injective`, `affine_char`.
  checkZero  : M * K = 0
  checkSplit : P * M + K * Q = d • 1
  checkInj   : Q * K = d • 1
T0 (known-result reproduction, ABHY 1711.09102 eq. 5, 6, 10): ker(eq.5 conservation) = range(eq.10 X → s),
   the eq.10 map is injective, finrank = n(n-3)/2 for n = 5, 6 (n = 7 size probe).
T1 (upgrade): GRADED-POSITROID N_ACC = 2 on R⁴, R = {p/q : |p| ≤ 10, 1 ≤ q ≤ 10}, yQ = 1.
Matrix literals pasted verbatim from sims/leancert1/certs_lean.txt.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.LeanCert

open Matrix

/-! ## Computable folds and Bool checkers -/

/-- Structurally recursive sum over `Fin n` (kernel-reducible). -/
def sumFin : (n : ℕ) → (Fin n → ℤ) → ℤ
  | 0, _ => 0
  | n + 1, f => f 0 + sumFin n (fun i => f i.succ)

/-- `sumFin n f` equals the Finset sum `∑ i, f i`. -/
theorem sumFin_eq : ∀ (n : ℕ) (f : Fin n → ℤ), sumFin n f = ∑ i, f i
  | 0, f => by simp [sumFin]
  | n + 1, f => by rw [sumFin, sumFin_eq n, Fin.sum_univ_succ]

/-- Structurally recursive conjunction over `Fin n`. -/
def allFin : (n : ℕ) → (Fin n → Bool) → Bool
  | 0, _ => true
  | n + 1, f => f 0 && allFin n (fun i => f i.succ)

/-- `allFin n f = true` iff `f i = true` for every `i`. -/
theorem allFin_iff : ∀ (n : ℕ) (f : Fin n → Bool), allFin n f = true ↔ ∀ i, f i = true
  | 0, f => by simp [allFin]
  | n + 1, f => by rw [allFin, Bool.and_eq_true, allFin_iff n, Fin.forall_fin_succ]

variable {m n k : ℕ}

/-- Entry (i, j) of A * B via `sumFin`. -/
def mulE {o : ℕ} (A : Matrix (Fin m) (Fin n) ℤ) (B : Matrix (Fin n) (Fin o) ℤ) (i : Fin m) (j : Fin o) : ℤ :=
  sumFin n (fun l => A i l * B l j)

/-- `mulE A B i j` is the `(i, j)` entry of `A * B`. -/
theorem mulE_eq {o : ℕ} (A : Matrix (Fin m) (Fin n) ℤ) (B : Matrix (Fin n) (Fin o) ℤ) (i : Fin m) (j : Fin o) :
    mulE A B i j = (A * B) i j := by
  simp [mulE, sumFin_eq, Matrix.mul_apply]

/-- Boolean check that `M * K = 0` (computed with `mulE`, kernel-reducible). -/
def checkZero (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ) : Bool :=
  allFin m (fun i => allFin k (fun j => mulE M K i j == 0))

/-- Boolean check that `P * M + K * Q = d • 1`. -/
def checkSplit (P : Matrix (Fin n) (Fin m) ℤ) (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ)
    (Q : Matrix (Fin k) (Fin n) ℤ) (d : ℤ) : Bool :=
  allFin n (fun i => allFin n (fun j => mulE P M i j + mulE K Q i j == if i = j then d else 0))

/-- Boolean check that `Q * K = d • 1`. -/
def checkInj (Q : Matrix (Fin k) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ) (d : ℤ) : Bool :=
  allFin k (fun a => allFin k (fun b => mulE Q K a b == if a = b then d else 0))

/-- Boolean entrywise equality of two integer matrices. -/
def checkEq (A B : Matrix (Fin m) (Fin n) ℤ) : Bool :=
  allFin m (fun i => allFin n (fun j => A i j == B i j))

/-- `checkZero M K = true` iff `M * K = 0`. -/
theorem checkZero_spec (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ) :
    checkZero M K = true ↔ M * K = 0 := by
  simp only [checkZero, allFin_iff, beq_iff_eq, mulE_eq]
  constructor
  · intro h; ext i j; simpa using h i j
  · intro h i j; simp [h]

/-- `checkSplit P M K Q d = true` iff `P * M + K * Q = d • 1`. -/
theorem checkSplit_spec (P : Matrix (Fin n) (Fin m) ℤ) (M : Matrix (Fin m) (Fin n) ℤ)
    (K : Matrix (Fin n) (Fin k) ℤ) (Q : Matrix (Fin k) (Fin n) ℤ) (d : ℤ) :
    checkSplit P M K Q d = true ↔ P * M + K * Q = d • (1 : Matrix (Fin n) (Fin n) ℤ) := by
  simp only [checkSplit, allFin_iff, beq_iff_eq, mulE_eq]
  constructor
  · intro h; ext i j; have := h i j; simp only [Matrix.add_apply, Matrix.smul_apply,
      Matrix.one_apply] at this ⊢
    rw [this]; try (split_ifs <;> simp)
  · intro h i j; rw [← Matrix.add_apply, h]; simp only [Matrix.smul_apply, Matrix.one_apply,
      smul_eq_mul]
    split_ifs <;> simp

/-- `checkInj Q K d = true` iff `Q * K = d • 1`. -/
theorem checkInj_spec (Q : Matrix (Fin k) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ) (d : ℤ) :
    checkInj Q K d = true ↔ Q * K = d • (1 : Matrix (Fin k) (Fin k) ℤ) := by
  simp only [checkInj, allFin_iff, beq_iff_eq, mulE_eq]
  constructor
  · intro h; ext i j; rw [h i j]; simp only [Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
    split_ifs <;> simp
  · intro h i j; rw [h]; simp only [Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
    split_ifs <;> simp

/-- `checkEq A B = true` iff `A = B`. -/
theorem checkEq_spec (A B : Matrix (Fin m) (Fin n) ℤ) : checkEq A B = true ↔ A = B := by
  simp only [checkEq, allFin_iff, beq_iff_eq]
  exact ⟨fun h => Matrix.ext h, fun h i j => by rw [h]⟩

/-! ## Soundness over ℚ -/

/-- Cast an integer matrix to ℚ. -/
abbrev cq {a b : ℕ} (A : Matrix (Fin a) (Fin b) ℤ) : Matrix (Fin a) (Fin b) ℚ := A.map (Int.castRingHom ℚ)

/-- `cq` commutes with matrix multiplication. -/
theorem cq_mul {o : ℕ} (A : Matrix (Fin m) (Fin n) ℤ) (B : Matrix (Fin n) (Fin o) ℤ) :
    cq (A * B) = cq A * cq B := Matrix.map_mul

/-- `cq (d • 1) = (d : ℚ) • 1`. -/
theorem cq_smul_one (d : ℤ) : cq (d • (1 : Matrix (Fin n) (Fin n) ℤ)) = (d : ℚ) • (1 : Matrix (Fin n) (Fin n) ℚ) := by
  ext i j; simp only [cq, Matrix.map_apply, Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  split_ifs <;> simp

/-- `cq` commutes with addition. -/
theorem cq_add (A B : Matrix (Fin m) (Fin n) ℤ) : cq (A + B) = cq A + cq B := by
  ext i j; simp

/-- **Soundness.** A verified split certificate characterises the rational kernel of M as the image
  of K. -/
theorem kernel_char (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ)
    (P : Matrix (Fin n) (Fin m) ℤ) (Q : Matrix (Fin k) (Fin n) ℤ) (d : ℤ) (hd : d ≠ 0)
    (hz : checkZero M K = true) (hs : checkSplit P M K Q d = true) (x : Fin n → ℚ) :
    cq M *ᵥ x = 0 ↔ ∃ t, x = cq K *ᵥ t := by
  have hz' : cq M * cq K = 0 := by rw [← cq_mul, (checkZero_spec M K).1 hz]; ext; simp
  have hs' : cq P * cq M + cq K * cq Q = (d : ℚ) • (1 : Matrix (Fin n) (Fin n) ℚ) := by
    rw [← cq_mul, ← cq_mul, ← cq_add, (checkSplit_spec P M K Q d).1 hs, cq_smul_one]
  have hdq : (d : ℚ) ≠ 0 := by exact_mod_cast hd
  constructor
  · intro hx
    refine ⟨(d : ℚ)⁻¹ • (cq Q *ᵥ x), ?_⟩
    have h1 := congrArg (fun A => A *ᵥ x) hs'
    simp only [Matrix.add_mulVec, ← Matrix.mulVec_mulVec, hx, Matrix.mulVec_zero, zero_add,
      Matrix.smul_mulVec, Matrix.one_mulVec] at h1
    rw [Matrix.mulVec_smul, h1, smul_smul, inv_mul_cancel₀ hdq, one_smul]
  · rintro ⟨t, rfl⟩
    rw [Matrix.mulVec_mulVec, hz', Matrix.zero_mulVec]

/-- **Soundness.** A verified left-inverse certificate makes K injective over ℚ. -/
theorem leftInv_injective (Q : Matrix (Fin k) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ) (d : ℤ) (hd : d ≠ 0)
    (hi : checkInj Q K d = true) : Function.Injective (fun t : Fin k → ℚ => cq K *ᵥ t) := by
  have hi' : cq Q * cq K = (d : ℚ) • (1 : Matrix (Fin k) (Fin k) ℚ) := by
    rw [← cq_mul, (checkInj_spec Q K d).1 hi, cq_smul_one]
  have hdq : (d : ℚ) ≠ 0 := by exact_mod_cast hd
  intro s t hst
  have h := congrArg (fun v => cq Q *ᵥ v) hst
  simp only [Matrix.mulVec_mulVec, hi', Matrix.smul_mulVec, Matrix.one_mulVec] at h
  exact smul_right_injective _ hdq h

/-- **Soundness, affine form.** With a particular solution x0 (M x0 = b), solutions of M x = b are
  x0 + K t. -/
theorem affine_char (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ)
    (P : Matrix (Fin n) (Fin m) ℤ) (Q : Matrix (Fin k) (Fin n) ℤ) (d : ℤ) (hd : d ≠ 0)
    (hz : checkZero M K = true) (hs : checkSplit P M K Q d = true)
    (x0 x : Fin n → ℚ) (b' : Fin m → ℚ) (h0 : cq M *ᵥ x0 = b') :
    cq M *ᵥ x = b' ↔ ∃ t, x = x0 + cq K *ᵥ t := by
  have key := kernel_char M K P Q d hd hz hs (x - x0)
  rw [Matrix.mulVec_sub, h0, sub_eq_zero] at key
  rw [key]
  constructor
  · rintro ⟨t, ht⟩; exact ⟨t, by rw [← ht]; abel⟩
  · rintro ⟨t, ht⟩; exact ⟨t, by rw [ht]; abel⟩

/-- Kernel = range as ℚ-submodules, plus finrank, from a full certificate. -/
theorem ker_eq_range (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ)
    (P : Matrix (Fin n) (Fin m) ℤ) (Q : Matrix (Fin k) (Fin n) ℤ) (d : ℤ) (hd : d ≠ 0)
    (hz : checkZero M K = true) (hs : checkSplit P M K Q d = true) :
    LinearMap.ker (cq M).mulVecLin = LinearMap.range (cq K).mulVecLin := by
  ext x
  simp only [LinearMap.mem_ker, LinearMap.mem_range, Matrix.mulVecLin_apply]
  rw [kernel_char M K P Q d hd hz hs x]
  exact ⟨fun ⟨t, ht⟩ => ⟨t, ht.symm⟩, fun ⟨t, ht⟩ => ⟨t, ht.symm⟩⟩

/-- If all three checks pass and `d ≠ 0`, the rational kernel of `M` has dimension `k` (the number
  of columns of `K`). -/
theorem finrank_ker (M : Matrix (Fin m) (Fin n) ℤ) (K : Matrix (Fin n) (Fin k) ℤ)
    (P : Matrix (Fin n) (Fin m) ℤ) (Q : Matrix (Fin k) (Fin n) ℤ) (d : ℤ) (hd : d ≠ 0)
    (hz : checkZero M K = true) (hs : checkSplit P M K Q d = true) (hi : checkInj Q K d = true) :
    Module.finrank ℚ (LinearMap.ker (cq M).mulVecLin) = k := by
  rw [ker_eq_range M K P Q d hd hz hs, LinearMap.finrank_range_of_inj]
  · simp
  · exact leftInv_injective Q K d hd hi

/-! ## Certificates (verbatim from sims/leancert1/certs_lean.txt, run LEANCERT1-2026-10-23-r1) -/
/-- Certificate data for the ABHY n = 5 kinematic space (eq. (5) map): the constraint matrix `M`, a
  5×10 integer matrix. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def abhy5_M : Matrix (Fin 5) (Fin 10) ℤ := !![1, 1, 1, 1, 0, 0, 0, 0, 0, 0; 1, 0, 0, 0, 1, 1, 1, 0,
    0, 0; 0, 1, 0, 0, 1, 0, 0, 1, 1, 0; 0, 0, 1, 0, 0, 1, 0, 1, 0, 1; 0, 0, 0, 1, 0, 0, 1, 0, 1, 1]
/-- Certificate data for the ABHY n = 5 kinematic space (eq. (5) map): the kernel-basis matrix `K`
  (columns span ker M), a 10×5 integer matrix. Emitted verbatim by the generator; correctness is
  only what the `_cert` theorem checks. -/
def abhy5_K : Matrix (Fin 10) (Fin 5) ℤ := !![1, 0, 0, 0, 0; -1, 1, -1, 0, 0; 0, -1, 1, -1, 0; 0, 0,
    0, 1, 0; 0, 0, 1, 0, 0; 0, 0, -1, 1, -1; -1, 0, 0, -1, 1; 0, 0, 0, 0, 1; 1, -1, 0, 0, -1; 0, 1,
    0, 0, 0]
/-- Certificate data for the ABHY n = 5 kinematic space (eq. (5) map): the splitting matrix `P`
  (with `Q`: `P·M + K·Q = d•1`), a 10×5 integer matrix. Emitted verbatim by the generator;
  correctness is only what the `_cert` theorem checks. -/
def abhy5_P : Matrix (Fin 10) (Fin 5) ℤ := !![0, 0, 0, 0, 0; 0, 0, 0, 0, 0; 0, 0, 0, 0, 0; 2, 0, 0,
    0, 0; 0, 0, 0, 0, 0; 0, 0, 0, 0, 0; 0, 2, 0, 0, 0; 1, 1, 1, 1, -1; -1, -1, 1, -1, 1; -1, -1, -1,
    1, 1]
/-- Certificate data for the ABHY n = 5 kinematic space (eq. (5) map): the left-inverse matrix `Q`
  (`Q·K = d•1`), a 5×10 integer matrix. Emitted verbatim by the generator; correctness is only
  what the `_cert` theorem checks. -/
def abhy5_Q : Matrix (Fin 5) (Fin 10) ℤ := !![2, 0, 0, 0, 0, 0, 0, 0, 0, 0; 2, 2, 0, 0, 2, 0, 0, 0,
    0, 0; 0, 0, 0, 0, 2, 0, 0, 0, 0, 0; -2, -2, -2, 0, 0, 0, 0, 0, 0, 0; -2, -2, -2, 0, -2, -2, 0,
    0, 0, 0]
/-- Certificate data for the ABHY n = 5 kinematic space (eq. (5) map): the nonzero integer scale `d`
  of the certificate. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def abhy5_d : ℤ := 2

/-- Certificate data for the ABHY n = 6 kinematic space (eq. (5) map): the constraint matrix `M`, a
  6×15 integer matrix. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def abhy6_M : Matrix (Fin 6) (Fin 15) ℤ := !![1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 1, 0, 0,
    0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0; 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0; 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 0; 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1; 0, 0, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1]
/-- Certificate data for the ABHY n = 6 kinematic space (eq. (5) map): the kernel-basis matrix `K`
  (columns span ker M), a 15×9 integer matrix. Emitted verbatim by the generator; correctness is
  only what the `_cert` theorem checks. -/
def abhy6_K : Matrix (Fin 15) (Fin 9) ℤ := !![1, 0, 0, 0, 0, 0, 0, 0, 0; -1, 1, 0, -1, 0, 0, 0, 0,
    0; 0, -1, 1, 1, -1, 0, 0, 0, 0; 0, 0, -1, 0, 1, -1, 0, 0, 0; 0, 0, 0, 0, 0, 1, 0, 0, 0; 0, 0, 0,
    1, 0, 0, 0, 0, 0; 0, 0, 0, -1, 1, 0, -1, 0, 0; 0, 0, 0, 0, -1, 1, 1, -1, 0; -1, 0, 0, 0, 0, -1,
    0, 1, 0; 0, 0, 0, 0, 0, 0, 1, 0, 0; 0, 0, 0, 0, 0, 0, -1, 1, -1; 1, -1, 0, 0, 0, 0, 0, -1, 1; 0,
    0, 0, 0, 0, 0, 0, 0, 1; 0, 1, -1, 0, 0, 0, 0, 0, -1; 0, 0, 1, 0, 0, 0, 0, 0, 0]
/-- Certificate data for the ABHY n = 6 kinematic space (eq. (5) map): the splitting matrix `P`
  (with `Q`: `P·M + K·Q = d•1`), a 15×6 integer matrix. Emitted verbatim by the generator;
  correctness is only what the `_cert` theorem checks. -/
def abhy6_P : Matrix (Fin 15) (Fin 6) ℤ := !![0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0,
    0; 0, 0, 0, 0, 0, 0; 2, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0; 0,
    2, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0; 0, 0, 2, 0, 0, 0; 1, 1, 1, 1, 1, -1; -1, -1,
    -1, 1, -1, 1; -1, -1, -1, -1, 1, 1]
/-- Certificate data for the ABHY n = 6 kinematic space (eq. (5) map): the left-inverse matrix `Q`
  (`Q·K = d•1`), a 9×15 integer matrix. Emitted verbatim by the generator; correctness is only
  what the `_cert` theorem checks. -/
def abhy6_Q : Matrix (Fin 9) (Fin 15) ℤ := !![2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 2, 2, 0,
    0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0; 2, 2, 2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0,
    2, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0; -2, -2, -2, -2, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0; -2, -2, -2, -2, 0, -2,
    -2, -2, 0, 0, 0, 0, 0, 0, 0; -2, -2, -2, -2, 0, -2, -2, -2, 0, -2, -2, 0, 0, 0, 0]
/-- Certificate data for the ABHY n = 6 kinematic space (eq. (5) map): the nonzero integer scale `d`
  of the certificate. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def abhy6_d : ℤ := 2

/-- Certificate data for the ABHY n = 7 kinematic space (eq. (5) map): the constraint matrix `M`, a
  7×21 integer matrix. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def abhy7_M : Matrix (Fin 7) (Fin 21) ℤ := !![1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0; 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 1, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0; 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0,
    0, 0; 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0; 0, 0, 0, 0, 1, 0, 0, 0, 0,
    1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1; 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1,
    1]
/-- Certificate data for the ABHY n = 7 kinematic space (eq. (5) map): the kernel-basis matrix `K`
  (columns span ker M), a 21×14 integer matrix. Emitted verbatim by the generator; correctness is
  only what the `_cert` theorem checks. -/
def abhy7_K : Matrix (Fin 21) (Fin 14) ℤ := !![1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; -1, 1, 0,
    0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, -1, 1, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, -1, 1, 0, 1,
    -1, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, -1, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0; 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, -1, 1, 0, 0, -1, 0, 0, 0,
    0, 0; 0, 0, 0, 0, 0, -1, 1, 0, 1, -1, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, -1, 1, 0, 1, -1, 0, 0,
    0; -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0; 0, 0,
    0, 0, 0, 0, 0, 0, -1, 1, 0, -1, 0, 0; 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 1, -1, 0; 1, -1, 0, 0,
    0, 0, 0, 0, 0, 0, -1, 0, 1, 0; 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0; 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, -1, 1, -1; 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1; 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1; 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1; 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
/-- Certificate data for the ABHY n = 7 kinematic space (eq. (5) map): the splitting matrix `P`
  (with `Q`: `P·M + K·Q = d•1`), a 21×7 integer matrix. Emitted verbatim by the generator;
  correctness is only what the `_cert` theorem checks. -/
def abhy7_P : Matrix (Fin 21) (Fin 7) ℤ := !![0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0,
    0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 2, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0,
    0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 2, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0,
    0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 0, 2, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0; 0, 0,
    0, 0, 0, 0, 0; 0, 0, 0, 2, 0, 0, 0; 1, 1, 1, 1, 1, 1, -1; -1, -1, -1, -1, 1, -1, 1; -1, -1, -1,
    -1, -1, 1, 1]
/-- Certificate data for the ABHY n = 7 kinematic space (eq. (5) map): the left-inverse matrix `Q`
  (`Q·K = d•1`), a 14×21 integer matrix. Emitted verbatim by the generator; correctness is only
  what the `_cert` theorem checks. -/
def abhy7_Q : Matrix (Fin 14) (Fin 21) ℤ := !![2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0; 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 2, 2, 2, 0, 0, 0, 2, 2,
    0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0; 2, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0,
    0, 0; 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 2, 2, 0,
    0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0,
    0; -2, -2, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0,
    0, 0; -2, -2, -2, -2, -2, 0, -2, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0; 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0; -2, -2, -2, -2, -2, 0, -2, -2, -2, -2, 0, -2, -2,
    -2, 0, 0, 0, 0, 0, 0, 0; -2, -2, -2, -2, -2, 0, -2, -2, -2, -2, 0, -2, -2, -2, 0, -2, -2, 0, 0,
    0, 0]
/-- Certificate data for the ABHY n = 7 kinematic space (eq. (5) map): the nonzero integer scale `d`
  of the certificate. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def abhy7_d : ℤ := 2

/-- Certificate data for the GPOS linear anomaly system: the constraint matrix `M`, a 3×4 integer
  matrix. Emitted verbatim by the generator; correctness is only what the `_cert` theorem checks. -/
def gpos_M : Matrix (Fin 3) (Fin 4) ℤ := !![3, 3, 2, 1; 0, 0, 1, 0; 1, 1, 0, 0]
/-- Certificate data for the GPOS linear anomaly system: the kernel-basis matrix `K` (columns span
  ker M), a 4×1 integer matrix. Emitted verbatim by the generator; correctness is only what the
  `_cert` theorem checks. -/
def gpos_K : Matrix (Fin 4) (Fin 1) ℤ := !![-1; 1; 0; 0]
/-- Certificate data for the GPOS linear anomaly system: the splitting matrix `P` (with `Q`: `P·M +
  K·Q = d•1`), a 4×3 integer matrix. Emitted verbatim by the generator; correctness is only what
  the `_cert` theorem checks. -/
def gpos_P : Matrix (Fin 4) (Fin 3) ℤ := !![0, 0, 0; 0, 0, 1; 0, 1, 0; 1, -2, -3]
/-- Certificate data for the GPOS linear anomaly system: the left-inverse matrix `Q` (`Q·K = d•1`),
  a 1×4 integer matrix. Emitted verbatim by the generator; correctness is only what the `_cert`
  theorem checks. -/
def gpos_Q : Matrix (Fin 1) (Fin 4) ℤ := !![-1, 0, 0, 0]
/-- Certificate data for the GPOS linear anomaly system: the nonzero integer scale `d` of the
  certificate. Emitted verbatim by the generator; correctness is only what the `_cert` theorem
  checks. -/
def gpos_d : ℤ := 1

/-- Particular integer solution `x₀ = (−2, 0, −3, 6)` of the GPOS linear system (`gpos_x0_sol`). -/
def gpos_x0 : Fin 4 → ℤ := ![-2, 0, -3, 6]

/-! ## T0: ABHY kinematic space, matrices regenerated in Lean from eq. (5) and eq. (10) -/

/-- Mandelstam labels (i, j), 1 ≤ i < j ≤ n, lexicographic. -/
def pairsList (n : ℕ) : List (ℕ × ℕ) :=
  (List.range' 1 n).flatMap fun i => (List.range' (i + 1) (n - i)).map fun j => (i, j)

/-- Planar variables X_ab: b ≥ a + 2, (a, b) ≠ (1, n), lexicographic. -/
def diagsList (n : ℕ) : List (ℕ × ℕ) :=
  (pairsList n).filter fun p => decide (p.1 + 2 ≤ p.2) && !(p.1 == 1 && p.2 == n)

/-- Cyclic label in 1..n. -/
def cyc (n a : ℕ) : ℕ := (a + n - 1) % n + 1

/-- Coefficient of the planar variable `dg` in X_{a,b} (0 for adjacent / X_{1n} / X_{aa}). -/
def Xcoef (n : ℕ) (dg : ℕ × ℕ) (a b : ℕ) : ℤ :=
  if (min (cyc n a) (cyc n b), max (cyc n a) (cyc n b)) = dg then 1 else 0

/-- ABHY eq. (10): s_ij = X_{i,j+1} + X_{i+1,j} − X_{i,j} − X_{i+1,j+1}. -/
def eq10 (n N D : ℕ) : Matrix (Fin N) (Fin D) ℤ := fun i j =>
  let p := (pairsList n).getD i (0, 0); let dg := (diagsList n).getD j (0, 0)
  Xcoef n dg p.1 (p.2 + 1) + Xcoef n dg (p.1 + 1) p.2 - Xcoef n dg p.1 p.2 - Xcoef n dg (p.1 + 1) (p.2 + 1)

/-- ABHY eq. (5): row i is Σ_{j ≠ i} s_ij. -/
def eq5 (n N : ℕ) : Matrix (Fin n) (Fin N) ℤ := fun i q =>
  let p := (pairsList n).getD q (0, 0)
  if p.1 = i.val + 1 ∨ p.2 = i.val + 1 then 1 else 0

/-- The stored n = 5 matrices equal the ones regenerated in Lean: `abhy5_M = eq5 5 10` and `abhy5_K
  = eq10 5 10 5`. -/
theorem abhy5_matrices : abhy5_M = eq5 5 10 ∧ abhy5_K = eq10 5 10 5 := by
  rw [← checkEq_spec, ← checkEq_spec]; decide +kernel

/-- The stored n = 6 matrices equal the ones regenerated in Lean: `abhy6_M = eq5 6 15` and `abhy6_K
  = eq10 6 15 9`. -/
theorem abhy6_matrices : abhy6_M = eq5 6 15 ∧ abhy6_K = eq10 6 15 9 := by
  rw [← checkEq_spec, ← checkEq_spec]; decide +kernel

/-- Kernel check (`decide`) that the n = 5 certificate passes `checkZero`, `checkSplit` and
  `checkInj`; with `finrank_ker` this gives dim ker(eq5 5) = 5 over ℚ. -/
theorem abhy5_cert : checkZero abhy5_M abhy5_K = true ∧ checkSplit abhy5_P abhy5_M abhy5_K abhy5_Q abhy5_d = true ∧
    checkInj abhy5_Q abhy5_K abhy5_d = true := by decide +kernel

/-- Kernel check (`decide`) that the n = 6 certificate passes `checkZero`, `checkSplit` and
  `checkInj`; with `finrank_ker` this gives dim ker(eq5 6) = 9 over ℚ. -/
theorem abhy6_cert : checkZero abhy6_M abhy6_K = true ∧ checkSplit abhy6_P abhy6_M abhy6_K abhy6_Q abhy6_d = true ∧
    checkInj abhy6_Q abhy6_K abhy6_d = true := by decide +kernel

/-- Held-out consequence, PROVED: eq. (10) solves eq. (5) (momentum conservation), n = 6. -/
theorem abhy6_conservation : eq5 6 15 * eq10 6 15 9 = 0 := by
  obtain ⟨h1, h2⟩ := abhy6_matrices; rw [← h1, ← h2]; exact (checkZero_spec _ _).1 abhy6_cert.1

/-- ABHY: the kernel of the n = 6 conservation map is exactly the image of the planar-X map. -/
theorem abhy6_kernel_eq_range :
    LinearMap.ker (cq (eq5 6 15)).mulVecLin = LinearMap.range (cq (eq10 6 15 9)).mulVecLin := by
  obtain ⟨h1, h2⟩ := abhy6_matrices; rw [← h1, ← h2]
  exact ker_eq_range _ _ _ _ _ (by decide) abhy6_cert.1 abhy6_cert.2.1

/-- ABHY: the planar X are independent (eq. 10 map injective), n = 6. -/
theorem abhy6_injective : Function.Injective (fun t : Fin 9 → ℚ => cq (eq10 6 15 9) *ᵥ t) := by
  rw [← abhy6_matrices.2]; exact leftInv_injective _ _ _ (by decide) abhy6_cert.2.2

/-- **ABHY eq. (6) reproduced, n = 6:** dim K₆ = 6·3/2 = 9. -/
theorem abhy6_finrank : Module.finrank ℚ (LinearMap.ker (cq (eq5 6 15)).mulVecLin) = 9 := by
  rw [← abhy6_matrices.1]
  exact finrank_ker _ _ _ _ _ (by decide) abhy6_cert.1 abhy6_cert.2.1 abhy6_cert.2.2

/-- **ABHY eq. (6) reproduced, n = 5:** dim K₅ = 5. -/
theorem abhy5_finrank : Module.finrank ℚ (LinearMap.ker (cq (eq5 5 10)).mulVecLin) = 5 := by
  rw [← abhy5_matrices.1]
  exact finrank_ker _ _ _ _ _ (by decide) abhy5_cert.1 abhy5_cert.2.1 abhy5_cert.2.2

/-- Planted wrong certificate: A₆ with entry (1, 0) sign-flipped is rejected by the same checker. -/
def abhy6_Kflip : Matrix (Fin 15) (Fin 9) ℤ := fun i j => if i = 1 ∧ j = 0 then -abhy6_K i j else abhy6_K i j

/-- Planted wrong answer: `checkZero` rejects the n = 6 kernel basis with one sign flipped
  (`abhy6_Kflip`). -/
theorem planted_abhy_flip_rejected : checkZero abhy6_M abhy6_Kflip = false := by decide +kernel

/-! ## T0 size probe: n = 7 (21 × 14 certificate; prereg: not a pass condition) -/

/-- The stored n = 7 matrices equal the ones regenerated in Lean: `abhy7_M = eq5 7 21` and `abhy7_K
  = eq10 7 21 14`. -/
theorem abhy7_matrices : abhy7_M = eq5 7 21 ∧ abhy7_K = eq10 7 21 14 := by
  rw [← checkEq_spec, ← checkEq_spec]; decide +kernel

/-- Kernel check (`decide`) that the n = 7 certificate passes `checkZero`, `checkSplit` and
  `checkInj`; with `finrank_ker` this gives dim ker(eq5 7) = 14 over ℚ. -/
theorem abhy7_cert : checkZero abhy7_M abhy7_K = true ∧ checkSplit abhy7_P abhy7_M abhy7_K abhy7_Q abhy7_d = true ∧
    checkInj abhy7_Q abhy7_K abhy7_d = true := by decide +kernel

/-- **ABHY eq. (6) reproduced, n = 7 (held-out size):** dim K₇ = 14. -/
theorem abhy7_finrank : Module.finrank ℚ (LinearMap.ker (cq (eq5 7 21)).mulVecLin) = 14 := by
  rw [← abhy7_matrices.1]
  exact finrank_ker _ _ _ _ _ (by decide) abhy7_cert.1 abhy7_cert.2.1 abhy7_cert.2.2

/-! ## T1: GRADED-POSITROID N_ACC = 2 (upgrade of GPOS-2026-10-22-r1 from SIMULATED to PROVED) -/

/-- The four anomaly-cancellation conditions at yQ = 1 (grav, SU(2)²U(1), SU(3)²U(1), cubic). -/
def ACC (u d l e : ℚ) : Prop :=
  6 + 3 * u + 3 * d + 2 * l + e = 0 ∧ 3 + l = 0 ∧ 2 + u + d = 0 ∧
  6 + 3 * u ^ 3 + 3 * d ^ 3 + 2 * l ^ 3 + e ^ 3 = 0

/-- `ACC` is decidable (it is a conjunction of rational equalities). -/
instance (u d l e : ℚ) : Decidable (ACC u d l e) := by unfold ACC; infer_instance

/-- GPOS domain R = {p/q : −10 ≤ p ≤ 10, 1 ≤ q ≤ 10}. -/
def R : Finset ℚ := ((Finset.Icc (-10 : ℤ) 10) ×ˢ (Finset.Icc (1 : ℤ) 10)).image fun pq => (pq.1 : ℚ) / pq.2

/-- The tuples `(u, d, l, e) ∈ R⁴` satisfying `ACC` (a finite search set). -/
def accSet : Finset (ℚ × ℚ × ℚ × ℚ) :=
  (R ×ˢ R ×ˢ R ×ˢ R).filter fun x => ACC x.1 x.2.1 x.2.2.1 x.2.2.2

/-- Kernel check (`decide`) that the GPOS certificate passes `checkZero`, `checkSplit` and
  `checkInj`. -/
theorem gpos_cert : checkZero gpos_M gpos_K = true ∧ checkSplit gpos_P gpos_M gpos_K gpos_Q gpos_d = true ∧
    checkInj gpos_Q gpos_K gpos_d = true := by decide +kernel

/-- Over ℚ, `gpos_M (u, d, l, e) = (3u + 3d + 2l + e, l, u + d)`. -/
theorem gpos_M_mulVec (u d l e : ℚ) :
    cq gpos_M *ᵥ ![u, d, l, e] = ![3 * u + 3 * d + 2 * l + e, l, u + d] := by
  ext i; fin_cases i <;> simp [cq, gpos_M, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

/-- `gpos_M x₀ = (−6, −3, −2)`. -/
theorem gpos_x0_sol : cq gpos_M *ᵥ (fun i => ((gpos_x0 i : ℤ) : ℚ)) = ![-6, -3, -2] := by
  ext i; fin_cases i <;> simp [cq, gpos_M, gpos_x0, Matrix.mulVec, dotProduct,
      Fin.sum_univ_succ] <;> norm_num

/-- **Linear ACC, through the certificate** (`affine_char`; no linarith on the system):
the three linear ACC hold iff (yu, yd, yL, ye) = (−2 − t, t, −3, 6). -/
theorem gpos_linear_iff (u d l e : ℚ) :
    (6 + 3 * u + 3 * d + 2 * l + e = 0 ∧ 3 + l = 0 ∧ 2 + u + d = 0) ↔
      ∃ t : ℚ, u = -2 - t ∧ d = t ∧ l = -3 ∧ e = 6 := by
  have hlin : (6 + 3 * u + 3 * d + 2 * l + e = 0 ∧ 3 + l = 0 ∧ 2 + u + d = 0) ↔
      cq gpos_M *ᵥ ![u, d, l, e] = ![-6, -3, -2] := by
    rw [gpos_M_mulVec]
    simp only [funext_iff, Fin.forall_fin_succ, IsEmpty.forall_iff, and_true]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_succ]
    constructor
    · rintro ⟨h1, h2, h3⟩; exact ⟨by linear_combination h1, by linear_combination h2,
        by linear_combination h3⟩
    · rintro ⟨h1, h2, h3⟩; exact ⟨by linear_combination h1, by linear_combination h2,
        by linear_combination h3⟩
  rw [hlin,
      affine_char gpos_M gpos_K gpos_P gpos_Q gpos_d (by decide) gpos_cert.1 gpos_cert.2.1 _ _ _ gpos_x0_sol]
  constructor
  · rintro ⟨t, ht⟩
    refine ⟨t 0, ?_, ?_, ?_, ?_⟩ <;>
    [have := congrFun ht 0; have := congrFun ht 1; have := congrFun ht 2; have := congrFun ht 3] <;>
    simpa [cq, gpos_K, gpos_x0, Matrix.mulVec, dotProduct, sub_eq_add_neg, add_comm] using this
  · rintro ⟨t, hu, hd, hl, he⟩
    refine ⟨fun _ => t, ?_⟩
    ext i; fin_cases i <;> simp [cq, gpos_K, gpos_x0, Matrix.mulVec, dotProduct, hu, hd, hl,
        he] <;> ring

/-- Cubic ACC restricted to the certified line: −18 (t + 4)(t − 2). -/
theorem gpos_cubic_on_line (t : ℚ) :
    6 + 3 * (-2 - t) ^ 3 + 3 * t ^ 3 + 2 * (-3 : ℚ) ^ 3 + 6 ^ 3 = -18 * (t + 4) * (t - 2) := by ring

/-- The four anomaly conditions `ACC u d l e` hold iff `(u, d, l, e)` is `(2, −4, −3, 6)` or `(−4,
  2, −3, 6)`. -/
theorem acc_iff (u d l e : ℚ) :
    ACC u d l e ↔ (u = 2 ∧ d = -4 ∧ l = -3 ∧ e = 6) ∨ (u = -4 ∧ d = 2 ∧ l = -3 ∧ e = 6) := by
  constructor
  · rintro ⟨h1, h2, h3, h4⟩
    obtain ⟨t, hu, hd, hl, he⟩ := (gpos_linear_iff u d l e).1 ⟨h1, h2, h3⟩
    rw [hu, hd, hl, he, gpos_cubic_on_line] at h4
    have : t + 4 = 0 ∨ t - 2 = 0 := by
      rcases mul_eq_zero.1 h4 with h | h
      · exact Or.inl (by simpa using h)
      · exact Or.inr h
    rcases this with h | h
    · left; exact ⟨by rw [hu]; linarith, by rw [hd]; linarith, hl, he⟩
    · right; exact ⟨by rw [hu]; linarith, by rw [hd]; linarith, hl, he⟩
  · rintro (⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩) <;> refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num

/-- Every integer in `[−10, 10]` lies in the GPOS domain `R`. -/
theorem int_mem_R (z : ℤ) (h1 : -10 ≤ z) (h2 : z ≤ 10) : (z : ℚ) ∈ R :=
  Finset.mem_image.2 ⟨(z, 1), by simp [h1, h2], by simp⟩

/-- **N_ACC set (PROVED; was SIMULATED in GPOS-2026-10-22-r1).** -/
theorem nacc_set_eq : accSet = {(-4, 2, -3, 6), (2, -4, -3, 6)} := by
  ext ⟨u, d, l, e⟩
  simp only [accSet, Finset.mem_filter, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton,
    Prod.mk.injEq]
  constructor
  · rintro ⟨-, h⟩
    rcases (acc_iff u d l e).1 h with h | h
    · right; exact h
    · left; exact h
  · intro h
    have hacc : ACC u d l e := (acc_iff u d l e).2 (h.symm.imp id id)
    refine ⟨?_, hacc⟩
    rcases h with ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩
    · exact ⟨by exact_mod_cast int_mem_R (-4) (by norm_num) (by norm_num),
        by exact_mod_cast int_mem_R 2 (by norm_num) (by norm_num),
        by exact_mod_cast int_mem_R (-3) (by norm_num) (by norm_num),
        by exact_mod_cast int_mem_R 6 (by norm_num) (by norm_num)⟩
    · exact ⟨by exact_mod_cast int_mem_R 2 (by norm_num) (by norm_num),
        by exact_mod_cast int_mem_R (-4) (by norm_num) (by norm_num),
        by exact_mod_cast int_mem_R (-3) (by norm_num) (by norm_num),
        by exact_mod_cast int_mem_R 6 (by norm_num) (by norm_num)⟩

/-- **GPOS N_ACC = 2 (PROVED).** -/
theorem nacc_eq_two : accSet.card = 2 := by
  rw [nacc_set_eq]; exact Finset.card_pair (by norm_num)

/-! ## Planted wrong answers (must be REJECTED) -/

/-- Planted wrong kernel basis (one sign flipped) for the rejection test `planted_flip_rejected`. -/
def gpos_Kflip : Matrix (Fin 4) (Fin 1) ℤ := !![-1; -1; 0; 0]
/-- Planted wrong splitting matrix for the rejection test `planted_split_rejected`. -/
def gpos_Pbad : Matrix (Fin 4) (Fin 3) ℤ := !![1, 0, 0; 0, 0, 1; 0, 1, 0; 1, -2, -3]

/-- Planted wrong answer: `checkZero` rejects the sign-flipped kernel basis `gpos_Kflip`. -/
theorem planted_flip_rejected : checkZero gpos_M gpos_Kflip = false := by decide +kernel

/-- Planted wrong answer: `checkSplit` rejects the corrupted splitting matrix `gpos_Pbad`. -/
theorem planted_split_rejected : checkSplit gpos_Pbad gpos_M gpos_K gpos_Q gpos_d = false := by decide +kernel

/-- Planted wrong answer: `(−4, 2, −3, 7) ∉ accSet`. -/
theorem planted_tuple_rejected : ((-4 : ℚ), (2 : ℚ), (-3 : ℚ), (7 : ℚ)) ∉ accSet := by
  rw [nacc_set_eq]; simp only [Finset.mem_insert, Finset.mem_singleton, Prod.mk.injEq]; norm_num
end PositiveGeometryEmergentSpaceTime.LeanCert
