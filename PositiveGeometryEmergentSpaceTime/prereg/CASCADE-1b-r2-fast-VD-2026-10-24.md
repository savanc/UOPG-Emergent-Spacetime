# PREREG CASCADE-1b r2: re-run of the CASCADE-1b blind n = 6 re-test with a faster V_D (supersedes the r1 checker for r2 only)
Written 2026-10-24 by Grok. Same the author-approved rung as r1 ( "Ok go cascade1b and cascade 2", 2026-10-23, relayed). Not AutoResearch (paused at 39582f6, untouched).
Parent: prereg `prereg/CASCADE-1b-split-fix-blind-retest-2026-10-23.md` (27a47fd, LOCKED, not edited), refusal c008a8e, r1 result 3a57a17.
Pushed ALONE, ff-only, with checker v3, planted spec r2 and import test v3, before any r2 live computation. No physical datum enters.

## 0. Why r2, and what stays on record
- r1 (`CASCADE1b-2026-10-23-r1`) is **NOT-EVALUATED** (rule 3: V_D time kill 3600 s at n = 6, diamond X14). That verdict stays on record. The CASCADE-1 FAIL stays on record.
- Cause: v2 `V_D` brings the 14-term amplitude to a common denominator with sympy `together` on symbolic v (reviews/CASCADE-1b-result-2026-10-23.md §3).
- **Blind status:** no physical n = 6 V_D, S3/S4 cell, held-out test or control has been seen. r1 finished diamond X13 but the result was discarded in memory and never printed or stored. The target is unspent.

## 1. What r2 changes (and nothing else)
Checker v3 `sims/cascade1b/cascade1b_checker_v3.py` = v2 with only:
1. **V_D by the numerator method.** Write A_y = N/L with L the lcm of the term denominators (products of linear forms in y). On the locus {c^y_D = v} (solved linearly for |D| of the y, same `_pick`), A_y ≡ 0 iff N(sol) ≡ 0 as a polynomial in the free y, provided no factor of L vanishes identically. The coefficients of N(sol) in the free y generate the ideal; denominator factors that become functions of v only are removed by saturation (extra variable t, 1 − t·Π g, eliminated). A factor of L vanishing identically on the locus raises an error (counts as ILL-DEFINED). Same lex Gröbner in v; same `zero_only` and `gens` outputs. v2 `V_D` is kept as `V_D_v2`.
2. Per-diamond checkpoints `runs/CASCADE1b-2026-10-24-r2/vd.jsonl` and `progress.log`; stdout line-buffered.
3. Planted **PL10** (v3 V_D = v2 V_D on all 7 n = 4, 5 diamonds) and **PL11** (v3 V_D on a seeded (611) random-coefficient n = 6 triangulation sum, NOT the physical amplitude, all 9 diamonds, each < 60 s). Spec: `sims/cascade1b/planted_cases_r2.json` (PL1–PL11).
4. PREREG / RUN_ID / hash regex / output file names (`cascade1b_r2_planted.txt`, `cascade1b_r2_output.txt`, `cascade1b_r2_live.json`).

Unchanged: all definitions (r1 prereg §2), predictions (§3, copied below without edits), verdict rules (§6, incl. the 3600 s per-diamond V_D kill and the 900 s symbolic kill), held-out points and seed **202610231** (kept so that the only difference from r1 is the V_D implementation), data tiers, environment, guard logic.

