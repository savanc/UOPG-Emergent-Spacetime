/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
SURF-1′ crossed box, u-channel: combine the 64 per-orientation kernel certificates (`Box/C0..C3`)
into W(tree4_u ∘ box1234) at c = 1. The combination is a rewrite of `vsum` plus a decision on
literal lists; no enumeration is redone here.
-/
import PositiveGeometryEmergentSpaceTime.Surf1.Box.C0
import PositiveGeometryEmergentSpaceTime.Surf1.Box.C1
import PositiveGeometryEmergentSpaceTime.Surf1.Box.C2
import PositiveGeometryEmergentSpaceTime.Surf1.Box.C3

/-!
# PositiveGeometryEmergentSpaceTime.Surf1.Box

Supporting module of the `PositiveGeometryEmergentSpaceTime` Lean library. See the declarations below for
the statements; each theorem is checked by the Lean kernel.
-/


set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Surf1

/-- W(tree4_u ∘ box1234) = −32N³ + 480N − 1728/N + 1280/N³ = −32(N²−1)(N²−4)(N²−10)/N³. -/
theorem boxU_c1 : W1 boxU = [(3, -32), (1, 480), (-1, -1728), (-3, 1280)] := by
  unfold W1 coefs
  rw [boxU_hiW, boxU_lenW, boxU_nV]
  simp only [vsum, boxU_o0, boxU_o1, boxU_o2, boxU_o3, boxU_o4, boxU_o5, boxU_o6, boxU_o7, boxU_o8,
      boxU_o9, boxU_o10, boxU_o11, boxU_o12, boxU_o13, boxU_o14, boxU_o15, boxU_o16, boxU_o17,
      boxU_o18, boxU_o19, boxU_o20, boxU_o21, boxU_o22, boxU_o23, boxU_o24, boxU_o25, boxU_o26,
      boxU_o27, boxU_o28, boxU_o29, boxU_o30, boxU_o31, boxU_o32, boxU_o33, boxU_o34, boxU_o35,
      boxU_o36, boxU_o37, boxU_o38, boxU_o39, boxU_o40, boxU_o41, boxU_o42, boxU_o43, boxU_o44,
      boxU_o45, boxU_o46, boxU_o47, boxU_o48, boxU_o49, boxU_o50, boxU_o51, boxU_o52, boxU_o53,
      boxU_o54, boxU_o55, boxU_o56, boxU_o57, boxU_o58, boxU_o59, boxU_o60, boxU_o61, boxU_o62,
      boxU_o63]
  decide

end PositiveGeometryEmergentSpaceTime.Surf1
