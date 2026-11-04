# PREREG CASCADE-1: does any constraint stage fix a mass ratio in mass-shifted Tr φ³ at n = 4, 5?
Written 2026-10-23 by Grok. This is a **The author-directed manual frontier rung**, not AutoResearch (AutoResearch is paused and is not touched). The author said "Ok go" at on 2026-10-23, relayed by the parent: run LEAN-CERT-1 (done, 515084c), then CASCADE-1, and not NL9c.
Source spec: `notes/LIT-REVIEW-2026-10-22-cosmic-nine-loops-ai-physics.md` §6 CASCADE-1 (commit 5017263).
Pushed ALONE, ff-only, with the locked checker, planted spec and import test, before any live computation. No physical datum enters.

## 1. Hypothesis and target
**H (headline, from the lit review).** For a fixed, pre-declared ansatz of mass-shifted Tr φ³ amplitudes at n = 4 and 5, apply the constraint stages in the fixed order (§2). The final free-parameter count K_final equals the number of independent mass offsets N_off. In other words, no stage removes a mass ratio (INT-1 `ratio_free` expectation).

**Target.** The cascade table K_s = dim Θ_s + f_s for s = S0…S4, in four cells:
- settings {E0, EM};
- n ∈ {4, 5}.

## 2. Exact definitions
**Kinematics** (arXiv 2312.16282, Arkani-Hamed–Cao–Dong–Figueiredo–He; CITED, fetched 2026-10-23 at arxiv.org/abs/2312.16282, HTML full text through §7.1):
- Planar variables X_{i,j} = (p_i + … + p_{j−1})².
- Chords: (a, b), 1 ≤ a < b ≤ n, b − a ≥ 2, (a, b) ≠ (1, n). There are N_off := n(n−3)/2 of them (2 and 5).
- Boundary: X_{i,i+1} = p_i² = m_i and X_{1,n} = m_n, where m_i denotes the external mass squared.
- c_{i,j} = X_{i,j} + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j} (eq. 2.4), with cyclic labels. The physical c_{i,j} = −2 p_i·p_j, including the boundary masses.

**Parameters Θ.**
- Chord mass offsets μ_ab; propagators are y_ab := X_ab − μ_ab.
- Setting **E0:** m_i = 0 (massless external legs), Θ = μ, so dim Θ_0 = N_off.
- Setting **EM:** Θ = (μ, m_1…m_n), so dim Θ_0 = N_off + n.
- Both settings are pre-declared and both are reported. N_off counts chord offsets in both settings, matching the INT-1 `mass_shift` m : Fin 5 → ℝ at n = 5.

**Ansatz (fixed now; kill (c) guard).**
- A = N(y) / Π_chords y_ch, where N is an arbitrary polynomial of total degree ≤ D_n := (n−3)(n−2)/2.
- So D_4 = 1 (3 coefficients) and D_5 = 3 (56 coefficients).
- The cap is fixed by mass dimension: A_n ∼ [mass]^{−2(n−3)} with no contact terms of non-negative dimension.
- Polynomials of degree ≤ D in y and in X are the same space.

**Count.**
- f_s is the projective dimension (dimension − 1) of the amplitude family that solves stages ≤ s at a generic point of Θ_s. The unknowns are the coefficients a, plus κ from S2 on.
- Θ_s is the set of admissible parameters, with its real dimension. K_s = dim Θ_s + f_s.

**Stages, in this order:**
- **S0 ansatz.** No constraint.
- **S1 poles/adjacency.** There is no simultaneous pole on crossing chords: for every crossing pair (P, Q), N|_{y_P = y_Q = 0} ≡ 0. Simple poles only at y_ch = 0 hold by construction.
- **S2 factorisation.** For every chord P, Res_{y_P=0} A = κ · A_L · A_R, with one κ common to all channels.
  - A_3 = 1.
  - A_4 on a sub-quadrilateral is the n = 4 cascade's own S2 output, mapped onto the sub-polygon's chords with offsets inherited. (n = 5 uses n = 4; it is not typed in.)
