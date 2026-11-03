/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
JORD-1 (prereg/JORD-1-positivity-closure-2026-10-28.md, run JORD1-2026-10-28-r1).
The Jordan product of h3(O) from the Fano lines, its sparse structure-constant table, the derivation
predicate `IsDer`, and a kernel-checkable sparse derivation test `derS` with its soundness proof.
No `sorry`, no `native_decide`.
-/
import PositiveGeometryEmergentSpaceTime.LeanCert2.Core
import PositiveGeometryEmergentSpaceTime.Jord1.Table

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Jord1

open Matrix PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.LeanCert2

/-! ## Octonion units from the Fano lines and the h3(O) product -/

/-- Fano lines: `e_x e_y = e_z` along each oriented line (cyclically). -/
def fano : List (ℕ × ℕ × ℕ) := [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2),
    (7, 1, 3)]

/-- Product of two imaginary units along one line, if they lie on it. -/
def lineHit (a b : ℕ) (t : ℕ × ℕ × ℕ) : Option (ℤ × ℕ) :=
  if a = t.1 ∧ b = t.2.1 then some (1, t.2.2) else
  if a = t.2.1 ∧ b = t.2.2 then some (1, t.1) else
  if a = t.2.2 ∧ b = t.1 then some (1, t.2.1) else
  if a = t.2.1 ∧ b = t.1 then some (-1, t.2.2) else
  if a = t.2.2 ∧ b = t.2.1 then some (-1, t.1) else
  if a = t.1 ∧ b = t.2.2 then some (-1, t.2.1) else none

/-- `e_a e_b = s e_c` as `(s, c)` (`e_0 = 1`). -/
def ou (a b : ℕ) : ℤ × ℕ :=
  if a = 0 then (1, b) else if b = 0 then (1, a) else if a = b then (-1, 0)
  else (fano.findSome? (lineHit a b)).getD (0, 0)

/-- A sparse octonion-matrix entry `(row, col, unit, coefficient)`. -/
abbrev Ent := ℕ × ℕ × ℕ × ℤ

/-- Off-diagonal blocks `(base, row, col)`: coordinates `base..base+7` are the octonion at `(row,
  col)`. -/
def blk : List (ℕ × ℕ × ℕ) := [(3, 1, 2), (11, 2, 0), (19, 0, 1)]

/-- Basis element `b_i` of h3(O) as a sparse hermitian octonion matrix. -/
def basisE (i : ℕ) : List Ent :=
  if i < 3 then [(i, i, 0, 1)] else
  (blk.filter (fun t => decide (t.1 ≤ i ∧ i < t.1 + 8))).flatMap
    (fun t => [(t.2.1, t.2.2, i - t.1, 1), (t.2.2, t.2.1, i - t.1, if i - t.1 = 0 then 1 else -1)])

/-- Sparse matrix product (octonion entries multiplied with `ou`). -/
def mprod (X Y : List Ent) : List Ent :=
  X.flatMap (fun p => Y.filterMap (fun q =>
    if p.2.1 = q.1 then some (p.1, q.2.1, (ou p.2.2.1 q.2.2.1).2,
        (ou p.2.2.1 q.2.2.1).1 * p.2.2.2 * q.2.2.2)
    else none))

/-- Sum of the coefficients at `(r, c, u)`. -/
def sumAt (P : List Ent) (r c u : ℕ) : ℤ :=
  ((P.filter (fun e => e.1 == r && e.2.1 == c && e.2.2.1 == u)).map (fun e => e.2.2.2)).sum

/-- Coordinate `l` of a sparse hermitian matrix in the basis `b_0..b_26`. -/
def coordE (P : List Ent) (l : ℕ) : ℤ :=
  if l < 3 then sumAt P l l 0 else
  ((blk.filter (fun t => decide (t.1 ≤ l ∧ l < t.1 + 8))).map (fun t => sumAt P t.2.1 t.2.2 (l - t.1))).sum

/-- Coordinates of `2 b_i∘b_j = b_i b_j + b_j b_i`. -/
def jprod (i j : ℕ) : List ℤ :=
  (List.range 27).map (coordE (mprod (basisE i) (basisE j) ++ mprod (basisE j) (basisE i)))

/-! ## Sparse vectors -/

/-- Coefficient of index `l` in a sparse vector. -/
def coefS : List (ℕ × ℤ) → ℕ → ℤ
  | [], _ => 0
  | p :: r, l => (if p.1 = l then p.2 else 0) + coefS r l

/-- Sparse-dense dot product. -/
def dotS : List (ℕ × ℤ) → List ℤ → ℤ
  | [], _ => 0
  | p :: r, c => p.2 * c.getD p.1 0 + dotS r c

/-- All indices of a sparse vector are below 27. -/
def idxOK (s : List (ℕ × ℤ)) : Bool := s.all (fun p => decide (p.1 < 27))

