# PREREG HG-DIM-1 (curvature half): is the associahedron flip graph positively curved, or is its Ollivier curvature a local polygon count? (locked)

Authorisation: author approved (2026-10-31). Base: origin/main db715b9. METHOD re-read at commit 74b2015 (`git log -1 --format=%h -- notes/AUTORESEARCH-METHOD.md`).

## 0. Why this rung (re-rank over the full trade space and the Lean map)
Excluded by the brief: M5, MC-1, TS-1, EW-Z1, CASCADE-2, pilot-wave rungs; PositiveGeometryEmergentSpaceTime-owned CASCADE-1b and the two worktrees. Lean map: `graph/analysis.json` (1806 nodes; 1172 thm, 634 def) has the geometry component (Associahedron, PositroidCells, IsingOG) disconnected from the STRUCT component (STRUCT1-3, FRMU, Separation, X6). A rung that adds a geometric invariant of the trunk object (associahedron) is the cheapest way to give that component a new measurable property.

| Rung | P_naive (M⁺) | P_used = 0.3·P | EMC = P_used·|M⁺| + (1−P_used)·|M⁻| | IV_min | d vs RG-IR-1 / CHIRAL v2 / RP-TN-1 | Killed on paper? |
|---|---|---|---|---|---|---|
| **HG-DIM-1 curvature on K_n (this)** | 0.2 (POS-CURVED) | 0.06 | 0.06·3 + 0.94·2 = **2.06** | 2 | 4 / 4 / 3 | no; sign outcome open, exact, Lean-certifiable |
| LAT-KNEST-1 (runner-up 1) | 0.1 | 0.03 | 0.03·2 + 0.97·1 = 1.03 | 1 | 2 / 3 / 3 | near-foregone by universality (method value only) |
| HURWITZ-TP Lean anchor (runner-up 2) | 0.05 | 0.015 | ≈ 1.0 | 1 | 2 / 3 / 2 | foregone theorem (Routh–Hurwitz TN is classical), credit 0 |
| R1 anomaly polynomial as canonical-form residue | — | — | — | — | — | yes: FM-QNBLIND (torus-invariant geometry, BRIDGE-PL-ASSOC) vs FM-TAUT (graded version, GRADED-POSITROID) |
| POS-GAP | — | — | — | — | — | yes: FM-FREE (ScaleNoGo; ABHY mass shift free) |
| TP-1BR | — | — | — | — | — | yes: FM-RANGE (Lusztig positivity exists for all types) |
| HG-DIM-1 dimension half | — | — | — | — | — | yes: FM-SMALL; on Catalan-sized graphs ball-growth dimension tracks the input D and is biased at small radius |
| HG-CI-1 | low | — | method only | 1 | — | not killed; costly Lean, method value only |

- M⁺ (POS-CURVED): HG-DIM-1 node live; first geometric (curvature) invariant of the trunk with a definite sign; edge Associahedron → HG frontier becomes a measured edge. M⁻ (LOCAL-COUNT / MIXED / NULL-LIKE): HG-DIM-1 curvature half closes with an exact statement (blocker row), plus a Lean certificate of a negative edge.
- Diversity axes (basin, SM ledger line, method class, declared failure tag): vs RP-TN-1: basin HG vs RP-BRIDGE (1), ledger none = none (0), method discrete optimal transport vs minor enumeration (1), tag FM-MODEL vs FM-TAUT (1) → 3. vs CHIRAL v2 and RG-IR-1: 4 each. Exploration slot already satisfied by RP-TN-1 in the last 3; this rung is still exploration-eligible.
- Honest framing: no candidate in the current map has a credible breakthrough probability toward a zero-parameter SM. The pick maximises decisive, exact information per CPU hour on the trunk geometry.
- **Declared deviation from the draft (notes/FRONTIER-HYPERGRAPH-2026-10-30.md §HG-DIM-1):** the draft objects (ht2_cells_n{2,3,4}, 8/64/256 entries) are FM-SMALL; I use the associahedron flip graphs K_n, n = 6..11 (N = 14..4862), the trunk positive geometry (Lean module `PositiveGeometryEmergentSpaceTime.Associahedron`). The draft's dimension estimator is dropped (killed on paper above). The draft's curvature prediction "κ ≥ 0 on most edges" is kept as the POS-CURVED branch.
- Feasibility: n = 11 has 4862 vertices, 19448 edges, D = 8; per edge one 9×9 assignment. Nulls 3 × same size. LP cross-checks ≤ 300 edges per n plus all edges for n ≤ 9 at idleness 1/2. Estimate < 15 min CPU, < 1 GB. Kill: > 60 min or > 2 GB → PARTIAL-LIMIT, no verdict.

