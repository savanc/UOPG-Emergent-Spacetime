/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.LeanCert2.Core

/-! LEAN-CERT-2 (run LEANCERT2-2026-10-28-r1): one FR-WZW certificate per module (split to bound memory). -/

set_option autoImplicit false

namespace PositiveGeometryEmergentSpaceTime.LeanCert2
open Matrix PositiveGeometryEmergentSpaceTime.LeanCert

-- frwzw_k0p: m = 120, n = 1, k = 1
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): rows of `M`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0p_Mr : List (List ℤ) := [[0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0],
  [0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): columns of `M`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0p_Mc : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): rows of `K`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0p_Kr : List (List ℤ) := [[1]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): columns of `K` (kernel basis). Emitted verbatim by the generator;
  correctness is only what `certL` checks. -/
def frwzw_k0p_Kc : List (List ℤ) := [[1]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): rows of `P`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0p_Pr : List (List ℤ) := [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): rows of `Q`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0p_Qr : List (List ℤ) := [[1]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): columns of `Q`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0p_Qc : List (List ℤ) := [[1]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = +1 system (120 × 1 constraint matrix, certified
  kernel dimension 1): nonzero integer scale `d`. Emitted verbatim by the generator; correctness
  is only what `certL` checks. -/
def frwzw_k0p_d : ℤ := 1


/-- Kernel check (`decide`) that the FRWZW k = 0, σ = +1 list certificate passes `certL 120 1 1`
  (kernel dimension 1 over ℚ). -/
theorem frwzw_k0p_cert : certL 120 1 1 frwzw_k0p_Mr frwzw_k0p_Mc frwzw_k0p_Kr frwzw_k0p_Kc frwzw_k0p_Pr frwzw_k0p_Qr frwzw_k0p_Qc frwzw_k0p_d = true := by
  decide +kernel

/-- FR-WZW count, k = 0, σ = +1: dim ker = 1 (PROVED; was SIMULATED). -/
theorem frwzw_k0p_finrank : Module.finrank ℚ (LinearMap.ker (cq (rowsM 120 1 frwzw_k0p_Mr)).mulVecLin) = 1 :=
  finrank_of_certL frwzw_k0p_cert

end PositiveGeometryEmergentSpaceTime.LeanCert2
