# Trade space 2026-10-28: supersede note for notes/TRADE-SPACE-2026-10-23.md (Grok, deep review, author approved)

The earlier notes (-10-22, -10-22b, -10-22c, -10-23) are left unchanged. This note supersedes their status lines for the rungs below and adds the basin view from notes/AUTORESEARCH-METHOD.md (91578b8, 2026-10-28). Everything not named here still stands. The figure figures/trade-space-traffic-light.mmd/.png was updated in aada524 to match this note.

Tags: PROVED (Lean, standard axioms only) / SIMULATED (run id) / CITED / CONJECTURE / SPECULATION / [ASSESS] (judgement by the reviewer, not a computation).

## 0. Mission-level position (unchanged in substance, restated)
- **Goal:** a positive-geometry structure that boots up the Standard Model with zero fitted parameters.
- **Where it stands:** **NOT ACHIEVED.**
  - The latest derivation meter (R4-DM v2, 2026-10-20, prereg af4430e) counts 1/89 DERIVED items: EW-Z1b.forced only. That item is CONDITIONAL, amplitude-sourced and an SM-MATCH (CGW 2601.16860 CITED). Approved by the author.
  - meter_Q = 0/73: no quantum number, N_c, N_gen or chirality is derived from positive geometry. Items sourced from positive geometry: 0.
  - No rung since then has changed this. [ASSESS: every rung after 10-20 was a NO-GO, NOT-WELL-POSED, ILL-DEFINED, method or NOT-EVALUATED result.]
- **Lean base** (PROVED, `lake build` green, re-checked 2026-10-28 in a fresh clone at 68ef38c and in the review worktree):
  - 1027 theorems + 538 defs;
  - 0 nonstandard axioms, 0 sorry-dependent decls, 0 `axiom` / `opaque` decls.
  - FRONTIER-AXIOM appears only as a declared hypothesis, never as an `axiom`.

## 1. Rung status (supersedes earlier status lines)
| Rung | Status 2026-10-28 | Evidence | Tag |
|---|---|---|---|
| LEAN-CERT-1 | DONE, UPGRADED (method; credit 0) | reviews/LEAN-CERT-1-result-2026-10-23.md; `PositiveGeometryEmergentSpaceTime.LeanCert` | PROVED (N_ACC = 2; ABHY dims 5/9/14) |
| LEAN-CERT-2 | **ILL-DEFINED** (locked null N2 131/480; post hoc the 131 are valid alternative P certificates). Lean: FR-WZW k = 0, 1 + ABHY **PROVED**; k = 2, 3 **memory LIMIT**, not claimed | bba9b34; reviews/LEAN-CERT-2-result-2026-10-28.md; run LEANCERT2-2026-10-28-r1 | PROVED (k = 0, 1) / SIMULATED (8/8 dims) / LIMIT (k = 2, 3) |
| CASCADE-1 | **Locked FAIL** (kill b). H REFUTED-AS-STATED; RATIOS-FREE. The checker mass-mapping defect was found on audit; the VOID-ON-AUDIT reading has **no ruling** (the author), so FAIL stands | 9ed0afd; run CASCADE1-2026-10-23-r1; `PositiveGeometryEmergentSpaceTime.Cascade1` | SIMULATED + PROVED (`em_n5_zero_iff`, `split5_of_rel_*`) |
| CASCADE-1b r1 | **NOT-EVALUATED** (locked v2 V_D hit the 3600 s kill at the n = 6 diamond X14) | 3a57a17 (2026-10-24); run CASCADE1b-2026-10-23-r1 | SIMULATED (planted ALL OK; n = 4, 5 reproduction) |
| CASCADE-1b r2 | **IN PROGRESS / UNGRADED.** Prereg 9b1dca2 (2026-10-24), guard refusal b9f97a8; the blind n = 6 target is **unspent** | not graded in this review (the run process was still live during the review and was not touched) | none yet |
| CASCADE-2 | Prereg 012ead2 (2026-10-28), guard refusal 5bb3693. **NOT RUN, deferred** (AUTORESEARCH-STOP) | prereg/CASCADE-2-delta-deformed-ratio-test-2026-10-28.md | none |
| TRIALITY-WHY | NOT-FORCED / TAUTOLOGICAL-CONDITION (NO-GO) | 519d7fb; `PositiveGeometryEmergentSpaceTime.TrialityWhy` | PROVED + SIMULATED |
| GRADED-POSITROID | NO-LINK (TAUTOLOGICAL-REPRODUCTION) / NO-GO | reviews/GRADED-POSITROID-result-2026-10-22.md | PROVED (`graded_cubic_iff_acc`) |
| INT-1 | PASS (CHAMBER-CONSTANT) ⇒ P1 CLOSED as a no-go | reviews/INT-1-result-2026-10-22.md; `PositiveGeometryEmergentSpaceTime.IntChamber` | PROVED + SIMULATED |
| FL-1Z | NOT-WELL-POSED; no TS-1 entry | reviews/FL-1Z-result-2026-10-22.md; run FL1Z-2026-10-22-r3 | PROVED (`D3_rank_one`) + SIMULATED |
| FR-MU | NUMEROLOGY (in EXCLUSION and BACKLOG; **was missing from the blocker index, added 2026-10-28**) | notes/EXCLUSION-LEDGER.md | [ASSESS] |

