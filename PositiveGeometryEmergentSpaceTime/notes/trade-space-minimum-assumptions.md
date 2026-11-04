# Trade space: minimum assumptions for M0–M6

*10 Oct 2026. This analysis is for the author to decide on. `MISSION.md` is **not** changed.*

- **Level:** everything here is vyāvahārika (mathematics, physics, Lean).
- **Tags:** as in `MISSION.md`. In addition, **[CHECKED]** means I verified it myself this session, either by a Lean run (`scripts/positivity_audit.lean`, output in `scripts/positivity_audit_output.txt`) or by reading the cited paper's abstract or text.

**Short answers:**
- **(a)** M0 doesn't need to be thrown away. It needs to be **re-scoped**. Gr(2,4) is the right object for *points and lines* (spacetime points, loop variables). It is the wrong object for *particles and interactions*, which live in Gr(k,n), or in polytopes in kinematic space, with n = the number of particles.
- **(b)** No. M2 does not have to assume positivity. Positivity can be an axiom, can be derived, or can be dropped. Of these, the **derived** routes are both the most interesting and the only ones already tied to real-world data.

---

## 1. Assumptions currently baked into M0–M6

**N** = necessary for the current programme to mean anything · **C** = convenient (a choice that makes the work tractable) · **A** = arbitrary (a historical accident of the 2026 paper)

| # | Assumption | Where | N / C / A | What dropping it costs |
|---|---|---|---|---|
| 1 | The base object is a Grassmannian | M0–M2 | **C** | Little. Polytopes in kinematic space (associahedron, surfacehedra) and cosmological polytopes are positive geometries that aren't Grassmannians [CITED: Arkani-Hamed–Bai–He–Yan 2017; Arkani-Hamed–Benincasa–Postnikov 2017]. You lose the twistor picture of spacetime. |
| 2 | k = 2, n = 4 | M0 | **C** for spacetime points. **A** if read as "the seed". | Nothing, if Gr(2,4) is kept as one layer. Particle physics needs n = number of particles and general k (§2). |
| 3 | Real field (ℝ, ℚ) | M0, M2 | **C** | Real numbers are needed to *state* positivity. Complex numbers are needed for Lorentzian spacetime via Hermitian matrices, and for generic momenta. [CHECKED] Most of the core already works over any commutative ring or field, so it carries over to ℂ for free (§5). |
| 4 | Positivity | M0 (witness point), M2 | **Open question** (this note's §3) | Without it there are no positive geometries or canonical forms in the ABL sense, and the generic matroid strata are wild. You keep all the algebra (Plücker, Klein, null momenta). |
| 5 | The target is 4D spacetime | M1 | **N** for contact with LHC data | Kinematic-space polytopes work in "general spacetime dimensions" [CITED: ABHY 2017 abstract], so the geometry need not presuppose 4D. Only the data comparison does. |
| 6 | Twistor identification (Klein correspondence) | M0, M1 | **C** | Classical [CITED: Penrose, "Twistor Algebra", 1967]. Dropping it loses the "spacetime point = line in P³" picture. Momentum twistors use a *different* dictionary [CITED: Hodges, arXiv:0905.1473]. |
| 7 | The canonical form plays the role of dynamics or "volume" | M0–M5 | **C**, verging on **N** for the positive-geometry programme | Positive geometries are *defined* by having a canonical form: a unique form with logarithmic singularities and recursive residues [CHECKED: ABL 1703.04541 §2]. ABL also define **pseudo-positive geometries** (§2.2 there), a slightly weaker variant. Drop the form and you need some other dynamical principle. |
| 8 | Lean 4 + Mathlib as the formal base | all | **C** | Coq, Isabelle or exact computer algebra would also work. Lean is cheapest given what already exists. |
| 9 | The Standard Model as the target | M3–M6 | **N** (tier-1 evidence) | Nothing to drop. But the *order* matters. Real-world contact may come sooner through **pions** (the non-linear sigma model, NLSM, sits inside Tr(φ³) [CITED: arXiv:2401.05483]) or through **EFT positivity bounds** (§3) than through the electroweak sector. |
| 10 | Planarity and large N (implicitly, via the amplituhedron) | M2, M5 | **C** | The real world isn't planar. The curve-integral programme reaches all orders in the topological ('t Hooft) expansion for Tr(φ³) [CITED: arXiv:2309.15913]. |
| 11 | Supersymmetry (implicitly, via planar N=4) | M2 | **A** with respect to the mission | The real world isn't supersymmetric at accessible energies. Use the non-supersymmetric positive geometries (Tr(φ³), NLSM) as the main track. |
| 12 | Massless kinematics | M0–M2 | **C** | Masses need the massive spinor-helicity formalism [CITED: Arkani-Hamed–Huang–Huang, arXiv:1709.04891]. This is M5. |
| 13 | One structure ("seed") boots up everything | mission | **SPECULATION**, as a motivation | Keep it as the vision, not as an axiom in any theorem. |

