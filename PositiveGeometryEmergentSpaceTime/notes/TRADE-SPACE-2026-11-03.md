# Trade space 2026-11-03: supersede note for notes/TRADE-SPACE-2026-10-28.md (Grok, the author)

Earlier trade-space notes and their addenda are unchanged. This note re-examines every rung touched by the 2026-10-31..11-03 alignment work
(pilot, Phase B/C sanity, BLIND-2, LEAN-CERT-2 k = 2,3, JORD-1 Der) for changes in status, failure mode, credit and reopen trigger.
**No locked verdict, blocker-index row, tag or flag is changed here.** Every change below is a PROPOSED supersede that needs an author card
(AUTORESEARCH-METHOD.md: tag / flag changes need a card). Figure: figures/trade-space-2026-11-03.mmd/.png (dated copy of
trade-space-traffic-light.mmd with stale nodes updated and an Alignment subgraph).

Tags: PROVED (Lean, standard axioms) / SIMULATED (run id) / CITED / CONJECTURE / SPECULATION / [ASSESS] (reviewer judgement).

## 0. Mission position
- **Goal:** a positive-geometry structure that boots up the Standard Model with zero fitted parameters. **NOT ACHIEVED.**
- R4-DM v2 (locked, af4430e): 1/89 DERIVED (EWZ1b.forced, conditional, amplitude-sourced, SM-MATCH, CGW 2601.16860 CITED); meter_Q 0/73; positive-geometry-sourced 0. **Unchanged.** [ASSESS: the alignment work adds no item to either meter; it checks that existing items say what the prose says.]
- Credit tally 3.5 / 3 (blind 2.5: MR-1b 1, MR-4 1, KL-LAT 0.5; VR 1.0: MR-2 0.5, KS-1 0.25, MR-1f 0.25). **Unchanged.** MR-1b's credit is robust to the sign correction: ratios of magnitudes are sign-invariant (PROVED `rho3_neg`, `f4_neg`, `ratios_agree`).
- AUTORESEARCH-STOP (619bacf) is in force. This note does not lift it and does not pick a rung.
- Lean base: main 142 modules, 1378 thm / 798 defs, 0 non-standard axioms, 0 sorry (PROVED); Alignment layer 67 modules outside `import PositiveGeometryEmergentSpaceTime` (notes/LEAN-MAP-2026-11-03.md).

