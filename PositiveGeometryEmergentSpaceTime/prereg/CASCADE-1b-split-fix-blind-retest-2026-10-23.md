# PREREG CASCADE-1b: independent blind re-test of the CASCADE-1 cascade at n = 6 with a mass-consistent held-out split test
Written 2026-10-23 by Grok. **The author-directed manual frontier rung** ("Ok go cascade1b and cascade 2 and unpause AutoResearch", 2026-10-23, relayed by the parent). Not AutoResearch; AutoResearch is not touched.
Parent rung: CASCADE-1 (prereg af1bb37, refusal 42608d9, result 9ed0afd). Source of this rung: BACKLOG entry CASCADE-1b (PROPOSED in 9ed0afd).
Pushed ALONE, ff-only, with the locked checker v2, planted spec and import test, before any live computation. No physical datum enters.

## 0. Status of CASCADE-1 (unchanged by this rung)
- The CASCADE-1 locked python verdict **FAIL** (EM-n5 held-out splits 0/10) **stays on record**. This prereg does **not** void it; the author has not ruled on "void on audit".
- The CASCADE-1 result traced the failure, post hoc, to a split_test mass-mapping defect: the locus was solved with symbolic m while the amplitude had m → t.
- CASCADE-1b is an **independent re-test**. It has a new locked checker v2 (`sims/cascade1b/cascade1b_checker.py`), which supersedes v1 for this rung only. v1 files are not edited.
- The verdict-bearing target is a **NEW held-out family at n = 6** that has never been computed on any massive family.

## 1. Hypothesis and target
**H (unchanged from CASCADE-1, re-tested at a new n).** In the pre-declared mass-shifted Tr φ³ setting, the final free-parameter count equals the number of chord offsets: K_final = N_off (N_off = 9 at n = 6). In other words, no stage removes a mass ratio.

**H-split (the held-out claim being re-tested; new target).** On the S4 final family of EM-n6, the near-zero factorisation of 2312.16282 (eq. 3.8; explicit forms eq. 3.7) holds. Each near-zero locus is built from the **physical** c_ij with the **same** final-family substitution applied to the locus and to the amplitude (the v2 fix).

## 2. Exact definitions (2312.16282, CITED, fetched 2026-10-23, text at /tmp/hz.txt during the run)
**Kinematics.**
- Kinematics, the parameters Θ = (μ, m) and the settings E0/EM are as in CASCADE-1 §2.
- Chords (a, b); X_{i,i+1} = m_i, X_{1,n} = m_n.
- c_{i,j} per eq. 2.4.
- Amplitude A_X = A_y(y = X − μ). A_y is the massless Tr φ³ amplitude:
  - at n = 4, 5, the S2 output of the CASCADE-1 stage-0–2 construction, recomputed and checked to equal the v1 f-counts (2, 1, 0) and (55, 4, 0);
  - at n = 6, **declared input:** the triangulation sum (14 terms; PL1).

**Stages S0–S2 at n = 6 are NOT computed.** The ansatz has 5005 monomials. The n = 6 count uses f_s := 0 as a declared assumption (CONJECTURE). Support (CITED, 2312.16282 §8, line "imposing the zeros … does fully fix the amplitude … n = 5, 6, 7") is for a different ansatz (numerator linear in each X).

**S3 zeros = causal diamonds (2312.16282 §3.2, CITED).**
- For each chord X_B = (a, b): D(a,b) = {c_ij : i ∈ [a … b−2], j ∈ [b … a−2] cyclic}, with top X_T = X_{b−1,a−1}.
- This gives n(n−3)/2 diamonds: at n = 6, 6 skinny of size 3 and 3 squares of size 4.
- **Correction to CASCADE-1:** v1 used only the skinny "Z_i" loci, which are complete at n ≤ 5 but miss the 3 squares at n = 6.
- Condition: A_X(θ) vanishes identically on {physical c_ab = 0, ab ∈ D} for every D.

**S3 computation by translation.**
- Write c^X_ab = c^y_ab + o_ab(θ), with o linear in θ.
- For each D, V_D := {v : A_y ≡ 0 on {c^y_D = v}}, computed by a lex Gröbner basis.
- Then Θ_3 = {θ : −o_D(θ) ∈ V_D for all D}, solved by Gröbner/linear algebra in θ.
- This is exact. If V_D = {0} for every D, then Θ_3 is linear.

