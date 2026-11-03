# Tag changes after the alignment work (2026-11-03)

Authority: author approved (2026-11-03). Items (a) and (b) are CARD-A and CARD-B of notes/TRADE-SPACE-2026-11-03.md §6 (fddab86). AUTORESEARCH-STOP (619bacf) stays in force. Credit is unchanged by every item below.
This record **supersedes**, in part, the verdict lines in the original reviews (reviews/LEAN-CERT-2-*, and the OP-2 / BR-4 records). Those reviews are locked and were not edited.
The change is applied through `scripts/blocker_tags.py` (row text, `FM`, `CONV_DONE`) and the regenerated notes/BLOCKER-INDEX-2026-10-13.md, in the same way as reviews/TAG-CHANGE-CONV-2026-10-30.md (eb384df).

## Supersedes

| # | Rung | Old | New | Reason | Evidence |
|---|---|---|---|---|---|
| (a) SUPERSEDE-1 | LEAN-CERT-2 | CERTS-OK (Python); Lean **PARTIAL-LIMIT** (k = 0, 1 PROVED; k = 2 over the RSS cap; k = 3 not attempted); FM `FM-SPEC` `FM-LIMIT` | CERTS-OK (Python); Lean **PROVED for all 8 counts**; FM `FM-SPEC` | Reopen clause "a memory-lean kernel encoding … for the k = 2, 3 certificates" fired and was executed. `LeanCert2K23`: `k2p/k2m/k3p/k3m_finrank` = 5 / 0 / 10 / 2 via `certL`, plus X permutation laws and symbolic vanishing of the N rows. The clause "a repo fact that needs certificates at this size" also fired (JORD-1 Der). The sampled checks stay SIMULATED. Credit 0. | ad57ef6 (module), f25ae12 (Phase C axiom audit: standard axioms only), notes/alignment/SANITY-2026-11-03b.md |
| (b) SUPERSEDE-6 | OP-2 scale | NO-GO; `CONV-UNSCREENED` | NO-GO; **`CONVENTION-ROBUST`** | AUTORESEARCH-METHOD.md:185ff: a valid re-check must show that the verdict survives a change of convention. BR-4 Compare proves that the blind statement (over ℝ, invariance under c > 0, integer degree k ≠ 0) and the original (any field, nonzero c, natural degree k) imply each other on their common core (ℝ, k : ℕ, k ≠ 0): `orig_to_blind`, `blind_to_orig`. "f determines σ" ↔ "σ factors through f" is `determines_iff_factors`, and `blind_negative_degree` extends the result to k < 0. The two statements differ in generality (Compare verdict DIFFERENT), but the no-go holds under both. **Weak case (caveat):** this is a mathematical scaling convention (degree and sign range of the rescaling), not a change of units or field basis. | a73cd28 (Compare/BR4.lean), notes/alignment/BLIND-2026-11-03.md |

Tally effect: CONV-UNSCREENED 26 → 25 and CONVENTION-ROBUST 4 → 5 (index occurrences). FM-LIMIT 1 → 0 rungs. Tags and verdict tallies are unchanged. Credit: 0 and 3.5/3 unchanged.

## Note-only items (same approval; row text only, no tag change)

| # | Rung | Note | Evidence |
|---|---|---|---|
| SUPERSEDE-2 | LEAN-CERT-1 | Reopen trigger "a SIMULATED repo fact that is an exact rank/kernel statement at N in the hundreds" FIRED and was executed by JORD-1 Der (finrank_ℚ Der J3(O) = 52 via chunked kernel certificates). | 8469ca1 |
| SUPERSEDE-3 | JORD-1 | dim Der h3(O) = 52 is **PROVED** (`Jord1Der.finrank_der`). Der h3(O) ≅ f4 stays **CITED** (not formalised). NO-GO and FM-SPEC are unchanged. | 8469ca1 |
| SUPERSEDE-4 | SURF-1′ | The K3,3 coefficient table, the last SIMULATED premise, is kernel-checked (`Surf1K33.coeffs_K33`, 64 orientations × 4 blocks; `claimEnumerated`). The Lean no-go is now **unconditional**. | 4ab351e |
| SUPERSEDE-5 | EW-Z1b | An independent SIM, a 5D index-sum Feynman-rule derivation, agrees with Lean `EWZ1b.N` on 200/200 exact points, and the controls fail as expected (run **EWZ1B-INDEP-2026-11-03-r1**, SIMULATED). The Lean-side Feynman-rule tie is still open. | e9817d4 |

## Files changed
- `scripts/blocker_tags.py`:
  - row text for LEAN-CERT-2, LEAN-CERT-1, JORD-1, SURF-1′ and EW-Z1b (appended; the original text is kept);
  - `FM["LEAN-CERT-2"]` changed from `FM-SPEC FM-LIMIT` to `FM-SPEC`;
  - `CONV_DONE["OP-2 scale"]` added;
  - the `CONV_DONE["LEAN-CERT-2"]` text is annotated.
- notes/BLOCKER-INDEX-2026-10-13.md is regenerated. Before this change the script reproduced the committed index byte for byte.
- notes/TRADE-SPACE-2026-11-03.md: an "Applied" addendum. figures/trade-space-2026-11-03.mmd/.png: the LC2 node and the OP-2 edge are updated.
