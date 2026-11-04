# LEAN-CERT-2 convention-invariance re-check (2026-10-30)

Authority: author approved (2026-10-30). Prereg `prereg/CONV-LEAN-CERT-2-canonical-class-2026-10-30.md`, pushed alone as 3131dd6 before any checker ran (refusals: `sims/convcheck/guard_refusal_leancert2.txt`). Checker `sims/convcheck/leancert2_conv.py`.

## Outcome: **FLIPPED** (FM-SPEC; reopen) — Python verdict ILL-DEFINED → **CERTS-OK**
The locked N2 null failed (131/480) because every accepted corruption edited P in a zero row of M, which leaves P·M (and validity) unchanged. Under the proved class equivalence, N2′ = **0/480** class changes. All other locked conditions already held (planted PL1–PL3 OK, B1/B2 rejected, all 8 certified dims = SIMULATED, rivals agree, N1 0/160), so the Python verdict becomes CERTS-OK. Lean verdict stays **PARTIAL-LIMIT** (k=2,3 not proved), not re-scored.

**Deviation (declared in prereg):** the screened equivalence named "Hermite/Smith normal form"; the class key used is (K, PM, Q, d), the minimal invariant the equivalence needs.

## Lean (PROVED, 0 sorry, no native_decide)
`PositiveGeometryEmergentSpaceTime.LeanCertConv.split_iff_of_PM_eq`, `PositiveGeometryEmergentSpaceTime.LeanCertConv.valid_iff_of_PM_eq` (def `PositiveGeometryEmergentSpaceTime.LeanCertConv.Valid`). Build LEAN_NUM_THREADS=1, 8 GB anon-RSS cap (peak 666 MB). AxiomsAll: theorems=1172 defs=634 nonstandard=0 sorry_dependent=0.

## Controls
- Planted: PL1 zero-row P edit valid + same key (all 8 certs); PL2 K edit changes key; PL3 replay reproduces 131 accepted. OK.
- Broken: raw-P key reproduces the locked 131/480. OK.
- Null: N2′ 0/480.
- Rival: zero-row canonicalisation key 0/480 — agrees.

## Prior art / contamination
Non-uniqueness of left inverses modulo a kernel is standard (Storjohann 2000). Foregone from diag_n2 (declared). No numeric target. Credit: proposal 0 (method rung; a CERTS-OK Python verdict may merit PositiveGeometryEmergentSpaceTime's review for the method line).