**S4.** Positivity μ ≥ 0, m ≥ 0, with exact witness/Farkas certificates (v1 `cone_dim`, copied).

**Count.** K_final := dim Θ_4 + f_2, with f_2(n = 6) := 0 assumed. Outcomes MATCH / BELOW / ABOVE vs N_off. Ratio sub-verdict as in CASCADE-1.

**Held-out (never imposed; verdict-bearing only at n = 6 on the EM-n6 final family).**
1. **Factor-count test**, 30 cases: every (D, c⋆) with c⋆ ∈ D, at n = 6.
   - Locus: {physical c_ab = 0, ab ∈ D ∖ c⋆}.
   - Eliminate |D|−1 of the involved X (all choices with an invertible Jacobian).
   - Cancel, factor the numerator and denominator over ℚ, and count connected components of the "variables share an irreducible factor" graph. k = max over choices.
   - PASS iff k equals the massless reference k0 (same function, μ = m = 0, same run) and k0 ≥ 2.
   - Evaluated at N_POINTS = 3 seeded rational points of the final family. Seed 202610231 (`random.Random`); parameters ∈ {a/b : a ∈ 1..40, b ∈ 1..6}.
2. **Eq. 3.7 rank-1 identities** (both lines × 6 rotations = 12) at the same 3 points, as exact identities in the free X.
3. **Symbolic attempt:** eq. 3.7 rotation 0, both lines, on the full symbolic family. Time kill 900 s; a kill gives NOT-EVALUATED, which is not a FAIL.

**The v2 fix (the only change to the split methodology).** The substitution dict tv (final-family values of μ and m) is applied to the locus equations c_ab **and** to the amplitude. Under v1, the amplitude got m → t but the locus kept symbolic m; PL6 replicates that defect and checks it fails 0/10.

## 3. Predictions (written before any n = 6 S3/S4/held-out computation)
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

**Mechanism behind the prediction (CONJECTURE, to be audited).** Because y = X − μ is a translation, the zeros hold exactly when every physical c_ab is preserved. The near-zero factorisation of the massless amplitude then transports exactly to the final family, so the held-out test should pass. If it does, H-split is a consequence of S3, not an independent check of physics. The review must say so.

**Refutation condition.** Python verdict **FAIL** if, with planted ALL OK and reproduction exact, **any** of the following occurs on the EM-n6 final family:
- any factor-count test at any of the 3 points has k ≠ k0;
- any eq. 3.7 point identity fails;
- the symbolic attempt (if completed) fails.

**PASS-UNDERPOWERED** if the held-out passes but the off-family control also passes 30/30.

## 4. Foregone / contamination (declared)
**Smoke test** (from a guard-stubbed copy in /tmp, before locking):
- planted PL1–PL9;
- the full n = 4, 5 cells (stages 0–2, V_D, S3, S4, families) and the n = 5 fixed templates;
- the n = 5 factor-count at 1 point;
- the massless n = 6 reference k0 table.

All n = 4, 5 quantities are public CASCADE-1 results.

**Seen in the smoke test:**
- f = (2, 1, 0) and (55, 4, 0).
- V_D zero-only at n = 4, 5.
- The four n = 4, 5 cells reproduce v1 (relations row-space equal, K equal).
- n = 5 fixed templates 10/10. n = 5 factor-count 10/10 (k0 = k = 2).
- Massless n = 6 k0: 2 for all 18 skinny-diamond cases, 3 for all 12 square cases.

**Edits made after the smoke test:**
- PL1 n = 6 redefined. Literal 6-fold summation of the eq. 3.6 representative 1/(X13X36X46) double-counts an order-3 orbit, so PL1 now checks 14 terms, the representatives and cyclic invariance.
- `components` uses cancel (a spurious common factor had been left by together).
- A `.get` fix in cell.
- The V_D time kill was wired in.

**Never executed before this push:**
- any n = 6 V_D;
- any n = 6 S3/S4 cell (E0 or EM);
- any held-out test on a massive n = 6 family;
- the off-family control.

**Non-blind:**
- E0-n6 Θ_3 is the δ-line *iff* V_D = {0}, because PL9 checks the §7.1 kernel (CITED). The blind content of that cell is V_D.
- The uniform interior point is hand-derived.

