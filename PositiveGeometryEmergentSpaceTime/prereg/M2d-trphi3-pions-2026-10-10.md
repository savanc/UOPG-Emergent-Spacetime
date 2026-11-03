# Pre-registration — M2d: from Tr(φ³) to pions (the δ-shift)

Date: 2026-10-10 (Europe/London). Committed **before** any M2d Lean, script or figure.
Branch: P-Pole, continued from M2c. Rules as before: no `sorry`, no `native_decide`, no custom axioms;
reuse Mathlib first; every equation below was read in the PDFs on 2026-10-10.

**Disclosure.** Before writing this file I read the papers and did two short hand calculations (the n = 4
example, which the paper prints, and the leading large-δ term of the shifted n = 5 amplitude, used in
target (c)). No script, Lean or figure work has been done.

## 0. Sources: which paper says what (verified)

- **[H]** N. Arkani-Hamed, Q. Cao, J. Dong, C. Figueiredo, S. He, *Hidden zeros for particle/string
  amplitudes and the unity of colored scalars, pions and gluons*, arXiv:2312.16282. The title and five
  authors match the brief. **Hidden zeros and near-zero factorisation are here** (§3: eqs. 3.1–3.7, Figs. 5–7).
  So is the **NLSM** in the Cayley parametrisation (§4: eq. 4.1 Lagrangian, eq. 4.2 vertices, **eq. 4.3 the
  6-pion amplitude**, eq. 4.4 the 4-pion zero, eqs. 4.5–4.6 factorisation). The δ-shift appears only at
  the **stringy** level (§7, eq. 7.13 with α′δ ∈ (0,1)).
- **[N]** same five authors, *NLSM ⊂ Tr(φ³)*, arXiv:2401.05483. This is the **field-theory δ → ∞ statement**
  we test (§I, eqs. 1–2):
  - shift `X̃_ij = X_ij + δ_ij`, with `δ_{e,e} = −δ_{o,o} = δ` and `δ_{o,e} = 0` ("e/o" = even/odd label);
  - this leaves every `c_ij = X̃_ij + X̃_{i+1,j+1} − X̃_{i,j+1} − X̃_{i+1,j}` unchanged (eq. 1), so the zeros survive;
  - `lim_{δ→∞} δ^{2n−2} A^δ_{2n}(X̃) = A^NLSM_{2n}(X)` for 2n particles (eq. 2), with f_π² = δ;
  - the worked example `δ² (X13+X24)/((X13−δ)(X24+δ)) → −(X13+X24) = A^NLSM_4`.
- **[AF]** N. Arkani-Hamed, C. Figueiredo, arXiv:2403.04826 (*Circles and Triangles, the NLSM and Tr(Φ³)*).
  This is the reverse-direction proof. CITED only; it is not used for any target.
- **[ABHY]** arXiv:1711.09102 (M2c). Data and LO theory: **[W]** S. Weinberg, PRL 17 (1966) 616. **[CGL]**
  G. Colangelo, J. Gasser, H. Leutwyler, Nucl. Phys. B603 (2001) 125, hep-ph/0103088 (eq. 1.2 LO formulae;
  eq. 11.2 `a0⁰ = 0.220 ± 0.005`, `a0² = −0.0444 ± 0.0010`; eq. 12.2 chiral series `a0⁰ = 0.159 → 0.200 → 0.216`,
  `a0² = −0.0454 → −0.0445 → −0.0445`; uses M_π = M_π± and F_π = 92.4 MeV). **[NA48]** J. R. Batley et al.
  (NA48/2), Eur. Phys. J. C70 (2010) 635, doi:10.1140/epjc/s10052-010-1480-6, Ke4 result:
  `a0⁰ = 0.2220 ± 0.0128_stat ± 0.0050_syst ± 0.0037_th`, `a0² = −0.0432 ± 0.0086_stat ± 0.0034_syst ± 0.0028_th`.
  I read these numbers from the journal abstract, not the full PDF.
- Kampf–Novotný–Trnka (arXiv:1304.3048) is the brief's suggested 6-pt reference. I use [H] eq. 4.3 instead
  (same Cayley parametrisation, written in X variables), plus an **independent** check from [H] eq. 4.2
  Feynman rules (see (b)).

