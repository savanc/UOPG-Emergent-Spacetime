# Lean naming map 2026-10-28 (supersedes additions to notes/LEAN-NAMING-MAP-2026-10-15.md; that file is unchanged)

Grok, deep review 2026-10-28 (author approved). The -10-15 map still holds for every module it covers: its renames, its docstring-only aliases and its policy (one canonical Lean identifier per quantity; prior names and literature aliases go in `Also known as:` docstring lines). This note adds the modules that came later and the alias fixes made in this review. **No identifiers were renamed.** Every change below is a docstring or glossary text change, so no statement changed (`lake build` green, AxiomsAll 1027 thm / 538 def / 0 nonstandard / 0 sorry).

Source of truth for every row: `graph/lean-glossary.csv` (regenerated 2026-10-28 by `scripts/lean_glossary.py` from `graph/raw_decls.jsonl`, 1589 exported decls).

## 1. Alias collisions resolved (9 → 0 broken aliases in `graph/lean-glossary-aliases.json`)

An alias was "broken" when the same alias string named two different quantities. Each fix makes the alias module-qualified or more specific. Canonical names are unchanged.

| Alias before | Now | Where |
|---|---|---|
| `FRWZW` (module and count both) | `FRWZW.N` for the count | FRWZW docstring |
| `N` (STRUCT-2 colours vs other N) | `Nc`, `STRUCT2.N` | STRUCT2 docstring |
| `P` (BR5p external momenta vs TP-1b char. poly) | `BR5p.P`, `TP1b.P` | BR5p, TP1b docstrings; glossary NOTE |
| `P3` (Legendre vs trace-order) | `three-state P3` | MarkovTrace docstring |
| `P4` / `u` (Legendre ratio vs Mandelstam u) | `LECRatio.P4`, "in s and u" | LECRatio docstring |
| `br` (affine bracket in 3 modules) | `Assoc.br`, `IsingTiling.br`, `MassiveSpinor.br` | docstrings |
| `eta` (OG signature vs Minkowski form) | `OG eta` (IsingTiling8/10), `eta(v)` (Spinor / SliceBridge) | docstrings; glossary NOTE |
| `mdot` (two Minkowski products) | `COS1b.mdot`, `SliceBridge.mdot` | docstrings; glossary NOTE |
| `t = exp(τλ)` (torus element vs binder `t`) | removed; `torusAct` aka charge cocharacter, the torus element is the binder `t` | glossary NOTE |

Not a collision: the `COLLISIONS` line printed by `lean_glossary.py` (`w`, `m1`, `m2`, `m3`, `ACC`, `ogSignature`, `C2`, `isingMinor`) lists short names reused in different namespaces. They are namespaced Lean identifiers with different meanings per module and do not clash. Listed for readers.

## 2. Modules added since 2026-10-15 (canonical names = Lean identifiers; aliases from docstrings)

From the handoff deltas (notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-22, -23, -28), now applied:

