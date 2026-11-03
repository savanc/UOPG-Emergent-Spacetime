/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# BH-2: massive spinor helicity (Arkani-Hamed–Huang–Huang 1709.04891), little group, x-factor

Conventions (ours; consistent with AHH/Ochirov 1802.06730 up to signs): a massive spinor pair is a pair of
2×2 complex matrices `Λ, Λ̃` (row = Lorentz index α, column = little-group index I) with `p = Λ Λ̃ᵀ`.
`ε = !![0,1;-1,0]`. Brackets `⟨1 2⟩ := Λ₁ᵀ ε Λ₂` (a 2×2 matrix in the little-group indices I, J).

* (a) existence of the decomposition for `det p = m² ≠ 0`, rank 2; real future-timelike case `p = Λ Λᴴ`.
* (b) SL(2) / SU(2) little-group covariance; SL(2,ℂ) Lorentz invariance of brackets; `⟨1 1⟩ = det Λ · ε`.
* (c) equal-mass condition `det(p₁+k) = det p₁ ⇔ ⟨3|p₁|3] = 0`; existence, uniqueness, ζ-independence and
  little-group weight −2 of the x-factor `p₁ ε λ̃₃ = m x λ₃`.
* (d) scalarised minimal-coupling uniqueness: an amplitude that is a polynomial in `1/m` (the CHKL basis
  term `a` carries `m^{-a}`) stays bounded as `m → 0` iff it has degree 0, i.e. only `g₀` survives.
Pre-registration: `prereg/BH-2-massive-spinor-helicity-2026-10-12.md`.
-/

open Matrix Complex Filter
open scoped MatrixGroups

namespace PositiveGeometryEmergentSpaceTime.MassiveSpinor

/-- 2×2 complex matrices (massive momenta in bispinor form).

Also known as: M, 2×2 complex matrix (little-group / spinor).
-/
abbrev SpinorMat := Matrix (Fin 2) (Fin 2) ℂ

/-- The SL(2) invariant `ε`. -/
def eps : SpinorMat := !![0, 1; -1, 0]

/-! ## (a) decomposition -/

/-- **(a)** Every `p` with `det p = m²`, `m ≠ 0`, is `Λ Λ̃ᵀ` with `det Λ = det Λ̃ = m` (AHH eq.
  13–14). -/
theorem exists_massive_decomp (p : SpinorMat) {m : ℂ} (hm : m ≠ 0) (hp : p.det = m ^ 2) :
    ∃ L Lt : SpinorMat, p = L * Ltᵀ ∧ L.det = m ∧ Lt.det = m := by
  obtain ⟨c, hc⟩ := IsAlgClosed.exists_eq_mul_self m
  have hc0 : c ≠ 0 := by rintro rfl; simp at hc; exact hm hc
  refine ⟨c • 1, (c⁻¹ • p)ᵀ, ?_, ?_, ?_⟩
  · rw [transpose_transpose, smul_mul_assoc, one_mul, smul_smul, mul_inv_cancel₀ hc0, one_smul]
  · rw [det_smul, det_one]; simp [hc, sq]
  · rw [det_transpose, det_smul, hp]; simp
    rw [hc]; field_simp

/-- A massive momentum (`det ≠ 0`) has rank 2 (massless ones have rank ≤ 1: `PositiveGeometryEmergentSpaceTime.LightCone`). -/
theorem massive_rank_two (p : SpinorMat) (hp : p.det ≠ 0) : p.rank = 2 := by
  have : IsUnit p := (isUnit_iff_isUnit_det p).mpr (Ne.isUnit hp)
  simpa using rank_of_isUnit p this

/-- M1's σ-map (`PositiveGeometryEmergentSpaceTime.sigma`), restated locally to avoid import coupling. -/
noncomputable def sig (v : Fin 4 → ℝ) : SpinorMat :=
  !![((v 0 + v 3 : ℝ) : ℂ), (v 1 : ℂ) - (v 2 : ℂ) * I; (v 1 : ℂ) + (v 2 : ℂ) * I,
      ((v 0 - v 3 : ℝ) : ℂ)]

