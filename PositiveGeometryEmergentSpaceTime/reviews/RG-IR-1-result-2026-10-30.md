# RG-IR-1 result (2026-10-30): one-loop SM top-Yukawa quasi-fixed point vs UV memory

Failure-mode: FM-FREE (the QFP narrows the UV prior but does not select y_t; the low-energy window is set by the declared lower end of the UV prior)
Authority: author approved (2026-10-30). Prereg v1 `prereg/RG-IR-1-top-yukawa-uv-memory-2026-10-30.md` (e9a8b94, pushed alone with refusals bdbf04d); v1 planted P3 failed (design error), superseded by v2 `prereg/RG-IR-1-v2-supersede-P3-2026-10-30.md` (bf3c12b, refusals b2a1c24) with verdict rule verbatim. Checker `sims/rgir1/rgir1_checker_v2.py`; outputs `sims/rgir1/rgir1_v2_{planted,broken,live}.json`.

## Outcome: **PARTIAL (QFP-NARROWING)** → ledger tag NO-GO for "y_t removed as an input"
- SIMULATED: S = 0.0768, A = 0.591; y_t(M_Pl) ∈ [1, √4π] ↦ y_t(M_Z) ∈ [1.224, 1.294], W = 0.056 (threshold PASS ≤ 0.02, PARTIAL ≤ 0.2). Box 27/27 PARTIAL (W 0.054–0.058). Closed form vs RK4 agree to 1e-13.
- SIMULATED, report-only: GUT range W = 0.076; prior [0.5, √4π] W = 0.204; [0.1, √4π] W = 1.15 (FM-FREE: the answer is the prior).
- Rivals: QCD-only (Pendleton–Ross) W = 0.075; Yukawa-only no gauge W = 0.166; no running W = 1.12. SM/no-gauge ratio 0.34.
- Null (2000 random one-loop flows, seed 20261030): PASS 13.8%, PARTIAL-or-better 96.2% ⇒ narrowing is generic, not SM-specific (FM-QNBLIND-adjacent).
- CONTAMINATED, report-only: the memorised MS-bar y_t(M_Z) ≈ 0.94–0.99 lies **below** the window; the one-loop SM QFP over-shoots (folklore, consistent with hep-ph/9603432's review). Not a gate.
- Convention screening: E1 GUT normalisation of g1 and E2 ln μ² give identical W (CONVENTION-ROBUST).

## Lean (PROVED, 0 sorry, no native_decide; standard axioms only)
`PositiveGeometryEmergentSpaceTime.RgIr1.u_flow_affine`, `qcd_ratio_fixed`, `qcd_sensitivity_exponent`, `exp_ratio_invariant`, `affine_width`, `affine_contracts`, `sm_exponent_signs`. LEAN_NUM_THREADS=1, anon-RSS watchdog 8 GB (peak 0.66 GB). AxiomsAll 1179 thm / 634 defs / 0 nonstandard / 0 sorry-dependent. Algebra is elementary (FM-TAUT-level Lean, honest: it certifies the affine structure, not a physics claim).

## Controls
Planted v2 P1–P4 + gate self-tests ALL OK; broken B1 (b3 = +7 → Landau pole, ILL-DEFINED), B2 (α_s < 0), B3 (reversed prior) all rejected. v1 planted P3 FAILED (no-gauge W = 0.166 is PARTIAL, not FAIL); live not run under v1.

## Deviations
1. v1 P3 expectation wrong (Yukawa IR triviality narrows on its own). 2. v1 P4 computed the SM W (0.0560) inside the planted suite, so the live number was seen before the v2 lock; disclosed, v2 changed no threshold, prior, input or seed.

## Prior art / contamination
CITED: Lanzagorta–Ross hep-ph/9501394; Froggatt hep-ph/9603432; Shaposhnikov–Wetterich 0912.0208; Eichhorn–Held 1707.01107; Luo–Wang–Xiao hep-ph/0211440; Pendleton–Ross 1981, Hill 1981 (not on arXiv). Inputs and beta coefficients memorised (MEMORISED-INPUT). No novelty claimed for the closed form. Credit: proposal 0.
