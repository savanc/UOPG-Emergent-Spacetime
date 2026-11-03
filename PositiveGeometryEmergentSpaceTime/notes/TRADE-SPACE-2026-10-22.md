# Trade space 2026-10-22: review of the author's five proposals

Written 2026-10-22. Base: origin/main 89295e4. **Review and proposals only.** No new rung, no prereg, and
AutoResearch stays PAUSED (STOP 87a7a1f, 2026-10-20). Every rung below is PROPOSED and needs the author's go plus a
dated, immutable prereg in `prereg/` before anything runs. Bridge statements stay [SPECULATION].

Figure: `figures/trade-space-2026-10-22.mmd` → `figures/trade-space-2026-10-22.png`.

Tags: PROVED (Lean in repo), SIMULATED, CITED (fetched in this review run or in a cited repo file), CONJECTURE, SPECULATION.

## A. Classification of each sub-idea (with evidence)

| # | Sub-idea | Status | Evidence | Assumption a new attempt must drop / add |
|---|---|---|---|---|
| P1a | Residues quantised | MIS-STATED / trivial | ABL 1703.04541 §2.1 [CITED]: leading residues are ±1 **by definition** of a positive geometry. Lean pentagon `res_X13`..`res_X35`, `tendsto_res_X13` (`lean/PositiveGeometryEmergentSpaceTime/Associahedron.lean`, 4e8351c) [PROVED] are instances. Non-leading residues and the canonical form are continuous in the kinematic offsets. | Needs an integer that is **not** fixed by the definition. |
| P1b | Lattice points / toric | NEW | ABL §5.6 eq. 57 [CITED]: toric positive geometries come from lattice vectors with projective normality. The lattice is an input, not an output. | Must say what forces the lattice. Otherwise it is "integers by hand". |
| P1c | Winding / Chern classes | NEW, no concrete identity | No repo file. The mass offsets in ABHY/F-COULOMB live in an open chamber. Integer invariants are locally constant there (see INT-1 below). | A topological sector (flux, bundle) that is external to the positive geometry. |
| P1d | Spin quantisation → M5 | ALREADY CLOSED as a mass source | AHH 1709.04891 (MISSION.md:86): spin is a little-group label, so it is automatic. FZ-1 (1948069, Lean `PositiveGeometryEmergentSpaceTime.PauliZero`): the massive zero holds iff g = 2, so a W/fermion g = 2 rung repeats FZ-1. | Spin is integral for free and carries no mass ratio. A new attempt must drop "spin → mass". |
| P1e | Integrality as the F-COULOMB fix | NEW: it is the recorded reopen trigger | BACKLOG F-COULOMB entry and `notes/AUTORESEARCH-METHOD.md:141`: "strict-inequality positivity cannot quantise without an added integrality/topological condition". Lean `FCoulomb.allowed_u_eq_Ioi`, `mass_ratio_free` (4ec488b), prereg 19a54a4. | Kill if the integers are inserted by hand (the author's own kill). |
| P2a | Scale from anomaly / transmutation | ALREADY CLOSED in the scale-free setting | BR-4 `no_scale`, `fixes_scale_not_blind` (`lean/PositiveGeometryEmergentSpaceTime/BR4.lean`, 5ca8fcd). Transmutation needs one dimensionful boundary value: one unit per sector (counting rule). | Drop classical scale invariance, or accept one unit per sector (then cap 0.25). |
| P2b | Modular invariance fixes the scale | PARTLY DONE (as flavour, not scale) | OOB scan FL-1 #7 (`notes/OUT-OF-BOX-SCAN-2026-10-13.md:96`, 41a8732), never run. Chen–Li–Liu–Ratz 2506.23343 [CITED]: for k_det < 12, det M zeros lie only at i, ω, i∞; hierarchy exponents are integers ≤ k_det; ε (distance from the fixed point) is a **free continuous** modulus. | The modular weights are model choices. ε stays free, so the scale gap moves into ε. |
| P2c | Phase transition | ALREADY CLOSED as scale | SG-1/1b/1c FAIL (b2d5da1), PG-1 NO-GO (75f6b46), SC-1/2/2b PARTIAL, SC-3 step 0 NOT-WELL-POSED (BACKLOG:137). | Same as P2a. |
| P2d | Prereg invariant → mass-ratio dictionary | NEW but high risk | A dictionary choice is a look-elsewhere degree of freedom. FR-MU (BACKLOG) shows that a band ≪ null width is needed. | The dictionary must be fixed before the data. Count it as a trial. |
| P2e | Celestial / twistor modulus | PARTLY DONE (scan only) | OOB scan: celestial has "no data". Celestial CFT is conformal, so BR-4 applies directly. | Needs a scale-breaking datum. |
| P3 | Finish M5 + prereg massive 3/4-pt observable | PARTLY DONE, not ticked | M5 exists as named (MISSION.md:86, unticked). `reviews/LADDER-REVIEW-2026-10-10.md:47` says "M5, M6 … not started", but that predates BH-1 (0cc2ba7, Kerr minimal coupling, Lean) and BH-2 (b770770, massive spinor). Both are formalisation PASSes, non-blind, with no data. | Masses are labels in AHH, so M5 cannot give a mass. Its observable is a GR/SM reproduction (cap 0.25). |
| P4 | Blind test of a published zero-parameter geometric ratio | NEW, but the candidates fail the premise | See B-P4: CCM is not zero-parameter, and Singh self-retracted. | Choose a claim that really is zero-parameter, or reframe the work as method calibration. |
| P5 | More TS-1 predictions | PARTLY DONE | `predictions/TS-1-2026-10-13.md` (635cda7): TS1-1..11 and NU1a–f. | A new entry needs its own prereg and approval. |

### the author's claims checked

| Claim in | Finding | Evidence |
|---|---|---|
| "M1b is a no-go" | **Correct but narrower.** It is a strict-positivity NO-GO: no real (1,3) point is in Gr⁺(2,4), and at n = 5 all planar X > 0 is impossible. The boundary case (X ≥ 0 with some X = 0) is **OPEN**. Lean is D = 4 only. | `reviews/M1b-result-2026-10-11.md` forward note H1 (8998cd6) |
| "F-COULOMB is a quantisation no-go" | **Correct for its scope only.** It covers strict positivity of one deformed amplituhedron (2311.10814): u ∈ (1, ∞), mass ratio free. It is not a no-go for every geometry. | BACKLOG F-COULOMB; FCoulomb.lean 4ec488b |
| "M3 LEC ratio" | **MIS-STATED if read as a no-go.** M3 is a REFUTED miss: L3/L2 = −2 vs −3.79 ± 0.31. | `reviews/M3-result-2026-10-10.md` (b55de05) |
| "thin Markov-trace map" | **Not a recorded no-go.** The nearest text is H-T2: "thin slice of its cell". That is an observation, not a theorem. | `reviews/H-T2-result-2026-10-11.md:28` (28be129) |
| M5 exists as named | **Yes:** MISSION.md:86 "Mass from on-shell structure" (AHH 1709.04891). It is unticked. | MISSION.md |
| Physlib spinor drafts | They are local, never submitted: `drafts/physlib-pr/` (README, PR1–PR3, patch; 81b6d01) and `<local path>` branch `draft/spinor-helicity-null` commit bcba75b. PR2 and PR3 are plans only. | BACKLOG "Outreach" item 3 |
| (implicit) R4-DM as evidence | R4-DM is a meter (0/73), not a no-go. | 200dbbc, e76283d, 4d390a2 |

## B. Steelman and first-principles risk

**P1 Integrality.**
- *Steelman.* Every exact dimensionless number in physics that is not tuned (charge quantisation, Dirac monopole, anomaly cancellation, quantum Hall plateaus, the E8 golden ratio in CoNb₂O₆) comes from an integer or a group. Positive geometry has not yet been asked for any integer beyond definitional ones. F-COULOMB recorded this as the exact missing ingredient.
- *Risk.* In ABHY-type geometries, masses enter as real facet offsets. Every integer invariant of a polytope (face numbers, normalised volume, Euler characteristic, Ehrhart data) is constant on the open chamber of offsets, so an integer cannot select an offset. It can only change at walls, which are codimension-1 linear relations such as thresholds (m_a = m_b + m_c), not isolated ratios [CONJECTURE, to be PROVED in INT-1]. Toric integrality needs a chosen lattice, which is input by hand.
- *Verdict.* Worth one cheap rung that turns this into a theorem. Either it closes P1 for the whole class or it finds the exception.

**P2 Scale.**
- *Steelman.* Dimensional transmutation is the one known way that nature makes a scale from a dimensionless coupling (Λ_QCD).
- *Risk.* Transmutation needs one boundary value g(μ₀), which is exactly one unit per sector. This is the counting rule, and BR-4 is PROVED. Connes–Chamseddine is the cautionary case. hep-th/0610241 [CITED] predicted m_H ≈ 170 GeV from the spectral action at the unification scale. 1208.1030 "Resilience" [CITED] then rescued 125.5 GeV with a singlet σ, a free n (k^ν = √n k^u) and a unification scale u ∈ (25, 35) tuned "on an almost straight curve". The top mass comes out a few % low, and unification is not exact. That is fitting in disguise.
- *Verdict.* Last.

**P3 M5.**
- *Steelman.* The massive spinor-helicity formalism is the natural home for the "masses from on-shell structure" mission rung. BH-1 and BH-2 already formalise Kerr as minimal coupling.
- *Risk.* In AHH, masses are little-group labels, so the formalism cannot output a mass. Any massive 3/4-point observable fixed by on-shell consistency (g = 2, Kerr κ_s = 1) is a GR/SM reproduction (cap 0.25) and is not blind. Its g = 2 version repeats FZ-1.
- *Verdict.* Tick M5 if the author agrees that BH-1/BH-2 meet the pass test. A data rung is low value.

**P4 External stress-test.**
- *Steelman.* A blind test of someone else's claim calibrates our anti-numerology filter on material that we did not build.
- *Risk.* The fetched candidates are not zero-parameter:
  - **CCM (hep-th/0610241, 1208.1030) [CITED].** Input is C⊕H⊕H⊕M₃(C) plus a unification scale and RG running. It was refuted (170 GeV) and then rescued by tuning n and u.
  - **Singh 2508.10131 [CITED].** The v4 abstract claimed "several parameter-free predictions" (δ² = 3/8, √(mτ/mμ) = √(ms/md), √me:√mu:√md = 1:2:3). The latest version (20 Oct 2026, "Exceptional Jordan spectra and conditional fermion mass relations") itself says "δ²=3/8 specifies its normalization rather than a derived physical mass scale". It says selections, centres and the transport rule are model inputs, and "Neither is claimed here". Its own Table 1 at M_Z shows √(mu/me) +25.6%, √(md/me) +27.4%, √(mt/mc) −25.5%, transport R_SM = 0.92459 vs 1 (B_R = 0.012), and up-sector C − 2T + 1 = −9.475 vs 0. A "blind" test by us is redundant, and I am now contaminated because I have read it.
  - **Modular-flavour fits [CITED].** 2506.23343 has ε free. 2502.12662 says τ = ω exactly is excluded (two massless ν), with a deviation of about 0.006. 2409.15823 has 14 real constants.
- *Verdict.* Reframe P4 as MC-1, a method calibration with these as **negative controls**. The positive control is the Coldea E8 golden ratio, which really is zero-parameter but is blocked by DATA-IN-FIGURES (TP-1d, 5495801).

**P5 TS-1.**
- *Steelman.* These are cheap, honest and time-stamped. They are the only route to real blind credit.
- *Risk.* An entry without a geometric derivation is just a forecast of the SM. Credit needs the entry to follow from a mechanism that has zero fitted constants.
- *Verdict.* Feed it from FL-1Z, not by hand.

## C. Rung sketches (PROPOSED, not approved, no prereg written)

### R-A INT-1: "integer invariants are chamber-constant" (P1; gap: DISCRETENESS)

- **One dimensionless target:** the mass ratio u = m_a/m_b in the ABHY/F-COULOMB class. The pre-declared prediction is "not fixed by any integer invariant except at walls".
- **Statement:** for the kinematic associahedron with real offsets c, the combinatorial type (and so every integer invariant built from the face lattice) is locally constant on the open chamber of c. Integer jumps occur only on walls, which are finite unions of hyperplanes. The set of offsets selected by any integer condition is therefore open or codimension ≥ 1, never a discrete set of ratios.
- **Data source:** none. This is a theorem rung, and it moves no data-credit.
- **Kill criterion:** a counterexample in the class, meaning an integer invariant that is non-constant inside a chamber. Then P1 is OPEN and a quantising rung follows.
- **Planted-answer test:** the pentagon (n = 5) with the face vector (5,5) recovered as constant over a random chamber sample. Also a planted wall where two offsets merge, where the face vector must drop. Both are recovered blind by the script before the Lean proof.
- **Lean deliverable:** `IntChamber.faceType_locallyConstant` for the pentagon (extend `Associahedron.lean`), plus `IntChamber.jump_only_on_wall`. These are 0 sorry, standard axioms.
- **CPU cost:** low (about 1–2 h of Lean, seconds of scripts).
- **What closes:** it extends F-COULOMB from one geometry to the "integers from the polytope itself" class. It names the drop-assumption for any future P1 attempt: the integers must come from an external discrete datum (lattice, flux, modular weight).

### R-B FL-1Z: modular fixed-point integrality → blind neutrino entry (P1 + P5; gap: DISCRETENESS)

- **One dimensionless target:** the neutrino mass ordering plus one ε-independent correlation at a fixed point (i or ω) of a single pre-chosen minimal modular model. One example is the sign or band of |m_ββ|/√Δm²_atm. It is fixed before any fit.
- **Mechanism:** SL(2,ℤ) forces the critical points i, ω, i∞. The valence formula forces integer hierarchy exponents ≤ k_det (2506.23343) [CITED]. Ratios of logs cancel ε at leading order [CONJECTURE].
- **Data source:** future JUNO / DUNE / Hyper-K ordering and δ_CP, plus 0νββ (KamLAND-Zen, LEGEND). Entry goes into TS-1, time-stamped.
- **Kill criteria:**
  - (i) The model needs ≥ 1 continuous coefficient fitted to oscillation data before the entry: then it is a fit (cap 0.25 or 0).
  - (ii) The modular weights are not unique given the declared rules: then the integers are by hand, which is the author's kill.
  - (iii) The prediction does not depend on the fixed point: then it is not discrete.
- **Planted-answer test:** reproduce the published "τ = ω exactly ⇒ two massless ν" exclusion (2502.12662) and the ε², ε³ bounds (2506.23343) from a planted model. Both must come out before the live model is opened.
- **Lean deliverable:** the valence-formula count for weight k < 12 (zeros at i, ω, i∞ only) as a finite combinatorial lemma on k = 4a + 6b + 12c, `FL1Z.valence_lt12`. This is cheap.
- **CPU cost:** low to medium.
- **Risk:** the charged-lepton log-ratio is CONTAMINATED (masses are memorised), so only the neutrino sector is blind. A binary ordering alone cannot reach p < 0.01, so a correlated band is needed.
- **EV:** low (≈0.05), but it is the only fetched mechanism with real discreteness.

### R-C MC-1: anti-numerology filter calibration (P4 reframed)

- **Target:** does our counting rule plus p < 0.01 filter flag the known hidden parameters? These are CCM's n and u, and Singh's δ normalisation, selections and transport rule. The positive control is the E8 golden ratio (TP-1e digitisation).
- **Kill:** the filter scores either negative control as zero-parameter.
- **Lean:** none.
- **CPU:** trivial.
- **Credit:** 0 to the mission. Method only.

### R-D M5-K: Kerr κ_s = 1 vs GW spin-induced quadrupole bounds (P3)

- **Target:** κ_s.
- **Data:** GWTC tests of GR. The source must be fetched at prereg; it is not CITED here.
- **Kill:** none informative, because κ_s = 1 is GR.
- **Credit:** cap 0.25, non-blind. Reuses BH-1 Lean. Low priority.

### Ranking

1. **INT-1** (cheap, decisive for P1, generalises F-COULOMB).
2. **FL-1Z** (the only mechanism found with forced integers; produces TS-1 entries).
3. MC-1 (method only).
4. M5-K, and ticking M5 on the BH-1/BH-2 evidence.
5. P2 sub-ideas.

This differs from the author's order (1 > 2 > 3 > 4 > 5) only in pushing P2 to last and P4 below P5/FL-1Z. Reason: BR-4 is PROVED, and the P4 candidates fail the zero-parameter premise.

## D. Backlog table (all PROPOSED, nothing approved)

| ID | From | Gap | Status | EV (rough) | Cost | Needs |
|---|---|---|---|---|---|---|
| INT-1 | P1 | discreteness | PROPOSED | 0.03 (closure) | low | The author go + prereg |
| FL-1Z | P1+P5 | discreteness | PROPOSED | 0.05 | low–med | The author go + prereg; TS-1 entry approval |
| MC-1 | P4 | method | PROPOSED | 0 (method) | trivial | The author go |
| M5-tick | P3 | quantum numbers | DECISION | — | none | The author: do BH-1/BH-2 meet MISSION.md:86 pass test? |
| M5-K | P3 | — | PROPOSED | ≤0.25 capped | low | The author go + prereg |
| P2-x | P2 | scale | PARKED | ≈0 under BR-4 | — | a stated dropped assumption |

## Approvals needed (the author)

1. A go/no-go on INT-1 and/or FL-1Z. Each needs a dated prereg in `prereg/` before it runs.
2. Whether to resume AutoResearch. It stays paused until then.
3. Whether to tick M5 on BH-1 and BH-2.
4. Whether to add any new TS-1 entries.
5. Whether to run MC-1 as a method check.
