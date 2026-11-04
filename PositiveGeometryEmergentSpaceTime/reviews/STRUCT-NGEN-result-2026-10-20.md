# STRUCT-NGEN sharpen result (2026-10-20, Grok; continuous-mode own pick (author approved 2026-10-20))
**Verdict: NOT-FORCED (SM, consistency only) — NO-GO; RIVAL-SINGLES-OUT-3.** Foregone and declared. Credit 0 (proposal). Prereg b3f0202 (pushed alone); live run.

## Question
STRUCT-3 gave N_gen ∈ {3,4,5} (AF upper bounds + KM lower bound). Does any declared genuine theory-consistency condition force N_gen = 3, once experimental inputs are separated out?

## Declared trials and results (sims/ngen/ngen_output.txt; N = 1…20)
| Content | Core (K) | +D1 Banks–Zaks | +C1 triality Z₉ | +C2 Spin-Z₄ Z₁₆ |
|---|---|---|---|---|
| SM | {1,…,5} NOT-3 | {1,…,4} | **{3} CONDITIONAL-3** | ∅ (needs νᶜ) |
| SM+νᶜ | {1,…,5} | {1,…,4} | **{3} CONDITIONAL-3** | {1,…,5} |
| Rival 3-3-1 | **{3} RIVAL-SINGLES-OUT-3** | ∅ (n_f = 9 ⇒ b₁ < 0) | n/a | n/a |
Report-only E: SM + KM CP ⇒ {3,4,5} (STRUCT-3 recovered). 3 of 10 evaluated trials hit {3}; none is an unconditional SM-consistency set.
Planted all OK (STRUCT-3 window, b₀(SU2)(3) = 19/6, AF(SU3) max 8, triality residue −3/gen, 331 anomaly at N = 3, 6 not 2, b₁(n_f = 6) = 26). Broken "SM consistency set forces 3" REJECTED.

## Lean `PositiveGeometryEmergentSpaceTime.STRUCTNGen` (12 theorems + 3 defs; 0 sorry; no native_decide; #lint clean; standard axioms; no FRONTIER-AXIOM)
`sm_core_window`, `sm_core_not_forced`, `bz_two_loop_iff`, `triality_sum`, `triality_iff`, `triality_window`, `triality_su3_only_not_forced`, `z16_no_nuc_iff`, `z16_no_nuc_window_empty`, `rival331_anomaly_iff`, `rival331_window`, bundle `structngen_summary`.

## Reading
- Strict SM consistency (all anomalies, incl. Witten, Wang–Wen–Witten and Dai–Freed) is N_gen-blind; AF supplies only upper bounds. The lower bound ≥ 3 is empirical (CP violation), as are N_ν ≈ 3 (LEP) and the exclusion of a sequential 4th generation (Higgs/EW data) — CITED, not forcing.
- The only routes to exactly 3: (i) gauging baryon triality (García-Etxebarria–Montero 1808.00009, Z₉ anomaly ⇒ 3 | N) plus AF of SU(2) — conditional on an extra symmetry whose gauging is motivated by proton stability, i.e. phenomenology; with AF of SU(3) alone it allows 6; (ii) the non-SM 3-3-1 gauge group, where SU(3)_L anomaly cancellation ties N_gen to N_c. The same type of condition singles out 3 more cleanly for a non-SM group, so it is not evidence for SM structure.
- Mission: N_gen = 3 is not fixed by SM consistency; a forcing would need either a consistency reason to gauge triality, or an embedding of the SM into 3-3-1-like structure from geometry/consistency.

## Caveats
One Higgs doublet; one-loop AF (two-loop only as D1); νᶜ triality charge taken as 0; K7–K9 (unitarity, vacuum stability, U(1) Landau pole) need mass/coupling data and were declared blind/excluded, not evaluated. Not touched: CREDITS.md, EW-Z1 paths, R4Indep blueprint block, XResearch; trade-space figure and Lean naming map (deltas in notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-20.md).

## Reopen triggers
A consistency (not phenomenological) reason to gauge baryon triality or another Z_n with N_gen-dependent anomaly; a derivation of the gauge group that embeds the SM into 3-3-1-type structure; a strict-consistency lower bound N_gen ≥ 3.