---

## 2. The dimension question: what Gr(2,4) gives vs higher objects

### What Gr(2,4) actually gives

- **2-planes in ℂ⁴ are lines in twistor space ℂP³, i.e. points of compactified complexified Minkowski space.** The Plücker relation P₀₁P₂₃ − P₀₂P₁₃ + P₀₃P₁₂ = 0 is the Klein quadric. Two spacetime points are null-separated exactly when their twistor lines meet [CITED: Penrose 1967; PROVED: Lean, `UOPG0/Klein.lean`, `nullSeparation_iff`].
- **Real Gr(2,4) gives split signature (2,2).** Real Minkowski space is the real slice picked out by a Hermitian structure, not by positivity. [PROVED: Lean, `Klein.lean`, for det(x−y)=0 over any field; the signature issue is from the earlier UOPG review.]
- **A second natural role: loop momenta.** In the amplituhedron, each loop is a **line (AB) in momentum-twistor space**, which is again a point of Gr(2,4) [CITED: Arkani-Hamed & Trnka, arXiv:1312.2007].

So Gr(2,4) is natural as a **point/loop layer** in two different dictionaries.

### What higher objects give

| Object | What it encodes | Status |
|---|---|---|
| **Gr≥0(k,n) and its positroid cells** (decorated permutations, plabic graphs) | Combinatorics of on-shell diagrams for n particles | Mathematics: theorem [CITED: Postnikov, math/0609764]. Physics link to planar N=4 on-shell diagrams: established [CITED: arXiv:1212.5605] |
| **Momentum twistors** Zᵢ ∈ ℂP³, i = 1…n (a point of Gr(4,n) modulo torus) | n-particle planar kinematics with momentum conservation built in | Established [CITED: Hodges, arXiv:0905.1473] |
| **Tree amplituhedron** A(n,k,m) ⊂ Gr(k, k+m), m = 4 | Planar N=4 tree amplitudes | The BCFW cells **triangulate** it (a theorem) [CITED: Even-Zohar, Lakrec & Tessler, arXiv:2112.02703, *Invent. Math.* 2025]. "Canonical form = tree amplitude" then follows from BCFW recursion [my inference; not separately checked] |
| **Loop amplituhedron** | All-loop planar N=4 integrand | [CONJECTURE] with extensive checks [CITED: 1312.2007]. I did not find a general proof |
| **Sign-flip / winding description** | An equivalent "binary" definition of the amplituhedron; locality and unitarity follow | [CITED: Arkani-Hamed, Thomas & Trnka, arXiv:1704.05069] |
| **Cluster algebras of Gr(4,n)** | Symbol letters of planar N=4 amplitudes; the hexagon/heptagon bootstrap (the nine-loop result sits here) | [CITED: Golden et al., arXiv:1305.1617]: two-loop MHV amplitudes are written in cluster coordinates on Conf_n(P³) |
| **Totally nonnegative flag varieties** | Generalisations of Gr≥0 | Surveyed [CITED: Lam, "An invitation to positive geometries", arXiv:2208.05407] |
| **Kinematic associahedron** | Tree amplitudes of the bi-adjoint φ³ scalar, directly in kinematic space, **in general dimension**. "Locality and unitarity … fully determined by the geometry" | [CITED: Arkani-Hamed, Bai, He & Yan, arXiv:1711.09102, *JHEP* 05 (2018) 096] |
| **Surfacehedra / curve integrals** | Tr(φ³) at all loops and all orders in the topological expansion; no Feynman diagrams | [CITED: Arkani-Hamed, Frost, Salvatori, Plamondon & Thomas, arXiv:2309.15913, *JHEP* 08 (2025) 194] |
| **NLSM ⊂ Tr(φ³)** | **Pion** amplitudes obtained from Tr(φ³) by a kinematic shift, extending to all loops in the planar limit | [CITED: Arkani-Hamed, Cao, Dong, Figueiredo & He, arXiv:2401.05483] |
| **Cosmological polytopes** | Wavefunction of the universe in toy FRW cosmologies | [CITED: arXiv:1709.02813] |
| **Tropical Grassmannian and generalised bi-adjoint amplitudes (k ≥ 3)** | Positive geometry beyond k = 2 for "CEGM" amplitudes (the k ≥ 3 generalisation by Cachazo, Early, Guevara and Mizera) | [CITED: Speyer & Sturmfels, math/0304218; CEGM, arXiv:1903.08904]. Physical meaning beyond k = 2: open |

