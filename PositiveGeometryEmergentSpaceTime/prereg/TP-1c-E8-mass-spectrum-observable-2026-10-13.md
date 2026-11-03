# TP-1c prereg — E8 PF eigenvector → measured quasiparticle mass ratios (2026-10-13)
Written before any computation or data access.

## Claim under test
The Perron–Frobenius eigenvector of the E8 Cartan/adjacency matrix (TP-1b, Lean) gives the 8 particle masses of the
Ising field theory in a longitudinal field (Zamolodchikov 1989; Braden–Corrigan–Dorey–Sasaki). Predicted ratios m_k/m_1
will be computed by committed script `sims/tp1c/tp1c_masses.py` from the TP-1b eigenvector (no memorised numbers).
Novelty: none (known theory). This rung tests whether the PositiveGeometryEmergentSpaceTime PF chain reaches an observable; credit expected 0.

## Data cells (cell-level prereg; nothing else opened)
Only the *abstracts* of:
- D1: Coldea et al., Science 327, 177 (2010), "Quantum criticality in an Ising chain: experimental evidence for emergent E8 symmetry" (CoNb2O6): the reported m2/m1 value (+uncertainty if given).
- D2: Zou et al., PRL 127, 077201 (2021), "E8 spectra of quasi-one-dimensional antiferromagnet BaCo2V2O8 under transverse field": any mass ratios stated in the abstract.
Pulled by a committed script that saves only the abstract text; no figures/tables/supplements opened. If an abstract is
unavailable via public read-only fetch, that datum is recorded as MISSING (not filled from memory).
Contamination disclosure: I recall D1 reports m2/m1 ≈ 1.6 (golden ratio). Prediction is fixed by theory so cannot be tuned.

## Verdicts (exhaustive)
- PASS: m2/m1 from D1 within 2σ of prediction (or within 3% if no σ), AND every ratio stated in D2's abstract within 2σ/3%.
- PARTIAL: m2/m1 matches as above but some D2 ratio fails, or D2 MISSING/has no numeric ratio.
- FAIL: m2/m1 outside 5% of prediction.
- otherwise → UNCLASSIFIED (incl. D1 MISSING, or between 3% and 5% without σ).
