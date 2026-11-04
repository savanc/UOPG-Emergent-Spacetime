# Pre-registration: M2f, a mass shift for Weinberg's s − M²

Date: 2026-10-10 (Europe/London). Committed and pushed **before** any M2f script, Lean file or figure exists.
Approved by the author. Rules as before: honest tags; no `sorry`/`native_decide`/custom axioms; exact arithmetic only.
Builds on M2d (`lean/PositiveGeometryEmergentSpaceTime/NLSM.lean`, the δ-limits) and M2e (`ShiftForced*.lean`).

**Disclosure.** While reading the prior art (below) I worked out the n = 4 expectation by hand: a constant offset μ
on X13, X24 turns −(X13 + X24) into −(X13 + X24 + μ13 + μ24). That one line is written down here as a prediction.
No script, CAS or Lean has been run for M2f.

## 0. Prior art (rung protocol, step 1). Swept 2026-10-10 before writing this file

Papers opened and read (PDF text, the relevant sections):

- **[N] arXiv:2401.05483** (Arkani-Hamed, Cao, Dong, Figueiredo, He, *NLSM ⊂ Tr(Φ³)*, v3). The brief's "eq. 8" is
  verified. In §III, after the χ/ϕ colour-line rule (eq. 7: X_(χ,ϕ),(χ,ϕ) − δ, X_(χ†,ϕ̃),(χ†,ϕ̃) + δ, mixed unshifted),
  **eq. 8** is the general kinematic shift X_(χ,ϕ),(χ,ϕ) → X + m²_ϕ, X_(χ†,ϕ̃),(χ†,ϕ̃) → X + m²_ϕ̃,
  X_(χ,ϕ),(χ†,ϕ̃) → X + m²_χ. It "produces amplitudes for our cubic Lagrangian with general masses for ϕ, ϕ̃ and χ".
  Pure Goldstone scattering puts χ on odd legs and χ† on even legs, so (o,o) ↔ m²_ϕ, (e,e) ↔ m²_ϕ̃,
  (o,e) ↔ m²_χ. The massless NLSM is m²_ϕ = −δ, m²_ϕ̃ = +δ, m²_χ = 0, and §III notes m²_ϕ + m²_ϕ̃ = 0 is what
  lets the cubic theory non-linearly realise U(N). [N] uses a sign convention in which a massive propagator is
  1/(X + m²) (mostly-plus). [N] does **not** discuss a Goldstone (pion) mass, Weinberg's s − M², ChPT's mass
  term or scattering lengths. [CITED]
