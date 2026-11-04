# CONV-JORD-1 — convention-invariance re-check of JORD-1 (trace-form / unit-scale rescaling)

Written 2026-10-30. Authorisation: The author directly, AutoResearch, 2026-10-30 ("You unpause and run those three - @PositiveGeometryEmergentSpaceTime I approve it"): exactly three convention re-check rungs, this is 1/3. Rule: notes/AUTORESEARCH-METHOD.md *Convention-invariance check (2026-10-30)*. Run id CONV-JORD1-2026-10-30-r1. CPU only. Worktree <local path>

## 1. Target
JORD-1 (run JORD1-2026-10-28-r1, prereg 719e85d, review reviews/JORD-1-result-2026-10-28.md) was ILL-DEFINED because the locked F_A consistency flag `FA_all_idempotent` failed: the locked list gave E1–E3 at unit scale and P_ij at 2P scale, and `is_idempotent2` tests the 2P scale. Locked file sims/jord1/jord1_checker.py is NOT edited; this re-check SUPERSEDES its F_A consistency step.

## 2. Well-posedness gate: the equivalence (refinement 1)
Map φ_λ: v ↦ λv, λ ∈ Q∖{0}, applied uniformly to every idempotent representative. Physics-preserving because (PROVED, to be committed in lean/PositiveGeometryEmergentSpaceTime/JordConv.lean, 0 sorry, no native_decide):
- `PositiveGeometryEmergentSpaceTime.JordConv.der_smul_eq_zero_iff` / `stab_smul_eq`: a linear map (derivation D) kills λv iff it kills v ⇒ stab(φ_λ S) = stab(S).
- `PositiveGeometryEmergentSpaceTime.JordConv.idem_scale_iff`: for bilinear B and λ ≠ 0, B(λx,λx) = λ(λx) ⇔ B(x,x) = x ⇒ "P idempotent at unit scale" ≡ "2P passes the 2P-scale test".
The locked mixed list is not a single convention. Conventions scored: CA (all at 2P scale, locked is_idempotent2) and CB (all at unit scale, exact Fractions, C(v,v) = 2v with C the locked 2× Jordan table).

## 3. Hypothesis and pass/flip rule (fixed now)
H: the ILL-DEFINED verdict is a convention artefact. Recompute the locked `consistent` formula (not(NOT-POSITIVITY-CLOSED and SM hits) and all idempotent and k ≥ 1) in CA and in CB, with tier A, tier B and all 1326 F_A stabilisers re-run through the locked functions.
- FLIPPED if consistent in both CA and CB; new verdict = the locked non-ILL label "tierA / tierB label (/ NO-GO)". Tag FM-SPEC, reopen.
- CONVENTION-ROBUST if inconsistent in both (ILL-DEFINED stands).
- ILL-DEFINED (re-check) if CA and CB disagree, or any planted/broken gate fails.

## 4. Planted / broken / null / rival (no tuning)
- Planted: PL1 F_A stabiliser-dimension histogram identical under CA, CB, λ = 3 and λ = −1/2 (note: locked stab_vecs primitivises integer vectors via intvec, so PL1 is partly structural; the Lean lemma is the real proof); PL2 the locked mixed list reproduces exactly E1, E2, E3 failing.
- Broken (must be REJECTED by the idempotency test in both conventions): BR1 E1+2E2; BR2 P12(+e0) with its octonion coefficient doubled; BR3 E1−E2.
- Null: 200 random NON-uniform rescalings (each representative its own λ ∈ {±1, ±2, ±3, ±1/2}, seed 20261030): fraction passing the fixed-scale test (expected low ⇒ the test is scale-sensitive) and fraction with unchanged single stabiliser dims (expected 200/200).
- Rival (strong, scale-free): projective idempotency (x∘x ∈ span(x), x ≠ 0) on the locked mixed list; must agree with CA/CB.

## 5. Prior art, contamination, digit masking
Prior art: rescaling invariance of idempotents/Peirce decomposition in Jordan algebras is textbook (McCrimmon, *A Taste of Jordan Algebras*, 2004; the 2× product convention of Baez, Bull. AMS 39 (2002), arXiv:math/0105155 — verified on arXiv). No new physics claim is made. Contamination: I (AutoResearch) wrote JORD-1 and the post-hoc diag (sims/jord1/posthoc_diag_out.txt already shows 2E_i passes), so the expected outcome is known; this rung is a formal superseding record, declared foregone. Digit masking: no numerical target; outputs are booleans and integer histograms compared to the locked live_out.json.

## 6. Lock
`jord1_conv.py` sha256 `d1c8f24be21750591537c7a821fb4609672a6769afa895da8b72bbc702835066`
`conv_guard.py` sha256 `1a80238b736516ca3a507af5281a7a556923b9ce8fb3df64d88aeef131074cc8`
Guard: guard inside every scoring/live function; re-reads this file, re-hashes both files and re-checks prereg-commit ancestry of origin/main on EVERY call; no pass flag. Import test and CLI must refuse before this prereg is pushed.
Lean: build with LEAN_NUM_THREADS=1, anon-RSS watchdog 8 GB; fresh AxiomsAll via a temp file; commit lean/AxiomsAll_output.txt.
Credit: proposal only (expected 0).
