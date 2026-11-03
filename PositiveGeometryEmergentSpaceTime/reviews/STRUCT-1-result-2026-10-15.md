# STRUCT-1 review — hypercharge anchor (2026-10-15)
**Verdict: PASS (Lean anchor) / NO-LINK (geometry)** (prereg 13e0ea8). Proposed credit **0** (known result). SM ledger line: hypercharges / chiral content.

## Exact assumptions
- One generation; left-handed Weyl fields Q (3,2), uᶜ (3̄,1), dᶜ (3̄,1), L (1,2), eᶜ (1,1); optionally νᶜ (1,1). Gauge group SU(3)×SU(2)×U(1) **assumed**, representation content **assumed**.
- Charges in ℚ. Perturbative anomaly conditions only: SU(3)²U(1), SU(2)²U(1), mixed gravitational, U(1)³ (coefficients CITED in the definitions `ACC`, `ACCnu`). No global or Witten anomaly used. No Yukawa or mass conditions.
- C1 additionally assumes yQ ≠ 0. Uniqueness is up to overall normalisation and the uᶜ↔dᶜ relabelling.

## Results (Lean `PositiveGeometryEmergentSpaceTime.STRUCT1`, 8 theorems, 0 sorry)
- `hypercharge_unique` (C1): without νᶜ and with yQ ≠ 0, (yu,yd,yL,ye) = yQ·(−4,2,−3,6) or yQ·(2,−4,−3,6). With yQ = 1/6 this is the SM (−2/3, 1/3, −1/2, 1). Key step: `cubic_factor`.
- `yQ_zero_family`, `yQ_zero_family_not_sm` (C2): the yQ ≠ 0 hypothesis is needed.
- `bminusl_anomaly_free`, `sm_nu_anomaly_free`, `not_unique_with_nu` (C3): with νᶜ the anomaly conditions do **not** fix hypercharge. The sympy check shows a one-parameter family (yd = −yu − 2, ye = 2 − yu, yν = yu + 4 at yQ = 1, plus the u↔d branch).
- Checker (sims/struct1/struct1_acc_output.txt) agrees on all three. Planted pair OK (toy singlet pair recovered; dropping SU(2)²U(1) rejected). All ratios are in the fixed basis (|p|,|q| ≤ 10). Checker hash verified unedited.

## Geometry assessment (honest)
**NO-LINK.** STRUCT1 imports only Mathlib, and its graph edges go to no positive-geometry module. Nothing in the Associahedron, positroid, spinor or hidden-zero library constrains U(1) charges. Hidden zeros and factorisation in our modules are colour-ordered statements about a fixed adjoint/bi-adjoint theory; they say nothing about chiral representation content or anomalies. The hypercharges are fixed by anomaly cancellation given (gauge group, field content, yQ ≠ 0, no νᶜ). **Every one of those givens is an assumption the geometry does not currently supply.** STRUCT-1 is therefore an anchor (a target), not a geometric derivation.

## exclusion ledger
`not_unique_with_nu`: rules out "hypercharge fixed by perturbative anomaly cancellation alone" once νᶜ is present. An extra principle is needed (Majorana-mass/Yukawa conditions or a geometric input). Added to notes/EXCLUSION-LEDGER.md.

## Blockers / reopen triggers
`FRONTIER-THEORY`: a positive-geometry statement that forces (i) the chiral field content or (ii) an anomaly-cancellation-equivalent constraint (e.g. consistency of colour-dressed amplitudes, or a Gr⁺ orientation fixing chirality, CROSS-DOMAIN X6). Reopen trigger: a Lean theorem in a geometry module whose conclusion is one of the ACC equations.

## Compliance
Prior art (memory, CITED; Physlib framework noted) ✔ · fitness gate ✔ · METHOD update committed first (62aa72e) ✔ · prereg alone (13e0ea8) ✔ · planted pair ✔ · fixed basis ✔ · locked checker hash ✔ · Lean PROVED, fresh AxiomsAll ✔ · exclusion ledger ✔ · blocker + reopen ✔.

## Lesson
Anchor theorems should state every external given as an explicit hypothesis. The geometry question then becomes "which hypothesis can a geometry module discharge?", and the answer for each one is a ledger entry.