set_option linter.unusedVariables false in
set_option linter.unusedSectionVars false in
/-- **(a, real)** A real future-timelike momentum `σ(v)` with `v⁰+v³ > 0`, `η(v) = m²`, `m > 0` is `Λ Λᴴ` with
`det Λ = m` (λ̃ = λ*: the Lorentzian reality condition), via an explicit Cholesky factor. -/
@[nolint unusedArguments]
theorem exists_real_decomp (v : Fin 4 → ℝ) {m : ℝ} (hm : 0 < m) (hpos : 0 < v 0 + v 3)
    (heta : v 0 ^ 2 - v 1 ^ 2 - v 2 ^ 2 - v 3 ^ 2 = m ^ 2) :
    ∃ L : SpinorMat, sig v = L * Lᴴ ∧ L.det = m := by
  set s := Real.sqrt (v 0 + v 3) with hs
  have hs0 : 0 < s := Real.sqrt_pos.mpr hpos
  have hss : s * s = v 0 + v 3 := Real.mul_self_sqrt hpos.le
  refine ⟨!![(s : ℂ), 0; ((v 1 : ℂ) + (v 2 : ℂ) * I) / s, (m : ℂ) / s], ?_, ?_⟩
  · have hsC : (s : ℂ) ≠ 0 := by exact_mod_cast hs0.ne'
    ext i j; fin_cases i <;> fin_cases j <;>
      simp [sig, Matrix.mul_apply, Fin.sum_univ_two, conjTranspose_apply] <;>
      apply Complex.ext <;> simp [Complex.div_re, Complex.div_im] <;> field_simp <;>
      nlinarith [hss, heta]
  · rw [det_fin_two]; simp
    have hsC : (s : ℂ) ≠ 0 := by exact_mod_cast hs0.ne'
    field_simp

/-! ## (b) little group and brackets -/

/-- Little-group action `(Λ, Λ̃) ↦ (Λ W, Λ̃ W⁻ᵀ)`, `W ∈ SL(2,ℂ)`, leaves `p` invariant. -/
theorem littleGroup_mom (L Lt : SpinorMat) (W : SL(2, ℂ)) :
    (L * W) * (Lt * (↑(W⁻¹) : SpinorMat)ᵀ)ᵀ = L * Ltᵀ := by
  rw [transpose_mul, transpose_transpose, mul_assoc, ← mul_assoc (W : SpinorMat)]
  rw [← Matrix.SpecialLinearGroup.coe_mul, mul_inv_cancel, Matrix.SpecialLinearGroup.coe_one,
      one_mul]

/-- ...and both determinants (so `det Λ = det Λ̃ = m` is a little-group-invariant gauge). -/
theorem littleGroup_det (L Lt : SpinorMat) (W : SL(2, ℂ)) :
    (L * W).det = L.det ∧ (Lt * (↑(W⁻¹) : SpinorMat)ᵀ).det = Lt.det := by
  refine ⟨?_, ?_⟩
  · rw [det_mul, W.2, mul_one]
  · rw [det_mul, det_transpose, (W⁻¹).2, mul_one]

/-- For `W ∈ SU(2)` (`W Wᴴ = 1`, `det W = 1`) the reality condition `Λ̃ = Λ*` is preserved: the real
little group is SU(2). -/
theorem littleGroup_SU2_real (L : SpinorMat) (W : SL(2,
    ℂ)) (hU : (W : SpinorMat) * (W : SpinorMat)ᴴ = 1) :
    L.map (starRingEnd ℂ) * (↑(W⁻¹) : SpinorMat)ᵀ = (L * W).map (starRingEnd ℂ) := by
  have hinv : (↑(W⁻¹) : SpinorMat) = (W : SpinorMat)ᴴ := by
    calc (↑(W⁻¹) : SpinorMat) = ↑(W⁻¹) * ((W : SpinorMat) * (W : SpinorMat)ᴴ) := by rw [hU, mul_one]
      _ = (↑(W⁻¹ * W) : SpinorMat) * (W : SpinorMat)ᴴ := by rw [Matrix.SpecialLinearGroup.coe_mul,
          mul_assoc]
      _ = (W : SpinorMat)ᴴ := by rw [inv_mul_cancel, Matrix.SpecialLinearGroup.coe_one, one_mul]
  rw [hinv, Matrix.map_mul]
  congr 1

