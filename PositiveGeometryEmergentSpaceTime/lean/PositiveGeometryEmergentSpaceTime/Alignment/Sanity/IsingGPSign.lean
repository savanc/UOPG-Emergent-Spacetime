/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE C (2026-11-03) — H-T5: the GP sign rule at n = 3 recovered by exhaustion.
Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.IsingStar

/-!
# H-T5: GP sign rule, n = 3, by exhaustion over sign patterns

The GP matrix of the star has entries `1` on the diagonal column pair and `(ε, −ε)·tᵢtⱼ` on the
off-diagonal pair `(2j, 2j+1)` of row `i`. There are six off-diagonal signs `ε i j`, i.e. 64 patterns
(bit `pid i j` of `n < 64` set ↔ `ε i j = −1`).

At the exact point `t = (1/2, 1/3, 1/4)`:
* `pos_unique`: exactly one pattern makes all twenty 3×3 minors positive, and it is `n = 38`;
* `orth_count`: exactly 8 of the 64 patterns satisfy the OG relations `M η Mᵀ = 0`;
* `gp_eq`: pattern 38 is GP's transcribed rule `IsingStar.gpRule` (`gpSign`), entry by entry.

So positivity alone singles out the transcribed sign rule at n = 3 (at this point); this does not derive
GP's rule for general n, and it does not prove that orthogonality holds for all t (that is
`IsingStar.gpRule_orth`).
-/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.IsingGPSign
open PositiveGeometryEmergentSpaceTime.Alignment.Sanity.IsingStar

/-- Bit index of the off-diagonal pair `(i, j)`, `i ≠ j`, in `0 … 5`. -/
def pid (i j : ℕ) : ℕ := 2 * i + (if i < j then j - 1 else j)

/-- Sign pattern `n`: `ε i j = −1` iff bit `pid i j` of `n` is set. -/
def eps (n i j : ℕ) : ℚ := if n.testBit (pid i j) then -1 else 1

def tq (i : ℕ) : ℚ := if i = 0 then 1/2 else if i = 1 then 1/3 else 1/4

/-- Signed star matrix for pattern `n` at `t = (1/2, 1/3, 1/4)`. -/
def sR (n : ℕ) (i c : ℕ) : ℚ :=
  if c / 2 = i then 1 else eps n i (c / 2) * (tq i * tq (c / 2)) * (if c % 2 = 0 then 1 else -1)

/-- 3×3 minor on columns `a b c`. -/
def mnr (n a b c : ℕ) : ℚ :=
  sR n 0 a * (sR n 1 b * sR n 2 c - sR n 1 c * sR n 2 b) - sR n 0 b * (sR n 1 a * sR n 2 c - sR n 1 c * sR n 2 a) +
    sR n 0 c * (sR n 1 a * sR n 2 b - sR n 1 b * sR n 2 a)

def triples : List (ℕ × ℕ × ℕ) :=
  (List.range 6).flatMap fun a => (List.range 6).flatMap fun b => (List.range 6).filterMap fun c =>
    if a < b ∧ b < c then some (a, b, c) else none

def posAll (n : ℕ) : Bool := triples.all fun p => decide (0 < mnr n p.1 p.2.1 p.2.2)

def sig (m : ℕ) : ℚ := if m % 2 = 0 then 1 else -1

def orthAll (n : ℕ) : Bool :=
  [(0, 1), (0, 2), (1, 2)].all fun p => decide (((List.range 6).map (fun m => sR n p.1 m * sig m * sR n p.2 m)).sum = 0)

theorem triples_length : triples.length = 20 := by decide

/-- **H-T5 sign rule, n = 3.** Exactly one of the 64 sign patterns is totally positive at `t₀`: `n = 38`. -/
theorem pos_unique : (List.range 64).filter posAll = [38] := by decide +kernel

/-- Exactly 8 of the 64 patterns satisfy the OG relations at `t₀` (positivity is the selecting condition). -/
theorem orth_count : ((List.range 64).filter orthAll).length = 8 := by decide +kernel

/-- The selected pattern is orthogonal. -/
theorem orth_38 : orthAll 38 = true := by decide +kernel

/-- Tie: pattern 38 is GP's transcribed rule `gpRule` on the star correlations at `t₀`. -/
theorem gp_eq : ∀ i : Fin 3, ∀ c : Fin 6, sR 38 i c = gpRule (starM t0) i c := by
  have h0 : Nat.testBit 38 0 = false := by decide
  have h1 : Nat.testBit 38 1 = true := by decide
  have h2 : Nat.testBit 38 2 = true := by decide
  have h3 : Nat.testBit 38 3 = false := by decide
  have h4 : Nat.testBit 38 4 = false := by decide
  have h5 : Nat.testBit 38 5 = true := by decide
  intro i c; fin_cases i <;> fin_cases c <;>
    simp [sR, eps, pid, tq, gpRule, gpSign, starM, t0, h0, h1, h2, h3, h4, h5] <;> norm_num

/-- Planted: flipping one sign of the GP pattern (bit 0) loses positivity. -/
theorem planted_flip : posAll (38 ^^^ 1) = false := by decide +kernel

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.IsingGPSign
