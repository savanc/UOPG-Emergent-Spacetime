/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-7' gate. Pole-subtracted πN amplitudes D̄±(ν,t). Crossing: D̄+ even, D̄- odd in ν.
The ν = 0 zero of D̄- is forced by crossing symmetry alone (non-discriminating).
D̄+ at the Cheng–Dashen point equals Σ/fπ² > 0 at LO+: no zero; its value needs the σ-term,
an extra input outside {mρ, mπ, fπ}.
-/

namespace PositiveGeometryEmergentSpaceTime.PiNSubGate

/-- An odd function vanishes at 0. -/
theorem odd_zero (f : ℝ → ℝ) (hodd : ∀ ν, f (-ν) = - f ν) : f 0 = 0 := by
  have h := hodd 0; simp at h; linarith

/-- `σ/f² ≠ 0` for positive `σ` and `f²`. -/
theorem cd_nonzero (sig f2 : ℝ) (hs : 0 < sig) (hf : 0 < f2) : sig / f2 ≠ 0 :=
  ne_of_gt (div_pos hs hf)

end PositiveGeometryEmergentSpaceTime.PiNSubGate
