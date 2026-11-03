# CASCADE-1b result: locked verdict NOT-EVALUATED (V_D time kill at n = 6); no n = 6 prediction was scored
Written 2026-10-24 by Grok. The author-approved rung ( "Ok go cascade1b and cascade 2", relayed). Not AutoResearch (paused at 39582f6, untouched).

- Prereg: `prereg/CASCADE-1b-split-fix-blind-retest-2026-10-23.md`, commit 27a47fd (22:43:40 +0100), pushed alone, ff-only. Unchanged; nothing here amends it.
- Guard refusal: commit c008a8e (`sims/cascade1b/guard_refusal.txt`). Declared deviation (already in that commit message): recorded in a scratch clone pinned to pre-prereg main 39582f6, after the prereg push.
- Run: `CASCADE1b-2026-10-23-r1`, seed 202610231, locked checker v2 sha256 `977d66f1…`.
  - planted: PL1–PL9 ALL OK (`sims/cascade1b/cascade1b_planted.txt`);
  - live: started, ended ≈ 2026-10-24 (`cascade1b_output.txt`, `cascade1b_live.json`, `runs/CASCADE1b-2026-10-23-r1/progress.log`).
- Credit: 0 proposed (method rung, nothing scored).

Tags: PROVED = Lean, 0 sorry, standard axioms. SIMULATED(r1) = locked run above. SIMULATED(post-hoc) = scratch diagnostic after the run, not preregistered. CITED = arXiv 2312.16282 as fetched for the prereg.

## 1. Verdict
**NOT-EVALUATED** (prereg §6 rule 3): `VERDICT (python): NOT-EVALUATED (V_D time kill 3600s at n=6)`. Rules 1–2 did not fire (planted ALL OK, reproduction exact). No S3/S4 cell, held-out test or control at n = 6 was computed, so H, the RATIO sub-verdicts and the split fix are **untested**, not passed and not failed. The CASCADE-1 locked FAIL stays on record and is not re-labelled.

## 2. Predicted vs observed
| item (prereg §3) | prediction | observed |
|---|---|---|
| reproduction n = 4, 5 stages 0–2 = v1 | exact (0.97) | exact: f = (2,1,0) and (55,4,0), A = triangulation sum — SIMULATED(r1) |
| V_D = {0}, n = 4 | yes | yes, 2/2 diamonds, Gröbner [v0] — SIMULATED(r1) |
| V_D = {0}, n = 5 | yes | yes, 5/5, Gröbner [v0, v1] — SIMULATED(r1) |
| V_D = {0}, n = 6 | yes (0.85) | NOT-EVALUATED: diamond X13 (skinny) finished in ≈12 min but its result was discarded when the list comprehension raised Kill on diamond X14 (square, 3600 s); 7 diamonds not reached |
| E0-n6 dim Θ3 = 1, K = 0 BELOW | 0.85 | NOT-EVALUATED. The run-independent half is PROVED: `e0_n6_offsets_zero_iff` (c-preserving E0 shifts = δ-line, 2312.16282 §7.1 CITED) and `e0_n6_collapse` |
| EM-n6 dim Θ3 = 6; S4 dim 6; K = 6 < 9 BELOW, RATIOS-FREE | 0.70 / 0.75 / 0.70 | NOT-EVALUATED |
| H re-test REFUTED-AS-STATED | 0.80 | NOT-EVALUATED |
| held-out factor count 90/90; eq. 3.7 36/36; symbolic 2/2 | 0.85 each | NOT-EVALUATED |
| control fails ≥ 1 | 0.90 | NOT-EVALUATED |
| n = 5 EM templates 10/10 | 0.97 | NOT-EVALUATED (scheduled after S3 in run_live) |

Figure: `figures/cascade1b-2026-10-23.png` (V_D status per diamond; script `sims/cascade1b/cascade1b_figure.py`, reads the JSON and progress log only).

## 3. Why the kill fired (audit; no re-score)
- v2 `V_D` calls `poly_coeff_eqs(A_y.subs(sol), free)`, which puts the 14-term n = 6 amplitude over a common denominator with sympy `together`/`cancel` on symbolic v. py-spy at 23:58 and showed the process inside `poly_coeff_eqs` on diamond X14 (`progress.log`). The cost is the rational-function arithmetic, not the Gröbner step (≤ 4 variables).
- Planted coverage gap (declared): PL7 tests V_D only at n = 4; no planted case timed V_D at n = 6 under the 3600 s budget. Same failure class as CASCADE-1 (planted cases not covering the n of the blind target).
- Second defect: `[with_kill(...) for d in diamonds(n)]` loses completed diamonds when a later one is killed. Results should be written per diamond.
- SIMULATED(post-hoc): a numerator-polynomial V_D (N = Σ_T a_T Π_{P∉T} y_P, substitute the locus, coefficients in the free y, Gröbner in v, saturate v-only denominators) reproduces v2's Gröbner bases on all 7 n = 4, 5 diamonds and takes 0.08 s / 0.22 s on n = 6 diamonds X13 / X14 for a **random-coefficient** n = 6 sum (seed 99), not the physical amplitude. The physical n = 6 V_D was not computed, so the blind target is unspent.

## 4. Lean
`lean/PositiveGeometryEmergentSpaceTime/Cascade1b.lean` (namespace `PositiveGeometryEmergentSpaceTime.Cascade1b`): 2 theorems + 1 def, imports Mathlib only, no native_decide, 0 sorry; `lake build PositiveGeometryEmergentSpaceTime.Cascade1b` OK. Prereg §7 item 1 only (re-worded: the δ-line is stated as ∃ d, μ_ee = d, μ_oo = −d, μ_eo = 0; positivity uses μ13, μ24 ≥ 0, which suffices). Items 2–5 need run relations and are **not done**. AxiomsAll totals: see `lean/AXIOMS.md`.

## 5. What remains untested
Everything at n = 6 listed in §2 (V_D, both cells, H, RATIO, held-out, control, n = 5 templates under v2), plus prereg §12 (n ≥ 7, S0–S2 at n = 6, non-translation mass insertions, the CASCADE-1 VOID-ON-AUDIT question).

## 6. Next
Proposed: **CASCADE-1b r2** under a new superseding prereg (this one stays locked): checker v3 = v2 with only `V_D` replaced by the numerator method (planted-equal to v2 at n = 4, 5, per-diamond checkpoints, flushed output), same predictions, same kill budget, new run id. Because no n = 6 physical V_D or cell was computed, the blind target is still clean. Run it before CASCADE-2 consumes the n = 6 V_D.
