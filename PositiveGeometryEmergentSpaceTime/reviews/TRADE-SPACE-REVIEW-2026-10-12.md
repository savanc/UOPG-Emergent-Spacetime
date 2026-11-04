# Trade-space review (step back, not a rung), 2026-10-12

Scope: the ladder to date (M0–M3c, M1b, H-T1 to H-T5g, NL9), closing out the network branch, and the mass-scale gap.

Tags: [PROVED] = Lean or exact; [SIMULATED] = certified or high-precision numerics; [CITED]; [CONJECTURE]; [SPECULATION].

**Strictness rule.** "Prior art" means the physics or mathematics statement was published before we did it.
"Plausibly new" means no prior statement was found in *our* sweep. That is not a literature guarantee.

---
## 1. Ledger

Sources: the reviews in `reviews/` and the MISSION ladder table.

| Rung | Verdict | What it established | Novelty | Tag |
|---|---|---|---|---|
| M0 | ✅ | Gr(2,4) algebra (Plücker, Klein, null momenta) in Lean over any field | Prior art (classical); Lean is ours | PROVED |
| M0′ (via M2c) | ✅ | One n-particle object in Lean | Prior art (ABHY) | PROVED |
| M1 | PASS | (1,3) signature via the complex spinor form | Prior art; Lean ours | PROVED |
| M2 (P-EFT) | PASS, not blind | l̄₂ ≥ 27/20 as a *conclusion* of positive spectral weights | Prior art (positivity bounds, Adams et al. 2006; Manohar–Mateu); Lean ours | PROVED |
| M2b | PASS (maths) | EFT-hedron Hankel bound f₀f₂ ≥ f₁² | Prior art (AHH 2020); Lean ours | PROVED |
| M2c | PASS | n = 5 associahedron: canonical form = m₅; a sign-flip counterexample | Prior art (ABHY 2017). Counterexample is minor-new | PROVED |
| M2d | PASS with limits | Tr φ³ → pions via the δ-shift | Prior art (2312.16282, 2401.05483) | PROVED (limits) |
| M2e | PASS within ansatz | Shift forced at n = 6 by power counting + Adler on 3 legs | **Plausibly new (modest)**: a forcing route without assuming zeros | PROVED / script |
| M2f | PASS, structure only | s − M² mass structure; n = 6 offset uniqueness from two zeros | Core prior (Carrillo González–Ward 2601.16860); offset uniqueness **plausibly new (small)** | PROVED |
| M3 | **FAIL** (recorded miss) | Hidden zero ⇒ L3/L2 = −2 vs BE14 NNLO −3.79 ± 0.31 (3.8σ) | The prediction is prior art (Polyakov–Vereshagin 1996; Bartsch et al. 2024) | PROVED + data |
| M3w | CONDITIONAL | Data point outside R_full unless there is a ≥ 6.5% 1/N_c band | **Plausibly new (bookkeeping)**: an explicit well-posedness region | SIMULATED / PROVED |
| M3c | WRONG-SIDE | Adler-compatible Coon gives ε > 0 (zero-curve lemma) | Lemma **plausibly new (small)**; Coon prior (Figueroa–Tourkine; Cheung–Remmen) | PROVED |
| M3b | Prereg, not run | ε chord, Lovelace–Shapiro (LS) ↔ ρ | — | — |
| M1b | NO-GO (theorem) | No open set of real Minkowski points on the positive slice; kill #1 second clause fired | **Plausibly new** in this form; folklore-adjacent | PROVED |
| H-T1 | PASS | *Traces* §3 entropy conjecture refuted; corrected inequality; trace = Kron reduction → Lam points | Refutation **new** (it is of the trace-order preprint's conjecture). Kron/Lam prior | PROVED / CITED |
| H-T2 | (a,b,d) PASS, (c) FAIL | Lam cells = medial pairing (302 networks); Y–Δ preserves the dlog form; Ω₃ candidate | Mostly prior art (Lam). Ω₃ candidate is **plausibly new (conjectural)** | PROVED / SIMULATED |
| H-T3 | (a,b) PASS, (c) PARTIAL, (d) FAIL | Ising → OG≥0 cells exact; ABJM measure = carrier × J | Prior art (Galashin–Pylyavskyy; HWX 2014) | PROVED / SIMULATED |
| H-T3b | PASS | HWX J in Ising variables; (2.55) in Lean | Prior art (HWX); Lean ours | PROVED |
| H-T5 | (a) PASS, (b) INCONCLUSIVE, (d) FAIL | n = 6 Lean point; Ising does not select a tiling | Prior art (HKWZ, He–Kuo–Zhang) | PROVED |
| H-T5b | PASS | Certified n = 8 tiling via a linear fiber; spurious poles cancel | Tiling prior (HW, HKWZ). Certified *method* **plausibly new (methodological)** | SIMULATED (certified) |
| H-T5d | R1 FAIL, R2 PASS | n = 10 trees = Perlstein–Tessler BCFW cells, certified | Prior art (PT 2501.07576); check is ours | SIMULATED (certified) |
| H-T5f | B PASS, A FAIL / post hoc | Wall graph = associahedron flips (n = 8, 10, 12) | Prior art (PT Cor. 4.3.5) | PROVED (exact combinatorics) |
| H-T5g | Stage 1 verified; Stage 2 PASS | Tile measure = 2^{n−5} × carrier × J_V (cut-set form of HWX J), n = 8, 10 | Rule prior (HWX). Cut-set form, tile check and constants **plausibly new (small)** | SIMULATED (≥ 20 digits) |
| NL9 | Candidate | Blind positivity check on the 9-loop hexagon (Zenodo 10.5281/zenodo.22949278) | — | — |

**Count (19 decided rungs, excluding M3b and NL9):**
- **13** mainly confirm prior art: M0, M0′, M1, M2, M2b, M2c, M2d, M3, H-T3, H-T3b, H-T5, H-T5d, H-T5f.
- **6** carry a plausibly new but small element: M2e, M2f (part), M3w, M3c (lemma), M1b, H-T1 (refutation).
- **Weaker items:** H-T5b (method), H-T5g (form and constants) and H-T2 (Ω₃, conjectural) are methodological or
  small.
- **No rung has produced a new physical prediction confirmed by data.** The only data test, M3, failed.

---
## 2. Close-out of the network branch (H-T1 to H-T5g)

### Established for the mission

1. **Real positivity reaches Gr≥0 and OG≥0** from probabilities and couplings: Markov/electrical → Gr≥0 (Lam);
   Ising → OG≥0 (Galashin–Pylyavskyy). This is the only positivity route that survives M1b's no-go
   [PROVED / CITED].
2. **Ising trees tile the ABJM orthogonal momentum amplituhedron** at n = 6, 8, 10, as the BCFW cells
   [SIMULATED, certified; CITED: PT].
3. **The tiles glue like an associahedron:** wall graph = flip graph [PROVED combinatorially; CITED: PT].
4. **The measure on a tile = carrier × J**, with J the HWX loop factor in cut-set form. The constant is 8 at n = 8
   and 32 at n = 10 [SIMULATED].

### Not established

- **No mass scale.** ABJM is a conformal 3D theory.
- **No 4D.**
- **No selection principle:** Ising data describe the tiling but do not pick it (H-T5, H-T5d).
- **No physical meaning for "conscious-agent" weights** [CONJECTURE remains].

### Recommendation on the n = 8 symbolic proof

Do one cheap sympy proof of Ω_tile = 8 · carrier · J_V at n = 8 (both trees), with a ≤ 1-day budget. It makes the
cut-set statement citable as an identity, not just numerics. Skip Lean unless the identity reduces to rational
algebra (it involves the Haar density, so likely not cheap).

After that, **freeze the branch**: no n = 12 and no face-loop rung unless a mass or selection question needs it.

---
## 3. The mass-scale problem (the central gap)

**Ground rule:** pure geometry is dimensionless. A dimensionful scale needs **one input**, at best. Everything else
can only be a **dimensionless ratio**.

The aim is therefore "one unit + zero fitted parameters + blind ratios". Tags show the status of each option.

### (a) Dimensional transmutation (scale from a running coupling) [CITED: Coleman–Weinberg; Gross–Wilczek]
- **Input remaining:** one, Λ_QCD (or α_s at one scale).
- **Zero-parameter prediction:** only ratios at fixed N_c (lattice).
- **Testability:** high (lattice and PDG).
- **Lean:** low (needs RG flow).
- **Link:** none yet to the associahedron or networks.
- **Honest cost:** this is the Standard Model's own answer and adds nothing geometric.

### (b) Massive positive geometry [CITED]
- **Sources:** AHH massive spinor helicity; the Coulomb-branch "deformed amplituhedron"; kinematic mesh /
  surfaceology with masses; massive hidden zeros 2601.16860.
- **Input remaining:** the masses are free deformation parameters. Geometry fixes *where* they enter (X → X − M²;
  M2f) but not their values. Coulomb branch: masses = vevs, still inputs.
- **Zero-parameter predictions:**
  - mass *patterns* such as the uniform-mass requirement for zeros (2601.16860);
  - spurion-controlled NLSM mass terms, which imply **relations among O(p⁴) mass-dependent LECs** (ratios).
- **Testability:** medium (chiral LECs from FLAG / lattice).
- **Lean:** feasible (rational limits, as in M2f).
- **Link:** a direct continuation of M2d–M2f and the associahedron.

### (c) Ratios only [CITED]
- **Targets:**
  - Regge / Lovelace–Shapiro spectra: with the Adler zero fixing α₀ = 1/2, m²_J ∝ (J − 1/2), so m_{f2}²/m_ρ² = 3;
  - KSRF: m_ρ² = 2 g² f_π²;
  - Coon spectra;
  - coupling and width ratios (ρ vs f2).
- **Input remaining:** one unit (α′ or f_π).
- **Zero-parameter predictions:** yes, for several ratios.
- **Testability:** high (PDG).
- **Lean:** feasible (Beta-function residues).
- **Link:** M3, M3b, M3c and the hidden zeros.
- **Honest cost:** famous ratios (m_{f2}/m_ρ, KSRF) are **already known to us**, so they are not blind. Only lesser
  quantities we have not looked at qualify.

### (d) Species scale / holography / entropy bounds [CITED earlier]
- **Input remaining:** M_Pl and N_species.
- **Zero-parameter prediction:** inequalities, not values.
- **Testability:** very low.
- **Lean:** low.
- **Link:** weak.

### (e) Connes-style spectral action [CITED; cautionary]
- **Input remaining:** cutoff Λ plus the spectral function moments.
- **Prediction:** the 2008 Higgs-mass prediction (~170 GeV) failed and was later patched. This is a warning about
  post-hoc rescue.
- **Lean:** low.
- **Link:** none.

### (f) Trace-order "entropy rate as mass" [CONJECTURE]
- **Input remaining:** a unit conversion plus the choice of Markov chain (many parameters).
- **Prediction:** none zero-parameter so far. H-T1 already refuted a related *Traces* §3 entropy claim.
- **Testability:** none at present.
- **Link:** networks (H-T1).

### (g) Skyrmion masses in units of f_π/e [CITED: Adkins–Nappi–Witten 1983]
- **Input remaining:** f_π and e (two inputs; e is fitted).
- **Zero-parameter ratios:** M_Δ/M_N-type rotor ratios, but these are known and not blind.
- **Lean:** medium (rotor algebra).
- **Link:** pions (M2d), weak.

### Summary table

| Option | Inputs left | Zero-parameter dimensionless prediction | Data | Lean | Link to built work |
|---|---|---|---|---|---|
| (a) transmutation | 1 (Λ) | lattice ratios only | high | low | none |
| (b) massive positive geometry | masses (1+) | LEC relations, mass patterns | medium | **good** | **strong** (M2d–M2f) |
| (c) ratios / Regge | 1 unit | **yes** (spectra, couplings) | **high** | good | **strong** (M3*) |
| (d) species / holography | M_Pl, N | inequalities | very low | low | weak |
| (e) Connes | Λ + moments | Higgs/top ratios (failed) | high | low | none |
| (f) trace-order entropy-rate | many | none | none | — | networks |
| (g) Skyrmion | 2 | rotor ratios (not blind) | high | medium | weak |

---
## 4. Recommended next rungs (each needs a prior-art sweep first; no data seen before prereg)

### Top pick: MR-1, the zero-parameter LS ρ/f2 coupling (width) ratio

**Question:** does the hidden-zero / Adler-fixed Lovelace–Shapiro amplitude predict a ratio of ρ and f2 couplings?
- The amplitude has α₀ = 1/2 and α′ as the only unit, with **no ε**. It is the ε = 0 corner of M3b.
- Target: R = Γ(f2 → ππ)/Γ(ρ → ππ), or equivalently g̃_{f2}²/g̃_ρ², with phase-space factors fixed.

**Protocol:**
1. Reconcile with M3b: run MR-1 as M3b's zero-parameter arm, or let it supersede M3b.
2. Do an M3w-style well-posedness check first. This must show that the unitary large-N class can reach the PDG
   value at all.
3. Pre-register the formula, the number and a 1/N_c band (±30%, per M3) *before* opening the PDG f2/ρ width
   entries.

**Disclosure:** I know the rough sizes of the ρ and f2 widths from general knowledge; this goes in the prereg.

**Kill criterion:** if the PDG ratio falls outside the pre-registered ±30% band, record a miss for the
LS hidden-zero class at the resonance level. This would be the second miss after M3, and would trigger moving to
(b) as the primary mass route.

### MR-2: massive hidden zeros → chiral mass LEC relation
- **Basis:** 2601.16860 shows that spurion-controlled pion masses keep the zeros.
- **Pre-register:** the large-N_c relation the zeros impose on the mass-dependent O(p⁴) LECs (e.g. L5, L8 or ℓ̄3
  combinations), derived in Lean in the M2f style.
- **Test:** compare against FLAG averages, unopened before prereg.
- **Kill:** no relation follows (structure-only), or the relation misses beyond a 1/N_c band.

### MR-3 (cheap, citability): symbolic n = 8 identity Ω = 8 · carrier · J_V
- **Budget:** ≤ 1 day.
- **Then:** freeze the network branch.

### Alternative
NL9 (a blind positivity check on the 9-loop data) remains a good *method* rung but says nothing about mass.

---
## 5. Prior-art sweep (brief; URLs for (b) and (c))

**(b) Massive positive geometry**
- Arkani-Hamed, Huang, Huang, *Scattering amplitudes for all masses and spins*:
  https://arxiv.org/abs/1709.04891
- Arkani-Hamed, Flieger, Henn, Schreiber, Trnka, *Coulomb branch amplitudes from a deformed amplituhedron*
  (PRL 132, 211601): https://arxiv.org/abs/2311.10814
- Carrillo González, Ward et al., *Hidden zeros in massive theories* (kinematic mesh; spurion NLSM):
  https://arxiv.org/abs/2601.16860
- Arkani-Hamed, Cao, Dong, Figueiredo, He, *Hidden zeros…; unity of colored scalars, pions and gluons*
  (JHEP 10 (2024) 231): https://arxiv.org/abs/2312.16282
- *NLSM ⊂ Tr φ³*: https://arxiv.org/abs/2401.05483
- Hidden zeros ⇔ enhanced UV scaling; Tr φ³ uniqueness: https://arxiv.org/abs/2406.04234
- Surfaceology / curve integrals (Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas):
  https://arxiv.org/abs/2309.15913

**(c) Ratios**
- Lovelace 1968 and Shapiro 1969 (classic; dual-resonance ππ).
- Polyakov–Vereshagin 1996 (LS → chiral LECs).
- Bartsch et al. 2024 (hidden zeros → LECs).
- Figueroa & Tourkine, *Unitarity and low-energy expansion of the Coon amplitude*:
  https://arxiv.org/abs/2201.12331
- Cheung & Remmen, *Veneziano variations*: https://arxiv.org/abs/2302.12263
- Albert & Rastelli, *Bootstrapping pions at large N*: https://arxiv.org/abs/2203.11950
- Fernandez, Pomarol, Riva, Sciotti, *Cornering large-N_c QCD with positivity bounds*:
  https://arxiv.org/abs/2211.12488
- KSRF: Kawarabayashi–Suzuki 1966; Riazuddin–Fayyazuddin 1966.

**(d)–(g)**
- Dvali (species scale): https://arxiv.org/abs/0706.2050
- Chamseddine–Connes–Marcolli 2007: https://arxiv.org/abs/hep-th/0610241
- Adkins–Nappi–Witten, Nucl. Phys. B228 (1983) 552.
- the trace-order preprint (see H-T1).

**Caveat:** the ratio literature (Albert–Rastelli; Fernandez et al.) already bounds ρ/f2 couplings at large N.
The MR-1 sweep must check whether the LS ε = 0 width ratio is already stated there. If it is, MR-1 becomes a
reproduction with a blind data check: still useful, but it should be labelled that way.
