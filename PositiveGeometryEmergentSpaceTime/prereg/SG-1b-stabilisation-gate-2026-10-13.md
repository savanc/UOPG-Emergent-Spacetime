# SG-1b prereg: can a positivity / PF-style stabilisation fix μR without a new input? — 2026-10-13

Status: PRE-REGISTERED before computation (AutoResearch). Follows SG-1 (G2 FAIL: μR free).

## Setup
Sector unit μ with E8 PF masses m_a = μ x_a (x_1 = 1). One compact dimension, length L = 2πR. Dimensionless target: t = μR.

## Prior art
Casimir/radion stabilisation (Appelquist–Chodos 1983; Ponton–Poppitz hep-ph/0105021; Arkani-Hamed et al. "SM from extra dims" hep-th/0703067) *(memory)*: stabilisation generically needs bosons and fermions with chosen masses/BCs or a bulk cosmological constant. Nothing new is expected on the physics; the claim tested is specific to PF-weighted towers.

## Candidate conditions (no new dimensionless input allowed)
- **S1 Casimir, single statistics:** 5D Casimir density for each E8 state, ρ(L) ∝ ∓ L⁻⁵ Σ_n c_n f(n m_a L)/n⁵, f(x)=(3+3x+x²)e^{-x}, c_n=1 (periodic) or (−1)ⁿ (antiperiodic). Both PF-weighted towers with all BCs fixed by the same rule (all periodic bosons; bosons+Scherk–Schwarz fermions with identical PF masses). PASS if V(L) has an isolated minimum at finite t.
- **S2 mixed signs:** E8 bosons plus N_f massless periodic fermions. Recorded: does a minimum exist, and does t* depend on N_f? If t* depends on a chosen count, that count is a new input → FAIL for "no new input".
- **S3 PF self-consistency:** combined operator A_E8 ⊗ 1 + κ·1 ⊗ T_KK (κ = 1/(μR)); does any intrinsic PF condition (e.g. degeneracy/level crossing of the PF eigenvalue, or PF vector of a single graph) pick a unique κ? PASS if unique without a chosen integer/graph.
- Lean: prove f antitone on x ≥ 0 (single-signed Casimir terms are monotone ⇒ no minimum) where feasible.

## Verdicts
PASS if any of S1–S3 fixes t uniquely with no added dimensionless input; PARTIAL if fixed only with one discrete choice (count, BC, graph); FAIL otherwise. Max credit 0.25 (mechanism is SM-external, no data). Credit proposed only.
