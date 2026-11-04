# H-T5d pre-registration: is the n = 10 (k = 5) ABJM-amplituhedron tiling chosen by Ising networks? (2026-10-12)

Written and pushed **before any result computing**.
- Gauge, GP map, η, positive branch, Λ (moment curve x = 1..10, now 10×7) and the certified-membership standard are
  all as in H-T5b.
- Environment: `<local path>` + `requirements-lock.txt` (python-flint 0.9.0 added).

## Prior art and re-read gap disclosure

**Already proved (credited, not re-claimed):**
- *Perlstein–Tessler, "The BCFW tiling of the ABJM amplituhedron", arXiv:2501.07576 (2025):*
  - the images of the BCFW orthitroid cells tile O_k for all k and strongly positive Λ;
  - injectivity and local separation hold for all positive Λ;
  - BCFW cells for k ≥ 3 are exactly the "tree-of-triangles" (ToT) OG graphs whose triangle tree has a vertex between
    external legs 2k and 1. The triangle tree is a trivalent plane tree G with k external vertices and M(G) = Γ (the
    medial graph), i.e. it is a GP/Ising network.
- *Huang–Wen 2014:* the Grassmannian BCFW for ABJM.
- *HKWZ 2111.03037 and He–Kuo–Zhang 2111.03130:* define O_k and give numerical evidence.
- *He–Kuo–Zhang et al., "The ABJM amplituhedron" 2306.00951 (and slides):* at n = 10 there are **25** (n−3)-dim cells
  relevant to loop chambers.
- *Galashin–Pylyavskyy 1807.03282:* OG≥0 cells = Ising networks.

**Tile count.** We have *not* looked at an explicit n = 10 BCFW tile list. From Perlstein–Tessler's description, the
count should be the number of trivalent plane trees with k = 5 leaves, Catalan(3) = **5** (n = 8: Catalan(2) = 2,
matching H-T5b). This is a [CITED-derived] expectation, checked after the run.

**What we already know (disclosed):**
- n = 8: HW σ2 = N1 − (2,3) and σ1 = N1 − (1,2), where N1 = star(c; 1..4) + bonds (1,2), (2,3).
- In checking the rule definitions (not results) we found:
  - these two n = 8 cells are exactly the two trivalent trees ((12)(34)) and ((23)(41)) (τ computed);
  - so the n = 8 "cut a neighbouring bond" tiles are star–triangle equivalent to trees.
- **Rule R2 below is therefore informed by Perlstein–Tessler and is not a blind guess.** R1 is the rule derived from
  n = 8 Ising data alone.

## Rules (fixed now)

Let W5 = star(c; 1..5) + all boundary bonds (1,2), (2,3), (3,4), (4,5), (5,1). τ(W5) is the top cell: 10 crossings,
dim 10 = dim OG(5,10). Note N1 = W4 − {(3,4), (4,1)}: the bonds touching the last spin are cut.

**R1 (primary, "cut neighbouring boundary bonds"):**
- Always cut the bonds touching spin k: (4,5) and (5,1).
- Then cut exactly one more of the neighbouring chain (1,2), (2,3), (3,4).
- Predicted tiles: 3 cells, each star(c; 1..5) + two kept bonds:

| Tile | Kept bonds | τ |
|---|---|---|
| R1a | (1,2), (2,3) | (5,6,9,8,1,2,10,4,3,7) |
| R1b | (1,2), (3,4) | (4,7,9,1,8,10,2,5,3,6) |
| R1c | (2,3), (3,4) | (5,9,7,8,1,10,3,4,2,6) |

All three are 7-dim (7 crossings).

**R2 (alternative, "trivalent tree networks"):** the tiles are the 5 trivalent plane tree Ising networks T_x,
x = 1..5. Leaf x is attached to the middle vertex v, and the cherries (x+1, x+2) and (x+3, x+4) (mod 5) are attached
to u and w. τ(T_1..T_5):
- T1 = (5,8,6,9,1,3,10,2,4,7)
- T2 = (6,9,7,10,8,1,3,5,2,4)
- T3 = (4,6,8,1,9,2,10,3,5,7)
- T4 = (7,9,6,8,10,3,1,4,2,5)
- T5 = (4,7,9,1,8,10,2,5,3,6) = R1b

All are 7-dim.

## Method fitness (hard gate)

**Dimensions (verified):**
- dim OG(5,10) = 10;
- the OMA has dim 2k − 3 = 7 (Perlstein–Tessler Thm 2.2.3);
- the fiber of m ↦ Y has dim 3. On a test point, the 10 linear equations C(m)λ̃ = 0 have rank 7.

**The linear-fiber trick still holds:** the GP chart is global on the big cell and C(m) η C(m)ᵀ ≡ 0, so the fiber is
an exact rational **affine 3-plane**, not a line.

**Certified alternative to 1-dim root isolation:**
1. On the 3-plane (coordinates a, b, c), the closure of a 7-dim cell τ is cut out by the minors in Z_τ. On a test
   point, Z_τ has 20 minors, all *quadrics* in (a, b, c).
2. Compute a lex Gröbner basis (sympy, test time 0.03 s). If the ideal is not zero-dimensional, flag the sample as
   *degenerate*.
