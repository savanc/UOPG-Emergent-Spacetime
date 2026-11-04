/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.ScaleNoGo
import PositiveGeometryEmergentSpaceTime.SG1
/-!
# BR-4: degree-0 homogeneity ⇒ no scale (2026-10-14)
One lemma behind ScaleNoGo (OP-2), SG1 and the LS rescaling: data invariant under `x ↦ c • x`
cannot determine any quantity that is homogeneous of nonzero degree. Instances below reuse the
existing theorems unchanged. Structural only; no physics claim beyond dimensional analysis.
-/
namespace PositiveGeometryEmergentSpaceTime.BR4

/-- `f` is blind to rescaling by nonzero scalars. -/
def ScaleBlind {K X Y : Type*} [Zero K] [SMul K X] (f : X → Y) : Prop :=
  ∀ c : K, c ≠ 0 → ∀ x, f (c • x) = f x

/-- Main lemma: scale-blind data agree on `x` and `c • x`, while a degree-`k` scale `σ` differs
whenever `c ^ k ≠ 1` and `σ x ≠ 0`. -/
theorem no_scale {K X Y : Type*} [Field K] [SMul K X] {f : X → Y} (hf : ScaleBlind (K := K) f)
    (σ : X → K) (k : ℕ) (hσ : ∀ (c : K) x, σ (c • x) = c ^ k * σ x)
    {x : X} (hx : σ x ≠ 0) {c : K} (hc : c ≠ 0) (hck : c ^ k ≠ 1) :
    f (c • x) = f x ∧ σ (c • x) ≠ σ x := by
  refine ⟨hf c hc x, ?_⟩
  rw [hσ]
  intro h
  apply hck
  have h' : (c ^ k - 1) * σ x = 0 := by rw [sub_mul, h]; ring
  rcases mul_eq_zero.mp h' with h1 | h1
  · exact sub_eq_zero.mp h1
  · exact absurd h1 hx

/-- What an MG4 mechanism must break: a map that determines a degree-`k` scale on some point with
`σ x ≠ 0` and some `c` with `c ^ k ≠ 1` cannot be scale-blind. -/
theorem fixes_scale_not_blind {K X Y : Type*} [Field K] [SMul K X] (f : X → Y)
    (σ : X → K) (k : ℕ) (hσ : ∀ (c : K) x, σ (c • x) = c ^ k * σ x)
    (hdet : ∀ x y, f x = f y → σ x = σ y)
    {x : X} (hx : σ x ≠ 0) {c : K} (hc : c ≠ 0) (hck : c ^ k ≠ 1) :
    ¬ ScaleBlind (K := K) f := by
  intro hf
  exact (no_scale hf σ k hσ hx hc hck).2 (hdet _ _ (no_scale hf σ k hσ hx hc hck).1)

/-! ## Instances -/

section Stab
variable {G K V : Type*} [Group G] [Field K] [AddCommGroup V] [Module K V]
  [MulAction G V] [SMulCommClass G K V]
/-- (I1) Stabiliser data (OP-2) is scale-blind. -/
theorem stabilizer_blind : ScaleBlind (K := K) (fun v : V => MulAction.stabilizer G v) :=
  fun _ hc v => PositiveGeometryEmergentSpaceTime.ScaleNoGo.stabilizer_smul_eq (G := G) v hc
end Stab

/-- (I2) Perron–Frobenius eigen-data: "x is an eigenvector of A with eigenvalue λ" is scale-blind. -/
theorem eigen_blind {n : ℕ} (A : Matrix (Fin n) (Fin n) ℝ) (lam : ℝ) :
    ScaleBlind (K := ℝ) (fun x : Fin n → ℝ => A.mulVec x = lam • x) := by
  intro c hc x
  apply propext
  constructor
  · intro h
    have := PositiveGeometryEmergentSpaceTime.SG1.eigen_scale A (c • x) lam c⁻¹ h
    simpa [smul_smul, inv_mul_cancel₀ hc] using this
  · exact PositiveGeometryEmergentSpaceTime.SG1.eigen_scale A x lam c

/-- (I3) LS amplitude as a function of (s, u, m²) is scale-blind (all m², incl. the junk value m² =
  0). -/
theorem LS_blind (a0 : ℝ) :
    ScaleBlind (K := ℝ) (fun p : ℝ × ℝ × ℝ => PositiveGeometryEmergentSpaceTime.ScaleNoGo.LS a0 p.1 p.2.1 p.2.2) := by
  intro c hc p
  obtain ⟨s, u, m2⟩ := p
  by_cases hm : m2 = 0
  · subst hm; simp [PositiveGeometryEmergentSpaceTime.ScaleNoGo.LS]
  · exact PositiveGeometryEmergentSpaceTime.ScaleNoGo.LS_scale a0 s u m2 c hc hm

/-- Non-vacuity witness: the hypotheses of `no_scale` are satisfiable (LS instance, σ = m², k = 1,
point (1,1,1), c = 2). -/
theorem no_scale_witness (a0 : ℝ) :
    ∃ (p : ℝ × ℝ × ℝ) (c : ℝ), c ≠ 0 ∧
      PositiveGeometryEmergentSpaceTime.ScaleNoGo.LS a0 (c • p).1 (c • p).2.1 (c • p).2.2 = PositiveGeometryEmergentSpaceTime.ScaleNoGo.LS a0 p.1 p.2.1 p.2.2 ∧
      (c • p).2.2 ≠ p.2.2 := by
  refine ⟨(1, 1, 1), 2, by norm_num, ?_⟩
  have h := no_scale (LS_blind a0) (fun p : ℝ × ℝ × ℝ => p.2.2) 1
    (fun c p => by simp) (x := ((1:ℝ), (1:ℝ),
        (1:ℝ))) (by norm_num) (c := (2:ℝ)) (by norm_num) (by norm_num)
  exact ⟨h.1, h.2⟩

end PositiveGeometryEmergentSpaceTime.BR4
