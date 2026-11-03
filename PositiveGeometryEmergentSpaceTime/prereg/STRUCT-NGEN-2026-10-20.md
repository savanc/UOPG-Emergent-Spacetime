# PREREG STRUCT-NGEN sharpen: does any declared theory-consistency condition force N_gen = 3?
Written 2026-10-20 by Grok. continuous-mode own pick (author approved 2026-10-20); last rung before the pause. STOP absent on origin/main at rung start.
Pushed ALONE (with locked checker, planted spec and import test) before any checker computation. No physical datum is used for the verdict.

## 0. Re-read: STRUCT-3 (reviews/STRUCT-3-result-2026-10-15.md, Lean `PositiveGeometryEmergentSpaceTime.STRUCT3`)
Verdict NO-GO-FOR-N_gen=3: AF(SU3) ⇒ N ≤ 8, AF(SU2) ⇒ N ≤ 5, KM ⇒ N ≥ 3, window {3,4,5}. Exact assumptions: one Higgs doublet; one-loop AF only (two-loop/Banks–Zaks not considered); KM requires CP violation from the CKM; "forced" = constant over the family. **Correction now applied:** KM is an experimental input (CP violation is observed, not required by consistency), so under this rung's rules it cannot support forcing.

## 1. Declared conditions = trials (look-elsewhere), by kind
**K — theory consistency (may support "forces"):**
- K1 local perturbative gauge ACC — N-blind (`STRUCT3.acc_ngen_blind`).
- K2 Witten SU(2) global anomaly (# doublets even) — 4 doublets/generation ⇒ blind (`witten_ngen_blind`).
- K3 Wang–Wen–Witten "new SU(2) anomaly" (1810.00844, verified abstract): concerns spin-(4r+3/2) multiplets; none in the SM ⇒ blind (CITED).
- K4 Dai–Freed refinement for the SM gauge group (García-Etxebarria–Montero 1808.00009: SM anomaly-free) ⇒ blind (CITED).
- K5 AF of SU(3)_c (one loop): N ≤ 8 (textbook, FOREGONE).
- K6 AF of SU(2)_L (one loop, one Higgs doublet): N ≤ 5 (FOREGONE; weaker status: a Higgsed SU(2) need not be AF — flagged).
- K7 perturbative unitarity (Chanowitz–Furman–Hinchliffe) and K8 vacuum stability: bound MASSES, not N; N-blind without mass data (not evaluated; declared blind).
- K9 U(1)_Y Landau pole below M_Pl: needs the measured α_Y (data) — declared excluded from forcing, not computed.
**D — dynamical (not strict consistency):** D1 no two-loop Banks–Zaks zero in QCD (b₁ > 0): N ≤ 4.
**C — conditional consistency (requires an extra gauged discrete symmetry; not SM consistency per se):**
- C1 baryon triality Z₉ (1808.00009 §4.2, verified text: "total charge mod 9 … is 3 per generation, so we need the number of generations to be a multiple of 3"): 3 | N.
- C2 Spin-Z₄ / Z₁₆ (1808.00009 §4.3): 16 | (Weyl count)·N; without νᶜ ⇒ 16 | N; with νᶜ blind.
**E — experimental (CITED, report-only, never forcing):** E1 KM CP violation ⇒ N ≥ 3; E2 LEP light-neutrino count N_ν ≈ 3 (Janot–Jadach 1912.02067; memorised value, not used); E3 Higgs + EW data exclude a sequential 4th generation (Djouadi–Lenz 1204.1252; Eberhardt et al. 1209.1101).

## 2. Contents and rival
SM (15 Weyl/gen), SM+νᶜ (16), and the **rival** SU(3)_c×SU(3)_L×U(1)_X 3-3-1 model (Pisano–Pleitez hep-ph/9206242, verified abstract; Frampton PRL 69 (1992) 2889): SU(3)_L anomaly #3 = #3̄ ⇒ 3 | N; QCD AF with n_f = 3N ⇒ N ≤ 5.
Trials: 3 contents × {core, +D1, +C1, +C2} = 12 nominal (331 + C1/C2 not applicable ⇒ 10 evaluated). Scan N = 1…20.

## 3. Rule (fixed)
- SM verdict from the SM CORE set (K1–K6, N ≥ 1): FORCES-3 iff window = {3}; else NOT-FORCED.
- Variants: a {3} window from D1 is DYNAMICAL-3, from C1/C2 CONDITIONAL-3, from E1 EMPIRICAL-3 — never FORCES-3.
- Rival: 331 core = {3} ⇒ RIVAL-SINGLES-OUT-3 (the condition type is not SM-specific).
- Planted failure ⇒ ILL-DEFINED.

## 4. Foregone (declared; Lean `PositiveGeometryEmergentSpaceTime.STRUCTNGen`, compiled BEFORE this prereg, no data)
`sm_core_window` / `sm_core_not_forced`: SM core = {1,…,5} ⇒ NOT-FORCED is FOREGONE (textbook). `triality_window` (C1 + K6 ⇒ {3}; `triality_su3_only_not_forced`: with K5 only {3,6}), `z16_no_nuc_window_empty`, `bz_two_loop_iff`, `rival331_window` (331 ⇒ {3}) — all known in the literature (CITED) and FOREGONE. Content of the rung: the K/D/C/E classification and the formal statement that the only routes to exactly 3 are conditional (gauged triality) or non-SM (3-3-1).

## 5. Planted and broken
Planted (inline in checker): STRUCT-3 window with KM = [3,4,5]; b₀(SU2) at N = 3 equals 19/6; AF(SU3) max 8; triality residue per generation −3; 331 anomaly true at N = 3, 6, false at 2; QCD b₁(n_f = 6) = 26. Broken (proved false, `STRUCTNGen.sm_core_not_forced`): "the SM unconditional consistency set forces N_gen = 3" — must be REJECTED.

## 6. Anti-numerology / contamination
No fit. All window results memorised/textbook (contaminated, declared); the verdict uses no data. νᶜ triality charge taken as 0 (not in the paper's MSSM table) — report-only caveat.

## 7. Prediction
SM core NOT-FORCED ~99%; SM+C1 CONDITIONAL-3 ~95%; 331 RIVAL-SINGLES-OUT-3 ~95%; SM+C2 without νᶜ empty ~95%.

## 8. Guard and locks
Hardened guard as before (`guard` in b0_*, b1_qcd, witten_ok, acc_blind, anomaly331, triality_ok, z16_ok, km_ok, window, label, verdict); no pass flag; per-call re-verification; caches keyed by origin/main sha; fetch once per process. Import test: 2 direct calls must refuse before the push; before the push only `py_compile` was run.

Locked:
- `sims/ngen/ngen_checker.py` sha256 `5aeccca1ce54ac789703e96aab17a6c7fe580033a765c56435576af00d0eb1dd`
- `sims/ngen/planted_cases.json` sha256 `4919494252189dbebbe90cb6a039580eaf98418b0599a7144989800d7f212137`
- `sims/ngen/import_guard_test.py` sha256 `8b9df00f886029117aa85a4420a97172b61dc8c318312f6abdc6536235785c18`