**Correction to the brief.** The brief says odd-n amplitudes "vanish in the limit". The sources do not say
this. NLSM has no odd-point amplitudes. Shifted odd-point Tr(φ³) gives *mixed* pion + scalar amplitudes
([H] §4.2 eq. 4.6; [N] §IV). For odd n the shift also cannot preserve every c_ij ([H] §7 discussion).
Target (c) below is rewritten to test what the papers actually claim.

## 1. Conventions

Labels 1..n, planar `X_ij` with `X_{i,i+1} = X_{1,n} = 0`, `c_ij` as above with indices mod n (`X_ij = X_ji`).
Massless: `X13 = s = (p1+p2)²`, `X24 = t = (p2+p3)²`.
- n = 4: X13 is (o,o) → `X13 − δ`; X24 is (e,e) → `X24 + δ`.
- n = 5: X13, X35 are (o,o) → −δ; X24 is (e,e) → +δ; X14, X25 are (o,e), unshifted.
- n = 6: (o,o) = X13, X15, X35 → −δ; (e,e) = X24, X26, X46 → +δ; (o,e) = X14, X25, X36, unshifted.

## 2. Targets

(a) **n = 4.** `δ² A4(X̃) → −(X13 + X24)` as δ → ∞, where `A4 = 1/X13 + 1/X24`. Lean: a genuine
  `Filter.Tendsto … atTop` (LIMIT). Also the algebraic statement `A4^NLSM = X13+X24 = c13` (COEFFICIENT/IDENTITY).
(b) **n = 6.** `lim δ⁴ A6(X̃) = σ · A6^NLSM`, where A6 = the 14 planar cubic diagrams and A6^NLSM is [H] eq. 4.3:
  `(X13+X24)(X15+X46)/X14 − X13 − X24` + its images under i → i+2. Exact rational-function identity for
  the limit. Prediction: **σ = +1**. Reasoning: the overall sign of a 2n-point NLSM amplitude flips as
  (−1)^{n−1} under λ² → −λ², and n = 4 has the opposite sign between [N] and [H]. The target is met if
  the identity holds with σ = ±1 exactly. A wrong σ prediction is recorded as a miss on the convention
  argument. Independent check (script): build the 6-pion amplitude from [H] eq. 4.2 Cayley vertices
  (three V4·V4 exchanges on X14, X25, X36 plus V6), using off-shell dot products, and compare with eq. 4.3
  up to one overall normalisation fixed at n = 4. Lean: the limit as a `Tendsto`, if `field_simp`/`ring`
  can carry it. Otherwise a cleared-denominator polynomial identity, clearly labelled.
  Also O(δ⁻¹), O(δ⁻²) and O(δ⁻³) all cancel (the "non-trivial" claim in [N] after eq. 2).
(c) **n = 5, odd (rewritten).** Predictions from my hand calculation, in the [N] shift convention:
  `δ · A5(X̃) → 0` (the O(δ⁻¹) parts cancel in pairs), and
  `δ² A5(X̃) → L5 := 1 − (X13+X24)/X14 − (X24+X35)/X25`. L5 has poles only at the (o,e) chords X14 and X25.
  It is dimensionless (X⁰), matching the [N] counting X^{3−nΦ} for a mixed amplitude with 3 scalars and
  2 pions. So it is **not** a 5-pion amplitude. Of the five c's, the shift changes only `c14` (by −δ).
  Lean: both limits. Script: the c-shifts. I identify L5 with a specific mixed amplitude only as far as the
  script's soft-limit scan supports; I do not prove it.
(d) **Hidden zeros.** In the full 5-dimensional kinematic space (free X13, X14, X24, X25, X35), with
  `c13 = X13+X24−X14`, `c14 = X14+X25−X24`, `c24 = X24+X35−X25`, `c25 = X25+X13−X35`, `c35 = X35+X14−X13`:
  m5 = 0 on each of the five skinny-rectangle loci {c13,c14}, {c24,c25}, {c35,c13}, {c14,c24}, {c25,c35}
  ([H] §3.1.1: "pick i, set c_ij = 0 for all j non-adjacent to i"). M2c proved only {c13,c14}, and only on H.
  Near-zero factorisation: `c14 = 0 ⇒ m5 = (1/X13+1/X25)(1/X14+1/X35)` ([H] eq. 3.3) and
  `c13 = 0 ⇒ m5 = (1/X13+1/X25)(1/X24+1/X35)` ([H] eq. 3.5). NLSM inherits the zeros:
  `A4^NLSM = c13` vanishes at c13 = 0 ([H] eq. 4.4), and A6^NLSM vanishes on the skinny rectangle
  {c13, c14, c15} = 0 and its cyclic images. Shifted A6(X̃) vanishes on the same loci at finite δ. All in
  Lean, with nonzero-denominator hypotheses stated. For n = 5 the shifted A5 keeps exactly the zeros
  that avoid c14 (script).
