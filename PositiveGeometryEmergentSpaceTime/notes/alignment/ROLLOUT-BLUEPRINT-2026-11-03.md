# Rollout: prose-to-Lean blueprint rows for every rung (2026-11-03)

Scope (author approved 2026-11-03): blueprint rows only, every rung, plus glossary and DEF rows. No sanity theorems, no blind versions, no paper edits (edits are proposed below), no new builds.

## What was run

- `tools/alignment/extract.py`: parses all `lean/PositiveGeometryEmergentSpaceTime/**/*.lean` (declaration index) and the three papers (every PROVED / `\lean` / 'Lean proves' / listing sentence) → `out/claims.json`.
- `tools/alignment/verdicts.py`, `defs_glossary.py`: the judgements (one entry per claim row, DEF row and glossary term; every Lean name checked against the index).
- `tools/alignment/build.py` → `blueprint.tsv`, `BLUEPRINT-ALL.md`, `GLOSSARY.md`, `out/BlueprintCheck.lean`; `rollout.py` → this file.
- One batched check, `cd lean && lake env lean ../tools/alignment/out/BlueprintCheck.lean` (44 s wall, CPU, existing oleans): **all 409 cited declarations exist; 384 use only standard axioms (propext / Classical.choice / Quot.sound), 25 use none; no sorryAx, no error.** Output: `tools/alignment/out/BlueprintCheck.out`.
- `lean/AxiomsAll_output.txt` unchanged: TOTAL theorems=1378 defs=798 nonstandard=0, sorry_dependent=0. No Lean file edited; `PositiveGeometryEmergentSpaceTime.lean` untouched.

## Counts

- Rows: 186 total = CLAIM 69, DEF 28, LISTING 11, META 55, PAPER 6, SCOPE 17. PAPER and META rows are listed but not judged.
- Rungs with judged rows: 23 (+ GENERAL rows about the whole programme): BR-4, CAPPED-FORMAN-1, CASCADE-1, CASCADE-1b r2, CHIRAL-LATTICE-1, CURV-LEAN, EW-Z1b, FL-1Z, GRADED-POSITROID, H-T5, HG-DIM-1, HG-DIM-2, INT-1, JORD-1, LEAN-CERT-1, LEAN-CERT-2, M3, MR-1b, MR-3, RG-IR-1, RP-TN-1, SURF-1′, TRIALITY-WHY.
- Verdicts over the 125 judged rows: MATCH 108, NAME-ONLY 8, OVERSTATES 9. UNDERSTATES 0, MISSING-LEAN 0.
- By type: CLAIM: MATCH 59, NAME-ONLY 1, OVERSTATES 9; LISTING: MATCH 11; SCOPE: MATCH 17; DEF: MATCH 21, NAME-ONLY 7.
- Glossary (34 terms): DEFINED 18, MISMATCH 4, MISSING-IN-PAPER 12.
- Pilot reuse: SURF-1′, HG-DIM-1 and RG-IR-1 rows cite `PILOT-2026-10-31.md` and the Alignment modules; no new pilot work.

## Non-MATCH claim rows and proposed rewordings (papers not edited)

### II:65 — GENERAL — OVERSTATES

- Reason: Omits the paper-proved and conjecture tags that the paper uses (e.g. HG-DIM-1 \PAPERPROVED).
- Lean: 
- Proposed rewording: Every claim carries one status tag: proved in Lean, proved on paper, computed in a preregistered simulation with locked checkers and planted controls, cited, or conjectural.

### II:95 — MR-1b — OVERSTATES

- Reason: Abstract: 'blind LS coupling ratios 5/16 and 49/240 PROVED' has the same gap as the MR-1b card.
- Lean: LSResidue.rho3_ratio, LSResidue.f4_ratio
- Proposed rewording: ... blind Lovelace--Shapiro coupling ratios $5/16$ and $49/240$ (Legendre arithmetic \PROVED; coefficient-to-coupling map a stated convention) agree with both width sources ...

### II:96 — SURF-1′ — OVERSTATES

- Reason: Abstract drops the model scope the pilot said abstract-level wording must carry.
- Lean: Surf1.no_sign_coherent_N
- Proposed rewording: SURF-1$'$: in the d-type $\mathrm{Tr}\,\phi^3$ colour model, no $N\ge3$ makes the one-loop colour factors of the triangle-type and crossed-box ($K_{3,3}$) graphs sign-coherent \PROVED; robust under the convention re-check \SIM.

### II:302 — MR-1b — OVERSTATES

