/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
LEAN-CERT-2 (prereg/LEAN-CERT-2-modp-frwzw-2026-10-28.md, run LEANCERT2-2026-10-28-r1).
List-based kernel-dimension certificates: matrices are `List (List ℤ)` (rows, or columns for the
`…c` transposes), dot products by structural recursion.  Soundness is proved once here and feeds
`PositiveGeometryEmergentSpaceTime.LeanCert.finrank_ker`.  No `sorry`, no `native_decide`.
-/
import PositiveGeometryEmergentSpaceTime.LeanCert

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.LeanCert2

open Matrix PositiveGeometryEmergentSpaceTime.LeanCert

/-! ## List matrices and the list dot product -/

/-- Dot product of two integer lists (stops at the shorter one). -/
def dotL : List ℤ → List ℤ → ℤ
  | [], _ => 0
  | _ :: _, [] => 0
  | a :: as, b :: bs => a * b + dotL as bs

/-- Matrix whose row `i` is `L[i]` (missing entries are 0). -/
def rowsM (a b : ℕ) (L : List (List ℤ)) : Matrix (Fin a) (Fin b) ℤ := fun i j => (L.getD i []).getD j 0

/-- Matrix whose column `j` is `L[j]` (missing entries are 0). -/
def colsM (a b : ℕ) (L : List (List ℤ)) : Matrix (Fin a) (Fin b) ℤ := fun i j => (L.getD j []).getD i 0

/-- Every list in `L` has length at most `n`. -/
def lenL (n : ℕ) (L : List (List ℤ)) : Bool := L.all (fun r => decide (r.length ≤ n))

/-- Entry `(i, j)` of a list product: row `i` of `A` against column `j` of `B` (given as a list). -/
def mulL (A B : List (List ℤ)) (i j : ℕ) : ℤ := dotL (A.getD i []) (B.getD j [])

/-- If `r` has length at most `n`, `dotL r c` equals the `Fin n` sum of `r[j] · c[j]` (missing
  entries read as 0). -/
theorem dotL_eq : ∀ (n : ℕ) (r c : List ℤ), r.length ≤ n →
    dotL r c = ∑ j : Fin n, r.getD j 0 * c.getD j 0
  | 0, r, c, h => by
    cases r with
    | nil => simp [dotL]
    | cons a as => simp at h
  | n + 1, r, c, h => by
    rw [Fin.sum_univ_succ]
    cases r with
    | nil => simp [dotL]
    | cons a as =>
      cases c with
      | nil => simp [dotL]
      | cons b bs =>
        simp only [List.length_cons, Nat.add_le_add_iff_right] at h
        simp [dotL, dotL_eq n as bs h]

/-- If `lenL n A`, every row `A[i]` (default `[]`) has length at most `n`. -/
theorem getD_len {n : ℕ} {A : List (List ℤ)} (h : lenL n A = true) (i : ℕ) : (A.getD i []).length ≤ n := by
  rw [List.getD_eq_getElem?_getD]
  cases hi : A[i]? with
  | none => simp
  | some r =>
    have hr : r ∈ A := List.mem_of_getElem? hi
    have := List.all_eq_true.mp h r hr
    simpa using this

/-- If the rows of `A` have length at most `n`, `mulL A B i j` is the `(i, j)` entry of `rowsM a n A
  * colsM n b B`. -/
theorem mulL_eq {a n b : ℕ} {A : List (List ℤ)} (B : List (List ℤ)) (h : lenL n A = true)
    (i : Fin a) (j : Fin b) : (rowsM a n A * colsM n b B) i j = mulL A B i j := by
  rw [Matrix.mul_apply, mulL, dotL_eq n _ _ (getD_len h i)]
  rfl

/-! ## Bool checkers and their soundness -/

/-- Boolean check that the row-list `R` and the column-list `C` describe the same `a × b` matrix. -/
def tposL (a b : ℕ) (R C : List (List ℤ)) : Bool :=
  allFin a (fun i => allFin b (fun j => (R.getD i []).getD j 0 == (C.getD j []).getD i 0))

