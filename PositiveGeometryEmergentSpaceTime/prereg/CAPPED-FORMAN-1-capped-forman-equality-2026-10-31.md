# PREREG CAPPED-FORMAN-1: is Ollivier curvature equal to the capped Forman value on every edge of a simple polytope? (locked)

**Authorisation.** the author, owner message **** (2026-10-31, relayed by Grok/PositiveGeometryEmergentSpaceTime): "Lets run this as proper rung go, 'It's the most interesting claim in the paper, and also the least checked. I'd run it as a proper rung, or have'".

**Scope and limits.**
- CPU only and modest: at most 8 CPU and 15 GB RAM (I use 7 worker processes), no paid compute, no publishing.
- AUTORESEARCH-STOP stays in place.
- `<local path>` and `<local path>` are not touched, and neither is any public repo.
- This is a check of a claim in our own paper (`papers/paper-curvature/main.tex`, Prop. `prop:capped`, Conj. `conj:capped`). It is not a physics rung, so EMC is not computed.

## 0. Claim under test

Let P be a simple D-polytope and e = xy an edge of its graph. For each 2-face F ∋ e, let k_F be its number of sides. Let κ be the Ollivier curvature with the uniform measure on the closed ball (idleness 1/(D+1)).

- **INEQ (prop:capped, paper-proved):** κ(e) ≥ B(e) := 1 − Σ_F min(3, k_F − 3)/(D+1) = (κ_F(e) + Σ_F (k_F − 6)₊)/(D+1).
- **EQ (conj:capped):** κ(e) = B(e) on every edge of every simple polytope.

## 1. Literature and proof audit (done BEFORE this lock)

- `notes/CAPPED-FORMAN-1-novelty-sweep-2026-10-31.md`
  - 17 arXiv queries, 4 zbMATH queries and a web search. Google Scholar was blocked (HTTP 302) and is logged as inaccessible.
  - **CITED (full text): Jost–Münch, arXiv:2110.04554, Cor. 6.2.** F_K(x) ≤ κ(x) for every cell complex K. Applied to the unit-weight complex of 2-faces with ≤ 5 sides, F_K(e) = (D+1)·B(e). With κ_JM = (D+1)·κ_lazy, this **implies INEQ**.
  - So INEQ is KNOWN in substance, and the paper's "not recorded" claim must be corrected.
  - No statement or counterexample for EQ on polytopes was found.
- `notes/CAPPED-FORMAN-1-proof-audit-2026-10-31.md`
  - The paper's coupling proof of INEQ is correct. There are three minor implicit steps (G1–G3).
  - Overclaim O1: the intro says the inequality "shows the link survives exactly as long as faces have ≤ 6 sides". It shows only that the link breaks at ≥ 7.
  - Overclaim O2: novelty.
  - **ARGUED** (from JM Thm 5.1 + Thm 4.2): EQ holds on every edge that lies on **no non-facial cycle of length ≤ 5**. EQ is therefore open only on edges with non-facial 3-, 4- or 5-cycles.

## 2. Predictions (written before any live run)

- **P1:** INEQ holds on every edge (probability > 0.99, since two proofs exist). If an edge comes out below B, the verdict is recorded as INEQ-FAILS as computed. The review will then name a bug or a non-simple input as the likely cause and investigate in a superseding rung. The verdict will not be hand-edited.
- **P2:** EQ holds on every edge in D = 2 and D = 3 (probability 0.85).
- **P3:** EQ in D ≥ 4 (probability 0.55). Edges on non-facial short cycles could allow cheaper cross-matchings. The likeliest refuters are dual cyclic polytopes C_D(m)*, random duals in 4–6 dimensions, and truncations.
- **P4 (SC-DERIVATION):** every edge with no non-facial ≤5-cycle has κ = B exactly (probability > 0.98). A violation would refute my §4 derivation, not the paper.
- **P5 (conventions):**
  - κ_{1/2} = (D+1)/(2D)·κ on every edge (Bourne).
  - κ_JM (HiGHS LP) = (D+1)·κ on every edge.
  - The Forman identities F_orig = κ_F and F_K = (D+1)B hold on every edge.
  - κ₀ ≥ b₀ := 1 − (1 + Σ min(3, k−3))/D on every edge. This is valid by moving y → x. Equality at idleness 0 is exploratory only, with no prediction.
- **Predicted overall verdict:** INEQ-HOLDS+EQ-HOLDS (probability ≈ 0.5). The second most likely is INEQ-HOLDS+EQ-FAILS, driven by D ≥ 4 edges with non-facial short cycles.

## 3. Verdict branches and refutation criteria

The verdict is computed by `verdict` in the locked checker. Hand adjudication is forbidden.

1. **ILL-DEFINED** if any of the following happens. The run then says nothing about the claim.
   - any planted control fails;
   - the run is empty;
   - on any live edge, any integrity gate fails:
     - `solvers_agree`: Hungarian = networkx min-cost flow at all three idleness values;
     - `bourne_half`;
     - `jm_norm`: |LP − (D+1)κ| < 1e-6;
     - `forman_id`.
   - Simple-polytope structure violations in an input are **not** ILL-DEFINED. The input is skipped and listed, and every skip is reported. A skip can only arise from Wythoff patterns that are not simple polytopes, or from a random dual or truncation that is not simple.
