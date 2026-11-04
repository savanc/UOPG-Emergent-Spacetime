# GB-1a prereg: closed-string glueball ratios (PREDICTIONS, registered before any comparison) — 2026-10-13

Status: REGISTERED by AutoResearch. Nothing from the arXiv 2106.00364 tables (or any other SU(N) glueball table) has been opened. Script: `sims/gb1a/gb1a_predict.py` → `_output.txt`.

## Models (zero fitted parameters; unit √σ, the fundamental string tension)
- **A, Nambu–Goto closed string, light-cone, D = 4:** m² = 8πσ(N − (D−2)/24), level matching N = Ñ. The leading spin at level N is J = 2N (C = +, P = +). The intercept 1/12 comes from the transverse zero-point (Casimir) energy, a geometric fact of the string worldsheet, not a fit.
- **B, LS-anchored closed trajectory:** the open LS intercept α₀ = 1/2 is fixed by the Adler zero (our MR rungs). A closed string has slope α′/2 and intercept 2α₀ = 1, so m² = 4πσ(J − 1).

Prior art: Isgur–Paton flux tube; Nambu–Goto closed-string glueballs (Johnson–Teper, Athenodorou–Bringoltz–Teper) *(memory)*; pomeron/glueball trajectory (hep-ph/0008212, seen in a GB-1 snippet). Model A is standard. Model B's anchoring to the LS Adler intercept is ours (CONJECTURE).

## Registered predictions (continuum, any N ≥ 4; both models are N-independent at leading order)
| Quantity | A | B |
|---|---|---|
| m(2++)/√σ | 4.7998 | 3.5449 |
| m(4++)/√σ | 6.9405 | 6.1400 |
| m(6++)/√σ | 8.5618 | 7.9267 |
| m(4++)/m(2++) | 1.4460 (√(23/11)) | 1.7321 (√3) |
| m(6++)/m(2++) | 1.7838 (√(35/23)·√(23/11)) | 2.2361 (√5) |

Contamination: my GB-1 memory dump has m(2++)/√σ ≈ 4.7 at N = ∞. So the m(2++) rows are CONTAMINATED: A looks close and B looks off, and I know it. **Blind-eligible rows (by self-report only, soft-contaminated):** m(4++)/√σ, m(4++)/m(2++), m(6++) at N = 4…12.

## Scoring (applied later, by whoever opens the data, with the author's go)
For each N in {4, 6, 8, 10, 12} where a continuum 4++ spin assignment exists:
- PASS if |pred − lattice| ≤ max(2σ_lat, 5 %).
- PARTIAL if ≤ 10 %.
- FAIL otherwise.

Model verdict: PASS if ≥ 3/5 N values pass on m(4++)/m(2++). Kill: if A and B both FAIL on 4++/2++, the closed-string-ratio route for glueballs is REFUTED at leading order.

Well-posedness: both models produce only C = + even-J states on the leading trajectory. If lattice 4++ spins are flagged ambiguous for some N, that N is excluded beforehand by the paper's own spin labels.

Max credit: 0.5 per model if PASS (soft-blind cap from GB-1). Proposed only. **No comparison is made in this run** (instruction: never open the 2106.00364 tables). A future lattice spectrum dated after this prereg would be cleanly blind.
