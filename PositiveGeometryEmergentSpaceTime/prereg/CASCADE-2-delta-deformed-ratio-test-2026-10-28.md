# PREREG CASCADE-2: does a δ-deformed (Λ-mass) stage of the mass-shifted Tr φ³ cascade fix a mass ratio?
Written 2026-10-28 by Grok. The author-approved rung: "Ok go cascade1b and cascade 2" (2026-10-23) and "Ok go" (2026-10-27), relayed. Not AutoResearch.
Pushed ALONE, ff-only, with the locked checker, planted spec and import test, BEFORE any CASCADE-2 live computation. Order change vs the 2026-10-28 draft (declared before locking): the draft said "after the CASCADE-1b r2 result"; at the r2 live run (pid 529310, started) was still in its un-killed held-out eq. 3.7 point tests (~35 min per test, 36 tests), so this prereg is pushed while r2 runs. Nothing in CASCADE-2 uses an r2 held-out, symbolic, control or verdict output; the r2 outputs seen before locking are only its stages 0–2, V_D (zero-only at n = 4, 5, 6), cell table and k0 reference (sims/cascade1b/cascade1b_r2_output.txt, lines before "held-out point"). No physical datum (no measured mass, coupling or ratio) enters. Zero fitted parameters.

## 0. Context and what stays on record
- CASCADE-1 (9ed0afd) locked FAIL and CASCADE-1b r1 (3a57a17) NOT-EVALUATED stay on record. The CASCADE-1b r2 result (run `CASCADE1b-2026-10-24-r2`) is still running when this file is pushed (see header); it is graded only by its own locked prereg 9b1dca2 and is not re-labelled here.
- BACKLOG item: "CASCADE-2: the cascade with δ-deformed or string zeros (2312.16282 §7), the only remaining non-linear P4 stage. Prior of a ratio fix ≈ 0.05 (CONJECTURE)."
- CITED (arXiv 2312.16282, Arkani-Hamed–Cao–Dong–Figueiredo–He, HTML fetched 2026-10-27/28): §7 eq. (7.1)–(7.2) the δ-deformation shifts X_ee → X_ee + δ, X_oo → X_oo − δ (field-theory form used in eq. 7.16: X13 − δ, X24 + δ); §7.1 this is the unique c-preserving shift (n even); eq. (7.17) n = 4: A → (1/δ)(1 − 1) − (1/δ²)(X13 + X24) + O(δ⁻³); eq. (7.19)–(7.20) n = 6: the shifted amplitude starts at −δ⁻⁴ × (NLSM bracket).

## 1. Definitions (fixed before the run)
- Kinematics, chords, diamonds, offsets o_ab(θ), V_D, Θ_3, S4 cone and final family: exactly as CASCADE-1b (prereg 27a47fd §2; V_D by the numerator method of checker v3, prereg 9b1dca2). Settings E0 (massless legs, θ = μ_P) and EM (θ = μ_P and leg masses m_i), n = 4, 5, 6.
- **Deformation (Λ-masses).** Propagators y_P = X_P − μ_P − Λ κ_P with Λ → ∞ and κ ∈ ℚ^{chords} a free direction. κ_P is the "Λ-mass" of chord P (internal mass² = μ_P + Λ κ_P). The 2312.16282 δ-shift is the special direction κ_oo = +1, κ_ee = −1, κ_oe = 0 with Λ = δ.
- **Stages, in this order** (checker `cell2`):
  - **S3′ (zeros for all Λ):** A(X − μ − Λκ) vanishes on every causal-diamond zero locus, identically in Λ. Conditions = coefficients in Λ of the V_D Gröbner generators at v = −(o(θ) + Λ o_E0(κ)). Linear in (θ, κ).
  - **S5 (NLSM limit):** on the S3′ κ-family, A = O(Λ^{−(n−2)}) with a non-vanishing Λ^{−(n−2)} coefficient (generic point), κ ≠ 0 on its support. Conditions = coefficients in x of the ε^j series terms, j < n − 2 (ε = 1/Λ, x_P = X_P − μ_P).
  - **S4 (positivity):** S4 cone of the θ-block as CASCADE-1b. Secondary: **strict positivity** = every internal M² = μ_P + Λκ_P ≥ 0 for large Λ, i.e. κ ≥ 0 on all chords (dimension of the κ cone reported).
