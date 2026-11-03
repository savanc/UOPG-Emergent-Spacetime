# Trade-space expansion 2026-10-28 (first principles, systems map, wide scan, deep dives)

Grok (AutoResearch), 2026-10-28. **PROPOSAL ONLY. Credit 0 proposed.** No rung, checker, prereg or
compute experiment was run for this note. AUTORESEARCH-STOP stays in place (not lifted).

**Provenance.** author direct, 2026-10-28 (verbatim):
> "Ok for any rungs and also part of frontier and based on systems thinking, first principles and wide and deep reviews you can propose or expand the trade space"

Recorded reading: The author approves (a) out-of-box and exploration rungs as legitimate frontier picks, (b) the MISSION
Frontier-mode item 4 amendment proposed in notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-28.md (applied in this commit, see the
handoff section), and (c) AutoResearch proposing or expanding the trade space. He did **not** lift AUTORESEARCH-STOP.

Tags: PROVED / SIMULATED / CITED / CONJECTURE / SPECULATION. CITED here means the claim is in the arXiv abstract (or, for
math/0105155, the paper text) of the ID given, checked on 2026-10-28. All P, V, EMC and d numbers are CONJECTURE
(our assessment, METHOD 2026-10-28 scoring); they are not measurements.

Scoring (METHOD-EXPLORATION-2026-10-28): P_used = 0.3 × P_naive; EMC = P_used·|M⁺| + (1 − P_used)·|M⁻|; IV_min =
min(|M⁺|, |M⁻|) ≥ 1; diversity d (axes A1 basin, A2 SM ledger line, A3 method class, A4 most-likely FM tag) ≥ 3 against
each of the last 3 rungs on main: TRIALITY-WHY (B3, N_gen, exact count, FM-TAUT/RANGE), CASCADE-1b (B5, ratios, exact
search, FM-LIMIT), LEAN-CERT-2 (B4, no line, certificate, FM-SPEC). Map items are named by id: `HUB-QN`, `HUB-RANGE`
(TRADE-SPACE-2026-10-28 hubs), `RT:X` (reopen trigger of BLOCKER-INDEX row X), `EXCLUSION:decl` (EXCLUSION-LEDGER row),
`BL:n` (BACKLOG item), `TS28:x` (TRADE-SPACE-2026-10-28 node/basin state). Proposed new ids are marked (new).

---

## (i) First-principles decomposition

Goal G: a Standard-Model ledger line (a dimensionless number or a discrete structure) derived from a positive-geometry
object with zero fitted parameters, Lean-defined, and preregistered.

Sub-goals, read off the failure modes the map has already logged:

| id | Sub-goal | Failure mode when missing | Where the map hit it |
|---|---|---|---|
| N1 | **Visibility**: the object's defining data depend on the target quantity (charges, N_c, N_gen, group type) | FM-QNBLIND | B2 (BRIDGE-PL-ASSOC, GRADED-POSITROID), X6 |
| N2 | **Selection**: a mechanism that turns a consistent window into one point (discrete classification, extremality, non-linear fixed point, integrality) | FM-RANGE, FM-FREE | B3 (windows {1..5}, odd N_c), B5 (linear ⇒ free ratio) |
| N3 | **Non-tautology**: inputs do not already encode the answer | FM-TAUT | TRIALITY-WHY, GRADED-POSITROID |
| N4 | **Scale carrier** (dimensionful lines only) | NO-GO (OP-2) | BR-4, PG-1 |
| N5 | **Well-posedness**: a Lean `def` with explicit hypotheses | FM-SPEC / ILL-DEFINED | F-DIM, LEAN-CERT-2 scope |
| N6 | **Model fidelity** (data-comparison rungs only) | FM-MODEL | B1 (LS-pion ×3) |

- **Necessary** for any dimensionless line: N1, N2, N3, N5. N4 is necessary only for dimensionful lines; N6 only when the
  rung compares with data.
