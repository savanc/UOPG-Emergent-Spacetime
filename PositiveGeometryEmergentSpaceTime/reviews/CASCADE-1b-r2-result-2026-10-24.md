# CASCADE-1b r2 result: PASS (held-out n = 6 factorisation on the EM-n6 final family); ratios stay free

Graded 2026-10-29 by Grok, after the run ended (LIVE_EXIT 0, about on 29 Oct). The author's standing instruction is to grade with the locked v3 checker, build the Lean, push, then pause.
The file name follows the r2 prereg manifest (§6: `reviews/CASCADE-1b-r2-result-2026-10-24.md`); the date is the run ID's, not the grading date.

- Prereg: `prereg/CASCADE-1b-r2-fast-VD-2026-10-24.md` (9b1dca2, on origin/main). Verdict rules: r1 prereg `prereg/CASCADE-1b-split-fix-blind-retest-2026-10-23.md` §6 (27a47fd), unchanged.
- Guard refusal before push: b9f97a8 (`sims/cascade1b/guard_refusal_r2.txt`).
- Run: `CASCADE1b-2026-10-24-r2`, seed 202610231, started 2026-10-28, elapsed 151 630 s (42.1 h). Mode live, with the checker's line "GUARD OK: prereg 9b1dca2aa on origin/main; checker hash matches".
- Outputs, copied unchanged from the run worktree:
  - `sims/cascade1b/cascade1b_r2_output.txt`
  - `cascade1b_r2_planted.txt`
  - `cascade1b_r2_live.json`
  - `runs/CASCADE1b-2026-10-24-r2/` (vd.jsonl, progress.log)
- Figure: `figures/cascade1b-r2-2026-10-24.png` (from `sims/cascade1b/cascade1b_r2_figure.py`).

## 1. Manifest check (SIMULATED, re-run at grading)
| locked file | prereg sha256 | sha256 at grading | |
|---|---|---|---|
| sims/cascade1b/cascade1b_checker_v3.py | 055468a0…5ad6 | 055468a0…5ad6 | unchanged |
| sims/cascade1b/planted_cases_r2.json | f8666259…be | f8666259…be | unchanged |
| sims/cascade1b/import_guard_test_v3.py | ec84b5ee…cf2c | ec84b5ee…cf2c | unchanged |

- Seed 202610231, as preregistered.
- The worktree's tracked files under sims/, prereg/ and lean/ were unmodified (`git diff --quiet HEAD`).
- Planted PL1–PL11: ALL OK (PLANTED_EXIT 0).

**Disclosure.** Two earlier r2 attempts were interrupted:
- `runs/CASCADE1b-2026-10-24-r2-interrupted-attempt1/` (LIVE_EXIT 143);
- `-attempt2/`.

Both stopped after the massless reference k0, before any held-out point or the control. Their printed S3/S4 cells are identical to the scored run, which is expected because the code is deterministic. No held-out or control number was seen before the scored run. Both folders are kept in the record.

## 2. Verdict, by the locked rule
r1 prereg §6, applied in order:

| rule | condition | this run | fires? |
|---|---|---|---|
| 1 | planted failure, or n = 4, 5 reproduction not exact → ILL-DEFINED | PL1–PL11 ALL OK; stages 0–2 reproduce v1 True; relations and K at n = 4, 5 match v1 (4/4) | no |
| 2 | EM-n6 Θ_3 nonlinear or empty → NOT-POSED | Θ_3 linear, dim 6 | no |
| 3 | V_D time kill (3600 s per diamond) → NOT-EVALUATED | all 16 diamonds zero-only; max 0.28 s at n = 6 | no |
| 4 | held-out violated → FAIL | factor count 90/90 (k = k0 at every test, 3 points); eq. 3.7 36/36 | no |
| 5 | held-out passes and control passes everywhere → PASS-UNDERPOWERED | control off Θ_3: 0/30 | no |
| 6 | otherwise → PASS | | **yes** |

**Verdict: PASS.** It was decided by rule 6, after rules 4 and 5 did not fire.