- Reason: Lean proves the residue decompositions and the ratio arithmetic; the coefficient->coupling map is not mechanised (module docstring says so). 'The ratios ... are PROVED' reads as the physical coupling ratios.
- Lean: LSResidue.rho3_residue, LSResidue.f4_residue, LSResidue.rho3_ratio, LSResidue.f4_ratio
- Proposed rewording: The Legendre decompositions of the $\rho_3$ and $f_4$ residues (\leanname{rho3\_residue}, \leanname{f4\_residue}) and the arithmetic giving $5/16$ and $49/240$ from their coefficients (\leanname{rho3\_ratio}, \leanname{f4\_ratio}) are \PROVED; the step from Legendre coefficient to coupling ($g^2\propto$ coefficient$/(2J+1)$, normalised to $g_\rho^2=1/2$) is a stated convention, not in Lean.

### II:438 — JORD-1 — OVERSTATES

- Reason: Group vs algebra: Lean is about derivations (the Lie algebra), the prose and heading say 'gauge group'.
- Lean: Jord1.gsm_not_pointwise_stabiliser
- Proposed rewording: We proved that the SM gauge algebra $\mathfrak g_{\rm SM}=\mathrm{stab}(E_1)\cap\mathrm{setstab}(h_3(\mathbb C))\subset\mathrm{Der}\,J_3(\mathbb{O})$ (over $\mathbb{Q}^{27}$) is not the pointwise stabiliser, within $\mathrm{Der}\,J_3(\mathbb{O})$, of any subset of $J_3(\mathbb{O})$ \PROVED. (Heading II:430: ``the SM algebra is not a pointwise stabiliser''.)

### I:42 — GENERAL — OVERSTATES

- Reason: Paper I abstract tag list omits paper-proved (\PAPERPROVED, defined at I:47).
- Lean: 
- Proposed rewording: Every claim carries one epistemic tag (Lean-proved, paper-proved, simulated, cited, conjecture, speculation).

### I:420 — GENERAL — OVERSTATES

- Reason: Counterexamples: MR-1b coefficient->coupling step, HG-DIM-1 general-n per-edge formula and CAPPED-FORMAN-1 general bound are on paper.
- Lean: 
- Proposed rewording: Every lemma tagged \PROVED{} is proved in Lean~4 on Mathlib; steps proved only on paper are tagged \PAPERPROVED{}.

### I:805 — GENERAL — NAME-ONLY

- Reason: 'ratio families ... stay free (PROVED)' names no declaration; freedom is proved per rung only in some cases.
- Lean: IntChamber.invariant_chamber_constant, MassiveLS.positivity_forces_chiral, Cascade1.em_n5_zero_iff
- Proposed rewording: ... stay free under the positivity and integrality constraints we studied (\PROVED{} where a rung names its Lean module, e.g.\ \texttt{IntChamber}, \texttt{Cascade1}; otherwise \SIM).

### C:69 — HG-DIM-1 — OVERSTATES

- Reason: Contribution (I) carries the same \lean tag.
- Lean: HgDim1.edge_neg, HgDim1.edge_pos
- Proposed rewording: \lean{}\,(two $\K_7$ edges: matching cost and potential gap; reduction on paper)

### C:201 — HG-DIM-1 — OVERSTATES

- Reason: \lean tag on the theorem reads as 'Ollivier curvature of two K7 edges checked'; Lean checks optimal-matching cost and a 1-Lipschitz potential gap between listed sets.
- Lean: HgDim1.edge_neg, HgDim1.kappa_neg, HgDim1.edge_pos, HgDim1.kappa_pos
- Proposed rewording: \lean{}\,(two edges of $\K_7$: optimal matching cost and matching potential gap between the listed closed neighbourhoods; the reduction to Ollivier curvature is on paper, \cref{sec:lean})

MISSING-LEAN: none. Every prose PROVED / `\lean` claim the extractor found resolves to existing, axiom-clean declarations; the gaps are in what the prose says those declarations mean.

## DEF rows not MATCH (hidden-definition risk)

NAME-ONLY means a headline theorem is about this Lean object, and its identification with the object the paper names is in a name, docstring or generating script only.

