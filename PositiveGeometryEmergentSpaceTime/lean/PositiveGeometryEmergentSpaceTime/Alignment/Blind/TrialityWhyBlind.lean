/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of TRIALITY-WHY (window theorem).
Written ONLY from Paper II v8 §"TRIALITY-WHY" prose ("the exactness window (the generation
numbers N with k ∣ N c …) … both are multiples of k/gcd(k,c) PROVED") and Paper I v9
§TRIALITY-WHY, BEFORE opening the original Lean module, the blueprint row or the
generated/lean listing. Reading: for k > 0 the window {N | k ∣ N·c} is exactly the set of
multiples of k / gcd(k,c); "not forced" = the window is closed under multiples, so it is never
the singleton {3}.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.TrialityWhyBlind

/-- The exactness window of a ℤ_k symmetry whose per-generation instanton charge is `c`. -/
def window (k c : ℕ) : Set ℕ := {N | k ∣ N * c}

/-- BLIND CLAIM (window theorem): for k > 0, N is in the window iff k / gcd(k,c) ∣ N. -/
def ClaimWindow : Prop :=
  ∀ k c N : ℕ, 0 < k → (N ∈ window k c ↔ k / Nat.gcd k c ∣ N)

theorem claimWindow : ClaimWindow := by
  intro k c N hk
  show k ∣ N * c ↔ k / Nat.gcd k c ∣ N
  have hg : 0 < Nat.gcd k c := Nat.gcd_pos_of_pos_left c hk
  obtain ⟨k', hk'⟩ := Nat.gcd_dvd_left k c
  obtain ⟨c', hc'⟩ := Nat.gcd_dvd_right k c
  set g := Nat.gcd k c with hgdef
  have hcop : Nat.Coprime k' c' := by
    have := Nat.coprime_div_gcd_div_gcd (m := k) (n := c) hg
    rw [← hgdef] at this
    have e1 : k / g = k' := by rw [hk']; exact Nat.mul_div_cancel_left k' hg
    have e2 : c / g = c' := by rw [hc']; exact Nat.mul_div_cancel_left c' hg
    rwa [e1, e2] at this
  have hkdiv : k / g = k' := by rw [hk']; exact Nat.mul_div_cancel_left k' hg
  rw [hkdiv]
  constructor
  · intro h
    have h2 : g * k' ∣ g * (N * c') := by
      have : N * c = g * (N * c') := by rw [hc']; ring
      rw [← this, ← hk']; exact h
    have h3 : k' ∣ N * c' := Nat.dvd_of_mul_dvd_mul_left hg h2
    exact hcop.dvd_of_dvd_mul_right h3
  · intro h
    obtain ⟨m, hm⟩ := h
    refine ⟨m * c', ?_⟩
    rw [hm, hk', hc']; ring

/-- BLIND CLAIM (not forced): the window is closed under multiplication, so if 3 is allowed then
6 is allowed; in particular the window is never exactly {3}. -/
def ClaimNotForced : Prop :=
  ∀ k c : ℕ, window k c ≠ {3}

theorem claimNotForced : ClaimNotForced := by
  intro k c h
  have h3 : (3 : ℕ) ∈ window k c := by rw [h]; rfl
  have h6 : (6 : ℕ) ∈ window k c := by
    show k ∣ 6 * c
    have : k ∣ 3 * c := h3
    exact Dvd.dvd.trans this ⟨2, by ring⟩
  rw [h] at h6
  simp at h6

/-- Instance: baryon triality reading k = 3, c = 1 gives "N_gen ≡ 0 mod 3". -/
theorem triality_instance (N : ℕ) : N ∈ window 3 1 ↔ 3 ∣ N := by
  rw [claimWindow 3 1 N (by norm_num)]; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.TrialityWhyBlind
