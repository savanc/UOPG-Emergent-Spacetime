# CHIRAL-LATTICE-1 v2 result (1 rung, Grok, 2026-10-30; author approved)

Supersedes v1 (prereg 8733135, result d26f3b4; v1 files unchanged). Prereg a921fff (pushed alone first), guard refusals edc6a67. Locked checker `sims/chirallat1v2/chirallat1v2_checker.py` (sha256 8649f9eb…cd95), unchanged after the push. Outputs: `sims/chirallat1v2/chirallat1v2_{planted,broken,live}.json`.

## Verdict (locked, as-is; no hand adjudication)
**VACUOUS.** SIMULATED. 71 records (v1 corpus at 8733135): BITES 0, ESCAPED 0, NOT-BITES 71. Every basin `a` (B1 6, B2 2, B3 2, B4 2, B5 5, B7 1, B8 1, RG-IR 1, pre-basin 51); B6/B9/B10/B11 NO-RECORD.
Clause census: 24 fermion-sense chiral clauses in 9 records (M3, MR-1f-eta, FT-1, MR-7′, SC-1, STRUCT-1, X6 / XD-6 / R2, BRIDGE-PL-ASSOC, GRADED-POSITROID): 20 mention (no output verb), 3 negated, 1 modal (STRUCT-1 reopen line), 0 input, **0 claim**.

- Planted: ALL OK. The 9 v1 false-positive records → NOT-BITES; synthetic S1, S2 (output chiral fermion, no escape), S5 (claim + negated escape), S14 (markdown), S15 (NFKC ligature) → BITES; S3 domain wall, S4 overlap/Ginsparg–Wilson → ESCAPED; S6–S13 (cannot, rules out, ≠, ChPT ×2, input labels, reopen trigger, mention) → NOT-BITES; verdict map incl. null-gate failure; gate self-tests.
- Broken: 7/7 rejected. No-negation (fails S6, S7, S8, FT-1, MR-7′); no-ChPT-exclusion (S9, S10, FT-1, MR-7′); no-INPUT (S11); no-MODAL (S12, STRUCT-1); no-ESC (S3, S4); no-normalisation (S15); empty corpus → ILL-DEFINED.
- Null: 45 control records (B1, B4, hadron/ChPT/LS pre-basin rungs): `c` rate 0/45; gate passes.
- Rivals: matches the FM-QNBLIND prior (all NOT-BITES); does not match the v1 locked checker (BITES, 9).
- CONV-NA (text classification; no physics convention). Markdown/NFKC invariance planted (S14, S15).

## Comparison with v1
v1 locked: BITES [MECH-FP] on 9 records, then a report-only hand reading said VACUOUS. v2 locked: VACUOUS with no reading step. The two agree on substance; the difference is that the verdict now comes from the instrument. Of the 9 v1 records, 5 no longer contain a fermion-sense chiral clause (ChPT senses removed or no chiral word: MR-2b, MR-3, MR-3b, FZ-1, STRUCT-1b); BRIDGE-PL-ASSOC's Weyl clauses are mentions (no output verb); FT-1/MR-7′ are negated (≠); STRUCT-1's reopen line is modal.

## Observations (report-only; none changes the verdict; no checker flaw recorded)
- The INPUT screen fired on 0 live clauses: the input/output distinction was tested only in planted S11, not exercised by the corpus.
- v2's FERM is narrower than v1's HIT (no bare "fermion", "hypercharge", "generation"); a claim worded only as "produces the SM fermion content" without chiral/Weyl/handed vocabulary would be missed. Declared in the prereg rule; a reopen route if such a record appears.
- Method-integrity only: v1 outcome known (prereg §1), VACUOUS expected, credit 0.

## Lean
None added (optional). v1 `PositiveGeometryEmergentSpaceTime.ChiralLat1` stands. AxiomsAll unchanged (1185 thm / 637 defs / 0 nonstandard / 0 sorry-dependent).

## Credit
Proposal: 0.

Failure-mode: FM-QNBLIND (no basin record claims chiral fermion output, so Nielsen–Ninomiya has nothing to act on). The v1 instrument's FM-SPEC is superseded by this locked instrument; the v1 row's tag change (ILL-DEFINED → superseded) is a proposal for PositiveGeometryEmergentSpaceTime/the author, not applied.
