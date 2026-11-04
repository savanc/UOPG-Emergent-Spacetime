/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
/-
  PositiveGeometryEmergentSpaceTime/OrderParameter.lean — rung OP-1 (imported from scratch draft 2026-10-12).
  Claim under study: "gauge symmetry breaking and spacetime emergence share an order parameter".
  What this file can show: both are instances of ONE formal Landau pattern
  (group G acting on V, point v, unbroken subgroup = stabiliser, broken ⇔ stabiliser ≠ ⊤).
  It does NOT show they are one physical field.
  Does not import or depend on UOPG.lean / UOPGv2.lean (both contain `sorry`).
-/
import Mathlib

open Matrix

namespace PositiveGeometryEmergentSpaceTime.OrderParam

/-! ## (a) Generic order parameter -/

/-- An order parameter: a point `v` of a `G`-space whose symmetry is broken
(stabiliser is a proper subgroup). -/
class OrderParameter (G V : Type*) [Group G] [MulAction G V] where
  /-- The distinguished vector (vacuum / background) in `V`. -/
  v : V
  /-- The stabiliser of `v` is a proper subgroup. -/
  broken : MulAction.stabilizer G v ≠ ⊤

variable {G V : Type*} [Group G] [MulAction G V]

/-- Unbroken subgroup. -/
abbrev unbroken (v : V) : Subgroup G := MulAction.stabilizer G v

/-- Every element of the unbroken subgroup fixes `v`. -/
theorem unbroken_invariant (v : V) (h : unbroken (G := G) v) : (h : G) • v = v :=
  h.2

/-- Broken ⇔ some group element moves `v`. -/
theorem broken_iff (v : V) : unbroken (G := G) v ≠ ⊤ ↔ ∃ g : G, g • v ≠ v := by
  constructor
  · intro h
    by_contra hc
    push Not at hc
    exact h (eq_top_iff.2 fun g _ => hc g)
  · rintro ⟨g, hg⟩ htop
    exact hg (by
      have : g ∈ unbroken (G := G) v := htop ▸ Subgroup.mem_top g
      exact this)

/-- Vacuum manifold: orbit ≃ G/H (Mathlib `orbitEquivQuotientStabilizer`). -/
noncomputable def vacuumManifold (v : V) : MulAction.orbit G v ≃ G ⧸ unbroken (G := G) v :=
  MulAction.orbitEquivQuotientStabilizer G v

/-- In a broken phase the orbit is not a single point. -/
theorem orbit_nontrivial_of_broken [inst : OrderParameter G V] :
    ∃ g : G, g • inst.v ≠ inst.v :=
  (broken_iff inst.v).1 inst.broken

/-! ## (b) Gauge instance: SU(2) × U(1) on ℂ² -/

/-- The special unitary group SU(2) as 2×2 complex matrices. -/
abbrev SU2 := Matrix.specialUnitaryGroup (Fin 2) ℂ
/-- The electroweak gauge group `SU(2) × U(1)` (U(1) as the unit circle). -/
abbrev Gauge := SU2 × Circle

/-! Doublet action ψ ↦ z · (U ψ). NOTE: the U(1) factor acts with charge 1 in the
parameter `z`; physical hypercharge ½ corresponds to z = e^{iθ/2} (a reparametrisation /
double cover of the θ-circle). -/

/-- The raw action map. -/
noncomputable def gact (g : Gauge) (ψ : Fin 2 → ℂ) : Fin 2 → ℂ :=
  ((g.2 : Circle) : ℂ) • ((g.1 : SU2).1 *ᵥ ψ)

/-- Action of `SU(2) × U(1)` on doublets: `(U, z) • ψ = z (U ψ)`. -/
noncomputable instance gaugeAction : MulAction Gauge (Fin 2 → ℂ) where
  smul := gact
  one_smul ψ := by
    show gact 1 ψ = ψ
    simp [gact]
  mul_smul g h ψ := by
    show gact (g * h) ψ = gact g (gact h ψ)
    simp only [gact, Prod.fst_mul, Prod.snd_mul, Submonoid.coe_mul, Circle.coe_mul]
    rw [Matrix.mulVec_smul, ← Matrix.mulVec_mulVec, smul_smul]

/-- Unfolded form of the doublet action: `g • ψ = g.2 · (g.1 ψ)`. -/
theorem gauge_smul_def (g : Gauge) (ψ : Fin 2 → ℂ) :
    g • ψ = ((g.2 : Circle) : ℂ) • ((g.1 : SU2).1 *ᵥ ψ) := rfl

