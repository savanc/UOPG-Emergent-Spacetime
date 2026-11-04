# CONV-LEAN-CERT-2 — convention-invariance re-check of LEAN-CERT-2 (canonical certificate class)

Written 2026-10-30. Authorisation: The author directly, AutoResearch, 2026-10-30: exactly three convention re-check rungs, this is 3/3. Rule: notes/AUTORESEARCH-METHOD.md *Convention-invariance check (2026-10-30)*. Run id CONV-LEANCERT2-2026-10-30-r1. CPU only. Worktree <local path>

## 1. Target
LEAN-CERT-2 (prereg prereg/LEAN-CERT-2-modp-frwzw-2026-10-28.md, locked sims/leancert2/leancert2_checker.py): Python verdict ILL-DEFINED because null N2 accepted 131/480 single-entry corruptions (rule: N2 must be 0/480). Post-result diag (sims/leancert2/diag_n2.txt): all 131 are P-entries in zero rows of M. Lean verdict PARTIAL-LIMIT (k=2,3) — not re-scored here. Locked checker NOT edited; this re-check supersedes only the N2 step.

## 2. Well-posedness gate: the equivalence
Certificates (M,K,P,Q,d) and (M,K,P',Q,d) with P M = P' M are the same certificate class: validity (MK=0, PM+KQ=dI, QK=dI) depends on P only through PM. PROVED (lean/PositiveGeometryEmergentSpaceTime/LeanCertConv.lean, 0 sorry, no native_decide): `PositiveGeometryEmergentSpaceTime.LeanCertConv.split_iff_of_PM_eq`, `PositiveGeometryEmergentSpaceTime.LeanCertConv.valid_iff_of_PM_eq`. Canonical class key (K, PM, Q, d). **Deviation** from the screened wording "canonical representative (Hermite/Smith normal form)": PM is the minimal invariant that the equivalence actually needs; HNF/SNF of P is neither necessary nor implied.

## 3. Hypothesis and rule (fixed now)
N2′: replay the locked N2 loop exactly (seed 20261028, 60 corruptions per certificate, order (k, σ=+1 first), certs parsed from sims/leancert2/certs_lean.txt via emit_lean.parse_certs, as diag_n2.py), counting an accepted corruption only if the class key changes.
- FLIPPED (Python verdict CERTS-OK; tag FM-SPEC, reopen) if N2′ = 0/480 and gates pass. Expected.
- CONVENTION-ROBUST (ILL-DEFINED stands) if N2′ > 0.
- GATE-FAIL if any planted/broken gate fails. Lean PARTIAL-LIMIT for k=2,3 is unchanged either way.

## 4. Planted / broken / null / rival
- Planted: PL1 a P edit in a zero row of M stays valid with the same key; PL2 a K edit changes the key; PL3 the replay reproduces the locked 131 accepted.
- Broken: the raw-P key (K,P,Q,d) must reproduce the locked failure (131 changed).
- Null: N2′ itself (single-entry corruptions; 0/480 required).
- Rival: zero-row canonicalisation (P columns at zero rows of M set to 0 before keying); reported.

## 5. Prior art, contamination, digit masking
Prior art: kernel certificates and their non-uniqueness (any left inverse modulo the kernel) are standard (Storjohann 2000 thesis; Mathlib Matrix API). Contamination: I (AutoResearch) wrote LEAN-CERT-2 and diag_n2 already shows the mechanism; outcome foregone and declared. Digit masking: no numerical target.

## 6. Lock
`leancert2_conv.py` sha256 `77c943e693fdc0e8ae584275bf3aabaae6ac1b0796e903cd8be4ec3d5d394c06`
`conv_guard.py` sha256 `1a80238b736516ca3a507af5281a7a556923b9ce8fb3df64d88aeef131074cc8`
Guard as in CONV-JORD-1. Import test and CLI must refuse before this prereg is pushed. Lean: LEAN_NUM_THREADS=1, 8 GB anon-RSS watchdog; fresh AxiomsAll; commit lean/AxiomsAll_output.txt. Credit: proposal only (expected 0).