### Recommendation on (a)

- **Keep Gr(2,4) as the point/loop layer** ("spacetime points and loop lines"). The existing M0 Lean work is reusable there as-is.
- **Add a separate particle/interaction layer, and keep it switchable:**
  - **L-A:** Gr≥0(k,n) → amplituhedron (planar N=4; supersymmetric, not real-world).
  - **L-B:** kinematic-space polytopes. Associahedron → surfacehedra → NLSM. These are non-supersymmetric, work in any dimension, and **reach pions**, which are real particles.
- **Prefer L-B as the main track toward real particles.** L-A remains the best-developed mathematics. [Recommendation; the physics status is as tagged in the table.]
- **What is not established:** that any of these layers describes the Standard Model, or that a single "seed" generates both layers [SPECULATION].

---

## 3. The positivity question: does M2 have to assume it?

### Options

| Option | Meaning | Examples | What it buys | What it costs |
|---|---|---|---|---|
| **(i) Axiom** | Start from Gr>0 / Gr≥0 | Current UOPG (`chart_minors_pos`, `positive_gauge_chart`); amplituhedron with positive external data Z | Canonical forms, triangulations, theorems | Planar-N=4 flavour; the "why positivity?" question is left open |
| **(ii-a) Derived from unitarity, causality and analyticity** | Positivity is a *consequence* of physical principles | **EFT positivity bounds:** certain coefficients "must be strictly positive to ensure UV analyticity" [CITED: Adams et al., hep-th/0602178]. The **EFThedron** finds "a hidden 'totally positive' structure" from causality and unitarity [CITED: Arkani-Hamed, Huang & Huang, arXiv:2012.15849] | **Real-world, tier-1-testable.** Adams et al. note that negative anomalous quartic W/Z couplings at colliders would falsify local QFT | Gives inequalities, not a spacetime |
| **(ii-b) Derived from pole structure** | Fix the form by its singularities; the positive region is then the one whose boundaries are the physical poles | Kinematic associahedron: positivity of planar variables is chosen so that the facets are exactly the propagator poles [CITED: ABHY 2017] | Ties positivity to locality | Still a choice of region |
| **(ii-c) Derived from positive weights on a network** (the Markov-network branch) | Positive edge weights imply a point of Gr≥0 | Postnikov's boundary measurement: positive weights on a planar network give a point of Gr≥0 [CITED: math/0609764]. **Electrical networks:** conductances give a point of Gr≥0(n−1, 2n) [CITED: Lam, arXiv:1402.6261]. **Reversible Markov chains are exactly random walks on electrical networks**, with conductances C_xy = w_x P_xy [CITED: Doyle & Snell, math/0001057] | **Keeps the transition probabilities**, unlike *Fusions*' map, which keeps only class structure. Positivity is then *inherited from probabilities being positive* | Needs reversibility and a circular-planar graph with boundary nodes. Physical meaning: [CONJECTURE] |
| **(iii) Drop it** | General Gr(k,n), matroid strata, tropical geometry | Speyer–Sturmfels; CEGM | Maximum generality; complex kinematics | Generic matroid strata are notoriously badly behaved; positroid cells are the well-behaved, cell-like part [CITED: Postnikov]. No canonical forms in the ABL sense |
| **(iv) A weaker condition** | Sign flips or winding instead of positive minors | The amplituhedron "can be fully described in binary … locality and unitarity … easily derived" [CITED: arXiv:1704.05069]; pseudo-positive geometries [CHECKED: ABL §2.2] | A topological/combinatorial condition, possibly closer to physics | Still uses positive external data Z in the amplituhedron case |