/-- Higgs vev (0, v₀). -/
def higgsVev (v0 : ℂ) : Fin 2 → ℂ := ![0, v0]

/-- Diagonal SU(2) element diag(z, z⁻¹) ... membership left open below if needed. -/
noncomputable def diagMat (z : Circle) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.diagonal ![(z : ℂ), ((z⁻¹ : Circle) : ℂ)]

/-- `diag(z, z⁻¹)` lies in SU(2) for `z` on the unit circle. -/
theorem diagMat_mem (z : Circle) : diagMat z ∈ SU2 := by
  rw [Matrix.mem_specialUnitaryGroup_iff]
  refine ⟨?_, ?_⟩
  · rw [Matrix.mem_unitaryGroup_iff]
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [diagMat, Matrix.mul_apply, Matrix.diagonal,
        Matrix.star_apply, Circle.coe_inv] <;>
      first
        | (rw [← mul_inv, Complex.mul_conj, Complex.normSq_eq_norm_sq]; simp)
        | (rw [Complex.mul_conj, Complex.normSq_eq_norm_sq]; simp)
  · simp [diagMat, Matrix.det_diagonal, Fin.prod_univ_two, Circle.coe_inv]

/-- Electromagnetic U(1) embedding z ↦ (diag(z, z⁻¹), z). -/
noncomputable def emEmbed (z : Circle) : Gauge := (⟨diagMat z, diagMat_mem z⟩, z)

/-- The image of the electromagnetic embedding fixes the vev `(0, v₀)`. -/
theorem emEmbed_mem_unbroken (v0 : ℂ) (z : Circle) :
    emEmbed z ∈ unbroken (G := Gauge) (higgsVev v0) := by
  rw [MulAction.mem_stabilizer_iff, gauge_smul_def]
  ext i
  fin_cases i <;> simp [emEmbed, diagMat, higgsVev, Circle.coe_inv]

/-- The electromagnetic embedding `U(1) → SU(2) × U(1)` is injective. -/
theorem emEmbed_injective : Function.Injective emEmbed := by
  intro a b h
  exact congrArg Prod.snd h

/-- The pure hypercharge phase z = -1 moves the vev (needs v₀ ≠ 0): symmetry broken. -/
theorem gauge_broken (v0 : ℂ) (hv : v0 ≠ 0) :
    unbroken (G := Gauge) (higgsVev v0) ≠ ⊤ := by
  rw [broken_iff]
  refine ⟨(1, -1), ?_⟩
  intro h
  have h1 := congrFun h 1
  simp [gauge_smul_def, higgsVev] at h1
  exact hv (by linear_combination -h1 / 2)

/-- Unbroken subgroup ⊆ image(emEmbed): with `emEmbed_mem_unbroken` and `emEmbed_injective`, H ≅ U(1).
(Closed 2026-10-12 in OP-1 by the elementary 2×2 unitary argument: U₀₁=0, zU₁₁=1, det ⇒ U₀₀=z, column norm ⇒ U₁₀=0.) -/
theorem gauge_unbroken_eq_em (v0 : ℂ) (hv : v0 ≠ 0) :
    ∀ g ∈ unbroken (G := Gauge) (higgsVev v0), ∃ z : Circle, g = emEmbed z := by
  rintro ⟨U, z⟩ hg
  rw [MulAction.mem_stabilizer_iff, gauge_smul_def] at hg
  have h0 := congrFun hg 0
  have h1 := congrFun hg 1
  simp [higgsVev] at h0 h1
  have hz : (z : ℂ) ≠ 0 := Circle.coe_ne_zero z
  have hU01 : U.1 0 1 = 0 := by
    rcases h0 with h | h
    · exact h
    · exact absurd h hv
  have hU11 : (z:ℂ) * U.1 1 1 = 1 := by
    have : ((z:ℂ) * U.1 1 1 - 1) * v0 = 0 := by linear_combination h1
    rcases mul_eq_zero.1 this with h | h
    · linear_combination h
    · exact absurd h hv
  have hdet := (Matrix.mem_specialUnitaryGroup_iff.1 U.2).2
  rw [Matrix.det_fin_two, hU01] at hdet
  have hun := (Matrix.mem_unitaryGroup_iff'.1 (Matrix.mem_specialUnitaryGroup_iff.1 U.2).1)
  have hu11 := congrFun (congrFun hun 1) 1
  have hu00 := congrFun (congrFun hun 0) 0
  simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.star_apply, hU01] at hu11 hu00
  -- U00 = z
  have hU00 : U.1 0 0 = z := by
    have : U.1 0 0 * U.1 1 1 = 1 := by simpa using hdet
    have h2 : (z:ℂ) * U.1 1 1 = 1 := hU11
    have hne : U.1 1 1 ≠ 0 := by rintro h; simp [h] at h2
    exact mul_right_cancel₀ hne (by rw [this, h2])
  -- U10 = 0 from column 0 norm: star U10 * U10 = 0 after |U00|=1
  have hU10 : U.1 1 0 = 0 := by
    rw [hU00] at hu00
    have hzz : (starRingEnd ℂ) (z:ℂ) * z = 1 := by
      rw [mul_comm, Complex.mul_conj, Complex.normSq_eq_norm_sq]; simp
    have : (starRingEnd ℂ) (U.1 1 0) * U.1 1 0 = 0 := by linear_combination hu00 - hzz
    rw [mul_comm, Complex.mul_conj] at this
    exact_mod_cast Complex.normSq_eq_zero.1 (by exact_mod_cast this)
  refine ⟨z, ?_⟩
  refine Prod.ext ?_ rfl
  apply Subtype.ext
  ext i j
  fin_cases i <;> fin_cases j <;> simp [emEmbed, diagMat, hU00, hU01, hU10, Circle.coe_inv]
  exact eq_inv_of_mul_eq_one_right hU11