- **Sufficient** (for a CONJECTURE-grade candidate worth preregistering): N1 ∧ N2 ∧ N3 ∧ N5 holding *in the same object*.
  No rung on main has had all four. B4 supplies N5 alone; B3 had N1 with no N2; B5 had N2-attempts that were linear
  (so not selectors); B2 failed N1.
- **First-principles finding (CONJECTURE, Lean target, cheap).** For a flag variety G/P_λ the totally non-negative part
  and its cell/canonical-form data depend on λ only through supp(λ) (the parabolic), and T_{>0} acts on it. If true, charge
  *magnitudes* are invisible to Lusztig positivity in every Lie type, so `HUB-QN` extends from Gr(k,n) to all G/P.
  Positivity can at most see the **group type** and the parabolic. This points N1 at a ledger line the map has never
  targeted: **the gauge-group type itself** (no EXCLUSION row targets it; every B3 rung takes G_SM as input; the
  `RT:STRUCT-NGEN` trigger asks for "a geometry/consistency derivation of the SM gauge group").
- **Selector classes for N2.** Only one class gives isolated points by construction: (s1) **classification theorems**
  of positivity-native objects (formally real Jordan algebras, finite-type Cartan/cluster data). The others: (s2)
  extremality/kinks (gives a point on the boundary of a window, needs a "why the extremum" argument); (s3) non-linear
  fixed points (gives algebraic numbers, but of the object, not obviously of the SM); (s4) integrality (gives lattices;
  ratios can stay free).
- **Consequence for the queue.** The leverage is objects where N1 is native (they see group type or N directly) **and**
  N2 comes from s1. That is JORD-1 and TP-1BR. SURF-1 is the best N1-native object for N_c (N^χ weights), but its N2 is
  open.

## (ii) Systems map

**Stocks:** Lean-certified results (1565 graph nodes); EXCLUSION rows (33); reopen triggers (BLOCKER-INDEX); frozen basins.

**Feedback loops.**
- **R1, basin lock-in (reinforcing).** Certified no-go → EXCLUSION row → reopen trigger phrased in that basin's language →
  the next rung aims at the trigger → same object, same question → another no-go of the same FM. This produced B1
  (FM-MODEL ×3), B5 (FM-FREE ×4) and conditional B3.
- **R2, contamination (reinforcing).** Targets with known values (N_gen = 3, N_c = 3, PDG ratios) → preregs that can be
  hit by tuning → "foregone" or "tuned hit" verdicts → credit 0 → pressure to pick another known target.
- **B1, saturation brake (balancing; adopted 2026-10-28).** Basin trigger + exploration slot (≥ 1 in 3, d ≥ 3) + FM tags.
  This note is the first use of it.
- **B2, certification throttle (balancing).** Lean viability limits which objects can be rungs, so objects not in
  mathlib (octonions, Jordan algebras, flag varieties beyond Gr) are under-explored. That is a selection bias, not evidence.

**Bottlenecks.** (1) N1 ∧ N2 in one object (above). (2) Lean viability of non-linear or non-mathlib objects. (3) Literature
verification time for out-of-basin areas (this note dropped 9 candidate citations, list below).

**Leverage points (high to low).** (L1) *Goal*: add the gauge-group-type ledger line (unmapped). (L2) *Rules*: the
exploration slot (done) plus an EMC granularity cap (method flag F5, proposal). (L3) *Information flow*: write each reopen
trigger as an object-independent condition (e.g. "a selector of class s1–s4 on the target line"), so triggers stop
pointing back into their own basin. (L4) *Parameters*: P and V tweaks (low leverage).

**Frozen basins.**

| Basin | State (TS28) | FM tags | Representative axes (A1, A2, A3, A4) |
|---|---|---|---|
| B1 LS-pion amplitude and deformations | FIRED | FM-MODEL ×3 | B1, pion masses/widths/LECs, data comparison, MODEL |
| B3 SM-consistency counting | conditional fire | FM-RANGE, FM-TAUT | B3, N_c/N_gen/hypercharge, exact count, RANGE |
| B5 ratio fixing (linear stages) | FIRED | FM-FREE ×4 | B5, mass ratios, analytic+exact search, FREE |
| B2 positroid↔charge (not frozen) | 2 QNBLIND, 1 TAUT | — | one more QNBLIND fires its mode form |
| B4 Lean certification (not frozen) | method basin | — | — |

