/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT2

/-!
# STRUCT-3 / R3 — `N_gen` from consistency or a discrete geometric invariant

Also known as: generation count, N_g, number of families, STRUCT route R3, PJ-B1 (Euler count).

Result: NO-GO for `N_gen = 3`.
* ACC and Witten are blind to `N_gen` (anomalies are additive per generation).
* One-loop asymptotic freedom (CITED b₀ coefficients) gives `N_gen ≤ 8` for SU(3) and `N_gen ≤ 5` for SU(2)
  with one Higgs doublet.
* Kobayashi–Maskawa (CITED; observed CP violation as a structural input) gives `N_gen ≥ 3`.
* The window is `{3, 4, 5}`, so 3 is not selected. Discrete positive-geometry counts hit 3 only at tuned parameters.
-/

namespace PositiveGeometryEmergentSpaceTime.STRUCT3

/-- G1: one-generation ACC ⇒ every `N_gen`-fold sum of the four anomaly polynomials vanishes. -/
theorem acc_ngen_blind {N_c yQ yu yd yL ye : ℚ} (h : STRUCT2.ACCN N_c yQ yu yd yL ye) (N_gen : ℚ) :
    N_gen * (2 * yQ + yu + yd) = 0 ∧ N_gen * (N_c * yQ + yL) = 0 ∧
    N_gen * (2 * N_c * yQ + N_c * yu + N_c * yd + 2 * yL + ye) = 0 ∧
    N_gen * (2 * N_c * yQ ^ 3 + N_c * yu ^ 3 + N_c * yd ^ 3 + 2 * yL ^ 3 + ye ^ 3) = 0 := by
  obtain ⟨h1, h2, h3, h4⟩ := h; simp [h1, h2, h3, h4]

/-- G1: Witten with `N_gen` generations (`N_gen (N_c + 1)` doublets) holds for every `N_gen` once
  `N_c` is odd. -/
theorem witten_ngen_blind {N_c : ℕ} (h : Odd N_c) (N_gen : ℕ) : Even (N_gen * (N_c + 1)) :=
  (Nat.even_add_one.2 (Nat.not_even_iff_odd.2 h)).mul_left N_gen

/-- One-loop SU(3) coefficient with `N_gen` generations (CITED: b₀ = 11 − (2/3)·n_f, n_f = 2 N_gen).
Also known as: b0_SU3, b₀(SU(3)), β₀ QCD. -/
def b0SU3 (N_gen : ℕ) : ℚ := 11 - 4 / 3 * N_gen

/-- One-loop SU(2) coefficient with `N_gen` generations and one Higgs doublet (CITED: 22/3 − (4/3)N_gen − 1/6).
Also known as: b0_SU2, b₀(SU(2)_L), β₀ weak. -/
def b0SU2 (N_gen : ℕ) : ℚ := 22 / 3 - 4 / 3 * N_gen - 1 / 6

/-- Number of physical CP phases in the N_gen × N_gen CKM matrix (CITED: Kobayashi–Maskawa).
Also known as: KM phase count, (N−1)(N−2)/2. -/
def kmPhases (N_gen : ℕ) : ℕ := (N_gen - 1) * (N_gen - 2) / 2

/-- Planted: SM SU(2) value. -/
theorem b0SU2_three : b0SU2 3 = 19 / 6 := by norm_num [b0SU2]

/-- G2: AF(SU(3)) ⇔ N_gen ≤ 8 (n_f ≤ 16). -/
theorem af_SU3_iff (N_gen : ℕ) : 0 < b0SU3 N_gen ↔ N_gen ≤ 8 := by
  unfold b0SU3
  have e : (0 : ℚ) < 11 - 4 / 3 * N_gen ↔ ((4 * N_gen : ℕ) : ℚ) < (33 : ℕ) := by
    push_cast; constructor <;> intro h <;> linarith
  rw [e, Nat.cast_lt]; omega

/-- G2: AF(SU(2), one Higgs doublet) ⇔ N_gen ≤ 5. -/
theorem af_SU2_iff (N_gen : ℕ) : 0 < b0SU2 N_gen ↔ N_gen ≤ 5 := by
  unfold b0SU2
  have e : (0 : ℚ) < 22 / 3 - 4 / 3 * N_gen - 1 / 6 ↔ ((8 * N_gen : ℕ) : ℚ) < (43 : ℕ) := by
    push_cast; constructor <;> intro h <;> linarith
  rw [e, Nat.cast_lt]; omega

/-- G3: a CP-violating phase exists ⇔ N_gen ≥ 3. -/
theorem km_pos_iff (N_gen : ℕ) : 0 < kmPhases N_gen ↔ 3 ≤ N_gen := by
  unfold kmPhases
  constructor
  · intro h; by_contra hc
    interval_cases N_gen <;> simp_all
  · intro h
    apply Nat.div_pos _ (by norm_num)
    have h1 : 2 ≤ N_gen - 1 := by omega
    have h2 : 1 ≤ N_gen - 2 := by omega
    nlinarith

/-- G4: AF(SU(3)) ∧ AF(SU(2)) ∧ CP phase ⇔ N_gen ∈ {3, 4, 5}. -/
theorem ngen_window (N_gen : ℕ) :
    (0 < b0SU3 N_gen ∧ 0 < b0SU2 N_gen ∧ 0 < kmPhases N_gen) ↔ (3 ≤ N_gen ∧ N_gen ≤ 5) := by
  rw [af_SU3_iff, af_SU2_iff, km_pos_iff]; omega

/-- G4 (exclusion): N_gen = 3 and N_gen = 4 both pass, so the stack does not single out 3. -/
theorem three_not_selected_ngen :
    (0 < b0SU3 3 ∧ 0 < b0SU2 3 ∧ 0 < kmPhases 3) ∧ (0 < b0SU3 4 ∧ 0 < b0SU2 4 ∧ 0 < kmPhases 4) :=
  ⟨(ngen_window 3).2 (by norm_num), (ngen_window 4).2 (by norm_num)⟩

/-- G5: positroid cells of Gr≥0(1,n) number 2ⁿ − 1; this equals 3 only at the tuned value n = 2. -/
theorem cells_gr1_eq_three_iff (n : ℕ) : 2 ^ n - 1 = 3 ↔ n = 2 := by
  constructor
  · intro h
    have h4 : 2 ^ n = 2 ^ 2 := by have := Nat.one_le_two_pow (n := n); omega
    exact Nat.pow_right_injective (le_refl 2) h4
  · rintro rfl; rfl

/-- G5: the associahedron vertex count (Catalan number) is never 3. -/
theorem catalan_ne_three (n : ℕ) : catalan n ≠ 3 := by
  intro h
  have hc := succ_mul_catalan_eq_centralBinom n
  rw [h] at hc
  rcases Nat.lt_or_ge n 4 with hn | hn
  · interval_cases n <;> simp_all [Nat.centralBinom, Nat.choose]
  · have hb := Nat.four_pow_le_two_mul_self_mul_centralBinom n (by omega)
    rw [← hc] at hb
    have key : ∀ m, 4 ≤ m → 2 * m * ((m + 1) * 3) < 4 ^ m := by
      intro m hm
      induction m, hm using Nat.le_induction with
      | base => norm_num
      | succ k hk ih => rw [pow_succ]; nlinarith
    exact absurd hb (not_le.2 (key n hn))

end PositiveGeometryEmergentSpaceTime.STRUCT3
