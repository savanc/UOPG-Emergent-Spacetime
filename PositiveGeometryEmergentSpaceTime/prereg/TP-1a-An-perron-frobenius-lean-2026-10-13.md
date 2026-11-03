# TP-1a prereg: Lean proof of the A_n Perron–Frobenius eigenvector (Coxeter bridge, first brick) — 2026-10-13

Status: PRE-REGISTERED before any computation or Lean work (AutoResearch). **Data cells: none.**

## Claim to formalise
For n ≥ 1 and the path-graph (A_n Dynkin) adjacency A (A_{k,k±1} = 1), set θ = π/(n+1) and x_k = sin(kθ), k = 1…n.
- (a) Each x_k > 0.
- (b) (A x)_k = 2cos θ · x_k for all k, including the ends, because x₀ = x_{n+1} = 0.
- (c) The eigenvalue is 2cos(π/h) with Coxeter number h = n+1, matching SG-1 G1 numerics for A1–A8.
- (d) Ratios x_k/x₁ = sin(kθ)/sin θ (quantum integers at q = e^{iθ}). For n = 4 this gives x₂/x₁ = 2cos(π/5) = φ, the golden ratio, linked to SG1 `two_cos_pi_div_five`.

Prior art: classical (Dorey; Kostant) *(memory)*. Possibly already in Mathlib in some form; I will search Mathlib first and credit it if found. New here: only our formal link to SG-1.

## Verdicts (exhaustive)
- **PASS:** (a)–(d) proved in Lean with 0 sorry and standard axioms only, and a numeric cross-check script agrees with SG-1 (A1–A8).
- **PARTIAL:** (a)–(c) proved, (d) not.
- **FAIL:** (b) not proved within the session.
- **Otherwise → UNCLASSIFIED** (closest category and why).

Credit 0 (structural; no observable). Proposed only.
