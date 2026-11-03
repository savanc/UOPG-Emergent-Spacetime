# PREREG RG-IR-1 v2: supersede the v1 checker after planted P3 failed (verdict rule unchanged)

Supersedes the checker locked in prereg/RG-IR-1-top-yukawa-uv-memory-2026-10-30.md (e9a8b94). v1 checker and its outputs are kept, not edited.

## 1. What failed
v1 planted run (sims/rgir1/rgir1_planted.json): P1, P2, P4 and all gate self-tests passed; **P3 failed**. P3 declared "no gauge couplings (c = 0) ⇒ FAIL (W > 0.2)". The checker returned W = 0.166 (PARTIAL band). This is a design error in the prereg, not a code bug: with c = 0, u = 1/y² still shifts by A0 = 2aL/(16π²) ≈ 2.24 over the Planck range, so the Yukawa's own IR triviality narrows the prior (u_UV ∈ [1/4π, 1] ↦ [A0 + 1/4π, A0 + 1]). Lesson: W mixes gauge QFP attraction with Yukawa IR triviality.
Per METHOD planted rule (stop, fix the pipeline, re-run planted before real data) the v1 live mode was **not** run.

## 2. Disclosure (contamination of this supersede)
v1 planted P4 computed W for the SM itself (W_sm = 0.0560) as part of the convention-equivalence check. So the live number was seen before this v2 lock. Therefore v2 changes **nothing** in the verdict rule, thresholds (0.02 / 0.2), UV prior, inputs, box, null or seed. The verdict will be read from the v2 live run under the v1 rule verbatim.

## 3. Changes (only these)
- P3 now: c = 0 must give S = 1 to 1e-12 and W equal to the analytic W(1, A0) to 1e-9 (recover a known answer).
- live adds report-only: rival "Yukawa-only, no gauge" and the ratio W_sm / W_nogauge (not verdict-bearing).
- PREREG path points to this file.

## 4. Lock
`rgir1_checker_v2.py` sha256 `a1e9d2d92ae471e6cb00d91d3099b5a04b6b7206c35838aa573631b79124a8f3`
`guard.py` sha256 `e1bff0e236144d7a8ae18d32f9241963c884a0ce7b46dfa5c7cc630b3a15345c`
Guard unchanged (re-read, re-hash, ancestry on every call, no pass flag). Import test (import_guard_test_v2.py) and CLI must refuse before this prereg is pushed.
