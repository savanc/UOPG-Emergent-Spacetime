/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of BR-4 (`no_scale`).
Written ONLY from Paper II v8 §"BR-4" prose and Fig. caption ("a scale-blind map f takes the
same value on x and c•x, while a degree-k quantity changes by c^k, so f cannot fix it … an
earlier AI-generated draft … concluded σ = 0 and assumed c > 0"), BEFORE opening
lean/PGEST/BR4.lean, ScaleNoGo, SG1, the blueprint row or generated/lean/no_scale.lean.

Reading of "f cannot fix q": q does not factor through f (no g with q = g ∘ f) unless q ≡ 0.
We prove it under the WEAKER hypothesis that f is blind only to positive scalings (and q is
homogeneous only for positive scalings), for any integer degree k ≠ 0, over any real vector
space. The three instances (stabilisers, eigen-data, LS amplitude) are not specified in the
prose and are NOT formalised here.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.Br4Blind

/-- BLIND CLAIM (no scale). -/
theorem no_scale {X Y : Type*} [AddCommGroup X] [Module ℝ X]
    (f : X → Y) (q : X → ℝ) (k : ℤ) (hk : k ≠ 0)
    (hf : ∀ c : ℝ, 0 < c → ∀ x, f (c • x) = f x)
    (hq : ∀ c : ℝ, 0 < c → ∀ x, q (c • x) = c ^ k * q x)
    (g : Y → ℝ) (hfix : ∀ x, q x = g (f x)) : ∀ x, q x = 0 := by
  intro x
  have h2 : q ((2 : ℝ) • x) = q x := by rw [hfix, hfix, hf 2 (by norm_num)]
  rw [hq 2 (by norm_num)] at h2
  have hne : (2 : ℝ) ^ k ≠ 1 := by
    intro h
    have := (zpow_right_injective₀ (by norm_num : (0 : ℝ) < 2) (by norm_num)) (h.trans (zpow_zero 2).symm)
    exact hk this
  have : ((2 : ℝ) ^ k - 1) * q x = 0 := by linarith
  rcases mul_eq_zero.mp this with h | h
  · exact absurd (sub_eq_zero.mp h) hne
  · exact h

/-- Contrapositive form: a non-zero homogeneous quantity is not a function of a scale-blind map. -/
theorem no_scale' {X Y : Type*} [AddCommGroup X] [Module ℝ X]
    (f : X → Y) (q : X → ℝ) (k : ℤ) (hk : k ≠ 0)
    (hf : ∀ c : ℝ, 0 < c → ∀ x, f (c • x) = f x)
    (hq : ∀ c : ℝ, 0 < c → ∀ x, q (c • x) = c ^ k * q x)
    (x₀ : X) (hx₀ : q x₀ ≠ 0) : ¬ ∃ g : Y → ℝ, ∀ x, q x = g (f x) := by
  rintro ⟨g, hg⟩
  exact hx₀ (no_scale f q k hk hf hq g hg x₀)

/-- Witness that the hypotheses are satisfiable non-trivially: on ℝ, f = constant and q = id
(degree 1); q ≠ 0, so q is not fixed by f. -/
theorem witness : ¬ ∃ g : Unit → ℝ, ∀ x : ℝ, x = g ((fun _ => ()) x) :=
  no_scale' (X := ℝ) (fun _ => ()) id 1 one_ne_zero (fun _ _ _ => rfl)
    (fun c _ x => by simp [smul_eq_mul]) 1 one_ne_zero

/-- Degree 0 is genuinely excluded: q = constant 1 is fixed by any f. -/
theorem degree_zero_control : ∃ g : Unit → ℝ, ∀ x : ℝ, (fun _ => (1 : ℝ)) x = g ((fun _ => ()) x) :=
  ⟨fun _ => 1, fun _ => rfl⟩

end PositiveGeometryEmergentSpaceTime.Alignment.Br4Blind
