/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.BR4
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.Br4Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: BR-4 (scale-blind no-go)

Blind: over ℝ, `f` invariant under positive rescalings, `q` homogeneous of integer degree `k ≠ 0`
under positive rescalings ⇒ `q` is not a function of `f` (unless `q ≡ 0`).
Original: over any field `K`, `f` invariant under all nonzero rescalings, `σ` homogeneous of
natural degree `k` ⇒ for a single `c` with `c^k ≠ 1`, `f` cannot separate `x` from `c•x` while
`σ` does; `fixes_scale_not_blind` packages this as "if `f` determines `σ` then `f` is not blind".

VERDICT: **DIFFERENT** (incomparable generality). Original is more general in the field and the
explicit witness `c`; blind is more general in the degree (`k : ℤ`) and needs invariance only under
`c > 0`. On the common core (ℝ, `k : ℕ`, `k ≠ 0`) each implies the other — proved below, with
"`f` determines `σ`" ↔ "`∃ g, σ = g ∘ f`" proved as `determines_iff_factors`.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.BR4

open PositiveGeometryEmergentSpaceTime.Alignment

/-- The original's "f determines σ" is the blind's "σ factors through f". -/
theorem determines_iff_factors {X Y Z : Type*} [Inhabited Z] (f : X → Y) (q : X → Z) :
    (∀ x y, f x = f y → q x = q y) ↔ ∃ g : Y → Z, ∀ x, q x = g (f x) := by
  classical
  constructor
  · intro h
    refine ⟨fun y => if hy : ∃ x, f x = y then q hy.choose else default, fun x => ?_⟩
    have hx : ∃ x', f x' = f x := ⟨x, rfl⟩
    simp only [hx, dite_true]
    exact h _ _ hx.choose_spec.symm
  · rintro ⟨g, hg⟩ x y hxy
    rw [hg, hg, hxy]

/-- Original ⇒ blind conclusion on the common core (ℝ, natural degree k ≥ 1),
given the original's stronger hypothesis (invariance under all `c ≠ 0`). -/
theorem orig_to_blind {X Y : Type*} [AddCommGroup X] [Module ℝ X] (f : X → Y)
    (hf : PositiveGeometryEmergentSpaceTime.BR4.ScaleBlind (K := ℝ) f) (q : X → ℝ) (k : ℕ) (hk : k ≠ 0)
    (hq : ∀ (c : ℝ) x, q (c • x) = c ^ k * q x) (x₀ : X) (hx₀ : q x₀ ≠ 0) :
    ¬ ∃ g : Y → ℝ, ∀ x, q x = g (f x) := by
  rw [← determines_iff_factors]
  intro hdet
  have h2 : (2 : ℝ) ^ k ≠ 1 := (one_lt_pow₀ (by norm_num : (1 : ℝ) < 2) hk).ne'
  exact PositiveGeometryEmergentSpaceTime.BR4.fixes_scale_not_blind f q k hq hdet hx₀ (c := 2) two_ne_zero h2 hf

/-- Blind ⇒ the original's `fixes_scale_not_blind` conclusion, on the common core, from the blind's
weaker hypotheses (positive rescalings only). -/
theorem blind_to_orig {X Y : Type*} [AddCommGroup X] [Module ℝ X] (f : X → Y)
    (hf : ∀ c : ℝ, 0 < c → ∀ x, f (c • x) = f x) (q : X → ℝ) (k : ℕ) (hk : k ≠ 0)
    (hq : ∀ c : ℝ, 0 < c → ∀ x, q (c • x) = c ^ k * q x) (x₀ : X) (hx₀ : q x₀ ≠ 0) :
    ¬ ∀ x y, f x = f y → q x = q y := by
  rw [determines_iff_factors]
  exact Br4Blind.no_scale' f q (k : ℤ) (by exact_mod_cast hk) hf
    (fun c hc x => by rw [hq c hc x, zpow_natCast]) x₀ hx₀

/-- Gap witness (blind-only generality): degree `k = -1` is covered by the blind theorem but is not
expressible in the original (`k : ℕ`). On ℝ \ {0}-style data: `q x = x⁻¹`, `f` constant. -/
theorem blind_negative_degree :
    ¬ ∃ g : Unit → ℝ, ∀ x : ℝ, x⁻¹ = g ((fun _ => ()) x) :=
  Br4Blind.no_scale' (fun _ : ℝ => ()) (fun x => x⁻¹) (-1) (by norm_num) (fun _ _ _ => rfl)
    (fun c hc x => by rw [smul_eq_mul, mul_inv, zpow_neg_one]) 1 (by norm_num)

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.BR4
