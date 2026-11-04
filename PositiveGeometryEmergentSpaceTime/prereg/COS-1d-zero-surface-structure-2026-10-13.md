# COS-1d prereg: structure of the COS-1c zero surface — 2026-10-13

Status: PRE-REGISTERED before any computation (AutoResearch). **Data cells: none.**
**Disclosure:** while planning, I did a short hand sketch that suggested the numerator reduces to Y[Y·(J_L·J_R)_Mink − E·J⁰_L J⁰_R]. That is not yet verified. The definitions below are fixed regardless of that sketch, and the verdict uses them as written.

## Definitions (fixed now)
Let ψ_γ = P/D (COS-1c), with D the product of manifestly positive physical factors (E, Y, X_L+Y, X_R+Y). Write M := (J_L·J_R)_Mink, the flat-amplitude numerator.
- **S1, CGW-type structured zero:** the zero set contains, or equals, a locus defined by linear conditions on the invariants c_ij = −2p_i·p_j alone, with constant coefficients and no explicit energy dependence.
- **S2, deformed-amplitude zero:** after removing positive factors, P = (positive) × [α(Y, E)·M − β(Y, E)·G], with α, β monomials in the graph energies {E, Y, X_L, X_R} and G a single monomial in leg-energy differences. The zero is then a one-parameter (E) deformation of the flat zero M = 0, reducing to it as E → 0.
- **Generic:** neither of the above (irreducible numerator not of these forms).

## Tests
- T1 (sympy, exact): factor P using only the null-leg identities J⁰X = J·Y (left) and J⁰_R X_R = −J_R·Y (right). Classify as S1, S2 or generic.
- T2 (numeric): on the 200 COS-1c-type zeros (regenerated with the same seed), check that the factored form vanishes there (|residual| < 1e−10).
- T3: S1 test. Do the four-point conditions c₁₃ = c₂₄ = 0 (any linear c-set) force P = 0 for generic energies? Check symbolically or by random sampling on that locus.
- Lean: prove the factorisation identity (ring), if T1 confirms it.

## Verdicts
- **PASS-S1:** structured CGW-type zero.
- **PARTIAL-S2:** deformed-amplitude zero.
- **FAIL:** generic.

Credit 0 (formal, no data). Proposed only.
