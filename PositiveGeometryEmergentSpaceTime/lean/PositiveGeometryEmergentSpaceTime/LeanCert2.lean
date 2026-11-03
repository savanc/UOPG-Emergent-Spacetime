/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.LeanCert2.FrwzwK0p
import PositiveGeometryEmergentSpaceTime.LeanCert2.FrwzwK0m
import PositiveGeometryEmergentSpaceTime.LeanCert2.FrwzwK1p
import PositiveGeometryEmergentSpaceTime.LeanCert2.FrwzwK1m

/-! # LEAN-CERT-2 (Grok, 2026-10-28; one-rung own pick, author approved 2026-10-27)
Run LEANCERT2-2026-10-28-r1.  Umbrella: list-certificate soundness, ABHY reproduction and the
broken-case rejection live in `PositiveGeometryEmergentSpaceTime.LeanCert2.Core`; one FR-WZW certificate per submodule
(split to bound memory after two out-of-memory box restarts).

Declared reduced scope (deviation from prereg §4): only the k = 0, 1 FR-WZW certificates are
kernel-checked.  The k = 2 certificates (120×21, 107/153-digit entries) exceeded the 8 GB RSS cap
used on this 16 GB box (stricter than the prereg's 15 GB kill) in the `decide +kernel` step, and
the k = 3 certificates (120×56, 439/518 digits) and planted PL2 (1231 digits) were not attempted.
Those counts stay SIMULATED (LIMIT); see reviews/LEAN-CERT-2-result-2026-10-28.md. -/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.LeanCert2
open Matrix PositiveGeometryEmergentSpaceTime.LeanCert

/-- The four kernel-checked FR-WZW counts: k = 0 gives 1 (σ = +1) and 0 (σ = −1); k = 1 gives
2 (σ = +1) and 0 (σ = −1). -/
theorem frwzw_counts_k01 :
    Module.finrank ℚ (LinearMap.ker (cq (rowsM 120 1 frwzw_k0p_Mr)).mulVecLin) = 1 ∧
    Module.finrank ℚ (LinearMap.ker (cq (rowsM 120 1 frwzw_k0m_Mr)).mulVecLin) = 0 ∧
    Module.finrank ℚ (LinearMap.ker (cq (rowsM 120 6 frwzw_k1p_Mr)).mulVecLin) = 2 ∧
    Module.finrank ℚ (LinearMap.ker (cq (rowsM 120 6 frwzw_k1m_Mr)).mulVecLin) = 0 :=
  ⟨frwzw_k0p_finrank, frwzw_k0m_finrank, frwzw_k1p_finrank, frwzw_k1m_finrank⟩

end PositiveGeometryEmergentSpaceTime.LeanCert2
