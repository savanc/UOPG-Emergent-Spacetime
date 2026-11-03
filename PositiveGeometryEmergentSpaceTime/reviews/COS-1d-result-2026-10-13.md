# COS-1d result: zero surface of the spin-1 exchange wavefunction — PARTIAL-S2 (deformed-amplitude zero) (2026-10-13)

Prereg: `prereg/COS-1d-zero-surface-structure-2026-10-13.md` (0349f86, definitions fixed before computation; hand sketch disclosed). Script: `sims/cos1d/cos1d_zero_surface.py` → `_output.txt`. Lean: `lean/PositiveGeometryEmergentSpaceTime/COS1d.lean` (`psi_factor`, `psi_zero_iff`), wired; build 9042 jobs; AxiomsAll **569 thm, 193 defs, nonstandard = 0**.

## Result (exact)
ψ_γ = [Y·M − E·J⁰_L J⁰_R] / [Y·E·(X_L+Y)(X_R+Y)],  with M = (J_L·J_R)_Mink = (p₁−p₂)·(p₃−p₄) and J⁰_L J⁰_R = (ω₁−ω₂)(ω₃−ω₄).

- **T1:** sympy factorisation confirms the hand sketch exactly (ratio = 1). Lean proves the identity and that ψ = 0 ⇔ Y·M = E·(ω₁−ω₂)(ω₃−ω₄), with all denominators positive.
- **T2:** the factored form vanishes at all 200 zeros (≤ 1e−16 E³). Its sign matches ψ at 10⁶/10⁶ points.
- **T3, S1:** fails. On the c₁₃ = c₂₄ = 0 locus, ψ never vanishes (0/2000). The only linear c-locus available at 4 pt with null legs is collinear, and ψ ≠ 0 there.

**Verdict: PARTIAL-S2** (per prereg). The zero is a structured one-parameter deformation of the flat amplitude zero: M = (E/Y)·(ω₁−ω₂)(ω₃−ω₄). It reduces to M = 0 as E → 0 and to the charge-symmetric slice M = 0 when ω₁ = ω₂ or ω₃ = ω₄. It is not a CGW-type linear-in-c zero.

## Physical reading
The correction term is the instantaneous (Coulomb) piece. The wavefunction zero is shifted off the amplitude zero by an amount ∝ E/Y, i.e. it grows away from the energy-conserving limit and is largest for soft exchanged momentum Y. This is the concrete "wavefunction-specific" structure COS-1c found numerically.

## Not done / assumptions
- dS₄ ⇔ flat carries over only under the (memory) Weyl-invariance assumption.
- No observable: this is not yet the inflaton trispectrum.
- Gauge choice: Coulomb gauge was used, with κ fixed by Lorentz invariance of the residue. Another gauge could add boundary terms; that is not checked.

## Blocker tags / next
`FRONTIER-THEORY` (observable). Next candidate, COS-1e: the same analysis for graviton or spin-1 exchange between *inflaton* legs (an EFT-of-inflation trispectrum). Does the S2 zero M = (E/Y)·G survive, and is it inside the SO/Euclid-accessible shape region?

## Proposed credit (NOT awarded): 0 (formal result, no data).
