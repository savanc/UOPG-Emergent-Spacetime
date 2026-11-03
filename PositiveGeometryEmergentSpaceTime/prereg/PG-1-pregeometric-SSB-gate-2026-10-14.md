# PG-1 prereg — pre-geometric SSB scale gate (2026-10-14), committed before Lean work
Source of the physics inputs: notes/PLANCK-BH-SURVEY-2026-10-13.md (V7; Meluccio–Pluzhnikov 2610.11357, verified there).
Gate: (a) Lean: the SSB orientation data ⟨φ⟩ = v·e (any linear group action, e.g. SO(1,3) on ℝ⁴) has stabiliser
independent of v ≠ 0 and is ScaleBlind (instance of BR4.stabilizer_blind / no_scale with σ = v, k = 1);
(b) input ledger of dimensionful inputs as listed in the survey note (m, v, k, plus the unspecified potential).
Verdicts (exhaustive): PASS = some ratio (e.g. Λ/M_P²) is forced by the stabiliser data alone (not expected);
NO-GO (≡ FAIL for the scale question) = (a) proved and the ledger shows ≥1 free dimensionful input;
PARTIAL = (a) proved but ledger incomplete; otherwise UNCLASSIFIED. Credit 0.
