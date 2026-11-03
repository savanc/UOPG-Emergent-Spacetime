# Lean parameter & definition glossary — 2026-10-15

**Status:** read-only extraction. No Lean theorem *meanings* or credit/OP-2/EXCLUSION changed by
this glossary. `AUTORESEARCH-STOP` left in place. AutoResearch not contacted.

**Naming pass (same day):** identifiers for shared masses / STRUCT-2 `N_c` / SC1 `ap`
were unified per `notes/LEAN-NAMING-MAP-2026-10-15.md`. Canonical Lean tokens now appear
in binder rows; prior names are listed as *Also known as* in Lean docstrings. This file
was regenerated after that pass (`scripts/lean_glossary.py`). Unknown meanings/dimensions were filled in the **unknowns pass** the same day
(`notes/GLOSSARY-UNKNOWNS-PASS-2026-10-15.md`): GraphExport placeholders → **[NOTE]** from
module headers; dimensions from DEF_META/DEF_DIM/heuristics. **No guessing.**

**Regenerate:** `<local path> scripts/lean_glossary.py`
(inputs: `graph/raw_decls.jsonl` — already complete: 686 thm + 295 def + aux —
and `lean/PositiveGeometryEmergentSpaceTime/*.lean`; no re-export needed).

**Outputs:**
| Path | What |
|---|---|
| `notes/LEAN-GLOSSARY-2026-10-15.md` | this note (counts + overlaps / candidate bridges) |
| `graph/lean-glossary.csv` | full table (searchable in any spreadsheet) |
| `graph/lean-glossary.html` | standalone searchable HTML (client-side filter; no CDN) |
| `graph/lean-glossary-overlaps.json` | machine-readable overlap summary |
| `figures/glossary-overlaps-2026-10-15.png` | module graph: edges = shared physical quantities |

---

## 1. Method (what was / was not inferred)

- **Definitions (259 core):** every non-auxiliary `def` in `raw_decls.jsonl` (aux `mk` /
  `noConfusion` / `recOn` / `ctorIdx` filtered). Meaning taken from the Lean docstring
  when present (**[DOC]**). If the docstring is the generic GraphExport placeholder
  ("Auxiliary definition …") or absent, meaning comes from **`DEF_META`** (**[NOTE]**,
  module header / adjacent comments) or the curated quantity dictionary (**[CURATED]**).
  **No guessing** — if still unclear, leave `unknown` (none left after 2026-10-15 pass).
- **Parameters (322):** binder names extracted from Lean sources, aggregated per
  `(module, binder)`. Tagged only when (a) the binder is an unambiguous long token
  (`m_pi`, `lam4`, `yQ`, …), or (b) the module is already listed for that quantity in
  `graph/analysis.json` `recurring_params`, or (c) EXCLUSION / STRUCT / SC modules force a
  module-level row. Unmatched binders that look like kinematics (`s,t,u,Xij,…`) or
  discrete indices are marked **variable**. Everything else is omitted rather than
  inventing an `unknown` for every `x : ℝ`.
- **Status** (ledger convention):
  - **fixed** — forced by a Lean result / geometry (e.g. `ap 0 = 1/2`, `lam4 = g²` gauge, hypercharges without νᶜ).
  - **cited** — taken from literature or data (`analysis.json` status `input`); geometry does not fix it.
  - **free** — undetermined, or ruled out as "from this geometric route" by EXCLUSION.
  - **variable** — kinematic / index placeholder, not an SM input.
  - **unknown** — documented meaning but not an SM-ledger fixed/cited/free/variable tag.
- **Sources of status:** `graph/analysis.json` `recurring_params` (review keyword hits),
  `notes/EXCLUSION-LEDGER.md`, module headers for STRUCT-1/1b/2, SC-1/2, EW-Z1b (lam4 = VVVV
  contact, **not** Higgs quartic — correction 754f5ef).

Curated quantity ids: `m_π`, `m_ρ`, `m_K`, `f_π`, `σ-term`, `scale (dimensionful unit)`,
`couplings g / lambda`, `shift ansatz (NLSM δ / mesh)`, `LECs L_i / l_i`, `N_c`,
`hypercharges y_i`, `α' (Regge slope)`, `string tension σ`, `dispersion curvature c`,
`vev v`, `b₀ (β-function / curve count)`, `θ_W`, `spurion / quark mass`.

---

## 2. Counts

