# FT-5a prereg — O(p^4) single-trace counterterm trees at unequal-mass 6-pt hidden-zero loci (2026-10-13)
Committed before any FT-5 computation. Gate: notes/FT-5-prior-art-gate-2026-10-13.md.

## Setup
Flavour-ordered U(3) quark-line amplitudes, LO L = ½tr(∂U∂U†)+tr(M(U+U†)) as in sims/ft2, plus ε_A·O_L0 + ε_B·O_B
(O_L0 = tr(∂μU∂νU†∂μU∂νU†), O_B = tr(∂μU∂μU†∂νU∂νU†)). Compute T_A, T_B = ∂A/∂ε at ε=0 (one insertion, trees,
dual numbers) with sims/ft5/ft5a.py. Engine validation: generic operator engine must reproduce ft2.amp exactly at LO,
and exp vs Cayley parametrisations must agree on-shell for T_A, T_B (on-shell field-redefinition invariance).
Loci (FT-2): 4-pt {p0·p2=0}; 6-pt skinny {(0,2),(0,3),(0,4)} and 2×2 {(0,3),(0,4),(1,3),(1,4)}; nulls {(0,3)}.
Chains: udsuds, uuddss, ududud, ususus, uuuuus; mass sets massless, equal (1,1,1), unequal (1,2,7); 2 rational points each.

## Control (C): massless, 6-pt: T_A = 0 on both loci and T_B ≠ 0 on at least one (2403.10594 statement).
## Verdicts (exhaustive)
- PASS: C holds AND T_A = 0 exactly on both 6-pt loci for all chains for equal AND unequal masses.
- PARTIAL: C holds AND T_A = 0 for equal masses on both loci but ≠ 0 for unequal masses on some locus/chain.
- FAIL: C holds AND T_A ≠ 0 at equal nonzero masses on some 6-pt locus.
- otherwise → UNCLASSIFIED (incl. control C fails, validation fails).
Secondary (reported, not part of verdict): whether any combination aT_A+bT_B other than (1,0) vanishes; 4-pt behaviour.
Credit: proposal only; expected 0 (no observable; FT-2 NO-GO).
