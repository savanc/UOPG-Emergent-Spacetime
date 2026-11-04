/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# TRIALITY-WHY (2026-10-23): is there a consistency reason to gauge baryon triality?

Continuous-mode own pick (author approved 2026-10-23).
Prereg `prereg/TRIALITY-WHY-2026-10-23.md`; checker `sims/triwhy/triwhy_checker.py`.

Generation-universal `Z_k` charges of the SM Weyl fields (left-handed convention):
`qQ, qL, qH` free; the Yukawas `Q dᶜ H`, `Q uᶜ H*`, `L eᶜ H`, `L νᶜ H*` fix
`qU = qH - qQ`, `qD = -qQ - qH`, `qE = -qL - qH`, `qN = qH - qL`.

Results (standard axioms only; see lean/AxiomsAll_output.txt):
* `sphaleron_eq_wwx`, `exact_iff_wwx`: invariance of the SU(2) instanton ('t Hooft) vertex under `Z_k`
  is the same integer as the Ibáñez–Ross SU(2)²–Z_k linear anomaly sum: the gauge-anomaly condition is
  literally the condition for the global symmetry to be exact (TAUTOLOGICAL-CONDITION).
* `ccx_zero`: the SU(3)²–Z_k sum vanishes for every Yukawa-compatible charge.
* `grav_nuc_zero`, `grav_no_nuc`: the gravity²–Z_k sum per generation is 0 with νᶜ, `qL - qH` without.
* `doublet_charge_Y_shift`: the doublet charge `3 qQ + qL` is invariant under hypercharge shifts.
* `window_iff`: `k ∣ N c ↔ k / gcd k c ∣ N` — the window of any `Z_k` is the multiples of its order
  on the doublet charge (rival ORDER rule).
* `b3_exact_iff`, `z9_exact_iff`: baryon triality (hep-ph/0512163 charges) and the `Z_9` of `3B`
  are exact iff `3 ∣ N`; `b3_eq_neg_BminusTwoY`: B3 = −(B − 2Y) mod 3 field by field.
* `qqql_*`: `QQQL` is SM-gauge-invariant, has ΔB = 1 and B3 charge ≢ 0: the "break" branch of the
  no-global-symmetries dichotomy is always available, so the dichotomy constrains no N (`qg_window`).
* `real_cube_root_one`, `torus_z3_trivial`: no nontrivial `Z_3` acts through a real torus
  (positive-geometry column torus), so the geometry side is triality-blind.
* `null_count_d3`, `null_count_singleton`: 12 of the 170 declared `(k, c)` pairs single out N = 3;
  32 single out some N in {3, 4, 5}.
-/

namespace PositiveGeometryEmergentSpaceTime.TrialityWhy

/-- Doublet charge per generation: `N_c = 3` quark doublets and one lepton doublet. -/
def doubletCharge (qQ qL : ℤ) : ℤ := 3 * qQ + qL

/-- Charge carried by the SU(2) instanton ('t Hooft) vertex for `N` generations
(one zero mode per doublet per generation). -/
def sphaleronCharge (qQ qL : ℤ) (N : ℕ) : ℤ := (N : ℤ) * doubletCharge qQ qL

/-- Ibáñez–Ross SU(2)²–Z_k linear sum: Σ over SU(2) doublets of the charge, `N` generations. -/
def wwxSum (qQ qL : ℤ) (N : ℕ) : ℤ :=
  ∑ _g ∈ Finset.range N, ((∑ _c ∈ Finset.range 3, qQ) + qL)

/-- The instanton-vertex charge equals the Ibáñez–Ross SU(2)²–Z_k sum. -/
theorem sphaleron_eq_wwx (qQ qL : ℤ) (N : ℕ) : sphaleronCharge qQ qL N = wwxSum qQ qL N := by
  simp [sphaleronCharge, wwxSum, doubletCharge, Finset.sum_const, Finset.card_range]

/-- `k` divides the instanton-vertex charge iff it divides the SU(2)²–Z_k sum. -/
theorem exact_iff_wwx (k qQ qL : ℤ) (N : ℕ) :
    k ∣ sphaleronCharge qQ qL N ↔ k ∣ wwxSum qQ qL N := by
  rw [sphaleron_eq_wwx]

/-- SU(3)²–Z_k sum per generation (`Q` counts twice, `uᶜ`, `dᶜ` once) with Yukawa-fixed charges. -/
def ccxSum (qQ qH : ℤ) : ℤ := 2 * qQ + (qH - qQ) + (-qQ - qH)

/-- With Yukawa-fixed charges the SU(3)²–Z_k sum vanishes identically. -/
theorem ccx_zero (qQ qH : ℤ) : ccxSum qQ qH = 0 := by unfold ccxSum; ring

/-- Gravity²–Z_k sum per generation (all Weyl components), without νᶜ. -/
def gravSum (qQ qL qH : ℤ) : ℤ :=
  6 * qQ + 3 * (qH - qQ) + 3 * (-qQ - qH) + 2 * qL + (-qL - qH)

/-- Without νᶜ, the gravity²–Z_k sum is `q_L − q_H`. -/
theorem grav_no_nuc (qQ qL qH : ℤ) : gravSum qQ qL qH = qL - qH := by unfold gravSum; ring

/-- Adding a νᶜ of charge `q_H − q_L` cancels the gravity²–Z_k sum. -/
theorem grav_nuc_zero (qQ qL qH : ℤ) : gravSum qQ qL qH + (qH - qL) = 0 := by
  rw [grav_no_nuc]; ring

/-- Integer hypercharge `6Y`: `Q ↦ 1`, `L ↦ -3`. A hypercharge shift leaves the doublet charge
  fixed. -/
theorem doublet_charge_Y_shift (qQ qL r : ℤ) :
    doubletCharge (qQ + r) (qL - 3 * r) = doubletCharge qQ qL := by
  unfold doubletCharge; ring

/-- Window rule: `k ∣ N c` iff the order `k / gcd k c` divides `N`. -/
theorem window_iff (k c N : ℕ) (hk : 0 < k) : k ∣ N * c ↔ k / Nat.gcd k c ∣ N := by
  have hg : 0 < Nat.gcd k c := Nat.gcd_pos_of_pos_left c hk
  have hcop : Nat.Coprime (k / Nat.gcd k c) (c / Nat.gcd k c) := Nat.coprime_div_gcd_div_gcd hg
  have hk' : k = Nat.gcd k c * (k / Nat.gcd k c) := (Nat.mul_div_cancel' (Nat.gcd_dvd_left k c)).symm
  have hc' : c = Nat.gcd k c * (c / Nat.gcd k c) := (Nat.mul_div_cancel' (Nat.gcd_dvd_right k c)).symm
  constructor
  · intro h
    have h2 : Nat.gcd k c * (k / Nat.gcd k c) ∣ Nat.gcd k c * (N * (c / Nat.gcd k c)) := by
      have e : N * c = Nat.gcd k c * (N * (c / Nat.gcd k c)) := by
        conv_lhs => rw [hc']
        ring
      rw [← hk', ← e]; exact h
    have h3 := Nat.dvd_of_mul_dvd_mul_left hg h2
    exact hcop.dvd_of_dvd_mul_right h3
  · intro h
    rw [hk']
    have e : N * c = Nat.gcd k c * (N * (c / Nat.gcd k c)) := by
      conv_lhs => rw [hc']
      ring
    rw [e]
    exact Nat.mul_dvd_mul_left _ (Dvd.dvd.mul_right h _)

/-- Baryon triality B3 = R₃L₃ (hep-ph/0512163 eq. 2.17, (m,n,p) = (1,0,1)): qQ = 0, qL = −1. -/
theorem b3_exact_iff (N : ℕ) : (3 : ℤ) ∣ sphaleronCharge 0 (-1) N ↔ 3 ∣ N := by
  unfold sphaleronCharge doubletCharge
  constructor
  · intro h; omega
  · intro h; omega

/-- `Z_9` acting by `3B` (qQ = 1, qL = 0): exact iff 3 ∣ N (cf. 1808.00009). -/
theorem z9_exact_iff (N : ℕ) : (9 : ℤ) ∣ sphaleronCharge 1 0 N ↔ 3 ∣ N := by
  unfold sphaleronCharge doubletCharge
  constructor
  · intro h; omega
  · intro h; omega

/-- `B − L` (×3; with νᶜ): doublet charge 0, exact for every N. -/
theorem bminusl_doublet_zero : doubletCharge 1 (-3) = 0 := by unfold doubletCharge; norm_num

/-- B3 charges equal −(B − 2Y) field by field (Q, uᶜ, dᶜ, L, eᶜ), physical Y. -/
theorem b3_eq_neg_BminusTwoY :
    ([(1/3 : ℚ) - 2 * (1/6), -1/3 - 2 * (-2/3), -1/3 - 2 * (1/3), 0 - 2 * (-1/2),
        0 - 2 * 1] : List ℚ)
      = [0, 1, -1, 1, -2] ∧
    ([0, -1, 1, -1, 2] : List ℤ).map (fun x => -x) = [0, 1, -1, 1, -2] := by
  constructor <;> norm_num

/-- `QQQL`: hypercharge sum 0, colour ε-contraction (three triplets), four doublets (even). -/
theorem qqql_gauge_invariant : 3 * (1/6 : ℚ) + (-1/2) = 0 ∧ 3 % 3 = 0 ∧ 4 % 2 = 0 := by norm_num

/-- Arithmetic: `3 · (1/3) = 1` (QQQL changes baryon number by 1). -/
theorem qqql_deltaB : 3 * (1/3 : ℚ) = 1 := by norm_num

/-- B3 charge of `QQQL` is `3·0 + (−1) = −1 ≢ 0 (mod 3)`: the operator breaks B3. -/
theorem qqql_breaks_b3 : ¬ (3 : ℤ) ∣ (3 * 0 + (-1)) := by decide

/-- No-global-symmetries dichotomy: an exact global symmetry must be gauged or broken. With the break
branch available (`qqql_breaks_b3`) the dichotomy holds for every N, so its window is the SM core window. -/
def qgOK (exact gauged broken : Prop) : Prop := exact → gauged ∨ broken

/-- With the break branch available, the no-global-symmetry condition is automatic, so the window is
  `1 ≤ N ≤ 5`. -/
theorem qg_window (N : ℕ) :
    (1 ≤ N ∧ N ≤ 5 ∧ qgOK ((3 : ℤ) ∣ sphaleronCharge 0 (-1) N) False (¬ (3 : ℤ) ∣ (3 * 0 + (-1))))
      ↔ (1 ≤ N ∧ N ≤ 5) := by
  constructor
  · rintro ⟨h1, h5, _⟩; exact ⟨h1, h5⟩
  · rintro ⟨h1, h5⟩; exact ⟨h1, h5, fun _ => Or.inr qqql_breaks_b3⟩

/-- A real number with `x³ = 1` is `1`. -/
theorem real_cube_root_one (x : ℝ) (h : x ^ 3 = 1) : x = 1 := by
  have h' : (x - 1) * (x ^ 2 + x + 1) = 0 := by ring_nf; linarith
  rcases mul_eq_zero.mp h' with h0 | h0
  · linarith
  · nlinarith [sq_nonneg (x + 1/2)]

/-- Any `Z_3` acting through a real torus `(ℝˣ)ⁿ` (column torus of Gr(k,n)(ℝ)) is trivial. -/
theorem torus_z3_trivial (n : ℕ) (t : Fin n → ℝ) (h : ∀ i, t i ^ 3 = 1) : ∀ i, t i = 1 :=
  fun i => real_cube_root_one (t i) (h i)

/-- The cyclic symmetry of Gr⁺(k,n) has a `Z_3` subgroup only when 3 ∣ n: not constant in n. -/
theorem cyclic_z3_not_family_constant : 3 ∣ 6 ∧ ¬ 3 ∣ 5 := by decide

/-- Declared null family: pairs (k, c) with 2 ≤ k ≤ 18 and 0 ≤ c < k (170 pairs). -/
def nullFamily : Finset (Σ _k : ℕ, ℕ) := (Finset.Icc 2 18).sigma (fun k => Finset.range k)

set_option maxRecDepth 100000 in
/-- The declared null family has 170 pairs. -/
theorem null_card : nullFamily.card = 170 := by decide

set_option maxRecDepth 100000 in
/-- Exactly 12 pairs of the null family have `k / gcd(k, c) = 3`. -/
theorem null_count_d3 :
    (nullFamily.filter (fun p => p.1 / Nat.gcd p.1 p.2 = 3)).card = 12 := by decide

set_option maxRecDepth 100000 in
/-- Exactly 32 pairs of the null family have `k / gcd(k, c) ∈ {3, 4, 5}`. -/
theorem null_count_singleton :
    (nullFamily.filter (fun p => p.1 / Nat.gcd p.1 p.2 ∈ ({3, 4,
        5} : Finset ℕ))).card = 32 := by decide

/-- Bundle. -/
theorem triality_why_summary :
    (∀ k qQ qL N, (k ∣ sphaleronCharge qQ qL N ↔ k ∣ wwxSum qQ qL N)) ∧
    (∀ N : ℕ, ((3 : ℤ) ∣ sphaleronCharge 0 (-1) N ↔ 3 ∣ N)) ∧
    ¬ (3 : ℤ) ∣ (3 * 0 + (-1)) ∧
    (∀ x : ℝ, x ^ 3 = 1 → x = 1) ∧
    (nullFamily.filter (fun p => p.1 / Nat.gcd p.1 p.2 = 3)).card = 12 :=
  ⟨exact_iff_wwx, b3_exact_iff, qqql_breaks_b3, real_cube_root_one, null_count_d3⟩

end PositiveGeometryEmergentSpaceTime.TrialityWhy