| | |
|---|---|
| Declarations in export | 686 theorems + 295 defs (= 981; +18 aux induct/ctor/rec in raw_decls) |
| Glossary entries | **605** (259 definitions + 346 parameters) |
| Theorem-graph components | 260 (analysis.json; top sizes 109, 85, 58, 43, 30, …) |
| Distinct physical quantities tagged | 18 (+ kinematics / index) |

**Status breakdown (all entries):**

| status | n | role |
|---|---|---|
| variable | 293 | Mandelstam / planar / spinor / Plücker / indices / combinatorial helpers / types |
| unknown | 156 | defs with documented meaning that are not SM-ledger tagged (not blank physics) |
| fixed | 80 | geometry- or proof-forced / numeric certificates |
| cited | 47 | literature / data inputs |
| free | 29 | undetermined or EXCLUSION-ruled-out as geometry-fixed |

**Meaning / dimension (after unknowns pass 2026-10-15):**

| | n |
|---|---|
| `meaning = unknown` | **0** |
| `dimension = unknown` | **0** |
| [NOTE] fills (was GraphExport placeholder) | 60 |
| [DOC] real Lean docstrings | 197 |
| [CURATED] quantity/binder dictionary | 348 |

See `notes/GLOSSARY-UNKNOWNS-PASS-2026-10-15.md` for before/after and method.

Of the 259 definitions: **all** now carry a meaning tag (**[DOC]** or **[NOTE]** or **[CURATED]**); **all** carry a dimension string.

**Free entries concentrate on two recurring SM blockers:**
- **scale (dimensionful unit)** — 14 free rows across BR4, ScaleNoGo, SG1/SG1b, PG1,
  OrderParameter, NLSM, MassiveLS, SC1, GB1a, PiNGate, SubthresholdGate, UnequalLS.
- **couplings g / lambda** — free in MassiveSpinor, SG1, ScaleNoGo, SubthresholdGate,
  UnitarisedLS, BR5p, LECRatio; **fixed** inside EWZ1b (`lam3`, `lam4`, `a`) where the
  hidden-zero residual forces the gauge values.
- **N_c** — free in STRUCT2, GB1a, MassiveLS, SC1 (EXCLUSION: only odd N follows).


---

## 3. Overlaps / candidate bridges

Same physical quantity under different binder names, or the same quantity living in
**different theorem-graph components** (so Lean has no edge between them today). These
are **proposal-only** bridge candidates — no credit, no Lean change.

### Top overlaps (by #components reached)

| # | Quantity | comps | mods | status | Plain-words bridge |
|---|---|---|---|---|---|
| 1 | **scale (dimensionful unit)** | 32 | 13 | free | The same "unit of mass" hole appears in the scale cluster (BR4 / ScaleNoGo / OrderParameter / PG1), the NLSM chain, SC-1, and several hadron gates. EXCLUSION already records that geometry alone cannot fix v. Any future MG4/SC escape has to break classical homogeneity in **one** shared lemma instantiated by all of these. |
| 2 | **LECs L_i / l_i** | 25 | 6 | fixed | ChPT LECs show up as fixed pattern constraints (FT5aL zero-preserving, MassShift, MassiveZero*, PiKZero, FermionBridge) but live in many small components — a single "LEC from geometry" lemma would glue the S2/S4 forest. |
| 3 | **m_π** | 20 | 6 | cited | Pion mass is a cited input in KEtaGate, KLPhi, PiKZero, PiNSubGate, SplitZeroGate (and appears in STRUCT2 context). Ratio-only rungs (UnequalLS / KL-LAT) already treat it as an input, not a prediction. |
| 4 | **shift ansatz (NLSM δ / mesh)** | 18 | 6 | fixed | δ-shift / mesh offset is fixed inside the NLSM chain (NLSM, MassShift, ShiftForced*, BR1, COS1). The Lean edges already exist for most of this (comp C1); the residual bridge is COS1 / FT2Mesh ↔ MassShift (BR-2 in the theorem-graph note). |
| 5 | **m_K** | 16 | 8 | cited | Kaon mass as cited input across unequal-mass LS / KL / πK gates — same story as m_π; candidate for a shared "unequal-mass LS dictionary" lemma. |
| 6 | **m_ρ** | 16 | 5 | cited | ρ mass is the hadronic unit (m_ρ² = 1) in KEta / KLPhi / SplitZero / PiNSub / UnitarisedLS. SC-1 then predicts m_ρ/√σ = √π against lattice — the unit choice is shared, the prediction is not yet a Lean edge to the gates. |
| 7 | **couplings g / lambda** | 15 | 8 | free (mostly); fixed in EWZ1b | The EW-Z1b gauge relation `lam4 = g²` (VVVV contact) is fixed, but the same coupling letters are free in MassiveSpinor, SubthresholdGate, SG1, ScaleNoGo. Candidate: derive EWZ1b.N (or one helicity) from MassiveSpinor.M (BR-5 in the theorem-graph note). |
| 8 | **σ-term / f_π** | 9 / 8 | 3 | cited | Cheng–Dashen / πN gates share Σ and f_π as cited inputs (KEtaGate, PiNSubGate, SplitZeroGate) — already a soft cluster by quantity, not by Lean edge. |
| 9 | **b₀ (β / curve count)** | 9 | 2 | fixed | SC-2 / SC-2b: b₀ = −3/4 as a weighted count (PARTIAL). Lives in its own components; the mission bridge is to scale via dimensional transmutation (still needs one coupling). |
| 10 | **N_c** | 6 | 4 | free | STRUCT-2, GB1a, MassiveLS, SC1 all mention N_c; EXCLUSION says anomaly consistency only forces odd N. A shared "N_c as combinatorial count" lemma is still open (not selected by ACC+Witten). |
| — | **hypercharges y_i** | (STRUCT1/1b) | 2 | fixed (w/ caveats) | Unique without νᶜ; B−L family with νᶜ unless Majorana (STRUCT-1b). No positive-geometry input — quantity-level island. |