/-- For an index-valid sparse list `s`, `dotS s c` equals the dense sum `∑ l, coefS s l * c.getD l
  0`. -/
theorem dotS_eq : ∀ (s : List (ℕ × ℤ)) (c : List ℤ), idxOK s = true →
    dotS s c = ∑ l : Fin 27, coefS s l * c.getD l 0
  | [], c, _ => by simp [dotS, coefS]
  | p :: r, c, h => by
    simp only [idxOK, List.all_cons, Bool.and_eq_true, decide_eq_true_eq] at h
    rw [dotS, dotS_eq r c h.2]
    simp only [coefS, add_mul, Finset.sum_add_distrib, ite_mul, zero_mul]
    congr 1
    rw [Finset.sum_eq_single (⟨p.1, h.1⟩ : Fin 27)]
    · simp
    · intro b _ hb
      rw [ite_eq_right_iff]
      intro he; exact absurd (Fin.ext he.symm) hb
    · intro hn; exact absurd (Finset.mem_univ _) hn

/-! ## Structure constants and their checks -/

/-- `2 b_i∘b_j = Σ_l bc i j l • b_l`. -/
def bc (i j l : ℕ) : ℤ := coefS ((T1s.getD i []).getD j []) l

/-- Boolean check that each sparse table entry `T1s[i][j]` expands to the product row `jprod i j`. -/
def T1s_ok : Bool := allFin 27 (fun i => allFin 27 (fun j =>
  (List.range 27).map (coefS ((T1s.getD i []).getD j [])) == jprod i j))

/-- Boolean check that each sparse entry `T2s[j][k]` has coefficient `bc l j k` at every index `l`. -/
def T2s_ok : Bool := allFin 27 (fun j => allFin 27 (fun k => allFin 27 (fun l =>
  coefS ((T2s.getD j []).getD k []) l == bc l j k)))

/-- Boolean check that the structure constants are symmetric: `bc i j l = bc j i l`. -/
def comm_ok : Bool := allFin 27 (fun i => allFin 27 (fun j => allFin 27 (fun l => bc i j l == bc j i l)))

/-- Boolean check that every sparse entry of `T1s` and `T2s` uses only indices below 27. -/
def idx_ok : Bool := allFin 27 (fun i => allFin 27 (fun j =>
  idxOK ((T1s.getD i []).getD j []) && idxOK ((T2s.getD i []).getD j [])))

/-- The check `T1s_ok` evaluates to `true` (kernel decision). -/
theorem T1s_ok_true : T1s_ok = true := by decide +kernel
/-- The check `T2s_ok` evaluates to `true` (kernel decision). -/
theorem T2s_ok_true : T2s_ok = true := by decide +kernel
/-- The symmetry check `comm_ok` evaluates to `true` (kernel decision). -/
theorem comm_ok_true : comm_ok = true := by decide +kernel
/-- The index check `idx_ok` evaluates to `true` (kernel decision). -/
theorem idx_ok_true : idx_ok = true := by decide +kernel

/-- The table is the Fano-defined Jordan product `2 b_i∘b_j` of h3(O). -/
theorem bc_eq_jprod (i j l : Fin 27) : bc i j l = (jprod i j).getD l 0 := by
  have h := T1s_ok_true
  simp only [T1s_ok, allFin_iff, beq_iff_eq] at h
  have key : ∀ f : ℕ → ℤ, ((List.range 27).map f).getD (l : ℕ) 0 = f l := by
    intro f; rw [List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_range l.isLt]; rfl
  rw [← h i j, key]; rfl

/-! ## Derivations -/

/-- `D` (acting on column vectors) is a derivation of `(h3(O), ∘)`. -/
def IsDer (D : Matrix (Fin 27) (Fin 27) ℚ) : Prop :=
  ∀ i j k : Fin 27, ∑ l : Fin 27, (bc i j l : ℚ) * D k l =
    ∑ l : Fin 27, D l i * (bc l j k : ℚ) + ∑ l : Fin 27, D l j * (bc i l k : ℚ)

/-- Sparse derivation test on a row list `Dr` and its column list `Dc`. -/
def derS (Dr Dc : List (List ℤ)) : Bool :=
  allFin 27 (fun i => allFin 27 (fun j => allFin 27 (fun k =>
    dotS ((T1s.getD i []).getD j []) (Dr.getD k []) ==
      dotS ((T2s.getD j []).getD k []) (Dc.getD i []) + dotS ((T2s.getD i []).getD k []) (Dc.getD j []))))

