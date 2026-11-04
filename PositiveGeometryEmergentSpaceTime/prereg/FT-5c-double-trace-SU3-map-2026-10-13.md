# FT-5c prereg — completing the O(p^4) zero map: double-trace operators and the SU(3) LEC map (2026-10-13)
Committed before any FT-5c computation.

## Gate (well-posedness, decided before computing)
In the U(3) quark-line basis used by FT-2/5a/5b, a tree with one insertion of a double-trace operator
(L1, L2, L4, L6, L7 type) has a double-trace flavour structure and therefore does not enter the single-trace ordered
amplitudes whose hidden zeros we test. So the double-trace part of the map is structural (decoupled), not computed.
(Standard flavour-structure counting; stated as an argument, not simulated.) The non-trivial remaining task is the
Nf = 3 map: Cayley–Hamilton makes O_L0 a combination of the standard L1, L2, L3 operators.

## Computation (sims/ft5/ft5c_ch.py)
With A_μ = U†∂_μU (traceless, anti-Hermitian 3×3): O_L0 → tr(A_μA_νA_μA_ν), O_B (= L3 operator) → tr(A_μA_μA_νA_ν),
O_1 (L1 op) → tr(A_μA_μ)², O_2 (L2 op) → tr(A_μA_ν)tr(A_μA_ν) (sign conventions as derived in the script).
Least-squares fit tr(AμAνAμAν) = a·tr(AμAμAνAν) + b·tr(AμAμ)² + c·tr(AμAν)² over ≥ 40 random samples (4 random
traceless anti-Hermitian matrices each, Euclidean contraction), then rationalise. Control: for 4×4 (Nf = 4) the
same fit must NOT be exact (no Cayley–Hamilton reduction at quartic order for N ≥ 4).

## Zero map output
FT-5a/5b selection (single-trace): coefficient of O_B = 0, single-trace L5 = L8 = 0, L0 free. With the Nf = 3 map
this gives L1 = b·L0, L2 = c·L0, L3 = a·L0 + (double-trace-free) and, if double-trace coefficients vanish
(large-Nc assumption, stated), ratios L2/L1 = c/b, L3/L1 = a/b, L4 = L6 = 0, L5 = L8 = 0.

## Verdicts (exhaustive)
- PASS: Nf=3 fit exact (max residual < 1e-10) with rational (a,b,c), Nf=4 control not exact (residual > 1e-3).
- PARTIAL: Nf=3 exact but control also exact, or coefficients not cleanly rational.
- FAIL: Nf=3 fit not exact.
- otherwise → UNCLASSIFIED.
Contamination: I recall the standard L0 elimination at Nf=3 and phenomenological L_i signs/sizes; the fit is computed,
not copied. No LEC data compared here (that is LEC-1, separate cell-level prereg). Credit: proposal only.