/-- 2×2 identity: `Aᵀ ε A = det A · ε` (ε is SL(2)-invariant). -/
theorem transpose_eps_mul (A : SpinorMat) : Aᵀ * eps * A = A.det • eps := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps, Matrix.mul_apply, Fin.sum_univ_two, det_fin_two] <;> ring

/-- Angle bracket `⟨1^I 2^J⟩` as a little-group matrix.

Also known as: MassiveSpinor.br, ⟨L₁ L₂⟩ spinor angle bracket.
-/
def angleBracket (L1 L2 : SpinorMat) : SpinorMat := L1ᵀ * eps * L2

/-- **(b)** Little-group covariance: `⟨1 2⟩ ↦ W₁ᵀ ⟨1 2⟩ W₂`. -/
theorem angleBracket_covariant (L1 L2 W1 W2 : SpinorMat) : angleBracket (L1 * W1) (L2 * W2) = W1ᵀ * angleBracket L1 L2 * W2 := by
  simp only [angleBracket, transpose_mul, Matrix.mul_assoc]

/-- **(b)** Lorentz invariance: `A ∈ SL(2,ℂ)` acting on the α index leaves `⟨1 2⟩` unchanged. -/
theorem angleBracket_lorentz (L1 L2 : SpinorMat) (A : SL(2,
    ℂ)) : angleBracket ((A : SpinorMat) * L1) ((A : SpinorMat) * L2) = angleBracket L1 L2 := by
  have h := transpose_eps_mul (A : SpinorMat)
  rw [A.2, one_smul] at h
  simp only [angleBracket, transpose_mul]
  calc L1ᵀ * (A : SpinorMat)ᵀ * eps * ((A : SpinorMat) * L2) = L1ᵀ * ((A : SpinorMat)ᵀ * eps * (A : SpinorMat)) * L2 := by
        simp only [Matrix.mul_assoc]
    _ = L1ᵀ * eps * L2 := by rw [h]

/-- **(b)** `⟨1^I 1^J⟩ = det Λ · ε^{IJ}` (= m ε for det Λ = m; cf. Ochirov eq. 15 up to sign
  convention). -/
theorem angleBracket_self (L : SpinorMat) : angleBracket L L = L.det • eps := by
  exact transpose_eps_mul L

/-! ## (c) the x-factor -/

/-- `⟨a b⟩ = aᵀ ε b` on 2-spinors. -/
def ang (a b : Fin 2 → ℂ) : ℂ := a ⬝ᵥ (eps *ᵥ b)

/-- `p₁ ε λ̃₃` : the undotted spinor `p₁|3]`. -/
def u (p : SpinorMat) (lt : Fin 2 → ℂ) : Fin 2 → ℂ := p *ᵥ (eps *ᵥ lt)

/-- **(c)** Equal-mass kinematics: `det(p₁ + λ₃λ̃₃ᵀ) = det p₁ ⇔ ⟨3|p₁|3] = 0`, with `⟨3|p₁|3] := ⟨λ₃
  (p₁ ε λ̃₃)⟩`. -/
theorem det_add_null (p : SpinorMat) (l lt : Fin 2 → ℂ) :
    (p + vecMulVec l lt).det = p.det - ang l (u p lt) := by
  simp [det_fin_two, ang, u, eps, vecMulVec_apply, mulVec, dotProduct, Fin.sum_univ_two]; ring

/-- Rank-one update: `det(p + λ λ̃ᵀ) = det p` iff `⟨λ, u p λ̃⟩ = 0`. -/
theorem equalMass_iff (p : SpinorMat) (l lt : Fin 2 → ℂ) :
    (p + vecMulVec l lt).det = p.det ↔ ang l (u p lt) = 0 := by
  rw [det_add_null]; constructor <;> intro h <;> linear_combination -h

