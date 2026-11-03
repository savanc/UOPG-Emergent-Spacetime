# COS-1c result: spin-1 exchange wavefunction has zeros in the physical region — gate PASS (weak) (2026-10-13)

Prereg: `prereg/COS-1c-spin1-exchange-wavefunction-gate-2026-10-13.md` (02bff26; data cells: none). Script: `sims/cos1c/cos1c_gate.py` → `_output.txt`.

## Results
- **T0:** the Coulomb-gauge coefficient κ is fixed to −1 by requiring the E→0 residue to equal the Lorentz amplitude (sympy). This matches the hand derivation. The identity J⁰X = J·Y holds for null legs off the energy shell (dev 1e−14). So there is **no free boundary constant**, unlike COS-1b's c.
- **T1:** over 10⁶ physical configurations, ψ_γ > 0 in 49.9 % and < 0 in 50.1 %.
- **T2:** 200 zeros located by bisection (|ψE| ≤ 7e−16). At all of them, E, X_L+Y, X_R+Y and Y stay ≥ 0.037 E, i.e. every propagator is finite and the point is in the open physical region. The zero set is a real hypersurface.
- **T3:** the ψ-zero locus is *not* the flat-amplitude zero (J_L·J_R)_Mink = 0. The amplitude numerator on ψ-zeros has median 0.015 E², and only 2 % of zeros have it below 1e−3. Signs agree in 94 % of configurations, so the two zero sets are close but distinct.

**Verdict: PASS (per prereg), with a caveat that weakens it.** The pass criterion was only "a codimension-1 zero set in the physical region". Any sign-indefinite smooth function has one, so this does not show a *structured* (CGW-type, linear-condition) hidden zero. Part of the sign structure is also forced by charge-conjugation antisymmetry (J_L → −J_L under 1↔2).

What is genuinely established:
- A gauge-fixed, boundary-constant-free cosmological wavefunction can vanish at physical energies with all propagators finite. COS-1, COS-1b and COS-1r showed this is impossible for positive (Tr φ³) or basis-free NLSM contact cases.
- The locus differs from the amplitude zero, so it is wavefunction-specific.

## Assumptions / not done
- Weyl invariance of conformally coupled scalar QED in 4D (flat → dS₄) is *memory*, not checked here.
- No Lean module: the numerics plus the sympy residue check are the evidence (SIMULATED).
- There is no data test. Charged conformally coupled spectators are not the curvature perturbation, so there is no near-term observable yet.

## Blocker tags / next
`FRONTIER-THEORY` for observability. Proposed COS-1d:
1. Characterise the zero hypersurface analytically, i.e. whether it is a linear condition in some variables (structured hidden zero) or generic.
2. Check whether an inflaton-coupled analogue (graviton or spin-1 exchange in the scalar trispectrum) inherits it, which would give a template for SO/Euclid/SPHEREx.

## Proposed credit (NOT awarded): 0 (gate, no observable).
