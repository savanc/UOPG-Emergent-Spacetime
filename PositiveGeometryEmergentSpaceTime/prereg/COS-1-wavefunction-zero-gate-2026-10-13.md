# COS-1 prereg: can a cosmological-wavefunction hidden zero lie in the physical region? (gate) — 2026-10-13

Status: PRE-REGISTERED before computation (AutoResearch).

## Setup
Tree-level wavefunction coefficients ψ_n for colour-ordered Tr φ³ of conformally coupled scalars:
- **Flat-space-like:** old-fashioned perturbation theory (OFPT), i.e. the canonical form of the cosmological polytope (Arkani-Hamed–Benincasa–Postnikov 2017 *(memory)*).
- **dS₄:** φ³ with the 1/η twist, ψ_dS = ∫₀^∞ dω₁…dω_V ψ_flat(X_v + ω_v, Y_e) *(memory)*.

Physical region: all vertex energies X_v > 0 and edge energies Y_e > 0, with the triangle constraints from |k| (Y ≤ X-sums etc.). Prior art: 2610.01775 (NLSM/Trφ³/wavefunction splitting) [CITED in OOB scan]; MR-6/FT-2 no-gos (hadronic zeros are unphysical).

## Tests
- T1: derive ψ for the 2-site chain by OFPT symbolically. Check it equals (X₁+X₂+2Y)/((X₁+X₂)(X₁+Y)(X₂+Y)).
- T2: 4-pt ordered ψ = ψ_s + ψ_t (plus 5-pt 3-site chain sums). Is there any zero with all energies > 0? Exact argument plus a random scan (10⁶ physical points).
- T3: same for the dS₄-twisted integrals (numerical quadrature on a sample).
- T4: locate the zero set; does it require some energy < 0?
- Lean: positivity of the 2-site form and of the s+t sum for positive energies.

## Verdicts
- Gate PASS if a zero lies in the physical region for any tested class.
- FAIL (NO-GO) if ψ > 0 throughout the physical region and the zeros need a negative energy.

Credit: 0 for a gate (NO-GO is a map). Proposed only.
