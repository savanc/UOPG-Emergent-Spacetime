# Trade space 2026-10-23: supersede note for notes/TRADE-SPACE-2026-10-22c.md (and through it 22 and 22b) (Grok, 2026-10-23)
The earlier notes are left unchanged. This note supersedes only the items below. Everything else in 22c and 22b still stands, including FL-1Z NOT-WELL-POSED, INT-1 CHAMBER-CONSTANT and the P1 correction. Both rungs below came from the lit review (notes/LIT-REVIEW-2026-10-22-cosmic-nine-loops-ai-physics.md) and were run on the author's go at on 2026-10-23, with LEAN-CERT-1 first and then CASCADE-1. NL9c was not run.

## R-B LEAN-CERT-1 (lit review 2026-10-22, lesson 4; BACKLOG "LEAN-CERT-1 (method)")
- **Status: DONE. Verdict UPGRADED** (reviews/LEAN-CERT-1-result-2026-10-23.md; run SIMULATED LEANCERT1-2026-10-23-r1; prereg 689d929, refusal 3fc8fc1, result 515084c). No kill fired: the module took 10.2 s and 6.8 GB.
- **No TS-1 entry.** This is a method rung with credit 0:
  - GRADED-POSITROID N_ACC = 2 moves SIMULATED → PROVED (`PositiveGeometryEmergentSpaceTime.LeanCert.nacc_eq_two`, `nacc_set_eq`, `acc_iff`).
  - ABHY 1711.09102 dim K_n = 5 / 9 / 14 is reproduced as PROVED for n = 5 / 6 / 7.
- **Method lesson:** integer split certificates (MK = 0, PM + KQ = d·1, QK = d·1) checked by `decide +kernel` through a once-proved soundness layer turn exact SIMULATED rank and kernel facts into PROVED ones in seconds, up to about 21×21. An extrapolated limit near N ≈ 200 is CONJECTURE. The path was reused unchanged by CASCADE-1 (`em4_cert`, `em5_cert`).
- **Revised feed:** the SIMULATED → PROVED backlog now has a cheap path for linear facts. Candidates are SIMULATED repo claims that are exact integer or rational rank or kernel statements. P1–P5 are unchanged.
- **New PROPOSED item (needs the author's go and a prereg):** LEAN-CERT-2, mod-p certificates with rational reconstruction on a matrix of at least 100×100 from an existing SIMULATED rung, with timing against the N^3.2 extrapolation. Cost: low. Prior that it completes under the 1 h kill: about 0.6 (CONJECTURE).

## R-B CASCADE-1 (lit review 2026-10-22; BACKLOG "CASCADE-1 (P4 method)")
- **Status: DONE. Overall verdict REFUTED-AS-STATED; locked python verdict FAIL (kill b), VOID-ON-AUDIT reading pending the author** (reviews/CASCADE-1-result-2026-10-23.md; run SIMULATED CASCADE1-2026-10-23-r1; prereg af1bb37, refusal 42608d9).
  - K_final against N_off: E0-4 0/2 BELOW, EM-4 4/2 ABOVE, E0-5 0/5 BELOW, EM-5 5/5 MATCH.
  - Hidden zeros ⇔ five linear relations μ_ab = c_ab(m) (PROVED `PositiveGeometryEmergentSpaceTime.Cascade1.em_n5_zero_iff`, both directions).
  - The EM-5 held-out splits failed 0/10 in the locked checker. The cause is a checker defect: the locus masses were not mapped to the final family. They pass 10/10 mass-consistently, with a control of 2/10 off the relations (SIMULATED post-hoc), and are PROVED `split5_of_rel_*`.
- **No TS-1 entry.** P4 at tree level, n ≤ 5, is NO-GO for ratio fixing:
  - every consistency stage is linear in (μ, m);
  - RATIOS-FREE holds in both EM cells (dims 4 and 5, PROVED via `em_n4_finrank` / `em_n5_finrank` plus the uniform interior point);
  - the E0 collapses come from hand-inserted massless legs (kill-(a) audit: not a positive surprise).
  - The only pure-mass output is the n = 4 linear sum rule m1 + m3 = m2 + m4 (PROVED `em_n4_zero_iff`), which fixes no ratio.
- **Lessons:**
  - (i) With INT-1 and FL-1Z the pattern becomes "linear consistency conditions tie parameters together but never fix a ratio; integers pick loci, not values" (CONJECTURE). A ratio fix needs a non-linear stage (string or δ-deformed zeros, loops) or an imported integrality.
  - (ii) Method: planted suites must include the massive or deformed version of every held-out test. PL2 was massless-only and missed the mass-mapping defect.
- **Revised P4 feed:** the hidden-zero cascade for Tr φ³ at n ≤ 5 is closed. Next P4 options are non-linear stages only. P1, P2, P3 and P5 are unchanged.
- **New PROPOSED items (need the author's go and a prereg):**
  - CASCADE-1b: a blind massive held-out split re-test with a fixed `split_test`, a planted massive-split case and the D3 control, on a new blind target (mass-shifted n = 6 or δ-deformed zeros). Cost: low–medium. Prior that splits pass: about 0.8 (CONJECTURE).
  - CASCADE-2: the same cascade with δ-deformed or string zeros (2312.16282 §7), testing whether a non-linear stage can drop K below N_off without hand input. Cost: medium. Prior of a ratio fix: about 0.05 (CONJECTURE).
