# TP-1d prereg — numeric E8 ratio cells (2026-10-13)
Follows TP-1c (UNCLASSIFIED: abstracts non-numeric). Prediction fixed in sims/tp1c/tp1c_masses_output.txt (ebc4ced):
m_k/m_1 = 1, 1.618034, 1.989044, 2.404867, 2.956295, 3.218340, 3.891157, 4.783386.
Memory-contaminated (≈1.6 recalled); no blindness claimed. Prediction is theory-fixed, nothing tunable.

## Cells (only these are opened; pulled by committed script sims/tp1d/tp1d_cells.py)
Source text: arXiv full-text PDFs of 1103.3694 (D1) and 2005.13302 (D2), converted with pdftotext inside the script; full text is never printed or saved.
- D1 cells: sentences (split on ". ") of 1103.3694 containing "golden" or "m2/m1"/"m_2/m_1" or "ratio" AND a digit. Max 6 sentences.
- D2 cells: sentences of 2005.13302 containing ("m_" or "m1".."m8" or "ratio" or "golden") AND a digit with decimal point. Max 10 sentences.
Only these sentences are written to sims/tp1d/tp1d_cells.txt and read.

## Scoring
Use only numeric ratios m_k/m_1 (or energies from which a ratio to m_1 is formed) stated in the cells, with stated σ where given.
Match: within 2σ, or within 3% if no σ.
## Verdicts (exhaustive)
- PASS: D1 m2/m1 matches AND all D2 ratios found match (≥1 D2 ratio with k≥3 found).
- PARTIAL: D1 m2/m1 matches but D2 has no k≥3 ratio, or some D2 ratio fails.
- FAIL: D1 m2/m1 off by >5% (and >2σ).
- otherwise → UNCLASSIFIED.
