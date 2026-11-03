/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# F-COULOMB — deformed-amplituhedron positivity leaves mass ratios continuous

Also known as: F-COULOMB, M-CB route, deformed amplituhedron (Arkani-Hamed–Flieger–Henn–Schreiber–Trnka,
arXiv:2311.10814, CITED).

The paper's one-loop deformed region (eqs. (7)–(8)) is a product of two wedges
`y > ρ z > 0, z > ρ̃ y > 0` and `w > η x > 0, x > η̃ w > 0`. Their derivation from the momentum-twistor
inequalities (1), (4)–(6) is CITED and checked numerically by the locked checker `sims/fcoulomb`. Here:
* a wedge is non-empty **iff** `ρ ρ̃ < 1` (an open condition);
* the dual-conformal cross-ratio `u = (1+ρρ̃)²/(4ρρ̃)` (eq. (21)) fills exactly `(1, ∞)`, an infinite continuum;
* the mass ratio `m₁/m₃` in eq. (22) and the shift ratio `ρ/ρ̃` are free for every allowed `u`.
Verdict: CONTINUOUS (NO-GO for quantisation by positivity). No axioms; no FRONTIER-AXIOM.
-/

namespace PositiveGeometryEmergentSpaceTime.FCoulomb

/-- Dual-conformal cross-ratio of eq. (21) as a function of `r = ρ ρ̃`. Also known as: u, v (with `r
  = η η̃`). -/
noncomputable def crossRatioU (r : ℝ) : ℝ := (1 + r) ^ 2 / (4 * r)

/-- Eq. (22) right-hand side: `(−s + m₁² + m₃²)² / (4 m₁² m₃²)`. Also known as: u(s, m₁, m₃). -/
noncomputable def crossRatioMass (s m1 m3 : ℝ) : ℝ := (-s + m1 ^ 2 + m3 ^ 2) ^ 2 / (4 * m1 ^ 2 * m3 ^ 2)

/-- Deformed wedge of eq. (7) (the (y, z) half; eq. (8) is the same with (x, w), η, η̃).
Also known as: deformed amplituhedron one-loop region, wedge. -/
def Wedge (rho rhot y z : ℝ) : Prop := 0 < y ∧ 0 < z ∧ rho * z < y ∧ rhot * y < z

/-- The wedge is non-empty iff `ρ ρ̃ < 1`: positivity imposes only an open inequality. -/
theorem wedge_nonempty_iff {rho rhot : ℝ} (h1 : 0 < rho) (h2 : 0 < rhot) :
    (∃ y z, Wedge rho rhot y z) ↔ rho * rhot < 1 := by
  constructor
  · rintro ⟨y, z, hy, hz, ha, hb⟩
    have : rho * (rhot * y) < rho * z := mul_lt_mul_of_pos_left hb h1
    nlinarith
  · intro h
    refine ⟨(rho + 1 / rhot) / 2, 1, ?_, one_pos, ?_, ?_⟩
    · positivity
    · have : rho < 1 / rhot := by rw [lt_div_iff₀ h2]; linarith
      linarith
    · have e : rhot * ((rho + 1 / rhot) / 2) = (rho * rhot + 1) / 2 := by field_simp
      rw [e]; linarith

/-- Every allowed `r ∈ (0, 1)` gives `u > 1`. -/
theorem crossRatio_gt_one {r : ℝ} (h0 : 0 < r) (h1 : r < 1) : 1 < crossRatioU r := by
  unfold crossRatioU
  rw [lt_div_iff₀ (by linarith)]
  nlinarith [sq_pos_of_pos (sub_pos.2 h1)]

