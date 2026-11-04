# PREREG GRADED-POSITROID: does a Cartan-weight-graded positroid moment give a charge condition beyond the anomaly polynomial, and is it earned?
Written 2026-10-22 by Grok. **continuous-mode own pick (author approved 2026-10-22).** STOP absent on origin/main at rung start (checked, origin a6bd44c).
Frontier rank: #2 in REVIEW-2026-10-20 / TRADE-SPACE-2026-10-22 after the approval-gated #1 (P = 0.10, value 0.9, P×V = 0.09; 0.3× = 0.027; next TRIALITY-WHY 0.05/0.015).
Overlap check vs PositiveGeometryEmergentSpaceTime's INT-1 / FL-1Z: INT-1 (origin 32cec63, a6bd44c) = chamber constancy of associahedron integer invariants with mass offsets, paths `sims/int1/`, `IntChamber`; FL-1Z paths `sims/fl1z`, `FL1Z`. This rung touches only `sims/gpos/`, `lean/PositiveGeometryEmergentSpaceTime/GradedPositroid.lean`, charge gradings of Gr⁺(k,15) columns: no shared files, objects or questions. `<local path>` and all other worktrees untouched (own worktree `<local path>`).
Pushed ALONE (with locked checker, planted spec, import test) before any checker computation. No physical datum is used for the verdict.

## 0. Re-read
- BRIDGE-PL-ASSOC (reviews/BRIDGE-PL-ASSOC-result-2026-10-20.md, Lean `PositiveGeometryEmergentSpaceTime.BridgePLCharge`): NO-LINK. M1 u-variables charge-blind; M2 (Y-only Δ(2,15) moment) gives Tr Y = Tr Y³ = 0, reproduced by the simplex rival and non-discriminating (35 vs 2 solutions).
- REVIEW-2026-10-20 suggestion: grade the columns by the full Cartan weight (H3, H8′, T3, Y) instead of Y only, so SU(3)²U(1) and SU(2)²U(1) could appear. Review kill rule: if this also reproduces only the anomaly polynomial, the steelman (positroid geometry adds nothing to charge selection) becomes the working position (a reading only; MISSION is not edited, that is approval-gated).

## 1. Trials (look-elsewhere)
- **G1** cells Δ(1,15), Δ(2,15), Δ(3,15) + rival cube [0,1]¹⁵: count hypercharge vectors (yQ = 1; yu, yd, yL, ye ∈ {p/q : |p|,|q| ≤ 10}, the STRUCT-1/BRIDGE basis, scaled by S = 2520) with all graded m1 = 0 and all graded m3 = 0. On m1 = 0, m3(z) = κ · Σᵢ (z·wᵢ)³ (Lean `polarized_cubic_reduction`, `triple_sum_general`), so the graded conditions are the Cartan-restricted cubic tensor Σᵢ wᵢᵃwᵢᵇwᵢᶜ = 0 for all a ≤ b ≤ c (20 components) when κ ≠ 0, and m1 only when κ = 0.
- **G3** proper nonempty unions of whole multiplets (Weyl-invariant faces of Δ(1,15)): any with vanishing graded m1 and cubic tensor for SM charges?
- **G4** m4, m5 of Δ(2,15) along Y for the SM: does m5 vanish (that would be a non-ACC condition the SM satisfies)?
Total 3 + 1 + 2 = 6 evaluated trials (4 G1 cells, 1 G3 scan, 1 G4 pair).

## 2. Contents and rival
Weights: colour (H3, H8′) ∈ {(1,1), (−1,1), (0,−2)}, antitriplets negated; T3 = ±1/2; Y: Q 1/6, uᶜ −2/3, dᶜ 1/3, L −1/2, eᶜ 1 (left-handed Weyl convention). Rivals: the simplex Δ(1,15) (Dirichlet) and the cube [0,1]¹⁵ (κ = 0, CITED in BRIDGE). Hypothesis cell Δ(2,15) as in BRIDGE.

## 3. Rule (fixed; in checker docstring)
WELL-POSED iff all planted OK (else ILL-DEFINED). G1 REPRODUCES iff N(Δ(2,15)) = N_ACC; EARNED iff REPRODUCES and the simplex rival N ≠ N_ACC. NEW-CONDITION iff G3 has a proper union satisfied by the SM, or G4 m5_SM = 0. LINK iff EARNED or NEW-CONDITION; otherwise NO-LINK (TAUTOLOGICAL-REPRODUCTION if REPRODUCES).