AutoResearch has been paused since 2026-10-28 (AUTORESEARCH-STOP on origin/main). This review does not lift it and does not pick a rung.

## 2. Basins and failure modes (fold-in of 91578b8; tallies re-run, not copied)
The 91578b8 note defines five basins and FM tags (FM-FREE, FM-SPEC, FM-RANGE, FM-MODEL, FM-QNBLIND, FM-TAUT, FM-LIMIT). The tags are now in scripts/blocker_tags.py (`FM`, `BASIN`, `B3_EARLIER`) and in a new "Failure mode" column of notes/BLOCKER-INDEX-2026-10-13.md. `python3 scripts/basin_tally.py` reproduces the counts:

| Basin | Rungs | FM tally (re-run 2026-10-28) | Saturation trigger (≥ 3 of one FM) |
|---|---|---|---|
| B1 LS-pion amplitude + deformations | F-DIM, F-DIM′, F-DIM-MASS, F-SCATLEN, F-RHOWIDTH, F-POSGEOM-DAUGHTER | MODEL 3, SPEC 2, RANGE 1, FREE 1 | **FIRED** (MODEL × 3) |
| B2 positroid / associahedron ↔ charge | BRIDGE-PL-ASSOC, GRADED-POSITROID | QNBLIND 2, TAUT 1 | not fired |
| B3 SM-consistency counting | STRUCT-NGEN, TRIALITY-WHY (+ earlier STRUCT-2, X6/XD-6/R2, STRUCT-3/R3) | RANGE 2, TAUT 1; earlier members RANGE 3 | fires **only if** the 3 earlier BACKLOG members are counted |
| B4 Lean certification (method) | LEAN-CERT-1, LEAN-CERT-2 | SPEC 1, LIMIT 1 | not fired |
| B5 ratio fixing (positivity / integrality / cascade) | F-COULOMB, INT-1, FL-1Z, CASCADE-1, CASCADE-1b | FREE 4, SPEC 2, LIMIT 1 | **FIRED** (FREE × 4) |
| All basin rungs | 17 | FREE 5, SPEC 5, RANGE 3, MODEL 3, QNBLIND 2, TAUT 2, LIMIT 2 | — |
| Mode form, last 5 rungs (LEAN-CERT-1, CASCADE-1, TRIALITY-WHY, CASCADE-1b, LEAN-CERT-2) | | SPEC 2, LIMIT 2, FREE 1, TAUT 1, RANGE 1 | not fired (the 91578b8 note left out the 1-counts; the conclusion is the same) |

Caveats [ASSESS]:
- (i) Every FM tag is a reviewer judgement. No review file carries a `Failure-mode:` line, so the tallies count judgements, not computations.
- (ii) B5's trigger counts INT-1, which is a PASS (CHAMBER-CONSTANT) whose content is a no-go. Without INT-1, FM-FREE is 3 and the trigger still fires.
- (iii) B3 saturation depends on the BACKLOG "class-not-point" phrase that admits the earlier members.
- (iv) basin_tally.py does not check that the rungs ran consecutively.

**Two cross-basin hubs** (added to the figure):
- **"Geometry is blind to quantum numbers"** (FM-QNBLIND / FM-TAUT). Edges from BRIDGE-PL-ASSOC, GRADED-POSITROID and TRIALITY-WHY.
- **"Consistency gives a window, not the point"** (FM-RANGE). Edges from STRUCT-NGEN, TRIALITY-WHY, X6/XD-6, STRUCT-2, STRUCT-3 and F-DIM′.

Status: CONJECTURE as a general pattern, supported by the tagged rungs above. It fits the CASCADE-1 lesson "linear consistency conditions tie parameters together but never fix a ratio" (CONJECTURE, 10-23 note).

## 3. Revised feed (proposals only; nothing here is approved)
- **P4 / B5:** the linear cascade is closed at n ≤ 5. CASCADE-2 (non-linear δ-deformed stage) is the only pre-registered next step. Its prior of a ratio fix is about 0.05 (CONJECTURE, 10-23 note). It is deferred.
- **CASCADE-1b r2** must be graded by its own prereg once its run ends. This review does not grade it.
- **B1, B3 (conditional) and B5 are saturated** under the 91578b8 rule. Under that rule, the next rung should come from a non-saturated basin or a new one. The rung choice, the MISSION "Frontier mode item 4" amendment and lifting STOP are **The author's decisions** (see DEEP-REVIEW-2026-10-28 "Needs the author").
- Unchanged: M5 tick, MC-1, the hand-added TS-1 entries and EW-Z1 (approval-gated, untouched).
