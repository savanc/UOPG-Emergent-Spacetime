import PositiveGeometryEmergentSpaceTime.HgDim2
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-!
# CappedForman — ℚ core of the capped-Forman bound (CAPPED-FORMAN-1, 2026-10-31)

Paper: papers/paper-curvature/main.tex, Prop. `prop:capped` (κ ≥ B := 1 − Σ_F min(3, k_F − 3)/(D + 1) on an edge of a
simple D-polytope) and Conj. `conj:capped` (equality). Audit: notes/CAPPED-FORMAN-1-proof-audit-2026-10-31.md.

* `face_term_le`, `face_term_max`: the per-face weight optimisation g_k(m) = m − 2|1 − m| − (k − 3) m over m ≥ 0 has
  maximum exactly 1 − min(3, k − 3), attained at m = 1 (k ≤ 6) or m = 0 (k ≥ 6). This is the algebra behind reading the
  capped bound as a maximised weighted Forman curvature (Jost–Münch 2110.04554 §5; the identification of g_k with their
  per-face term is ARGUED in the audit note, not formalised).
* `capped_ge_forman`: B ≥ κ_F/(D + 1) (the cap only raises the classical Forman bound) and `capped_eq_forman_iff`:
  equality iff every face has k ≤ 6.
Not formalised: the inequality κ ≥ B itself (paper-proved; also Jost–Münch Cor 6.2, CITED), the equality conjecture
(SIMULATED, run CAPPEDF1-20261031T120726Z), Kantorovich duality / Birkhoff (cited). Exact per-edge certificates for the
cap-active cases k = 7, 8 (prisms) and the truncated cube: `PositiveGeometryEmergentSpaceTime.CappedFormanCerts`.
-/

namespace PositiveGeometryEmergentSpaceTime.CappedForman

/-- Per-face term of a weighted Forman curvature with face weight m (audit note §3). -/
def g (k : ℕ) (m : ℚ) : ℚ := m - 2 * |1 - m| - ((k : ℚ) - 3) * m

/-- The capped per-face contribution 1 − min(3, k − 3) (natural subtraction is harmless for k ≥ 3). -/
def cap (k : ℕ) : ℚ := 1 - (min 3 (k - 3) : ℕ)

theorem cap_of_le {k : ℕ} (h3 : 3 ≤ k) (h : k ≤ 6) : cap k = 4 - k := by
  have : min 3 (k - 3) = k - 3 := min_eq_right (by omega)
  simp only [cap, this]; push_cast [Nat.cast_sub h3]; ring

theorem cap_of_ge {k : ℕ} (h : 6 ≤ k) : cap k = -2 := by
  have : min 3 (k - 3) = 3 := min_eq_left (by omega)
  simp only [cap, this]; norm_num

theorem face_term_le {k : ℕ} (h3 : 3 ≤ k) (m : ℚ) (hm : 0 ≤ m) : g k m ≤ cap k := by
  have hk : (3 : ℚ) ≤ k := by exact_mod_cast h3
  unfold g
  rcases le_total m 1 with h1 | h1
  · rw [abs_of_nonneg (by linarith)]
    rcases le_total k 6 with h6 | h6
    · rw [cap_of_le h3 h6]; have : (k : ℚ) ≤ 6 := by exact_mod_cast h6
      nlinarith
    · rw [cap_of_ge h6]; have : (6 : ℚ) ≤ k := by exact_mod_cast h6
      nlinarith
  · rw [abs_of_nonpos (by linarith)]
    rcases le_total k 6 with h6 | h6
    · rw [cap_of_le h3 h6]; nlinarith
    · rw [cap_of_ge h6]; have : (6 : ℚ) ≤ k := by exact_mod_cast h6
      nlinarith

theorem face_term_max {k : ℕ} (h3 : 3 ≤ k) : ∃ m : ℚ, 0 ≤ m ∧ g k m = cap k := by
  rcases le_total k 6 with h6 | h6
  · refine ⟨1, by norm_num, ?_⟩; rw [cap_of_le h3 h6]; simp only [g, sub_self, abs_zero]; ring
  · refine ⟨0, le_refl _, ?_⟩; rw [cap_of_ge h6]; simp only [g, sub_zero, mul_zero]; norm_num

/-- Capped bound B and the classical Forman bound κ_F/(D+1), κ_F = D + 1 − Σ (k − 3), for face sizes `ks`. -/
def capB (D : ℕ) (ks : List ℕ) : ℚ := 1 - (((ks.map fun k : ℕ => min 3 (k - 3)).sum : ℕ) : ℚ) / (D + 1)
def formanB (D : ℕ) (ks : List ℕ) : ℚ := 1 - (((ks.map fun k : ℕ => k - 3).sum : ℕ) : ℚ) / (D + 1)

theorem sum_min_le (ks : List ℕ) : (ks.map fun k => min 3 (k - 3)).sum ≤ (ks.map fun k => k - 3).sum := by
  induction ks with
  | nil => simp
  | cons k t ih => simp only [List.map_cons, List.sum_cons]; have := min_le_right 3 (k - 3); omega

theorem capped_ge_forman (D : ℕ) (ks : List ℕ) : formanB D ks ≤ capB D ks := by
  unfold capB formanB
  have h := sum_min_le ks
  have hD : (0 : ℚ) < D + 1 := by positivity
  have : (((ks.map fun k : ℕ => min 3 (k - 3)).sum : ℕ) : ℚ) ≤ (((ks.map fun k : ℕ => k - 3).sum : ℕ) : ℚ) := by
    exact_mod_cast h
  have := div_le_div_of_nonneg_right this hD.le
  linarith

theorem sum_min_eq_iff (ks : List ℕ) :
    (ks.map fun k => min 3 (k - 3)).sum = (ks.map fun k => k - 3).sum ↔ ∀ k ∈ ks, k ≤ 6 := by
  induction ks with
  | nil => simp
  | cons k t ih =>
    simp only [List.map_cons, List.sum_cons, List.mem_cons, forall_eq_or_imp]
    have h1 := min_le_right 3 (k - 3); have h2 := sum_min_le t
    constructor
    · intro h
      have hk : min 3 (k - 3) = k - 3 := by omega
      have ht : (t.map fun k => min 3 (k - 3)).sum = (t.map fun k => k - 3).sum := by omega
      exact ⟨by have := min_eq_right_iff.mp hk; omega, ih.mp ht⟩
    · rintro ⟨hk, ht⟩
      rw [ih.mpr ht, min_eq_right (by omega)]

theorem capped_eq_forman_iff (D : ℕ) (ks : List ℕ) : capB D ks = formanB D ks ↔ ∀ k ∈ ks, k ≤ 6 := by
  rw [← sum_min_eq_iff]
  unfold capB formanB
  have hD : (D : ℚ) + 1 ≠ 0 := by positivity
  constructor
  · intro h
    have : (((ks.map fun k : ℕ => min 3 (k - 3)).sum : ℕ) : ℚ) = (((ks.map fun k : ℕ => k - 3).sum : ℕ) : ℚ) := by
      have h' := congrArg (fun x : ℚ => (1 - x) * ((D : ℚ) + 1)) h
      simp only [sub_sub_cancel, div_mul_cancel₀ _ hD] at h'
      exact h'
    exact_mod_cast this
  · intro h; rw [h]

end PositiveGeometryEmergentSpaceTime.CappedForman
