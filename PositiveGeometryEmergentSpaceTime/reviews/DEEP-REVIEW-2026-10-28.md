# Deep review 2026-10-28: mission, trade space, Lean map, terms, publish-readiness

Reviewer: Grok (executor). Request: author approved, "full deep review of our mission and update full trade space, lean map, all terms and descriptions for lean and also make sure lean are ready to publish". Fold-in of 91578b8 per PositiveGeometryEmergentSpaceTime steering at. Locked files were not edited; superseding files are new and dated.

## 1. Summary
- **Mission: NOT ACHIEVED.**
  - No Standard-Model parameter, quantum number, N_c, N_gen or chirality has been derived from positive geometry: R4-DM v2 meter 1/89, meter_Q 0/73 (SIMULATED, run R4-DM-2026-10-20).
  - The single DERIVED item is EW-Z1b.forced. It is conditional, amplitude-sourced and an SM-MATCH (CGW 2601.16860 CITED).
  - Every rung since 10-20 ended as a NO-GO, NOT-WELL-POSED, ILL-DEFINED, method-only, FAIL or NOT-EVALUATED result. [ASSESS]
- **Lean: healthy and close to publishable** (PROVED).
  - 1027 theorems + 538 defs, standard axioms only, 0 sorry, clean-clone build green.
  - All 110 files have a module doc. 1487/1489 public decls have docstrings; the 2 without are auto `@[ext]` lemmas.
  - `#lint` shows only naming and unused-hypothesis style issues.
- **Remaining publish blockers:**
  - no LICENSE;
  - release scope (notebook vs Lean-only package);
  - certificate-data naming style.
  These are the author's decisions.
- **Most important corrections made:**
  - The theorem-map "primary rung" labelling was wrong for 32 modules, including Separation tagged R4, the R4-DM symptom. It is now derived from git history with a regression check.
  - FR-MU was missing from the blocker index.
  - The trade-space figure lagged three handoff deltas.
  - 9 broken glossary aliases.
  - README status counts were stale (336 theorems vs 1027 now).

