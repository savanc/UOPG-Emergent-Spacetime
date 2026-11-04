/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.RpTn1
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.RpTn1Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: RP-TN-1

Blind `C` is definitionally the original `corr2`. Both minor identities and the strict Toeplitz
negativity are interderivable. VERDICT: EQUIV.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.RPTN1

open PositiveGeometryEmergentSpaceTime.Alignment.RpTn1Blind

theorem C_eq : C = PositiveGeometryEmergentSpaceTime.RpTn1.corr2 := rfl

theorem hankel_blind_to_orig (w₁ w₂ x₁ x₂ : ℝ) (a c k l : ℕ) :
    PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ (a + c) * PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ (a + k + (c + l))
      - PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ (a + (c + l)) * PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ (a + k + c)
      = w₁ * w₂ * (x₁ * x₂) ^ (a + c) * ((x₂ ^ k - x₁ ^ k) * (x₂ ^ l - x₁ ^ l)) := by
  have h := hankel_identity w₁ w₂ x₁ x₂ a c k l
  rw [← C_eq, show a + k + (c + l) = a + k + c + l by omega, show a + (c + l) = a + c + l by omega, h]
  ring

theorem hankel_orig_to_blind (w₁ w₂ x₁ x₂ : ℝ) (a c k l : ℕ) :
    C w₁ w₂ x₁ x₂ (a + c) * C w₁ w₂ x₁ x₂ (a + k + c + l)
      - C w₁ w₂ x₁ x₂ (a + c + l) * C w₁ w₂ x₁ x₂ (a + k + c)
    = w₁ * w₂ * (x₁ * x₂) ^ (a + c) * (x₁ ^ k - x₂ ^ k) * (x₁ ^ l - x₂ ^ l) := by
  have h := PositiveGeometryEmergentSpaceTime.RpTn1.hankel2_minor_identity w₁ w₂ x₁ x₂ a c k l
  rw [show a + k + (c + l) = a + k + c + l by omega, show a + (c + l) = a + c + l by omega] at h
  rw [C_eq, h]; ring

theorem toeplitz_neg_blind_to_orig (w₁ w₂ x₁ x₂ : ℝ) (hw₁ : 0 < w₁) (hw₂ : 0 < w₂) (h₁ : 0 ≤ x₁)
    (h₂ : 0 ≤ x₂) (hne : x₁ ≠ x₂) (a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0) :
    PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ a * PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ b
      - PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ 0 * PositiveGeometryEmergentSpaceTime.RpTn1.corr2 w₁ w₂ x₁ x₂ (a + b) < 0 :=
  toeplitz_minor_neg w₁ w₂ x₁ x₂ hw₁ hw₂ h₁ h₂ hne a b (Nat.one_le_iff_ne_zero.mpr ha)
    (Nat.one_le_iff_ne_zero.mpr hb)

theorem toeplitz_neg_orig_to_blind (w₁ w₂ x₁ x₂ : ℝ) (hw₁ : 0 < w₁) (hw₂ : 0 < w₂) (h₁ : 0 ≤ x₁)
    (h₂ : 0 ≤ x₂) (hne : x₁ ≠ x₂) (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    C w₁ w₂ x₁ x₂ a * C w₁ w₂ x₁ x₂ b - C w₁ w₂ x₁ x₂ 0 * C w₁ w₂ x₁ x₂ (a + b) < 0 :=
  PositiveGeometryEmergentSpaceTime.RpTn1.toeplitz2_minor_neg w₁ w₂ x₁ x₂ hw₁ hw₂ h₁ h₂ hne a b (by omega) (by omega)

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.RPTN1