3. Isolate the real roots of the univariate element exactly.
4. Back-substitute exactly: require each remaining basis element to be linear in the next variable with a nonvanishing
   leading coefficient at the root (shape position); otherwise the point is *uncertified*.
5. Enclose the solution point in a rigorous interval box (mpmath `iv`, outward rounding, isolating width < 10⁻⁴⁰).
6. Decide all 252 Plücker signs by interval evaluation:
   - minors in Z_τ are exactly 0 by construction;
   - any other minor whose interval contains 0 makes the sample *uncertified* (expected only on measure-zero sets).

Z_τ for each cell is taken at two random rational forward points and must agree.

**Validation gate (must pass before samples):** 8 forward points per predicted cell (7 distinct cells). The rational
forward m must be among the certified solutions (exact substitution into the Gröbner basis), and the cell must be
reported as containing Y.

**Infrastructure:**
- The box was reset between rungs: the repo clone and the venv were wiped. The repo was re-cloned from GitHub (no
  loss; all work was pushed) and the venv rebuilt from the lock.
- ~3 GB free RAM, 8 CPUs.
- Cost: symbolic Z minors were measured at ~7 s per cell per sample (sympy). They will be computed by exact
  interpolation or flint instead. Target ≤ 1 s per cell-sample, i.e. 7 cells × ~1200 samples ≈ ≤ 2.5 h single core.
  The run may be split into ≤ 4 parallel processes (memory < 300 MB each).

**Simulation design:**
- Uniform-in-m rejection is **infeasible**: 0 of 10⁵ draws from [0,1]¹⁰ were positive. Fresh samples are therefore
  Ising-law samples on the top network W5:
  - F-W5u: 600 samples, t uniform (rational, denominator 1000);
  - F-W5log: 400 samples, J log-uniform on (e⁻⁴, e²), t rationalised to 10⁻¹²;
  - B-near: 100 samples, one t ∈ {10⁻⁶, 1 − 10⁻⁶};
  - B-on: 2 samples on each predicted cell (reported separately).
- Every interior point of OG>0 is a W5 point (GP: one reduced network parametrises the whole top cell), so these cover
  the whole OMA interior, but with Ising-law densities, not uniform ones (limit recorded).
- Coverage bound: 0 certified misses in N gives a 95% upper bound of 3/N on the uncovered fraction.

## Criteria

For each rule separately, over certified non-degenerate samples in F-W5u ∪ F-W5log:
- **PASS(tiling):** 0 certified overlaps (sample in ≥ 2 predicted tiles) and 0 certified misses (sample in none).
- **FAIL:** ≥ 1 certified overlap or ≥ 1 certified miss.
- **INCONCLUSIVE:** only uncertified or degenerate exceptions, or the gate fails.

**Rule verdict = PASS** iff PASS(tiling) **and** either:
- the tiles coincide with the BCFW cells (checked after the run against Perlstein–Tessler's description), or
- they form an independent tiling whose internal walls pass (c).

**(c) Spurious poles** (for each passing rule, every pair of tiles sharing a 6-dim internal boundary):
- Tile form Ω_τ(Y) = the Grothendieck residue, at the fiber point p_τ, of h = ρ_H · det(VᵀV) / (det[DΦ; Vᵀ] · Π_{i=1..5} M_i).
  - ρ_H, Φ and the gauge are as in H-T5b; V is the 10×3 fiber basis; Φ is a fixed 7-coordinate chart of gauge-fixed Y,
    checked nonsingular.
  - At a simple crossing of the three vanishing consecutive minors, Res = h·Π M_vanishing / det ∂(M_a, M_b, M_c)/∂(a, b, c).
  - If the crossing is not simple, (c) for that wall is INCONCLUSIVE.
- Wall point m* from the common-boundary network (trees: contract the internal edge being flipped; R1: cut both
  differing bonds). Path Y(ε) = C(m* + εw)Λ for ε = 10⁻² … 10⁻⁸.
- **PASS:** each |Ω| grows ≥ 10³× while |Ω_A + Ω_B| changes < 10×.
- **FAIL:** the sum grows like the terms.
- 40-digit floats [SIMULATED].

**Answer to "do networks choose the tiling?":**
- **YES** if R1 passes: an n = 8-derived Ising rule predicts n = 10.
- **PARTIAL** if only R2 passes: the tiles are exactly the loop-free (tree) Ising networks, which is natural in Ising
  terms but is Perlstein–Tessler's ToT characterisation in Ising language.
- **NO** if neither passes.

**Optional Lean:** an exact point in each passing tile (orthogonality plus the vanishing consecutive minors).

## Self-review against the four demands

1. **Infrastructure:** the reset is handled and the lock re-applied. Sharing a box with other agents is a risk, so we
   commit WIP often.
2. **Methods:** exact up to rigorous interval enclosure (certified, not exact-algebraic, for nonzero signs).
   Non-shape-position or positive-dimensional cases are flagged, not guessed.
3. **Simulation:** Ising-law sampling only (uniform-in-m is infeasible), no second independent top network, and
   N ≈ 1000 gives a bound of about 0.3%.
4. **Process:** R1 is from n = 8 data; R2 is prior-art-informed (disclosed). The criteria are fixed above.