/-- Every `u > 1` is realised by some allowed `r ∈ (0, 1)`. -/
theorem crossRatio_surj {u : ℝ} (hu : 1 < u) : ∃ r, 0 < r ∧ r < 1 ∧ crossRatioU r = u := by
  set a := Real.sqrt u with ha
  set b := Real.sqrt (u - 1) with hb
  have ha2 : a ^ 2 = u := Real.sq_sqrt (by linarith)
  have hb2 : b ^ 2 = u - 1 := Real.sq_sqrt (by linarith)
  have hb0 : 0 ≤ b := Real.sqrt_nonneg _
  have ha1 : 1 < a := by
    rw [ha]; rw [show (1 : ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_lt_sqrt (by norm_num) hu
  have hab : (a - b) * (a + b) = 1 := by nlinarith
  have hpos : 0 < a - b := by nlinarith
  have hlt : a - b < 1 := by nlinarith
  refine ⟨(a - b) ^ 2, by positivity, by nlinarith, ?_⟩
  unfold crossRatioU
  rw [div_eq_iff (by positivity)]
  have h1 : 1 + (a - b) ^ 2 = 2 * a * (a - b) := by nlinarith
  rw [h1, ← ha2]; ring

/-- The set of cross-ratios allowed by deformed positivity is exactly `(1, ∞)`. -/
theorem allowed_u_eq_Ioi :
    {u : ℝ | ∃ rho rhot,
        0 < rho ∧ 0 < rhot ∧ rho * rhot < 1 ∧ u = crossRatioU (rho * rhot)} = Set.Ioi 1 := by
  ext u; simp only [Set.mem_ofPred_eq, Set.mem_Ioi]
  constructor
  · rintro ⟨rho, rhot, h1, h2, h3, rfl⟩; exact crossRatio_gt_one (by positivity) h3
  · intro hu
    obtain ⟨r, hr0, hr1, hr⟩ := crossRatio_surj hu
    refine ⟨Real.sqrt r, Real.sqrt r, Real.sqrt_pos.2 hr0, Real.sqrt_pos.2 hr0, ?_, ?_⟩
    · rw [Real.mul_self_sqrt hr0.le]; exact hr1
    · rw [Real.mul_self_sqrt hr0.le, hr]

/-- Not quantised: the allowed cross-ratio set is infinite (a continuum). -/
theorem allowed_u_infinite :
    {u : ℝ | ∃ rho rhot,
        0 < rho ∧ 0 < rhot ∧ rho * rhot < 1 ∧ u = crossRatioU (rho * rhot)}.Infinite := by
  rw [allowed_u_eq_Ioi]; exact Set.Ioi_infinite 1

/-- The shift ratio `ρ/ρ̃` is free: any `q > 0` occurs together with any product `r > 0` (in
  particular every allowed `r ∈ (0, 1)`). -/
theorem rho_ratio_free {q r : ℝ} (hq : 0 < q) (hr0 : 0 < r) :
    ∃ rho rhot, 0 < rho ∧ 0 < rhot ∧ rho / rhot = q ∧ rho * rhot = r := by
  refine ⟨Real.sqrt (q * r), Real.sqrt (r / q), Real.sqrt_pos.2 (by positivity),
    Real.sqrt_pos.2 (by positivity), ?_, ?_⟩
  · rw [← Real.sqrt_div (by positivity)]
    rw [show q * r / (r / q) = q ^ 2 by field_simp, Real.sqrt_sq hq.le]
  · rw [← Real.sqrt_mul (by positivity), show q * r * (r / q) = r ^ 2 by field_simp,
      Real.sqrt_sq hr0.le]

/-- The physical mass ratio is free: for any allowed `u > 1` and any `q > 0` there is kinematics
`(s, m₁, m₃)` with `m₁/m₃ = q` satisfying eq. (22). -/
theorem mass_ratio_free {u q : ℝ} (hu : 1 < u) (hq : 0 < q) :
    ∃ s m1 m3, 0 < m1 ∧ 0 < m3 ∧ m1 / m3 = q ∧ crossRatioMass s m1 m3 = u := by
  refine ⟨q ^ 2 + 1 - 2 * q * Real.sqrt u, q, 1, hq, one_pos, by simp, ?_⟩
  unfold crossRatioMass
  have hs : Real.sqrt u ^ 2 = u := Real.sq_sqrt (by linarith)
  rw [div_eq_iff (by positivity)]
  have : -(q ^ 2 + 1 - 2 * q * Real.sqrt u) + q ^ 2 + 1 ^ 2 = 2 * q * Real.sqrt u := by ring
  rw [this]; nlinarith [hs]

/-- Bundle (F-COULOMB verdict CONTINUOUS): open existence condition, continuum of cross-ratios, free
  ratios. -/
theorem fcoulomb_continuous :
    (∀ rho rhot : ℝ, 0 < rho → 0 < rhot → ((∃ y z, Wedge rho rhot y z) ↔ rho * rhot < 1)) ∧
    {u : ℝ | ∃ rho rhot,
        0 < rho ∧ 0 < rhot ∧ rho * rhot < 1 ∧ u = crossRatioU (rho * rhot)} = Set.Ioi 1 ∧
    (∀ u q : ℝ, 1 < u → 0 < q → ∃ s m1 m3,
        0 < m1 ∧ 0 < m3 ∧ m1 / m3 = q ∧ crossRatioMass s m1 m3 = u) :=
  ⟨fun _ _ h1 h2 => wedge_nonempty_iff h1 h2, allowed_u_eq_Ioi,
      fun _ _ hu hq => mass_ratio_free hu hq⟩

end PositiveGeometryEmergentSpaceTime.FCoulomb
