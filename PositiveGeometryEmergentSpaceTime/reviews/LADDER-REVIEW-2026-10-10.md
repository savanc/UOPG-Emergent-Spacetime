# Ladder review after the M3 miss

*10 Oct 2026 (Europe/London). Written for the author after M3 failed its pre-registered test. I re-read everything first:
MISSION, README, all eight pre-registrations, all reviews (UOPG, M1–M3, Bandyopadhyay), the notes (trade space,
entropy sweep, source shelf, interests), the bridge essay, AXIOMS and CREDITS, and the git history of every prereg file.
No new physics was computed. There was one tiny well-posedness check (§3), which is now a Lean theorem.*

## Plain-language summary

- **What we have built** is a clean, machine-checked chain inside one toy corner of physics, the scattering of
  massless or massive pions at lowest order:
  1. one positive geometry (the associahedron);
  2. its boundaries give the poles and factorisation (locality and unitarity, at n = 5);
  3. a shift of that geometry that is *forced* (at n = 6, within a stated ansatz) turns it into pion amplitudes;
  4. translating it by M² gives the pion-mass structure s − M².
- About 180 Lean theorems back this chain, all on the three standard axioms. **Almost all of the physics was known
  before we did it.** What is ours is the formalisation, a few uniqueness/"forcing" statements, and honest bookkeeping.
- **The first attempt to get a number beyond chiral symmetry failed.** M3 asked what our geometry predicts at the next
  order. The answer is L3/L2 = −2, a ratio that was published in 1996. It misses the preferred modern fit (−3.79 ± 0.31)
  by 3.8σ beyond a ±30% band.
- **The review adds one important nuance.** That data point sits outside the region that *any* unitary large-N
  completion can reach (L3/L2 ≥ −3, Lean-proved in this review). So the M3 test could not have been passed by any
  large-N geometry at that scale and fit. The FAIL stands, because it was pre-registered. Its lesson, though, is as much
  "check that the data are in the theory's allowed region before testing" as "hidden zeros are wrong".
- **Distance to "one real particle, zero fitted parameters"** is still very large. Pions are composite, the scale (M, F)
  is an input, and nothing yet touches a Standard Model particle.

## 1. Status of every rung

Lean counts come from `lean/AxiomsAll.lean`, which enumerates every declaration in `PositiveGeometryEmergentSpaceTime.*`
(output in `lean/AxiomsAll_output.txt`). Totals: **181 theorems + 53 definitions, all on
[propext, Classical.choice, Quot.sound]; 0 nonstandard.**