- **"Fixes a mass ratio" (RATIO-FIXED).** For two of the mass parameters q_a, q_b ∈ {m_i, μ_P, κ_P} that are not identically zero on the final family, the ratio q_a/q_b is constant on the final family (linear family: rank-1 test, `linear_ratios`; S5-alone polynomial variety: finite value set, `ratio_analysis`).
- **PHYS ratio.** A RATIO-FIXED pair with ratio r > 0, r ≠ 1, not already fixed on the CASCADE-1b-type θ-family (`new_vs_1b`), and with both q_a, q_b > 0 attainable on the family (`both_nontachyonic_possible`). Only a PHYS ratio would count as the geometry fixing a physical mass ratio.
- **Observed statistic (anti-numerology).** S5-alone on the ee/oo support (κ free and nonzero on chords with a ≡ b mod 2, zero elsewhere) for the physical amplitude (all triangulation coefficients 1), n = 4 and n = 6. h(r) = max(|p|, |q|) for r = p/q in lowest terms; h_cell(n) = min height over the fixed ratios found; h_obs = min(h_cell(4), h_cell(6)) (None if no fixed ratio).
- **Null.** N_NULL = 300 draws, seed 202610232, each draw replaces the triangulation coefficients by independent uniform integers in [1, COEFF_MAX = 9] (n = 4 and n = 6), and recomputes the same statistic. p = (1 + #{null draws with h ≤ h_obs})/(N + 1).
- **Look-elsewhere.** Primary: the **global max-statistic** p_global, using per draw the min height over both cells and all pairs (so the search over cells and pairs is inside the null). Reported, not verdict-bearing: per-cell p and a Bonferroni bound L × min p_cell with L = number of ratio pairs examined.
- **Significance.** p_global < 0.01.
- Design constants (N_NULL, COEFF_MAX, seeds, kills) are fixed here and are not tuned after the run.

## 2. Predictions (probabilities are CONJECTURE)
| item | prediction | prob |
|---|---|---|
| planted PL1–PL11 | ALL OK (seen in a guard-stubbed smoke, §4) | 0.97 |
| V_D zero-only at n = 4, 5, 6 | yes (n = 6 already seen zero-only, 9/9, in the CASCADE-1b r2 live run; not blind) | 0.9 |
| E0-n4, EM-n4 | DEFORMATION-EXISTS, κ-family = δ-line κ13 = −κ24, only fixed κ ratio −1, no PHYS (seen in smoke, §4) | 0.97 |
| E0-n5, EM-n5 | NO-DEFORMATION (no c-preserving shift at odd n, §7.1; κ = 0 forced) | 0.9 |
| E0-n6 | DEFORMATION-EXISTS, κ-family = δ-line (dim 1), S5 holds (eq. 7.20), fixed κ ratios ∈ {+1, −1}, no PHYS | 0.85 |
| EM-n6 | same κ-family and ratios as E0-n6; θ-block ratios as CASCADE-1b; no PHYS | 0.8 |
| strict-positivity κ cone dim | 0 wherever a deformation exists (a tachyonic Λ-mass is forced) | 0.95 |
| S5-alone ee/oo n = 4 | ratio −1 (eq. 7.17) | 0.97 |
| S5-alone ee/oo n = 6 | the δ-line is the only nonzero component; ratios ∈ {+1, −1} | 0.75 |
| h_obs | 1 | 0.9 |
| null at n = 6 | generic draws EMPTY (smoke 3/3, not the locked seed) | 0.85 |
| p_global | ≈ 0.1 (n = 4 null has h = 1 with prob 1/9); NOT < 0.01 | 0.9 |
| p_cell(n6) | 1/301 if the n = 6 null is always EMPTY; below 0.01 but a reproduction of the CITED δ-line, not a new ratio | 0.75 |
| support enumeration n = 6 (511 supports) | COMPLETE within 3600 s; every support with a solution has fixed ratios only in {+1, −1} or FREE | 0.7 |
| **H2** | **REFUTED (no PHYS ratio)** | 0.93 |

## 3. Verdict rules (python, in this order; applied to run `CASCADE2-2026-10-28-r1`)
1. Planted failure, or a known-result reproduction fails (PL1 = eq. 7.17, PL2 = eq. 7.20, PL3 = §7.1, PL9 = CASCADE-1b V_D at n = 4, 5) → **ILL-DEFINED**.
2. V_D time kill (3600 s per diamond) → **NOT-EVALUATED**; a per-cell kill (3600 s) marks that cell NOT-EVALUATED; a crash or the V_D-not-zero-only assertion → **NOT-POSED** (reported, not re-run).
3. A PHYS ratio exists and p_global < 0.01 → **H2 CONFIRMED**.
4. A PHYS ratio exists and p_global ≥ 0.01 → **H2 REFUTED (fails anti-numerology)**.
5. Otherwise → **H2 REFUTED (no PHYS ratio)**.
Separately reported: RATIO-FIXED(any κ ratio), per-cell outcomes, p_global, p_cell, Bonferroni bound, support enumeration. A non-PHYS fixed ratio (e.g. κ13/κ24 = −1) is not a mass-ratio prediction.

## 4. Smoke / foregone (declared)
- Draft checker, planted spec, import test and a Lean draft were written 2026-10-23/24 before this prereg (never pushed; no prereg existed, so no guarded run was possible).
- Guard-stubbed scratch copies in /tmp (not scored, not the locked seed):
  - planted PL1–PL9 ALL OK; after adding PL10–PL11, PL1–PL11 ALL OK (PL10 n = 6 EMPTY 0.1 s; PL11 V_D 1.0 s, E0 and EM NOT-POSED in 0.1 s);
  - 3 random-coefficient null draws (seed 12345): n = 4 OK with heights 7, 3, 9; n = 6 EMPTY, 0.1 s each;
  - `cell2` at n = 4 E0 and EM on the physical amplitude (code-path check): both DEFORMATION-EXISTS, κ-family κ13 = −d0, κ24 = d0, only fixed ratio κ13/κ24 = −1, PHYS false. **The n = 4 cells are therefore not blind.**
- The 2026-10-23 Lean draft generator (`sims/cascade2/gen_lean.py`) computed the n = 6 S5 condition polynomials on the ee/oo support of the physical amplitude and checked that the CITED δ-line satisfies them. Their variety (uniqueness of the δ-line) was **not** computed. The generated draft module compiled (lake build, 2026-10-24) and is kept at /tmp/c2draft; the module pushed after the run is regenerated by the same script. No n = 5 or n = 6 cell, no S5-alone ratio analysis of the physical amplitude at n = 6, no locked-seed null and no support enumeration has been run.
- Planted coverage gap (declared): PL11 runs V_D + `cell2` at n = 6 on a random-coefficient sum, where S3′ is empty, so the S5/S4 branches of `cell2` at n = 6 are exercised only by the live run (protected by the 3600 s cell kill).

## 5. Lean (module `lean/PositiveGeometryEmergentSpaceTime/Cascade2.lean`, namespace `PositiveGeometryEmergentSpaceTime.Cascade2`, over ℚ; 0 sorry; no native_decide; standard axioms; AxiomsAll regenerated)
Generated by `sims/cascade2/gen_lean.py`, run-independent (from CITED formulas): `n4_delta_identity`, `n4_delta_remainder` (eq. 7.16/7.17), `n4_leading_iff` (Λ⁻¹ coefficient vanishes ⇔ κ24 = −κ13), `n4_tachyon_forced`, `n6_cond_k_delta_line` (each n = 6 ee/oo S5 condition vanishes on the δ-line), `n6_tachyon_forced`, `n6_eq720_leading` (the Λ⁻⁴ coefficient = −(eq. 7.20 bracket)). Uniqueness of the δ-line at n = 6 stays SIMULATED unless a certificate compiles. Re-wordings needed to compile are declared in the result.

## 6. Guard and manifest
- Guard as CASCADE-1b v3: fetch once per process; the add-commit of THIS prereg must be an ancestor of origin/main; checker sha256 below; `guard` in every scoring function; no pass flag.
- Import test must REFUSE after the local prereg commit and before the push; output `sims/cascade2/guard_refusal.txt`, committed alone after the prereg push.
- Outputs: `sims/cascade2/cascade2_planted.txt`, `cascade2_output.txt`, `cascade2_live.json`, `runs/CASCADE2-2026-10-28-r1/` (vd.jsonl, cells.jsonl, null.jsonl, progress.log); Lean module; AxiomsAll; figure `figures/cascade2-2026-10-28.png`; `reviews/CASCADE-2-result-2026-10-28.md`; BACKLOG / blocker / AXIOMS rows.

## 7. What remains untested (by design)
- Finite α′ (string-level) zeros; the YMS point α′δ = 1; Λ-dependence beyond linear (κ fixed direction).
- n ≥ 7 (odd n has no c-preserving shift); n = 8; loop level.
- Mass insertions that are not translations of X; S0–S2 at n = 6 (f := 0 assumed, as CASCADE-1b).
- The null family (uniform coefficients in [1, 9]) is one choice; other coefficient laws are untested.
- Any link to a measured SM mass ratio: none is attempted; a PHYS ratio would only be a CONJECTURE input to a later rung.

Locked:
- `sims/cascade2/cascade2_checker.py` sha256 `3651ea0ba997e3699bf33ea4cc98c653dfbf4671f04342574f2fcdf28a9c9f31`
- `sims/cascade2/planted_cases.json` sha256 `6957822ab04e5e168ac03929c9e49dfe7627f83695f90b7b0109efcf770e7258`
- `sims/cascade2/import_guard_test.py` sha256 `3c9180b4ae24032ba75100264b0cf14c31aa757b4ea12ab3cccfc60ea075fc18`
