# BR-5′ prereg: Lean Feynman-rule construction of EWZ1b.N (2026-10-14), pushed alone before any Lean/sympy
Approval: author approved (2026-10-14).
Target: audit item A-4 (LEAN-AUDIT-2026-10-13), for EWZ1b.N only. FT5aL `T_*` and the MassiveZero G¹ literals stay open.
## Construction (new module lean/PositiveGeometryEmergentSpaceTime/BR5p.lean; EWZ1b files imported, never edited)
Transcribe the Feynman rules of sims/ewz1b/ewz1b.py into Lean over ℚ with abstract invariants:
- **Vector type:** coefficients on the basis {p1,p2,p3,e1..e4} plus a 5th (Higgs-direction) component.
- **Gram (dot4):** pᵢ·pⱼ in terms of k1..k3, s, t; eᵢ·eⱼ = eeij; eᵢ·pⱼ = eipj; eᵢ·pᵢ = eᵢ·eᵢ = 0; e4·p3 = −e4p1 − e4p2.
- **Vertices:**
  - VVV (lam3) and VVS (a) in the current J (three-term cyclic V3);
  - VSS (gs), which drops out for external W;
  - VVVV contact lam4·[2(13)(24) − (12)(34) − (14)(23)].
- **Currents and amplitude:**
  - s-channel J(1,2)·J(3,4) and t-channel J(2,3)·J(4,1), with 4D part − (5th·5th);
  - N_built = n_s(T − M_t²) + n_t(s − M_s²) + contact·(s − M_s²)(T − M_t²);
  - on the hidden-zero locus: ee13 = e1p3 = e3p1 = 0, with t eliminated via u − m1² − m3² = 2k1k3.
## Claim
`theorem built_eq_N : N_built … = PositiveGeometryEmergentSpaceTime.EWZ1b.N …` by `unfold`/`simp`/`ring` (any closing tactic; no hypotheses).
## Verdicts (exhaustive)
- **PASS:** unconditional equality proved; witness lemma; checklist plus #lint clean; alignment ALIGNED. A-4 is closed for EWZ1b.N (SIMULATED → PROVED link).
- **PARTIAL:** equality holds only under extra hypotheses, or only up to a coupling-independent term or overall sign/normalisation.
- **FAIL:** a Lean-proved discrepancy (a nonzero difference at an explicit point). EWZ1b.N would then be mis-generated, and EW-Z1b results get flagged (EW-Z1 files are not edited; flag to the author).
- **Otherwise:** UNCLASSIFIED.
## Caveat registered in advance
Lean checks that the polynomial follows from the transcribed rules. It does not check that the rules are CGW's 5D-YM reduction (a physics transcription, which stays CITED).
## Credit
Proposed 0 (self-audit of own pipeline).
