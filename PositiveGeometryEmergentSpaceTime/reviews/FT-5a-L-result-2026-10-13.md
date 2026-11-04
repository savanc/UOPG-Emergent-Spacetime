# FT-5a-L result — Lean proof of the 4-point L0 hidden-zero statement (2026-10-13)
Deviation disclosed: no separate prereg file; the target (prove FT-5a's 4-pt statement) was fixed by the author's instruction
and the FT-5a prereg. Contact formulas were derived symbolically first (sims/ft5/ft5aL_sym.py → output):
T_L0 = 4(p0·p2)(p1·p3), T_B = 2(p0·p1)(p2·p3) + 2(p0·p3)(p1·p2). These match the FT-5a numerics (T_L0 zero, T_B not).
Lean (lean/PositiveGeometryEmergentSpaceTime/FT5aL.lean, 0 sorry): `L0_zero` (any masses), `B_not_zero` (massless conserved witness),
`B_not_zero_massive` (unequal masses witness), `only_L0` (in span{T_L0,T_B}, vanishing on the locus forces b = 0).
Verdict: **PASS** (4-pt statement proved, given the derived contact formula; the derivation itself is SIMULATED/symbolic,
not formalised). Note: at 4 pt the zero is the trivial factor p0·p2 of T_L0, so the 6-pt result (FT-5a) remains the non-trivial one.
Proposed credit: 0.
