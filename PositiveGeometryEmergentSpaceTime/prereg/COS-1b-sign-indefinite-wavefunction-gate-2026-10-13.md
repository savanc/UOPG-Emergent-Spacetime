# COS-1b prereg: hidden zero of a sign-indefinite (NLSM-type) wavefunction in physical k? — 2026-10-13

Status: PRE-REGISTERED before computation (AutoResearch). Reopen trigger of COS-1. **Data cells to be opened: none** (no external data; the cell-level rule is satisfied trivially).

## Setup (flat-space wavefunction, massless boundary fields, mostly-plus metric)
Boundary legs p_i = (ω_i, k_i) with ω_i = |k_i| and Σk_i = 0. Energy is not conserved: E = Σω_i > 0.
Ordered 4-pt NLSM contact wavefunction: ψ₄ = N/E. Its E→0 residue must reproduce the ordered amplitude ∝ s₁₃ (hidden zero at s₁₃ = 0, CGW) *(memory)*.
The most general cyclic numerator with that residue, at the 2-derivative order: N_c = (p₁·p₃ + p₂·p₄) + c E². Here c is a boundary-term / field-basis ambiguity: it vanishes on the energy-conserving shell.

## Tests
- T1 (c = 0): sign of N₀ on 10⁶ random physical configurations; analytic bound N₀ ≤ 0, with equality iff k₁ ∥ k₃ and k₂ ∥ k₄ (collinear boundary).
- T2: for which c do zeros enter the physical region? Find the range of −N₀/E² over the scan.
- T3: check that c drops out of the E→0 residue, i.e. c is not fixed by the amplitude.

## Verdicts
- PASS if a zero lies in the open physical region for a numerator fixed without a free c.
- PARTIAL if zeros are physical only for c in some range (basis-dependent).
- FAIL / NO-GO if the c-independent zero lies only on the collinear boundary.

Spinning (spin-1/2) exchange is not covered by this prereg; it would be COS-1c. Credit 0 for a gate. Proposed only.