## 2. What changed (all pushed ff-only to origin/main; no force, no history rewrite)
| Commit | Content |
|---|---|
| 7dd1653 | **Lean docs + lint.** Module docstrings and public-decl docstrings across 85 files; 9 alias-collision fixes in docstrings; 7 linter fixes: dead `<;> ring` in Network and PositroidCells; unused `have` in SliceBridge and IsingLoop; dead `try` in ScaleNoGo; Associahedron doc. **No statement changed.** |
| 43eec32 | **Map + tags.** New `scripts/primary_rung.py`: primary = the earliest review in git history that names the module. `theorem_graph.py` now has a baseline `graph/primary_rungs.json` with a regression check: it exits 1 on any change to the primary rung unless run with `--accept-primary-changes`. A negative test was run. It also registers nested modules (`LeanCert2.*`). `blocker_tags.py` gains CASCADE-1b (NOT-EVALUATED) and FR-MU (NUMEROLOGY) rows, plus `FM`, `BASIN` and `B3_EARLIER` registries and an FM column. New `scripts/basin_tally.py`. Regenerated BLOCKER-INDEX, graph/*, glossary and blueprint. EXCLUSION: appended failure-mode tally section. |
| aada524 | **Trade-space figure.** Applied handoff deltas -10-22, -10-23 and -10-28: GRADED-POSITROID and TRIALITY-WHY as run nodes; INT-1, FL-1Z, LEAN-CERT-1/2 and CASCADE-1/1b/2 nodes; basins B1–B5 and 2 hubs. Also notes/LEAN-NAMING-MAP-2026-10-28.md. |
| 9dfeac7 | notes/TRADE-SPACE-2026-10-28.md, notes/PUBLISH-CHECKLIST-2026-10-28.md, README dated status/build block |
| (this commit) | this review |

## 3. Tagged claim table (headline claims as of 2026-10-28)
| # | Claim | Tag | Evidence |
|---|---|---|---|
| 1 | The Lean library has 1027 theorems / 538 defs on standard axioms, 0 sorry | PROVED | AxiomsAll at 68ef38c (clean clone) and at the review HEAD |
| 2 | The SM is booted with zero fitted parameters | **NOT SUPPORTED** (mission goal; 0/73 meter_Q) | R4-DM v2, af4430e |
| 3 | EW-Z1b: the hidden zero forces a = ±g, λ4 = g² in the CGW Coulomb-branch toy | PROVED (Lean `EWZ1b`) + CITED (CGW). SM-MATCH, conditional, **not** a positive-geometry derivation | BLOCKER-INDEX |
| 4 | Positive-geometry data are scale-blind (no dimensionful output) | PROVED (ScaleNoGo, BR4 `no_scale`) | OP-2 / BR-4 / SG-1 |
| 5 | Graded positroid cubic moment ⇔ ACC | PROVED (`graded_cubic_iff_acc`); physics reading NO-LINK (tautological) | GRADED-POSITROID |
| 6 | Triality / Z_k explains 3 generations | **NO-GO**: NOT-FORCED, tautological condition (PROVED + SIMULATED) | 519d7fb |
| 7 | INT-1 chamber constancy closes P1 | PROVED + SIMULATED; PASS(CHAMBER-CONSTANT) ⇒ P1 closed as a **no-go** | INT-1 |
| 8 | FL-1Z neutrino ratio from level-1 integrality | NOT-WELL-POSED (D3 rank one, PROVED); credit 0 | FL-1Z |
| 9 | LEAN-CERT-1: certified N_ACC = 2 and ABHY dims | PROVED; UPGRADED (method) | LeanCert |
| 10 | LEAN-CERT-2: FR-WZW k = 0..3 certified | **Downgraded:** ILL-DEFINED as preregistered. k = 0, 1 PROVED; k = 2, 3 memory LIMIT (not proved) | bba9b34 |
| 11 | CASCADE-1: the cascade fixes a mass ratio | **FAIL** (locked, kill b; SIMULATED + PROVED `em_n5_zero_iff`). Void-on-audit reading unruled | 9ed0afd |
| 12 | CASCADE-1b r1 | NOT-EVALUATED (timeout) | 3a57a17 |
| 13 | CASCADE-1b r2 | IN PROGRESS / UNGRADED; blind target unspent | 9b1dca2 |
| 14 | CASCADE-2 | Preregistered, not run, deferred | 012ead2 |
| 15 | Basins B1, B5 saturated; B3 conditionally | [ASSESS] tallies re-run by script; tags are judgements | basin_tally.py |
| 16 | Hubs "QN-blind" and "window not point" are general | CONJECTURE | TRADE-SPACE-2026-10-28 §2 |
| 17 | 6 arXiv citations in Lean that had no in-repo record | CITED, verified at title/author level 2026-10-28 (arXiv API); equation numbers unchecked | checklist |

## 4. Findings (downgrades and overclaims)
1. **R4-DM-class mislabel was systemic.** 32 modules had the wrong primary rung in the theorem map (e.g. Separation R4 → GEOMETRY-STRUCT-SEPARATION, Network H-T2 → H-T1, BR4 PG-1 → BR-4, FDim F-DIM2 → F-DIM). Fixed by derivation from git history. **The author to confirm the 32 relabels** (list in §6). `TP1bMatrix` has no primary because no review names it.
2. **FR-MU (NUMEROLOGY) was missing from BLOCKER-INDEX** even though EXCLUSION and BACKLOG have it. Added.
3. **README overclaimed currency.** Its status blocks quoted "336 theorems" (13 Oct). The figure is now 1027 and the current state is in a dated block. Older blocks are kept as history.
4. **91578b8 tallies hold up, with caveats** [ASSESS]: FM tags are not recorded in any review; B5 counts INT-1, which is a PASS whose content is a no-go (still fires without it); B3 fires only with BACKLOG's earlier members; the tally script does not check consecutiveness. The "last-5 mode" line in 91578b8 leaves out the 1-counts but reaches the right verdict (not fired).
5. **LEAN-CERT-2 must not be cited as "k = 0..3 certified".** Only k = 0, 1 are PROVED.
6. **Glossary:** 9 broken aliases → 0. 125 of 186 physics-binder rows still have no stated meaning ("unverified"), including the Cascade1b binders `m13…m46`. Not guessed.
7. **IntChamber 26 vs 22**, raised in the -10-22 handoff, is **already reconciled** in lean/AXIOMS.md (e9f03cd: +4 compiler `.eq_n` lemmas). Not an open item.
8. **Lint:** 101 `defsWithUnderscore` come from certificate-data naming, partly emitted by the locked `sims/leancert2/emit_lean.py`. 20 `unusedArguments` are prereg-shaped hypotheses. Style only; no soundness impact.

## 5. Lint and axioms (2026-10-28)
- AxiomsAll: TOTAL theorems = 1027, defs = 538, nonstandard = 0; axiom_decls = 0, opaque = 0, sorry_dependent = 0.
- `#lint in PositiveGeometryEmergentSpaceTime` (15 linters): 121 errors in 1509 decls: defsWithUnderscore 101, unusedArguments 20; docBlame 0.
- Compiler warnings: 12 unnecessarySeqFocus (style).
- Docstrings: 1489 public, 2 missing (auto `@[ext]`).

## 6. The 32 primary-rung relabels (old → new; proposal for the author to confirm)
Null TH-1→M1; MassiveSpinor EW-Z1b→BH-2; BR6 none→BR-6; Associahedron STRUCT-1→M2c; BridgePLAssoc none→BRIDGE-PL-ASSOC; PositroidCells H-T3→H-T2; Network H-T2→H-T1; LECRatio M3w→M3; FT5aL FT-5c→FT-5a-L; COS1 COS-1r→COS-1; Cascade1b none→CASCADE-1b; Legendre TH-1→HANG-1; LSResidue MR-1c→MR-1; MassiveLS SC-1→MR-3; UnequalLS KL-LAT→KL-1-MR-1f-KS-1; HadronKinematics none→HANG-1; MassiveZero MR-2b→MR-2; KEtaGate FT-1-MR-7p→FRONTIER-1-rank-and-MR-1f-eta; LatticeGate LAT-3p-DZ-1→LAT-2; FT3Gate none→FT-3-gate; FT4Gate none→FT-4-gate; BR5p none→BR-5p; ScaleNoGo BR-4→OP-2; SG1 BR-4→SG-1; BR4 PG-1→BR-4; SC2 SC-2b→SC-2; FDim F-DIM2→F-DIM; RelEntropy none→DORAU-MUCH; STRUCT1 STRUCT-1b→STRUCT-1; Separation R4→GEOMETRY-STRUCT-SEPARATION; R4Indep R4-indep→R4-INDEPENDENT; AuditWitnesses none→LEAN-AUDIT. LeanCert2 and its 5 submodules → LEAN-CERT-2 (new modules).

## 7. Needs the author (nothing below was done)
1. MISSION "Frontier mode" item 4 amendment (91578b8 proposal): not applied.
2. Lift AUTORESEARCH-STOP: not lifted. AutoResearch was not restarted.
3. Next rung pick (B1, B3 and B5 saturated under the 91578b8 rule): not picked.
4. CASCADE-1 VOID-ON-AUDIT ruling: FAIL stands until ruled.
5. CASCADE-1b r2 grading: after its run ends, by its own prereg.
6. Confirm the 32 primary relabels (§6) and a primary for TP1bMatrix.
7. LICENSE choice and the public/private decision; release scope (Lean-only package recommended [ASSESS]).
8. Certificate-data renames vs `@[nolint]` for Mathlib-style naming.
9. Approval-gated items left untouched: M5 tick, MC-1, the hand-added TS-1 entries, EW-Z1. No credit changes were made.
