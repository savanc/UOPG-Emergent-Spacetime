/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
CASCADE-1b (prereg/CASCADE-1b-split-fix-blind-retest-2026-10-23.md, §7 item 1).
E0 (massless legs), n = 6: the nine physical-c offsets o_ab(μ) of the translation y = X − μ
(2312.16282 eq. 2.4 with X_{i,i+1} = 0; offsets as printed by the locked checker v2 `offsets`).
Run-independent: it does not use any n = 6 V_D output (run CASCADE1b-2026-10-23-r1 was NOT-EVALUATED).
Items 2–5 of §7 need run relations and are not done here.
-/

namespace PositiveGeometryEmergentSpaceTime.Cascade1b

/-- The nine E0 offsets at n = 6, indexed by the non-adjacent pairs (13,14,15,24,25,26,35,36,46). -/
def offsetsE0 (m13 m14 m15 m24 m25 m26 m35 m36 m46 : ℚ) : List ℚ :=
  [m13 - m14 + m24, m14 - m15 - m24 + m25, m15 - m25 + m26, m24 - m25 + m35,
   m25 - m26 - m35 + m36, m13 + m26 - m36, m35 - m36 + m46, -m13 + m14 + m36 - m46,
   -m14 + m15 + m46]

/-- 2312.16282 §7.1 (CITED), reproduced: the c-preserving shifts at n = 6 (E0) are exactly the δ-line
μ_ee = δ, μ_oo = −δ, μ_eo = 0. -/
theorem e0_n6_offsets_zero_iff (m13 m14 m15 m24 m25 m26 m35 m36 m46 : ℚ) :
    (∀ o ∈ offsetsE0 m13 m14 m15 m24 m25 m26 m35 m36 m46, o = 0) ↔
      ∃ d : ℚ, m24 = d ∧ m26 = d ∧ m46 = d ∧ m13 = -d ∧ m15 = -d ∧ m35 = -d ∧
        m14 = 0 ∧ m25 = 0 ∧ m36 = 0 := by
  constructor
  · intro h
    simp only [offsetsE0, List.mem_cons, List.mem_nil_iff, or_false, forall_eq_or_imp,
        forall_eq] at h
    obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := h
    refine ⟨m24, rfl, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> linarith
  · rintro ⟨d, h24, h26, h46, h13, h15, h35, h14, h25, h36⟩
    subst h24 h26 h46 h13 h15 h35 h14 h25 h36
    simp only [offsetsE0, List.mem_cons, List.mem_nil_iff, or_false, forall_eq_or_imp, forall_eq]
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> ring

/-- With non-tachyonic offsets (all μ ≥ 0) the δ-line collapses to μ = 0 (E0-n6 S4 if V_D = {0}). -/
theorem e0_n6_collapse (m13 m14 m15 m24 m25 m26 m35 m36 m46 : ℚ)
    (h : ∀ o ∈ offsetsE0 m13 m14 m15 m24 m25 m26 m35 m36 m46, o = 0)
    (p13 : 0 ≤ m13) (p24 : 0 ≤ m24) :
    m13 = 0 ∧ m14 = 0 ∧ m15 = 0 ∧ m24 = 0 ∧ m25 = 0 ∧ m26 = 0 ∧ m35 = 0 ∧ m36 = 0 ∧ m46 = 0 := by
  obtain ⟨d, h24, h26, h46, h13, h15, h35, h14, h25,
      h36⟩ := (e0_n6_offsets_zero_iff _ _ _ _ _ _ _ _ _).1 h
  have hd : d = 0 := by linarith
  subst hd
  refine ⟨?_, h14, ?_, h24, h25, h26, ?_, h36, h46⟩ <;> simp_all

end PositiveGeometryEmergentSpaceTime.Cascade1b
