import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Positivity

/-!
# SurfConv — convention invariance of SURF-1′ sign profiles (2026-10-30, the author)

Graph-uniform rescaling (trivalent vertex × λ, propagator × μ) multiplies an interference ratio
`K = W(num)/W(den)` by `λ^(ΔV3) μ^(ΔE)`. In the cubic theory ΔV3 = 2k is even, so for λ ≠ 0, μ > 0
the sign of every K, hence every SURF-1′ positivity set, is unchanged.
-/

namespace PositiveGeometryEmergentSpaceTime.SurfConv

/-- Even power of a nonzero scalar is positive. -/
theorem even_pow_pos {F : Type*} [Field F] [LinearOrder F] [IsStrictOrderedRing F] {lam : F} (h : lam ≠ 0) (k : ℕ) :
    0 < lam ^ (2 * k) := by
  rw [pow_mul]; exact pow_pos (by positivity) k

/-- Sign of a K value is invariant under the graph-uniform rescaling. -/
theorem pos_iff_scaled {F : Type*} [Field F] [LinearOrder F] [IsStrictOrderedRing F] {lam mu x : F}
    (hl : lam ≠ 0) (hm : 0 < mu) (k m : ℕ) :
    0 < lam ^ (2 * k) * mu ^ m * x ↔ 0 < x := by
  have h : 0 < lam ^ (2 * k) * mu ^ m := mul_pos (even_pow_pos hl k) (pow_pos hm m)
  exact ⟨fun hx => pos_of_mul_pos_right hx h.le, fun hx => mul_pos h hx⟩

/-- Ratio form: scaling numerator and denominator by the uniform rule preserves the sign of num/den. -/
theorem ratio_pos_iff {F : Type*} [Field F] [LinearOrder F] [IsStrictOrderedRing F] {s a b : F} (hs : 0 < s) :
    0 < (s * a) * b ↔ 0 < a * b := by
  rw [mul_assoc]; exact ⟨fun h => pos_of_mul_pos_right h hs.le, fun h => mul_pos hs h⟩

end PositiveGeometryEmergentSpaceTime.SurfConv