## 5. Planted-answer tests (`sims/cascade1b/planted_cases.json`): PL1–PL9 as listed there. Any failure gives ILL-DEFINED and live is not scored.

## 6. Verdict rules (python, in this order)
1. Planted failure, or n = 4, 5 reproduction not exact → **ILL-DEFINED**.
2. EM-n6 Θ_3 nonlinear or empty → **NOT-POSED**.
3. V_D time kill (3600 s per diamond) → **NOT-EVALUATED**.
4. Held-out violated → **FAIL**.
5. Held-out passes and the control passes everywhere → **PASS-UNDERPOWERED**.
6. Otherwise → **PASS**.

Separately reported:
- H re-test (CONFIRMED only if all 6 cells MATCH);
- per-cell RATIO sub-verdict.

Whatever the result, the CASCADE-1 FAIL is not re-labelled.

## 7. Lean (new module `lean/PositiveGeometryEmergentSpaceTime/Cascade1b.lean`, namespace `PositiveGeometryEmergentSpaceTime.Cascade1b`, over ℚ; 0 sorry; no native_decide; standard axioms; AxiomsAll regenerated)
1. `e0_n6_offsets_zero_iff`: all 9 E0 offsets vanish ↔ μ = δ·(δ-vector); with positivity, μ = 0.
2. `em_n6_offsets_zero_iff`: all 9 EM offsets vanish ↔ the live relations (generated from the run output).
3. `zeros6_of_rel`: on the relations, A6(X − μ) = 0 on a skinny and a square diamond locus (field identity).
4. `split37_of_rel`: on the relations, eq. 3.7 lines 1 and 2 hold for the massive family (field identity).
5. `uniform_interior`: the uniform point satisfies the relations.

Re-wordings needed to compile are declared in the result.

## 8. Simulation plan
- Run id `CASCADE1b-2026-10-23-r1`, seed `202610231`. Modes: `planted`, then `live` (only if planted is ALL OK).
- Outputs: `sims/cascade1b/{cascade1b_planted.txt, cascade1b_output.txt, cascade1b_live.json}`.
- Figure (post-run, reads JSON only).

## 9. Data tiers. Tier 0 mathematics only (2312.16282 CITED; repo Cascade1/MassShift PROVED). No experimental data.

## 10. Pinned environment
- Python 3.13.5 `<local path>`, sympy 1.14.0, scipy 1.18.1.
- Lean v4.34.1, Mathlib d13f23b7.
- 8 CPU, no GPU.

## 11. Guard and run manifest
- Guard copied from v1 (fetch once per process; the prereg add-commit must be an ancestor of origin/main; checker sha256).
- `guard` is called in every scoring function. There is no pass flag.
- The import test must REFUSE before the push. Its output goes to `sims/cascade1b/guard_refusal.txt` (own commit).
- Result manifest:
  - sims outputs;
  - Lean module, axioms file and output;
  - `figures/cascade1b-2026-10-23.png`;
  - `reviews/CASCADE-1b-result-2026-10-23.md`;
  - ledger/glossary/graph/blueprint/BACKLOG/blocker/AXIOMS updates.

## 12. What remains untested (by design)
- n ≥ 7; S0–S2 at n = 6 (f := 0 assumed); other ansätze/degree caps.
- Massive deformations that do not preserve the physical c (CASCADE-2 covers the δ-type tachyonic one).
- The held-out family is a consequence of S3 under translation (§3 mechanism). This rung therefore tests the code path and the v2 fix, not new physics. An independent held-out target (e.g. loop-level, or non-translation mass insertions) remains open.
- Whether the CASCADE-1 FAIL should be voided on audit (the author's decision; not taken here).

Locked:
- `sims/cascade1b/cascade1b_checker.py` sha256 `977d66f16e9eec08538569840429f1144080f5bfc4346d1dc025cc1b0ab78167`
- `sims/cascade1b/planted_cases.json` sha256 `8cc6030787a179ffef7cb7b93427cb74162989f4a13f84ddd1bc238b2fe699ad`
- `sims/cascade1b/import_guard_test.py` sha256 `1230ff6d0eaca86c6633522e00026f2fef5fd02400a54ea05cd6bbedb7165954`
