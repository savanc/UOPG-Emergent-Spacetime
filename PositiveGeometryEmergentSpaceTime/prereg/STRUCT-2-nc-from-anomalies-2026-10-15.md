# STRUCT-2 prereg — does anomaly consistency fix the number of colours? (2026-10-15)
Pushed alone, before any Lean/sympy run for this rung. SM ledger line: **gauge group choice (colour number N_c)**.

## Prior art (memory, CITED)
SM-like content with general N_c: perturbative anomalies cancel for every N_c with hypercharges depending on N_c (e.g. Bär–Wiese "Can one see the number of colors?" 2001; Abbas; Shrock). Witten's SU(2) global anomaly requires an even number of doublets: N_c + 1 even ⇒ N_c odd. Known → credit 0.
## Fitness gate
Finite algebra; extends STRUCT1 (N = 3 must reproduce `hypercharge_unique`). ✔
## Setting (fixed)
One generation, Q (N,2,y_Q), uᶜ (N̄,1,y_u), dᶜ (N̄,1,y_d), L (1,2,y_L), eᶜ (1,1,y_e), no νᶜ. ACC: SU(N)²U(1): 2y_Q+y_u+y_d=0; SU(2)²U(1): N y_Q+y_L=0; grav: 2N y_Q+N y_u+N y_d+2y_L+y_e=0; cubic: 2N y_Q³+N y_u³+N y_d³+2y_L³+y_e³=0. Witten condition (CITED, as a definition): the number of SU(2) doublets (N+1) is even.
## Claims (Lean)
- N1: for N ≠ 0 and y_Q ≠ 0, y_u ∈ {(N−1)y_Q, −(N+1)y_Q} (cubic factor −6N y_Q (y_Q+y_u−N y_Q)(y_Q+y_u+N y_Q)), with y_L = −N y_Q, y_e = 2N y_Q.
- N2 (exclusion): for every N a solution exists, so perturbative ACC do not fix N_c.
- N3: Witten ⇔ N odd (N : ℕ).
- N4 (exclusion): N = 3 and N = 5 both satisfy ACC + Witten ⇒ consistency does not single out N_c = 3.
## Fixed basis
Rationals |p|,|q| ≤ 20 (charge ratios at N ≤ 7).
## Locked checker
`c450435bab5d3b009d7b5c2d39344918fd641de7cc69d9e95ba1632ba42b67b2  sims/struct1/struct2_nc.py`
## Planted-answer test (after this push, before live)
Planted: N = 3 must reproduce STRUCT-1's two branches. Broken: N = 0 must be REJECTED (degenerate). Log → sims/struct1/struct2_planted.txt.
## Verdicts (exhaustive)
- NO-GO-FOR-N_c=3 (exclusion PASS): N1–N4 PROVED (ACC + Witten restrict N_c only to odd values).
- SELECTS-3: ACC + Witten force N_c = 3 (would contradict N4).
- PARTIAL: N1–N3 proved but N4 fails or needs extra assumptions.
- Otherwise → UNCLASSIFIED. Geometry link reported separately.
**Proposed credit:** 0.