- `IsingTiling.C` (H-T5, lean/PositiveGeometryEmergentSpaceTime/IsingTiling.lean:21): one certified rational point of OG(3,6); 'star network' (II:326) is not in Lean or defined in the paper.
- `FL1Z.D3` (FL-1Z, lean/PositiveGeometryEmergentSpaceTime/FL1Z.lean:61): literal 3×3 matrix 'Eq. (D.3) of 2502.12662 at τ=ω'; that this is the Zee--Babu neutrino mass matrix is a transcription, no theorem.
- `EWZ1b.N` (EW-Z1b, lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean:25): script-generated (sims/ewz1b/mklean.py) residual of A[1234] already restricted to the CGW zero locus; faithfulness to the Feynman rules is not in Lean. Rung status DERIVED (conditional) is the right tag.
- `LeanCert2.frwzw_k0p_Mr` (LEAN-CERT-2, lean/PositiveGeometryEmergentSpaceTime/LeanCert2/FrwzwK0p.lean:20): fusion-rule matrices are script data; no theorem ties them to WZW fusion rules (the rung is a method rung that moves no ledger value).
- `Surf1.boxU` (SURF-1′, lean/PositiveGeometryEmergentSpaceTime/Surf1/Box/Graph.lean:28): half-edge lists; '≅ K3,3' is a docstring identification. Pilot cross-check is SIMULATED; the prism gives the opposite sign, so it matters (disclosed at II:421).
- `Surf1.ttU` (SURF-1′, lean/PositiveGeometryEmergentSpaceTime/Surf1/Box/Graph.lean:32): '≅ double square' by docstring; pilot kernel check (blind_dsq) confirms the Laurent data, i.e. PROVED equal colour data.
- `HgDim1.NA_neg` (HG-DIM-1, lean/PositiveGeometryEmergentSpaceTime/HgDim1.lean:93): hand-listed 'closed neighbourhoods'; no theorem that they are {v | v = 2 ∨ adj 2 v}. Same for NB_neg, NA_pos, NB_pos.

Proposed treatment (no new Lean): say once per affected rung, next to the PROVED tag, that the object is entered by hand / by script, e.g. HG-DIM-1: 'closed neighbourhoods listed by hand and checked against the flip graph by script'; FL-1Z: 'the matrix of Eq. (D.3) of [2502.12662] transcribed at τ=ω'; EW-Z1b: 'residual generated from the Feynman rules by `sims/ewz1b/mklean.py`'. A cheap Lean fix for HG-DIM-1 (`NA_neg = closed nbhd of 2` by `decide`) belongs to the sanity-theorem step.

## Glossary edits (MISSING-IN-PAPER and MISMATCH)

- **hidden zero** — MISSING-IN-PAPER: Defined in Paper II at II:481 (EW-Z1b card), after the first use at II:132. Paper I uses it at I:552 in quotes, undefined. Edit I:552 and II:132: add '(a kinematic point where a colour-ordered tree amplitude vanishes)'.
- **Lovelace--Shapiro amplitude** — MISSING-IN-PAPER: Named and cited, but neither paper writes the formula. Edit II:284: add the formula and α(s)=α₀+α′s.
- **Legendre coefficient / partial-wave coupling** — MISMATCH: Lean stops at Legendre coefficients; prose calls the resulting ratios 'coupling ratios' (MR-1b OVERSTATES). Edit: define the coefficient→coupling convention at II:302 and tag it as a convention.
- **kinematic associahedron (ABHY)** — MISSING-IN-PAPER: Used from II:132 with citation only. Edit: one sentence at first use in II.
- **Ising cell / star network** — MISSING-IN-PAPER: 'Ising cells' defined at II:319; 'star network' (II:326) is not defined and not in Lean. Edit: drop '(star network)' or define it and say the Lean point is one rational point of OG(3,6).
- **pointwise stabiliser** — MISMATCH: II:431 defines it for groups ('the group fixing a set of positive points one by one'); Lean defines it in the derivation algebra Der h3(O). Edit: 'the algebra of derivations annihilating every point of S'.
- **exceptional Jordan algebra J3(O)** — MISSING-IN-PAPER: Named and cited at II:431 (27-dimensional); product not stated. Minor.
- **SM gauge algebra g_SM** — MISMATCH: Paper says 'SM gauge group'; Lean object is the algebra (JORD-1 OVERSTATES).
- **baryon triality / exactness window** — MISSING-IN-PAPER: 'exactness window' and 'linear anomaly window' (II:454) are not defined. Edit: define both in one clause.
- **graded positroid / Cartan grading** — MISSING-IN-PAPER: 'graded first and cubic moments' (II:466) not defined. Edit: '(the sums Σ_i w_i and Σ_i w_i³ of the grading weights)'.
- **colour-ordered amplitude** — MISSING-IN-PAPER: Used at II:481 without definition. Minor.
- **stage-3 relations** — MISSING-IN-PAPER: II:542/582 use 'stage-3 relations' without stating them. Edit: point to tab:cascade1diag or the relation file and state them for n=5.
- **fusion-rule (WZW) matrix** — MISSING-IN-PAPER: Not defined; the rung moves no ledger value. Minor.
- **per-face weight g_k(m)** — MISSING-IN-PAPER: Used at II:802, C:474, C:567 only; never defined. Edit C:474: add 'where $g_k(m)=m-2|1-m|-(k-3)m$ is the per-face term of the weighted Forman curvature'.
- **Toeplitz / Hankel minor; reflection positivity** — MISSING-IN-PAPER: II:710 uses 'reflected/unreflected minor' without the matrices. Edit: write the two 2×2 minors.
- **status tags (PROVED, PAPERPROVED, SIM, CITED)** — MISMATCH: Defined at I:47, II:74, but the abstracts (I:42, II:65) list a tag set without paper-proved (GENERAL OVERSTATES rows).