The symbolic eq. 3.7 sub-check was killed at its 900 s limit. The prereg treats that case in two places:
- §2 Held-out item 3 says "a kill gives NOT-EVALUATED, which is not a FAIL";
- the refutation condition counts it only "if completed".

Rule 3 covers only the V_D kill. So the symbolic kill is reported as NOT-EVALUATED and does not block PASS. The point-wise eq. 3.7 checks (36/36) are the scored ones.

Reported separately, as the rules require:
- **H re-test:** REFUTED-AS-STATED. H is CONFIRMED only if all 6 cells MATCH; here E0-n4 BELOW, EM-n4 ABOVE, E0-n5 BELOW, EM-n5 MATCH, E0-n6 BELOW, EM-n6 BELOW.
- **RATIO sub-verdicts:** E0 cells NO-MASSES-SURVIVE; EM cells RATIOS-FREE (n = 4, 5, 6).

The CASCADE-1 locked FAIL (9ed0afd) stays on record. Whether it is void on audit is still the author's decision. The r1 NOT-EVALUATED (3a57a17) also stays on record.

## 3. Numbers (SIMULATED)
- **E0-n6:** dim Θ_3 = 1 (δ-line), dim Θ_4 = 0, K = 0, N_off = 9, BELOW, NO-MASSES-SURVIVE.
- **EM-n6:** dim Θ_3 = 15 − 9 = 6, dim Θ_4 = 6, K = 6, N_off = 9, BELOW, RATIOS-FREE.
  - Of the 9 relations, exactly one involves masses only: m1 − m2 + m3 − m4 + m5 − m6 = 0.
  - Final family: 6 free parameters t0..t5 (m2..m6 = t1..t5, mu46 = t0).
- **Massless reference:** k0 = 2 on 18 tests and k0 = 3 on 12.
- **Held-out points 0–2:** factor count 30/30 each; eq. 3.7 12/12 each.
- **Control:** a generic θ off Θ_3 (seeded) gives k = 1 ≠ k0 on all 30 tests (0/30 pass), so the test has power.
- **Other checks:** n = 5 EM fixed v1 templates 10/10 (symbolic). V_D = {0} at every diamond, n = 4, 5, 6.
- **Predictions (prereg §2):** every scored prediction came true. These include dim 6 with one alternating mass relation (prob 0.70), K = 6 < 9 BELOW, H refuted, 90/90, 36/36 and the control failing. The symbolic attempt was killed; the prereg gave that a 0.4 chance.

## 4. What it means (ASSESS)
- **What passed.** On the EM-n6 final family, the near-zero factorisation of 2312.16282 (eq. 3.7/3.8, CITED) holds at three blind seeded points, and an off-family control fails. The v2 split fix (same substitution in the locus and the amplitude) works at n = 6. PL11 adds a planted case at the blind n for V_D (random-coefficient n = 6 sum), which narrows the coverage gap behind CASCADE-1 and r1. There is still no planted n = 6 held-out split case; the off-family control plays that role.
- **What it does not show.** The prereg's own mechanism (§3) says the held-out family follows from S3, because y = X − μ is a translation that preserves every physical c_ab. So this PASS tests the code path and the split fix, not new physics. The Lean module below proves that mechanism (`c_transport`, `zeros6_of_rel_*`). An independent held-out target, such as loop level or non-translation mass insertions, remains open (r1 prereg §12).
- **The ratio question is unchanged.** Every EM cell is RATIOS-FREE. At n = 6 the hidden-zero cascade leaves a 6-dimensional family with every mass ratio free, and only the alternating mass-sum relation constrains masses. No stage fixes a ratio. This is the FM-FREE pattern of basin B5.
- **The cascade hypothesis H stays REFUTED-AS-STATED,** now with n = 6 included: K is below N_off in both n = 6 cells.

**Steelman.** CASCADE-1 failed on a checker defect, and r1 was killed by cost. r2 now shows a clean n = 6 blind pass with a working control and 11/11 planted cases. The machinery (V_D numerator method, mass-consistent splits, guard and manifest) is sound at the target n. The full prediction table came true. That shows the analytic picture of the cascade is right: hidden zeros fix the mass offsets linearly and leave the ratios free. That is a clean statement to build on. CASCADE-2 (012ead2, the non-linear δ-deformed stage) is the preregistered next test of whether a non-translation stage can do more.