- **[H] arXiv:2312.16282** §7 (the stringy δ-shift; eq. 7.16–7.17 at n = 4; "the mass of X_e,e is minus that of
  X_o,o", otherwise "closer to φ⁴"). Massless pions only. [CITED]
- **[AF] arXiv:2403.04826** (*Circles and Triangles*, JHEP 09 (2025) 189). Massless only. [CITED]
- **[CGW] arXiv:2601.16860**, M. Carrillo González and F. Ward, *Hidden Zeros in Massive Theories* (Jan 2026;
  published as Phys. Rev. D, doi:10.1103/9wbw-9jxb). **This is the closest prior art, and it largely anticipates
  the core of M2f.** Mostly-minus signature. Results:
  - Uniformly massive Tr Φ³: with X̃_ij := X_ij − m² (eq. 10), X̃_{i,i+1} = 0, and c̃_ij = c_ij (eq. 12), all hidden
    zeros and factorisations carry over. The 4-point zero sits at s13 = 2m² (eq. 13).
  - A naive mass term −m² Tr(π²)/2 spoils the zeros: eq. 24 gives A[1234] = (1/2F²)(c13 − (2/3)m²) in the
    exponential parametrisation.
  - The **spurion** potential L_pot = (F²m²/4) Tr(U + U† − 2) (eq. 26; the standard LO ChPT mass term with uniform
    spurion M = m²·1) gives "mNLSM". Eq. 28: A4 = −(s13 − 2m²)/(2F²) = c13/(2F²), with c13 = X̃13 + X̃24. Eqs. 29–35
    (minimal parametrisation, Catalan-number vertices) show **all mNLSM tree amplitudes are the massless NLSM
    amplitudes with X → X̃**, so the hidden zeros are inherited.
  - "For mNLSM we no longer have the Adler zero, instead having in the leading-order soft limit some non-vanishing
    constant controlled by … m", fixed by PCAC (§V.B.4).
  - Footnote 6: the one-dimensional kernel of the c-equations "is equivalent to the δ-shifts of [9]".
  - App. B computes A6^mNLSM by a hidden-zero recursion.
  - I found **no** statement in [CGW] that composes this with the δ-limit of [N], and nothing about scattering
    lengths or data. [CITED]
- **Jagadale and Laddha, arXiv:2206.07979**, *Towards positive geometries of massive scalar field theories*
  (cited by [CGW] for the massive associahedron as the massless one translated by m²). Title and authors checked
  on arXiv; I have not read the body. [CITED, abstract level]
- **Paranjape, Skowronek, Spradlin, Volovich, arXiv:2504.11253** (*Large deformations of Tr(Φ3) and the world at
  infinity*, g-vector shifts generalising the δ-shift). Massless external pions; the "massive legs" there are
  internal sub-diagram momenta, not pion masses. [CITED]
- **Jones and Paranjape, arXiv:2505.02520** (JHEP 07 (2025) 251), smooth splitting from recursion; massless. [CITED,
  abstract level]
- **Knecht, Moussallam, Stern, hep-ph/9411259** (*The ππ amplitude in generalised ChPT*), eq. 1: at O(p²),
  A(s|t,u) = (β/F²)(s − 4M²/3) + αM²/(3F²) + O(p⁴). Standard ChPT is α = β = 1, i.e. Weinberg's (s − M²)/F².
  (The PDF text extraction lost the Greek letters. α and β are identified from the structure and the standard
  usage of this formula.) [CITED]
- Weinberg, PRL 17 (1966) 616 (LO ππ). CGL 2001 (hep-ph/0103088) and NA48/2 (EPJC 70 (2010) 635), as in M2d. [CITED]
- **Searches with no hit:** arXiv/web searches for "massive NLSM / pion mass / chiral perturbation theory /
  surfaceology / curve integral / scalar-scaffolded" × "Tr(φ³) / δ-shift", 2024–2026. Apart from [CGW], the only
  massive surfaceology work found is massive Tr φ³ curve integrals used as an IR regulator (arXiv:2503.07707).
  *The arXiv API query timed out; the searches went through the web index, so coverage is good but not exhaustive.*
- **Lean/Coq/Isabelle:** GitHub code search ("NLSM", Lean), Mathlib and Physlib (grep: pion, chiral, sigma model,
  amplitude). Nothing on NLSM, ChPT or Tr φ³ amplitudes; the "amplitude" hits in Physlib are about wave
  amplitudes in condensed matter. No formalisation found.

**New versus prior, claimed in advance:**

| Item | Status |
|---|---|
| Massive NLSM with the standard (spurion) mass term = massless NLSM at X̃ = X − M², all n, tree | **prior art** [CGW] eqs. 26–35 |
| NLSM = δ-limit of Tr φ³ | prior art [N] eq. 2 (our Lean limits: M2d) |
| The general mass deformation of the shift | prior art [N] eq. 8 |
| ⇒ δ-limit of the **uniformly massive** Tr φ³ = massive NLSM; Weinberg's s − M² at n = 4 | **immediate corollary** of [N] + [CGW]. Not found stated explicitly. We claim only the explicit statement, the [N]-eq.-8 parameter identification and the Lean proof, **not a discovery** |
| Independent n = 6 check of [CGW]'s X → X̃ claim with a *different* parametrisation (Cayley) | new as a cross-check (SIMULATED) |
| Classification of constant offsets: what the shift ansatz allows (a one-parameter s − c family), and which condition forces c = M² | new as far as the sweep found (modest, n ≤ 6, ansatz-dependent) |
| Lean formalisation of all of the above | new |

If a reference turns up that states the δ-shift-of-massive-Tr φ³ ⇒ Weinberg result or the offset classification,
those rows drop to "independent re-derivation + formalisation".

## 1. Conventions

- **Mostly-minus**, as in [CGW]. X_ij = (p_i + … + p_{j−1})², p_i² = M² (all pions have mass M), so
  X_{i,i+1} = M². X̃ := X − M² (X̃_{i,i+1} = 0). c_ij := −2 p_i·p_j = X_ij + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j}
  (masses cancel, so the same formula holds with X̃). Massive propagator 1/(X − M²) = 1/X̃.
- Tr φ³ functions A4, A6 and the NLSM functions A4N, A6N are **the M2d definitions** (same Lean defs), used as
  functions of their arguments.
- [N]'s convention is the mirror of this one (the sign of each X flips, and the δ-shift becomes its mirror −a\*). Both
  are immaterial up to an overall sign: shown in M2d/M2e, re-checked here.

## 2. The ansatz (itself an assumption)

Y_ij = X_ij + μ_ij + δ·a\*_ij on the planar chords (n = 4: X13, X24; n = 6: the nine hexagon chords), where:

