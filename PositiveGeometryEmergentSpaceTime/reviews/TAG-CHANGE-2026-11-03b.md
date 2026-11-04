# Tag change record b (2026-11-03): SUPERSEDE-7, KL-LAT / KS-1 Lean evidence (note only)

Authority: author approved (2026-11-03). The proposal is in notes/alignment/CREDITED-2026-11-03.md (6a01b7b). AUTORESEARCH-STOP (619bacf) stays in force. **Credit is unchanged** (3.5/3: KL-LAT blind 0.5, KS-1 VR 0.25). No status or tag changes.

This record **supersedes, in part, the Lean-evidence wording** in the locked records listed below. Those records were not edited:
- prereg/KL-1-MR-1f-KS-1-prereg-2026-10-13.md:7;
- reviews/KL-1-MR-1f-KS-1-result-2026-10-13.md:7;
- reviews/KL-LAT-result-2026-10-13.md:5.

It follows the style of SUPERSEDE-1 to SUPERSEDE-6 (reviews/TAG-CHANGE-2026-11-03.md).

## Supersede

| # | Rung | Old evidence wording | New evidence wording | Reason | Evidence |
|---|---|---|---|---|---|
| SUPERSEDE-7 | KL-LAT, KS-1 | "the intercepts are fixed by demanding that the dual zero line α_ρ(t)+α_K(u)=1 be exactly the CGW / MR-4 hidden-zero line … PROVED (UnequalLS.zero_line, zero_line_conv)" | Intercept derivation **PROVED** in two steps in `PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.KLLAT`: (1) `rho_intercept_from_pipi`: the equal-mass ππ hidden-zero line fixes α_ρ(mπ²) = ½; (2) `k_intercept_from_rho`: given (1), the πK line fixes α_K(mK²) = ½. The πK line **alone** fixes only the sum a + b = 1 − α′(mπ² + mK²) (`KlLatBlind.zero_line_conv`, `split_not_forced`). `UnequalLS.zero_line` / `zero_line_conv` **assume** the ½ intercepts and are a **consistency check**, not the derivation. | BLIND-3 (blind statement written from the prose, prereg e6e1666 before opening originals) found the cited theorems take α(m_P²) = ½ as a hypothesis. The predicted numbers use exactly the forced intercepts, so no value moves. | e6e1666 (prereg), cdb8c21 (Compare/KLLAT, axiom audit: standard axioms only, 0 sorry, 0 native_decide), 6a01b7b (blueprint rows C11, C12: OVERSTATES) |

Blueprint rows C11 and C12 (notes/alignment/blueprint-credited-2026-11-03.tsv) keep their OVERSTATES verdict. That verdict describes the original evidence pointer. The resolution is this record.

## Files changed
- `scripts/blocker_tags.py`: a note is appended to the KS-1 row text; the original text is kept. KL-LAT is not an index row; it sits in the official tally line only.
- notes/BLOCKER-INDEX-2026-10-13.md is regenerated. Before this change the script reproduced the committed index byte for byte.
- Paper wording follows in the v8.2 / v9.2 paper edits (notes/PAPER-EDIT-QUEUE-ADDENDUM-2026-11-03.md).

Tally effect: none. Tags, verdict tallies, FM and CONV flags are unchanged. Credit is 0 change.
