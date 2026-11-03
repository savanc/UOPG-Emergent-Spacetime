/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.STRUCT2
import PositiveGeometryEmergentSpaceTime.Separation

/-!
# R4 independent attempt (2026-10-16) — charge-visibility lemmas

Also known as: R4-indep, unify-inputs second attempt.

The pion (adjoint, colour-singlet) sector sees quark charges only through differences `Q_i − Q_j`;
the hypercharge `y_Q` (trace / baryon-number part) drops out. N_c is visible only in N_f ≥ 3
odd-intrinsic-parity (WZW) vertices (CITED: Bär–Wiese hep-ph/0105258), which the current geometry chain
does not produce.
-/

namespace PositiveGeometryEmergentSpaceTime.R4Indep
open PositiveGeometryEmergentSpaceTime.Separation

/-- Electric charge of the flavour-ordered meson `q_i q̄_j`: `Q_i − Q_j` (adjoint action of `Q`).
Also known as: Q_ij, adjoint charge. -/
def mesonCharge (qi qj : ℚ) : ℚ := qi - qj

/-- (a) The adjoint charge is blind to a common shift `Q ↦ Q + c·1` (the trace / y_Q part). -/
theorem mesonCharge_shift (qi qj c : ℚ) : mesonCharge (qi + c) (qj + c) = mesonCharge qi qj := by
  unfold mesonCharge; ring

/-- (a) π⁺ = u d̄ has charge 1 for every `y_Q`: the pion sector cannot see the hypercharge. -/
theorem piPlus_charge_yQ_blind (yQ : ℚ) : mesonCharge (chargeUp yQ) (chargeDown yQ) = 1 := by
  unfold mesonCharge chargeUp chargeDown; ring

/-- (c) DGMLY charge factor `(Q_u − Q_d)²` of the π⁺–π⁰ EM splitting. Also known as: dgmlyCharge. -/
def dgmlyCharge (yQ : ℚ) : ℚ := (chargeUp yQ - chargeDown yQ) ^ 2

/-- (c) The DGMLY charge factor is 1 for every `y_Q` (and has no `N_c`). -/
theorem dgmlyCharge_blind (yQ : ℚ) : dgmlyCharge yQ = 1 := by
  unfold dgmlyCharge chargeUp chargeDown; norm_num

/-- (e) η⁸→π⁺π⁻γ box coefficient `N_c (Q_u − Q_d)` (Bär–Wiese eq. 5.9, up to 1/(4√3)). -/
def etaPiPiGamma (N_c yQ : ℚ) : ℚ := N_c * (chargeUp yQ - chargeDown yQ)

/-- (e) It sees `N_c` and nothing else: equals `N_c` for every `y_Q`. -/
theorem etaPiPiGamma_eq (N_c yQ : ℚ) : etaPiPiGamma N_c yQ = N_c := by
  unfold etaPiPiGamma chargeUp chargeDown; ring

/-- (e) π⁰K⁺K⁻γ coefficient `N_c Q_u` (Bär–Wiese eq. 5.12, up to 1/4). -/
def pi0KKGamma (N_c yQ : ℚ) : ℚ := N_c * chargeUp yQ

/-- (e) Under ACC (lepton doublet −1/2), `N_c Q_u = (N_c + 1)/2`: a strange-sector WZW vertex sees
  N_c. -/
theorem pi0KKGamma_acc {N_c yQ yu yd ye : ℚ} (h : STRUCT2.ACCN N_c yQ yu yd (-1 / 2) ye) :
    pi0KKGamma N_c yQ = (N_c + 1) / 2 := by
  obtain ⟨_, h2, _, _⟩ := h
  unfold pi0KKGamma chargeUp; linear_combination h2

/-- (d) Under ACC, `2 N_c y_Q = 1`: the global quotient is `ℤ_{2N_c}` (ℤ₆ ⇔ N_c = 3), fixed by N_c,
  not by pions. -/
theorem quotient_order_acc {N_c yQ yu yd ye : ℚ} (h : STRUCT2.ACCN N_c yQ yu yd (-1 / 2) ye) :
    2 * N_c * yQ = 1 := by
  obtain ⟨_, h2, _, _⟩ := h
  linear_combination 2 * h2

/-- (d) Any colour-singlet q q̄ meson has integer-difference charge independent of `y_Q`
(same as (a)); hence the ℤ_{2N_c} data is invisible to the pion sector. -/
theorem meson_quotient_blind (yQ yQ' : ℚ) :
    mesonCharge (chargeUp yQ) (chargeDown yQ) = mesonCharge (chargeUp yQ') (chargeDown yQ') := by
  rw [piPlus_charge_yQ_blind, piPlus_charge_yQ_blind]

end PositiveGeometryEmergentSpaceTime.R4Indep