Proposed new basins (new): **B6** Lie-type total positivity (G/P, Cartan monoids); **B7** Jordan-cone / octonionic
positivity; **B8** surfaceology colour expansion; **B9** EW EFT positivity cones; **B10** representation polytopes. COS
nodes stay in the existing COS lineage.

## (iii) Wide scan

Every node: P_naive → P_used, V (value if M⁺), |M⁺|/|M⁻| with ids, EMC, d (min over last 3; vs frozen B1/B3/B5),
eligibility. "Reopen" = a B5 ingredient reopen (§2d; must name the ingredient), not an exploration pick.

| Node | Object / question | P_n→P_u | V | EMC | d (last3; B1/B3/B5) | Slot |
|---|---|---|---|---|---|---|
| **JORD-1** (new) | formally real Jordan algebras / symmetric cones: does positivity + classification select h3(O) and G_SM non-tautologically? | 0.10→0.03 | 0.5 | **4.06** | 3; 4/3/4 | exploration |
| **TP-1BR** (new; TP-1 bridge leg) | Lusztig positivity on G/P and Cartan monoids: supp-only lemma + can positivity distinguish A2⊕A1? | 0.05→0.015 | 0.3 | **4.02** | 3; 4/3/4 | exploration |
| **SURF-1** (new) | curve-integral / surfacehedra colour expansion: does any positivity/convergence condition on the N^χ-weighted sum fix N_c? | 0.03→0.009 | 0.6 | **3.01** | 4; 4/3/3 | exploration |
| **EW-POS** (+EW-POS-K) | our M2b EFT-hedron cone vs EW aQGC positivity cone; K: does an extremal/kink point carry an SM-fixed ratio? | 0.05→0.015 | 0.1 | **3.00** | 3; 3/3/4 | exploration |
| **REP-POLY** (new) | BZ/hive polytopes (QN-native): is any canonical-form property of SM rep polytopes tied to anomaly freedom? | 0.03→0.009 | 0.3 | 2.01 | 3; 4/3/4 | exploration |
| **COSP-1** (new) | cosmohedra (shaved cosmological polytopes): does the shaving fix a dimensionless number? | 0.03→0.009 | 0.2 | 2.00 | 3; 4/4/3 | exploration |
| COS-2 | cosmological-collider spin-1 template | 0.05→0.015 | 0.8 | 2.01 | **2** (vs LEAN-CERT-2: same "no line" + FM-SPEC) | HELD (d) |
| CLU-1 (new) | cluster Laurent-positivity integrality as the "integrality positivity" ingredient for F-COULOMB / INT-1 | 0.05→0.015 | 0.4 | 3.03 | 2 vs CASCADE-1b | reopen (B5) |
| TROP-1 (new) | positive tropical Grassmannian / Dressian: piecewise-linear walls as a non-linear selector | 0.05→0.015 | 0.4 | 3.02 | 2 | reopen (B5) |
| HTC-1 (new) | Markov trace chain: fixed points of iterated Kron reduction on self-similar networks (non-linear stage) | 0.6→0.18 | 0.05 | 2.36 | 2 | reopen (B5), mechanism only |
| BOOT-NC (new) | positivity bootstrap + anomaly matching with explicit N dependence as an N_c bound | 0.05→0.015 | 0.4 | 3.03 | 3; **B1: 2** | HELD (basin ruling) |
| OCT-1 (as stated) | "Does Furey–Hughes yield any dimensionless number? (expected NO)" | — | — | IV_min 0 | 2 (N_gen) | foregone (§2f) → merged into JORD-1 as OCT-1′ |
| TP-2 | already run 2026-10-13 (PASS, contaminated, credit 0) | — | — | — | — | reopen only, no ingredient named |
| ANOM-1 | cobordism / reflection positivity on the SM | — | — | — | 1–2 (inside B3) | not eligible (known outcome) |
| NCG-1 | spectral-triple classification | — | — | — | — | strong rival, not a node |

