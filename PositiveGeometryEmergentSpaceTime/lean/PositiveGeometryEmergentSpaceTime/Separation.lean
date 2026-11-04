/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT1
import PositiveGeometryEmergentSpaceTime.STRUCT1b
import PositiveGeometryEmergentSpaceTime.STRUCT2
import PositiveGeometryEmergentSpaceTime.STRUCT3
import PositiveGeometryEmergentSpaceTime.X6

/-!
# R4 → R5 — `geometry_struct_separation`

Also known as: R5 fallback, unify-inputs no-go, `ew_from_pion_geometry` (R4) negative result.

R4 has no concrete candidate. The pion geometry (NLSM ⊂ Tr φ³, associahedron, hidden zeros) produces
flavour-stripped partial amplitudes; quark charges enter only through the gauged embedding Q = T₃ + Y, which
the geometry does not output. The one pion object that does see the charges (WZW / Goldstone–Wilczek,
π⁰→γγ) has no positive-geometry construction, and with anomaly-consistent charges it is `N_c`-blind
(CITED: Bär–Wiese hep-ph/0105258). This module proves that blindness and bundles the STRUCT / X6 no-gos.
-/

namespace PositiveGeometryEmergentSpaceTime.Separation

/-- Up-quark electric charge `Q_u = T₃ + Y = 1/2 + yQ`. Also known as: Q_u, e_u, Q_up. -/
def chargeUp (yQ : ℚ) : ℚ := yQ + 1 / 2

/-- Down-quark electric charge `Q_d = −1/2 + yQ`. Also known as: Q_d, e_d, Q_down. -/
def chargeDown (yQ : ℚ) : ℚ := yQ - 1 / 2

/-- π⁰→γγ anomaly coefficient `N_c (Q_u² − Q_d²)` (= 2 Tr(T³Q²)). Also known as: A_π⁰γγ, triangle
  coefficient. -/
def pi0Anomaly (N_c yQ : ℚ) : ℚ := N_c * (chargeUp yQ ^ 2 - chargeDown yQ ^ 2)

/-- R4 exclusion (Bär–Wiese): ACC with lepton doublet `yL = −1/2` ⇒ the π⁰→γγ coefficient is 1 for every
  `N_c`. -/
theorem pi0Anomaly_nc_blind {N_c yQ yu yd ye : ℚ} (h : STRUCT2.ACCN N_c yQ yu yd (-1 / 2) ye) :
    pi0Anomaly N_c yQ = 1 := by
  obtain ⟨_, h2, _, _⟩ := h
  unfold pi0Anomaly chargeUp chargeDown; linear_combination 2 * h2

/-- Planted: at `N_c = 3` the charges are the SM values 2/3, −1/3. -/
theorem sm_charges_three {yQ yu yd ye : ℚ} (h : STRUCT2.ACCN 3 yQ yu yd (-1 / 2) ye) :
    chargeUp yQ = 2 / 3 ∧ chargeDown yQ = -1 / 3 := by
  obtain ⟨_, h2, _, _⟩ := h
  unfold chargeUp chargeDown; constructor <;> linarith

/-- R5 bundle (`geometry_struct_separation`): the Lean no-gos that keep geometry and the EW/STRUCT
  inputs apart. -/
theorem geometry_struct_separation :
    -- hypercharges: not unique with νᶜ (STRUCT-1); Dirac family (STRUCT-1b)
    (¬ ∃ c : ℚ, ((1:ℚ)/3 = c * (1/6) ∧ (-1:ℚ)/3 = c * (-2/3) ∧ (-1:ℚ)/3 = c * (1/3)) ∨
              ((1:ℚ)/3 = c * (1/6) ∧ (-1:ℚ)/3 = c * (1/3) ∧ (-1:ℚ)/3 = c * (-2/3))) ∧
    ((STRUCT1.ACCnu 1 (-4) 2 (-3) 6 0 ∧ STRUCT1b.Yuk 1 (-4) 2 (-3) 6 0 3) ∧
      (STRUCT1.ACCnu 1 (-1) (-1) (-3) 3 3 ∧ STRUCT1b.Yuk 1 (-1) (-1) (-3) 3 3 0) ∧ ((-4 : ℚ) ≠ -1)) ∧
    -- N_c: 3 and 5 both consistent (STRUCT-2)
    ((STRUCT2.ACCN 3 1 2 (-4) (-3) 6 ∧ STRUCT2.Witten 3) ∧ (STRUCT2.ACCN 5 1 4 (-6) (-5) 10 ∧ STRUCT2.Witten 5)) ∧
    -- chirality: Gr₊(2,4) is orientation-blind; vector-like ⇒ ACC vacuous (X6)
    (∀ p : X6.Plucker24, p.pos → p.rel →
      (X6.parityDual p).pos ∧ (X6.parityDual p).rel ∧ (X6.reflect p).pos ∧ (X6.reflect p).rel) ∧
    -- N_gen: 3 and 4 both pass AF + KM (STRUCT-3)
    ((0 < STRUCT3.b0SU3 3 ∧ 0 < STRUCT3.b0SU2 3 ∧ 0 < STRUCT3.kmPhases 3) ∧
      (0 < STRUCT3.b0SU3 4 ∧ 0 < STRUCT3.b0SU2 4 ∧ 0 < STRUCT3.kmPhases 4)) ∧
    -- pion ↔ charge link is N_c-blind (R4)
    (∀ N_c yQ yu yd ye : ℚ, STRUCT2.ACCN N_c yQ yu yd (-1 / 2) ye → pi0Anomaly N_c yQ = 1) :=
  ⟨STRUCT1.not_unique_with_nu, STRUCT1b.dirac_not_unique, STRUCT2.three_not_selected,
    fun _ h hr => X6.positivity_orientation_blind h hr, STRUCT3.three_not_selected_ngen,
    fun _ _ _ _ _ h => pi0Anomaly_nc_blind h⟩

end PositiveGeometryEmergentSpaceTime.Separation
