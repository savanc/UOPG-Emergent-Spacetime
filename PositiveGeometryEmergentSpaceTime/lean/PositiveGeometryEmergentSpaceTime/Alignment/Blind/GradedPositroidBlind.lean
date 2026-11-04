/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of GRADED-POSITROID.
Written ONLY from Paper II v8 §"GRADED-POSITROID" prose ("Grading the 15 Weyl-state columns …
by their Cartan weights w_i = (H₃, H₈, T₃, Y), the vanishing of all graded first moments Σ w_iᵃ
and cubic moments Σ w_iᵃ w_iᵇ w_iᶜ is equivalent to the four anomaly-cancellation conditions")
and Paper I v9 glossary ("gravitational, SU(3)²U(1), SU(2)²U(1) and U(1)³ conditions on the
hypercharges"), BEFORE opening the original module, blueprint row or generated/lean listing.

Blind conventions (one generation, all left-handed Weyl): Q (3 colours × 2 isospin, Y_Q),
u^c and d^c (anti-triplets, Y_u, Y_d), L (doublet, Y_L), e^c (singlet, Y_e). Hypercharges are
FREE rational variables; the colour/isospin weights are fixed. Cartan weights are rescaled to
integers (2H₃ ∈ {1,−1,0}, 2√3·H₈ ∈ {1,1,−2}, 2T₃ ∈ {1,−1}); vanishing of moments is
invariant under this per-coordinate rescaling. Index order a ∈ Fin 4 = (H₃, H₈, T₃, Y).
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.GradedPositroidBlind

/-- hypercharge assignment (Y_Q, Y_u, Y_d, Y_L, Y_e) -/
structure Hyp where
  yQ : ℚ
  yu : ℚ
  yd : ℚ
  yL : ℚ
  ye : ℚ

/-- weights of the 15 states: 6 Q, 3 u^c, 3 d^c, 2 L, 1 e^c. -/
def w (y : Hyp) : Fin 15 → Fin 4 → ℚ := ![
  ![1, 1, 1, y.yQ], ![1, 1, -1, y.yQ],
  ![-1, 1, 1, y.yQ], ![-1, 1, -1, y.yQ],
  ![0, -2, 1, y.yQ], ![0, -2, -1, y.yQ],
  ![-1, -1, 0, y.yu], ![1, -1, 0, y.yu], ![0, 2, 0, y.yu],
  ![-1, -1, 0, y.yd], ![1, -1, 0, y.yd], ![0, 2, 0, y.yd],
  ![0, 0, 1, y.yL], ![0, 0, -1, y.yL],
  ![0, 0, 0, y.ye]]

def firstMomentsVanish (y : Hyp) : Prop := ∀ a, ∑ i, w y i a = 0
def cubicMomentsVanish (y : Hyp) : Prop := ∀ a b c, ∑ i, w y i a * w y i b * w y i c = 0

/-- the four ACC (one generation, left-handed fields) -/
def ACC (y : Hyp) : Prop :=
  6 * y.yQ + 3 * y.yu + 3 * y.yd + 2 * y.yL + y.ye = 0 ∧
  2 * y.yQ + y.yu + y.yd = 0 ∧
  3 * y.yQ + y.yL = 0 ∧
  6 * y.yQ ^ 3 + 3 * y.yu ^ 3 + 3 * y.yd ^ 3 + 2 * y.yL ^ 3 + y.ye ^ 3 = 0

/-- BLIND CLAIM (tautological reproduction): vanishing first + cubic moments ⇔ ACC. -/
theorem moments_iff_acc (y : Hyp) :
    (firstMomentsVanish y ∧ cubicMomentsVanish y) ↔ ACC y := by
  constructor
  · rintro ⟨h1, h3⟩
    have g := h1 3
    have s3 := h3 0 0 3
    have s2 := h3 2 2 3
    have u1 := h3 3 3 3
    simp [w, Fin.sum_univ_succ] at g s3 s2 u1
    refine ⟨by linarith, by linarith, by linarith, by linarith⟩
  · rintro ⟨g, s3, s2, u1⟩
    refine ⟨?_, ?_⟩
    · intro a; fin_cases a <;> simp [w, Fin.sum_univ_succ] <;> linarith
    · intro a b c
      fin_cases a <;> fin_cases b <;> fin_cases c <;>
        simp [w, Fin.sum_univ_succ] <;> (try ring_nf) <;> (try ring_nf at g s3 s2 u1) <;>
        linarith

/-- Control: SM hypercharges (Y_Q, Y_u, Y_d, Y_L, Y_e) = (1/6, −2/3, 1/3, −1/2, 1) satisfy ACC. -/
theorem sm_acc : ACC ⟨1/6, -2/3, 1/3, -1/2, 1⟩ := by
  unfold ACC; norm_num

/-- Broken control: Y_e = 0 instead of 1 violates ACC. -/
theorem broken_acc : ¬ ACC ⟨1/6, -2/3, 1/3, -1/2, 0⟩ := by
  unfold ACC; norm_num

end PositiveGeometryEmergentSpaceTime.Alignment.GradedPositroidBlind