### Is positivity physically fundamental or a planar-N=4 artefact?

- **Evidence that it's more than an artefact:**
  - It appears outside N=4: the bi-adjoint φ³ associahedron in any dimension, cosmological polytopes, surfacehedra / Tr(φ³) at all loops, pions via NLSM ⊂ Tr(φ³) [CITED, all above].
  - It also appears independently from **causality and unitarity** in real-world EFTs [CITED: Adams et al. 2006; EFThedron 2021].
- **Evidence that it's limited:**
  - The *Grassmannian* positivity (Gr>0, the amplituhedron) is established only for planar N=4.
  - The non-planar and Standard Model cases have no positive-geometry formulation that I found.
  - The real-signature issue: positive real twistor data naturally live in split signature (2,2).
- **What breaks without positivity:** canonical forms in the ABL sense (they are defined for positive or pseudo-positive geometries), triangulation theorems, and the "locality and unitarity emerge" story. The algebra and the twistor geometry survive (§5).

### Recommendation on (b)

- **M2 should not assume positivity. It should test which positivity is forced.**
- The cleanest falsifiable variant is **(ii-a)**: derive a positivity statement from unitarity, causality and analyticity, and compare it with data.
- The most mission-specific variant is **(ii-c)**: derive Gr≥0 from positive Markov/electrical weights. This is the Markov-network branch, and it is richer than *Fusions*.

---

## 4. The minimal kernel proposal

**The smallest assumption set that still allows a falsifiable step:**

- **K1, a base object:** a complex projective variety with a combinatorial stratification. The default is Gr(k,n) over ℂ, with real structures (Hermitian, split, positive) as options rather than axioms.
- **K2, a form principle:** the observable is a differential form, fixed by its singularities and residues (canonical-form logic), on whatever region an option selects.
- **K3, an explicit dictionary:** a pre-registered map from geometric quantities to measured observables, stated *before* computing (MISSION M4).
- **K4, a formal base:** Lean 4 + Mathlib, or exact arithmetic for numerics.

Positivity, k, n, the layer (point vs particle), the spacetime signature and the theory (N=4 / Tr(φ³) / NLSM / EFT) are all **switchable options**.

**The smallest falsifiable step under this kernel:**
- **Branch P-EFT:** formalise the simplest dispersion-relation positivity bound (the sign of the forward s² coefficient) in Lean.
- **Then:** confront it with a tier-1 measured or bounded EFT coefficient. Adams et al. name anomalous quartic gauge couplings.

This is falsifiable *by data*, which no current UOPG rung is. [Proposal; the physics behind it is CITED; the specific Lean target is new work.]

### Proposed diff (Applied 2026-10-10)

*Applied to MISSION.md on 10 Oct 2026 with the author's approval, together with the minimal kernel K1–K4 and matching updates to kill criteria 1 and 2.*

