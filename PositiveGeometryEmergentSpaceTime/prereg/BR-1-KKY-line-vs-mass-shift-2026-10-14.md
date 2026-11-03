# BR-1 prereg — UnequalLS (KKY dual zero line, credited KL-LAT) ↔ MassShift/NLSM δ-shift zero (2026-10-14)
Prior art: KKY 1969 (πK dual amplitude); CGW 2601.16860 (massive c13 = X13+X24−X14−X23 with on-shell boundary values;
uniform case only); our MassShift.mshift4_limit / mshift4_eq_neg_c13; FT-1 (`shifted_zero_line`, `chiral_match_iff`):
with free offsets μ1+μ2 the δ-shift line matches the chiral line only by fitting one input.
Question: is there an assignment of the δ-shift offsets that is fixed by on-shell data (not fitted) under which the
δ-shift 4-pt zero equals the KKY zero line s = mπ² + mK²?
Candidate (decided now, before Lean work): the unequal-mass generalisation of CGW's on-shell boundary prescription,
μ13 + μ24 = −(X14 + X23)|on-shell = −(m4² + m2²) for ordering (1234) with legs 2,4 = π,K.
Well-posedness/memory: no data; KKY line already credited (KL-LAT); FT-1 shows the δ-shift alone does not fix μ.
## Verdicts (exhaustive)
- PASS: Lean proves equivalence (limit value 0 ⇔ KKY dual-zero condition ⇔ s13 = mπ²+mK²) with μ fixed by on-shell
  boundary values AND the prescription is itself derived (not assumed) in Lean from an existing theorem.
- PARTIAL: equivalence proved, but the on-shell-boundary prescription for unequal masses is an assumption
  (CGW uniform case + FT-2 mesh cancellation as support, not a derivation).
- FAIL: no on-shell-fixed assignment gives the KKY line.
- otherwise → UNCLASSIFIED.
Credit: 0 (no new data; joins credited result to the chain only).
