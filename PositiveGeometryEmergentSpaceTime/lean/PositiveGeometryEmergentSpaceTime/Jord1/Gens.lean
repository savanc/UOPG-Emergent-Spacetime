/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
JORD-1 (prereg/JORD-1-positivity-closure-2026-10-28.md, run JORD1-2026-10-28-r1).
Kernel checks that the 12 live-run elements `Gs[k]` lie in `g_sm`, and that `W` is a derivation.
No `sorry`, no `native_decide`.
-/
import PositiveGeometryEmergentSpaceTime.Jord1.Alg
import PositiveGeometryEmergentSpaceTime.Jord1.Data

/-!
# PositiveGeometryEmergentSpaceTime.Jord1.Gens

Supporting module of the `PositiveGeometryEmergentSpaceTime` Lean library. See the declarations below for
the statements; each theorem is checked by the Lean kernel.
-/


set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Jord1

open Matrix PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.LeanCert2

/-- Generator `k` of the real list `Gs` as integer rows (empty if out of range). -/
def gR (k : ℕ) : List (List ℤ) := Gs.getD k []
/-- Generator `k` of the list `GsC` as integer rows (empty if out of range). -/
def gC (k : ℕ) : List (List ℤ) := GsC.getD k []

/-- All kernel checks for generator `k`. -/
def genOK (k : ℕ) : Bool :=
  tposL 27 27 (gR k) (gC k) && col0L (gR k) && presBL (gR k) && derS (gR k) (gC k)

/-- All kernel checks `genOK 0` pass for generator 0. -/
theorem gen0_ok : genOK 0 = true := by decide +kernel
/-- All kernel checks `genOK 1` pass for generator 1. -/
theorem gen1_ok : genOK 1 = true := by decide +kernel
/-- All kernel checks `genOK 2` pass for generator 2. -/
theorem gen2_ok : genOK 2 = true := by decide +kernel
/-- All kernel checks `genOK 3` pass for generator 3. -/
theorem gen3_ok : genOK 3 = true := by decide +kernel
/-- All kernel checks `genOK 4` pass for generator 4. -/
theorem gen4_ok : genOK 4 = true := by decide +kernel
/-- All kernel checks `genOK 5` pass for generator 5. -/
theorem gen5_ok : genOK 5 = true := by decide +kernel
/-- All kernel checks `genOK 6` pass for generator 6. -/
theorem gen6_ok : genOK 6 = true := by decide +kernel
/-- All kernel checks `genOK 7` pass for generator 7. -/
theorem gen7_ok : genOK 7 = true := by decide +kernel
/-- All kernel checks `genOK 8` pass for generator 8. -/
theorem gen8_ok : genOK 8 = true := by decide +kernel
/-- All kernel checks `genOK 9` pass for generator 9. -/
theorem gen9_ok : genOK 9 = true := by decide +kernel
/-- All kernel checks `genOK 10` pass for generator 10. -/
theorem gen10_ok : genOK 10 = true := by decide +kernel
/-- All kernel checks `genOK 11` pass for generator 11. -/
theorem gen11_ok : genOK 11 = true := by decide +kernel

/-- All kernel checks `genOK k` pass for each of the 12 generators. -/
theorem gens_ok : ∀ k : Fin 12, genOK k = true := by
  intro k; fin_cases k
  exacts [gen0_ok, gen1_ok, gen2_ok, gen3_ok, gen4_ok, gen5_ok, gen6_ok, gen7_ok, gen8_ok, gen9_ok,
    gen10_ok, gen11_ok]

/-- Each `Gs[k]` is an element of `g_sm`. -/
theorem gen_mem_gsm (k : Fin 12) : cq (rowsM 27 27 (gR k)) ∈ gsm := by
  have h := gens_ok k
  simp only [genOK, Bool.and_eq_true] at h
  obtain ⟨⟨⟨ht, h0⟩, hb⟩, hd⟩ := h
  exact ⟨isDer_of_derS ht hd, mulVec_E1_of h0, presB_of hb⟩

/-- Kernel check `tposL 27 27 Wr Wc` evaluates to `true`. -/
theorem W_tpos : tposL 27 27 Wr Wc = true := by decide +kernel
/-- Kernel check `derS Wr Wc` evaluates to `true`. -/
theorem W_derS : derS Wr Wc = true := by decide +kernel

/-- `W` is a derivation of h3(O). -/
theorem W_isDer : IsDer (cq (rowsM 27 27 Wr)) := isDer_of_derS W_tpos W_derS

/-- `W` does not preserve `h3(C)`: `W` maps `b_1 = E2` to a vector with a nonzero `b_5` (unit `e2`)
  component. -/
theorem W_not_presB : ¬ PresB (cq (rowsM 27 27 Wr)) := by
  intro h
  have hv : rowsM 27 27 Wr 5 1 = -1 := by decide +kernel
  have := h 5 1 (by decide) (by decide)
  simp [cq, hv] at this

end PositiveGeometryEmergentSpaceTime.Jord1