2. **INEQ-FAILS** if any edge has κ < B. This refutes prop:capped (and, through the normalisation, would contradict JM Cor 6.2).
3. **INEQ-HOLDS+EQ-FAILS** if no edge is below B and some edge has κ > B. This refutes conj:capped. Each strict edge is a counterexample, reported with its face sizes, κ, B and non-facial cycle lengths.
4. **INEQ-HOLDS+EQ-HOLDS** otherwise. This supports conj:capped on the tested families; it does not prove it.

Further reporting rules:
- Sub-verdicts are reported per dimension (2, 3, ≥ 4) and per family from the same counts.
- The **SC-DERIVATION** line is CONSISTENT if no scfree edge is strict, VIOLATED otherwise. It is reported separately and does not change the main verdict.
- Max and min gap κ − B are reported, along with the per-signature tables (D, sorted face sizes, κ, non-facial cycle lengths).

## 4. Conventions covered

- **Idleness 1/(D+1)**, the lazy uniform closed-ball measure, is the claim.
- **Idleness 1/2:** covered exactly by Bourne linearity. The gate checks κ_{1/2} = (D+1)/(2D)·κ, so INEQ and EQ transfer with B_{1/2} = (D+1)/(2D)·B.
- **LLY and κ_JM:** covered, by the same scaling and gated through the LP.
- **Idleness 0:** **not covered** by the claim. Only κ₀ ≥ b₀ is gated, as part of `judge`; it is reported and does not enter the verdict. Equality counts are exploratory.

## 5. Checker and method

- `sims/cappedf1/cappedf1_checker.py`, locked.
- **Input representation.** A polytope is its vertex–facet incidence: a vertex is a D-set of facet labels.
- **Structure checks.** The checker verifies simplicity:
  - every (D−1)-subset lies in exactly 2 vertices;
  - the graph is D-regular and connected;
  - every 2-face, i.e. the vertices containing a given (D−2)-set, is an induced connected cycle.
- **Distances.** Distances between B(x) and B(y) are exact local values in {0, 1, 2, 3}.
- **κ by two independent exact integer solvers:**
  1. scipy `linear_sum_assignment` on unit atoms;
  2. networkx `min_cost_flow` on the mass network.
- **Three idleness values:** lazy (masses 1 each), 1/2 (centre D, neighbours 1) and 0 (open ball).
- **Third cross-check:** a HiGHS LP for κ_JM = inf{Δf(x) − Δf(y) : f(y) − f(x) = 1, f 1-Lipschitz on B(x) ∪ B(y)}. On K4 it gives 4 = (D+1)·1.
- **Forman counts.** Independent counts from enumerating parallel edges: F_orig for all 2-faces, and F_K for the ≤5-faces.
- **Non-facial cycles.** Non-facial cycles of length ≤ 5 through e are found by DFS.

## 6. Planted controls (hand-derived, all must pass)

30 controls:

- **Polygons:** C3 = 1, C4 = 2/3, C5 = 1/3, C6 = C8 = 0 (κ = B).
- **C6 at idleness 0:** κ₀ = 0, b₀ = −1.
- **K4 = Δ3:** lazy 1, κ_{1/2} = 2/3, κ₀ = 2/3 = b₀.
- **Simplices:** Δ4 = Δ5 = 1.
- **Hypercubes:** Q3 = 1/2, Q4 = 2/5, Q5 = 1/3.
- **Prisms C_k × I:**
  - horizontal edges: k = 4..9 give 1/2, 1/4, 0, 0, 0, 0;
  - rungs: 1/2 for k = 5, 7, 8;
  - k = 8 horizontal: κ_F/4 = −1/2, the uncapped link fails, and κ = B = 0.
- **Truncated cube** (Wythoff B3 110, 24 vertices): oct–oct edges κ = B = −1/2; tri–oct edges κ = B = 1/4.
- **Graph-only controls:** the 3-regular tree root edge gives −1/2; K5 gives 1.
- **Gate-firing controls:**
  - Q3 with its face sizes mislabelled as 6 must give κ > B (the EQ gate fires);
  - Q3 with sizes mislabelled as 3 must give κ < B (the INEQ gate fires).
- **Construction agreement:**
  - Π4 built from orderings, from the K4 graph associahedron and as A3 Wythoff 111 must have identical (face sizes, κ) multisets over 36 edges;
  - Q3 from products must match B3 Wythoff 100;
  - H3 100 must be the dodecahedron (20 vertices, all pentagons).
- **Non-facial cycle finder:** K4 edges give {4}, triangular-prism edges {5}, and Q3 and the truncated cube give none.

## 7. Broken checkers (each must be rejected, i.e. verdict ILL-DEFINED)

Each variant is run on the planted controls plus 4 objects: the prism k = 7, the truncated cube, Q4 and C_4(7)*.