- **`PositiveGeometryEmergentSpaceTime.GradedPositroid`** (GRADED-POSITROID, 2026-10-22): `genW` (aka generation weight vector, ℚ⁵ → 15 Weyl weights), `smW` (aka SM hypercharge weights), `m1` (aka graded first moment / Tr Y), `cub` (aka graded cubic moment component), `ACC` (aka four anomaly cancellation conditions: grav, SU(3)²U(1), SU(2)²U(1), U(1)³). κ = exchangeable cubic coefficient.
- **`PositiveGeometryEmergentSpaceTime.FL1Z`** (FL-1Z, 2026-10-22): `D3` (aka m_ν(ω), D.3 matrix), `w` (aka fixed-point vector (2, −ω², 2ω)), `hv` (aka level-1 valence hypothesis 12n + 6a + 4b = k), ρ (aka Δm²sol/Δm²atm, (m2/m3)²).
- **`PositiveGeometryEmergentSpaceTime.TrialityWhy`** (TRIALITY-WHY, 2026-10-23): `doubletCharge` (aka Z_k charge of one SU(2)-doublet generation, 3qQ + qL), `sphaleronCharge` (aka SU(2)-instanton Z_k charge, N·(3qQ + qL)), `wwxSum` (aka Ibáñez–Ross SU(2)²–Z_k sum), `ccxSum` (aka SU(3)²–Z_k sum), `gravSum` (aka grav²–Z_k sum), `qgOK` (aka no-global-symmetry dichotomy: exact → gauged ∨ broken), `nullFamily` (aka declared (k, c) null family, 170 pairs).
- **`PositiveGeometryEmergentSpaceTime.LeanCert2`** (LEAN-CERT-2, 2026-10-28), split into the nested modules `PositiveGeometryEmergentSpaceTime.LeanCert2.{Core, FrwzwK0p, FrwzwK0m, FrwzwK1p, FrwzwK1m}` (the first nested modules in the repo; now registered by `mod` in scripts/theorem_graph.py): `dotL` (aka list dot product), `rowsM` / `colsM` (aka rows-/columns-to-matrix), `lenL` (aka row-length bound), `mulL` (aka list matrix product entry), `tposL` (aka transpose consistency check), `zeroL` (aka list check MK = 0), `splitL` (aka splitting certificate PM + KQ = d·1), `injL` (aka injectivity certificate QK = d·1), `certL` (aka kernel-dimension certificate); data `<cert>_{Mr, Mc, Kr, Kc, Pr, Qr, Qc, d}` for `abhyL5/6/7`, `brokenB1`, `frwzw_k0p/k0m/k1p/k1m` (aka certificate data).

Not in any handoff; added here from the module docstrings:

- **`PositiveGeometryEmergentSpaceTime.LeanCert`** (LEAN-CERT-1, 2026-10-23): `ACC` (aka the four ACC at yQ = 1), `R` (aka GPOS domain {p/q : |p| ≤ 10, 1 ≤ q ≤ 10}), `Xcoef` (aka planar-variable coefficient in X_{a,b}); data `abhy{5,6,7}_{M,K,P,Q,d}`, `gpos_{M,K,P,Q,d,x0}` (aka certificate data); planted-wrong data `abhy6_Kflip`, `gpos_Kflip`, `gpos_Pbad`.
- **`PositiveGeometryEmergentSpaceTime.Cascade1`** (CASCADE-1, 2026-10-23): `A5` (aka cascade S2 amplitude, n = 5), `Rel5` (aka EM n5 zero relations), `Zeros5` (aka n5 hidden-zero condition); data `em4_{M,K,P,Q,d}`, `em5_{M,K,P,Q,d}` (aka n4 / n5 relation matrix, Θ_3 basis, splitting / injectivity certificate, certificate scale).
- **`PositiveGeometryEmergentSpaceTime.Cascade1b`** (CASCADE-1b, 2026-10-23): `offsetsE0` (aka the nine E0 offsets at n = 6). The binders `m13 … m46` have no docstring meaning, so the glossary marks them "unverified" (open item; meaning not guessed).
- **`PositiveGeometryEmergentSpaceTime.IntChamber`** (INT-1, 2026-10-22): `chamberSign` (aka chamber label, sign vector σ), `f0` / `f1` (aka f₀ number of vertices / f₁ number of edges), `forms` (aka wall arrangement, the six wall forms), `pt` (aka pair point), `vertexType` (aka face type, I_comb), `σPos` / `σWall` / `σBeyond` (aka all-positive chamber / merging wall / beyond the wall).

## 3. Open naming items (not changed here)

- **101 `defsWithUnderscore` lint hits.** All are certificate-data defs (`abhy5_M`, `em4_K`, `frwzw_k0p_Qc`, …) in LeanCert, LeanCert2, Cascade1 and BridgePLAssoc (`channel01_23` …). Renaming them to Mathlib lowerCamelCase would change public identifiers that reviews, preregs and run artifacts cite, including the locked generator `sims/leancert2/emit_lean.py`. This is proposed, not done. For publication, either rename them in a new module version or add `@[nolint defsWithUnderscore]`.
- **`TP1bMatrix`** has no primary rung because no review mentions the module by name. It needs a hand decision; see DEEP-REVIEW-2026-10-28.
- **Unverified physics binder rows:** 125 of the 186 rows in `lean_glossary.py` still say "unverified", which means no docstring names their meaning. They are listed in graph/lean-glossary.csv.
