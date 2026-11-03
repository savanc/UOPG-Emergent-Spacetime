# Trade space 2026-10-22b — supersede note for notes/TRADE-SPACE-2026-10-22.md (Grok, 2026-10-22)
The original note is left unchanged. This note supersedes only the items listed.

## P1 Integrality — "Risk" paragraph (original §B, P1)
- Original wording: "Every integer invariant of a polytope (face numbers, normalised volume, Euler characteristic, Ehrhart data) is constant on the open chamber of offsets".
- **Correction (INT-1, SIMULATED INT1-2026-10-22-r1):** this holds for the combinatorial class I_comb (labelled face lattice, f-vector, Euler characteristic). It does **not** hold for normalised volume, which is a continuous polynomial in c′, or for Ehrhart/lattice-point data. Lattice-point counts took 28 distinct values on the positive chamber and are constant only on the finer lattice cells.
- The conclusion is unchanged: an integer cannot select an offset. I_comb is chamber-constant (PROVED n=5 `PositiveGeometryEmergentSpaceTime.IntChamber.invariant_chamber_constant`; SIMULATED n=6). I_lat needs an imported lattice.
- **P1 status: CLOSED (NO-GO) for the associahedron class.** μ = c13′/c14′ is free in (0,∞) and dense (`ratio_free`, `lattice_ratio`). Reopen triggers are in reviews/INT-1-result-2026-10-22.md.

## Rung table (original lines 128–129)
- R-A / INT-1: PROPOSED → **DONE (PASS, CHAMBER-CONSTANT; P1 NO-GO)**, prereg 32cec63, the author-directed 2026-10-22.
- R-B / FL-1Z: PROPOSED → see the FL-1Z result (this run).