| Rung | Goal | Verdict | Lean thms | New vs prior art (honest) | Still assumed | Review |
|---|---|---|---|---|---|---|
| **M0** | Gr(2,4) algebra (point layer) | ✅ (inherited) | 161 in the UOPG repo (not here) | Formalisation of classical facts; positivity used in 8/161 | Positivity of the chart is an option | `reviews/uopg-review-2026-10-09.md` |
| **M0′** | One n-particle object (L-B) | ✅ **via M2c** (was never ticked; fixed now) | see M2c | — | — | `reviews/M2c-result-2026-10-10.md` |
| **M1** | Lorentz signature (1,3) from the spinor/Hermitian form | PASS | 32 | Classical maths (Penrose, Klein); new only as this formalisation | **Positivity does not live on the Hermitian slice** (kill #1 caveat) | `reviews/M1-result-2026-10-10.md` |
| **M2** (P-EFT) | Positivity as a *conclusion*: l̄₂ ≥ 27/20 | PASS (z = 7.15) | 17 | Bound published (Manohar–Mateu 2008); new: Lean proof of the positivity step | Unitarity (Im T ≥ 0), dispersion relation, O(p⁴) matching are hypotheses; tests QFT+ChPT, **not** our geometry; not blind | `reviews/M2-result-2026-10-10.md` |
| **M2b** | EFT-hedron Hankel bound f₀f₂ ≥ f₁² | PASS | 18 | Arkani-Hamed–Huang–Huang 2020 maths; new: Lean (PSD any size for point masses, 2×2 for measures) | Moment representation is the hypothesis; no data | `reviews/M2b-result-2026-10-10.md` |
| **M2c** (P-Pole) | n = 5 associahedron: canonical form = m₅, residues = factorisation | PASS | 30 | ABHY 2017; new: Lean, and a sign-flip counterexample showing positivity carries weight | n = 5 only; the "locality from boundaries" reading is ABHY's | `reviews/M2c-result-2026-10-10.md` |
| **M2d** | Tr φ³ → pions by the δ-shift | PASS with limits | 23 | 2401.05483 / 2312.16282; new: Lean `Tendsto` limits | The shift was an input rule; M, F by hand; D2 "within tolerance" while a0⁰ is 4.4σ off (flagged §4) | `reviews/M2d-result-2026-10-10.md` |
| **M2e** | Is the shift forced at n = 6? | PASS within ansatz | 17 | c-preserving uniqueness (2312.16282 §7.1) is prior; new (modest): forcing from power counting + Adler on 3 legs, without assuming c-preservation | **Linear δ-uniform shift ansatz**; limits → equations is script-only; n = 6 only | `reviews/M2e-result-2026-10-10.md` |
| **M2f** | Mass structure s − M² | PASS (structure only) | 22 | Core anticipated by Carrillo González–Ward 2601.16860; new: Lean limits, n = 6 offset uniqueness from two non-adjacent zeros | Constant-offset ansatz; **hidden zeros imposed as a condition**; M, F inputs; parts script-only | `reviews/M2f-result-2026-10-10.md` |
| **M3** | One dimensionless O(p⁴) ratio from the geometry | **FAIL** (recorded miss); a **reproduction** | 22 | L3 = −2L2: Polyakov–Vereshagin 1996; hidden zeros ⇒ L0: Bartsch et al. 2024. New: one structural reason across four completions, the even/odd-spin-balance reading, [H]'s C-odd O(p⁴) term, the data test, Lean | **Completion class** (c-preserving ⇒ hidden zeros); large N_c; μ = 0.77 GeV; choice of BE14 NNLO fit | `reviews/M3-result-2026-10-10.md` |
| M4 | Pre-register before computing | **practised at every rung** (in `prereg/`) | — | — | Folder rule fixed (§5) | this file |
| M5, M6 | Massive on-shell structure; one real particle | not started | — | — | — | — |

## 2. What the chain has actually established

Everything below is **tree level, leading order, colour-ordered, planar U(N) flavour, and pions only**.

1. **One positive geometry → poles and factorisation.** The n = 5 kinematic associahedron's canonical form is the
   bi-adjoint φ³ amplitude, and each facet residue is the 4-point amplitude [PROVED, M2c]. Flipping one positivity
   sign removes a facet and its pole, so positivity does work here, unlike in M0/M1.
2. **→ pions, by a shift that is forced.** δ-shifting the same function gives the 4- and 6-pion NLSM amplitudes with
   hidden zeros and the Adler zero [PROVED, M2d]. Within linear δ-uniform shifts at n = 6, pion power counting plus the
   Adler zero on three consecutive legs leave only that shift [algebra PROVED; reduction script-verified, M2e].
3. **→ the mass structure.** Translating the associahedron by M² and shifting gives Weinberg's (s − M²)/F² and the
   massive 6-pion amplitude. Massive hidden zeros force the offsets [PROVED, M2f].
4. **Positivity of the EFT coefficient space is a theorem, not an axiom** [PROVED, M2/M2b], given unitarity and
   analyticity as hypotheses.

**Inputs still required:**
- M and F_π (every GeV);
- the linear-shift and constant-offset ansätze;
- hidden zeros, the Adler zero and pion power counting, as conditions we choose to impose;
- the choice of UV completion (M3);
- the identification "this amplitude = QCD pions" [CITED].
- Signature: (1,3) is reached on the Hermitian slice, while positivity lives on the split slice. They have not been
  joined.

## 3. What M3's failure teaches

- **The hidden-zero class is too rigid at O(p⁴).** All four completions in our chain have the overall factor
  (X13 + X24). That pins g2,1 = g2,0, i.e. equal even- and odd-spin weight in ⟨(−1)^J/m⁴⟩. One condition fixes the
  only free O(p⁴) direction, and the data do not sit there.
- **The data lean to (and past) ρ dominance.** At μ = 0.77 GeV the NNLO fit gives L3/L2 = −3.79. The vector-only edge
  of the large-N positivity wedge is L3/L2 = −3 (VMD/Skyrme).
- **Well-posedness check (new, tiny).** AR's bound g2,1 ≤ 2g2,0, through the large-N map, is exactly
  L3 ≥ −3L2 [PROVED: `LECRatio.l3_ge_neg3_l2`, `be14_outside_wedge`]. So the primary data point is outside the region
  *any* unitary large-N tree completion can reach, by 2.5σ (the secondary SU(2) CGL point is outside too: g̃2′/g̃2 = −3.0 < 0). M3 compared a large-N tree statement with an N_c = 3 fit
  whose loop/scale effects (L2 runs; the ratio is −2.3 at 0.5 GeV and −6.1 at 1 GeV) are larger than the effect
  tested. **The FAIL is valid under the rule we fixed. It is weak evidence against hidden zeros in particular**,
  because VMD fails the same comparison.
- **Which assumption to relax (minimum-assumptions principle).** Keep the geometry; drop "hidden zeros to all orders"
  as a *condition*. Hidden zeros are the strongest assumption we added beyond Adler + power counting (M2f imposed them,
  M3 inherited them). Relaxing them to "Adler zero + factorisation + positivity" opens the one-parameter even/odd weight
  ε = ⟨(−1)^J/m⁴⟩/⟨1/m⁴⟩ ∈ [−1, 1]. The hidden zero is ε = 0, vector dominance ε = −1. The question becomes whether a
  geometric deformation naturally produces ε ≠ 0.
- **Branches still alive.**

| Branch | Status | Why alive |
|---|---|---|
| P-EFT | alive (passed M2/M2b) | Gives bounds, and now the wedge that M3's data violated; the right framework for M3b |
| P-Pole / L-B (surfaceology) | alive (M2c–M2f) | The hidden-zero class is one corner of it; non-c-preserving deformations are untested |
| P-Net / H-Markov (Markov network) | untested | Lean 2-node network → Gr≥0(1,4) not started; the essay's Q1 Fusions map still open |
| L-A amplituhedron | untested | Planar N=4 only; no data contact possible, but maths is rich |
| Hermitian ↔ split slice bridge | open near-miss (kill #1) | Must show positivity matters for (1,3) physics, or concede it lives only in the particle layer |
| Entropy/holography scale | parked | No credible literature route to a GeV (`notes/positive-geometry-entropy-sweep-2026-10-10.md`) |

## 4. Kill-criteria audit

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Signature cannot be fixed | **not fired; conditional clause in force** | (1,3) from Hermitian matrices (M1). Positivity is natural only on the split slice, so for now positivity "survives only as a statement about the particle layer". Near-miss: still unresolved |
| 2 | No positivity is forced | not fired | M2 (P-EFT) derives coefficient positivity; M2c shows a sign flip kills a pole. P-Net untested |
| 3 | Fitting creeps in | not fired | No tuned constants anywhere. Watch-item: the completion *class* is a discrete choice. If we try classes until one fits, that is fitting by another name. Each new class must be pre-registered |
| 4 | Pre-registered miss | **FIRED at M3** | Recorded in MISSION, README and the M3 review; target not moved |
| 5 | Tier-1 contradiction | not fired for the framework | M3's miss is against a fit (BE14), not a PDG precision value. It ends the hidden-zero class *as a model of O(p⁴) QCD at μ ≈ m_ρ*, not M2d–M2f |
| 6 | Dependence on tier-3 leads | not fired | Bandyopadhyay is kept as REPORTED-UNREPLICATED; nothing depends on it |
| 7 | Level confusion | not fired | Bridge statements stay tagged [SPECULATION] in the essay |

**Post-hoc risks to flag:**
- M2: the bound and its agreement with data were published in 2008. Disclosed as not blind.
- M2d D2: the 30% tolerance was taken from CGL's own series, and "within tolerance" hides a 4.4σ experimental pull.
  The tag was generous.
- M2f: −7/2 is Weinberg 1966. Correctly not used as a target.
- **M3: data were seen before the pre-registration, and the predicted number was known analytically.** Both are
  disclosed in the prereg. The primary-fit rule ("authors' preferred fit") went against us (the p⁴ fit passes). That
  is the opposite of a favourable bias, but the verdict is still fit-dependent. The prereg also lacked a
  well-posedness check (data inside the theory's allowed region); see §3.

## 5. Process audit

- **Rung protocol followed?** Yes, in order, for M2–M3. Git history shows every prereg committed before its first
  script/Lean commit. The only amendment, M2e A1 (prior art), was made 3 minutes after the prereg and before any
  result. **No prereg was edited after a result.**
- **Speed.** M1–M3 all happened on one day; the M3 prereg-to-result gap was 8 minutes. Pre-registration protects
  against moving targets, not against haste. Future rungs should leave room for an independent re-read of the prereg.
- **Tags too generous.**
  - M2d's D2 "within tolerance" (above).
  - M2e "forced" depends on a script-only reduction; it is tagged that way in the review, but the MISSION line reads
    stronger.
  - M3's `be14_fail` is "PROVED" arithmetic, not physics. The review now says so.
  - M0′ was never ticked although M2c meets its pass test (fixed).
  - AXIOMS.md listed only some declarations (M1 helpers and M2e names were missing). It is now complete through
    `AxiomsAll.lean`.
- **Script-only steps** (to Lean-verify): M2e limits → equations; M2f (c2), (d1′), (d2′); M3 α′-expansions (digamma);
  SU(2) isospin projections.
- **Folder inconsistency (fixed).** MISSION's M4 said `predictions/`; every rung used `prereg/`. Rule adopted:
  **`prereg/` is the single pre-registration folder** (eight dated files, full history kept, no moves needed). MISSION
  M4 is updated. A prereg is immutable once a result commit exists; corrections go in a dated "Amendment" section.

## 6. Revised ladder (re-ordered)

1. **M3w, well-posedness first (small).** Before any new data test, prove or compute that the data lie inside the
   theory's allowed region (as `l3_ge_neg3_l2` does now). Make it a protocol step.
2. **M3b, a ρ-compatible deformation as a 1-parameter family.** Parametrise ε (even/odd spin balance; hidden zero
   ε = 0, VMD ε = −1) by a geometric deformation that breaks the 4-point hidden zero but keeps Adler + factorisation:
   e.g. a non-c-preserving surface deformation, LS with a non-hidden-zero satellite, or the Coon q-deformation. Key
   question: **is the parameter geometric** (fixed by the surface), or a new dial? If it is a dial, M3b is a
   measurement, not a prediction. Data comparison only in a scheme that passes M3w (e.g. large-N lattice LECs, if
   available).
3. **Lean-verify the script-only reductions** (M2e, M2f, M3 expansions). This hardens what we already claim.
4. **Hermitian ↔ split slice bridge** (kill #1 near-miss). Find one statement where split-slice positivity constrains
   (1,3) particle kinematics, or prove an obstruction.
5. **P-Net / Markov-network branch.** Lean: a 2-node reversible network → a point of Gr≥0(1,4) with nonnegative minors, then
   the *Fusions* Definition-2 map (essay Q1). This is the only branch that connects to conscious-agent dynamics.
6. **n = 8 shift forced** (extend M2e) and **exact 6-point L0 uniqueness** (check Bartsch et al.). Consolidation.
7. **L-A amplituhedron fact** (n = 5/6 positroid cell ↔ canonical form): maths only.
8. **Scale:** parked until a dimensionless chain works. Keep M and F as declared inputs.

## 7. Honest overall assessment

Measured against M6, we are at the very beginning. Nothing produced so far is a new, successful, zero-parameter
prediction. The one zero-parameter number the chain fixes beyond chiral symmetry was already known and misses the
data, as does every other large-N tree completion on that comparison. The value built today is a trustworthy, reusable
Lean base for amplitude positivity and the Tr φ³ → pion bridge, plus a working pre-registration habit that has already
recorded a real miss without moving the goalposts. That is a legitimate small success in the MISSION's own terms. The
path to a Standard Model particle would need, at minimum: gauge bosons and fermions in the particle layer (L-B covers
neither), a dimensionless electroweak quantity, and a dictionary (K3) that doesn't sneak in a scale. None of these has a
known route. Expect years, or never, as MISSION already says.

---
**Correction (2026-10-11, M3w).** The statement in §3 that no unitary large-N tree completion could pass the M3
comparison is wrong under M3's pre-registered rule: the vector edge (−3) with its ±30 % band passes. The M3 FAIL of
the hidden-zero value stands and is stronger evidence than §3 suggests. See `reviews/M3w-result-2026-10-11.md`.