```diff
- | **M0** ✅ | Gr⁺(2,4) algebra in Lean | Done: no `sorry` | done |
+ | **M0** ✅ | Point/loop layer: Gr(2,4) algebra in Lean (Plücker, Klein, null momenta, rank-one), valid over any field; positive-chart results as one option | Done: no `sorry`; positivity used in 8 of 161 theorems | done |
+ | **M0′** | Particle layer, chosen from the options: L-A Gr≥0(k,n)/amplituhedron, or L-B kinematic associahedron → surfacehedra → NLSM | Lean statement of one n-particle object (e.g. the n=5 associahedron facets ↔ planar propagators) | moderate |
- | **M2** | **Make positivity do work.** Find one physically meaningful statement that is *false* without positivity and *true* with it … | A Lean theorem whose proof genuinely uses positivity, and a counterexample without it | Hard … |
+ | **M2** | **Find out which positivity, if any, is forced.** Pick one branch: (P-EFT) derive a positivity bound from unitarity + analyticity; (P-Net) derive Gr≥0 points from positive network/Markov weights; (P-Pole) derive the positive region from the physical poles. Record branches that fail. | A Lean theorem in which positivity is a **conclusion**, not a hypothesis, plus a stated data comparison (P-EFT) or counterexample | Hard; P-EFT has the shortest path to tier-1 data |
```

### Trade-space table

| Option | Assumption | What it buys | Risk | Test |
|---|---|---|---|---|
| **Pt-Gr24** | Gr(2,4) as the point/loop layer | Reuses all of M0; the twistor picture | Mistaking it for "the seed" | M1 Hermitian signature theorem |
| **L-A** | Particle layer = Gr≥0(k,n) / amplituhedron | Deepest mathematics; proved BCFW triangulation | Planar N=4 only (supersymmetric) | Lean: an n=5 or n=6 positroid-cell / canonical-form fact |
| **L-B** | Particle layer = kinematic polytopes (associahedron → surfacehedra → NLSM) | Non-supersymmetric, any dimension, **reaches pions** | Colour-ordered, scalar-centric; the SM gauge sector isn't covered | Lean: associahedron facets ↔ planar poles for n=5 |
| **P-Ax** | Positivity as an axiom | Canonical forms immediately | Unmotivated; the "why?" question stays open | Must still pass M2 |
| **P-EFT** | Positivity from unitarity + causality + analyticity | **Tier-1 falsifiable** | Gives bounds, not a spacetime or a "seed" | Lean dispersion bound, then a data sign check |
| **P-Pole** | Positive region fixed by the physical poles | Links positivity ↔ locality | Circular, if the poles are put in by hand | Derive the region without listing the poles first |
| **P-Net / H-Markov** (the Markov-network branch) | Reversible Markov kernel → conductances → Gr≥0(n−1,2n) (Lam) | Keeps probabilities; positivity *derived*; a real bridge to conscious-agent dynamics | Reversibility and planarity restrictions; physical meaning is [CONJECTURE] | ~~Lean: a 2-node network → Gr≥0(1,4)~~ done (H-T1). H-T2: cells = Lam's medial-pairing cells; the canonical form is combinatorial (dlog conductances), not amplitude-like without kinematics |
| **H-Fusions** | *Fusions* Definition 2 (communicating classes → decorated permutation) | Already computed (`scripts/fusions_check.py`) | Discards all probabilities; not onto; **H-T2: a strict coarsening of Lam's network cell** (only connectivity survives) | Superseded by Lam's map for networks |
| **P-None** | Drop positivity (matroid / tropical) | Generality, complex kinematics | Wild strata; no canonical forms | Only worth taking up if every positive branch fails |
| **Sig-H** | Hermitian real slice for (1,3) | Real Minkowski space | Positivity becomes harder to state | M1 |
| **Sig-S** | Stay in split (2,2) | Positivity is natural there | Not our spacetime | Only acceptable if the physics comes through the particle layer instead |

### Mass scale options (from sweep)

*Added 10 Oct 2026. Source: `notes/positive-geometry-entropy-sweep-2026-10-10.md`.*

