# H-T5f pre-registration: pure carrier on tree tiles, and the tile adjacency graph vs the associahedron (2026-10-12)

Written and pushed **before computing**. Environment: `<local path>` + `requirements-lock.txt`. The gauge
convention is G2 throughout, as in H-T3–H-T5d.

## Prior art (credited)

- **Perlstein–Tessler, arXiv:2501.07576 (2025):**
  - BCFW cells = tree-of-triangles graphs;
  - Cor. 4.3.5 / Fig. 9: an internal codim-1 boundary contracts two adjacent triangles of the triangle tree into a
    square, and is shared by exactly two BCFW cells (Γ₊, Γ₋), i.e. the two resolutions of the square. **This is a flip
    of the triangle tree.** So "BCFW tile adjacency = flip graph (associahedron 1-skeleton)" is essentially **already
    in PT**; our Part B is an independent check, not a discovery.
  - Thm 5.0.3: boundary strata of BCFW cells map injectively.
- **Huang–Wen 2014:** BCFW for ABJM, measure dlog in BCFW-bridge coordinates.
- **HWX 2014:** loop factor J in Ising/OG variables. Our H-T3b found that HWX rule C1 has V-faces with Π sech 2J.
- **2510.25733 (ABJM loop BCFW):** odd/even triangulations of an n-gon.
- **Arkani-Hamed–Bai–He–Yan / Arkani-Hamed–He–Lam:** associahedra for bi-adjoint φ³ (other context).
- **Łukowski et al.:** BCFW cell adjacency in other amplituhedra.

**Re-read gap disclosure:**
- We know H-T5d's wall list (T1·T3, T2·T4, T3·T5, T4·T1, T5·T2). It was *chosen* by contracting internal tree edges,
  so it is not independent evidence.
- We know H-T3/H-T3b: the ABJM measure = 2⁻ᵏ · carrier · J, and rule C1 gives V-faces a Π sech 2J factor. That makes
  "J = 1 on trees" doubtful a priori.

## Part A: carrier on tree tiles

Tile form, two ways, at the tile's own exact forward points (rational t = tanh J):
- **(i) Residue of the Lee/HW top form:**
  - n = 10: the H-T5d Grothendieck residue on the 3-fiber;
  - n = 8: the H-T5b 1-dim residue.
- **(ii) Pushforward of the pure carrier:** Ω_car = Π_e (2 coth 2J_e) / det(∂Φ/∂J). Φ is the same Y-chart as in (i),
  and J ranges over the tree's edges (7 at n = 10, 5 at n = 8).

**Hypotheses:**
- **H0 (pure carrier, J = 1):** R = Ω_res / Ω_car is the same constant (up to a sign fixed per tile) at every point of
  every tree tile.
- **H1 (alternative, rule-C1 V-faces):** R / J_C1 is constant, with
  J_C1 = Σ_{S ⊆ interior vertices} Π_{v∈S} Π_{e∋v} sech 2J_e, where an edge joining two vertices of S is counted once.
- **H2:** neither.

**Design:** 8 points per tile (n = 10: 5 tiles, 40 points; n = 8: 2 tiles, 16 points), at mp.dps = 40. Finite
differences use h = 10⁻¹⁵, so about 25 digits are reliable.

**Criteria:**
- **PASS H0:** relative spread of |R| < 10⁻¹⁵ over all points of all tiles at that n.
- **PASS H1:** the same for |R/J_C1|.
- If both or neither pass: report.

Symbolic proof is attempted only if numerics pass and a closed form is cheap. Otherwise the result is [SIMULATED]
(this limit is disclosed in advance).

**Signs:** report sign(R) per tile and its relation to sign det(∂Φ/∂J) (the orientation induced by the network chart).

**Amplitude statement:** if H0 passes, then "amplitude form = Σ_tree tiles pushforward of 2⁻ᵏ·carrier" follows from
BCFW = amplitude (HW, CITED) + PT tiling + H0. It is stated as conditional, not as a new theorem.

## Part B: adjacency vs associahedron

**Bijection (fixed now):**
- Trivalent plane tree with leaves 1..k ↔ triangulation of a k-gon whose sides are labelled 1..k (side i dual to
  leaf i). Polygon vertex v_i sits between sides i and i+1.
- A cherry (i, i+1) is the diagonal (v_{i−1}, v_{i+1}).
- n = 10: T_x (leaf x in the middle, cherries (x+1, x+2), (x+3, x+4)) ↔ diagonals {(v_x, v_{x+2}), (v_{x+2}, v_{x+4})},
  the fan at v_{x+2}.
- **Predicted flip graph:** T_x — T_{x+2}, i.e. the 5-cycle 1-3-5-2-4-1.
- n = 8: the two trees ((12)(34)) and ((23)(41)), one flip edge.

**Wall graph (independent of flips):**
- For each tree tile, take all 2·(#edges) network degenerations (each edge t → 0 or t → 1) and keep those with exactly
  dim − 1 crossings. These are the codim-1 boundary cells, identified exactly by τ (exact rational arithmetic).
- Two tiles are adjacent iff they share a codim-1 boundary τ. A boundary shared by exactly two tiles is "internal".
- Y-space confirmation is reused from H-T5d (c) for n = 10 and H-T5b (c) for n = 8: spurious-pole cancellation on
  those walls.

**PASS:** the wall graph equals the flip graph under the bijection (same edge set). **FAIL:** otherwise.

**n = 12 fitness:** the combinatorial wall graph needs only exact τ computations, which is cheap. So it **will be run**
on the 14 tree tiles (expected K_5 1-skeleton: 14 vertices, 21 edges). Certified Y-space membership at n = 12 (6-dim
fibers) is out of scope (not fit for the box in this rung). The n = 12 tiling itself is not re-tested.

## Self-review against the four demands

- **Methods:** Part B is exact combinatorics; Part A is 40-digit numerics with finite differences (not certified).
- **Process:** prior art says Part B is known, so it is a check.
- **Simulation:** small N, but each test is a functional identity.
- **Infrastructure:** cheap (< 10 min).
