# Pre-registration — M2b: the EFT-hedron's first non-linear bound

Date: 2026-10-10 (Europe/London). Committed **before** any M2b Lean code, script or figure.
Branch: P-EFT (continues M2). Rules as M1/M2: Mathlib/Physlib first with credit; no `sorry`,
no `native_decide`, no custom axioms; every number and citation checked from the source.

## 0. What M2 left open

M2 proved the *linear* statement: a positive spectral density forces the forward curvature
`A''(0) ≥ 0` (PositiveGeometryEmergentSpaceTime/Dispersion.lean). Linear positivity of single coefficients is only the
first face of the EFT-hedron. M2b targets the first **non-linear** face: the 2×2 Hankel
(Cauchy–Schwarz) inequality `f0·f2 ≥ f1²`, plus the gap (support) inequality.

## 1. Statement (CITED; normalisation fixed here)

Sources, checked from the papers (PDF/HTML read 2026-10-10):
- Bellazzini, Elias Miró, Rattazzi, Riembau, Riva, *Positive Moments for Scattering Amplitudes*,
  arXiv:2011.00037 — arcs eq. (2)–(3), moment form eq. (7), Hankel conditions eqs. (16)–(19),
  the A(2) region eq. (20), tree-level match `a_n = c_{2n+2}` eq. (30), finite-resonance
  arcs eq. (33), loop caveats §II.2 (incl. eq. (48): the tree-level determinant can go
  negative from RG running).
- Arkani-Hamed, Huang, Huang, *The EFT-Hedron*, arXiv:2012.15849 — Hankel matrix eq. (6.29)
  ("totally positive", Stieltjes half-moment problem), 3×3 determinant eq. (6.28), gapped
  constraints §7 (eq. (7.45) neighbourhood), type-I forward coefficients `a_{k,0} = ζ(k+2)` eq. (3.11).
- Adams, Arkani-Hamed, Dubovsky, Nicolis, Rattazzi, hep-th/0602178 — type-I forward limit
  `M(s,t→0) → s tan πs` eq. (27); type-II Regge part eq. (64).
- Caron-Huot & Van Duong, *Extremal Effective Field Theories*, arXiv:2011.02957 (JHEP05(2021)280)
  — semidefinite carving of a light real scalar's EFT space with mass gap M. **Correction to the
  brief:** from its abstract it is a single-real-scalar study, not a pion-data application, so it
  is cited for "two-sided bounds / gap M", not for a pion comparison.

**Setup (massless, s↔u symmetric, tree-level-matched, forward t = 0).** The low-energy forward
amplitude is `A(s) = c0 + c2 s² + c4 s⁴ + c6 s⁶ + …` (only even powers by s↔u crossing). With
analyticity, crossing, `A/s² → 0` (Froissart-type) and `Im A ≥ 0` (optical theorem) as
HYPOTHESES (CITED, not proved), Bellazzini et al. eq. (3) with ŝ → 0 gives

    f_k := c_{2k+2} = (2/π) ∫_{M²}^∞ ds' Im A(s') / s'^{2k+3}      (k = 0, 1, 2, …)

**Normalisation we commit to.** Change variable `x = 1/s'²` and set
`dμ(x) = (1/π) Im A(1/√x) dx` (Bellazzini eq. (7) at ŝ = 1). Then

    f_k = ∫ x^k dμ(x),   μ ≥ 0,   supp μ ⊂ (0, 1/M⁴].

Note: the brief wrote `x = 1/s'` and `1/M²`. That is the *s-channel-only* (colour-ordered,
EFT-hedron §3) convention, where every power of s appears. For the s↔u-symmetric forward
amplitude the natural variable is `x = 1/s'²`, so the gap is `1/M⁴`. Both conventions are
"moments of a positive measure on a bounded interval"; the math theorems below are stated for
an arbitrary bound `xmax`, so they cover both. Toy T4 uses the colour-ordered convention.

**Target inequalities.**
- (H2) `f0·f2 ≥ f1²`, equivalently `[[f0,f1],[f1,f2]]` is positive semidefinite.
- (H3) `[[f0,f1,f2],[f1,f2,f3],[f2,f3,f4]]` PSD (so its determinant ≥ 0, EFT-hedron eq. (6.28)).
- (G)  gap/support: `f_{k+1} ≤ xmax · f_k`, i.e. `c_{2k+4} M⁴ ≤ c_{2k+2}` (Bellazzini eq. (6)/(31)).
- Dimensionless region plotted: `u = f1/(xmax f0)`, `v = f2/(xmax² f0)`; A(2) (Bellazzini eq. (20))
  is `u² ≤ v ≤ u`, `0 ≤ u ≤ 1`. Lower edge = moment-curve parabola `v = u²` (single-resonance
  theories); upper edge = gap line.

## 2. Is a pion-data check meaningful? Decision: **NO data check in M2b**

Reasons, stated before looking at any numbers:
1. H2 needs the forward s², s⁴ **and s⁶** coefficients of ππ. The s⁶ term is O(p⁸) in ChPT; no
   controlled phenomenological value of the O(p⁸) forward coefficient is available to me with a
   citable uncertainty. (CGL 2001 give O(p⁶) quantities, not O(p⁸).)
