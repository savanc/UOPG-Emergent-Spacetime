# LEC-1 prereg — FT-5c zero-preserving LEC pattern vs BE14 fit (2026-10-13)
Committed before reading any value. CONTAMINATED: I recall phenomenological L_i signs/sizes (L5 clearly nonzero);
expectation is FAIL. Prediction (FT-5c, tree-level, large-Nc assumption): L2 = 2L1, L3 = −2L2, L4 = L6 = 0, L5 = L8 = 0.
Scale ambiguity disclosed: tree relations compared at the fit's μ (no running applied).

## Precheck (no values seen): sims/lec1/lec1_numcheck.py, lec1_structure.py → ar5iv 1405.6488 (Bijnens–Ecker) figure
index 2 ("Table 3"), header [fit, BE14, free fit], rows 10^3 L_A^r, L_1^r … L_8^r, χ², F_0.
## Cells (only these; sims/lec1/lec1_cells.py): BE14 column, rows L1, L2, L3, L4, L5, L6, L8 (value ± error).
Errors combined in quadrature, correlations ignored (stated limitation).
## Verdicts (exhaustive)
- PASS: all six relations (L2−2L1, L3+2L2, L4, L6, L5, L8 = 0) within 2σ.
- FAIL: L5, L8, or L3+2L2 differs from 0 by > 3σ.
- PARTIAL: not PASS, not FAIL, and L3 + 2L2 within 2σ.
- otherwise → UNCLASSIFIED (incl. parse failure, missing errors).
Credit: 0 expected (contaminated).