- a\* is the M2d/M2e δ-shift (a_oo = −1, a_ee = +1, a_oe = 0);
- μ_ij are **constant offsets** (independent of δ and X), δ → +∞, physical X with X_{i,i+1} = M².

The output is lim δ^{2n−2} A_{2n}^{Trφ³}(Y). Special point: **uniform mass**, μ_ij = −M² for all chords. That is
Tr φ³ with every propagator of mass M, then δ-shifted. In [N] eq. 8 language (mostly-plus, mirror) this is
m²_χ = M², m²_ϕ = M² − δ, m²_ϕ̃ = M² + δ, so m²_ϕ + m²_ϕ̃ = 2m²_χ. Stated now, to be checked.

**What is NOT derived:** the value of M (and of F). M and F_π remain inputs. This rung asks whether the **structure**
s − M² comes out of the geometry, not the value of M.

## 3. Targets and pre-registered expectations

**(a) n = 4.** Prediction:
`δ²·A4(Y) → −(X13 + X24 + μ13 + μ24)`. At uniform mass this is `−(X̃13 + X̃24) = −c13 = −(s + t − 2M²)` with
s = s12 = X13 and t = s23 = X24. SU(2) dressing (as M2d D1, Tr(σσσσ) = 2(δδ − δδ + δδ)) of an ordered
amplitude κ(s + t − 2c) gives M_ab;cd = 8κ[(s − c)δ_abδ_cd + (t − c)δ_acδ_bd + (u − c)δ_adδ_bc]. That is
A(s,t,u) ∝ s − c, which is Weinberg's (s − M²)/F² **iff c = M²**. With uniform offsets, c = −(μ13 + μ24)/2 = M².
**Identification:** M² = −μ (the uniform offset) = the external mass². F² ∝ δ as in M2d (f_π² = δ); the overall
normalisation is convention.
PASS (a) = Lean `Tendsto` for the n = 4 limit with offsets + exact dressing giving (s − M²) at uniform mass.

**(b) Soft behaviour.** Expectations:

- **(b1)** The massive planar soft map (the massless soft map applied to X̃: X̃_{1,j} → X̃_{2,j},
  X̃_{1,3}, X̃_{2,n} → 0) gives **exactly 0** at n = 4 and n = 6. This is inherited from the massless Adler zero. It is
  **not** a physical soft limit, since a massive on-shell pion cannot go soft. At n = 4 the point is
  s = t = M² (u = 2M²), the c13 = 0 hidden zero.
- **(b2)** The naive soft point in physical variables, where every invariant containing p1 is set to its massless
  soft value (n = 4: X13 = X24 = 0, i.e. s = t = 0): the amplitude is **not** zero. It equals the O(M²) constant
  **+2M²** in the normalisation of (a) (i.e. −c13 = 2M² − s − t at s = t = 0). Equivalently, Weinberg's A(0,t,u) = −M²/F².
  This is the expected breaking: proportional to M², vanishing as M → 0, consistent with [CGW]'s "non-vanishing
  constant controlled by m". At n = 6 the value is reported (expected nonzero, → 0 as M → 0), not graded.