M⁺ / M⁻ item lists (counts above):
- **JORD-1.** M⁺ (6): `HUB-QN` (counter-edge), `RT:STRUCT-NGEN` (gauge-group derivation), `RT:STRUCT-2`, `RT:STRUCT-3`,
  `EXCLUSION:Separation.geometry_struct_separation` (scope), `BL:6/OCT-1`. M⁻ (4): `BL:6/OCT-1` (closed/merged), proposed EXCLUSION
  row `JORD1.input_encodes_three` (new), `HUB-QN` (+TAUT edge from B7), `TS28` node JORD-1 FAIL.
- **TP-1BR.** M⁺ (5): `HUB-QN` (counter), `RT:R4→R5`, `RT:STRUCT-2`, `EXCLUSION:BridgePLCharge.bridge_charge_nolink` (scope),
  `BL:6/TP-1`. M⁻ (4): `HUB-QN` generalised to all Lie types via proposed `TP1BR.supp_only` (new), `RT:BRIDGE-PL-ASSOC`
  (scope extended), `BL:6/TP-1` (closed), proposed `TP1BR.cartan_monoid_any_type` (new).
- **SURF-1.** M⁺ (4): `RT:STRUCT-2`, `EXCLUSION:FRWZW.nc_not_selected` (scope), `EXCLUSION:STRUCT2.three_not_selected` (a
  non-anomaly selector), `HUB-RANGE` (counter). M⁻ (3): proposed `SURF1.nc_free` (new), `RT:FR-WZW` (N_c-freeness extended
  from WZW to the full colour sum), new BACKLOG/OOB entry closed.
- **EW-POS.** M⁺ (3): `BL:6/EW-POS`, `HUB-RANGE` (counter), `RT:UL-1` analogue outside B1. M⁻ (3): `BL:6/EW-POS`
  closed, M2b node scope (prior art recorded), `HUB-RANGE` (+edge).
- **REP-POLY.** M⁺ (3): `HUB-QN`, `RT:R4→R5`, `RT:GRADED-POSITROID`. M⁻ (2): `HUB-QN` (+TAUT), proposed EXCLUSION row.
- **COSP-1.** M⁺ (2): COS-1 lineage edge, `HUB-RANGE`. M⁻ (2): COS-1 PARTIAL scope, proposed EXCLUSION row.
- **CLU-1.** M⁺ (5): `RT:F-COULOMB`, `RT:INT-1`, `RT:CASCADE-1`, `TS28:B5` freeze lift, `EXCLUSION:FCoulomb.mass_ratio_free`
  (scope). M⁻ (3): `RT:F-COULOMB` (integrality ingredient closed), proposed `CLU1.integral_still_free`, B5 tally +1.
- **TROP-1.** M⁺ (4): `RT:INT-1`, `RT:CASCADE-1`, `TS28:B5`, `EXCLUSION:IntChamber.ratio_free` (scope). M⁻ (3): same three
  minus the freeze lift, plus proposed `TROP1.walls_ratio_free`.
- **HTC-1.** M⁺ (4): `RT:CASCADE-1`, `RT:INT-1`, `BL:1` (trace-order note unparked), `EXCLUSION:IntChamber.ratio_free` (scope).
  M⁻ (2): `BL:1` closed, proposed `HTC1.no_rational_fixed_point`.

Literature basis (CITED = in the abstract / text of the arXiv ID):
- **Lie / cluster positivity.** Lusztig attaches a non-negative monoid to any Cartan matrix [CITED 1812.09313].
  Fomin–Zelevinsky double Bruhat cells and total positivity [CITED math/9802056]; cluster algebras I [CITED
  math/0104151]; Postnikov positroid cells [CITED math/0609764]; Lam's invitation to positive geometries [CITED 2208.05407];
  Laurent positivity [CITED 1306.2415, 1411.1394].