2. Pion loops: below the cutoff the forward amplitude has `s⁴ log s` etc. The quantities that obey
   the moment conditions are the **arcs** a_n(ŝ), not the Lagrangian c_n; Bellazzini §II.2 shows
   the naive tree-level determinant `c2 c6 − c4²` can be negative in a consistent theory (eq. (48)).
   A naive "measured c's in the Hankel matrix" test would be wrong in principle.
3. Massive pions: the cut starts at 4m_π² and the crossing variable is ŝ = s − 2m²; computing the
   arcs needs the full two-loop amplitude plus Roy-equation input above threshold. That is a
   separate project, not a cheap check.

So M2b is pre-registered as **math (Lean) + toy UV completions**. This tests our derivation and
transcription, not nature. It does not test the M2 kind of QFT axioms against new data.

## 3. Toy checks (script `scripts/m2b_hankel_check.py`, mpmath, ≥ 50 digits)

Each must satisfy H2, H3 and G with the stated xmax. Truly positive UV completions:
- **T1 single heavy scalar / linear σ-model** (Bellazzini fn. 5): `c_{2n} = λ/m_h^{2n}` → one delta at
  `x = 1/m_h⁴`. Predicted: H2 and G **saturated** (equalities); the point is (u,v) = (1,1).
- **T2 type-I forward, `s tan πs`** (Adams eq. (27)), α' = 1. Poles at s² = (n+½)²; lowest
  M² = ½ so xmax = 4. f_k = Taylor coefficient of s^{2k+2}, k = 0…4, computed both from the series
  of tan and from the explicit partial-fraction measure (cross-check).
- **T3 type-II Regge part** (Adams eq. (64)): coefficients `−ψ2(1), −ψ4(1)/192, −ψ6(1)/92160`
  of s⁴, s⁶, s⁸ form the shifted sequence (f_k = c_{2k+4}, still a moment sequence). Lowest massive
  pole s = 4 → xmax = 1/16. Only 3 coefficients are quoted, so H2 and G only (no H3).
- **T4 type-I colour-ordered** (EFT-hedron eq. (3.11)): `a_k = ζ(k+2)`, s-channel convention,
  x = 1/n, xmax = 1. H2, H3, G for k = 0…4.

Deliberate non-positive cases (must **violate** at least one of H2/G):
- **C1 signed measure** `μ = δ_{1/2} − ½ δ_1`: f0 = ½, f1 = 0, f2 = −¼ ⇒ f0 f2 = −1/8 < 0 = f1².
- **C2 "super-soft" amplitude** `A = c4 s⁴` with c2 = 0, c4 > 0 (Bellazzini §II.1, (∂∂φ)⁴):
  f0 = 0, f1 = c4 > 0 violates G (`f1 ≤ xmax f0`).

## 4. Lean targets (file `lean/PositiveGeometryEmergentSpaceTime/Hankel.lean`)

- (La) measure version: for a finite measure μ on ℝ with x, x² integrable,
  `(∫ x dμ)² ≤ (μ univ).toReal · ∫ x² dμ`.
- (Lb) the 2×2 Hankel matrix of (La) is `Matrix.PosSemidef` (Mathlib definition).
- (Lc) discrete, any size n: for `w_i ≥ 0`, the n×n Hankel matrix `H_ij = Σ_l w_l x_l^{i+j}` is
  `PosSemidef`; hence (Mathlib `PosSemidef.det_nonneg`) the 3×3 determinant is ≥ 0. Gap: support in
  [0, xmax] ⇒ `f_{k+1} ≤ xmax · f_k` (discrete and measure).
- (Ld) exact rational toys: a concrete positive 3-delta measure satisfies H2, H3, G by `norm_num`;
  C1 violates H2; and therefore (contrapositive of Lc) **no** positive weights reproduce C1's
  moments — positivity is doing the work.
- (Le) link to M2: the M2 curvature (Dispersion.lean) is itself a moment `f`-type integral of the
  same positive density; state it as a theorem if cheap, otherwise document the identity.

## 5. Pass / fail rule

**PASS** iff all of:
1. (La), (Lb), (Lc incl. 3×3), (Ld) compile with no `sorry`/`native_decide`; `#print axioms` shows
   only `propext`, `Classical.choice`, `Quot.sound`.
2. Every positive toy T1–T4 satisfies H2, G (and H3 where available) to the working precision
   (violation tolerance: relative 1e-40); T1 saturates H2 and G to that precision.
3. Each of C1, C2 violates at least one inequality.

**FAIL** if any positive toy violates an inequality beyond tolerance (that would mean a transcription
or derivation error, or a false citation), or if a counterexample passes (then the inequality isn't
testing positivity). (Le) is not required for PASS. Stretch items that are not finished are reported
as open, not as failures.

What a PASS shows: the first non-linear face of the EFT-hedron follows from Im A ≥ 0 alone (a
moment/Cauchy–Schwarz fact), and known UV-complete amplitudes sit inside the region. What it does
**not** show: anything about pion data, our Gr⁺ geometry, or nature.
