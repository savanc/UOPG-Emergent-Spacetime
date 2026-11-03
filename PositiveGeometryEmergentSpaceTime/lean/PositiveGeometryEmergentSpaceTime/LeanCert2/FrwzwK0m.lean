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

-- frwzw_k0m: m = 120, n = 1, k = 0
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): rows of `M`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0m_Mr : List (List ℤ) := [[0],
  [1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [-1],
  [0],
  [0],
  [1],
  [0],
  [0],
  [1],
  [0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): columns of `M`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0m_Mc : List (List ℤ) := [[0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): rows of `K`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0m_Kr : List (List ℤ) := [[]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): columns of `K` (kernel basis). Emitted verbatim by the generator;
  correctness is only what `certL` checks. -/
def frwzw_k0m_Kc : List (List ℤ) := []
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): rows of `P`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0m_Pr : List (List ℤ) := [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): rows of `Q`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0m_Qr : List (List ℤ) := []
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): columns of `Q`. Emitted verbatim by the generator; correctness is only what
  `certL` checks. -/
def frwzw_k0m_Qc : List (List ℤ) := [[]]
set_option maxHeartbeats 0 in
/-- List certificate data for the FRWZW k = 0, σ = −1 system (120 × 1 constraint matrix, certified
  kernel dimension 0): nonzero integer scale `d`. Emitted verbatim by the generator; correctness
  is only what `certL` checks. -/
def frwzw_k0m_d : ℤ := 1


/-- Kernel check (`decide`) that the FRWZW k = 0, σ = −1 list certificate passes `certL 120 1 0`
  (kernel dimension 0 over ℚ). -/
theorem frwzw_k0m_cert : certL 120 1 0 frwzw_k0m_Mr frwzw_k0m_Mc frwzw_k0m_Kr frwzw_k0m_Kc frwzw_k0m_Pr frwzw_k0m_Qr frwzw_k0m_Qc frwzw_k0m_d = true := by
  decide +kernel

/-- FR-WZW count, k = 0, σ = −1: dim ker = 0 (PROVED; was SIMULATED). -/
theorem frwzw_k0m_finrank : Module.finrank ℚ (LinearMap.ker (cq (rowsM 120 1 frwzw_k0m_Mr)).mulVecLin) = 0 :=
  finrank_of_certL frwzw_k0m_cert

end PositiveGeometryEmergentSpaceTime.LeanCert2