/-- Boolean list check that `M * K = 0` (rows of `M` against columns of `K`). -/
def zeroL (m k : ℕ) (Mr Kc : List (List ℤ)) : Bool :=
  allFin m (fun i => allFin k (fun j => mulL Mr Kc i j == 0))

/-- Boolean list check that `P * M + K * Q = d • 1` (`n × n`). -/
def splitL (n : ℕ) (Pr Mc Kr Qc : List (List ℤ)) (d : ℤ) : Bool :=
  allFin n (fun i => allFin n (fun j => mulL Pr Mc i j + mulL Kr Qc i j == if i = j then d else 0))

/-- Boolean list check that `Q * K = d • 1` (`k × k`). -/
def injL (k : ℕ) (Qr Kc : List (List ℤ)) (d : ℤ) : Bool :=
  allFin k (fun a => allFin k (fun b => mulL Qr Kc a b == if a = b then d else 0))

/-- If `tposL a b R C`, then `rowsM a b R = colsM a b C`. -/
theorem tposL_spec {a b : ℕ} {R C : List (List ℤ)} (h : tposL a b R C = true) : rowsM a b R = colsM a b C := by
  simp only [tposL, allFin_iff, beq_iff_eq] at h
  ext i j; exact h i j

/-- Soundness: if the rows of `Mr` have length at most `n` and `zeroL` passes, then `rowsM Mr *
  colsM Kc = 0`. -/
theorem zeroL_spec {m n k : ℕ} {Mr Kc : List (List ℤ)} (hl : lenL n Mr = true) (h : zeroL m k Mr Kc = true) :
    checkZero (rowsM m n Mr) (colsM n k Kc) = true := by
  rw [checkZero_spec]
  simp only [zeroL, allFin_iff, beq_iff_eq] at h
  ext i j; rw [mulL_eq _ hl]; simpa using h i j

/-- Soundness: if the length checks hold and `splitL` passes, then `P * M + K * Q = d • 1` for the
  decoded matrices. -/
