/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# Shared πK kinematic quantities (HANG-1)

Canonical names for the cited mass combinations that recur across credited hadron gates
(KL-LAT / UnequalLS, LAT-2 / LatticeGate, MR-4 / PiKZero, BR-1). These are the same Σ and
on-shell stu sum that those modules already used as `m_pi2 + m_K2` — not new physics.

Also known as: Σ = m_π² + m_K², stu sum 2Σ.
-/

namespace PositiveGeometryEmergentSpaceTime.HadronKinematics

/-- Σ_πK = m_π² + m_K², the CGW / KKY dual-zero line value for πK.

Also known as: m_pi2 + m_K2, Σ, Σ_πK. Status: combination of cited mass inputs. -/
def sigmaPiK (m_pi2 m_K2 : ℝ) : ℝ := m_pi2 + m_K2

/-- Unfolded form: `sigmaPiK m_π² m_K² = m_π² + m_K²`. -/
@[simp] theorem sigmaPiK_eq (m_pi2 m_K2 : ℝ) : sigmaPiK m_pi2 m_K2 = m_pi2 + m_K2 := rfl

/-- On-shell Mandelsam sum for elastic πK: s + t + u = 2 Σ_πK.

Also known as: 2(m_pi2 + m_K2). -/
def stuSumPiK (m_pi2 m_K2 : ℝ) : ℝ := 2 * sigmaPiK m_pi2 m_K2

/-- Unfolded form: `stuSumPiK m_π² m_K² = 2(m_π² + m_K²)`. -/
@[simp] theorem stuSumPiK_eq (m_pi2 m_K2 : ℝ) :
    stuSumPiK m_pi2 m_K2 = 2 * (m_pi2 + m_K2) := by simp [stuSumPiK, sigmaPiK]

/-- πK c.m. momentum squared (LAT-2). Shared so LatticeGate and any consumer share one def.

Also known as: q²(s). -/
noncomputable def q2PiK (m_pi m_K s : ℝ) : ℝ :=
  (s - (m_K + m_pi) ^ 2) * (s - (m_K - m_pi) ^ 2) / (4 * s)

/-- On the line `s = Σ`, the πK c.m. momentum squared is `q² = −m_π² m_K² / Σ`. -/
theorem q2PiK_on_line (m_pi m_K : ℝ) (h : sigmaPiK (m_pi ^ 2) (m_K ^ 2) ≠ 0) :
    q2PiK m_pi m_K (sigmaPiK (m_pi ^ 2) (m_K ^ 2)) =
      -(m_pi ^ 2 * m_K ^ 2) / sigmaPiK (m_pi ^ 2) (m_K ^ 2) := by
  unfold q2PiK sigmaPiK at *; field_simp; ring

end PositiveGeometryEmergentSpaceTime.HadronKinematics
