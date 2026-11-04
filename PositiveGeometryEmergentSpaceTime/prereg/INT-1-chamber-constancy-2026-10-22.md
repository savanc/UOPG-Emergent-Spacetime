# PREREG INT-1: are integer invariants of the kinematic associahedron (with mass offsets) constant within each chamber?
Written 2026-10-22 by Grok. This is a **The author-directed manual frontier rung**, not AutoResearch. The author at: "Dont forget we need to keep frontier research so we need to work on formal lean maths and simulations". The parent relayed it at: run INT-1 and then FL-1Z.
AUTORESEARCH-STOP: the stop file was added in 87a7a1f. At rung start, origin/main has 343ae42, "Remove AUTORESEARCH-STOP: resume continuous mode (author approved 2026-10-22)", pushed at. This rung does not depend on that file either way. It is run under the manual instruction. The conflict with the relayed "AutoResearch stays paused" is reported to the author; this rung does not act on it.
Pushed ALONE, together with the locked checker, planted spec and import test (precedent: STRUCT-NGEN, R4-DM v3), before any checker computation. No physical datum enters.
Source sketch: `notes/TRADE-SPACE-2026-10-22.md` §C R-A (PROPOSED there; now approved for a run by the author's message above).

## 1. Hypothesis
**H (INT-1).** Take the ABHY kinematic associahedron (1711.09102) with mass offsets. It is cut out by X_ij ≥ m²_ij on the planar variables, with c_ij held constant (eq. 24). Fix a declared class of integer-valued invariants. Each invariant in the class is constant on every open chamber of a finite hyperplane arrangement in the offset space (c, m²), and it can change only on the walls. Consequently, no integer condition from that class selects an isolated value of a dimensionless offset ratio. Each level set is a union of chambers and wall pieces. Any ratio μ that a level set contains, it contains together with an open interval or a dense set.

**Opposing hypothesis (what a kill would mean).** An integer invariant of the polytope itself varies inside a chamber, or it pins μ to a discrete set. Then P1 ("integers from the polytope") is REOPENED.

## 2. Exact definitions
- n = 5. The planar variables are X13, X14, X24, X25, X35, in the facet order X14, X24, X25, X35, X13 of `PositiveGeometryEmergentSpaceTime.Assoc` (`lean/PositiveGeometryEmergentSpaceTime/Associahedron.lean`). The coordinates are x = X13, y = X14 (`Assoc.X c13 c14 c24 x y = ![y, y−x+c13, c13+c14−x, c14+c24−y, x]`).
- **Massive region:** X_k ≥ m²_k for real m²_k ≥ 0 (five offsets).
- **Effective constants (claimed; Lean `IntChamber.mass_shift` below):**
  - c13' = c13 + m²14 − m²13 − m²24
  - c14' = c14 − m²14 − m²25 + m²24
  - c24' = c24 − m²24 − m²35 + m²25
  - For general n: c'_ij = c_ij − m²_ij − m²_{i+1,j+1} + m²_{i,j+1} + m²_{i+1,j}, with the m² of non-diagonals set to 0.
  - The massive polytope is the massless one at c', translated by (m²13, m²14).
- **Walls (n = 5, derived before this prereg; FOREGONE, see §4):** the zero sets in c'-space of the six forms c13', c14', c24', c13'+c14', c14'+c24', c13'+c14'+c24'. The checker re-derives the wall set for n = 5 and n = 6 independently, as the slacks of every facet at every d-fold facet intersection, normalised up to scale.
- **Chamber:** a sign vector in {−,0,+}^(#forms). The open chambers are the sign vectors with no 0 entry.
- **Invariant classes, declared:**
  - **I_comb:** any function of the *labelled face lattice*, meaning faces given as sets of vertex tight-sets with facet labels. Examples are the f-vector, the Euler characteristic, which facets are present, and which vertices are simple. The claim **H applies to I_comb**.
  - **I_lat:** the lattice-point count |P ∩ ℤ^d| in the basis coordinates (X13, X14[, X15]). Declared in advance as **NOT chamber-constant**, because it has finer walls: the facet hyperplanes passing through integer points, an infinite but locally finite family. The declared I_lat claim is narrower: constant on each cell of the lattice-wall arrangement. I_lat varying inside an I_comb chamber is the **expected** outcome and is **not a kill**.
  - The trade-space sketch's phrase "Ehrhart data … constant on the open chamber" is therefore predicted to be **wrong as worded**. Volume is not integer-valued.
- **Dimensionless target (one):** μ = c13'/c14', an offset ratio of the declared form (m² differences over m² differences when c = 0). Prediction: no I_comb or I_lat level set pins μ. In the pentagon chamber μ ranges over all of (0, ∞). With c' ∈ ℤ³ (integral vertices) μ ranges over ℚ_{>0}, which is dense.

## 3. Theorem statements (Lean 4 + Mathlib; new module `lean/PositiveGeometryEmergentSpaceTime/IntChamber.lean`, namespace `PositiveGeometryEmergentSpaceTime.IntChamber`; 0 sorry; standard axioms only)
1. `slack_sign_eq`: the eight non-parallel facet-pair intersection points `pt c p` have explicit coordinates. For every p and facet k, SignType.sign (X c (pt c p) k) = σOf (chamberSign c) p k, where `chamberSign c i = sign (forms c i)` over the six forms and `σOf` is a fixed table with entries in {0, s_i, −s_i}.
2. `faceType_locallyConstant`: chamberSign c = chamberSign c' → vertexType c = vertexType c'. Here `vertexType c` is the finset of tight-facet sets of the feasible pair points, which is the labelled vertex set of the polygon. Corollary `invariant_chamber_constant`: the same holds for any F : Finset (Finset (Fin 5)) → ℤ (or ℕ) of the vertexType, which includes f0 and f1.
3. `jump_only_on_wall`: if every form is non-zero along the whole segment from c to c', then chamberSign c = chamberSign c'. Equivalently, vertexType can differ between two points only if the segment between them meets a wall.
4. `mass_shift` / `massRegion_iff`: X c (x, y) k − m²_k = X c' (x − m²13, y − m²14) k, so the massive region is the c'-region translated by (m²13, m²14).
5. Planted f-values by `decide` on σOf: positive chamber gives (f0, f1) = (5, 5) (`f_pos`); the merging wall c24' = 0 with c13', c14' > 0 gives (4, 4) plus a vertex with 3 tight facets {X24, X25, X35} (`f_wall`, `wall_triple`); beyond it (c24' < 0 < c14'+c24') gives (4, 4) with X25 absent (`f_beyond`).
6. `ratio_free`: ∀ r > 0, ∃ c' in the positive chamber with c13'/c14' = r. `lattice_ratio`: ∀ q : ℚ, 0 < q → ∃ positive integers (a, b) with a/b = q. Integer c' lies in the positive chamber (and gives integral vertices `pt`), so integrality leaves μ dense.
If a statement needs re-wording to compile, the change is declared in the result, never hidden. If no correct re-wording exists, the theorem is reported FAILED and the verdict follows §6.

## 4. Foregone / contamination (declared)
- Combinatorial type of the ABHY polytope for c > 0 (associahedron, pentagon at n = 5, (14, 21, 9) at n = 6): CITED, ABHY 1711.09102, fetched this session (eq. 24, 27–28, 29–33; §4.1 facet factorisation).
- The six-form factorisation of the n = 5 slack table was derived with sympy (`/tmp/slack.py`) BEFORE this prereg. So the n = 5 face-lattice constancy is **FOREGONE** (in effect a lemma whose proof is already known). Only the Lean formalisation is new.
- **Not foregone:**
  - n = 6 with mass offsets: the chamber structure, wall set, and constancy away from the positive chamber.
  - I_lat behaviour: the lattice-cell claim.
  - The μ level-set test.
  - The detector-power (broken-detector) test.

## 5. Predictions (written before running)
- n = 5 I_comb chamber-constant on all samples and segments: **97%**. KILL: 2%. ILL-DEFINED from a planted failure: 1%.
- n = 6 positive chamber gives (14, 21, 9) on every sample and segment: 99%. Number of n = 6 wall forms ≥ 10: 70% (a guess: ABHY n = 6 has 6 c's; expected ~20).
- I_lat varies inside the positive I_comb chamber: 99%. I_lat constant on lattice cells: 97%.
- Broken detector floor(4c13') is flagged and the f-vector is not: 99%.
- Every μ level with ≥ 20 samples shows ≥ 10 distinct μ: 99%.
- Lean: all §3 statements compile with standard axioms only: 85%. Partial (some re-worded): 12%.

## 6. Pass / fail / kill criteria
- **ILL-DEFINED:** any planted case (§7) fails. Then the live results are not scored.
- **KILL (P1 REOPENED)**, reported plainly, if any of the following holds:
  - any I_comb chamber, at n = 5 or n = 6, holds two different labelled face lattices;
  - a same-chamber segment changes lattice;
  - a crossing segment changes lattice inside an open interval between wall roots;
  - the massive and shifted-massless lattices differ;
  - an I_lat value changes inside a lattice cell;
  - a μ level with ≥ 20 samples has < 10 distinct μ;
  - a Lean §3 statement is proved FALSE (a counterexample).
- **PASS (CHAMBER-CONSTANT no-go)** otherwise, with Lean §3 compiled. If a Lean §3 statement fails to compile and is not proved false: PASS-SIMULATED only (Lean claim downgraded, reported).
- I_lat varying inside an I_comb chamber is NOT a kill (declared §2).

## 7. Planted-answer test (inline in the checker; list in `sims/int1/planted_cases.json`)
- P1a: c = (1, 1, 1) gives (5, 5).
- P1b: c = (2, 3, 5) with m²13 = ½, m²14 = ⅓, m²35 = ⅕ gives c' > 0 and (5, 5).
- P2a: the planted merging-offset wall. c = (1, 1, 1) with m²35 = 1 gives c24' = 0, (4, 4), and exactly one 3-tight vertex {X24, X25, X35}.
- P2b: m²35 = 3/2 gives (4, 4) with X25 absent.
- P3: broken detector. floor(4c13') is flagged non-constant on the positive chamber (200 samples) and the f-vector is not.
- P4: n = 6 with c ≡ 1 gives (14, 21, 9).
- P5: the derived n = 5 forms equal the six declared forms.
- P7: lattice count at c = (1, 1, 1) is 8.

## 8. Simulation plan (exact rational arithmetic, Python `fractions`)
- Run id `INT1-2026-10-22-r1`, seed `20261022` (P3 uses seed+3). Modes: `planted`, then `live` (live runs only if planted PASS).
- **S1:** n = 5, 4000 samples. c ∈ [−2, 3]³ rational with denominator ≤ 12. Half the samples have no masses; the other half have m² ∈ [0, 1.5] on all 5 diagonals. Labelled face lattice computed directly from the massive inequalities by brute-force vertex enumeration and intersection closure. Grouped by the sign vector of the derived forms at c'.
- **S1b:** ≤ 1000 same-chamber segments (15 interior points each) and 1000 random segments with exact wall roots. Each open interval is tested at two interior points.
- **S2/S2b:** I_lat on ≤ 600 positive-chamber samples, plus 60 segments split at exact lattice-wall roots (first 30 intervals each).
- **S3:** n = 6, 300 massless positive samples and 300 mixed samples (c ∈ [−1, 3], m² ∈ [0, ½]). Re-derived wall forms; 120 positive segments.
- **S4:** distinct ratios a/b with a, b ≤ N, for N = 5, 10, 20, 40.
- **S5:** μ level sets.
- **Figure:** slice c13' = 1, (c14', c24') ∈ [−2, 2]² on a 0.1 grid, coloured by f-vector, with walls overlaid. The figure script is written after the run and only reads `sims/int1/int1_live.json`; it is not a scoring script.
- Negative results are kept (JSON + text output committed).

## 9. Data sources and tiers
- Tier 0 (mathematics): ABHY 1711.09102 (CITED, fetched); existing repo Lean `PositiveGeometryEmergentSpaceTime.Assoc`.
- No experimental data. No data-credit moves.

## 10. Pinned environment
- Python 3.13.5 (`<local path>`): sympy 1.14.0, numpy 2.5.4, mpmath 1.3.0. The checker uses the stdlib only (fractions, itertools, random).
- Lean `leanprover/lean4:v4.34.1`, Mathlib rev `d13f23b723b8a846827a245b89c10fc7d3f11612` (lake-manifest). CPU only, no paid compute.
- Figure: `<local path>` (matplotlib).

## 11. Guard and run manifest
- Hardened guard, copied from `sims/bplc`. git fetch once per process. The prereg add-commit must be an ancestor of origin/main. The checker sha256 must match the line below. `guard` is called in every scoring function (`polytope`, `face_lattice`, `lattice_count`, `ceff`, `arrangement_forms`, `chamber_key`, `chamber_constancy`, `run_planted`, `run_live`). There is no pass flag.
- The import test must REFUSE before the push; its output is saved to `sims/int1/guard_refusal.txt`.
- Run manifest (result commit):
  - `sims/int1/int1_planted.txt`, `sims/int1/int1_output.txt`, `sims/int1/int1_live.json`
  - `lean/PositiveGeometryEmergentSpaceTime/IntChamber.lean`, `lean/axioms/IntChamber_axioms.lean`, `lean/axioms/IntChamber_output.txt`
  - `figures/int1-chambers-2026-10-22.png`, `reviews/INT-1-result-2026-10-22.md`
  - ledger/glossary/trade-space/BACKLOG updates

Locked:
- `sims/int1/int1_checker.py` sha256 `c7fcb1cdd3e4ec58bc023700a77dd1a523d967847674bcd3ac09ff4f51dd9b11`
- `sims/int1/planted_cases.json` sha256 `6faa23c9d19789775e0d051cd0770231910a84af0ff048cbc319956f7489ffbf`
- `sims/int1/import_guard_test.py` sha256 `495d751bd3cf0321ca24518abbf43a3bce67dbd4884a709deeb34aa1106281d1`