/-- The angle bracket is alternating: `⟨a, a⟩ = 0`. -/
lemma ang_self (a : Fin 2 → ℂ) : ang a a = 0 := by
  simp [ang, eps, mulVec, dotProduct, Fin.sum_univ_two]; ring

/-- The angle bracket is linear in its second argument: `⟨a, c b⟩ = c ⟨a, b⟩`. -/
lemma ang_smul_right (a b : Fin 2 → ℂ) (c : ℂ) : ang a (c • b) = c * ang a b := by
  simp only [ang, mulVec_smul, dotProduct_smul, smul_eq_mul]

/-- In two dimensions `⟨λ w⟩ = 0`, `λ ≠ 0` forces `w ∥ λ`. -/
theorem parallel_of_ang_zero {l w : Fin 2 → ℂ} (hl : l ≠ 0) (h : ang l w = 0) : ∃ μ : ℂ, w = μ • l := by
  have h' : l 0 * w 1 - l 1 * w 0 = 0 := by
    simpa [ang, eps, mulVec, dotProduct, Fin.sum_univ_two, sub_eq_add_neg, mul_comm] using h
  by_cases h0 : l 0 = 0
  · have h1 : l 1 ≠ 0 := by
      intro h1; exact hl (funext fun i => by fin_cases i <;> simp [h0, h1])
    refine ⟨w 1 / l 1, funext fun i => ?_⟩
    fin_cases i
    · simp; rw [h0] at h'; field_simp
      have : l 1 * w 0 = 0 := by linear_combination -h'
      rcases mul_eq_zero.mp this with h2 | h2
      · exact absurd h2 h1
      · simp [h2, h0]
    · simp; field_simp
  · refine ⟨w 0 / l 0, funext fun i => ?_⟩
    fin_cases i
    · simp; field_simp
    · simp; field_simp; linear_combination h'

/-- **(c)** Existence of the x-factor (AHH eq. 61): on equal-mass kinematics `p₁ ε λ̃₃ = m x λ₃`. -/
theorem x_exists (p : SpinorMat) {m : ℂ} (hm : m ≠ 0) {l lt : Fin 2 → ℂ} (hl : l ≠ 0)
    (heq : (p + vecMulVec l lt).det = p.det) : ∃ x : ℂ, u p lt = (m * x) • l := by
  obtain ⟨μ, hμ⟩ := parallel_of_ang_zero hl ((equalMass_iff p l lt).mp heq)
  exact ⟨μ / m, by rw [hμ]; congr 1; field_simp⟩

/-- **(c)** Uniqueness of `x`. -/
theorem x_unique {m x y : ℂ} (hm : m ≠ 0) {l w : Fin 2 → ℂ} (hl : l ≠ 0)
    (hx : w = (m * x) • l) (hy : w = (m * y) • l) : x = y := by
  obtain ⟨i, hi⟩ : ∃ i, l i ≠ 0 := by
    by_contra h; push Not at h; exact hl (funext h)
  have := congrFun (hx.symm.trans hy) i
  simp only [Pi.smul_apply, smul_eq_mul] at this
  have h2 : (m * (x - y)) * l i = 0 := by linear_combination this
  rcases mul_eq_zero.mp h2 with h | h
  · rcases mul_eq_zero.mp h with h | h
    · exact absurd h hm
    · exact sub_eq_zero.mp h
  · exact absurd h hi

/-- **(c)** Reference-spinor formula (AHH eq. 62): `x = ⟨ζ|p₁|3] / (m ⟨ζ 3⟩)` for any `ζ` with `⟨ζ 3⟩ ≠ 0`;
in particular it is independent of `ζ`. -/
theorem x_zeta (p : SpinorMat) {m x : ℂ} (hm : m ≠ 0) {l lt ζ : Fin 2 → ℂ}
    (hx : u p lt = (m * x) • l) (hζ : ang ζ l ≠ 0) : x = ang ζ (u p lt) / (m * ang ζ l) := by
  rw [hx, ang_smul_right]; field_simp

