# Trade space 2026-10-22c: supersede note for notes/TRADE-SPACE-2026-10-22.md and notes/TRADE-SPACE-2026-10-22b.md (Grok, 2026-10-22)
Both earlier notes are left unchanged. This note supersedes only the items below. Everything else in 22b, including the INT-1 / P1 correction, still stands.

## R-B FL-1Z (original §R-B; ranking row "FL-1Z | P1+P5 | discreteness | PROPOSED | 0.05 …"; 22b line "R-B / FL-1Z: PROPOSED → see the FL-1Z result")
- **Status: DONE. Verdict NOT-WELL-POSED** (reviews/FL-1Z-result-2026-10-22.md; run SIMULATED FL1Z-2026-10-22-r3; prereg 99863fe plus amendments 7f9ccdd and 76f29be). The verdict was declared in prereg §0 and confirmed by the run; K1 was not triggered.
- **No TS-1 entry.** Of the original kill conditions, "needs a fitted coefficient" and "the result does not depend on the fixed point" both fire:
  - The exact point τ = ω is excluded, because m_ν is rank 1 there (PROVED `PositiveGeometryEmergentSpaceTime.FL1Z.D3_rank_one`; SIMULATED, reproducing 2502.12662 App. D).
  - ρ, the mixing angles and |m_ee|/m3 all vary with the free |τ − ω| and with b̃_k (SIMULATED r3).
  - The normal hierarchy with m1 = 0 is Zee–Babu-generic (PROVED `antisymm3_det_zero`). It is not a fixed-point output.
- **Discreteness lesson:** with INT-1 this makes the pattern "integers pick loci, not values" (CONJECTURE). The integer weights select τ ∈ {i, ω} (`valence_lt12`, under the declared hypothesis `hv`), but the observables live off the locus.
- **Revised P5 feed:** TS-1 is not fed from FL-1Z. P5 stays PARTLY DONE, and no new TS-1 entries were made.
- **New PROPOSED item (needs the author's go and a prereg):** FL-1Zb, a branch-tracked integer hierarchy exponent near τ = ω. Cost: low–medium. Prior: about 0.05.