/-- H = image of the photon U(1), both directions. -/
theorem gauge_unbroken_iff_em (v0 : ℂ) (hv : v0 ≠ 0) (g : Gauge) :
    g ∈ unbroken (G := Gauge) (higgsVev v0) ↔ ∃ z : Circle, g = emEmbed z :=
  ⟨gauge_unbroken_eq_em v0 hv g, by rintro ⟨z, rfl⟩; exact emEmbed_mem_unbroken v0 z⟩

/-- The Higgs vev `(0, 1)` as an order parameter for `SU(2) × U(1)`. -/
noncomputable instance gaugeOP : OrderParameter Gauge (Fin 2 → ℂ) where
  v := higgsVev 1
  broken := gauge_broken 1 one_ne_zero

/-! ## (c) Spacetime instance: GL(4,ℝ) on bilinear forms by congruence -/

/-- The group GL(4,ℝ) of invertible real 4×4 matrices. -/
abbrev GL4 := (Matrix (Fin 4) (Fin 4) ℝ)ˣ
/-- Wrapper (so the default left-multiplication action of `GL4` on matrices does not clash
with the congruence action). -/
@[ext] structure Form4 where
  /-- The underlying real 4×4 matrix of the bilinear form. -/
  m : Matrix (Fin 4) (Fin 4) ℝ

/-- Congruence action B ↦ g B gᵀ (on all 4×4 matrices; preserves symmetric ones). -/
def cact (g : GL4) (B : Form4) : Form4 :=
  ⟨(g : Matrix (Fin 4) (Fin 4) ℝ) * B.m * (g : Matrix (Fin 4) (Fin 4) ℝ)ᵀ⟩

/-- Congruence action `B ↦ g B gᵀ` of GL(4,ℝ) on `Form4`. -/
instance congrAction : MulAction GL4 Form4 where
  smul := cact
  one_smul B := by
    show cact 1 B = B
    ext1; simp [cact]
  mul_smul g h B := by
    show cact (g * h) B = cact g (cact h B)
    ext1; simp [cact, Matrix.transpose_mul, Matrix.mul_assoc]

/-- Unfolded form of the congruence action: `(g • B).m = g B.m gᵀ`. -/
theorem congr_smul_def (g : GL4) (B : Form4) :
    (g • B).m = (g : Matrix (Fin 4) (Fin 4) ℝ) * B.m * (g : Matrix (Fin 4) (Fin 4) ℝ)ᵀ := rfl

/-- The congruence action preserves symmetric forms. -/
theorem congr_preserves_symm (g : GL4) (B : Form4) (hB : B.m.IsSymm) : (g • B).m.IsSymm := by
  unfold Matrix.IsSymm
  rw [congr_smul_def, Matrix.transpose_mul, Matrix.transpose_mul,
    Matrix.transpose_transpose, hB.eq, Matrix.mul_assoc]

/-- Minkowski form η = diag(1,-1,-1,-1), signature (1,3).

Also known as: eta, η=diag(1,−1,−1,−1) Minkowski metric Form4.
-/
def minkowskiForm : Form4 := ⟨Matrix.diagonal ![1, -1, -1, -1]⟩

/-- Lorentz group as a set, in the congruence convention g η gᵀ = η. -/
def lorentzSet : Set GL4 :=
  {g | (g : Matrix (Fin 4) (Fin 4) ℝ) * minkowskiForm.m * (g : Matrix (Fin 4) (Fin 4) ℝ)ᵀ = minkowskiForm.m}

