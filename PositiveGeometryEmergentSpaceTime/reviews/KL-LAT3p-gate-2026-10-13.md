# KL-LAT3′ gate (2026-10-13), mass-level rule: **GATE FAIL (stopped before any data)**

## Rule (author approved 2026-10-13)
Mass-level test; lattice vector masses (K*, phi, rho) with errors ≤1 %; only in the region where KL-1 and linear-ChPT rival N2 differ by >2σ combined; fitted rival curvature = extra input; pre-register both predictions + sign of our high offset.

## Gate: inputs only, SIMULATED (sims/kllat3p/gate_masslevel.py, *_output.txt)
KL-1: m_V²/m_rho² = 1 + n(K²−π²) (n=1 K*, n=2 phi); N2: m_V/m_rho = 1 + n·0.411(K²−π²) (c frozen in KL-LAT2). σ = 1 % on each, so σ_comb = 1.41 %. Grid π/ρ 0.15–0.50, K/ρ 0.50–1.00.
- K*: max z = 1.14 → **never** discriminating.
- phi: z > 2 only at **K/ρ ≥ 0.95** (z up to 3.4 at K/ρ = 1.0, light π; gap −3 to −5 %, KL-1 *below* N2). At K/ρ = 0.8 z ≤ 0.6, because the curves cross near K/ρ ≈ 0.75; at physical-like K/ρ ≈ 0.64, z ≈ 0.7–1.0. This **corrects** the KL-LAT3 note's "≳ 0.8" boundary: the real threshold is ≈ 0.95.
- Reaching K/ρ ≥ 0.95 needs m_K ≳ m_rho, meaning a sea strange mass of roughly 3× physical or more.

## Ensemble structure search (structure only; no vector-mass values read)
One search plus memory, disclosed. CLS/RQCD strange-varied (m_s up to ~1.2–1.5× phys, so K/ρ ≲ 0.7), BMW (near physical), HadSpec SU(3)-point (K = π, so K/ρ ≈ 0.4–0.5 and the gap is ~0), PACS-CS/QCDSF (K/ρ ≲ 0.7), ETMC Nf=2 K* (valence-heavy partially quenched, m_K ≤ 650 MeV, so K/ρ ≲ 0.7; also not unitary), HPQCD phi (physical m_s). **Zero groups** with full-QCD ensembles at K/ρ ≥ 0.95 and ≤1 % vector masses; need ≥2. Near K/ρ ≈ 1 the phi also sits close to K K̄ and the vector states are resonances, so a 1 % stable-state mass is doubtful even in principle.
Memory audit: I remember the physical K*/phi masses and the rough lattice trend; I don't remember any K/ρ ≥ 0.95 vector masses (none exist that I know of). Nothing was sealed or hashed, because there are no targets to seal. Prereg of predictions/offset sign: not filed (no test to attach it to).

## Nulls
Not run (no data). Inputs-only result: at ≤1 % the K* channel can never separate the rules. With 0.5 % errors, phi near physical K/ρ reaches z ≈ 1.5–2.0, still marginal.

## Lean
None. The result is numeric (SIMULATED); the algebra is already PROVED in KLPhi/UnequalLS.

## Blocker tag
`FRONTIER-DATA / DATA-ABSENT`: the discriminating region (phi, K/ρ ≥ 0.95, ≤1 %) has no ensembles from even one group. Reopen: a heavy-sea-strange 2+1 campaign, or ≤0.5 % phi masses near physical K/ρ from 2 groups. KL line otherwise parked as `NOT-DISCRIMINATING`.

## Proposed credit: 0. Tally unchanged: blind 2.5 | VR 1.0 | total 3.5/3.
