# Pre-registration — M2c: the n = 5 kinematic associahedron

Date: 2026-10-10 (Europe/London). Committed **before** any M2c Lean, script or figure.
Branch: P-Pole ("derive the positive region from the physical poles", MISSION M2). Rules as before.

Source (PDF read 2026-10-10): N. Arkani-Hamed, Y. Bai, S. He, G. Yan, *Scattering Forms and the
Positive Geometry of Kinematics, Color and the Worldsheet*, arXiv:1711.09102 (JHEP05(2018)096).
Equation numbers below are theirs.

## 1. Statement (CITED)

- **Kinematic space.** Planar variables `X_{i,j} = (p_i + … + p_{j−1})²`; `X_{i,i+1} = X_{1,n} = 0`.
  For n = 5 the non-trivial ones are `X13, X14, X24, X25, X35` (dim K_5 = 5).
- **Positive region** Δ_n: `X_{i,j} ≥ 0` (eq. 3.4).
- **Subspace H_n** (eq. 3.5–3.6): `c_ij := X_{i,j} + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j} = −s_ij` is a
  positive constant for every non-adjacent `1 ≤ i < j ≤ n−1`. For n = 5: `c13, c14, c24 > 0`, so
  dim H_5 = 2. **A_n := H_n ∩ Δ_n** is claimed to be an associahedron.
- **n = 5 parametrisation** (eqs. 3.10–3.14), basis `(X13, X14)`:
  `X35 = −X14 + c14 + c24`, `X25 = −X13 + c13 + c14`, `X24 = X14 − X13 + c13`.
  (I re-derived these from 3.5 with X23 = X34 = X15 = 0; they agree.)
- **Canonical form = amplitude** (eqs. 3.20–3.21, 3.24):
  `Ω(A_5) = m_5 d²X`, with
  `m_5 = 1/(X13 X14) + 1/(X14 X24) + 1/(X24 X25) + 1/(X25 X35) + 1/(X35 X13)`,
  the tree-level bi-adjoint φ³ amplitude m(I_5|I_5) (sum over the 5 planar cubic diagrams).
- **Factorisation** (eq. 4.3/4.10): `Res_{X_ij=0} Ω(A_n) = Ω(A_L) ∧ Ω(A_R)`. For n = 5 each facet is a
  segment A_4 × A_3 (A_3 a point), so the residue is the 4-point amplitude `1/s + 1/t` (eq. 3.22).
- **Soft limit** (eq. 4.11): `c13, c14 → 0` forces `X13 + X25 → 0`, squashes A_5, and m_5 → 0 on H.
- **Triangulation** (eq. 5.13, Fig. 17): ABHY's own check via 3 triangles from vertex A.
- **n = 6:** A_6 is a 3D associahedron (Fig. 8). Combinatorially 14 vertices (Catalan C_4) and
  9 facets (diagonals of a hexagon).

## 2. Targets

(a) **Pentagon.** Coordinates `x = X13, y = X14` on H, `c13, c14, c24 > 0`.
  - The five X's are affine in (x, y) (definitional).
  - Predicted vertices (counter-clockwise), each the meeting of two **compatible** (non-crossing) chords:
    `v1 = (0,0)` [X13=X14=0], `v2 = (c13,0)` [X14=X24=0], `v3 = (c13+c14, c14)` [X24=X25=0],
    `v4 = (c13+c14, c14+c24)` [X25=X35=0], `v5 = (0, c14+c24)` [X35=X13=0].
  - Lean: each v_k lies in the region and has exactly its two X's zero; any region point with two
    distinct X's zero is one of the v_k and the pair is cyclically adjacent in (X14, X24, X25, X35, X13);
    the 5 crossing pairs never vanish together in the region; each facet `X_ij = 0` meets the region in
    the segment between its two vertices. So: exactly 5 vertices, 5 edges, adjacency = compatibility.
(b) **Canonical form identity.** Independent definition: Ω(P) by fan triangulation from v1 with the
  standard simplex formula in affine brackets `⟨Y Z_i Z_j⟩` (projective-simplex canonical form,
  ABHY App. A eq. A.21 / Arkani-Hamed–Bai–Lam). Lean: `Ω_fan = m_5` as a rational identity
  (`field_simp; ring`), on the open region minus the two spurious diagonals.
  Residues: for each facet F, `X_F · m_5 = (two-term 4-pt amplitude on F) + X_F · (regular)`
  (multiplied-out identity, all 5 facets) and, for X13, the limit statement
  `X13 · m_5 → 1/X14 + 1/X35` as X13 → 0 (a genuine `Filter.Tendsto`).
(c) **Positivity doing work.**
  - If `c14 + c24 < 0` or `c13 + c14 < 0`: region empty.
  - All c = 0: region = the single point (0,0) (degenerate; no 2D canonical form).
  - `c13 < 0` (with c13+c14 > 0, c14+c24 > 0): `X14 > 0` on the whole region, so the facet X14 = 0 is
    missing; the region is a quadrilateral whose canonical form **differs** from m_5 (script, exact).
  - Soft limit: m_5 vanishes identically on H when `c13 = c14 = 0` (Lean, eq. 4.11).
(d) **Stretch.** By `decide` (no `native_decide`): number of triangulations (maximal sets of pairwise
  non-crossing diagonals) of the pentagon = 5, hexagon = 14; hexagon diagonals = 9. Vertex/facet
  counts of A_6 are then CITED via ABHY's vertex ↔ triangulation correspondence, not re-proved
  geometrically.

## 3. Script `scripts/m2c_associahedron_check.py` (exact `fractions.Fraction`)

For ≥ 20 random positive `(c13, c14, c24)` and ≥ 5 random interior points each:
1. vertices computed independently by intersecting all 10 pairs of lines `X = 0` and keeping
   feasible points → must be exactly the 5 predicted, with compatible pairs;
2. Ω via (i) fan triangulation from v1, (ii) fan from v3 (different triangulation), (iii) ABHY eq. 5.13
   triangle formulas → each must equal m_5 **exactly**;
3. residues: `X_F · m_5` evaluated at X_F = 0 (exact substitution on the facet line) equals the
   facet's 4-pt amplitude, all 5 facets;
4. counterexample `c13 < 0`: polygon has 4 vertices; its canonical form ≠ m_5 at interior points.
Figure: `figures/m2c-pentagon.png` — the pentagon in the (X13, X14) plane, facets labelled X_ij = 0,
vertices labelled by their planar cubic diagram (pair of propagators).

## 4. Pass / fail

**PASS** iff: Lean (a), (b) (identity + residues), (c) compile, axioms only
`propext, Classical.choice, Quot.sound`, no `sorry`/`native_decide`; and the script's exact checks 1–4
all hold. **FAIL** if the canonical-form identity or any residue fails, or the counterexample behaves
otherwise than predicted. (d) is stretch; not finishing it is reported, not a failure.

What PASS would show: for a toy scalar theory (bi-adjoint φ³, tree level, n = 5), a positive
geometry produces a real amplitude, with **locality** (poles only at X = 0 facets) and **unitarity /
factorisation** (residues = lower amplitudes) read off the boundary. Not the Standard Model; no data.
