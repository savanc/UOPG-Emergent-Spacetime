/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE B (2026-11-03) — JORD-1 sanity theorems for the product table, `IsDer` and `gsm`
(D165, D166). Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.Jord1

/-!
# JORD-1 sanity

The table `T1s` is already tied to the Fano-defined product (`Jord1.bc_eq_jprod`). Here we check that
this product behaves like the exceptional Jordan algebra `h3(O)`:

* Known values: `E1∘E1 = E1`; the unit `I = b₀+b₁+b₂` acts as the identity; the Peirce eigenvalues of `E1`
  are `1` (b₀), `0` (b₁, b₂ and the (1,2) block b₃..b₁₀) and `1/2` (the (2,0), (0,1) blocks b₁₁..b₂₆);
  octonion units square to `−1` and anticommute (Fano table).
* Jordan identity `(x∘y)∘(x∘x) = x∘(y∘(x∘x))` on all basis pairs and on a mixed `x` against all basis `y`.
* Planted: the product is not associative (`(E1∘E1)∘b₁₁ ≠ E1∘(E1∘b₁₁)`); the identity matrix is not a
  derivation.
* Non-vacuity: generator 0 of `gsm` is a nonzero matrix (20 nonzero entries), so `gsm ≠ {0}`.
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Sanity
open Matrix PositiveGeometryEmergentSpaceTime.Jord1 PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.LeanCert2

/-- Sparse `2 u∘v` from the table. -/
def prodS (u v : List (ℕ × ℤ)) : List (ℕ × ℤ) :=
  u.flatMap (fun p => v.flatMap (fun q =>
    ((T1s.getD p.1 []).getD q.1 []).map (fun r => (r.1, p.2 * q.2 * r.2))))
/-- Equality of sparse vectors in all 27 coordinates. -/
def eqS (u v : List (ℕ × ℤ)) : Bool := (List.range 27).all (fun l => coefS u l == coefS v l)
/-- Basis vector `b_i`. -/
def eB (i : ℕ) : List (ℕ × ℤ) := [(i, 1)]
/-- Scalar multiple. -/
def smulS (c : ℤ) (u : List (ℕ × ℤ)) : List (ℕ × ℤ) := u.map (fun p => (p.1, c * p.2))

/-- Known value: `2 E1∘E1 = 2 E1`. -/
theorem E1_idem : jprod 0 0 = (List.range 27).map (fun l => if l = 0 then 2 else 0) := by decide +kernel

/-- Known value: the unit `I = b₀ + b₁ + b₂` satisfies `2 I∘b_j = 2 b_j` for every basis element. -/
theorem unit_ok : allFin 27 (fun j => eqS (prodS [(0, 1), (1, 1), (2, 1)] (eB j)) (smulS 2 (eB j))) = true := by
  decide +kernel

/-- Peirce eigenvalue of `E1` on `b_j` (times 2). -/
def peirce2 (j : ℕ) : ℤ := if j = 0 then 2 else if j < 11 then 0 else 1

/-- Known value: Peirce decomposition of `E1`: `2 E1∘b_j = peirce2 j • b_j`. -/
theorem E1_peirce : allFin 27 (fun j => eqS (prodS (eB 0) (eB j)) (smulS (peirce2 j) (eB j))) = true := by
  decide +kernel

/-- Known value: octonion imaginary units square to `−1` and anticommute (Fano table). -/
theorem octonion_units : allFin 8 (fun a => allFin 8 (fun b =>
    if (a : ℕ) = 0 ∨ (b : ℕ) = 0 then true
    else if a = b then ou a b == (-1, 0)
    else ou a b != (0, 0) && (ou a b).2 == (ou b a).2 && (ou a b).1 == -(ou b a).1)) = true := by
  decide +kernel

/-- Jordan identity on all basis pairs (scaled by 2 at each product). -/
theorem jordan_basis : allFin 27 (fun i => allFin 27 (fun j =>
    let xx := prodS (eB i) (eB i)
    eqS (prodS (prodS (eB i) (eB j)) xx) (prodS (eB i) (prodS (eB j) xx)))) = true := by
  decide +kernel

/-- A mixed element touching every block: `x = b₀ − b₂ + b₄ + 2 b₁₃ − b₂₀ + b₂₆`. -/
def xMix : List (ℕ × ℤ) := [(0, 1), (2, -1), (4, 1), (13, 2), (20, -1), (26, 1)]

/-- Jordan identity for the mixed `x` against every basis `y`. -/
theorem jordan_mixed : allFin 27 (fun j =>
    let xx := prodS xMix xMix
    eqS (prodS (prodS xMix (eB j)) xx) (prodS xMix (prodS (eB j) xx))) = true := by
  decide +kernel

/-- Planted: the product is not associative: `(E1∘E1)∘b₁₁ ≠ E1∘(E1∘b₁₁)` (Peirce `1/2` vs `1/4`). -/
theorem planted_assoc : eqS (prodS (prodS (eB 0) (eB 0)) (eB 11)) (prodS (eB 0) (prodS (eB 0) (eB 11))) = false := by
  decide +kernel

/-- Planted: the identity matrix is not a derivation (`2 E1∘E1 = 2 E1` would force `bc 0 0 0 = 0`). -/
theorem planted_identity_not_der : ¬ IsDer (1 : Matrix (Fin 27) (Fin 27) ℚ) := by
  intro h
  have e := h 0 0 0
  simp only [Matrix.one_apply, mul_ite, mul_one, mul_zero, ite_mul, one_mul, zero_mul,
    Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_univ, ite_true] at e
  have hb : bc ((0 : Fin 27) : ℕ) ((0 : Fin 27) : ℕ) ((0 : Fin 27) : ℕ) = 2 := by decide +kernel
  rw [hb] at e; norm_num at e

/-- Non-vacuity: generator 0 has 20 nonzero integer entries, so `gsm` contains a nonzero element. -/
theorem gen0_nonzero : ((gR 0).flatten.filter (· ≠ 0)).length = 20 := by decide +kernel

theorem gsm_nontrivial : ∃ D ∈ gsm, D ≠ 0 := by
  refine ⟨cq (rowsM 27 27 (gR 0)), gen_mem_gsm 0, ?_⟩
  have hne : ∃ i j : Fin 27, rowsM 27 27 (gR 0) i j ≠ 0 := by
    have : (allFin 27 (fun i => allFin 27 (fun j => rowsM 27 27 (gR 0) i j == 0))) = false := by
      decide +kernel
    by_contra hc
    push Not at hc
    have : allFin 27 (fun i => allFin 27 (fun j => rowsM 27 27 (gR 0) i j == 0)) = true := by
      rw [allFin_iff]; intro i; rw [allFin_iff]; intro j; simp [hc i j]
    simp_all
  obtain ⟨i, j, hij⟩ := hne
  intro h0
  have := congrFun (congrFun h0 i) j
  simp [cq, Matrix.map_apply] at this
  exact hij this

/-- Tie D165↔D166: `gsm` lies in the pointwise stabiliser of `{E1}`. -/
theorem gsm_sub_stab : gsm ⊆ stab {E1v} := by
  rintro D ⟨hd, h0, _⟩
  exact ⟨hd, by rintro x rfl; exact h0⟩

/-- Tie D166: the stabiliser of `∅` is the whole derivation algebra. -/
theorem stab_empty : stab ∅ = {D | IsDer D} := by
  ext D; simp [stab]

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Sanity