**Critique.** The pass is close to guaranteed by construction (§3 mechanism), and the review must say so. The symbolic check did not complete. f_2(n = 6) = 0 is assumed (r1 prereg §12). Nothing here bears on an SM number.

## 5. Map and meter
- **Basin B5 (ratio fixing).** RATIOS-FREE again at n = 6. The verdict is PASS, so no blocker fires. Registry delta, applied in f60b159 (author approved 2026-10-29): CASCADE-1b failure mode FM-LIMIT (r1) → FM-FREE (r2 ratio sub-verdict) [ASSESS]. It moves B5 from FREE×4 to FREE×5.
- **Blocker registry.** The CASCADE-1b row text is updated to record r2. Tags are unchanged: NOT-EVALUATED stays as r1's locked verdict, and PASS is a status, not a blocker.
- **Derivation meter.**
  - The r2 prereg has no meter rule, so the meter is **not re-run** and stays at **1/87 DERIVED, meter_Q 0/73** (R4-DM v3, d9b60aa, 2026-10-20).
  - Note: neither `PositiveGeometryEmergentSpaceTime.Cascade1b` nor `PositiveGeometryEmergentSpaceTime.Cascade1bR2` is in the v3 meter's module classification, and the v3 meter predates both. A future meter run must classify them first, or it refuses (METHOD R4-DM rule).
  - The result contains no derived SM item: ratios are free.

## 6. Lean (PROVED, `lean/PositiveGeometryEmergentSpaceTime/Cascade1bR2.lean`, namespace `PositiveGeometryEmergentSpaceTime.Cascade1bR2`)
The module is generated by `sims/cascade1b/gen_lean_r2.py` from the EM-n6 relations in `cascade1b_r2_live.json`, with offsets re-derived independently from eq. 2.4. It is byte-identical to the worktree draft. Over ℚ; 0 sorry; no native_decide. The r1 prereg §7 items it covers:
- `em_n6_offsets_zero_iff` (item 2): all nine EM offsets vanish ⇔ the nine live relations hold.
- `a6_zero_skinny`, `a6_zero_square`: the massless A6 vanishes on a skinny and a square diamond locus (reproduces 2312.16282 §3, CITED).
- `c_transport`: on the relations, every physical c_ab(X) equals c_ab(y), with y = X − μ.
- `zeros6_of_rel_skinny`, `zeros6_of_rel_square` (item 3): on the relations, A6(X − μ) = 0 on the skinny and square loci.
- `eq37_line1`, `eq37_line2` (item 4): eq. 3.7 lines 1 and 2 as explicit factorisations (field identities).
- `uniform_interior` (item 5): the uniform point m_i = μ = M satisfies the relations.

Re-wordings, declared as the prereg requires:
- Items 3 and 4 are proved for the massless amplitude in y coordinates, plus the linear transport lemma.
- Eq. 3.7 is stated as an explicit factorisation; the checker tests the equivalent rank-1 condition.

What Lean does **not** check: the held-out point counts, the control and the RATIO sub-verdict. These are SIMULATED (python, locked checker).

AxiomsAll audit (2026-10-29, full `lake build` of all 9107 jobs OK): TOTAL theorems=1164 defs=633 nonstandard=0, axiom_decls=0, sorry_dependent=0 (was 1155/630 before this module). All 9 Cascade1bR2 theorems use only [propext, Classical.choice, Quot.sound]. See `lean/AxiomsAll_output.txt`.

## 7. Tags
- PASS: SIMULATED, locked checker v3.
- The mechanism (pass by translation): PROVED (Lean, above).
- RATIOS-FREE and H REFUTED-AS-STATED: SIMULATED.
- The reading in §4: ASSESS.
- The FM delta: ASSESS, applied in f60b159.
- Credit 0 (no SM quantity).

## 8. Next
Per the author's standing instruction, pause after this push: no further rungs. CASCADE-2 (012ead2) is preregistered and not run.

Failure-mode: none (PASS; ratio sub-verdict RATIOS-FREE reported separately)
