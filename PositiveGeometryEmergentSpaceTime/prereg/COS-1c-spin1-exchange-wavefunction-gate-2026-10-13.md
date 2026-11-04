# COS-1c prereg: physical-region zeros of a spin-1 exchange wavefunction (gate) — 2026-10-13

Status: PRE-REGISTERED before computation (AutoResearch). **Data cells: none.**

## Setup (derivation fixed now)
Charged massless (conformally coupled) scalars φ₁φ₂* → φ₃φ₄*, with s-channel photon exchange, flat-space wavefunction, Coulomb gauge (physical d.o.f. only, so there is no free boundary constant).
- Currents: J_L = (ω₁−ω₂, k₁−k₂), J_R = (ω₃−ω₄, k₃−k₄); Y = |k₁+k₂|, X_L = ω₁+ω₂, X_R = ω₃+ω₄, E = X_L+X_R.
- ψ_γ = (J_L·Π·J_R)/(E(X_L+Y)(X_R+Y)) + κ J⁰_L J⁰_R/(Y² E), where Π is the transverse projector.
- κ is fixed by requiring that the E→0 residue is the Lorentz-invariant amplitude (J_L·J_R)_Mink/(Y²−X_L²). Hand derivation gives κ = −1. The script must verify this symbolically and fail loudly if not.
- Assumption (memory): scalar QED with conformally coupled scalars is classically Weyl-invariant in 4D, so ψ_dS ∝ ψ_flat at tree level.

## Tests
- T0: symbolic E→0 residue check for κ = −1, using J⁰X = J·Y (null legs).
- T1: 10⁶ physical 3-momentum configurations; record the sign distribution of ψ_γ.
- T2: if both signs occur, locate zeros by bisection along random segments. Confirm E, X_L+Y, X_R+Y, Y > 0 there (all propagators finite), i.e. a hidden-type zero in the physical region.
- T3: compare with the flat-amplitude zero (J_L·J_R)_Mink = 0. Is it the same locus? Report the correlation.

## Verdicts
- **PASS:** T0 holds and a codimension-1 zero set exists in the open physical region (T2).
- **FAIL:** ψ_γ has a fixed sign.
- **INCONCLUSIVE:** T0 fails.

Credit: gate only, 0 (no data). If PASS, propose a follow-up COS-1d (an observable: a charged-spectator trispectrum template). Proposed only.
