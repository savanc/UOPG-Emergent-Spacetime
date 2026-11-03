# H-T5b pre-registration: exact membership for the n = 8 Ising/BCFW tiling of the ABJM orthogonal momentum amplituhedron (OMA) (2026-10-12)

Written and pushed **before any result computing**. Gauge convention: the same as H-T3/H-T5. The verdict uses gauge G2
(odd columns = I, so the OG block is in O(k) and the measure is Haar). C comes from the GP map M ↦ M̃ (1807.03282
eq. 2.4) with η = diag(+,−,…). Λ is the moment curve at x = 1..8 in 6 dims, as in H-T5.

**Re-read gap disclosure.** We have already seen H-T5's output.
- Membership patterns on the 200 samples (cells ordered (4,6,7,1,8,2,3,5), (5,6,8,7,1,2,4,3), (5,7,6,8,1,3,2,4),
  (6,5,7,8,2,1,3,4)): (1,1,0,0) 44, (1,0,0,1) 30, (0,1,1,0) 29, (0,0,0,0) 26, (0,0,1,0) 21, (1,0,0,0) 19,
  (0,0,1,1) 17, (0,1,0,0) 11, (0,0,0,1) 3.
- So we expect the HW pair {cell0, cell2} and the cyclic pair {cell1, cell3} each to tile. That expectation is stated
  here so it cannot be fitted afterwards.
- We also already know (prior art) that HKWZ/HW claim the BCFW tilings.

## Method fitness (hard gate)

**Infrastructure.**
- The old `<local path>` has a broken pip (`pip._internal.operations.build` missing). It was **not** repaired.
- A fresh venv `<local path>` (Python 3.13.5) was created, with numpy 2.5.4, scipy 1.18.1, sympy 1.14.0 and mpmath
  1.3.0. These are locked in `requirements-lock.txt`.
