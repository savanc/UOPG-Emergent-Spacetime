# KL-LAT: K* mass at unphysical pion masses vs lattice — **PASS 4/4 (3 blind-clean points, 3 groups)** — 2026-10-13
Prereg `prereg/KL-LAT-prereg-2026-10-13.md` (92eeee3, pushed before any lattice K* value). Predictions from inputs only `sims/kllat/predict.py` (00dbe80, pushed before reading targets). Check `sims/kllat/check.py`.

## Gates
- Prior art (CITED): AVW 1969 m_K*²−m_K² = m_ρ²−m_π²; Weinberg-type chiral derivation ("Stringy mass squared splittings reexamined"); KKY 1969. No lattice test of the relation across unphysical masses found in the sweep (not proof none exists). Ours: derivation of the intercept from the hidden-zero line (Lean UnequalLS, PROVED earlier: kstar_relation, mass_formula, 0 sorry, standard axioms).
- Method fitness: PASS. Ratios only (no scale input); lattice K* masses are outputs of Lüscher finite-volume analyses (no group tunes m_s with K*). Inputs m_π, m_ρ (OP-2 units) + m_K (strange free unit): 0 extra inputs; 1 observable (a function) at N points → counts as ONE observable.
- Well-posedness caveat: mass conventions differ (HadSpec/Brett BW mass, Rendon pole Re); used as quoted, ρ in the same group/ensemble.
- Memory audit: G3 (Graz, 891±14) excluded before reading. G1-391 flagged PARTIAL before reading; the read value (1406.4158 mR = 933 MeV) confirms my vague recall → **G1-391 CONTAMINATED**, reported, not counted blind. No recall of G1-239, G2, G4.
- Not collected: HadSpec 284/327 (no same-ensemble ρ located in time); K2* not available on these ensembles → J=2 not scored.

## Results (SIMULATED prediction from PROVED formula; data CITED)
δ = (m_K* − m_ρ)/(m_K − m_π); pass |Δδ| ≤ max(2σ, 0.10); null δ ~ U[0,1].
| Point | Group | m_K* pred | m_K* lattice | mass err | δ pred | δ obs ± σ | PASS | null f | blind |
|---|---|---|---|---|---|---|---|---|---|
| G1-391 | HadSpec | 0.1656 | 0.1652 | +0.3 % | 0.525 | 0.509 ± 0.045 | yes | 0.20 | no (contam.) |
| G1-239 | HadSpec | 0.1509 | 0.1487 | +1.5 % | 0.434 | 0.384 ± 0.011 | yes (band floor; 4.4σ statistically) | 0.20 | yes |
| G2-317 | Alexandrou/Rendon et al. | 0.5214 | 0.5173 | +0.8 % | 0.497 | 0.463 ± 0.035 | yes | 0.20 | yes |
| G4-230 | Bulava/Morningstar (Brett et al.) | 0.1511 | 0.1500 | +0.8 % | 0.434 | 0.408 ± 0.035 | yes | 0.20 | yes |
(lattice units; HadSpec MeV converted with the paper's own Ω scale; Rendon GeV with a = 0.11403 fm, same as the ρ paper.)

- Rung **PASS** by the prereg rule (≥2 groups, all points pass, each group discriminating). Blind-clean: 3 points, 3 analysis groups (G1-239 and G4-230 share one HadSpec gauge ensemble but are independent analyses).
- Null: per point 0.20; joint for the 3 blind points ≈ 0.008 (points correlated via shared physics, so treat as optimistic).
- Honest caveats: (1) prediction is systematically high in all 4 points (+0.3 to +1.5 % in mass); G1-239 passes only on the 0.10 floor, 4.4σ statistically. (2) A cruder baseline "δ fixed at its physical value ≈0.33" also passes 2/3 blind points (fails G2), so the test is moderately discriminating. (3) The relation is 1969 prior art; the blind content is its validity off the physical point, plus our hidden-zero derivation.

## Proposed credit (needs the author)
- **Blind line +0.5** (default: clean blind PASS, but prior-art relation, one observable, mild systematic tension). Alternative +1 if counted like MR-4. Tally would become blind 2.5 (or 3.0) | VR 1.0 | total 3.5 (or 4.0)/3.
