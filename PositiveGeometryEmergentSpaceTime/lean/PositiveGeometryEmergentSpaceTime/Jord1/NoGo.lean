/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
JORD-1 (prereg/JORD-1-positivity-closure-2026-10-28.md, run JORD1-2026-10-28-r1).
NO-GO: the SM-type subalgebra `g_sm = stab(E1) ∩ setstab(h3(C))` of `Der(h3(O))` (over ℚ) is not the
pointwise stabiliser of any subset of h3(O). Proof: every `x` fixed by the 12 elements `Gs[k] ∈ g_sm` is
killed by the derivation `W` (row-selection certificate `dW • W = Cm * Rsel`), so `W` lies in every
pointwise stabiliser that contains `g_sm`, but `W ∉ g_sm`.  No `sorry`, no `native_decide`.
-/
import PositiveGeometryEmergentSpaceTime.Jord1.Gens

/-!
# PositiveGeometryEmergentSpaceTime.Jord1.NoGo

Supporting module of the `PositiveGeometryEmergentSpaceTime` Lean library. See the declarations below for
the statements; each theorem is checked by the Lean kernel.
-/


set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Jord1

open Matrix PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.LeanCert2

/-- Row `r` of `Rsel` is row `selIdx[r].2` of generator `selIdx[r].1`. -/
def selOK : Bool := (List.range 25).all (fun r =>
  decide ((selIdx.getD r (0, 0)).1 < 12) && decide ((selIdx.getD r (0, 0)).2 < 27) &&
    (Rsel.getD r [] == (Gs.getD (selIdx.getD r (0, 0)).1 []).getD (selIdx.getD r (0, 0)).2 []))

/-- The selection check `selOK` evaluates to `true` (kernel decision). -/
theorem selOK_true : selOK = true := by decide +kernel

/-- A vector annihilated by all 12 generator matrices is also annihilated by `Rsel`. -/
theorem Rsel_kills (x : Fin 27 → ℚ) (hx : ∀ k : Fin 12, (cq (rowsM 27 27 (gR k))).mulVec x = 0) :
    (cq (rowsM 25 27 Rsel)).mulVec x = 0 := by
  have h := selOK_true
  simp only [selOK, List.all_eq_true, List.mem_range, Bool.and_eq_true, decide_eq_true_eq,
    beq_iff_eq] at h
  ext r
  obtain ⟨⟨hk, hρ⟩, hrow⟩ := h r r.isLt
  have e := congrFun (hx ⟨_, hk⟩) ⟨_, hρ⟩
  simp only [Matrix.mulVec, dotProduct, Pi.zero_apply] at e ⊢
  rw [← e]
  refine Finset.sum_congr rfl (fun j _ => ?_)
  have hj : rowsM 25 27 Rsel r j = rowsM 27 27 (gR (selIdx.getD r (0, 0)).1) ⟨_, hρ⟩ j := by
    simp only [rowsM, gR, hrow]
  simp only [cq, Matrix.map_apply, hj]

/-- Certificate: `Cm * Rsel = dW • W` (rows of `Rsel` given also as columns `RselC`). -/
def certW : Bool := lenL 25 Cm && tposL 25 27 Rsel RselC &&
  allFin 27 (fun i => allFin 27 (fun j => mulL Cm RselC i j == dW * (Wr.getD i []).getD j 0))

/-- The certificate check `certW` evaluates to `true` (kernel decision). -/
theorem certW_true : certW = true := by decide +kernel

/-- Integer certificate: `Cm * Rsel = dW • Wr` as matrices. -/
theorem certW_int : rowsM 27 25 Cm * rowsM 25 27 Rsel = dW • rowsM 27 27 Wr := by
  have h := certW_true
  simp only [certW, Bool.and_eq_true, allFin_iff, beq_iff_eq] at h
  obtain ⟨⟨hl, ht⟩, hm⟩ := h
  rw [tposL_spec ht]
  ext i j
  rw [mulL_eq _ hl, hm i j]
  simp [Matrix.smul_apply, rowsM]

/-- `W` kills every vector fixed by all 12 elements `Gs[k]` of `g_sm`. -/
theorem W_kills_fix (x : Fin 27 → ℚ) (hx : ∀ k : Fin 12, (cq (rowsM 27 27 (gR k))).mulVec x = 0) :
    (cq (rowsM 27 27 Wr)).mulVec x = 0 := by
  have hR := Rsel_kills x hx
  have hc : cq (rowsM 27 25 Cm) * cq (rowsM 25 27 Rsel) = (dW : ℚ) • cq (rowsM 27 27 Wr) := by
    rw [← cq_mul, certW_int]; ext i j
    simp only [cq, Matrix.map_apply, Matrix.smul_apply, smul_eq_mul, Int.coe_castRingHom,
        Int.cast_mul]
  have h1 : ((dW : ℚ) • cq (rowsM 27 27 Wr)).mulVec x = 0 := by
    rw [← hc, ← Matrix.mulVec_mulVec, hR, Matrix.mulVec_zero]
  rw [Matrix.smul_mulVec] at h1
  have hd : (dW : ℚ) ≠ 0 := by norm_num [dW]
  exact (smul_eq_zero.mp h1).resolve_left hd

/-- **JORD-1 NO-GO.** `g_sm = stab(E1) ∩ setstab(h3(C))` is not the pointwise stabiliser (in `Der h3(O)`,
over ℚ) of any subset of h3(O); in particular of no set of positive-cone points or faces. -/
theorem gsm_not_pointwise_stabiliser : ¬ ∃ S : Set (Fin 27 → ℚ), stab S = gsm := by
  rintro ⟨S, hS⟩
  have hW : cq (rowsM 27 27 Wr) ∈ stab S := by
    refine ⟨W_isDer, fun x hx => W_kills_fix x (fun k => ?_)⟩
    have hk : cq (rowsM 27 27 (gR k)) ∈ stab S := hS ▸ gen_mem_gsm k
    exact hk.2 x hx
  rw [hS] at hW
  exact W_not_presB hW.2.2

end PositiveGeometryEmergentSpaceTime.Jord1
