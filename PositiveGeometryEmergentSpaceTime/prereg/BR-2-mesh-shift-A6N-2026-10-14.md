# BR-2 prereg — mesh-compatible unequal shifts and A6N (2026-10-14)
DISCLOSURE: an exploratory sympy check (sims/br2/br2_check.py) was run BEFORE this prereg (process slip, logged as the
rung lesson). It showed that A6N is NOT invariant under a general pole-preserving spurion shift X_ij ↦ X_ij + ν_i + ν_j
(ν4 = −ν1, ν5 = −ν2, ν6 = −ν3). Hence this prereg is not blind; it fixes what will be proved and how it is graded.
Target (THEOREM-GRAPH BR-2 wording): "A6N invariant under any mesh-compatible unequal shift (generalising a6n_reparam)".
Lean plan: (a) `spurion_shift_mesh`: spurion shifts leave every mesh combination invariant (reuse FT2Mesh.mesh_shift_cancels);
(b) `a6n_reparam_is_spurion`: a6n_reparam is exactly the spurion shift with ν = (−l/2, l/2, −l/2, l/2, −l/2, l/2);
(c) `a6n_not_spurion_invariant`: explicit counterexample to general invariance (ν = (1,0,0)); (d) witness.
Verdicts (exhaustive): PASS = general invariance proved (now known false); PARTIAL = (a),(b),(c) proved, i.e. the bridge
identifies a6n_reparam as the unique (by MassShift.offsets_forced6) spurion direction; FAIL = (b) fails;
otherwise UNCLASSIFIED. Credit 0.