theorem splitL_spec {m n k : ℕ} {Pr Mc Kr Qc : List (List ℤ)} {d : ℤ} (hP : lenL m Pr = true)
    (hK : lenL k Kr = true) (h : splitL n Pr Mc Kr Qc d = true) :
    checkSplit (rowsM n m Pr) (colsM m n Mc) (rowsM n k Kr) (colsM k n Qc) d = true := by
  rw [checkSplit_spec]
  simp only [splitL, allFin_iff, beq_iff_eq] at h
  ext i j
  rw [Matrix.add_apply, mulL_eq _ hP, mulL_eq _ hK, h i j]
  simp only [Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  split_ifs <;> simp

/-- Soundness: if the length check holds and `injL` passes, then `Q * K = d • 1` for the decoded
  matrices. -/
theorem injL_spec {n k : ℕ} {Qr Kc : List (List ℤ)} {d : ℤ} (hQ : lenL n Qr = true)
    (h : injL k Qr Kc d = true) : checkInj (rowsM k n Qr) (colsM n k Kc) d = true := by
  rw [checkInj_spec]
  simp only [injL, allFin_iff, beq_iff_eq] at h
  ext i j
  rw [mulL_eq _ hQ, h i j]
  simp only [Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  split_ifs <;> simp

/-- All checks of a list certificate for `dim ker M = k` (M is `m × n`, given by rows `Mr`, columns
  `Mc`). -/
def certL (m n k : ℕ) (Mr Mc Kr Kc Pr Qr Qc : List (List ℤ)) (d : ℤ) : Bool :=
  (d != 0) && lenL n Mr && lenL m Pr && lenL k Kr && lenL n Qr &&
  tposL m n Mr Mc && tposL n k Kr Kc && tposL k n Qr Qc &&
  zeroL m k Mr Kc && splitL n Pr Mc Kr Qc d && injL k Qr Kc d

/-- **Soundness of the list certificate.** -/
theorem finrank_of_certL {m n k : ℕ} {Mr Mc Kr Kc Pr Qr Qc : List (List ℤ)} {d : ℤ}
    (h : certL m n k Mr Mc Kr Kc Pr Qr Qc d = true) :
    Module.finrank ℚ (LinearMap.ker (cq (rowsM m n Mr)).mulVecLin) = k := by
  simp only [certL, Bool.and_eq_true, bne_iff_ne, ne_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨hd, hlM⟩, hlP⟩, hlK⟩, hlQ⟩, htM⟩, htK⟩, htQ⟩, hz⟩, hs⟩, hi⟩ := h
  have hz' := zeroL_spec hlM hz
  have hs' := splitL_spec hlP hlK hs
  have hi' := injL_spec hlQ hi
  rw [← tposL_spec htM] at hs'
  rw [← tposL_spec htK] at hz' hi'
  rw [← tposL_spec htQ] at hs'
  exact finrank_ker _ _ _ _ d hd hz' hs' hi'


/-! ## Certificates (generated by sims/leancert2/emit_lean.py from the locked checker's output, run LEANCERT2-2026-10-28-r1) -/
-- abhyL5: m = 5, n = 10, k = 5
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): rows of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Mr : List (List ℤ) := [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
  [0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
  [0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
  [0, 0, 0, 1, 0, 0, 1, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): columns of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Mc : List (List ℤ) := [[1, 1, 0, 0, 0],
  [1, 0, 1, 0, 0],
  [1, 0, 0, 1, 0],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 0, 0],
  [0, 1, 0, 1, 0],
  [0, 1, 0, 0, 1],
  [0, 0, 1, 1, 0],
  [0, 0, 1, 0, 1],
  [0, 0, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): rows of `K`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Kr : List (List ℤ) := [[0, 0, 2, 2, 2],
  [2, 2, 0, 0, 2],
  [-2, 0, -2, 0, -2],
  [0, -2, 0, -2, -2],
  [-2, -2, -2, -2, -2],
  [2, 0, 0, 0, 0],
  [0, 2, 0, 0, 0],
  [0, 0, 2, 0, 0],
  [0, 0, 0, 2, 0],
  [0, 0, 0, 0, 2]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): columns of `K` (kernel
  basis). Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Kc : List (List ℤ) := [[0, 2, -2, 0, -2, 2, 0, 0, 0, 0],
  [0, 2, 0, -2, -2, 0, 2, 0, 0, 0],
  [2, 0, -2, 0, -2, 0, 0, 2, 0, 0],
  [2, 0, 0, -2, -2, 0, 0, 0, 2, 0],
  [2, 2, -2, -2, -2, 0, 0, 0, 0, 2]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): rows of `P`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Pr : List (List ℤ) := [[1, 1, -1, -1, -1],
  [1, -1, 1, -1, -1],
  [0, 0, 0, 2, 0],
  [0, 0, 0, 0, 2],
  [-1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): rows of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Qr : List (List ℤ) := [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): columns of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_Qc : List (List ℤ) := [[0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 0, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 5 (m = 5, n = 10, k = 5): nonzero integer scale `d`.
  Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL5_d : ℤ := 2

-- abhyL6: m = 6, n = 15, k = 9
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): rows of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Mr : List (List ℤ) := [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
  [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
  [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): columns of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Mc : List (List ℤ) := [[1, 1, 0, 0, 0, 0],
  [1, 0, 1, 0, 0, 0],
  [1, 0, 0, 1, 0, 0],
  [1, 0, 0, 0, 1, 0],
  [1, 0, 0, 0, 0, 1],
  [0, 1, 1, 0, 0, 0],
  [0, 1, 0, 1, 0, 0],
  [0, 1, 0, 0, 1, 0],
  [0, 1, 0, 0, 0, 1],
  [0, 0, 1, 1, 0, 0],
  [0, 0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0, 1],
  [0, 0, 0, 1, 1, 0],
  [0, 0, 0, 1, 0, 1],
  [0, 0, 0, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): rows of `K`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Kr : List (List ℤ) := [[0, 0, 0, 2, 2, 2, 2, 2, 2],
  [2, 2, 2, 0, 0, 0, 2, 2, 2],
  [-2, 0, 0, -2, 0, 0, -2, -2, 0],
  [0, -2, 0, 0, -2, 0, -2, 0, -2],
  [0, 0, -2, 0, 0, -2, 0, -2, -2],
  [-2, -2, -2, -2, -2, -2, -2, -2, -2],
  [2, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 2, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 2, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 2, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 2, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 2, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 2]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): columns of `K` (kernel
  basis). Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Kc : List (List ℤ) := [[0, 2, -2, 0, 0, -2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, -2, 0, -2, 0, 2, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, -2, -2, 0, 0, 2, 0, 0, 0, 0, 0, 0],
  [2, 0, -2, 0, 0, -2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
  [2, 0, 0, -2, 0, -2, 0, 0, 0, 0, 2, 0, 0, 0, 0],
  [2, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
  [2, 2, -2, -2, 0, -2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
  [2, 2, -2, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, 2, 0],
  [2, 2, 0, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): rows of `P`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Pr : List (List ℤ) := [[1, 1, -1, -1, -1, -1],
  [1, -1, 1, -1, -1, -1],
  [0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 2, 0],
  [0, 0, 0, 0, 0, 2],
  [-1, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): rows of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Qr : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): columns of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_Qc : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 6 (m = 6, n = 15, k = 9): nonzero integer scale `d`.
  Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL6_d : ℤ := 2

-- abhyL7: m = 7, n = 21, k = 14
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): rows of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Mr : List (List ℤ) := [[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): columns of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Mc : List (List ℤ) := [[1, 1, 0, 0, 0, 0, 0],
  [1, 0, 1, 0, 0, 0, 0],
  [1, 0, 0, 1, 0, 0, 0],
  [1, 0, 0, 0, 1, 0, 0],
  [1, 0, 0, 0, 0, 1, 0],
  [1, 0, 0, 0, 0, 0, 1],
  [0, 1, 1, 0, 0, 0, 0],
  [0, 1, 0, 1, 0, 0, 0],
  [0, 1, 0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0, 1, 0],
  [0, 1, 0, 0, 0, 0, 1],
  [0, 0, 1, 1, 0, 0, 0],
  [0, 0, 1, 0, 1, 0, 0],
  [0, 0, 1, 0, 0, 1, 0],
  [0, 0, 1, 0, 0, 0, 1],
  [0, 0, 0, 1, 1, 0, 0],
  [0, 0, 0, 1, 0, 1, 0],
  [0, 0, 0, 1, 0, 0, 1],
  [0, 0, 0, 0, 1, 1, 0],
  [0, 0, 0, 0, 1, 0, 1],
  [0, 0, 0, 0, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): rows of `K`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Kr : List (List ℤ) := [[0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
  [2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
  [-2, 0, 0, 0, -2, 0, 0, 0, -2, -2, -2, 0, 0, 0],
  [0, -2, 0, 0, 0, -2, 0, 0, -2, 0, 0, -2, -2, 0],
  [0, 0, -2, 0, 0, 0, -2, 0, 0, -2, 0, -2, 0, -2],
  [0, 0, 0, -2, 0, 0, 0, -2, 0, 0, -2, 0, -2, -2],
  [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
  [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): columns of `K` (kernel
  basis). Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Kc : List (List ℤ) := [[0, 2, -2, 0, 0, 0, -2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, -2, 0, 0, -2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, -2, 0, -2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, 0, -2, -2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, -2, 0, 0, 0, -2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, 0, -2, 0, 0, -2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, 0, 0, -2, 0, -2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
  [2, 2, -2, -2, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
  [2, 2, -2, 0, -2, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
  [2, 2, -2, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
  [2, 2, 0, -2, -2, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
  [2, 2, 0, -2, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
  [2, 2, 0, 0, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): rows of `P`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Pr : List (List ℤ) := [[1, 1, -1, -1, -1, -1, -1],
  [1, -1, 1, -1, -1, -1, -1],
  [0, 0, 0, 2, 0, 0, 0],
  [0, 0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 0, 2, 0],
  [0, 0, 0, 0, 0, 0, 2],
  [-1, 1, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): rows of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Qr : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): columns of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_Qc : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for ABHY eq. (5), n = 7 (m = 7, n = 21, k = 14): nonzero integer scale
  `d`. Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def abhyL7_d : ℤ := 2

-- brokenB1: m = 6, n = 15, k = 10
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): rows of `M`. Emitted verbatim
  by the generator; correctness is only what `certL` checks. -/
def brokenB1_Mr : List (List ℤ) := [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
  [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
  [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): columns of `M`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def brokenB1_Mc : List (List ℤ) := [[1, 1, 0, 0, 0, 0],
  [1, 0, 1, 0, 0, 0],
  [1, 0, 0, 1, 0, 0],
  [1, 0, 0, 0, 1, 0],
  [1, 0, 0, 0, 0, 1],
  [0, 1, 1, 0, 0, 0],
  [0, 1, 0, 1, 0, 0],
  [0, 1, 0, 0, 1, 0],
  [0, 1, 0, 0, 0, 1],
  [0, 0, 1, 1, 0, 0],
  [0, 0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0, 1],
  [0, 0, 0, 1, 1, 0],
  [0, 0, 0, 1, 0, 1],
  [0, 0, 0, 0, 1, 1]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): rows of `K`. Emitted verbatim
  by the generator; correctness is only what `certL` checks. -/
def brokenB1_Kr : List (List ℤ) := [[0, 0, 0, 2, 2, 2, 2, 2, 2, 2],
  [2, 2, 2, 0, 0, 0, 2, 2, 2, 0],
  [-2, 0, 0, -2, 0, 0, -2, -2, 0, 0],
  [0, -2, 0, 0, -2, 0, -2, 0, -2, 0],
  [0, 0, -2, 0, 0, -2, 0, -2, -2, 0],
  [-2, -2, -2, -2, -2, -2, -2, -2, -2, 0],
  [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 2, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): columns of `K` (kernel basis).
  Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def brokenB1_Kc : List (List ℤ) := [[0, 2, -2, 0, 0, -2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, -2, 0, -2, 0, 2, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 0, -2, -2, 0, 0, 2, 0, 0, 0, 0, 0, 0],
  [2, 0, -2, 0, 0, -2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
  [2, 0, 0, -2, 0, -2, 0, 0, 0, 0, 2, 0, 0, 0, 0],
  [2, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
  [2, 2, -2, -2, 0, -2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
  [2, 2, -2, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, 2, 0],
  [2, 2, 0, -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
  [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): rows of `P`. Emitted verbatim
  by the generator; correctness is only what `certL` checks. -/
def brokenB1_Pr : List (List ℤ) := [[1, 1, -1, -1, -1, -1],
  [1, -1, 1, -1, -1, -1],
  [0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 2, 0],
  [0, 0, 0, 0, 0, 2],
  [-1, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): rows of `Q`. Emitted verbatim
  by the generator; correctness is only what `certL` checks. -/
def brokenB1_Qr : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): columns of `Q`. Emitted
  verbatim by the generator; correctness is only what `certL` checks. -/
def brokenB1_Qc : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FORGED broken certificate B1 (claims k = 10 for ABHY n = 6, where
  the true value is 9; rejected by `broken_abhy6_dim10_rejected`): nonzero integer scale `d`.
  Emitted verbatim by the generator; correctness is only what `certL` checks. -/
def brokenB1_d : ℤ := 2


/-! ## Planted PL1: ABHY eq. (5), n = 5, 6, 7 (arXiv 1711.09102 eq. (6): dim = n(n−3)/2) -/

/-- The stored row list decodes to the Lean-generated matrix: `rowsM 5 10 abhyL5_Mr = eq5 5 10`. -/
theorem abhyL5_matrix : rowsM 5 10 abhyL5_Mr = eq5 5 10 := by rw [← checkEq_spec]; decide +kernel
/-- The stored row list decodes to the Lean-generated matrix: `rowsM 6 15 abhyL6_Mr = eq5 6 15`. -/
theorem abhyL6_matrix : rowsM 6 15 abhyL6_Mr = eq5 6 15 := by rw [← checkEq_spec]; decide +kernel
/-- The stored row list decodes to the Lean-generated matrix: `rowsM 7 21 abhyL7_Mr = eq5 7 21`. -/
theorem abhyL7_matrix : rowsM 7 21 abhyL7_Mr = eq5 7 21 := by rw [← checkEq_spec]; decide +kernel

/-- Kernel check (`decide`) that the list certificate passes `certL 5 10 5`; with `finrank_of_certL`
  this gives dim ker(eq5 5) = 5. -/
theorem abhyL5_cert : certL 5 10 5 abhyL5_Mr abhyL5_Mc abhyL5_Kr abhyL5_Kc abhyL5_Pr abhyL5_Qr abhyL5_Qc abhyL5_d = true := by
  decide +kernel
/-- Kernel check (`decide`) that the list certificate passes `certL 6 15 9`; with `finrank_of_certL`
  this gives dim ker(eq5 6) = 9. -/
theorem abhyL6_cert : certL 6 15 9 abhyL6_Mr abhyL6_Mc abhyL6_Kr abhyL6_Kc abhyL6_Pr abhyL6_Qr abhyL6_Qc abhyL6_d = true := by
  decide +kernel
/-- Kernel check (`decide`) that the list certificate passes `certL 7 21 14`; with
  `finrank_of_certL` this gives dim ker(eq5 7) = 14. -/
theorem abhyL7_cert : certL 7 21 14 abhyL7_Mr abhyL7_Mc abhyL7_Kr abhyL7_Kc abhyL7_Pr abhyL7_Qr abhyL7_Qc abhyL7_d = true := by
  decide +kernel

/-- Planted PL1, n = 5, through the list checker: dim K₅ = 5. -/
theorem abhy5_finrank' : Module.finrank ℚ (LinearMap.ker (cq (eq5 5 10)).mulVecLin) = 5 := by
  rw [← abhyL5_matrix]; exact finrank_of_certL abhyL5_cert
/-- Planted PL1, n = 6, through the list checker: dim K₆ = 9. -/
theorem abhy6_finrank' : Module.finrank ℚ (LinearMap.ker (cq (eq5 6 15)).mulVecLin) = 9 := by
  rw [← abhyL6_matrix]; exact finrank_of_certL abhyL6_cert
/-- Planted PL1, n = 7, through the list checker: dim K₇ = 14. -/
theorem abhy7_finrank' : Module.finrank ℚ (LinearMap.ker (cq (eq5 7 21)).mulVecLin) = 14 := by
  rw [← abhyL7_matrix]; exact finrank_of_certL abhyL7_cert

/-! ## Broken B1: "dim ker(ABHY eq5, n = 6) = 10" (false by `PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_finrank`) -/

/-- The forged 10-column certificate is rejected by the kernel. -/
theorem broken_abhy6_dim10_rejected :
    certL 6 15 10 brokenB1_Mr brokenB1_Mc brokenB1_Kr brokenB1_Kc brokenB1_Pr brokenB1_Qr brokenB1_Qc brokenB1_d = false := by
  decide +kernel

/-- No list certificate whatsoever can claim dim 10 for ABHY eq. (5), n = 6 (soundness +
  `abhy6_finrank`). -/
theorem no_abhy6_dim10_certL (Mr Mc Kr Kc Pr Qr Qc : List (List ℤ)) (d : ℤ) (hM : rowsM 6 15 Mr = eq5 6 15) :
    certL 6 15 10 Mr Mc Kr Kc Pr Qr Qc d = false := by
  cases h : certL 6 15 10 Mr Mc Kr Kc Pr Qr Qc d
  · rfl
  · have h10 := finrank_of_certL h
    rw [hM, abhy6_finrank] at h10
    exact absurd h10 (by decide)


end PositiveGeometryEmergentSpaceTime.LeanCert2