- **S3 hidden zeros** (2312.16282 §3.1.1, CITED).
  - For each i, Z_i = {physical c_{i,j} = 0 for every j non-adjacent to i}. After deduplication there are n(n−3)/2 loci: 2 at n = 4 ({c13 = 0}, {c24 = 0}) and 5 skinny rectangles at n = 5.
  - Condition: A(X − μ) vanishes identically on every Z_i, i.e. all numerator coefficients vanish as a polynomial in the free X on the locus. This gives polynomial conditions on Θ.
  - Θ_3 is their real variety, computed via a reduced Gröbner basis over ℚ. If it is linear, the dimension is that of the solution space. If it is nonlinear, the dimension is the maximum over components (and S4 is skipped, §6).
- **S4 positivity.** κ > 0 (an open condition), and a non-tachyonic spectrum: all μ_ab ≥ 0 and (in EM) all m_i ≥ 0.
  - Θ_4 = Θ_3 ∩ cone, and dim Θ_4 is the dimension of that polyhedral cone.
  - Every coordinate gets an exact certificate. Either a rational witness shows it can be > 0, or an exact Farkas vector λ ≥ 0 with λ_j > 0 and λᵀB = 0 shows it is forced to 0. scipy LP only proposes candidates.
- **Declared deviation from the lit-review wording.** "Lovelace–Shapiro" is **NOT-POSED** for this ansatz: a finite-pole field-theory amplitude has no Regge/LS tower. S4 is positivity only. The lit-review stage "hidden zeros/splits" is split in two: zeros are imposed, and splits are the held-out family (§5).

**Held-out family (never imposed): near-zero splits** (2312.16282 eqs. 3.3, 3.5 and cyclic images; CITED).
- On {c14 = 0}, A = F(X13, X25) · G(X14, X35), with X24 eliminated.
- On {c13 = 0}, A = F(X13, X25) · G(X24, X35), with X14 eliminated.
- Both are rotated by k = 0…4, giving 10 tests at n = 5.
- Each is tested mass-agnostically on the S4 final family, parametrised symbolically, as the exact rank-1 identity A(x,y)A(x′,y′) = A(x,y′)A(x′,y) for the two variable groups.
- At n = 4 the held-out family is VACUOUS: each zero locus carries a single c, so no proper split exists. This is declared now.

## 3. Predictions (written before the live run; see §4 for what was seen)
Shared stages (Θ-independent: S0–S2 involve only y, so they do not depend on Θ — a change of variables):
- n = 4: f0 = 2, f1 = 1, f2 = 0 (seen in the smoke test, §4).
- n = 5: f0 = 55, f1 = 4, f2 = 0 (seen in the smoke test, §4).
- The S2 amplitude equals the triangulation sum Σ Π 1/y (eq. 3.1 at Θ = 0) at both n (seen, §4).

| cell | S3 dim Θ | S4 dim Θ | K_final | vs N_off | prob |
|---|---|---|---|---|---|
| E0 n=4 | 1 (δ-line μ13 = −μ24, the 2312.16282 §7.1 shift) | 0 | 0 | BELOW | 95% (hand-analysed, non-blind) |
| EM n=4 | 4 (μ13+μ24 = m2+m4 = m1+m3) | 4 | 4 | ABOVE | 90% (hand-analysed, non-blind) |
| E0 n=5 | 0 | 0 | 0 | BELOW | 70% (alt: dim 1, 20%) |
| EM n=5 | 5 (all five c_{ij}(μ, m) = 0, i.e. zeros ⇔ every physical c is preserved) | 5 (uniform mass M is interior) | 5 | MATCH | 60% (alt: dim > 5, 25%; dim < 5, 15%) |

- Held-out splits pass on the final family in E0-5 and EM-5: 90%.
- **Mission sub-prediction (ratio):** in EM, dim Θ_final ≥ 2 at both n, so mass ratios stay free (RATIOS-FREE): 95%. A dim Θ_final = 1 in EM (RATIO-FIXED) would be the positive surprise.
- **Headline H** is expected to be REFUTED-AS-STATED (70%). The cells will not all MATCH, because the hidden-zero locus carries external-mass data (E0 forces massless internal lines; EM keeps more than N_off). The pre-written audit (§6) attributes BELOW in E0 to hand-inserted input (massless external legs inside the zero definition), not to a geometric ratio fix.
- Lean: the n = 4 iff, the E0 collapse, the n = 5 "if" direction, the held-out split identities and the Θ_3 dimension certificates compile with 0 sorry and standard axioms: 80%. The n = 5 "only if" direction in Lean: 35% (otherwise it stays SIMULATED, exact symbolic).

