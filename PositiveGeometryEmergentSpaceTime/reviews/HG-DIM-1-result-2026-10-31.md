# HG-DIM-1 result (curvature half; 1 rung, own pick, Grok, 2026-10-31; the author)

Provenance: The author's ("you pick next best rung out of our full trade space ... and run that one rung"); the rung is my own pick (prereg §0: EMC 2.06 vs LAT-KNEST-1 1.03 and HURWITZ-TP anchor ≈ 1.0). AUTORESEARCH-STOP stayed in place throughout. Base db715b9; prereg **bbfe77b** (pushed alone, first); checker + guard + import test + refusals 198b0d4 (guard refused on the unpushed prereg commit: CLI exit 1, import test 2/2 REFUSED, exit 2); live locked **dc76d4f**.
Locked checker `sims/hgdim1/hgdim1_checker.py` sha256 `a9e273fa…201e`, guard `8cc2ff03…8020`, unchanged after the push. Outputs `sims/hgdim1/hgdim1_{planted,broken,live}.json` (sha256 in `sims/hgdim1/result_sha256.txt`: planted 7429c065…6f50, broken 23c4c71b…ca22, live b1f3cd99…9364). Run manifest `sims/hgdim1/run_manifest.txt` (run id HGDIM1-LIVE-20261031T090819; Python 3.13.5, numpy 2.5.4, scipy 1.18.1, networkx 3.7; null seeds 20261031..33; 10.5 s wall, 136 684 kB peak RSS).

## Verdict (locked, as-is; no hand adjudication)
**LOCAL-COUNT** (my predicted branch, prior 0.7). SIMULATED (HGDIM1-LIVE-20261031T090819). On the associahedron flip graphs K_n, n = 6..11 (N = 14, 42, 132, 429, 1430, 4862; 26 175 edges in total), Ollivier curvature with uniform closed-neighbourhood measures is exactly

  **κ(e) = (2 − p(e))/(D+1)**, D = n − 3, p(e) = number of sides of the flip quadrilateral that are diagonals,

on **every** edge (0 exceptions; exact Fractions; HiGHS LP agrees on all edges n ≤ 8 and a seeded 300-edge sample per n ≥ 9). Negative edges exist iff n ≥ 7 (P-S holds). The draft prediction "κ ≥ 0" (HYPERGRAPH note) is **refuted** for n ≥ 7: min κ = −1/5 (n = 7), −1/3 (n = 8, p = 4), −2/7, −1/4, −2/9.

| n | D | N | edges | p = 1 / 2 / 3 / 4 | κ range | mean κ | fraction κ < 0 |
|---|---|---|---|---|---|---|---|
| 6 | 3 | 14 | 21 | 12 / 9 / 0 / 0 | [0, 1/4] | 1/7 | 0 |
| 7 | 4 | 42 | 84 | 35 / 42 / 7 / 0 | [−1/5, 1/5] | 1/15 | 1/12 |
| 8 | 5 | 132 | 330 | 112 / 168 / 48 / 2 | [−1/3, 1/6] | 1/33 | 5/33 |
| 9 | 6 | 429 | 1287 | 378 / 648 / 243 / 18 | [−2/7, 1/7] | 1/91 | 29/143 |
| 10 | 7 | 1430 | 5005 | 1320 / 2475 / 1100 / 110 | [−1/4, 1/8] | **0** | 22/91 |
| 11 | 8 | 4862 | 19448 | 4719 / 9438 / 4719 / 572 | [−2/9, 1/9] | −1/153 | 37/136 |

- Planted: ALL OK (PL1 K_5 → 1, PL2 C_8 → 0, PL3 Q_4 → 2/5, PL4 3-regular tree → −1/2, PL5 small flip graph, PL6 rule-8 valid alternatives accepted (edge orientation, dihedral rotation of the 7-gon), PL7 LP cross-check and idleness 1/2 on Q_4 → 1/4, PL8 gate self-tests, PL9 every verdict branch).
- Broken: ALL_REJECTED: open_nbhd fails PL1/3/4/5/8, dist_cap2 fails PL2/4/7/8, no_shared fails PL1/3/5/7/8, p_count_edges fails PL5 (each is a superset of the paper prediction), empty → ILL-DEFINED.
- Null (P-N): K_n is far from degree/size-matched random regular graphs on all 12 (n, seed) pairs: null mean κ −0.63..−0.68 (n = 8), −0.90..−0.93 (9), −1.13 (10), −1.27 (11); gap 0.66–1.27 ≫ 1/(D+1); KS p ≤ 2.5e−155. The flip graph is much less negatively curved than a random regular graph (its many 4-cycles from commuting flips), but it is not positively curved.
- Convention screen: in-rung **CONVENTION-ROBUST**. Idleness 1/2 checked by LP on every edge for n ≤ 9: κ_{1/2} = (D+1)/(2D)·κ_{1/(D+1)} exactly (CITED arXiv:1704.04398 Remark 5.4), so signs agree; in Lin–Lu–Yau form κ_LLY = (2 − p)/D. Under α = 0, κ_0 ≤ κ, so every negative edge stays negative.

