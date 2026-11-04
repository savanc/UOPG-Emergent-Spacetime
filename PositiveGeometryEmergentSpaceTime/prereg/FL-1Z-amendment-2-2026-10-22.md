# PREREG AMENDMENT FL-1Z A2 (2026-10-22)
This amends prereg/FL-1Z-modular-fixed-point-2026-10-22.md and A1 (prereg/FL-1Z-amendment-1-2026-10-22.md, 7f9ccdd). Both stay immutable.

## r2 record (FL1Z-2026-10-22-r2), kept
- **Planted:** identical to r1. L1, L2 and L3 PASS; L4 FAIL (2.8e-7 < 1e-3). PLANTED FAIL stands. File: fl1z_planted_r2.txt.
- **Live:** completed in 5 s. **Defect:** the random-start Newton charged-lepton fit converged at only 27 rows out of 383 points. It converged at no D3, D5 or larger-|δ| D1 points, and at only 5 D4 rows.
  - Even on those 27 rows no observable was constant. The rel. spread of ρ was 3.9e4 and of s12² was 1.9, so the verdict was "NOT-WELL-POSED (confirmed)".
  - The coverage is too thin to grade D1 (ρ → 0 as |δ| → 0) or to report D3.
  - Files: fl1z_output_r2.txt, fl1z_live_r2.json, fl1z_live_stderr_r2.txt.
  - I looked at the r2 outputs before writing this amendment. This amendment changes only the root-finder seeding. No definition, scan, threshold, prediction or verdict rule changes.

## Change
- The charged-lepton Newton is now seeded first from the 30 best points of a deterministic 140×140 signed-log grid, |β|, |γ| ∈ [1e-2, 1e3]. The 40 seeded random starts follow.
- The Newton step now has a backtracking line search.
- The run id is FL1Z-2026-10-22-r3. The seeds are unchanged.

## Manifest
- `sims/fl1z/fl1z_checker.py` sha256 `ff5abb31b7c2ab5518cecd2fde7cb5c4fad63b3f2b2ec0023ea2af270f98a912`
- `sims/fl1z/import_guard_test.py` and `planted_cases.json` are unchanged.
