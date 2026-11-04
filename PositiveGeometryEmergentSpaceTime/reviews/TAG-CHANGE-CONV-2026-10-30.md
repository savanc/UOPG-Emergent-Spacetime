# Tag changes after the convention re-checks (2026-10-30)

Authority: author approved (2026-10-30). Follows AUTORESEARCH-STOP cbc9a16.
This record **supersedes** the verdict tags in the original reviews (reviews/JORD-1-*, reviews/LEAN-CERT-2-*), which are locked and not edited.
Applied through `scripts/blocker_tags.py` (rows + CONV_DONE) and the regenerated notes/BLOCKER-INDEX-2026-10-13.md.

| Rung | Old tags | New tags | Basis |
|---|---|---|---|
| JORD-1 | ILL-DEFINED, NO-GO | **NO-GO** | CONV-JORD-1 prereg 32e8a9c, result c6b1f2c: FLIPPED under the trace-scale equivalence (JordConv, PROVED); verdict NOT-POSITIVITY-CLOSED / CHOICE-UNIQUE / NO-GO. Original checker recorded as **fragile (FM-SPEC)**: its F_A idempotent flag used the unit-scale Jordan product. |
| LEAN-CERT-2 | ILL-DEFINED | **CERTS-OK** (Python only) | CONV-LEAN-CERT-2 prereg 3131dd6, result a50369a: N2′ 0/480 under class key (K, PM, Q, d) (LeanCertConv, PROVED). **Lean stays PARTIAL-LIMIT for k = 2, 3.** Original N2 null recorded as fragile (FM-SPEC). |

Tally effect: ILL-DEFINED 5 → 3; NO-GO 32 → 32 (JORD-1 already carried NO-GO, so only ILL-DEFINED is dropped; the brief's "NO-GO +1" does not apply); new status label CERTS-OK 0 → 1. FM columns unchanged (both already FM-SPEC). Credit: 0 each.

## Equivalence review, LEAN-CERT-2 class key (PositiveGeometryEmergentSpaceTime, 2026-10-30) — PASS
Read: prereg/CONV-LEAN-CERT-2-canonical-class-2026-10-30.md, reviews/LEAN-CERT-2-convcheck-2026-10-30.md, lean/PositiveGeometryEmergentSpaceTime/LeanCertConv.lean.
- `valid_iff_of_PM_eq` / `split_iff_of_PM_eq` (PROVED) show validity (MK = 0, PM + KQ = dI, QK = dI) depends on P only through PM. So two certificates with the same (K, PM, Q, d) are valid together or not at all.
- Meaning is kept [ASSESS, on paper]: the certified quantity is the kernel dimension k (columns of K). With d ≠ 0, QK = dI makes K injective and PM + KQ = dI gives d·v = K(Qv) for every v in ker M, so K spans ker M ⊗ ℚ. P is only a witness; it never enters the certified number. Changing P with PM fixed is therefore a change of representative of the same certificate, which meets refinement (a).
- Notes, not caveats: (i) the key is the minimal invariant (PM), not the screened HNF/SNF; this was declared in the prereg; (ii) `Valid` does not itself require d ≠ 0 or state the rank conclusion; that step is the on-paper argument above, unchanged by the class key; (iii) the class key is coarser only in P, so an accepted K, Q or d corruption still counts.