## Observations (report-only; none changes the verdict; no checker flaw recorded)
- **Mean-curvature closed form (CONJECTURE, post-hoc fit):** mean κ(K_n) = (10 − n)/((n − 2)(2n − 5)) matches all six live sizes exactly and also n = 5 (1/3). It implies the mean curvature is positive for n ≤ 9, exactly zero at the decagon (n = 10), and negative from n = 11 on. Fitted after seeing the data, so it is a prediction for n = 12, 13 (not run), not a result.
- n = 6 (the 3D associahedron) is the last nonnegatively curved case: κ ∈ {0, 1/4}.
- The curvature is a purely local polygon count, so it carries no information beyond the flip quadrilateral. No dimension or scale enters; the result is a property of the combinatorics, as for every other invariant of the trunk.
- The dimension half of the draft was not run (killed on paper, FM-SMALL; prereg §0).

## Map change (M⁻ branch)
HG-DIM-1 node (notes/FRONTIER-HYPERGRAPH-2026-10-30.md): curvature half **closed** with an exact statement. The reading "the trunk positive geometry is a positively curved discrete space" is refuted for n ≥ 7 (NO-GO class per prereg §3). Positive things on the map: (i) the first exact, convention-robust geometric invariant of the associahedron graph, with a Lean certificate; (ii) the geometry component of the Lean map gains a new module (`PositiveGeometryEmergentSpaceTime.HgDim1`) but no edge to the STRUCT component (no SM line). The HGD node in figures/trade-space-traffic-light.mmd moves from `next` to `b_nogo` with this record. The edges HGD → CDT and HGD → M1 stay SPECULATION; the "emergent 4D rival" edge is weakened (no positive curvature, no dimension signal).

## Lean
`PositiveGeometryEmergentSpaceTime.HgDim1` (new; imported in PositiveGeometryEmergentSpaceTime.lean): 18 theorems + 21 defs, 0 sorry, no native_decide, kernel `decide` only, LEAN_NUM_THREADS=1. PROVED: `tris_valid` (42 masks, 4 pairwise noncrossing diagonals each), `tris_distinct`, `regular4`, `lip_walk` and `cost_lower` (weak duality: a 1-Lipschitz potential bounds every walk-realised matching, general), `edge_neg` (a K_7 flip with p = 3 has minimum matching cost exactly 6 between closed neighbourhoods, so κ = 1 − 6/5 = −1/5), `edge_pos` (p = 1, cost 4, κ = 1/5), `kappa_neg`, `kappa_pos`, `neg_edge_witness`. Scope: the lower bound is proved for matchings (enough for uniform equal-size measures by Birkhoff, not formalised); the fractional bound uses the same potential (Kantorovich duality, cited, not formalised). AxiomsAll after the rung: TOTAL theorems=1211 defs=659 nonstandard=0, axiom_decls=0, opaque_decls=0, sorry_dependent=0 (was 1193/638; +18/+21). Every HgDim1 declaration uses at most [propext, Classical.choice, Quot.sound].

## Tags
Verdict SIMULATED; κ formula on n ≤ 11 SIMULATED; two K_7 edges PROVED; idleness equivalence CITED (arXiv:1704.04398, fetched 2026-10-31); mean closed form CONJECTURE; general-n formula CONJECTURE (paper derivation in prereg §1, not proved). Blocker `NO-GO`.

## Credit
Proposal: 0.

Failure-mode: FM-MODEL (the positively curved, continuum-like reading of the trunk graph is the wrong model; Ollivier curvature is the local count (2 − p)/(D+1)).
Reopen: a different measure on the trunk graph that carries physical weights (e.g. canonical-form or kinematic weights rather than uniform), or a positive-curvature claim for a quotient or weighted associahedron graph; or a counterexample edge for n ≥ 12. Reopen flag: not set.