## Rungs with no blueprint row

55 of the 76 rungs in `notes/BLOCKER-INDEX-2026-10-13.md` carry no PROVED / Lean claim in the three papers, so they have no blueprint row. Where a Lean module with a matching name exists it is shown (name match only, not checked against the rung record); 'not located' means no module name matches.

| rung | Lean module by name |
|---|---|
| MR-1d | not located |
| MR-2b | not located |
| NL9 | not located |
| MR-3b | not located |
| OP-2 scale | not located |
| MR-2c | not located |
| MR-1e | not located |
| MR-1f | not located |
| MR-6 | not located |
| MR-5 | not located |
| MR-2e | not located |
| MR-7 | not located |
| MR-8 | not located |
| FZ-0 | not located |
| FZ-1 | not located |
| LAT-2 | not located |
| LAT-3 | not located |
| LAT-3' | not located |
| DZ-1 | not located |
| LAT-2' | not located |
| TH-1 | not located |
| KS-1 | not located |
| SUB-1 | not located |
| UL-1 | not located |
| MR-1f-eta | not located |
| FT-1 | not located |
| MR-7' | not located |
| FT-2 | FT2Mesh |
| FT-3 | FT3Gate |
| FT-4 | FT4Gate |
| PG-1 | PG1 |
| BR-5 | BR5p |
| GB-2 | not located |
| SC-2 | SC2b, SC2 |
| SC-3 | not located |
| SC-2b | SC2b |
| SC-1 | SC1 |
| STRUCT-1 | STRUCT1b, STRUCT1 |
| STRUCT-1b | STRUCT1b |
| STRUCT-2 | STRUCT2 |
| X6 / XD-6 / R2 | X6 |
| STRUCT-3 / R3 | STRUCT3 |
| R4 → R5 | R4Indep |
| R4-indep | R4Indep |
| FR-WZW | FRWZW |
| FR-MU | FRMU |
| F-COULOMB | FCoulomb |
| F-DIM | FDim, FDimMass |
| F-DIM′ (F-DIM2) | not located |
| F-DIM-MASS | FDimMass |
| F-SCATLEN | FScatLen |
| F-RHOWIDTH | FRhoWidth |
| F-POSGEOM-DAUGHTER | not located |
| BRIDGE-PL-ASSOC (charge) | BridgePLAssoc |
| STRUCT-NGEN | STRUCTNGen |

Also judged but not in the blocker index: MR-1b, BR-4, CURV-LEAN (curvature paper Lean section).

## Cost estimate for the sanity-theorem step (next, not done)

Pilot (2026-10-31): 3 rungs, 113 sanity/equivalence theorems, about 6–7 agent-hours plus one large CPU build. Proposed scope: the 9 OVERSTATES rungs' headline theorems plus the 7 NAME-ONLY DEF rows, i.e. about 10–12 rungs with 3–6 theorems each (known value, planted wrong case, non-vacuity, and for DEF rows one tie theorem such as `NA_neg = closedNbhd 2`).
Estimate: about 1.5–2 agent-hours per rung, so roughly 15–24 agent-hours in total, using the same CPU box (8 CPUs, 15 GB). Use one batched `lake build` of a single new `Alignment/Sanity2` module per batch of rungs; with existing oleans that is minutes per batch. Do not rebuild Mathlib. The largest risk is kernel time for `decide` on the HG-DIM n=9 data; reuse the pilot's HgKernel split.