- **Moduli positivity.** Cluster configuration spaces M_D exist for every Dynkin type, with A_{n−3} = M_{0,n} [CITED
  2005.11419]; binary geometries exist for any Dynkin type and factorise by removing nodes [CITED 1912.11764]; stringy
  canonical forms [CITED 1912.08707]; moduli spaces in positive geometry [CITED 2405.17332]; ABL positive geometries
  [CITED 1703.04541].
- **Tropical.** Tropical TP Grassmannian [CITED math/0312297]; tropical Grassmannian [CITED math/0304218]; positive
  Dressian = positive tropical Grassmannian [CITED 2003.10231]; positive configuration space [CITED 2003.03904];
  amplituhedron/hypersimplex [CITED 2002.06164]; CEGM [CITED 1903.08904]; tropical amplitudes for coloured Lagrangians
  [CITED 2402.06719].
- **Surfaceology.** All-loop counting via curves [CITED 2309.15913]; hidden zeros [CITED 2312.16282]; NLSM ⊂ Tr φ³
  [CITED 2401.05483]; scaffolded gluons [CITED 2401.00041]; ABHY [CITED 1711.09102]; also 1212.5605, 1312.2007, 1912.08222.
- **Cosmological.** Cosmological polytopes [CITED 1709.02813]; cosmohedra [CITED 2412.19881]; differential equations
  [CITED 2312.05303].
- **Octonions / Jordan.** Formally real Jordan algebras carry a partial order (b − a a sum of squares); JvNW
  classification = 4 infinite families + the one exception h3(O); OPⁿ exists only for n ≤ 2 [CITED math/0105155, §3, text].
  Boyle: exceptional Jordan algebra ↔ SM / left-right / Spin(10), triality for 3 generations [CITED 2006.16265].
  Krasnov: G_SM ⊂ Spin(9) as the commutant of a complex structure J from a unit imaginary octonion [CITED 1912.11282].
  Dubois-Violette; Dubois-Violette–Todorov; Todorov [CITED 1604.01247, 1808.08110, 1911.13124]. Furey–Hughes; Furey
  [CITED 2409.17948, 1806.00612].
- **Anomaly / cobordism.** García-Etxebarria–Montero [CITED 1808.00009]; Wan–Wang [CITED 1910.14668]; new SU(2) anomaly
  [CITED 1810.00844]; Freed–Hopkins reflection positivity [CITED 1604.06527].
- **Positivity bounds.** Adams et al. [CITED hep-th/0602178]; EFT-hedron [CITED 2012.15849]; aQGC positivity
  [CITED 1902.08977]; positive moments [CITED 2011.00037]; all EFT coefficients bounded and kinks ruled in by extremal
  amplitudes [CITED 2011.02957]; large-N pion bootstrap with a kink [CITED 2203.11950]; bounds with an explicit N dependence
  via anomaly matching [CITED 2307.01246].
- **Rivals.** CCM spectral action, Higgs ≈ 170 GeV prediction (a known miss) [CITED hep-th/0610241]; "Why the Standard
  Model" classification [CITED 0706.3688]. LR honeycombs / BZ polytopes [CITED math/9807160].

## (iv) Deep dives (top 3)