/-- **(c)** Little-group weight: under `(λ₃, λ̃₃) ↦ (t λ₃, t⁻¹ λ̃₃)` the x-factor goes to `t⁻² x`
(AHH: x carries one unit of helicity; with BH-1's `x_weight` convention, weight −2 in t). -/
theorem x_littleGroup (p : SpinorMat) {m x t : ℂ} (hm : m ≠ 0) (ht : t ≠ 0) {l lt : Fin 2 → ℂ}
    (hx : u p lt = (m * x) • l) : u p (t⁻¹ • lt) = (m * (t⁻¹ ^ 2 * x)) • (t • l) := by
  have : u p (t⁻¹ • lt) = t⁻¹ • u p lt := by simp only [u, mulVec_smul]
  rw [this, hx, smul_smul, smul_smul]; congr 1; field_simp

/-- The x-factor is invariant under the massive little group of particle 1 (it only sees `p₁`). -/
theorem x_massive_LG_blind (L Lt : SpinorMat) (W : SL(2, ℂ)) (lt : Fin 2 → ℂ) :
    u ((L * W) * (Lt * (↑(W⁻¹) : SpinorMat)ᵀ)ᵀ) lt = u (L * Ltᵀ) lt := by
  rw [littleGroup_mom]

/-! ## (d) scalarised minimal-coupling uniqueness (power counting in 1/m) -/

/-- **(d)** CHKL eq. 18/23: the basis term `a` (= `g_a ε^{2s−a}(x λ₃λ₃/m)^a`) carries `m^{-a}`. Writing the
amplitude at fixed dimensionless kinematics as `P(1/m)`, `P = Σ_a g_a c_a X^a`, it stays bounded along
`m = 1/n → 0` iff `deg P ≤ 0`, i.e. only the `a = 0` (minimal, pure x·ε) structure survives. -/
theorem bounded_iff_minimal (P : Polynomial ℂ) :
    (∃ C : ℝ, ∀ n : ℕ, ‖P.eval (n : ℂ)‖ ≤ C) ↔ P.degree ≤ 0 := by
  constructor
  · rintro ⟨C, hC⟩
    by_contra hdeg
    push Not at hdeg
    have ht : Tendsto (fun n : ℕ => ‖P.eval ((n : ℕ) : ℂ)‖) atTop atTop :=
      Polynomial.tendsto_norm_atTop P hdeg (z := fun n : ℕ => (n : ℂ))
        (by simpa using tendsto_natCast_atTop_atTop (R := ℝ))
    obtain ⟨n, hn⟩ := (ht.eventually (eventually_gt_atTop C)).exists
    exact absurd (hC n) (not_le.mpr hn)
  · intro h
    rw [Polynomial.eq_C_of_degree_le_zero h]
    exact ⟨‖P.coeff 0‖, fun n => by simp⟩

/-- Corollary: bounded high-energy behaviour forces every non-minimal coupling `g_a`, `a ≥ 1`, to
  vanish. -/
theorem nonminimal_vanish (P : Polynomial ℂ) (hb : ∃ C : ℝ, ∀ n : ℕ, ‖P.eval (n : ℂ)‖ ≤ C)
    {a : ℕ} (ha : 1 ≤ a) : P.coeff a = 0 := by
  have h := (bounded_iff_minimal P).mp hb
  apply Polynomial.coeff_eq_zero_of_degree_lt
  calc P.degree ≤ 0 := h
    _ < a := by exact_mod_cast ha

/-- Count of independent equal-mass 3-pt structures for spin s (AHH: 2s+1), i.e. the basis index
  set. -/
theorem num_structures (twoS : ℕ) : Fintype.card (Fin (twoS + 1)) = twoS + 1 := Fintype.card_fin _

end PositiveGeometryEmergentSpaceTime.MassiveSpinor