## 4. Foregone (declared; Lean `PositiveGeometryEmergentSpaceTime.GradedPositroid`, compiled BEFORE this prereg, no data)
- `graded_cubic_iff_acc`: for every (yQ, yu, yd, yL, ye) ∈ ℚ⁵, (all graded m1 = 0 ∧ all 64 cubic components = 0) ⇔ the four ACC. Hence G1 REPRODUCES for every κ ≠ 0 cell, including the simplex rival, so EARNED = false: FOREGONE.
- `no_proper_anomaly_free_union` (by `decide`): no proper union has Tr Y = Tr Y³ = 0, so G3 has no SM hit: FOREGONE.
- `sm_graded_quintic_ne`: Σ Y⁵ = 5/9 ≠ 0 for the SM; on p1 = p3 = 0, m5 ∝ p5 (planted check of the form), so m5_SM ≠ 0 unless the Δ(2,15) quintic coefficient vanishes (computed live; not foregone).
- `graded_charge_blind`: u-variables blind to any Cartan grading (corollary of `uCR_torus_invariant`).
Content of the rung: the formal statement that full Cartan grading recovers exactly the perturbative ACC and nothing more, and the live check of the higher-moment escape route (G4).

## 5. Planted and broken
Planted (inline, `planted_cases.json` lists them): κ(Δ(1,n)) = 2/(n(n+1)(n+2)) for n = 5, 15; κ(Δ(2,15)) = 129017/33392760 (BRIDGE); κ(Δ(2,4)) = 0; m3 = κ p3 on p1 = 0 on Δ(2,6) by brute force; m5 = c5 p5 + c23 p2p3 on Δ(2,7) (fit on 2 vectors, check a 3rd); SM and BRIDGE-rival (−7,0,8,−1) tables: cubic components equal the ACC combinations ((3,3,3) = Tr Y³, (2,2,3) = (6yQ + 2yL)/4, (0,0,3) = 2(2yQ + yu + yd), (1,1,3) = 3·(0,0,3)), all others 0; N_ACC = 2; Y-only count 35; G3 detector finds SM + vector-like (E, Ē) at Y = ±1.
Broken: "the Y-only graded Δ(2,15) reproduces the four ACC" (count 35 ≠ 2) must be REJECTED.

## 6. Anti-numerology / contamination
No fit to data. All anomaly facts textbook (Bilal, arXiv 0802.0634, verified title "Lectures on Anomalies"); positroid cells after Postnikov (arXiv math/0609764, verified title "Total positivity, Grassmannians, and networks"). Contaminated: the result is expected from the reduction; declared.

## 7. Prediction
NO-LINK (TAUTOLOGICAL-REPRODUCTION) ≈ 95%; G4 m5_SM ≠ 0 ≈ 97%.

## 8. Guard and locks
Hardened guard (`guard` in every scoring function: kappa_*, slice_moment, moment_direct, cubic_tensor, count_*, cubic_components_check, union_scan, classify, …); no pass flag; per-call re-verification of the checker sha256 against this file and of this prereg's add-commit as an ancestor of origin/main; caches keyed by origin/main sha; fetch once per process. Import test: 2 direct calls must refuse before the push; before the push only `py_compile` and the import test were run.

Locked:
- `sims/gpos/gpos_checker.py` sha256 `364bcfed929a0d9c377a3ac71bc7fc2c5cecda9ed5e7921ddeeba8de96656f0a`
- `sims/gpos/planted_cases.json` sha256 `6b2e10742c4efb0504336a0fb7449843baa01567b06a971b0e8e37e1314188be`
- `sims/gpos/import_guard_test.py` sha256 `9f7223753fa16be12a81d82be1381ff3783e5d668ddb62cc67b4e0b6ecd24629`
- (foregone-theorem file, not a scoring input; committed with the result) `lean/PositiveGeometryEmergentSpaceTime/GradedPositroid.lean` sha256 `5ffd1e80e1551594db710899cc617d91f0274f7a3d1f824925836a2b2914f955`
