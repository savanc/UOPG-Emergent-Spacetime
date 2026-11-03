# Tag change: CHIRAL-LATTICE-1 v1 superseded, v2 resolved (vacuous) (2026-10-30)

Authority: author approved (2026-10-30).
Public-bound form: author approved 2026-10-30. Follows AUTORESEARCH-STOP 3a0aa3b; docs only, no rung run.
This record **supersedes** the verdict tags in the original reviews (reviews/CHIRAL-LATTICE-1-result-2026-10-30.md,
reviews/CHIRAL-LATTICE-1v2-result-2026-10-30.md), which are locked and not edited. Applied through `scripts/blocker_tags.py`
(rows + CONV_NA text + new status label) and the regenerated notes/BLOCKER-INDEX-2026-10-13.md.

| Rung | Old tags | New tags | Basis |
|---|---|---|---|
| CHIRAL-LATTICE-1 (v1) | ILL-DEFINED | **SUPERSEDED** (by v2, result 4166f30) | v1 prereg 8733135, result d26f3b4: locked keyword checker said BITES on 9 records; a hand adjudication read all 9 as false positives (VACUOUS). The instrument is replaced by v2. FM tags kept (FM-SPEC, FM-QNBLIND); CONV-NA kept. |
| CHIRAL-LATTICE-1 v2 | RESOLVED | **RESOLVED (vacuous)** | v2 prereg a921fff, result 4166f30, count fix cc6a7b5 (verdict unchanged): locked clause checker VACUOUS, 0 BITES / 0 ESCAPED / 71 NOT-BITES, no hand adjudication. FM-QNBLIND and CONV-NA kept. |

`SUPERSEDED` was not an existing tag value. It is added as a non-blocking status label, with a one-line definition in
notes/AUTORESEARCH-METHOD.md (item 11) and in the BLOCKER-INDEX header. `RESOLVED` already existed; "(vacuous)" is recorded in the
v2 Reason text, so the tag value itself is unchanged.

Tally effect (73 rungs): ILL-DEFINED 4 → 3; SUPERSEDED 0 (new) → 1; RESOLVED 3 → 3 (v2 already carried RESOLVED). All other tag
counts unchanged. FM columns unchanged. Credit: 0 each.

Also updated: EXCLUSION-LEDGER CHIRAL-LATTICE rows (v1, v2, placeholder) and the trade-space node CHL (label + class `b_resolved`),
PNG re-rendered. Papers untouched (pinned to snapshot 16c67a4).
