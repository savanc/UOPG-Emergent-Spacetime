/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
MR-1f-eta gate. K eta -> K eta: K* exchange in s and u (su dual term).
With a_K(x) = 1/2 + a (x - m_K²), the su dual zero a_K(s) + a_K(u) = 1 forces t = 2 m_eta².
The LO ChPT K eta amplitude (9t - 6 m_eta² - 2 m_pi²) vanishes at t0 = (6 m_eta² + 2 m_pi²)/9.
The two coincide only if 12 m_eta² = 2 m_pi², impossible for m_eta > m_pi > 0.
-/

namespace PositiveGeometryEmergentSpaceTime.KEtaGate

/-- If `a ≠ 0`, `s + t + u = 2m_K² + 2m_η²` and `½ + a(s − m_K²) + ½ + a(u − m_K²) = 1`, then `t =
  2m_η²`. -/
theorem su_zero_line (a m_K2 m_eta2 s t u : ℝ) (ha : a ≠ 0)
    (hstu : s + t + u = 2 * m_K2 + 2 * m_eta2)
    (hz : (1/2 + a * (s - m_K2)) + (1/2 + a * (u - m_K2)) = 1) : t = 2 * m_eta2 := by
  have h1 : a * (s + u - 2 * m_K2) = 0 := by linarith
  have h2 : s + u - 2 * m_K2 = 0 := by
    rcases mul_eq_zero.mp h1 with h | h
    · exact absurd h ha
    · exact h
  linarith

/-- The dual su zero and the chiral LO zero never coincide when m_eta² > m_pi² > 0. -/
theorem dual_ne_chiral (m_eta2 m_pi2 : ℝ) (hp : 0 < m_pi2) (he : m_pi2 < m_eta2) :
    2 * m_eta2 ≠ (6 * m_eta2 + 2 * m_pi2) / 9 := by
  intro h; nlinarith

/-- Hence the LO chiral K eta amplitude is nonzero on the dual zero line: it equals 12 m_eta² - 2
  m_pi² > 0. -/
theorem chiral_on_dual (m_eta2 m_pi2 : ℝ) (hp : 0 < m_pi2) (he : m_pi2 < m_eta2) :
    9 * (2 * m_eta2) - 6 * m_eta2 - 2 * m_pi2 > 0 := by nlinarith

end PositiveGeometryEmergentSpaceTime.KEtaGate
