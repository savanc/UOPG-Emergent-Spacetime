# STRUCT-3 / R3 result — `N_gen` (2026-10-15)
Prereg + locked checker + planted pair: 924f548 (one commit, before the live run). Ranking: aecf7d1 (R3 EV 0.038 > R1 0.012).

## Verdict
**NO-GO-FOR-N_gen=3** (exclusion PASS). Geometry→STRUCT **NO-LINK**. Credit proposed 0.

## What ran
- Prior art: AF n_f ≤ 16 (Gross–Wilczek / Politzer), SM b₀(SU(2)) = 19/6, Kobayashi–Maskawa phase count, χ(Gr≥0) = 1 (Galashin–Karp–Lam 1707.02010), Postnikov cell counts.
- Planted pair: recovered (exit 0) and broken rejected (exit 1). The first planted attempt caught a wrong Higgs coefficient before locking; this is logged in the planted file.
- Live (sims/struct3/struct3_output.txt): AF(SU3) max 8, AF(SU2) max 5, AF ∧ KM window [3, 4, 5]. No invariant family is constantly 3. Hits at 3 come only from tuned parameters: Gr≥0(1,2), dim Gr(1,4) / Gr(3,4), and the n = 6 helicity-sector count. Catalan and χ never give 3.
- Lean `PositiveGeometryEmergentSpaceTime.STRUCT3`: 10 theorems + 3 defs, 0 sorry, standard axioms, lint clean.

## Reading
- Anomaly consistency (ACC, Witten) is blind to N_gen.
- The upper bounds come from AF (SU(2) is the tighter, ≤ 5). The lower bound comes from CP violation (≥ 3), which needs an empirical input.
- N_gen ∈ {3, 4, 5}: a class, not the point.
- Positive-geometry counts take the value 3 only when a free parameter (n, k) is chosen. That is look-elsewhere, not forcing. This confirms PJ-B1.
- After X6 the same pattern holds: consistency gives classes (odd N_c ≥ 3; N_gen ∈ [3, 5]), never the SM point.

## Assumptions
- One Higgs doublet.
- One-loop AF only (two-loop and Banks–Zaks windows not considered).
- KM as stated requires CP violation to come from the CKM.
- "Forced" means constant over the invariant's whole family in the checker's fixed list. Other invariants are not excluded (frontier).

## Blocker
`NO-GO` `FRONTIER-THEORY`. Reopen trigger: a geometry-module Lean theorem giving an index or count that is independent of n,k (or is fixed by kinematics, e.g. m = 4) and equals the number of generations, or an R1 identity tying generation number to a canonical-form residue.

## Lesson
For discrete targets, require the invariant to be **constant over its family** in the prereg. A single hit at 3 among many (k,n) is look-elsewhere noise, and the fixed-family rule makes rejecting it automatic.

## Credit
Proposal only: 0. CREDITS.md untouched.
