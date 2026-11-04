# SURF-1′ convention-invariance re-check (2026-10-30)

Authority: author approved (2026-10-30). Prereg `prereg/CONV-SURF-1-coupling-norm-2026-10-30.md`, pushed alone as 422faf1 before any checker ran (refusals: `sims/convcheck/guard_refusal_surf1.txt`). Checker `sims/convcheck/surf1_conv.py` (imports locked surf1_checker read-only).

## Outcome: **CONVENTION-ROBUST** — EMPTY / NO-GO stands (FM-RANGE unchanged)
Equivalence: every trivalent vertex × λ (λ≠0), every propagator × μ (μ>0); covers coupling sign/normalisation vs tree term, T_F 1/2 vs 1, d-vertex in the f/d basis. All 38 K ratios have ΔV3 = 2 (even). On the 18-point grid λ∈{±1,±2,±1/2}, μ∈{1/2,1,2}: validator accepted, every per-K sign profile identical, label EMPTY everywhere; locked all_K(scale=2) also EMPTY. Matches locked VERDICT EMPTY.

## Lean (PROVED, 0 sorry, no native_decide)
`PositiveGeometryEmergentSpaceTime.SurfConv.even_pow_pos`, `PositiveGeometryEmergentSpaceTime.SurfConv.pos_iff_scaled` (0 < λ^(2k) μ^m x ↔ 0 < x), `PositiveGeometryEmergentSpaceTime.SurfConv.ratio_pos_iff`. Build LEAN_NUM_THREADS=1, 8 GB anon-RSS cap (peak 706 MB). AxiomsAll: theorems=1170 defs=633 nonstandard=0 sorry_dependent=0.

## Controls
- Broken: numerator-only −1 on n3:triangle and on n2:bubble — both REJECTED by the validator.
- Null: 200 random per-K numerator sign flips changed the label 0/200. Disclosure: this null does not demonstrate label sign-sensitivity (an EMPTY intersection of 38 positivity sets survives random flips with high probability); non-vacuity is shown instead by the rivals.
- Rival (different theories, not equivalences): ghost c=−1 → RANGE INCLUDES-3; c=0 → RANGE INCLUDES-3. The label does move under non-equivalent changes.

## Prior art / contamination
Standard birdtrack/T_F rescaling (Cvitanović 2008; Peskin–Schroeder). Foregone by the parity argument; declared in prereg. No numeric target. Credit: proposal 0.