**(c) n = 6.** Predictions:
- (c1) `δ⁴·A6(Y) → A6N(X + μ)` for any constant μ. In particular, at uniform mass, `A6N(X̃)` (Lean `Tendsto`).
- (c2) **Independent check that A6N(X̃) is the massive 6-pion amplitude of LO U(N) ChPT.** This uses exact sympy
  Feynman rules from L = (F²/4)Tr(∂U∂U†) + (F²M²/4)Tr(U + U† − 2) in the **Cayley** parametrisation
  U = (1 + iΦ)(1 − iΦ)⁻¹ (not [CGW]'s minimal or exponential one). Prediction: A4_FR = ρ4·(X̃13 + X̃24),
  A6_FR = ρ6·A6N(X̃) with ρ6 = −ρ4², the ratio fixed by factorisation on X̃14 = 0. These are identities in
  (X̃, M²), with M² a free symbol. Also predicted: the massless limit M → 0 reproduces M2d's ratio.
  If (c2) fails, A6N(X̃) is *not* the massive 6-pion amplitude, and the uniform-mass shift fails at n = 6.

**(d) Uniqueness within the ansatz (kept small).** Offsets μ ∈ ℝ² (n = 4) or ℝ⁹ (n = 6).
- (d0) **Unobservable direction.** μ ↦ μ + λa\* only reparametrises δ (δ ↦ δ + λ), so the limit cannot depend on it.
  Prediction: A6N(Z + λa\*) = A6N(Z) exactly (and A4N likewise).
- (d1) **Target = Weinberg/ChPT.** Impose (P), "internal pion poles at the physical mass": μ14 = μ25 = μ36 = −M².
  Then require that the limit equals A6N(X̃). Prediction: this **forces μ = −M²·1 + λa\***, i.e. uniform mass, up to (d0).
  At n = 4: μ13 + μ24 = −2M².
- (d2) **Target-free version.** Replace "equals the ChPT amplitude" by "has the massive hidden zeros", i.e. vanishes
  on every skinny-rectangle locus c = 0 (n = 4: c13 = 0; n = 6: the six loci of M2d). Keep (P).
  Prediction: the **same** solution set. If hidden zeros allow more, or fewer, that is reported as the finding.
- (d3) **No condition beyond the ansatz.** Prediction: at n = 4 the shift alone yields the one-parameter family
  A ∝ s − c with c = −(μ13 + μ24)/2 free. That is exactly the O(p²) form of generalised ChPT [KMS] with β = 1 and
  α = 4 − 3c/M². So **the shift by itself does not fix c = M²**; a further condition ((d1) or (d2)) is needed.
  At n = 6 with (P), the predicted family is μ_oo = −c + λ, μ_ee = −c − λ, μ_oe = −M².
- Script/Lean split, declared now: the (d1)/(d2) solution sets come from exact sympy (generic-point evaluation and
  linear solve). Lean proves the algebra: (d1) "A6N(Z + v) = A6N(Z) for all Z with nonzero poles, v_oe = 0 ⇒
  v = λ·a\*-pattern", by evaluation at explicit points. Lean also proves (d0), the n = 4 versions of (d1)/(d2),
  and the converse. The n = 6 (d2) hidden-zero classification is script-only unless it is cheap in Lean.

**(e) Data (LO, as in M2d).** At c = M²: a0⁰ = 7M²/(32πF²), a0² = −M²/(16πF²). With general c:
a0⁰ = (12M² − 5c)/(32πF²), a0² = −2c/(32πF²).
- Inputs (labelled **inputs**, not predictions): M = M_π± = 139.57039 MeV and F = f_π+/√2 with
  f_π+ = 130.2(1.2) MeV (PDG 2024, rev. "Leptonic decays of charged pseudoscalar mesons", eq. 72.14),
  so F = 92.07 MeV. Secondary: the CGL inputs F = 92.4 MeV (M2d's choice).
- Data: NA48/2 Ke4 (EPJC 70 (2010) 635): a0⁰ = 0.2220 ± 0.0142, a0² = −0.0432 ± 0.0097 (errors in quadrature).
- **Tolerance: |LO − measured| ≤ 30% of |measured| for each**, as in M2d. It is informed by the known LO→NNLO series
  (CGL), so this check is not blind and does not discriminate. Expectation: within tolerance, a0⁰ near −27%.
- **Reported, not graded:** the dimensionless LO ratio a0⁰/a0² = −7/2 (it is −7/2 iff c = M²) against
  NA48/2's −5.14. It is not graded because the number is Weinberg's 1966 LO prediction, known to deviate at LO.
  Grading it now, after seeing the data, would be post hoc. It is discussed in the review as an M3 candidate.

## 4. Verdict rules

- **PASS:** (a) Lean limit + exact dressing to s − M² at uniform mass; (c1) Lean limit; (c2) exact Feynman-rule
  identity holds with ρ6 = −ρ4²; (d1) Lean-proved algebra + script solution set = prediction; (e) within tolerance.
  (b) and (d2) are reported against their predictions. A miss there is recorded, and it downgrades to PARTIAL only
  if it contradicts (a)/(c).
- **PARTIAL:** (a) holds but (c2) fails, or (d1) gives a different solution set, or a Lean target is only
  script-verified.
- **FAIL:** (a) fails, i.e. no constant offset in the ansatz gives (s − M²), or the dressing does not give Weinberg's form.
- Every prediction miss is kept on the record (kill criterion 4 spirit). No target is moved.

## 5. Kill-criteria watch

- (3) Fitting: M and F are inputs; no constant is tuned to data. One parameter, c (or μ), is fixed by a structural
  condition ((d1) or (d2)), not by data. If c could only be fixed by fitting the data, that would be fitting.
- (7) Level confusion: no step rests on "all is one".

## 6. Out of scope

The value of M_π (or of any GeV scale); loops; NLO; the stringy version; n ≥ 8; non-constant or δ-dependent
offsets beyond a\*; SU(3) or unequal masses (KK/unequal spurions in [CGW] are cited only).