(e) **Adler zero.** In X variables, p1 → 0 sends `X13 → 0`, `X26 → 0`, `X14 → X24`, `X15 → X25`, and leaves
  the rest unchanged. Then A6^NLSM = 0 identically (Lean identity), and A4^NLSM = X13 + X24 → 0. Tr(φ³) m5
  is not expected to have this property, because its 1/X13 pole blows up.

## 3. Connection to data (stated honestly)

The geometry produces only a **massless, flavour-ordered** amplitude `∝ (X13 + X24) = s + t`, with f_π² = δ a
free scale. Two checks:
- **D1 (structural, yes/no).** Dress the ordered 4-pt amplitude with SU(2) traces
  (`Tr(σaσbσcσd) = 2(δabδcd − δacδbd + δadδbc)`), sum the 3 inequivalent orderings with their reflections,
  and use s + t + u = 0. The predicted result is `M^{abcd} = κ[s δabδcd + t δacδbd + u δadδbc]` for one
  constant κ. That is Weinberg's chiral-limit amplitude A(s,t,u) ∝ s. The sign and size of κ are fixed by
  convention and F_π (input), not predicted. PASS = yes.
- **D2 (LO scattering lengths; not blind).** The pion mass is **not** in the geometry. Weinberg's mass
  insertion `A = (s − M²)/F²` is an **input**, and so are F_π = 92.4 MeV and M_π = 139.57 MeV (the CGL
  choices). It gives `a0⁰ = 7M²/(32πF²)` and `a0² = −M²/(16πF²)` (computed from the isospin projections
  T⁰ = 3A(s,t,u)+A(t,s,u)+A(u,t,s), T² = A(t,s,u)+A(u,t,s) at threshold, a = T/(32π)), compared with
  NA48/2 Ke4 (errors added in quadrature).
  **Tolerance: |LO − measured| ≤ 30% of |measured|, for each of a0⁰ and a0².** Justification: the LO
  truncation error is set by the chiral series. CGL eq. 12.2 shows LO → NNLO moving a0⁰ by +36% of its LO
  value (≈ 26% of the final value). This tolerance is *informed by known literature*, so D2 is a
  consistency check, not a discriminating test. Any LO chiral Lagrangian passes it, whatever its origin.
  The ratio a0²/a0⁰ = −2/7 is reported but not graded.

## 4. Pass/fail

- **PASS** if (a), (b) (identity with σ = ±1), (c) (both limits), (d) and (e) hold in Lean/script exactly, the
  Feynman-rule cross-check of eq. 4.3 agrees, D1 = yes, and D2 is within tolerance. Everything compiles with
  only propext / Classical.choice / Quot.sound.
- **FAIL** if any limit or identity is false, eq. 4.3 disagrees with the Feynman-rule computation, D1 = no,
  or D2 is outside tolerance. Partial results are reported as such. If a Lean target is too heavy, it is
  downgraded to SIMULATED (exact sympy), with the reason stated.
- **Kill-criteria watch.** Is anything fitted? F_π and M_π are inputs used only in D2, and labelled as such.
  Does any step rest on "all is one"? No.

## 5. What a PASS would and would not mean (written in advance)

It would mean that the same positive-geometry function (M2c's canonical form), deformed by a fixed shift,
reproduces the leading-order pion amplitude, its zeros and its Adler zero. That is the first contact of the
chain with a real particle's low-energy scattering, at LO. It would **not** derive the shift (an input rule,
motivated in [H]/[AF]), the pion mass, F_π, any GeV value, loops (beyond citing [N]), or anything about
fundamental SM particles. Pions are composite Goldstone bosons.