## 1. First principles and prior art
- Ollivier–Ricci curvature (Ollivier 2009, cited in the HYPERGRAPH note): κ(x,y) = 1 − W1(μ_x, μ_y)/d(x,y). Here μ_x = uniform on the closed neighbourhood N[x] (idleness α = 1/(D+1)).
- CITED (fetched 2026-10-31, arXiv:1704.04398, Bourne, Cushing, Liu, Münch, Peyerimhoff, "Ollivier-Ricci idleness functions of graphs"): Thm 4.4, the idleness function α ↦ κ_α is linear on [1/(max deg + 1), 1]; Remark 5.4, κ_α = (1−α)·κ_LLY there. For a D-regular graph: κ_LLY = 2κ_{1/2} = ((D+1)/D)·κ_{1/(D+1)}. Also κ_0 ≤ κ_α (the idleness function is concave and vanishes at 1).
- Associahedron 1-skeleton = flip graph of triangulations of a convex n-gon: N = Catalan(n−2), D = n−3 regular, adjacency = one flip.
- **Paper derivation (CONJECTURE, the thing tested):** for a flip e of diagonal δ inside quadrilateral Q, let p(e) ∈ {0..4} = number of sides of Q that are diagonals. Each of the other D−1 diagonals either commutes with the flip (cost 1 pairing) or is a side of Q, where the two flips form a pentagon (5-cycle) and the best pairing costs 2. This gives κ(e) = (2 − p(e))/(D+1), i.e. κ_LLY(e) = (2 − p(e))/D. Consequences: n ≤ 6 has p ≤ 2 so κ ≥ 0; p = 3 first occurs at n = 7 (κ = −1/5); p = 4 at n = 8. n = 5 (pentagon C5): κ = 1/3.
- Tree-like null (random D-regular, girth large): κ ≈ (4 − 2D)/(D+1) (SPECULATION as a number; only used for expectations).
- Not found / not fetched: any paper computing Ollivier curvature of associahedron flip graphs. If it exists the rung's value is the Lean certificate and the link to the trunk.

## 2. Memory / contamination disclosure
On paper only before this push: the derivation in §1 and the planted values. No code has been run on any K_n. The checker was only `py_compile`d.

## 3. Object, rule, verdict (locked; `sims/hgdim1/hgdim1_checker.py`)
- Objects: K_n for n = 6..11 (live), K_5 and K_7 also used in planted tests. Edge curvature computed exactly: supports are equal-size uniform closed neighbourhoods, graph distances among supports are in {0,1,2,3} (computed exactly by adjacency/common-neighbour tests), W1 = (min-cost assignment)/(D+1) via `linear_sum_assignment`, returned as an exact Fraction. LP (HiGHS) cross-check of the assignment on all edges for n ≤ 8 and a seeded 300-edge sample (seed 20261031 + n) for n ≥ 9.
- Predictions: **P-K** κ(e) = (2 − p(e))/(D+1) on every edge of every K_n, n = 6..11 (exact). **P-S** negative edges exist iff n ≥ 7. **P-N** for n = 8..11 and each null seed in {20261031, 20261032, 20261033} (networkx `random_regular_graph(D, N, seed)`): mean κ(K_n) − mean κ(null) ≥ 1/(D+1) and two-sample KS p < 0.01.
- Gates: planted_ok (all planted tests), lp_agree_all, sep_all (P-N on all 12 pairs), kmin_all (min κ over all live edges), formula_all (P-K), neg_from7 (P-S).
- **Decision rule (fixed now, first match):** ILL-DEFINED if planted fails, no sizes, or LP disagrees; **NULL-LIKE** if sep_all false; **POS-CURVED** if kmin_all ≥ 0 (draft prediction); **LOCAL-COUNT** if formula_all and neg_from7 (my prediction); **MIXED-NONLOCAL** if formula_all false; else **UNCLASSIFIED**.
- Predicted verdict: LOCAL-COUNT (prior ≈ 0.7); POS-CURVED ≈ 0.2 (requires my derivation to be wrong); others ≈ 0.1.
- Refutation: P-K is refuted by one edge with κ ≠ (2−p)/(D+1); the draft prediction (κ ≥ 0) is refuted by one live edge with κ < 0.
- Report-only: per n the κ min/max/mean, fraction negative/zero, p histogram, the idleness-1/2 relation check (n ≤ 9), null means and fractions negative.
- Verdict classes for the statechart: NULL-LIKE and LOCAL-COUNT / MIXED-NONLOCAL are NO-GO for the reading "the trunk geometry is positively curved"; POS-CURVED is the GO class.
- **NO hand adjudication.** If the checker is flawed I record the flaw and propose a superseding v2; locked files are never edited.

