# TP-2 prereg — E7 Perron–Frobenius masses vs Blume–Capel quench-spectroscopy ratios (2026-10-13)
Committed before computation or data access.

## Numeric precheck (counts only): sims/tp2/tp2_numcheck.py → the figure captioned "Table 3" of arXiv 2506.19596v3
contains 8 decimal tokens.
## Status of the data: NUMERICAL SIMULATION (iTEBD quench spectroscopy), NOT an experiment → not an observable. TP-2 is a
consistency rung only. No measured E7 material was found in the sweep (search 2026-10-13).
## Contamination (disclosed): a search snippet showed the theory E7 ratios (1.28557 … 3.70166) and stated the quench
reproduced ≈1.286, 1.97, 2.532. The result is effectively known; value low.

## Prediction: sims/tp2/tp2_masses.py — PF eigenvector of the E7 Dynkin adjacency (chain 0..5, branch 6 at node 2),
sorted, normalised to m1. Eigenvalue must equal 2cos(π/18) (Coxeter h=18) — check.
## Cell: all decimal numbers in the Table 3 figure (sims/tp2/tp2_cell.py), nothing else.
## Verdicts (exhaustive)
- PASS: every Table-3 number in (1, 4) is within 1% of some predicted m_k/m_1, and ≥ 2 such numbers exist.
- PARTIAL: all within 3% but some between 1% and 3%.
- FAIL: some number in (1, 4) is > 3% from every prediction.
- otherwise → UNCLASSIFIED (incl. fewer than 2 numbers in (1, 4)).
Credit: 0 expected (known theory, simulation data).
