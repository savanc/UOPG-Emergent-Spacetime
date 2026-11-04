# CAPPED-FORMAN-1 result: is the capped-Forman bound on simple polytopes an equality? (Grok, 2026-10-31; the author)

## Provenance
- Request: The author's ("Lets run this as proper rung go", quoting "It's the most interesting claim in the paper, and also the least checked. I'd run it as a proper rung"). AUTORESEARCH-STOP stayed in place.
- Base 800a566. Prereg **27395b7**, pushed alone and first (sha256 `48b42147…8d88`).
- Checker, guard, import test, refusal record, literature sweep and audit notes: **15e8af0**. The guard refused on the uncommitted prereg (import test 2/2 REFUSED, exit 2; `sims/cappedf1/guard_refusal.txt`).
- Run **CAPPEDF1-20261031T120726Z**, outputs **84c3261**. Lean **e0d5e72**. Write-ups and paper correction: this commit.
- Locked files, unchanged: checker `sims/cappedf1/cappedf1_checker.py` sha256 `7c6da283…38b1`; guard `4accb951…f62e`.
- Manifest `sims/cappedf1/run_manifest.txt`: Python 3.13.5, numpy 2.5.4, scipy 1.18.1, networkx 3.7; 7 workers; fixed seeds listed there. Planted 2 s, broken 6 s, live ≈ 384 s wall; peak RSS ≈ 0.85 GB. CPU only, no paid compute.
- Run note: the tool session that hosted the runner script was aborted after the broken mode finished. The live child process was unaffected and completed unattended; its exit line, the live wall time and the RSS peak were appended to the manifest by hand from file mtimes and a replacement sampler (marked as such). No result file was edited.
- Output sha256 (`sims/cappedf1/result_sha256.txt`): planted cfac19aa…, broken af59a200…, live 6324e806….

## Verdict (locked, as is; no hand adjudication)
**INEQ-HOLDS+EQ-HOLDS**, my predicted branch (p ≈ 0.5). SIMULATED (CAPPEDF1-20261031T120726Z).

- **513 simple polytopes, 140 107 edges, all computed exactly** (Hungarian assignment and networkx min-cost flow, agreeing at idleness 1/(D+1), 1/2 and 0; HiGHS LP for the Jost–Münch normalisation gate).
- κ = B on **every** edge: 0 strict, 0 below, **max gap 0, min gap 0**. No counterexample to Conj. conj:capped.
- **Cap active** (some 2-face with k ≥ 7, so κ > κ_F/(D+1)): 18 388 edges, 381 signatures, faces up to k = 12.
- **Non-facial short cycles** (a ≤ 5-cycle through e that is not a 2-face): 21 775 edges (lengths 5: 18 005; 4 and 5: 3 133; 4: 637), all at equality; 6 288 of them also cap-active.
- 33 Wythoff ring patterns skipped as not simple (listed in the log), as the prereg requires; 546 specs − 33 = 513.
- Planted **30/30** pass; broken **8/8** rejected (ILL-DEFINED). Integrity gates (solvers_agree, bourne_half, jm_norm, forman_id) pass on every live edge.
- **SC-DERIVATION: CONSISTENT** (118 332 edges with no non-facial short cycle, 0 strict). The condition is sufficient but evidently not necessary.
- Conventions: κ_{1/2} = (D+1)/(2D)·κ and κ_JM = (D+1)·κ on every edge, so INEQ and EQ transfer to idleness 1/2, LLY and the Jost–Münch normalisation. **Idleness 0 is not covered**: κ₀ ≥ b₀ held on every edge (0 failures); κ₀ = b₀ on 7 373 edges only (exploratory, no prediction).

| D | polytopes | edges | strict | cap-active | non-facial short cycles |
|---|---|---|---|---|---|
| 2 | 10 | 75 | 0 | 57 | 0 |
| 3 | 170 | 8 850 | 0 | 3 885 | 141 |
| 4 | 183 | 24 892 | 0 | 10 077 | 5 639 |
| 5 | 85 | 22 645 | 0 | 2 701 | 8 565 |
| 6 | 56 | 76 257 | 0 | 1 311 | 6 519 |
| 7 | 7 | 6 328 | 0 | 357 | 875 |
| 8 | 2 | 1 060 | 0 | 0 | 36 |