## 4. Foregone / contamination (declared)
- **Not blind at n = 4.** Before this prereg, I hand-derived that on {c13 = 0} the n = 4 amplitude 1/(X13−μ13) + 1/(X24−μ24) vanishes iff μ13 + μ24 = m2 + m4 (and cyclically m1 + m3). This is consistent with the repo's `MassShift.hidden_zero4_forces`.
- **Smoke test, declared.** Before locking, `run_planted` (PL1–PL8 all OK), the n = 4 E0/EM cascades and `run_stages012(5, 3)` were executed once in /tmp from a guard-stubbed copy, to catch crashes.
  - Seen at n = 4: E0 K = (4, 3, 2, 1, 0), relations [μ13 + μ24]; EM K = (8, 7, 6, 4, 4), relations [μ13 + μ24 − m2 − m4, m1 − m2 + m3 − m4].
  - Seen at n = 5: f0 = 55, f1 = 4, f2 = 0, A = triangulation sum.
  - After the smoke test, one edit was made: the nonlinear-Θ_3 branch now computes K_final (§6). No n = 5 S3/S4/held-out function was executed.
- **Blind:** the four n = 5 S3/S4 numbers, the n = 5 relations and the held-out split outcomes.

## 5. Planted-answer tests (`sims/cascade1/planted_cases.json`)
- PL1: the triangulation sum equals eq. (3.1).
- PL2: the massless splits 3.3/3.5 hold (10/10), and a planted non-separable function is REJECTED.
- PL3: A5 vanishes on all 5 Z_i, and the planted A5 + 1/(X13X14) is detected.
- PL4: a planted ratio-fixing stage μ13 = 2μ24 lowers dim Θ (detector power for kill (a)).
- PL5: S1 excludes the crossing double pole.
- PL6: cone_dim certificates on toy cones of dimension 0, 1, 2.
- PL7: the 2312.16282 §7.1 δ-shift keeps the n = 4 zero (known-result reproduction).
- PL8: a nonlinear Θ is detected.

**Known-result reproduction (live).** At Θ = 0, the S2 output is the unique massless Tr φ³ amplitude, equal to eq. (3.1) at n = 5. The E0 n = 4 Θ_3 equals the §7.1 δ-line.

## 6. Pass / fail / kill criteria and verdicts
- **ILL-DEFINED:** any planted case fails. Then live is not scored.
- **NOT-POSED (kill c):**
  - the S2 family at D_n does not reproduce massless Tr φ³; or
  - the verdict would need a degree cap other than D_n.

  The D_n + 1 run (`sens` mode, pre-declared) is secondary and never verdict-bearing.
- **FAIL (kill b):** any held-out split is violated on a final family where it is evaluated.
- **Per-cell outcome:** MATCH (K_final = N_off), BELOW, or ABOVE. If Θ_3 is nonlinear, K_final := dim Θ_3 (S4 not evaluated, flagged).
- **Kill (a), BELOW = surprise.** Pre-written audit, done in the review:
  - which stage drops K;
  - whether the drop comes from data inserted by hand (the zero-locus definition with fixed external masses, the positivity sign convention), or from a geometric relation that fixes a **ratio** among free masses.

  Only the latter counts as a positive surprise ("a stage fixes a ratio").
- **Overall:** CONFIRMED if all four cells MATCH and the held-out passes. Otherwise REFUTED-AS-STATED (with the per-cell table and audit). RATIO sub-verdict per cell: RATIOS-FREE (dim Θ_final ≥ 2), RATIO-FIXED (= 1), NO-MASSES-SURVIVE (= 0, all masses zero).