/-- Soundness of `derS`. -/
theorem isDer_of_derS {Dr Dc : List (List ℤ)} (ht : tposL 27 27 Dr Dc = true) (h : derS Dr Dc = true) :
    IsDer (cq (rowsM 27 27 Dr)) := by
  have hT := tposL_spec ht
  have hi := idx_ok_true
  have h2 := T2s_ok_true
  have hc := comm_ok_true
  simp only [idx_ok, T2s_ok, comm_ok, derS, allFin_iff, Bool.and_eq_true, beq_iff_eq] at hi h2 hc h
  intro i j k
  have e := h i j k
  rw [dotS_eq _ _ (hi i j).1, dotS_eq _ _ (hi j k).2, dotS_eq _ _ (hi i k).2] at e
  have eZ : ∑ l : Fin 27, bc i j l * rowsM 27 27 Dr k l =
      ∑ l : Fin 27, rowsM 27 27 Dr l i * bc l j k + ∑ l : Fin 27, rowsM 27 27 Dr l j * bc i l k := by
    have s1 : ∑ l : Fin 27, rowsM 27 27 Dr l i * bc l j k =
        ∑ l : Fin 27, coefS ((T2s.getD j []).getD k []) l * (Dc.getD i []).getD l 0 := by
      refine Finset.sum_congr rfl (fun l _ => ?_)
      rw [h2 j k l, congrFun (congrFun hT l) i, colsM, mul_comm]
    have s2 : ∑ l : Fin 27, rowsM 27 27 Dr l j * bc i l k =
        ∑ l : Fin 27, coefS ((T2s.getD i []).getD k []) l * (Dc.getD j []).getD l 0 := by
      refine Finset.sum_congr rfl (fun l _ => ?_)
      rw [h2 i k l, hc l i k, congrFun (congrFun hT l) j, colsM, mul_comm]
    rw [s1, s2]; exact e
  have eQ := congrArg (fun z : ℤ => (z : ℚ)) eZ
  simpa only [cq, Matrix.map_apply, Int.coe_castRingHom, Int.cast_add, Int.cast_sum,
      Int.cast_mul] using eQ

/-! ## The SM-type subalgebra and pointwise stabilisers -/

/-- The idempotent `E1`. -/
def E1v : Fin 27 → ℚ := fun l => if (l : ℕ) = 0 then 1 else 0

/-- Coordinates of `h3(C) ⊂ h3(O)` with `C = span{1, e1}`. -/
def inB (w : ℕ) : Bool := [0, 1, 2, 3, 4, 11, 12, 19, 20].contains w

/-- `D` maps `h3(C)` into itself. -/
def PresB (D : Matrix (Fin 27) (Fin 27) ℚ) : Prop :=
  ∀ k w : Fin 27, inB w = true → inB k = false → D k w = 0

/-- `g_sm = stab(E1) ∩ setstab(h3(C))` inside the derivations of h3(O) (over ℚ). -/
def gsm : Set (Matrix (Fin 27) (Fin 27) ℚ) := {D | IsDer D ∧ D.mulVec E1v = 0 ∧ PresB D}

/-- Pointwise stabiliser of `S ⊆ h3(O)` in the derivations. -/
def stab (S : Set (Fin 27 → ℚ)) : Set (Matrix (Fin 27) (Fin 27) ℚ) := {D | IsDer D ∧ ∀ x ∈ S,
    D.mulVec x = 0}

/-- Boolean check that column 0 of the integer matrix `Dr` (27 rows) is zero. -/
def col0L (Dr : List (List ℤ)) : Bool := allFin 27 (fun k => (Dr.getD k []).getD 0 0 == 0)

/-- Boolean check that `Dr` has zero entry `(k, w)` whenever `w` lies in `B` and `k` does not. -/
def presBL (Dr : List (List ℤ)) : Bool :=
  allFin 27 (fun k => allFin 27 (fun w => !(inB w && !inB k) || (Dr.getD k []).getD w 0 == 0))

/-- If `col0L Dr` holds, the rational matrix of `Dr` sends the basis vector `E1v` to zero. -/
theorem mulVec_E1_of {Dr : List (List ℤ)} (h : col0L Dr = true) : (cq (rowsM 27 27 Dr)).mulVec E1v = 0 := by
  simp only [col0L, allFin_iff, beq_iff_eq] at h
  ext k
  simp only [Matrix.mulVec, dotProduct, E1v, Pi.zero_apply]
  rw [Finset.sum_eq_single (0 : Fin 27)]
  · have h0 : rowsM 27 27 Dr k 0 = 0 := h k
    simp [cq, h0]
  · intro b _ hb
    have : (b : ℕ) ≠ 0 := fun h0 => hb (Fin.ext h0)
    simp [this]
  · simp

/-- If `presBL Dr` holds, the rational matrix of `Dr` satisfies `PresB`. -/
theorem presB_of {Dr : List (List ℤ)} (h : presBL Dr = true) : PresB (cq (rowsM 27 27 Dr)) := by
  intro k w hw hk
  simp only [presBL, allFin_iff] at h
  have := h k w
  simp only [hw, hk, Bool.not_false, Bool.and_true, Bool.not_true, Bool.false_or,
      beq_iff_eq] at this
  have h0 : rowsM 27 27 Dr k w = 0 := this
  simp [cq, h0]

end PositiveGeometryEmergentSpaceTime.Jord1
