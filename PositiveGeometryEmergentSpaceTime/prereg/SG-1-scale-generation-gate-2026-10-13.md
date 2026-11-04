# SG-1 prereg: scale generation, KK tower + Perron–Frobenius (gate) — 2026-10-13

Status: PRE-REGISTERED before any computation (AutoResearch). Proposed rung #2 of the out-of-box ladder.

## Question
Can a positive structure (Perron–Frobenius eigenvector of a non-negative matrix) plus a KK-type compactification produce (a) a discrete mass-ratio spectrum not put in by hand and (b) a dimensionful unit / an inter-sector ratio, i.e. break OP-2 ScaleNoGo?

## Prior art
E8 Toda / Ising-in-field masses = PF eigenvector of the E8 incidence matrix (Zamolodchikov 1989; Braden–Corrigan–Dorey–Sasaki 1990; Dorey 1991) *(memory)*; CoNb2O6, Coldea et al. Science 327 177 (2010) *(memory)*. KK towers m_n=n/R; CGW 2601.16860 [CITED]. Nothing new is claimed for (a); E8 values are remembered → CONTAMINATED, cap 0.25 (control).

## Tests
- **C (control):** compute exactly the PF eigenvector of the E8 Dynkin adjacency A. PASS if PF eigenvalue = 2cos(π/30), all components > 0, and m2/m1 = 2cos(π/5) = φ, full ratio list equals the standard closed forms to 1e-12.
- **G1 (ratios from positivity):** for every connected ADE graph (A_n n≤8, D_n n≤8, E6,E7,E8), PF eigenvector is strictly positive and its ratios are fixed by the graph alone (no continuous parameter). PASS/FAIL by exact check.
- **G2 (scale):** decide whether PF + KK can output a dimensionful quantity or fix the ratio between two sectors' units. Prediction (prior): NO — PF vectors are defined up to positive rescaling and the KK unit 1/R is free; product of a PF spectrum with a KK tower has a 2-dim scale freedom per sector. PASS (gate opens) only if an explicit mechanism fixes it without an added input.

## Verdicts
- SG-1 gate PASS if C, G1, G2 all pass; PARTIAL if C,G1 pass and G2 fails (structural no-go recorded, tag NO-GO); FAIL if C fails.
- Max credit: 0.25 (control, CONTAMINATED). Proposed only.