### Same short `def` name, different modules (name collisions)

These are **not** automatically the same quantity — just a reminder to read the module
docstring before identifying them:

| symbol | modules |
|---|---|
| `br` | Associahedron, IsingTiling, MassiveSpinor |
| `m2` / `m3` | FT5aL, IsingOG |
| `M` | IsingTiling8/10, MassiveSpinor |
| `P1`/`P2` | LSResidue, MassiveLS |
| `P4` | LECRatio, LSResidue |
| `P3` | MarkovTrace, LSResidue |
| `v` | OrderParameter, TP1b |
| `f` | BR5p, SG1b |
| `mdot` | COS1b, SliceBridge |

### Recurring free inputs (mission blockers)

1. **Scale / unit of mass** — dominant free input; BR-4 `no_scale` + PG-1 + EXCLUSION.
2. **Couplings outside the EW-Z1b gauge locus** — free until a geometry rule forces them.
3. **N_c = 3** — not selected by ACC + Witten (only odd).
4. **Hadron masses (m_π, m_K, m_ρ) and f_π, σ-term** — cited inputs; ratio-only rungs
   remove the unit but still take mass *ratios* from data / lattice.
5. **Higgs quartic λ_H** — absent from EW-Z1b (EXCLUSION / SC-3 step 0); do not confuse with `lam4`.

---

## 4. How this sits next to the theorem graph

`notes/THEOREM-GRAPH-2026-10-13.md` already measured that credited results sit in
**isolated** declaration components (largest component C0 = 109 has **no** credited
theorems). This glossary adds the complementary view: even without a Lean edge, the
**same SM / hadronic quantity** recurs across those islands. The figure
`figures/glossary-overlaps-2026-10-15.png` draws that quantity-sharing graph at
**module** granularity (40 modules, edges coloured by shared quantity; red = module
contains a credited theorem).

Strongest multi-quantity module pairs (from the figure):
- KEtaGate ↔ SplitZeroGate / PiNSubGate — share f_π, m_π, m_ρ, σ-term (and m_K with SplitZero).
- MassiveLS ↔ SC1 — share N_c, scale, α′.
- SG1 ↔ ScaleNoGo ↔ SubthresholdGate — share couplings + scale.
- GB1a ↔ MassiveLS / SC1 — share N_c + scale.

---

## 5. Limits

- Overlay params in `analysis.json` are keyword hits on reviews (**[EXTRACTED-UNCERTAIN]**);
  this glossary reuses them for status and marks meanings **[CURATED]** only for the
  quantity dictionary above.
- Binder extraction is regex over Lean source headers; it can miss binders written in
  unusual styles and can under-count multi-line signatures.
- Status-`unknown` residual is honest: improving it further means writing Lean docstrings
  and/or linking defs to the SM ledger — not inferring physics from a letter `a : ℝ`.
  Meaning/dimension unknowns were cleared in the 2026-10-15 unknowns pass.
- No credit proposed. No rung run. No push outside `the private research repository` `main`.
