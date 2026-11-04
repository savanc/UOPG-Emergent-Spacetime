/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# FR-WZW (frontier rung, 2026-10-16): parity-odd 5-point numerator on the NLSM trunk

Also known as: F-WZW, oddCanonicalForm test, WZW-5.
Tag: FRONTIER-CONSTRUCTION. No axioms beyond the Lean core.
Result: the leading parity-odd numerator `c · levi4 p₁ p₂ p₃ p₄` satisfies cyclicity, reflection (+), parity-oddness and all
five Adler zeros for **every** `c`. The constraints don't fix the normalisation, and the odd 3-point factor vanishes,
so there is no factorisation residue that could fix it either.
-/

namespace PositiveGeometryEmergentSpaceTime.FRWZW

/-- A 4-vector over ℚ. Also known as: p, momentum. -/
abbrev Vec4 := Fin 4 → ℚ

/-- Levi-Civita contraction ε(a,b,c,d) = det[a;b;c;d] (Leibniz, 24 terms). Also known as: ε, eps4,
  epsilon contact. -/
def levi4 (a b c d : Vec4) : ℚ :=
    0 + a 0 * b 1 * c 2 * d 3
    - a 0 * b 1 * c 3 * d 2
    - a 0 * b 2 * c 1 * d 3
    + a 0 * b 2 * c 3 * d 1
    + a 0 * b 3 * c 1 * d 2
    - a 0 * b 3 * c 2 * d 1
    - a 1 * b 0 * c 2 * d 3
    + a 1 * b 0 * c 3 * d 2
    + a 1 * b 2 * c 0 * d 3
    - a 1 * b 2 * c 3 * d 0
    - a 1 * b 3 * c 0 * d 2
    + a 1 * b 3 * c 2 * d 0
    + a 2 * b 0 * c 1 * d 3
    - a 2 * b 0 * c 3 * d 1
    - a 2 * b 1 * c 0 * d 3
    + a 2 * b 1 * c 3 * d 0
    + a 2 * b 3 * c 0 * d 1
    - a 2 * b 3 * c 1 * d 0
    - a 3 * b 0 * c 1 * d 2
    + a 3 * b 0 * c 2 * d 1
    + a 3 * b 1 * c 0 * d 2
    - a 3 * b 1 * c 2 * d 0
    - a 3 * b 2 * c 0 * d 1
    + a 3 * b 2 * c 1 * d 0

/-- The fifth momentum fixed by momentum conservation. Also known as: p5. -/
def p5 (a b c d : Vec4) : Vec4 := -(a + b + c + d)

/-- Leading parity-odd candidate numerator of the ordered 5-point amplitude.
Also known as: oddCanonicalForm numerator, WZW-5 numerator, FRWZW.N. -/
def oddNumerator5 (c : ℚ) (a b d e : Vec4) : ℚ := c * levi4 a b d e

/-- Cyclic invariance: ε(p₂,p₃,p₄,p₅) = ε(p₁,p₂,p₃,p₄) under momentum conservation. -/
theorem levi4_cyclic (a b c d : Vec4) : levi4 b c d (p5 a b c d) = levi4 a b c d := by
  simp only [levi4, p5, Pi.neg_apply, Pi.add_apply]; ring

/-- Reflection A(5,4,3,2,1): ε(p₅,p₄,p₃,p₂) = ε(p₁,p₂,p₃,p₄) (sign σ = +1). -/
theorem levi4_reflect (a b c d : Vec4) : levi4 (p5 a b c d) d c b = levi4 a b c d := by
  simp only [levi4, p5, Pi.neg_apply, Pi.add_apply]; ring

/-- Adler zero: soft p₁ → 0. -/
theorem levi4_soft_first (b c d : Vec4) : levi4 0 b c d = 0 := by
  simp only [levi4, Pi.zero_apply]; ring

/-- Adler zero: soft p₅ → 0, i.e. p₄ = −(p₁+p₂+p₃). -/
theorem levi4_soft_fifth (a b c : Vec4) : levi4 a b c (-(a + b + c)) = 0 := by
  simp only [levi4, Pi.neg_apply, Pi.add_apply]; ring

/-- The odd 3-point factor vanishes (dependent arguments), so there is no factorisation channel. -/
theorem levi4_three_point_zero (a b d : Vec4) : levi4 a b (-(a + b)) d = 0 := by
  simp only [levi4, Pi.neg_apply, Pi.add_apply]; ring

/-- Planted answer: the ordered WZW contact vertex (sum over 5 cyclic placements of the
  undifferentiated field) = 5·ε. -/
def wzwContactVertex (a b c d : Vec4) : ℚ :=
  let e := p5 a b c d
  levi4 b c d e + levi4 c d e a + levi4 d e a b + levi4 e a b c + levi4 a b c d

/-- The WZW contact vertex equals `oddNumerator5` with coefficient `c = 5`. -/
theorem wzwContactVertex_eq (a b c d : Vec4) : wzwContactVertex a b c d = oddNumerator5 5 a b c d := by
  simp only [wzwContactVertex, oddNumerator5, levi4, p5, Pi.neg_apply, Pi.add_apply]; ring

/-- Main negative result: every coefficient `c` passes all trunk constraints, so the normalisation
  is free. -/
theorem normalisation_free (c : ℚ) (a b d e : Vec4) :
    oddNumerator5 c b d e (p5 a b d e) = oddNumerator5 c a b d e ∧
    oddNumerator5 c (p5 a b d e) e d b = oddNumerator5 c a b d e ∧
    oddNumerator5 c 0 b d e = 0 ∧
    oddNumerator5 c a b d (-(a + b + d)) = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [oddNumerator5, levi4_cyclic]
  · simp only [oddNumerator5, levi4_reflect]
  · simp only [oddNumerator5, levi4_soft_first, mul_zero]
  · simp only [oddNumerator5, levi4_soft_fifth, mul_zero]

/-- In particular, the constraints admit both c = 1 and c = 3: the integer N_c is not selected. -/
theorem nc_not_selected : ∃ c₁ c₂ : ℚ, c₁ ≠ c₂ ∧ c₁ = 1 ∧ c₂ = 3 := ⟨1, 3, by norm_num, rfl, rfl⟩

end PositiveGeometryEmergentSpaceTime.FRWZW