1. Open neighbourhood used as "lazy".
2. Distance capped at 2.
3. Shared point charged (d(z,z) = 1).
4. Uncapped B.
5. Solver 1 replaced by the fixed index pairing (trace).
6. Empty run.
7. Solver 2 offset by +1.
8. Idleness 1/2 computed as lazy.

## 8. Live families (deterministic list, `live_specs`: 546 specs, seeds fixed)

**D = 2:** polygons C3..C12.

**D = 3:**
- prisms C_k × I for k = 3..12;
- Wythoff A3, B3 and H3 with all 7 ring patterns each, keeping the simple ones. This covers the tetrahedron, cube, dodecahedron, truncated tetrahedron, truncated cube, truncated octahedron, truncated dodecahedron, the fullerene C60 (the truncated icosahedron) and the great rhombi-solids;
- 120 random simple duals: polar duals of the hulls of 6..40 random points on S², seeds 0..119;
- Δ3, Q3, Π4, the associahedron K5, the cyclohedron W4 and the 3D stellohedron.
- Generic fullerenes beyond C20 and C60 are **not** included. This is disclosed as a coverage gap. The random duals and truncations stand in for them.

**D ≥ 4:**
- hypercubes Q4..Q8;
- simplices Δ4..Δ8;
- products:
  - C_a × C_b for 3 ≤ a ≤ b ≤ 10;
  - C_a × C_b × C_c for 3 ≤ a ≤ b ≤ c ≤ 6;
  - C_k × Q_m for k = 3..9, m = 2, 3;
  - C_k × Δ_n for k = 3..8, n = 2, 3.
- permutohedra Π5..Π7;
- graph associahedra:
  - paths on 5..8 nodes (associahedra);
  - cycles on 5..7 nodes (cyclohedra);
  - stars on 5..7 nodes (stellohedra);
  - complete graphs on 5..6 nodes (Π as graph associahedra);
  - 24 seeded random connected graphs on 5..7 nodes;
- dual cyclic polytopes C_D(m)*: D = 4 with m = 6..14, D = 5 with 7..13, D = 6 with 8..13, D = 7 with 9..12;
- Wythoff A4, B4 and F4 (all ring patterns, simple ones kept). H4 is excluded as too large;
- random duals: 60 in D = 4 (7..30 points), 40 in D = 5 (8..20 points), 16 in D = 6 (9..14 points).

**Truncations:** 60 seeded random truncation sequences. Each applies 3..7 truncations of random faces of dimension 0..D−2 to a base: the cube, the dodecahedron, Δ4, Q4, C5 × C6 or Δ5.

Construction smoke test (counts only, no curvature): 513 polytopes built, 33 skipped (all non-simple Wythoff patterns), 140,107 edges. Known counts reproduced: associahedron K6 has 42 vertices, cyclohedron W4 has 20, the 3D stellohedron has 16.

The **deliberate hunt for EQ counterexamples in D ≥ 4** is the dual-cyclic, random-dual, Δ_m-product, truncation and random graph-associahedron families. Their edges often lie on non-facial short cycles.

## 9. Contamination disclosure (honest)

**Before the lock:**
- The paper's unlocked LP script (`papers/paper-curvature/scripts/simple_polytopes_check.py`) had already reported equality, unlocked, on the dodecahedron, the truncated tetrahedron, the cube, the octahedron and icosahedron (those last two are not simple), a vertex-truncated cube, the prisms k = 3, 5, 6, 7, 9, 46 random 3D duals, and C_a × C_b for a, b ≤ 9.
- I developed and smoke-tested the checker on the planted controls only, by importing engine functions from /tmp scripts and not through the guarded modes.

**Live-family exposure during development**, all disclosed:
1. Construction counts (vertices, edges, simplicity) for all live specs, with no curvature computed.
2. The broken-variant dry run on the 4 broken-suite objects, which include C_4(7)* and Q4. Only gate-failure counts under broken variants were printed. No honest κ or B values were shown for C_4(7)*.
3. One timing probe of `process` on Q6 with honest settings. Only the edge count and time were printed, not κ.

## 10. Environment, run and limits

- **Environment:** Python 3.13.5, numpy 2.5.4, scipy 1.18.1, networkx 3.7 (pinned in the run manifest).
- **Run id** CAPPEDF1-<UTC timestamp>, with modes in the order planted → broken → live.
- **Limits:** a hard `timeout` of 45 min per mode. Memory is sampled, and if total RSS exceeds 8 GB the run is killed and recorded as PARTIAL-LIMIT.
- **Outputs** in `sims/cappedf1/`:
  - `cappedf1_{planted,broken,live}.json` and `.log`;
  - `run_manifest.txt`, `result_sha256.txt`, `live_time.txt`;
  - `guard_refusal.txt`, the pre-push refusal of both guarded calls, exit 2.
- Negative results are kept.

## 11. Locked hashes

`cappedf1_checker.py` sha256 `7c6da283a6329d9e0a77626db48f03f1b0bf675c5077110851632786c00238b1`
`guard.py` sha256 `4accb9516b2d33b7d036ac66eab6e20bd4814f3261a1d84bb02449fbe4ba119f`
