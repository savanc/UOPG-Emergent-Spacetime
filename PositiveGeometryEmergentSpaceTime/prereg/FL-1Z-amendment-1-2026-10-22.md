# PREREG AMENDMENT FL-1Z A1 (2026-10-22)
This amends prereg/FL-1Z-modular-fixed-point-2026-10-22.md (99863fe, pushed in ccc7284), which stays immutable. Everything in it stands except the points below.

## What happened under r1 (FL1Z-2026-10-22-r1), kept as a negative/defect record
- **Planted (r1):** L1, L2 and L3 PASS. L4 **FAIL**: with the broken f (f + 0.1·I), min m1/m3 = 2.8e-7. The criterion was > 1e-3.
  - So the L4 threshold was mis-set: the broken-f m1 is suppressed by the charged-lepton hierarchy, but it is still 9 orders above the L3 maximum of 1.5e-16 and 3 orders above the 1e-10 L3 threshold.
  - **The r1 planted verdict PLANTED FAIL stands on record.** L4 is NOT re-thresholded. The review will report it as FAIL (threshold mis-set), with the observed separation.
  - File: sims/fl1z/fl1z_planted_r1.txt.
- **Live (r1):** crashed before producing any output. The charged-lepton Newton iterate ran away (overflow), and LinAlgError followed in eigvalsh at the first D1 point. No observable was printed. File: sims/fl1z/fl1z_live_r1_crash.txt.

## Change (robustness only; no definition, scan, threshold or prediction changes)
- `_res` now returns None (an invalid start, discarded) if an iterate is non-finite or |β| or |γ| > 1e6.
- The guard now points at this amendment file.
- The run id is FL1Z-2026-10-22-r2. The seeds are unchanged.
- r2 re-runs planted and live. The r2 planted L4 is expected to FAIL again, identically; the code path is unchanged.

## Manifest
- `sims/fl1z/fl1z_checker.py` sha256 `44b64bb511244ea82297fb9245cd25db0c8866b4ab391f6b9f4d27a27bd115ae`
- `sims/fl1z/import_guard_test.py` sha256 `d719ad1382a8595cb76d7fb9c97cd27a5d5f76c29e6027dc8fad8cd82cb67fd2` (unchanged)
- `sims/fl1z/planted_cases.json` unchanged.
