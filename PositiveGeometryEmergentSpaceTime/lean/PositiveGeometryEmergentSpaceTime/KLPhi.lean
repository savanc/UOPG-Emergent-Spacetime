/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
KL-LAT2: phi (ss̄) from the KL-1 rule a_V(m_P²) = 1/2 with universal slope a = 1/(2(mρ² − mπ²)),
and m_ηs² = 2 m_K² − mπ² (leading-order GMOR; CITED assumption).

Also known as (mass binders): `m_pi`/`m_pi2` (formerly mp/mp2, mπ); `m_K`/`m_K2` (formerly mK/mK2); `m_rho2` (formerly mr2, mρ²); `m_eta2` (formerly me2); `m_Kstar2`/`m_phi2` (formerly mks2/mphi2).
-/

namespace PositiveGeometryEmergentSpaceTime.KLPhi

/-- φ pole: a_φ(mφ²) = 1 with a_φ(m_ηs²) = 1/2 gives mφ² = 2mK² + mρ² − 2mπ². -/
theorem phi_relation (m_pi2 m_rho2 m_K2 m2 : ℝ) (hne : m_rho2 - m_pi2 ≠ 0)
    (h : 1/2 + (1 / (2*(m_rho2 - m_pi2))) * (m2 - (2*m_K2 - m_pi2)) = 1) :
    m2 = 2*m_K2 + m_rho2 - 2*m_pi2 := by
  field_simp at h; linarith

/-- Equal spacing in squared masses: with m_K*² = m_K² + mρ² − mπ² (UnequalLS.kstar_relation),
mφ² − m_K*² = m_K*² − mρ². -/
theorem equal_spacing (m_pi2 m_rho2 m_K2 m_Kstar2 m_phi2 : ℝ)
    (hks : m_Kstar2 = m_K2 + m_rho2 - m_pi2) (hphi : m_phi2 = 2*m_K2 + m_rho2 - 2*m_pi2) :
    m_phi2 - m_Kstar2 = m_Kstar2 - m_rho2 := by
  subst hks; subst hphi; ring

/-- The φ prediction depends only on (mπ, m_K, mρ): it is 2 m_K*² − mρ². -/
theorem phi_from_kstar (m_pi2 m_rho2 m_K2 : ℝ) :
    2*m_K2 + m_rho2 - 2*m_pi2 = 2*(m_K2 + m_rho2 - m_pi2) - m_rho2 := by ring

end PositiveGeometryEmergentSpaceTime.KLPhi