| Option | Where the scale comes from | Status | Verdict for M3 |
|---|---|---|---|
| **S-Planck** | M_P = √(ħc/G), from G and ħ (holography, S = A/4L_P²) | [CITED] | The only scale gravity supplies. Even Jacobson 1995 takes G as an input. It is 10¹⁹ GeV, not a GeV. |
| **S-Species** | Λ_sp ≈ M_P/√N_sp, from black-hole entropy and counting (Dvali 0706.2050; vdHVWW 2212.06841) | [CONJECTURE] | A real "scale from counting states", but ≤ M_P and needs N as an input |
| **S-QCD** | Λ_QCD from running coupling (dimensional transmutation) | [CITED] | Sets hadron masses but is **not geometric**. Taking it as an input is honest. |
| **S-Input** | Keep M_π and F_π as measured inputs (as in M2d–M2f) | — | Current practice. Fine as long as M3 targets are dimensionless. |
| **D-Chiral** | a₀⁰/a₀² = −7/2 (M2f) | [CITED], Weinberg 1966 | Fixed by chiral symmetry. The geometry **reproduces** it. Pre-register it as a reproduction, not a prediction. |
| **D-Beyond** | A ratio where geometry claims more than chiral symmetry (e.g. NLO l̄ᵢ ratios from EFT-hedron plus a stringy/curve-integral completion) | open | The sane M3 target: falsifiable against Colangelo–Gasser–Leutwyler 2001 |

**Recommendation:** M3 stays scale-free. No credible literature route gives a GeV from geometry alone, so any "scale" claim would need extraordinary evidence.

---

## 5. Lean check: where positivity is actually used [CHECKED]

`scripts/positivity_audit.lean` ran against UOPG `mvp0/lean` after a fresh `lake build UOPG0` (Lean 4.34.1, Mathlib 4.34.1). Full output is in `scripts/positivity_audit_output.txt`.

- **161 theorems total.** Only **8** involve an order relation in a substantive way:
  - **7** assume an ordered field plus strict-positivity hypotheses: `chart_minors_pos`, `chartCoord_pos`, `positive_gauge_chart`, `face_{x,y,z,w}_P13_pos`.
  - **1** is the concrete witness over ℚ: `positiveExample_minors_pos`.
  - Two more hits (`vec2_mk_zero`, `vec2_mk_one`) are artefacts: `0 < 2` there is a *vector index* bound, not positivity.
- **`plucker_relation`** has UOPG0 dependencies {`plucker`, `pluckerQuad`} only. It does not use `<` or `≤`, and it holds over **any commutative ring** (`variable [CommRing α]`).
- **`nullSeparation_iff`, `det2_eq_zero_iff_exists_outer` and `parkeTaylorCoeff_eq_inv_cyclic`** don't use order either. They are stated over a general `Field` or `CommRing`.
- **What this implies:**
  - The Plücker, Klein, null-momenta, rank-one and Parke–Taylor results transfer to **ℂ unchanged**. M1's complexification costs nothing for them; only the Hermitian real structure is new.
  - Positivity currently does **no work** outside the chart/orthant lemmas. That matches the review's "positivity unused" gap, and it backs answer (b).
- **No repo files were modified.** The audit script was copied into `mvp0/lean` temporarily, run, and removed. The rebuilt `.lake` artefacts in `<local path>` are local only.

---

## Unverified or limited items

- **Tree-level "amplituhedron = amplitude":** that it follows from the BCFW triangulation plus BCFW recursion is my inference, and I didn't check it in a source.
- **Loop amplituhedron:** I found no general proof, but I didn't search exhaustively.
- **"Non-planar / SM: no positive-geometry formulation":** this rests on an absence in my searches, not on a source that says so.
- **"Generic matroid strata are badly behaved":** I didn't fetch the Mnëv / Gelfand–Goresky–MacPherson–Serganova universality sources.
- **Lam's electroid embedding:** I verified the abstract only. The exact form of the map, and which graphs it covers, should be read before any Lean work.
- **Adams et al. on anomalous quartic couplings:** quoted from the abstract. Whether current LHC bounds already test the sign: not checked.