- The box has 8 CPUs, 15 GB RAM (about 2 GB free because of other agents' browser processes), 103 GB disk, and no
  ulimit on CPU time.
- Sizing:
  - each sample needs one 8×6 exact rational linear solve, 70 minors of degree ≤ 4 in one variable, and root isolation;
  - target budget ≤ 1 s/sample, total ≤ 40 min;
  - memory is negligible (< 200 MB);
  - single process, so the shared box is not starved.

**Method: exact inverse, no iterative least squares.** Two structural facts make the inverse map exact:
1. The GP map sends *every* symmetric unit-diagonal M (6 entries m_ij) into OG(4,8). C(m) η C(m)ᵀ ≡ 0 was checked
   symbolically (method validation, not a result). The OG constraint is therefore automatic, and m is a global chart
   of the big cell.
2. For rational Y, let Y⊥ be the exact rational 6×2 kernel and λ̃ = Λ Y⊥ (8×2). Then Y = CΛ ⇔ C(m) λ̃ = 0. That is
   **8 linear equations in m**.

Expected rank: 5, which gives an affine line m(s) = m₀ + s v (the 1-dim fiber of the 6 → 5 map). The **fiber is
exact rational**. Any other rank is flagged *degenerate* and reported separately.

**Cell membership (certified).** The OG≥0 cells are positroid cells; OG≥0 = OG ∩ Gr≥0 on GP's positive branch.
1. For each of the four 5-dim cells τ, its zero set Z_τ of Plücker coordinates is computed exactly at a rational
   forward point of the cell's realising network (from H-T5).
2. Y is in cell τ iff some s* on the fiber has: all 70 maximal minors Δ_I(C(m(s*))) ≥ 0, Δ_I = 0 exactly for I ∈ Z_τ,
   and Δ_I > 0 for I ∉ Z_τ.
3. Candidate s* are the real roots of the gcd of the polynomials {Δ_I(s) : I ∈ Z_τ}. They are isolated with sympy
   (exact real root isolation).
4. Signs at s* are certified as follows:
   - Exact zero: the minimal polynomial divides Δ_I(s).
   - Nonzero: the sign comes from exact rational interval evaluation on an isolating interval refined until it
     excludes 0 (up to 200 bisections; anything else counts as *uncertified*).
5. **"In no cell" is declared only if certified exactly.** If any sign is uncertified, the sample is UNCERTIFIED.

**OG components and branches.** GP's M̃ parametrises one component of OG(4,8); positivity of all minors selects
OG≥0. The other component (one column-pair sign flip) cannot appear because our chart never leaves GP's component.
- A root s* where minors have mixed signs is "not in τ" (certified), not a branch failure.
- Roots are real algebraic numbers of degree ≤ 4. No square-root branch choice is needed because roots are kept
  exact (CRootOf).

**Validation before use (gate).** 40 forward points: rational t on each realising network give C, then Y. The inverse
must return the same C exactly, so the round-trip error is 0 in exact arithmetic (also printed at mp.dps = 40). The
inverse must also report the originating cell. Any failure stops the rung and the verdict is INCONCLUSIVE.

**Simulation design.**
- **R200 (blind rerun):** the H-T5 samples, reproduced from the same RNG seed and sequence. The edge weights
  t = tanh(e^u) are rationalised to denominators ≤ 10¹², so these are exact Y within ~10⁻¹² of the H-T5 points.
- **F-flip, 1000 fresh samples from the whole OMA, independent of Ising:**
  - Y = a random rational Gaussian 4×6 matrix (entries with denominator 1000), accepted iff the sign-flip definition
    holds (all ⟨Y i i+1⟩ > 0 with the twisted cyclic sign for ⟨Y 8 1⟩ checked on R200, and k = 4 flips in ⟨Y1j⟩);
  - then also required to satisfy momentum conservation;
  - a generic Y in Gr(4,6) is **not** in the 5-dim OMA (the OMA is codimension 3 in Gr(4,6)), so rejection on Gr(4,6)
    is impossible.
  - Replacement design, stated now: sample M uniformly from the box [−1, 1]⁶ and accept iff all 70 minors of C(M) are
    > 0 (an exact top-cell point, uniform in m rather than in Ising variables), with N = 1000. Y = C(M)Λ.
- **F-net:** 500 samples from networks N2 and N3, with t uniform on rationals in (0,1) (a different law from H-T5).
- **B (boundary, reported separately):** 100 samples with one t ∈ {10⁻⁶, 1 − 10⁻⁶}, plus 20 samples exactly on a
  5-dim cell (one t = 0), where we expect to find a fiber endpoint *at* that cell.
- **Coverage bound:** with zero certified "no cell" samples among N, the 95% upper bound on the uncovered fraction is
  3/N (rule of three; ≈ 0.3% for N = 1000).

## Criteria for (b)

Over non-degenerate, certified samples in R200 ∪ F-flip ∪ F-net:
- **PASS:** some pair {A, B} has every sample in exactly one of A, B, **and** {cell0, cell2} (HW σ1, σ2) or
  {cell1, cell3} (the cyclic shift) is such a pair.
- **FAIL:** no pair satisfies it, with a certified counterexample (a sample certified in both or in neither) for every
  pair.
- **INCONCLUSIVE:** no pair passes, but some pair's only counterexamples are uncertified or degenerate; or the
  validation gate fails.

Also reported: the full pattern counts, and the coverage bound per pair.

## (c) Canonical form / spurious poles (run only if (b) PASS)

**Top measure on the fiber.** The Lee/HW measure in the m-chart, gauge G2, is
f(m) d⁶m = ρ_H(m) d⁶m / Π_{i=1..8} M_i, where:
- ρ_H is the Haar density of O(4) pulled back through O = A(m)⁻¹ B(m) (A = odd columns, B = even columns), computed as
  the Riemannian volume factor of the bi-invariant metric;
- M_i are the consecutive minors of the gauge-fixed C.

**Tile forms.** The tile form at Y is Ω_τ(Y) = Res_{s=s_τ} f(m(s)) · J⊥(s) ds. Here J⊥ = |det[DΦ; vᵀ]|/|v|², and Φ
is a fixed 5-coordinate chart of the OMA: gauge-fixed Y entries (1,5), (1,6), (2,5), (2,6), (3,5). The chart is
checked nonsingular at each point. Evaluated at mp.dps = 40.

**Path test.** Take a point m* in a 4-dim common boundary of A and B (the tiling pair from (b)), obtained from a
realising network with two edges degenerated, plus a generic direction w. Set Y(ε) = C(m* + ε w)Λ for ε = 10⁻², …,
10⁻⁸.
- **PASS:** max |Ω_A|, |Ω_B| grows by ≥ 10³ over the ε range, while |Ω_A + Ω_B| changes by < 10× and stays bounded.
- **FAIL:** the sum grows like the individual terms.
- **INCONCLUSIVE:** the individual terms do not blow up (no spurious pole is seen on this path), or a numerical
  failure occurs.

**Optional Lean.** An exact n = 8 point in each HW cell (C η Cᵀ = 0, Y = CΛ), if cheap.

## Self-review against the four demands

1. **Infrastructure:** fixed by a fresh venv with locked versions. The remaining limit is the ~2 GB free RAM, which
   is fine at this size.
2. **Methods:** exact. Limits:
   - certification depends on positroid zero sets computed at one forward point per cell; a non-generic point could
     give extra zeros, so two points per cell are cross-checked;
   - (c) uses mp.dps = 40 floats (SIMULATED, not certified).
3. **Simulation:**
   - Sign-flip rejection on Gr(4,6) is infeasible (codimension 3), so "whole OMA" sampling uses uniform-in-m top-cell
     points. Their image is the whole OMA, but by the known image statement, not by sign flips.
   - The R200 points are within 10⁻¹² of H-T5's, not identical.
4. **Process:** criteria are fixed above, "no cell" only counts when certified, and the re-read gap is disclosed.
