# CONV-SURF-1′ — convention-invariance re-check of SURF-1′ (coupling / T_F / f-d normalisation)

Written 2026-10-30. Authorisation: The author directly, AutoResearch, 2026-10-30: exactly three convention re-check rungs, this is 2/3. Rule: notes/AUTORESEARCH-METHOD.md *Convention-invariance check (2026-10-30)*. Run id CONV-SURF1-2026-10-30-r1. CPU only. Worktree <local path>

## 1. Target
SURF-1′ (run SURF1-2026-10-28-r1, locked sims/surf1/surf1_checker.py, verdict EMPTY, tag NO-GO, FM-RANGE). Screened eligible for: T_F 1/2 vs 1, f/d vs trace basis, sign relative to the tree term. The locked checker is NOT edited; this re-check supersedes nothing unless the verdict flips.

## 2. Well-posedness gate: the equivalence
Graph-uniform rescaling: every trivalent vertex × λ (λ ∈ Q∖{0}), every propagator / colour contraction × μ (μ > 0). Every interference ratio K = W(num)/W(den) is multiplied by λ^{ΔV3} μ^{ΔE}. Covers coupling sign/normalisation relative to the tree term (λ), T_F 1/2 vs 1 (μ; ΔE can be odd, e.g. triangle, but μ > 0), and the d-vertex in the f/d basis (positive rescale). The f-coupling is a different theory, NOT an equivalence (treated as rival in the locked run). Physics-preserving because, in a cubic theory, ΔV3 = 2L is even (checked per K by the checker), and (PROVED, lean/PositiveGeometryEmergentSpaceTime/SurfConv.lean, 0 sorry, no native_decide): `PositiveGeometryEmergentSpaceTime.SurfConv.even_pow_pos`, `PositiveGeometryEmergentSpaceTime.SurfConv.pos_iff_scaled` (0 < λ^(2k) μ^m x ↔ 0 < x for λ ≠ 0, μ > 0), `PositiveGeometryEmergentSpaceTime.SurfConv.ratio_pos_iff`.

## 3. Hypothesis and rule (fixed now)
H: the EMPTY verdict is convention-robust. Grid λ ∈ {±1, ±2, ±1/2}, μ ∈ {1/2, 1, 2} (18 points). For each: equivalence validator accepts, every per-K sign profile (pos set up to bound, tail sign, den_ok) identical to baseline, locked classify label identical.
- CONVENTION-ROBUST if all 18 grid points agree, ΔV3 even for every K, broken rejected, and label = locked VERDICT (EMPTY).
- FLIPPED if gates pass but the label differs from the locked verdict (tag FM-SPEC, reopen).
- GATE-FAIL (re-check void) if any gate fails.

## 4. Planted / broken / null / rival
- Planted: the 18-point grid above; plus locked all_K(scale=2) label must match.
- Broken: a per-K numerator-only factor −1 (on n3:triangle, separately on n2:bubble) presented as a "convention": the validator must REJECT both.
- Null: 200 random per-K sign flips of numerators (seed 20261030): fraction changing the label (reported; shows the label is sign-sensitive, so robustness is not vacuous).
- Rival (not equivalences, different theories): ghost coefficient c = −1 and c = 0; labels reported only.

## 5. Prior art, contamination, digit masking
Prior art: rescaling invariance of colour factors is standard (Cvitanović, *Group Theory*, 2008, birdtracks; T_F conventions, Peskin–Schroeder §15–16). Contamination: I (AutoResearch) wrote SURF-1′; the algebraic argument above makes the outcome foreseeable; declared foregone. Digit masking: no numerical target; outputs are labels and integer sets compared to locked live_out.json.

## 6. Lock
`surf1_conv.py` sha256 `f3d01cb280b2871ba50e4b2b76914cfada1aca7e38037f1601c05be81c4d1e73`
`conv_guard.py` sha256 `1a80238b736516ca3a507af5281a7a556923b9ce8fb3df64d88aeef131074cc8`
Guard as in CONV-JORD-1 (re-hash + ancestry on every call, no pass flag). Import test and CLI must refuse before this prereg is pushed.
Lean: LEAN_NUM_THREADS=1, anon-RSS watchdog 8 GB; fresh AxiomsAll; commit lean/AxiomsAll_output.txt. Credit: proposal only (expected 0).
