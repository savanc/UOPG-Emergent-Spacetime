# M1b pre-registration: the Hermitian ↔ split slice bridge ("projection" rung)

Date: 2026-10-11 (Europe/London). Written and pushed before any M1b Lean or script. Context: `reviews/M1-result-2026-10-10.md`
(the positivity tension), `reviews/LADDER-REVIEW-2026-10-10.md` (kill #1 near-miss), `lean/PositiveGeometryEmergentSpaceTime/{Spinor,Klein}.lean`.

## Problem

Real Minkowski points are Hermitian X = σ(t,x,y,z) = [[t+z, x−iy],[x+iy, t−z]] (signature (1,3), M1). Gr⁺(2,4)
positivity lives on the real (2,2) slice. Does positivity do any work for real (1,3)?

## Prior art (sweep done; IDs checked unless marked)

- **Split signature as a computational device.** Witten, twistor string, hep-th/0312171 (real twistors ⇒ (2,2)).
  Atanasov–Ball–Melton–Raclariu–Strominger 2101.09591, "(2,2) Scattering and the celestial torus" (Klein space,
  analytic continuation from Minkowski). Arkani-Hamed–Trnka 1312.2007 (amplituhedron: real positive data, i.e.
  split or Euclidean regions, then continuation).
- **Real kinematics vs positivity.** Cachazo–Mizera–Zhang 1609.00008: the positive kinematic region K⁺_n has 4D
  kinematics "only in split signature"; Lorentzian needs λ̃ = ±λ̄, "not compatible with positivity". **This is the
  spinor-space form of the bridge question, already answered negatively.** Damgaard–Ferro–Łukowski–Parisi 1905.04216
  (momentum amplituhedron: real (2,2) spinors, positive planar Mandelstams). arXiv:2410.09574 (momentum amplituhedra
  ↔ origami, BCFW triangulation when planar Mandelstams ≥ 0; authors not checked). 2308.02438 (prescriptive
  unitarity from positive geometries, explicitly in R^{2,2}).
- **Euclidean region.** Five-point literature: "for five-point [one-mass] kinematics the Euclidean region (all
  ordered invariants negative) is not a physical region" (Abreu et al. 2005.04195). Physical-channel sign tables for
  massless five-point: Gehrmann–Henn–Lo Presti 1807.09812, Table 1. **So the n = 5 Euclidean no-go is known.** A
  general all-n, all-D statement with an elementary proof was not found stated.
- **Kinematic associahedron.** Arkani-Hamed–Bai–He–Yan 1711.09102: the region X_ij ≥ 0 lives on H_n
  (c_ij = −s_ij > 0, non-adjacent) in the space of Mandelstams. No real-momentum realisability is claimed.
- Lean: no formalisation of any of this found.

## Definitions (fixed now)

- Complex chart `chart X = [I | X]`, X ∈ M2(ℂ). Plücker vector p = (p01, p02, p03, p12, p13, p23)
  = (1, X10, X11, −X00, −X01, det X) (`Klein.chart_pl`).
- **Hermitian (1,3) real form:** X = Xᴴ, i.e. X = σ(v), v ∈ ℝ⁴. On Plücker space this is the antilinear involution
  τ(p) = (p̄01, −p̄13, p̄03, p̄12, −p̄02, p̄23). **Split (2,2) real form:** X ∈ M2(ℝ), i.e. X = σ(t, x, i y′, z),
  det = t² − x² + y′² − z².
- **Positivity:** Gr⁺ ⇔ ∃ λ ∈ ℂ*, all λ p_ij ∈ ℝ_{>0} (the column order 0 < 1 < 2 < 3 of the chart). Gr≥0: ℝ_{≥0},
  with λ p ≠ 0.
- **Kinematics:** real momenta in signature (1, D−1), mostly-minus, p_i null, Σ p_i = 0 (all incoming),
  s_ij = (p_i + p_j)². Planar variables X_{i,j} = (p_i + … + p_{j−1})². At n = 5 they are the five adjacent s_{i,i+1}.

## Bridges and pre-registered claims

- **(B1) no-go (expected PROVED).** (i) No Hermitian X has its chart Plücker vector in Gr⁺ (a stronger statement
  than "no open set"). (ii) The projective form: no τ-fixed (up to phase) Plücker vector is positive. (iii) Exactly
  which Hermitian X lie in Gr≥0 in the chart. My conjecture: X = diag(a, b) with a ≤ 0 ≤ b and ab = 0, i.e. two null
  half-rays in the (t, z) plane.
- **(B2) continuation.** The holomorphic data common to both slices: det (the complexified η) and the null quadric
  det = 0. The family X_w = σ_ℂ(t, x, w, z) (t, x, z real, w ∈ ℂ) contains Hermitian (w real) and split (w ∈ iℝ)
  points. Claim: X_w ∈ Gr⁺ in the chart ⇒ w ∈ iℝ with Im-part condition (expected y′ < −|x|, w = i y′). So positivity
  is reached *only* at the split end of a Wick rotation, never on the Hermitian or the common (1,2) slice (w = 0).
  Gr⁺ ∩ split is nonempty (explicit rational point) and lies in det > 0.
- **(B3) kinematic bridge.** In real (1, D−1) kinematics, any D:
  - n = 4: "all planar X > 0" (s, t > 0) is impossible; the Euclidean pattern s, t < 0 is realisable (explicit
    rational momenta).
  - n = 5: neither all five planar X > 0 nor all < 0 is realisable. So the interior of the M2c associahedron
    (in either metric sign convention) contains no real Lorentzian point.
  - n = 6: search for an all-Euclidean point (reported, no claim pre-registered).
  - In (2,2): explicit real-spinor n = 5 points with all planar X > 0 and with all < 0 (realisable, as in the
    momentum amplituhedron).
  - Lean: the null-cone lemma (same-sign null vectors have p·q ≥ 0) in D = 4; the odd-cycle alternation
    argument; the explicit configurations as exact arithmetic.

## Outcomes (fixed now)

- **PASS = a precise theorem establishing either a bridge or a no-go.** A no-go is a valid, informative result.
- **Kill criterion #1** (MISSION): "If [(1,3)] can only be obtained by dropping positivity …, positivity survives only
  as a statement about the particle layer or amplitudes, not about spacetime."
  - If B1 holds and B2 shows positivity only on the split end, the **second clause of #1 fires**: positivity is
    dead as a statement about spacetime points.
  - If B3 also shows that real Lorentzian kinematics cannot reach the planar-positive region (n = 5), positivity is
    not even a statement about *real* (1,3) momenta. It is a property of the analytically continued amplitude
    (Euclidean/split domains). Then the ladder must state this everywhere, and "positivity is fundamental" is
    re-tagged.
- **BRIDGE** (would revive spacetime positivity): a positivity notion on Hermitian X or on real Lorentzian planar
  kinematics that is nonempty-open and implies something proved. If found, record it as the bridge.
- **Not allowed:** changing the chart, the column order or the positivity notion after seeing results. Other orders
  and sign conventions may be reported as an addendum (B1 is expected to survive them, by the conjugate-pair
  argument).
