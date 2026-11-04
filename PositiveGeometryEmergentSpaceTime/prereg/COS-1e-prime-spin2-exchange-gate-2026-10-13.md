# COS-1e′ prereg: does Lorentz residue-matching fix the spin-2 exchange wavefunction? — 2026-10-13

Status: PRE-REGISTERED after one disclosed exploratory decomposition (see AUTORESEARCH-LOG). **Data cells: none.** Flat space; scalar legs are massless, minimally coupled, distinct species (1,2 | 3,4), s-channel graviton.

## Setup
- T_L^{μν} = p₁^μp₂^ν + p₂^μp₁^ν − η^{μν} p₁·p₂ (same for R). These are conserved off the energy shell (null legs).
- Lorentz numerator: N = T_L·T_R − ½ T_L T_R.
- ψ = N_TT/(E E_L E_R) + I/E, where I is an instantaneous kernel whose E→0 limit must equal (N − N_TT)/(Y² − X²).

## Tests
- T1: compute (N − N_TT)/(Y² − X²) with conservation. Is there a unique X-free off-shell expression? Record all off-shell lifts of the explicit X² term that agree at E = 0: X_L², X_R², −X_L X_R, and the one-parameter family X² → −X_L X_R + c·E(X_L − X_R)/2.
- T2: for each lift (c ∈ {−1, 0, 1}, plus X_L² and X_R²), sample 10⁵ physical points. Record the sign fractions of ψ and the fraction of points where the ψ sign differs between lifts.

## Verdicts
- **PASS (fixed):** T1 gives a unique lift, as in spin-1.
- **AMBIGUOUS:** the lifts differ in ψ (T2 > 0.1 % sign disagreement). The zero surface is then not fixed without the ADM constraint solution (`FRONTIER-THEORY`; reopen with a canonical ADM derivation).
- **FAIL:** ψ is single-signed for every lift.

Credit 0. Proposed only.
