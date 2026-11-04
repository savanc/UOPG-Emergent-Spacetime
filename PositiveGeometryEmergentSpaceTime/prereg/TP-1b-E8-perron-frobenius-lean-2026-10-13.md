# TP-1b prereg: E8 Perron–Frobenius eigenvector/eigenvalue in Lean — 2026-10-13

Status: PRE-REGISTERED before any computation (AutoResearch). **Data cells: none.**

## Plan
E8 graph as in SG-1: chain 0–1–2–3–4–5–6, branch node 7 attached to node 2. Write c for the eigenvalue. Running the recursion from node 6 (x₆ = 1) defines every x_i as a polynomial in c. The remaining node equation is a consistency polynomial P(c) = 0, to be derived by a committed sympy script.

## Targets
- (A) Lean: for any real c with P(c) = 0, the vector x(c) satisfies A x = c x, i.e. all 8 node equations (ring identities modulo P).
- (B) Lean: P has a root c* in an explicit rational interval of width ≤ 1e−6 containing 2cos(π/30) ≈ 1.98904379 (IVT plus norm_num sign checks). All x_i(c*) > 0 there, giving a strictly positive eigenvector.
- (C) Lean: c* = 2cos(π/30) exactly, i.e. P(2cos(π/30)) = 0 (e.g. via Chebyshev T₃₀ and factorisation).
- Numeric: the script checks P's roots, the bracket, and agreement with SG-1.

## Verdicts (exhaustive)
- **PASS:** (A), (B) and (C) proved (0 sorry, standard axioms only).
- **PARTIAL:** (A) and (B) proved, (C) not.
- **FAIL:** (A) not proved.
- **Otherwise → UNCLASSIFIED** (closest category and why).

Not claimed: uniqueness (PF theorem not formalised). Credit 0 (structural). Proposed only.
