# BR-5 prereg — feasibility gate: derive EWZ1b.N (WW→WW numerator) from MassiveSpinor in Lean (2026-10-14)
Committed and pushed on its own before reading EWZ1b in detail or writing any Lean/scripts.
Constraint: EW-Z1 files are read-only (PositiveGeometryEmergentSpaceTime owns them); no edits, no new imports into EWZ1b.
Gate questions (answered by reading EWZ1b.lean, MassiveSpinor.lean and the EW-Z1b review only):
 G1 inputs: which objects does N take (polarisation dot products, k_i, couplings) and how were they produced (script)?
 G2 path: does MassiveSpinor provide massive polarisation vectors / helicity components needed to build those inputs?
 G3 cost: number of Feynman diagrams/terms and whether a Lean derivation fits in one session without new infrastructure
    (Lorentz-vector algebra on ℂ⁴, polarisation sums, gauge + Higgs exchange).
Verdicts (exhaustive): FEASIBLE = G1–G3 all positive with an estimated ≤ 1 session; FEASIBLE-LONG = G1, G2 positive,
G3 > 1 session; NOT-FEASIBLE = G2 negative (missing infrastructure); otherwise UNCLASSIFIED. No Lean proof attempted. Credit 0.