## 4. Planted / broken / null / rival / conventions
- Planted (must all recover): PL1 complete graph K_5 → κ = 1; PL2 cycle C_8 → κ = 0 (consistent with arXiv:1704.04398, C_n n ≥ 6); PL3 hypercube Q_4 → κ = 2/5 (= 2/(d+1)); PL4 interior edge of a 3-regular tree → κ = −1/2; PL5 flip graph of the pentagon (n = 5, a 5-cycle) → κ = 1/3 on all edges and equals (2−p)/3.
- PL6 **valid alternatives that must be accepted (rule 8):** edge orientation κ(x,y) = κ(y,x); dihedral relabelling (rotation) of the 7-gon leaves the κ multiset and p unchanged.
- PL7 LP cross-check on Q_4 (0.4) and the tree (−0.5), and idleness 1/2 on Q_4 → 1/4 (Remark 5.4 relation).
- PL8 gate self-tests: formula gate true with 2/(d+1) and false with 2/d on Q_4; separation gate true for Q_4 vs random 4-regular graphs on 16 vertices, false for a graph against itself.
- PL9 verdict map: every branch reached on a synthetic gate dict.
- Broken variants (each must fail ≥ 1 planted, checked on paper): `open_nbhd` (PL1, PL3 fail), `dist_cap2` (PL4 fails), `no_shared` (PL1 fails), `p_count_edges` (PL5 fails), `empty` → ILL-DEFINED.
- Null: degree- and size-matched random regular graphs (3 seeds). Rival: "any D-regular graph looks like this" is the NULL-LIKE branch.
- **Convention-invariance declaration:** the physics-preserving equivalences are (a) the idleness convention α ∈ [1/(D+1), 1) and Lin–Lu–Yau, all positive multiples of each other on regular graphs (CITED Remark 5.4), so the sign of every edge and the formula shape are invariant (κ_LLY = (2−p)/D); checked live at α = 1/2 for n ≤ 9; (b) polygon relabelling (PL6). Under α = 0 (no laziness) κ_0 ≤ κ, so a negative edge stays negative, but nonnegative edges may not; α = 0 is declared out of scope. Not CONV-NA: the screening is the live α = 1/2 check.

## 5. Lean plan (post-live, PROVED)
`PositiveGeometryEmergentSpaceTime.HgDim1`: triangulations of the 7-gon as bitmasks over the 14 diagonals; certify one p = 3 edge with κ = −1/5 (upper bound by an explicit assignment of total cost (D+1)(1−κ) = 6, lower bound by an integer 1-Lipschitz potential), and one p = 1 edge with κ = 1/5, by `decide` (no `native_decide`). 0 sorry, 0 nonstandard axioms. If Lean memory is too tight, a smaller certificate is reported as such.

## 6. Tags and failure modes (declared)
Verdict SIMULATED (exact enumeration). Formula: CONJECTURE until the locked run; for n ≤ 11 SIMULATED; one K_7 edge PROVED (Lean). Failure-mode options: LOCAL-COUNT → **FM-MODEL** (the continuum, positively curved reading of the trunk graph is the wrong model; curvature is a local polygon count); NULL-LIKE → FM-MODEL; MIXED-NONLOCAL → none/FM-SPEC (formula wrong, curvature still computed); ILL-DEFINED → FM-SPEC; PARTIAL-LIMIT → FM-LIMIT; POS-CURVED → none. Credit: proposal 0 unless POS-CURVED (then proposal only, for the author).

## 7. Lock
`hgdim1_checker.py` sha256 `a9e273fae572b1113c89b4c172005351b685d90cdeddaa84b4870c350193201e`
`guard.py` sha256 `8cc2ff03a88ad55518a15cb914c3e9efbab501910c261b6ef59c5d10148a8020`