Families (polytopes / edges, all 0 strict): polygons 10/75; prisms 10/225; Wythoff A3,B3,H3,A4,B4,F4 simple patterns 33/9 110; random duals 3D 120/7 110, 4D 60/7 896, 5D 40/8 760, 6D 16/3 378; simplices 6/116; hypercubes 6/1 788; polygon products 36/3 084; triple products 20/5 670; polygon×cube 14/1 176; polygon×simplex 12/528; permutohedra 4/17 196; associahedra 5/6 727; cyclohedra 4/3 572; stellohedra 4/6 840; permutohedron-GA 3/2 076; random graph associahedra 24/47 377; dual cyclic C_D(m)* 26/3 665; random vertex truncations 60/3 738.

Predictions: P1 (INEQ) hit; P2 (EQ, D ≤ 3) hit; P3 (EQ, D ≥ 4, p 0.55) hit; P4 (SC-DERIVATION) hit; P5 (conventions) hit.

## Literature (notes/CAPPED-FORMAN-1-novelty-sweep-2026-10-31.md; CITED = fetched)
- **INEQUALITY KNOWN.** Jost–Münch arXiv:2110.04554 (full text fetched): Cor 6.2 (F_K ≤ κ for any 2-complex K) applied to K = the unit-weight 2-faces with ≤ 5 sides gives F_K = (D+1)B, i.e. Prop. prop:capped, after the normalisation κ_JM = (D+1)κ (gated numerically on every edge). CITED. The paper's "not recorded" claim for the inequality is wrong (O2).
- Cor 6.1 (κ = max_K F_K) and Thm 5.1 + Thm 4.2 give my sufficient condition for equality (no non-facial ≤ 5-cycle through e). ARGUED, SIMULATED-consistent; not a proof of the conjecture.
- Tee–Trugenberger (as reported in JM §6) give equality when short cycles share at most one edge; not the capped statement.
- **EQUALITY (conj:capped) not found** in arXiv, zbMATH or web searches. Google Scholar was inaccessible (302), so the sweep is not complete.

## Proof audit (notes/CAPPED-FORMAN-1-proof-audit-2026-10-31.md)
- Prop. prop:capped proof: **correct**, with three implicit steps (G1 simple-polytope face fact uncited; G2 injectivity of F ↦ u_F; G3 distinct faces through e meet only in e). PAPER-PROVED + CITED.
- O1: intro line "survives exactly as long as ≤ 6" overclaimed (that direction is the conjecture). Corrected.
- O2: novelty of the inequality. Corrected (credit JM Cor 6.2 at intro, prior-art table and remark).
- O3: "LLY equals max Forman" holds only up to the factor D on D-regular graphs. Corrected.
- 3D sketch: "reduces to the absence of short non-facial cycles" is wrong as stated (K4 and the triangular prism have such cycles yet attain equality). Corrected to "sufficient, not necessary". 3D equality remains CONJECTURE.

## Lean (e0d5e72; lake build passes, 0 sorry, no native_decide, decide +kernel only)
- `PositiveGeometryEmergentSpaceTime.CappedForman` (8 thm): per-face weight optimisation max_{m≥0} g_k(m) = 1 − min(3, k − 3) (`face_term_le`, `face_term_max`); capped bound ≥ Forman bound, equality iff all k ≤ 6 (`capped_ge_forman`, `capped_eq_forman_iff`). PROVED, all k, D.
- `PositiveGeometryEmergentSpaceTime.CappedFormanCerts` (42 thm): exact closed-neighbourhood matching cost and κ = B for one edge of each class of C_7×K_2 and C_8×K_2 (k-gon edge cost 4, κ = 0; vertical cost 2, κ = 1/2) and of the truncated cube (tri–oct cost 3, κ = 1/4; oct–oct cost 6, κ = −1/2). PROVED for the named edges (matching form; Birkhoff/Kantorovich cited; per-class edge-transitivity not formalised).
- Not formalised: Prop. prop:capped in general, Conj. conj:capped.
- AxiomsAll: **1378 theorems / 798 defs / 0 nonstandard / 0 sorry** (was 1328/746/0/0; +50/+52).

## Paper (papers/paper-curvature/main.tex)
Corrections were needed (O1–O3, 3D sketch) and are minimal; a status line was added to the conjecture evidence. Errata: notes/paper-curvature-errata-CAPPED-FORMAN-1-2026-10-31.md. latexmk clean (17 pages); PDF copied to <local path> (sha256 071b552a…3c887).

## Classification
Conjecture status: CONJECTURE, supported (SIMULATED, 140 107 edges, gap 0). Inequality: FM-KNOWN (JM Cor 6.2). Blocker tag: REDUNDANT for the inequality; the equality is OPEN. Credit 0 (no trade-space node).
Reopen: a proof of conj:capped (at least D = 3), or an edge of a simple polytope with κ > B (most likely in D ≥ 4 on non-facial short cycles; none found).
