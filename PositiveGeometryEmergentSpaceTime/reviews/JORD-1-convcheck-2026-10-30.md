# JORD-1 convention-invariance re-check (2026-10-30)

Authority: author approved (2026-10-30). Prereg `prereg/CONV-JORD-1-trace-scale-2026-10-30.md`, pushed alone as 32e8a9c before any checker ran (guard refusals: `sims/convcheck/guard_refusal_jord1.txt`).

## Outcome: **FLIPPED** (FM-SPEC; reopen)
Locked verdict ILL-DEFINED came from the F_A consistency flag failing on a *mixed* scale (E_i at unit trace scale, P_ij at 2P). Under the named equivalence (uniform trace-form rescaling of representatives, convention CA = all unit, CB = all 2P), both conventions give: all_idempotent=true, stab_hist {21:1200, 28:75, 36:51}, SM-type hits [], consistent=true. New verdict: **NOT-POSITIVITY-CLOSED / CHOICE-UNIQUE / NO-GO** (tierA NOT-POSITIVITY-CLOSED, tierB k=1). Well-defined; the ILL-DEFINED was an artefact of the locked checker's mixed normalisation. Proposed tag change ILL-DEFINED→NO-GO is left to PositiveGeometryEmergentSpaceTime/the author (index shows it in the Reopen flag only).

## Well-posedness (Lean, PROVED, 0 sorry, no native_decide)
`lean/PositiveGeometryEmergentSpaceTime/JordConv.lean`: `PositiveGeometryEmergentSpaceTime.JordConv.der_smul_eq_zero_iff`, `PositiveGeometryEmergentSpaceTime.JordConv.stab_smul_eq`, `PositiveGeometryEmergentSpaceTime.JordConv.idem_scale_iff` — stabiliser of a nonzero rescaled element equals the original; idempotency is scale-sensitive only by the explicit factor. Build LEAN_NUM_THREADS=1, anon-RSS cap 8 GB (peak 687 MB). AxiomsAll: theorems=1167 defs=633 nonstandard=0 sorry_dependent=0.

## Controls
- Planted: PL1 (CB, λ=3, λ=−1/2) and PL2 all OK. PL1 is partly structural (locked `stab_vecs` primitivises via intvec), disclosed in prereg.
- Broken: BR1–BR3 all rejected.
- Rival (projective test on the mixed list): passes, i.e. the flag failure is normalisation, not structure.
- **Null — deviation:** the code drew one λ per coordinate rather than one per representative as preregistered, so 0/200 pass / 0/200 unchanged measures a non-equivalence perturbation. Not verdict-bearing. Post-hoc debug only (not scored): uniform scaling E1×2, E1×(−1/2), P23×3 leaves stab dims unchanged (36).

## Prior art / contamination
Trace-form normalisation of h3(O) idempotents is textbook (Jordan–von Neumann–Wigner; Baez 2002); no numeric target, digits masked; nothing to contaminate.

## Notes
The locked JORD-1 checker is **fragile** (verdict depends on representative scale); kept unedited, superseded by `sims/convcheck/jord1_conv.py`. Runtime 597.7 s CPU. Credit: proposal only, 0.