## 7. Lean (new module `lean/PositiveGeometryEmergentSpaceTime/Cascade1.lean`, namespace `PositiveGeometryEmergentSpaceTime.Cascade1`, over ℚ; 0 sorry; no native_decide; standard axioms; AxiomsAll regenerated)
1. `zero4_iff`: (∀ x off the poles, 1/(x−a) + 1/((s−x)−b) = 0) ↔ a + b = s. This is the n = 4 S3 statement on the line X13 + X24 = s.
2. `e0_n4_collapse`: a + b = 0, a ≥ 0, b ≥ 0 → a = b = 0 (E0 n = 4 S4).
3. `em_n4_zero_iff`: both n = 4 zeros ↔ the two EM relations. `em_n4_finrank`: the relation space has dim 4 (LeanCert `finrank_ker` certificate).
4. n = 5, for the live relations R:
   - `zero5_of_rel`: R ⇒ A5(X − μ) = 0 on each Z_i (field identity);
   - `split5_of_rel`: the held-out split identities hold on R;
   - `em_n5_finrank` (and E0) via certificate.

   If R is not linear, (4) becomes the component statements, declared in the result.
5. Attempted: `zero5_only_if` (zeros ⇒ R). If not achieved, it stays SIMULATED (exact symbolic), declared.

Re-wordings needed to compile are declared in the result, never hidden.

## 8. Simulation plan
Run id `CASCADE1-2026-10-23-r1`, seed `20261023` (sens: seed + 1). Modes, in order:
1. `planted`;
2. `live`, only if planted is ALL OK;
3. `sens`, after live.

Outputs:
- `sims/cascade1/{cascade1_planted.txt, cascade1_output.txt, cascade1_live.json, cascade1_sens.json}`.
- Figure (post-run, reads JSON only): K_s against stage for the four cells, with N_off marked.
- Negative results are kept.

## 9. Data tiers
- Tier 0 (mathematics): 2312.16282 (CITED, fetched); repo MassShift/SplitZeroGate/IntChamber (PROVED).
- No experimental data. No data-credit moves.

## 10. Pinned environment
- Python 3.13.5 (`<local path>`), sympy 1.14.0, scipy 1.18.1.
- Lean `leanprover/lean4:v4.34.1`, Mathlib rev `d13f23b723b8a846827a245b89c10fc7d3f11612`.
- Box: 8 CPU, 15 GB, no GPU. CPU only.
- Figure: `<local path>`.

## 11. Guard and run manifest
- Hardened guard, copied from `sims/leancert1`. git fetch once per process. The prereg add-commit must be an ancestor of origin/main. The checker sha256 must match the line below.
- `guard` is called in every scoring function (`lin_solve_rows`, `poly_coeff_eqs`, `run_stages012`, `zero_conditions`, `variety`, `cone_dim`, `split_test`, `all_splits`, `cascade`, `run_planted`, `run_live`, `run_sens`). There is no pass flag.
- The import test must REFUSE before the push; its output goes to `sims/cascade1/guard_refusal.txt` (own commit).
- Result manifest:
  - sims outputs (§8);
  - `lean/PositiveGeometryEmergentSpaceTime/Cascade1.lean`, `lean/axioms/Cascade1_axioms.lean`, its output, `lean/AxiomsAll_output.txt`;
  - `figures/cascade1-2026-10-23.png`, `reviews/CASCADE-1-result-2026-10-23.md`;
  - ledger/glossary/graph/blueprint/BACKLOG/blocker/AXIOMS updates;
  - `notes/TRADE-SPACE-2026-10-23.md`.

## 12. What remains untested (by design)
- n ≥ 6, loop level, and non-planar or colour-dressed theories.
- Ansätze with numerator poles, or other degree caps (only the secondary D_n + 1).
- Massive generalisations of the zeros other than "physical c_{ij} = 0", e.g. the 2312.16282 §7 δ-deformed string version.
- Lovelace–Shapiro / Regge constraints (NOT-POSED here).
- NLSM / Yang–Mills mass shifts (repo MassShift covers NLSM n = 4 only).
- Whether "mass offset" should mean a chord offset or a physical pole mass in a theory with external masses. Both readings appear in the two settings; neither is privileged.

Locked:
- `sims/cascade1/cascade1_checker.py` sha256 `c4cdab6a4e1919e224827cea3c6653ba1cc3233e2d692b587196a715f5caaf16`
- `sims/cascade1/planted_cases.json` sha256 `64fc2ecd1b05a140e92a0eff04875377de13197057b1092416006634af551517`
- `sims/cascade1/import_guard_test.py` sha256 `6501a29e1eb1933a1622ff68abedfee1a2f527bdfa83af21765e14c9500d7507`
