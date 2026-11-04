# STRUCT-1 prereg — SM hypercharges as the unique anomaly-free assignment (2026-10-15)
Pushed alone, before any Lean/sympy run. author approved. SM ledger line: **hypercharges / chiral content (structural)**.

## Prior-art sweep (from memory, CITED, not re-derived from sources)
Geng–Marshak (PRD 39, 1989), Minahan–Ramond–Warner (PRD 41, 1990), Babu–Mohapatra (1989–90): one SM generation, perturbative anomalies fix hypercharge ratios up to normalisation (with ν^c, ambiguity unless mass/Yukawa conditions are added). Lohitsiri–Tong 2019 (hypercharge quantisation, global anomalies). Physlib (lake dependency) has an SM anomaly-cancellation framework (Tooby-Smith; e.g. `SMNoGrav` one-family `accGravSatisfied`) but, from a file scan, no direct hypercharge-uniqueness theorem; we write a self-contained ℚ statement and cite Physlib. **Known result → credit 0** (anchor).

## Fitness gate
Finite polynomial algebra over ℚ; Lean-friendly; well-posed. No data. ✔

## Exact setting and assumptions (fixed now)
Left-handed Weyl fields of one generation: Q (3,2,y_Q), u^c (3̄,1,y_u), d^c (3̄,1,y_d), L (1,2,y_L), e^c (1,1,y_e); optionally ν^c (1,1,y_ν). Conditions: SU(3)²U(1): 2y_Q+y_u+y_d=0; SU(2)²U(1): 3y_Q+y_L=0; grav²U(1): 6y_Q+3y_u+3y_d+2y_L+y_e(+y_ν)=0; U(1)³: 6y_Q³+3y_u³+3y_d³+2y_L³+y_e³(+y_ν³)=0. Global/Witten anomaly not used (automatic for one generation of doublets: 4 doublets).

## Claims to test (Lean)
- C1 (no ν^c): if y_Q ≠ 0, then (y_u,y_d,y_L,y_e) = y_Q·(−4,2,−3,6) or y_Q·(2,−4,−3,6) (u^c↔d^c relabelling). I.e. SM up to normalisation and u↔d.
- C2 (no ν^c, y_Q = 0): the extra family y_L = y_e = 0, y_d = −y_u (exists; shows the y_Q ≠ 0 assumption is needed).
- C3 (with ν^c): the conditions do not fix hypercharge: B−L (1/3,−1/3,−1/3,−1,1,1) is an anomaly-free solution not proportional to the SM one (non-uniqueness witness → exclusion ledger).
- G (geometry): does any existing Lean positive-geometry module constrain these charges? Assessed by a graph/import check: any Lean edge from STRUCT1 to a geometry module that is used in the hypothesis or conclusion counts as a link.

## Fixed constant basis
Rationals p/q with |p|,|q| ≤ 10 (charge ratios). Nothing else.
## Locked checker
`49b66238608f1c1941e495ca166404069fbc3d5b0efe5690e99194fb06b23ac8  sims/struct1/struct1_acc.py`
## Planted-answer test (run after this push, before live)
Planted: two singlets (a,b) with grav + cubic only, normalised a = 1 → must give b = −1 uniquely. Broken: SM without SU(2)²U(1) → must be REJECTED (not unique). Either failing ⇒ STOP. Log → sims/struct1/struct1_planted.txt.

## Verdicts (exhaustive)
- Lean part: PASS if C1, C2, C3 all PROVED (0 sorry, standard axioms) and the checker agrees; PARTIAL if C1 needs assumptions beyond y_Q ≠ 0 (and u↔d); FAIL if a counterexample to C1 is found.
- Geometry part: SELECTS if some geometry module's theorem implies a hypercharge constraint; NO-LINK otherwise.
- Reported as "<Lean part> / <geometry part>". Otherwise (checker error, outside basis) → UNCLASSIFIED.
**Proposed credit:** 0.