### D1. JORD-1: positivity classification as a selector (B7)
- **Why it is first.** It is the only node where N1 (the algebra's automorphism/stabiliser chain sees group type) and
  N2-s1 (a classification with an isolated exceptional member) are both native. Formal reality *is* a positivity axiom
  (sums of squares vanish only trivially), so positivity → JvNW list → h3(O) as the sole exceptional member
  [CITED math/0105155]. The G_SM chain is in the literature [CITED 1912.11282, 1604.01247, 2006.16265]. The
  positive-geometry link (canonical form of the cone of squares) is ours [SPECULATION]; that the symmetric-cone canonical
  form is ∝ det^{−n/r} on the cone is [CONJECTURE] (to state and check, not assumed).
- **Well-posedness sketch.** Define the cone Ω_n(K) = {squares in h_n(K)}; Lean `def` via explicit structure constants for
  O (no mathlib octonions assumed). Question Q-J1: under the stated axioms (formal reality + simple + "exceptional"
  i.e. not special), is the stabiliser of the chosen extra structure (J or a rank-1 idempotent) exactly G_SM up to finite
  quotient, with *no* other choice of equal minimality also giving a rank-12 compact group? Q-J2 (cheap Lean target):
  explicit rational witness that h_4(O) violates the Jordan identity, certifying "3" is the maximum size [CONJECTURE that a
  small witness exists; plan only].
- **Prereg target (to avoid R2).** Not "N_gen = 3" (known; foregone). Target the **gauge-group-type line**: the count of
  inequivalent minimal extra structures whose stabiliser is rank-4 with a U(1) factor, fixed before computing.
- **Strong rival.** NCG classification (0706.3688) also singles out the SM from a short list, and its spectral action made
  a wrong Higgs number (hep-th/0610241): classification frameworks can select structure and still miss numbers.
- **Null.** Choice multiplicity: count embeddings su3⊕su2⊕u1 ⊂ f4 / e6 reachable by *any* single-octonion choice; if the
  SM embedding is one of many equal-cost choices, FM-TAUT.
- **Feasibility.** Compute trivial (27-dim algebra, ~2·10⁴ structure constants). Lean medium: explicit tables + `decide` /
  `norm_num` on rational witnesses; no general Jordan theory needed for Q-J2.
- **Kill:** the extra structure that yields G_SM is not minimal or not unique among equal-cost choices (TAUT), or Q-J2 has
  no small witness and the general proof is out of Lean reach (SPEC). **Reopen:** a positivity-native reason (not a choice)
  for the complex structure J.
- **OCT-1′** (merged): Furey–Hughes (2409.17948) as the rival *construction* on the same object; audit where the "3"
  enters (input vs output). Only the audit, not the "any number?" question (foregone).

### D2. TP-1BR: Lie-type positivity (B6)
- **Two questions.** Q-T1 (closure lemma, cheap; foregone-like, so it does not fill the slot alone): (G/P_λ)_{≥0} cell data
  depend on λ only through supp(λ) [CONJECTURE] → `HUB-QN` extends to all Lie types. Q-T2 (live): does any positivity
  property of the Cartan-matrix monoid (1812.09313) or of (G/P)_{≥0} distinguish A2⊕A1 (⊕ abelian) from other rank-3/4
  reductive types, using only positivity data?
- **Expected outcome.** Q-T2 likely FM-RANGE, since a monoid exists for every Cartan matrix [CITED 1812.09313] and binary
  geometries exist for every Dynkin type [CITED 1912.11764]. The value is in mapping: it closes `BL:6/TP-1` with a proved
  generalisation of the B2 no-go, or finds a type-dependent positivity invariant.
- **Well-posedness.** SL3 concrete: Chevalley generators, minors, Lean-viable; Q-T1 for SL3 / SL2×SL2 flag varieties first.
- **Rival:** "every Cartan matrix admits equal positivity" (the RANGE hypothesis). **Null:** permuted / random Cartan
  labels give the same invariant.
- **Kill:** Q-T2 invariant is type-independent. **Reopen:** a positivity invariant that is not constant over Dynkin types
  of equal rank. **Diversity caution:** if the reviewer files it under B2, a QNBLIND outcome fires B2's mode form.

### D3. SURF-1: colour-sum positivity for N_c (B8)
- **Object.** The curve-integral formula organises amplitudes by surfaces [CITED 2309.15913]; the colour-dressed sum
  weights surfaces by N^χ (standard 't Hooft counting; the precise curve-integral statement must be extracted from
  2309.15913, not assumed).
- **Question.** Is there a positivity, convergence or factorisation condition on the full N-weighted sum (not one surface)
  that holds for a discrete set of N? [SPECULATION]. Default expectation FM-FREE (N is a free weight), which would extend
  `FRWZW.nc_not_selected` from the WZW coefficient to the whole colour expansion.
- **Well-posedness.** Restrict to Tr φ³ at one loop, n ≤ 4, planar vs non-planar ratio ∝ N^{−2}; exact rational
  computation; Lean viable for the small-n statement.
- **Rival:** large-N bootstrap bounds that depend on N via anomaly matching (2307.01246), which is B1-adjacent.
  **Null:** replace N^χ by an arbitrary positive weight w^χ; if every w > 0 passes, FM-FREE.
- **Kill:** the condition holds for all N > 0. **Reopen:** a non-planar curve-integral term whose sign depends on N.

## (v) Per-node detail (remaining nodes; the top 3 are above)

| Node | Well-posedness sketch | Feasibility | Rival / null | Kill / reopen |
|---|---|---|---|---|
| EW-POS(-K) | Cone C_M2b vs Zhang–Zhou cone (1902.08977) on the same operator basis; K: extremal rays (2011.02957) | trivial compute; Lean medium (cone inclusion = LP certificate) | rival: published cones (prior art, high contamination); null: random EFT basis rotation | kill: cones coincide and SM sits in the interior (f = 0), RANGE; reopen: an extremal ray fixed by an SM ratio |
| REP-POLY | BZ/hive polytope for SM reps (math/9807160); canonical form vs anomaly polynomial | trivial; Lean medium | rival: plain rep theory (TAUT); null: non-anomaly-free rep sets | kill: property holds for all rep sets; reopen: anomaly-only dependence |
| COSP-1 | cosmohedron face structure (2412.19881) vs COS-1 zeros | low; Lean medium | rival: cosmological polytope (1709.02813) alone; null: unshaved polytope | kill: no fixed number; reopen: a face-count fixed by FRW exponent |
| CLU-1 | Laurent positivity (1306.2415) as the integrality ingredient for `RT:F-COULOMB` | low; Lean viable for finite type A2/B2 | null: non-cluster integer lattice | kill: ratios stay free; reopen: integral + positive forces a ratio |
| TROP-1 | walls of Trop⁺Gr(2,n) (math/0312297) as selector | low; Lean viable | null: arbitrary PL fan | kill: walls leave ratios free inside cones |
| HTC-1 | iterated Kron reduction map on self-similar networks (H-T1 PROVED chain) | low; Lean high | null: random networks | kill: no rational fixed point; reopen: rational fixed point of a positivity-preserving RG (mechanism only, V low) |
| BOOT-NC | SDP bounds with N-dependent anomaly term (2307.01246) | SDP solver needed; Lean low | rival: FPRS large-N bounds (B1) | HELD until the author/PositiveGeometryEmergentSpaceTime rule whether it is B1 |

## (vi) Ranked exploration queue (PROPOSAL ONLY; nothing queued to run; STOP in place)

Rank by EMC (exploration slot; eligibility = IV_min ≥ 1, d ≥ 3, not frozen, not foregone); chance × value (EV = P_used·V)
logged alongside as amended MISSION item 4 requires.

| Rank | Node | P_used | EMC | EV | d_min | IV_min | Note |
|---|---|---|---|---|---|---|---|
| 1 | JORD-1 (+OCT-1′ audit) | 0.03 | 4.06 | 0.015 | 3 | 4 | gauge-group-type line; TAUT risk |
| 2 | TP-1BR | 0.015 | 4.02 | 0.0045 | 3 | 4 | Q-T1 lemma + Q-T2 live |
| 3 | SURF-1 | 0.009 | 3.01 | 0.0054 | 4 | 3 | N_c line, small-n first |
| 4 | EW-POS(-K) | 0.015 | 3.00 | 0.0015 | 3 | 3 | high prior-art risk |
| 5 | REP-POLY | 0.009 | 2.01 | 0.0027 | 3 | 2 | B2-adjacent |
| 6 | COSP-1 | 0.009 | 2.00 | 0.0018 | 3 | 2 | COS lineage |

Exploitation / reopen slot (B5 named ingredient, §2d): CLU-1 (3.03), TROP-1 (3.02), HTC-1 (2.36).
Held: BOOT-NC (basin ruling), COS-2 (d = 2 vs LEAN-CERT-2 until it leaves the last-3 window; earlier UNRELIABLE flag),
TP-2 (already run; needs an ingredient), OCT-1 as stated (foregone), ANOM-1 (inside B3, known outcome).

## Flags

- **F1.** TP-2 was already run (2026-10-13, PASS, contaminated, credit 0). The 10-28 handoff listed it as a candidate; it
  is a reopen only.
- **F2.** OCT-1 as phrased ("expected NO") is declared foregone, so IV_min = 0 (§2f), and its d vs TRIALITY-WHY is 2 if it
  targets N_gen. Reframed as OCT-1′ (gauge-group line, TAUT audit) inside JORD-1.
- **F3.** B5-reopen candidates (CLU-1, TROP-1, HTC-1) have d = 2 vs CASCADE-1b, so they cannot fill the exploration slot.
- **F4.** COS-2 fails d ≥ 3 against LEAN-CERT-2 (same "no line" and FM-SPEC).
- **F5 (method, SPECULATION, proposal).** At P_used ≤ 0.03, EMC ≈ |M⁻|, so the score ranks by how much a *failure*
  moves the map, and item counts are ours to choose (Goodhart risk). Proposed for METHOD (not adopted): cap |M±| ≤ 5,
  require every counted id to exist in a named file before the prereg, and log EMC⁺ = P_used·|M⁺| next to EMC.
- **F6.** Cobordism/anomaly routes are inside frozen B3 (d 1–2); BOOT-NC is B1-adjacent (d 2 vs B1). Both held.
- **F7.** No EXCLUSION row targets the gauge-group-type line; it is an unmapped ledger line (wide-scan finding).

## Dropped citations (not verified on arXiv; not used as CITED)
1. 1811.07902 (guessed ID; it is an unrelated astrophysics paper).
2. a related preprint by the same authors on fusions of Markov kernels (not found on arXiv).
3. Lusztig 1994 total positivity in reductive groups (only via 1812.09313's abstract).
4. Koecher–Vinberg / symmetric-cone characteristic function (not located on arXiv).
5. Kigami / Sierpiński resistance renormalisation (not located).
6. Jordan–von Neumann–Wigner 1934 (pre-arXiv; used only via 2006.16265 and math/0105155).
7. Dorey, Toda S-matrices (not located with a verified ID).
8. Froggatt–Nielsen (pre-arXiv; not used).
9. Singh's J3(O) mass-ratio claims (no verified ID; not used).

## Glossary (new symbols; non-Lean, so not in LEAN-GLOSSARY)
- **N1–N6**: first-principles sub-goals (visibility, selection, non-tautology, scale carrier, well-posedness, fidelity).
- **s1–s4**: selector classes (classification, extremality, non-linear fixed point, integrality).
- **R1, R2, B1, B2 (loops)**: feedback loops of §(ii); not the basins B1/B2 (basins are written "basin B1").
- **B6–B10**: proposed basins (Lie-type positivity; Jordan-cone; surfaceology colour; EW positivity; rep polytopes).
- **JORD-1, OCT-1′, TP-1BR, SURF-1, EW-POS-K, REP-POLY, COSP-1, CLU-1, TROP-1, HTC-1, BOOT-NC, ANOM-1, NCG-1**: node ids.
- **Q-J1, Q-J2, Q-T1, Q-T2**: sub-questions of JORD-1 and TP-1BR.
- **EMC⁺**: P_used·|M⁺| (F5 proposal).
- **Id prefixes**: `HUB-`, `RT:`, `EXCLUSION:`, `BL:`, `TS28:` (see header).

Credit 0 (proposal).
