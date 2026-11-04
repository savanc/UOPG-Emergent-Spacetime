/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
SURF-1′ n = 4 box in the u-channel (prereg §2): tree4_u ∘ box(1234) and its denominator tree4_u ∘ tree4_u.
tree4_u = vertices (1,3,e), (2,4,f), edge e–f. box(1234) = vertices (1,ab,da2), (2,bc,ab2), (3,cd,bc2),
(4,da,cd2), edges ab–ab2, bc–bc2, cd–cd2, da–da2. External legs glued 1–1, 2–2, 3–3, 4–4.
Half-edges: tree L1=0, L3=1, Le=2, L2=3, L4=4, Lf=5; box R1=6, ab=7, da2=8, R2=9, bc=10, ab2=11,
R3=12, cd=13, bc2=14, R4=15, da=16, cd2=17 (second tree: R1=6, R3=7, Re=8, R2=9, R4=10, Rf=11).
-/
import PositiveGeometryEmergentSpaceTime.Surf1.Enum

/-!
# PositiveGeometryEmergentSpaceTime.Surf1.Box.Graph

Supporting module of the `PositiveGeometryEmergentSpaceTime` Lean library. See the declarations below for
the statements; each theorem is checked by the Lean kernel.
-/


set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Surf1

/-- The box graph `boxU`: six vertices and nine edges, given as half-edge lists. -/
def boxU : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17]],
  [(2, 5), (7, 11), (10, 14), (13, 17), (16, 8), (0, 6), (3, 9), (1, 12), (4, 15)]⟩

/-- The graph `ttU`: four vertices and six edges, given as half-edge lists. -/
def ttU : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]],
  [(2, 5), (8, 11), (0, 6), (3, 9), (1, 7), (4, 10)]⟩

/-- The top exponent `hiW boxU` is 36. -/
theorem boxU_hiW : hiW boxU = 36 := by decide
/-- The coefficient window `lenW boxU` has length 46. -/
theorem boxU_lenW : lenW boxU = 46 := by decide
/-- `boxU` has 2^6 = 64 orientation patterns. -/
theorem boxU_nV : 2 ^ boxU.V.length = 64 := by decide

/-- Denominator: W(tree4_u ∘ tree4_u) = 4N⁴ − 36N² + 96 − 64/N² = 4(N²−1)(N²−4)²/N². -/
theorem ttU_c1 : W1 ttU = [(4, 4), (2, -36), (0, 96), (-2, -64)] := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Surf1
