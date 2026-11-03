# KL-LAT2 pre-registration (2026-10-13) — pushed BEFORE any target (K*, phi) value is read
Gate + memory audit: reviews/KL-LAT2-gate-2026-10-13.md. Lean: PositiveGeometryEmergentSpaceTime.KLPhi (phi_relation, equal_spacing, phi_from_kstar; 0 sorry; axioms propext/Classical.choice/Quot.sound only).
Predictions: sims/kllat2/predict.py → predictions.json (computed from inputs only; targets parsed and SEALED unprinted in targets_sealed_*.json by parse_pacs.py/parse_pq.py; digit-masked inspection of tables only).

## Data (selection fixed)
- PACS-CS Nf=2+1 (0807.1661 Table: masses in lattice units). m_s not tuned on phi/K* (physical point set by pi, K, Omega). Exclude a·m_pi<0.09 (m_pi<200 MeV).
- CP-PACS Nf=2 (hep-lat/0105015 tab:meson), UKQCD Nf=2 (hep-lat/0107021 tb:ps, tb:vector): partially quenched; light = sea kappa (unitary pi, rho); "strange" = any heavier valence kappa with PS(l,s), PS(s,s) available. Strange is valence-only (disclosed). UKQCD quenched set excluded. Some CP-PACS beta=2.10/2.20 rows not parsed by the regex (disclosed, not cherry-picked: parser fixed before reading targets).
- Independent groups: Tsukuba lineage (PACS-CS + CP-PACS, counted as ONE group) and UKQCD.
- Scored iff (m_K−m_pi)/m_rho ≥ 0.10 and m_pi/m_rho ≤ 0.80. All vector states here are ground-state energies (stable or treated as stable): no BW/pole convention issue.
- HadSpec 283/330 (2303.10701): same-ensemble rho found (BW a_t m = 0.13978(51) @330, 0.13440(34) @283; a_t m_pi, m_K in Table I), but NO HadSpec K* on these ensembles located → not scored (DATA-ABSENT). No lattice K2* found on any used ensemble → J=2 not scored.

## Observables and statistics
- O1 K*: δ = (m_K* − m_rho)/(m_K − m_pi); prediction from kstar_relation.
- O2 phi (NEW observable): ε = (m_phi − m_rho)/(2(m_K − m_pi)); prediction from phi_relation (LO GMOR). Secondary (reported, not scored): phi_alt with lattice eta_ss.
- Point PASS: |obs − pred| ≤ max(2σ, 0.10), σ from quoted target + rho errors (inputs' errors added in quadrature).
- Observable PASS: in EACH of the 2 groups ≥ 80% of scored points pass. Also reported: "all points pass" (KL-LAT-style strict rule).
- Nulls/baselines (stronger than KL-LAT):
  N1 band null f per point (U[0,1]).
  N2 heavy-vector ChPT-linear competitor: (m_V − m_rho)·m_rho = c (m_K² − m_pi²) per added strange quark, c = 0.411 from physical PDG masses (memorised; used for the null only). For phi: twice the K* shift.
  N3 δ, ε fixed at physical values (δ=0.336; ε=(1019.5−775.3)/(2·357.7)=0.341).
  An observable is DISCRIMINATING iff its pass fraction ≥ 0.8 AND exceeds both N2 and N3 pass fractions by ≥ 0.2 AND its mean |residual| is smaller than both.
- Offset check (KL-LAT systematic high): report mean signed mass residual (pred−obs)/obs per group. Pre-stated reading: if the K* prediction is high in ≥80% of these stable-state points, the KL-LAT offset is intrinsic to the relation (not a BW/pole convention artefact); if signs are mixed, the offset is consistent with convention/noise.

## Credit proposal fixed now
- O2 PASS + DISCRIMINATING in both groups → propose blind +0.5 (new observable; caveats: Nf=2 PQ strange, 1960s equal-spacing prior art, LO GMOR assumption). PASS but not discriminating → +0.25 at most (or 0). FAIL → 0, phi relation tagged REFUTED at these masses.
- O1 extension: corroborates KL-LAT; no new credit (same observable).
Tags: predictions SIMULATED from PROVED formulas; lattice values CITED. No tuning; no parameter refits.
