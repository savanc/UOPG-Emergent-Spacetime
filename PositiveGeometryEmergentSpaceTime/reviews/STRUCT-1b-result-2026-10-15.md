# STRUCT-1b review — hypercharge uniqueness with νᶜ (2026-10-15)
**Verdict: PASS (Lean) / NO-LINK (geometry)** (prereg d140e00). Proposed credit **0** (known results). SM ledger line: hypercharges (νᶜ case).

## Assumptions (exact)
One generation, STRUCT-1 content plus νᶜ (1,1,yν) and one Higgs doublet H (1,2,yH); gauge group and content assumed; charges in ℚ; perturbative ACC (`STRUCT1.ACCnu`); Yukawa invariance `Yuk` (Q H uᶜ, Q H* dᶜ, L H* eᶜ, L H νᶜ); Majorana ⇔ yν = 0; yQ ≠ 0 where stated.

## Results (Lean `PositiveGeometryEmergentSpaceTime.STRUCT1b`, 5 theorems, 0 sorry)
- `majorana_unique` (M): ACCnu + yν = 0 + yQ ≠ 0 ⇒ SM up to normalisation and uᶜ↔dᶜ. Real Lean edge to STRUCT1 (`hypercharge_unique`).
- `dirac_family`, `dirac_not_unique` (D, exclusion): ACCnu + all four Dirac Yukawas allow the family (1, t, −t−2, −3, 2−t, t+4), which contains the SM (t = −4) and 3·(B−L) (t = −1). **Dirac Yukawas do not restore uniqueness**, because B−L is a symmetry of the Yukawas.
- `yukawa_majorana` (MY): Yukawas + Majorana + only the linear SU(2)²U(1) condition ⇒ SM with yH = 3yQ (i.e. yH = 1/2 at yQ = 1/6). The SU(3)²U(1), gravitational and cubic conditions are not needed.
- Checker agrees (sims/struct1/struct1b_acc_output.txt): Majorana → two SM branches; Dirac → one-parameter family; both → unique SM with yH = 3. Planted pair OK (the no-νᶜ case recovered; νᶜ with no extra condition rejected). Basis |p|,|q| ≤ 10. Checker hash verified unedited.

## Geometry assessment
**NO-LINK.** STRUCT1b imports STRUCT1 and Mathlib only. The extra principle that restores uniqueness (lepton-number violation via a νᶜ Majorana mass) is a dynamical or symmetry input; no positive-geometry module supplies it.

## exclusion ledger
`dirac_not_unique`: rules out "hypercharge fixed by ACC + Dirac Yukawas" once νᶜ is present.

## Blockers / reopen triggers
`FRONTIER-THEORY` (same as STRUCT-1): a geometry-module theorem that forces yν = 0 (Majorana) or an ACC/Yukawa equation. Reopen trigger: a Lean edge from a geometry module into `ACCnu`/`Yuk`.

## Compliance
Timestamp-fix + re-rank commit (2993004) before the prereg ✔ · prereg alone (d140e00) ✔ · planted ✔ · basis ✔ · locked hash ✔ · Lean PROVED with fresh AxiomsAll ✔ · exclusion ✔ · blocker/reopen ✔.

## Lesson
Check whether an extra "selection" condition is invariant under the unwanted direction before testing it. Dirac Yukawas conserve B−L, so they could never remove the B−L family; a symmetry argument predicts the outcome in one line.
