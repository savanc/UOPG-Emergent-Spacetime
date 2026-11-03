# GRADED-POSITROID result (2026-10-22, Grok; continuous-mode own pick (author approved 2026-10-22))
Run id: GPOS-2026-10-22-r1 (single live run,, sims/gpos/gpos_output.txt; no reruns).
Verdict: protocol PASS (planted ALL OK, broken REJECTED) ⇒ substantive NO-LINK (TAUTOLOGICAL-REPRODUCTION) / NO-GO
Foregone and declared. Credit 0 (proposal). Prereg 0d78080 (pushed alone); planted 19:58:21, broken 19:58:23, live (all finished within 20 s).

## Question
BRIDGE-PL-ASSOC graded the 15 Weyl-state columns of Gr⁺(k,15) by Y only and got Tr Y = Tr Y³ = 0 (not earned, 35 vs 2 solutions). REVIEW-2026-10-20 follow-up: grade by the full Cartan weight (H3, H8′, T3, Y). Does the graded positroid object give any condition beyond the Cartan-restricted anomaly polynomial, and is it earned (not reproduced by the simplex/cube rivals)?

## Results (sims/gpos/gpos_output.txt)
| Trial | Result |
|---|---|
| G1 κ: Δ(1,15) / Δ(2,15) / Δ(3,15) / cube | 1/2040, 129017/33392760, 868271/85704820, 0 |
| G1 N (yQ = 1, basis \|p\|,\|q\| ≤ 10) | 2 / 2 / 2 / 131594 (cube: grav only); N_ACC = 2 |
| G1 Δ(2,15) solutions (yu, yd, yL, ye) | (−4, 2, −3, 6), (2, −4, −3, 6): SM and u↔d |
| G3 proper anomaly-free multiplet unions (SM) | none |
| G4 Δ(2,15) along Y, SM | m4 = 20438911/2163850848, m5 = 466133/1713048588 ≠ 0 (p5 = Σ Y⁵ = 5/9) |
REPRODUCES = True; EARNED = False (simplex rival also gives 2); NEW-CONDITION = False.
Planted ALL OK: κ(Δ(1,n)) = Dirichlet for n = 5, 15; κ(Δ(2,15)) = BRIDGE value; κ(Δ(2,4)) = 0; m3 = κ p3 (Δ(2,6) brute force); m5 = c5 p5 + c23 p2p3 (Δ(2,7)); SM and rival (−7,0,8,−1) component identities; N_ACC = 2; Y-only 35; G3 detector finds (E, Ē). Broken (Y-only reproduces ACC: 35 ≠ 2) REJECTED.

## Lean `PositiveGeometryEmergentSpaceTime.GradedPositroid` (9 theorems + 5 defs; 0 sorry; no native_decide; #lint clean; standard axioms; no FRONTIER-AXIOM)
`polarized_cubic_reduction`, `triple_sum_general` (Fin 5, three gradings), `graded_cubic_iff_acc` (∀ y ∈ ℚ⁵: all graded m1 and all 64 cubic components vanish ⇔ the four ACC), `sm_graded_cubic_zero`, `sm_weights_sum_zero`, `sm_graded_quintic_ne` (Σ Y⁵ = 5/9), `no_proper_anomaly_free_union` (`decide`), `graded_charge_blind` (corollary of `uCR_torus_invariant`, BRIDGE-PL-ASSOC rung), bundle `graded_positroid_nolink`. Defs `genW`, `smW`, `m1`, `cub`, `ACC`. AxiomsAll 885 / 399 / 0 / 0 (fresh, after rebase onto INT-1 8c16ce5 and FL-1Z commits; 859 / 386 before the rebase).

## Reading
- Full Cartan grading does recover SU(3)²Y and SU(2)²Y (what Y-only grading missed), but only as the restriction of the anomaly polynomial to the Cartan, multiplied by a geometry-only constant κ. Any exchangeable measure with κ ≠ 0 (the simplex, every Δ(k,15) checked) gives the same conditions; κ = 0 (cube) gives fewer. The geometry contributes a nonzero scalar, not a condition: TAUTOLOGICAL-REPRODUCTION.
- Higher moments are not an escape: m5 ≠ 0 for the SM, so imposing them would exclude the SM. No proper multiplet union is anomaly-free, so face restrictions add nothing.
- Per the review kill rule the steelman ("positroid geometry adds nothing to charge selection beyond the anomaly polynomial") is now the working position for the moment/torus route. This is a reading only; MISSION is not edited (approval-gated).

## Tags (P-6)
PROVED: the identities and the ⇔ in Lean above. SIMULATED (exact): κ values, counts, m4/m5 (checker). CITED (arXiv verified this session): positroid cells, Postnikov math/0609764; anomaly conditions, Bilal 0802.0634. Earlier BRIDGE citations unchanged. No MEMORY claim used for the verdict. CONJECTURE: none.

## Caveats
Only exchangeable (Sₙ-symmetric) moments of the uniform measure; only the declared cells; Cartan (not full group) weights, so non-abelian anomalies SU(3)³, SU(2) Witten enter only through their Cartan shadows; basis-limited counts (|p|,|q| ≤ 10). KLS (1111.3660) not cited (arXiv fetch timed out; unverified). Not touched: CREDITS.md, EW-Z1 paths, R4Indep blueprint block, XResearch, other worktrees; trade-space file/figure and Lean naming map (deltas in notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-22.md).

## Reopen triggers
A positroid object that is not an exchangeable moment of the graded weights (cell combinatorics depending on the multiplet structure) yielding a condition the SM satisfies but a generic ACC solution does not; a non-polynomial (canonical-form residue) charge functional with a Lean identity to a non-ACC SM property.