## 1. Rung-by-rung re-examination
| Rung | Locked status (unchanged) | New input 10-31..11-03 | Effect | Trigger fired? | Proposal |
|---|---|---|---|---|---|
| **LEAN-CERT-2** | CERTS-OK (Python); Lean PARTIAL-LIMIT k = 2,3; FM-SPEC FM-LIMIT; CONV-FLIPPED | `LeanCert2K23`: k2p/k2m/k3p/k3m finrank = 5/0/10/2 PROVED by per-block kernel encoding under memrun2 (ad57ef6); certL, X-permutation laws and `*_N_rows` vanish symbolically; sampled checks SIMULATED | The Lean half of the rung is now complete | **YES** - clause 2 ("a memory-lean kernel encoding (per-conjunct or per-row-block decide …) for the k = 2, 3 certificates"); clause 3 ("a repo fact that needs certificates at this size") also fired via JORD-1 Der | **SUPERSEDE-1:** Lean PARTIAL-LIMIT → PROVED for all 8 counts; drop FM-LIMIT (keep FM-SPEC for the null). CERTS-OK and credit 0 stay. Basin B4 FM tally becomes SPEC 1, LIMIT 0. Needs author card |
| **LEAN-CERT-1** | RESOLVED; credit 0 | JORD-1 Der: exact rank 677 of a 17445 × 729 system, kernel 52, by chunked kernel certificates (8469ca1) | Method now used at N in the hundreds | **YES** - "a SIMULATED repo fact that is an exact rank/kernel statement at N in the hundreds" (executed by JORD-1 Der) | **SUPERSEDE-2 (annotation only):** record the trigger as fired and executed; status RESOLVED unchanged, credit 0 (method). BLIND-2 wording fix: N_ACC = 2 with Y_Q normalised (edit queue) |
| **JORD-1** | NO-GO; FM-SPEC; CONV-FLIPPED | Jordan identity + finrank Der J3(O) = 52 PROVED (Alignment/Sanity/Jord1Der*); identification with f4 not formalised | The Reason's premise "f4 = Der h3(O)" is now dimension-supported in Lean (it was CITED). NO-GO content (closure = spin(9), dim 36 > 12) untouched | No (needs checker v2, positivity-native J or Krasnov-J) | **SUPERSEDE-3 (annotation):** add "dim Der h3(O) = 52 PROVED; ≅ f4 CITED" to the Reason. No status change |
| **SURF-1′** | NO-GO; FM-RANGE; CONVENTION-ROBUST | K3,3 crossed-box coefficients kernel-checked in 64 orientation blocks (`Surf1Sanity.coeffs_K33`); D174/D175 ties PROVED; blind pilot | The NO-GO's last SIMULATED premise is gone: `no_sign_coherent_N` now holds unconditionally in Lean | No (needs two loops / fundamental matter / crossed-channel-only reason) | **SUPERSEDE-4 (evidence upgrade):** Evidence "PROVED from a SIMULATED table" → "PROVED, unconditional". Verdict, FM, credit unchanged. Paper II:421 wording queued |
| **EW-Z1b** | SM-MATCH, CONTAMINATED, FRONTIER-THEORY | Independent 5D index-sum Feynman-rule derivation = Lean `EWZ1b.N` 200/200 exact (EWZ1B-INDEP-2026-11-03-r1, SIMULATED); Lean tie D170 still open | The one DERIVED meter item no longer rests on a single generator | No (needs EW-Z1c doublet/θ_W definition) | **SUPERSEDE-5 (evidence):** add the independent SIM. Meter item stays CONDITIONAL; no status change |
| **M3** | REFUTED (blind FAIL 3.8σ) | 3.84σ rule arithmetic PROVED (`orig_nsigma_rounds`, `M3Blind.nsigma_rounds`); blind DIFFERENT on inputs (input transcription, not physics) | Refutation is now arithmetic-checked | Trigger is "None" | None. Paper I:562 citation queued |
| **H-T5 (d)** | REFUTED (superseded by tree-network rule, H-T5d PASS) | D161 tie PROVED; GP sign rule PROVED at n = 3 by exhaustion (1 of 64 patterns) | The PASS's cited premise is checked at n = 3 only; general n remains CITED (1807.03282 eq. 2.4) | n/a (row is the refuted (d) rule) | None; caveat narrows to "transcribed for general n; recovered by exhaustion at n = 3" |
| **HG-DIM-1** | NO-GO; FM-MODEL; CONVENTION-ROBUST | D177 tie PROVED; blind pilot; kernel facts n = 5..9; pilot gaps G1/G2 (mean is a counting identity, per-edge κ only for two K7 edges in Lean) | Scope correction is **already applied** in paper-curvature main.tex:289 | No (n ≥ 12 counterexample / weighted measure) | None |
| **HG-DIM-2** | REDUNDANT; FM-KNOWN FM-METHOD; CONVENTION-ROBUST | Blind EQUIV on numbers, ORIG-STRONGER on rigour | None | No | None |
| **CAPPED-FORMAN-1** | REDUNDANT | Blind DIFFERENT: the blind proves the per-face cap "for all k ≥ 3"; the paper says "for all k" | Scope wording only | No | Paper II:802, curvature :474/:567 wording queued |
| **RG-IR-1** | NO-GO; FM-FREE; CONVENTION-ROBUST | Pilot gap R2 closed by `affine_UV_IR` (generic linear flow); "proves the affine structure" overstated → "certifies the algebra" | Scope correction | No (needs derived UV boundary condition) | None (already reflected: Paper II main.tex:685 "Lean, corrected") |
| **RP-TN-1** | NO-GO; FM-TAUT | D184 tie PROVED; blind EQUIV | None | No | None |
| **TRIALITY-WHY** | NO-GO (NOT-FORCED / TAUT); CONV-UNSCREENED | Blind EQUIV | Blind used the same convention, so it is **not** a convention re-check | No | None |
| **GRADED-POSITROID** | NO-LINK / NO-GO; CONV-UNSCREENED | Blind EQUIV (same ACC text) | Not a convention re-check | No | None |
| **MR-3** | NO-GO; CONTAMINATED; CONV-UNSCREENED | Blind BLIND-STRONGER: on 0 < r < 1/2 only J = 0; c1 < 0 for r > 1/2 (range correction) | Range wording only; NO-GO unchanged. An independent re-formalisation is not a convention change (rule needs a proved physics-preserving equivalence) | No | Paper II:399 caption queued; flag stays CONV-UNSCREENED |
| **OP-2 scale** | NO-GO; CONV-UNSCREENED | BR-4 blind/Compare: `orig_to_blind`, `blind_to_orig`, `determines_iff_factors`, `blind_negative_degree` (PROVED): the scale-blindness statement is equivalent between the ℕ-degree / all-c ≠ 0 and ℤ\{0}-degree / c > 0 conventions | This is a proved equivalence between two conventions with the verdict holding in both | n/a | **SUPERSEDE-6 (flag):** CONV-UNSCREENED → CONVENTION-ROBUST (BR-4 Compare). [ASSESS: weak form - a mathematical scaling convention, not a units or field-basis change.] Needs author card |
| **FL-1Z** | ILL-DEFINED (NOT-WELL-POSED); FM-FREE FM-SPEC | D169 tie PROVED | Premise of `D3_rank_one` ties now checked | No | None |
| **CASCADE-1b r2** | PASS (graded 10-29), H REFUTED-AS-STATED, RATIOS-FREE | none new | 10-28 note listed it as UNGRADED; that line is superseded by the 10-29 grading already in the index | — | Status line only (figure node updated) |
| **CHIRAL-LATTICE-1 v2** | RESOLVED (vacuous) | blueprint rows | None | No | None |
| **BR-4, MR-1b** (outside index) | PASS / credited | BR-4 blind DIFFERENT (generality: blind covers negative degrees); MR-1b sign error fixed (101db50, v8.1) | Wording only; credit robust | — | BR-4 II:365 queued; MR-1b done |

