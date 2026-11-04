/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-3 (2026-11-03) — BLIND second formalisation of MR-2 (massive hidden zero at P).
Written ONLY from the prose of reviews/MR-2-result-2026-10-12.md (Claims) and
prereg/MR-2-massive-hidden-zero-2026-10-12.md (§0, §1), BEFORE opening lean/PositiveGeometryEmergentSpaceTime/MassiveZero.lean
or its blueprint row. Prose claims: ordered f(s,t) vanishes on s + t = 2M²; "any symmetric ordered
amplitude with the massive zero on s+t=2M² gives SU(2) A(M²,M²,2M²)=0"; "O(p⁴): zero ⇔ a2=2a1 ∧
4a1+2a3+a4=0"; A(P) "contains M3's combination too"; "LO (Weinberg) vanishes at P".
Readings chosen here (blind): SU(2) dressing A(s,t,u) = f(s,t) + f(s,u) − f(t,u) (single trace);
O(p⁴) ordered polynomial f = a1(s²+t²) + a2 st + a3 M²(s+t) + a4 M⁴; Weinberg A = (s − M²)/F².
Not blinded: "G¹/F¹ polynomial values at P" (basis not in the prose).
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace PositiveGeometryEmergentSpaceTime.Alignment.Mr2Blind

variable {K : Type*} [Field K] [CharZero K]

/-- SU(2) single-trace dressing of an ordered amplitude. -/
def dress (f : K → K → K) (s t u : K) : K := f s t + f s u - f t u

/-- BLIND CLAIM: f symmetric with the zero on s + t = 2M² ⇒ A(M², M², 2M²) = 0. -/
theorem dress_zero_P (f : K → K → K) (M2 : K) (_hsym : ∀ x y, f x y = f y x)
    (hzero : ∀ s t, s + t = 2 * M2 → f s t = 0) : dress f M2 M2 (2 * M2) = 0 := by
  unfold dress; rw [hzero M2 M2 (by ring)]; ring

/-- Blind extra: symmetry is not needed for this (s = t at P). -/
theorem dress_zero_P_nosym (f : K → K → K) (M2 : K)
    (hzero : ∀ s t, s + t = 2 * M2 → f s t = 0) : dress f M2 M2 (2 * M2) = 0 := by
  unfold dress; rw [hzero M2 M2 (by ring)]; ring

/-- O(p⁴) ordered polynomial. -/
def fpoly (a1 a2 a3 a4 M2 s t : K) : K := a1 * (s ^ 2 + t ^ 2) + a2 * s * t + a3 * M2 * (s + t) + a4 * M2 ^ 2

/-- On the line, f = (a2 − 2a1) st + M⁴(4a1 + 2a3 + a4). -/
theorem fpoly_on_line (a1 a2 a3 a4 M2 s : K) :
    fpoly a1 a2 a3 a4 M2 s (2 * M2 - s) = (a2 - 2 * a1) * (s * (2 * M2 - s)) + M2 ^ 2 * (4 * a1 + 2 * a3 + a4) := by
  unfold fpoly; ring

/-- BLIND CLAIM: (M ≠ 0) the O(p⁴) polynomial vanishes on all of s + t = 2M² ⇔
a2 = 2a1 ∧ 4a1 + 2a3 + a4 = 0. -/
theorem poly_zero_iff (a1 a2 a3 a4 M2 : K) (hM : M2 ≠ 0) :
    (∀ s t, s + t = 2 * M2 → fpoly a1 a2 a3 a4 M2 s t = 0) ↔ (a2 = 2 * a1 ∧ 4 * a1 + 2 * a3 + a4 = 0) := by
  constructor
  · intro h
    have h0 := h 0 (2 * M2) (by ring)
    have h1 := h M2 M2 (by ring)
    unfold fpoly at h0 h1
    have hM2 : M2 ^ 2 ≠ 0 := pow_ne_zero 2 hM
    have hc : M2 ^ 2 * (4 * a1 + 2 * a3 + a4) = 0 := by linear_combination h0
    have hd : M2 ^ 2 * (a2 - 2 * a1) = 0 := by linear_combination h1 - h0
    have hc' := (mul_eq_zero.mp hc).resolve_left hM2
    have hd' := (mul_eq_zero.mp hd).resolve_left hM2
    exact ⟨by linear_combination hd', hc'⟩
  · rintro ⟨h2, hc⟩ s t hst
    have ht : t = 2 * M2 - s := by linear_combination hst
    rw [ht, fpoly_on_line, h2, hc]; ring

/-- BLIND CLAIM: A(P) for the polynomial = M⁴[(a2 − 2a1) + (4a1 + 2a3 + a4)]: it contains both the
massless (M3) combination a2 − 2a1 and the mass-term combination. -/
theorem dress_poly_P (a1 a2 a3 a4 M2 : K) :
    dress (fpoly a1 a2 a3 a4 M2) M2 M2 (2 * M2) = M2 ^ 2 * ((a2 - 2 * a1) + (4 * a1 + 2 * a3 + a4)) := by
  unfold dress fpoly; ring

/-- Weinberg LO. -/
def weinberg (M2 F s : K) : K := (s - M2) / F ^ 2

/-- BLIND CLAIM: Weinberg vanishes at P. -/
theorem lo_zero_P (M2 F : K) : weinberg M2 F M2 = 0 := by unfold weinberg; simp

/-- Consistency: the LO ordered amplitude f = (s + t − 2M²)/(2F²) has the zero and dresses to Weinberg. -/
theorem lo_dress (M2 F s t u : K) (hF : F ≠ 0) :
    dress (fun x y => (x + y - 2 * M2) / (2 * F ^ 2)) s t u = weinberg M2 F s := by
  unfold dress weinberg; field_simp; ring

end PositiveGeometryEmergentSpaceTime.Alignment.Mr2Blind
