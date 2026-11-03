# STRUCT-2 review — does anomaly consistency fix N_c? (2026-10-15)
**Verdict: NO-GO-FOR-N_c=3 (exclusion PASS) / geometry NO-LINK** (prereg 954f096). Proposed credit **0** (known results). SM ledger line: gauge group choice (colour number).

## Why this rung (re-rank)
Proposed from the ledger: "gauge group choice" was 0% covered. Calibrated EV 0.060 > X6 0.027 and BRIDGE-PL-ASSOC 0.027 (capped).

## Assumptions (exact)
One generation of SM-like content with N colours, no νᶜ; gauge group SU(N)×SU(2)×U(1) and the representations assumed; charges in ℚ; perturbative ACC (`ACCN`, CITED coefficients); Witten condition = even number of SU(2) doublets (CITED, definition `Witten`). N1 assumes N ≠ 0 and yQ ≠ 0.

## Results (Lean `PositiveGeometryEmergentSpaceTime.STRUCT2`, 7 theorems, 0 sorry)
- `accN_unique` (N1): yQ·(N−1, −(N+1), −N, 2N) or the uᶜ↔dᶜ swap (key: `cubicN_factor`).
- `accN_solution` (N2): a solution exists for **every** N.
- `accN_three_eq_struct1`: at N = 3 this is exactly STRUCT-1 (Lean edge to STRUCT1).
- `witten_iff_odd` (N3): Witten ⇔ N odd. `witten_excludes_two`: the constraint is real.
- `three_not_selected` (N4): N = 3 and N = 5 both satisfy ACC + Witten.
- Checker (sims/struct1/struct2_nc_output.txt): symbolic-N branches match N1; N = 1…7 all solvable, Witten passes exactly the odd N. Planted pair OK (N = 3 reproduces STRUCT-1; N = 0 rejected as degenerate). Charge ratios lie in the basis (|p|,|q| ≤ 20). Checker hash verified unedited.

## Interpretation
Anomaly consistency restricts N_c only to odd values; it does **not** select 3. Selecting 3 needs further input, e.g. hypercharge/electric-charge quantisation matched to an observed charge (N_c enters via q_u = (N+1)/(2N) in units where y_e = 1), proton/electron charge neutrality, or π⁰ → γγ (classic N_c probes, all empirical). Positive geometry supplies none of these.

## Geometry assessment
**NO-LINK.** STRUCT2 imports STRUCT1 and Mathlib only.

## exclusion ledger
`accN_solution` + `three_not_selected`: rules out "N_c = 3 from (perturbative + Witten) anomaly consistency alone".

## Blockers / reopen triggers
`FRONTIER-THEORY`: a geometry-module theorem fixing the gauge rank or colour number (e.g. a positive geometry whose combinatorics forces a rank-2 (SU(3)) colour factor). Reopen trigger: a Lean edge from a geometry module into `ACCN`/`Witten` or into a colour-factor count.

## Compliance
Re-rank log (54f058b) ✔ · prereg alone (954f096) ✔ · planted ✔ · basis ✔ · locked hash ✔ · Lean PROVED with fresh AxiomsAll ✔ · exclusion ✔ · blocker/reopen ✔ · real timestamps ✔.

## Lesson
For structural targets, prove the general-N family first. Consistency conditions usually restrict parameters to a class (here: odd N), and the class, not the point, is the honest result.
