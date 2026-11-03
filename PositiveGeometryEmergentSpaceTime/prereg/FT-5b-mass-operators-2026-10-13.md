# FT-5b prereg — single-trace O(p^4) mass operators (L5, L8 type) at unequal-mass hidden-zero loci (2026-10-13)
Committed before any FT-5b computation.

## Operators (U(3) quark-line, χ = M = diag(μ_u, μ_d, μ_s), real)
O_5 = tr(∂U ∂U† (χU† + Uχ†)),  O_8 = tr(χU†χU† + Uχ†Uχ†).
Positive controls (pure LO renormalisations, must keep zeros): O_kin = tr(∂U∂U†), O_mass = tr(M(U+U†)).

## Method (sims/ft5/ft5b.py)
Dual-number (ε) Berends–Giele with dual-valued Gram matrix. These operators have 2-point pieces, handled exactly:
inverse propagator K(p²) = p² − M0_ab + ε(α_ab p² + β_ab) (α, β extracted from the engine's 2-point vertex);
internal propagators resummed to O(ε); external legs on the corrected shell p² = M0 − ε(αM0+β) (dual Gram:
perturbation keeps row sums 0 and locus entries 0); LSZ factor Π √Z, Z = 1 − εα. T_op = ε-part of the amplitude.

## Validation (V), must all hold
V1: exp and Cayley parametrisations give identical T_op on-shell (field-redefinition invariance; tests LSZ).
V2: positive controls O_kin, O_mass give T = 0 on the loci (they only rescale F / shift μ).
V3: LO part reproduces ft2.amp.
Loci/chains/mass sets/points as in FT-5a (6-pt skinny and 2×2, null pair; 5 chains; equal (1,1,1), unequal (1,2,7); 2 points).

## Verdicts (exhaustive)
- PASS: V and T_5 = T_8 = 0 on both 6-pt loci, all chains, equal and unequal masses.
- PARTIAL: V and (exactly one of O_5, O_8, or a unique combination a O_5 + b O_8, keeps the zeros at all masses;
  or zeros kept only at equal masses).
- FAIL: V and no combination of O_5, O_8 keeps the zeros at equal masses.
- otherwise → UNCLASSIFIED (incl. any V failure).

## Contamination flag
I recall approximate phenomenological L5, L8 values (BE14/FLAG-type fits). They are NOT used here: no LEC numbers enter.
Any forced LEC relation would be compared to data only under a separate cell-level prereg, labelled CONTAMINATED.
Credit: proposal only; expected 0 (loci unphysical, FT-2 NO-GO).