/-- The stabiliser of the Minkowski form under congruence is exactly `lorentzSet`. -/
theorem unbroken_minkowskiForm_eq_lorentz : (unbroken (G := GL4) minkowskiForm : Set GL4) = lorentzSet := by
  ext g
  show g • minkowskiForm = minkowskiForm ↔ _
  rw [Form4.ext_iff, congr_smul_def]
  rfl

/-- Equivalence with the textbook convention gᵀ η g = η (uses η² = 1). -/
theorem lorentz_iff_transpose (g : GL4) :
    g ∈ lorentzSet ↔ (g : Matrix (Fin 4) (Fin 4) ℝ)ᵀ * minkowskiForm.m * (g : Matrix (Fin 4) (Fin 4) ℝ)
      = minkowskiForm.m := by
  have hη : minkowskiForm.m * minkowskiForm.m = 1 := by
    simp only [minkowskiForm, Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
    congr 1; ext i; fin_cases i <;> simp
  have key : ∀ A : Matrix (Fin 4) (Fin 4) ℝ, A * minkowskiForm.m * Aᵀ = minkowskiForm.m → Aᵀ * minkowskiForm.m * A = minkowskiForm.m := by
    intro A hA
    have h1 : (minkowskiForm.m * A * minkowskiForm.m) * Aᵀ = 1 := by
      calc (minkowskiForm.m * A * minkowskiForm.m) * Aᵀ = minkowskiForm.m * (A * minkowskiForm.m * Aᵀ) := by simp [Matrix.mul_assoc]
        _ = 1 := by rw [hA, hη]
    have h2 : Aᵀ * (minkowskiForm.m * A * minkowskiForm.m) = 1 := mul_eq_one_comm.1 h1
    calc Aᵀ * minkowskiForm.m * A = (Aᵀ * (minkowskiForm.m * A * minkowskiForm.m)) * minkowskiForm.m := by
          simp [Matrix.mul_assoc, hη]
      _ = minkowskiForm.m := by rw [h2, Matrix.one_mul]
  constructor
  · exact key _
  · intro h
    have := key (g : Matrix (Fin 4) (Fin 4) ℝ)ᵀ (by simpa using h)
    simp only [Matrix.transpose_transpose] at this
    exact this

/-- The Minkowski form is not fixed by all of GL(4,ℝ). -/
theorem spacetime_broken : unbroken (G := GL4) minkowskiForm ≠ ⊤ := by
  rw [broken_iff]
  refine ⟨Units.mk0 (2 : ℝ) two_ne_zero • (1 : GL4), ?_⟩
  intro h
  have h1 := congrFun (congrFun (congrArg Form4.m h) 0) 0
  rw [congr_smul_def] at h1
  simp [minkowskiForm, Units.smul_def, Matrix.diagonal, Matrix.smul_apply] at h1
  norm_num at h1

/-- The Minkowski form as an order parameter for GL(4,ℝ) acting by congruence. -/
instance spacetimeOP : OrderParameter GL4 Form4 where
  v := minkowskiForm
  broken := spacetime_broken

/-! ## (d) Shared structure -/

/-- Both sectors instantiate the same `OrderParameter` class, each with a nontrivial broken
phase. This is a FORMAL analogy (same Landau pattern); it is not a claim of one physical field. -/
theorem both_broken :
    (∃ g : Gauge, g • OrderParameter.v (G := Gauge) (V := Fin 2 → ℂ) ≠ OrderParameter.v Gauge) ∧
    (∃ g : GL4, g • OrderParameter.v (G := GL4) (V := Form4) ≠ OrderParameter.v GL4) :=
  ⟨orbit_nontrivial_of_broken, orbit_nontrivial_of_broken⟩

end PositiveGeometryEmergentSpaceTime.OrderParam

/-! ## Axiom audit -/
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.unbroken_invariant
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.broken_iff
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.vacuumManifold
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.orbit_nontrivial_of_broken
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.gaugeAction
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.diagMat_mem
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.emEmbed_mem_unbroken
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.emEmbed_injective
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.gauge_broken
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.gauge_unbroken_eq_em
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.gaugeOP
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.congrAction
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.congr_preserves_symm
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.unbroken_minkowskiForm_eq_lorentz
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.lorentz_iff_transpose
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.spacetime_broken
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.spacetimeOP
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.both_broken
#print axioms PositiveGeometryEmergentSpaceTime.OrderParam.gauge_unbroken_iff_em