## 2. Predictions (r1 prereg §3, unchanged)
| item | prediction | prob |
|---|---|---|
| V_D = {0} for all diamonds, n = 4, 5, 6 | yes (Θ_3 linear) | 0.85 |
| reproduction n = 4, 5 (relations, K, f) = v1 | exact | 0.97 (seen in smoke, §4) |
| E0-n6 | dim Θ_3 = 1 (the §7.1 δ-line μ_ee = −μ_oo), dim Θ_4 = 0, K = 0, BELOW | 0.85 |
| EM-n6 | dim Θ_3 = 15 − 9 = 6: offset map of rank 9, of which exactly one relation involves masses only (an alternating-type sum of m_i) | 0.70 (alt: dim 7, 0.15) |
| EM-n6 S4 | dim Θ_4 = 6 (uniform m_i = μ_P = M is an interior point) | 0.75 |
| EM-n6 K vs N_off | K = 6 < 9, BELOW; RATIOS-FREE | 0.70 |
| H re-test at n = 6 | REFUTED-AS-STATED (both n = 6 cells BELOW) | 0.80 |
| held-out factor count 90/90 (30 × 3 points) | PASS | 0.85 |
| held-out eq. 3.7 36/36 at points | PASS | 0.85 |
| eq. 3.7 symbolic | PASS 2/2 if not killed (P(killed) 0.4) | 0.85 |
| power control: generic θ off Θ_3 fails ≥ 1 of 30 factor-count tests | yes | 0.90 |
| n = 5 EM fixed v1 templates (symbolic) | 10/10 (seen in smoke, §4) | 0.97 |

## 3. Smoke / foregone (declared)
- v3 planted with the guard stubbed in a scratch copy (/tmp, not scored): **PL1–PL11 ALL OK** (PL11 max 0.30 s), ≈5 min.
- Post-hoc diagnostic in the r1 review: numerator method = v2 on n = 4, 5; 0.08 s / 0.22 s on n = 6 X13 / X14 for a random-coefficient sum (seed 99).
- r1 outputs (n = 4, 5 V_D = {0}; stages 0–2 reproduction) are known.
- The E0 and EM n = 6 offset maps o_ab(θ) were printed (analytic, not blind); E0 kernel = δ-line is PROVED (`Cascade1b.e0_n6_offsets_zero_iff`, 3a57a17). The rank of the EM map was not computed.
- **Never executed:** the physical n = 6 V_D (any diamond), any n = 6 cell, held-out, control, n = 5 templates under v3.

## 4. Verdict rules: r1 prereg §6, unchanged, applied to run `CASCADE1b-2026-10-24-r2`.

## 5. Lean: r1 prereg §7 items 2–5 in a new module `lean/PositiveGeometryEmergentSpaceTime/Cascade1bR2.lean` (namespace `PositiveGeometryEmergentSpaceTime.Cascade1bR2`), generated from the r2 output; item 1 is done (3a57a17). 0 sorry, no native_decide, standard axioms, AxiomsAll regenerated. Re-wordings declared in the result.

## 6. Guard and manifest
- Guard as v2: fetch once per process; the add-commit of THIS prereg must be an ancestor of origin/main; checker v3 sha256 below. `guard` in every scoring function (incl. the new `V_D`, `lcm_numerator`); no pass flag.
- Import test v3 must REFUSE before the push; output `sims/cascade1b/guard_refusal_r2.txt` (own commit, before the prereg push).
- Result manifest: r2 outputs + `runs/CASCADE1b-2026-10-24-r2/`; Lean module; AxiomsAll; `figures/cascade1b-r2-2026-10-24.png`; `reviews/CASCADE-1b-r2-result-2026-10-24.md`; BACKLOG/blocker/ledger/glossary/graph/AXIOMS updates.

## 7. What remains untested (by design): r1 prereg §12, unchanged.

Locked:
- `sims/cascade1b/cascade1b_checker_v3.py` sha256 `055468a070e3a21983e99fdabea07205573834030de77235475147f5f3ad5ad6`
- `sims/cascade1b/planted_cases_r2.json` sha256 `f86662598d43e07f22c302c462f798d56b1587a1885bc65aac1fa0c1ad82f4be`
- `sims/cascade1b/import_guard_test_v3.py` sha256 `ec84b5ee067654271790d1461ce57c8bb6406a8114d0a313f8975392d70cbf2c`