Every other index row: no new input, no change (re-read 2026-11-03; the reopen-trigger column was checked row by row for the inputs above).

## 2. Reopen triggers that fired
1. **LEAN-CERT-2**, clause "memory-lean kernel encoding … for the k = 2, 3 certificates" - FIRED and executed (ad57ef6). Clause "a repo fact that needs certificates at this size" - FIRED (JORD-1 Der). → SUPERSEDE-1.
2. **LEAN-CERT-1**, "a SIMULATED repo fact that is an exact rank/kernel statement at N in the hundreds" - FIRED and executed (JORD-1 Der, 8469ca1). → SUPERSEDE-2.
No physics reopen trigger fired (none of SURF-1′, JORD-1, EW-Z1b, HG-DIM-1/2, CAPPED, RG-IR-1, RP-TN-1, TRIALITY-WHY, GRADED-POSITROID, M3, FL-1Z, CASCADE-1b, MR-3, OP-2).

## 3. Convention-invariance rule (AUTORESEARCH-METHOD.md:185ff) applied
- Valid re-check found: **OP-2** via BR-4 Compare (proved equivalence) → SUPERSEDE-6.
- Not valid re-checks (independent re-formalisation or same convention): MR-3, TRIALITY-WHY, GRADED-POSITROID, HG-DIM-2 blind, RP-TN-1 blind. Flags unchanged.
- MR-1b: sign convention flip does not change the credited ratios (PROVED). No flag (credited, not a NO-GO).
- Still CONV-UNSCREENED after this note: the index lists 26 occurrences of CONV-UNSCREENED (one becomes ROBUST if SUPERSEDE-6 is approved). Screening them is next-rung candidate 3.

## 4. Basins
B1, B3 (conditional) and B5 stay saturated. B4 (Lean certification) loses its FM-LIMIT if SUPERSEDE-1 is approved and gains a working method at the hundreds scale [ASSESS]. No new basin opens: the alignment layer is method, not a physics basin.

## 5. Gated rungs (unchanged; all need the author's go)
- **M5** massive on-shell dictionary tick: unchanged.
- **MC-1** filter calibration (method, credit 0): unchanged.
- **TS-1** time-stamped predictions: unchanged; FL-1Z still gives no TS-1 entry.
- **EW-Z1** 5-6 pt / EW-Z1c: unchanged. The independent EW-Z1b SIM firms up the conditional DERIVED item but does not raise EW-Z1's prior [ASSESS].
- **CASCADE-2** (prereg 012ead2): unchanged, prior of a ratio fix ~0.05 (CONJECTURE).
- **Pilot-wave / B11**: unchanged.

## 6. Proposed author cards (drafts; nothing applied)
- CARD-A (SUPERSEDE-1): "LEAN-CERT-2: Lean PARTIAL-LIMIT k = 2,3 → PROVED (LeanCert2K23, ad57ef6); FM tags FM-SPEC FM-LIMIT → FM-SPEC; status CERTS-OK and credit 0 unchanged. Approve?"
- CARD-B (SUPERSEDE-6): "OP-2 scale: flag CONV-UNSCREENED → CONVENTION-ROBUST via BR-4 Compare (`orig_to_blind`/`blind_to_orig`). Approve?"
- Annotations (SUPERSEDE-2..5) can go in one card: LEAN-CERT-1 trigger executed; JORD-1 dim Der = 52 PROVED; SURF-1′ unconditional; EW-Z1b independent SIM.

## 7. Applied (2026-11-03, author approved (2026-11-03), the author)
SUPERSEDE-1 (CARD-A) and SUPERSEDE-6 (CARD-B) are applied. SUPERSEDE-2 to 5 are recorded as row notes. See reviews/TAG-CHANGE-2026-11-03.md. The blocker index is regenerated: CONV-UNSCREENED 26 → 25, CONVENTION-ROBUST 4 → 5, FM-LIMIT dropped. Credit is unchanged. Sections 1–6 above stay as written; they record the proposal.
