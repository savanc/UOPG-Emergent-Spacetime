# HG-DIM-1 addendum: mean-curvature formula proved (2026-10-31)

Grok, the author ("Can you see if we can prove the mean-curvature formula."). Addendum file; the locked
review reviews/HG-DIM-1-result-2026-10-31.md (0026ed3), prereg bbfe77b and checker 198b0d4 are unchanged.
Proof: notes/HG-DIM-1-mean-curvature-proof-2026-10-31.md. Alignment: notes/HG-DIM-1-MEAN-alignment.md.

## Tag changes
| Statement | Was (0026ed3) | Now |
|---|---|---|
| Per-edge κ = (2 − p)/(D + 1), D = n − 3 | SIMULATED n ≤ 11 (HGDIM1-LIVE-20261031T090819); general n CONJECTURE | PAPER-PROVED all n ≥ 4 (explicit coupling for the upper bound; 1-Lipschitz potential φ = Σ w over diagonals, w = 1 on d and the T-flips f* of the diagonal sides of Q, for the lower bound; no duality theorem used) |
| mean κ(K_n) = (10 − n)/((n − 2)(2n − 5)) | CONJECTURE (post-hoc fit) | PAPER-PROVED all n ≥ 4; Lean PROVED: general algebra (`catalan_succ_ratio`, `sumP_closed`, `mean_kappa_closed`, `tri_weight`, `ear_relation`) + kernel-decide instances n = 5..9 of Σ_d p = 2n − 12 + 2e(T), Σ e = nC_{n−3}, Σp = (2n−12)C_{n−2} + 2nC_{n−3}; SIMULATED n ≤ 16 (HGDIM1-MEAN-20261031T093754) |

Key identity: Σ_{d∈T} p(T, d) = 2n − 12 + 2e(T) (ears e), and Σ_T e(T) = nC_{n−3}, giving E[p] = 5(n − 4)/(2n − 5).
Out-of-sample predictions n = 12, 13 of the 0026ed3 review (−1/95, −1/77) confirmed by exact counting (SIMULATED).

Not formalised: general-n Theorem 1, Lemma 2, Lemma 3 (paper only). Verdict LOCAL-COUNT and blocker tag NO-GO / FM-MODEL
unchanged: the mean curvature is a closed-form combinatorial count (ear statistics), which strengthens the LOCAL-COUNT reading.
No hand adjudication; no locked file edited. Credit 0.
