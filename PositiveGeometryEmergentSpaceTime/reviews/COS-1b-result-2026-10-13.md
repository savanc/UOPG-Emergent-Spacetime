# COS-1b result: NLSM-type wavefunction zero in physical k — PARTIAL (basis-dependent), c-free zero = NO-GO (2026-10-13)

Prereg: `prereg/COS-1b-sign-indefinite-wavefunction-gate-2026-10-13.md` (f51ece6, before computation; no data cells). Script: `sims/cos1b/cos1b_gate.py` → `_output.txt`. Lean: `lean/PositiveGeometryEmergentSpaceTime/COS1b.lean` (3 thm, 1 def), wired; build 9041 jobs; AxiomsAll **567 thm, 193 defs, nonstandard = 0**.

## Results
- **T1 (c = 0):** N₀ = p₁·p₃ + p₂·p₄ < 0 at all 10⁶ physical points (max −6.0e−3). It is 0 only at collinear configurations (k₁ ∥ k₃, k₂ ∥ k₄; explicit check gives 0). Lean: `mdot_nonpos` (Cauchy–Schwarz) and `numerator_nonpos`.
- **T2:** a zero needs c = −N₀/E², found in [4.4e−4, 0.451] over the scan. So every c ∈ (0, ≈0.45] puts zeros in the open physical region, and c ≤ 0 gives none (Lean `zero_forces_c_nonneg`).
- **T3:** c drops out of the E → 0 residue, so the amplitude does not fix it.

**Verdict: PARTIAL** (per prereg). Physical zeros exist only for c > 0, and c is a boundary-term / field-basis choice. The c-independent zero sits on the collinear boundary only. It is the same structure as MR-6 (p_a·p_b ≥ m_a m_b).

Caveats:
- The claim that c is unphysical is a CONJECTURE, based on the known boundary-term ambiguity of wavefunction coefficients *(memory)*.
- Only flat-space contact at 4 pt was tested.
- dS NLSM, exchange (6 pt) and spinning fields are not covered (COS-1c).

## Blocker tags
`NO-GO` (c-free zero is boundary-only), `FRONTIER-THEORY` (no principle fixes c). Reopen trigger: a physical principle fixing the boundary term (e.g. a positive-geometry/cosmohedron canonical form for NLSM wavefunctions, as 2610.01775 suggests) that yields c > 0.

## Proposed credit (NOT awarded): 0.
