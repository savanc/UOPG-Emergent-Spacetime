# STRUCT-1b prereg — restoring hypercharge uniqueness with νᶜ (2026-10-15)
Pushed alone, before any Lean/sympy run for this rung. SM ledger line: **hypercharges (νᶜ case)**.

## Prior art (memory, CITED)
With νᶜ, anomaly cancellation leaves the B−L direction open; standard remedies are a Majorana mass for νᶜ (y_ν = 0) or Yukawa conditions (Babu–Mohapatra; Foot–Joshi–Lew–Volkas; Geng–Marshak). Dirac Yukawas preserve B−L, so they are not expected to fix it. Known results → credit 0.
## Fitness gate
Finite algebra over ℚ; reuses STRUCT1 (`ACC`, `ACCnu`, `hypercharge_unique`). ✔
## Setting (fixed)
STRUCT-1 fields + νᶜ (1,1,y_ν) + Higgs doublet H (1,2,y_H). Yukawa invariance: Q H uᶜ (y_Q+y_H+y_u=0), Q H* dᶜ (y_Q−y_H+y_d=0), L H* eᶜ (y_L−y_H+y_e=0), L H νᶜ (y_L+y_H+y_ν=0). Majorana: νᶜνᶜ invariant ⇔ y_ν = 0. Perturbative ACC only; y_Q ≠ 0; up to normalisation and uᶜ↔dᶜ.
## Claims (Lean)
- M: ACCnu + y_ν = 0 + y_Q ≠ 0 ⇒ SM (two labellings), via STRUCT1.hypercharge_unique.
- D (exclusion): ACCnu + all four Dirac Yukawas still allow a one-parameter family (contains SM and B−L) ⇒ not unique.
- MY: Yukawas + Majorana (without the cubic ACC) ⇒ SM with y_H = 3y_Q.
## Fixed basis
Rationals |p|,|q| ≤ 10.
## Locked checker
`67bc691a9318c67a45172369fb45365f11bf5828430dbf7301cfedf5d137d540  sims/struct1/struct1b_acc.py`
## Planted-answer test (after this push, before live)
Planted: the no-νᶜ case must return exactly the two SM branches (known STRUCT-1 answer). Broken: νᶜ with no extra condition must be REJECTED (free parameter). Log → sims/struct1/struct1b_planted.txt.
## Verdicts (exhaustive)
- PASS: M, D, MY all PROVED and the checker agrees.
- PARTIAL: M PROVED but D or MY fails or needs extra assumptions.
- FAIL: M false (a counterexample).
- Otherwise → UNCLASSIFIED. Geometry link reported separately (SELECTS / NO-LINK).
**Proposed credit:** 0.
