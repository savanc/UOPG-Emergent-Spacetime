# PREREG TRIALITY-WHY: is there a consistency (not phenomenological) reason to gauge baryon triality?
Written 2026-10-23 by Grok. **continuous-mode own pick (author approved 2026-10-23).** STOP absent on origin/main at rung start (checked, origin 6973f1b, the unpause commit).
Frontier rank: next ranked rung after GRADED-POSITROID in REVIEW-2026-10-20 §4 item 4 / trade-space OPEN subgraph (TRIALITY-WHY 0.10; P_naive = 0.05, P_used = 0.3 × 0.05 = 0.015). It is the STRUCT-NGEN reopen trigger ("a consistency (not phenomenological) reason to gauge baryon triality or another Z_n with N_gen-dependent anomaly").
Overlap check: PositiveGeometryEmergentSpaceTime runs CASCADE-1b / CASCADE-2 in its own worktree (`sims/cascade*`, `Cascade*`); INT-1 (`sims/int1`, `IntChamber`), FL-1Z (`sims/fl1z`, `FL1Z`), M5, MC-1, TS-1, EW-Z1 untouched. This rung touches only `sims/triwhy/`, `lean/PositiveGeometryEmergentSpaceTime/TrialityWhy.lean` and bookkeeping rows. Own worktree `<local path>`; `<local path>` and all other worktrees untouched.
Pushed ALONE (with locked checker, planted spec, import test) before any checker computation; before the push only `py_compile` and the import test were run. No physical datum is used for the verdict.

## 0. Prior art (each verified on arXiv 2026-10-23, abstract page or full text)
- García-Etxebarria, Montero, arXiv 1808.00009 ("Dai-Freed anomalies in particle physics"): the Z₉ baryon-triality anomaly cancels iff 3 ∣ N_gen; the paper stresses that an anomaly in a global symmetry is not an inconsistency (it only obstructs gauging), and motivates gauging through quantum-gravity arguments. CITED.
- Harlow, Ooguri, arXiv 1810.05337 ("Symmetries in quantum field theory and quantum gravity"): no global symmetries in quantum gravity (AdS/CFT); approximate global symmetries may survive, broken by Planck-suppressed terms. CITED.
- Banks, Seiberg, arXiv 1011.5120 ("Symmetries and Strings in Field Theory and Gravity", PRD 83 084019): in quantum gravity there are no global symmetries; discrete gauge symmetries. CITED.
- Dreiner, Luhn, Thormeier, arXiv hep-ph/0512163 ("What is the discrete gauge symmetry of the MSSM?"): Ibáñez–Ross linear conditions are necessary but not sufficient; B3 = R₃L₃ selected by phenomenological demands (proton decay); with sphalerons only B/3 − L_i are conserved; global discrete symmetries are typically violated by quantum gravity, motivating gauging. Ibáñez–Ross 1991 and Krauss–Wilczek 1989 are used only as "cited in hep-ph/0512163". CITED.
- Hsieh, arXiv 1808.02881 ("Discrete gauge anomalies revisited"): Spin×Z_n anomaly-free conditions; the cubic term can be trivialised by a symmetry extension, the linear (mixed) term cannot; reproduces Ibáñez–Ross. CITED.
Not found in this sweep: any paper deriving gauged B3 (or 3 ∣ N_gen) from a consistency requirement that does not presuppose that B3 is gauged. Absence in a sweep is not proof of absence.

## 1. Method-fitness and well-posedness gate (before any computation)
"Is there any reason to gauge B3" is open-ended, hence not well-posed as stated (REVIEW §4: "gate it on a stated mechanism, otherwise it is numerology"). Gate: restrict to a DECLARED FINITE mechanism list; each mechanism has a K/C/D/E class (STRUCT-NGEN): only K can support "forced".
- M1 [K] exactness ↔ linear gauge anomaly (SU(2)²Z_k, SU(3)²Z_k, grav²Z_k) — trial T1.
- M2 [C] Dai–Freed Z₉ (presupposes gauging) — trial T2.
- M3 [K-conjecture] no global symmetries in quantum gravity (exact global ⇒ gauged OR broken) — trial T3.
- M4 [geometry] positive-geometry side: Z₃ acting through the real column torus of Gr(k,n)(ℝ); cyclic Z_n of Gr⁺(k,n) — trial T4.
- M5 [E] proton stability (phenomenological) — T5, reported only, cannot force.
Any undeclared mechanism stays OPEN (blocker reopen trigger). Method fit: all quantities are integers/rationals (exact arithmetic, Python `fractions`, Lean `omega`/`decide`/`ring`/`nlinarith`); no continuous fitting, no free parameter. Gate verdict: WELL-POSED-RESTRICTED (to M1–M5).

## 2. Trials (look-elsewhere: 5 trials, Bonferroni ×5)
Charges: generation-universal Z_k, LH Weyl; qQ, qL, qH free; Yukawas fix qU = qH − qQ, qD = −qQ − qH, qE = −qL − qH, qN = qH − qL; doublet charge c = 3qQ + qL.
- **T1 [K]** scan k = 2..18, all (qQ, qL, qH) mod k, N = 1..20: SU(2)-instanton exactness window (k ∣ N c) vs Ibáñez–Ross SU(2)² window; SU(3)² sum and grav² sum (with νᶜ) vanish. TAUT iff all equal / zero.
- **T2 [C]** Dai–Freed Z₉ window (CITED 3 ∣ N) vs the T1 exactness window of Z₉ acting by 3B.
- **T3 [K-conj]** gauge-invariant dim-6 ΔB ≠ 0 operators (QQQL, uᶜuᶜdᶜeᶜ; QQuᶜeᶜ and QLuᶜdᶜ as same-chirality non-invariant controls): BREAK iff one is invariant, ΔB ≠ 0 and B3-odd. W_QG = core if BREAK, else core ∩ 3ℤ.
- **T4 [geometry]** real roots of x³ = 1 (torus_blind iff 1); fraction of n ∈ 4..20 with 3 ∣ n (cyclic family-constant iff 0 or 1).
- **T5 [E]** reported only.
B3 charges: hep-ph/0512163 eq. (2.17), (m,n,p) = (1,0,1): Q 0, uᶜ −1, dᶜ 1, L −1, eᶜ 2 (= −(B − 2Y) mod 3, so B3 ≅ Z₉(3B) modulo a U(1)_Y gauge rotation).

## 3. Null and rival
Null: (k, c) with 2 ≤ k ≤ 18, 0 ≤ c < k (170 pairs, uniform); window = multiples of d = k/gcd(k, c); P3 = P(window ∩ {1..5} = {3}). Foregone count (Lean `null_count_d3`): 12/170 ≈ 0.071; 32/170 single out some N ∈ {3,4,5}. Anti-numerology threshold: a "forcing" of 3 must have Bonferroni-corrected base rate < 0.01; 5 × 0.071 = 0.35, so a bare choice of Z_k cannot pass.
Rival ORDER (strong, no physics): "window = multiples of k/gcd(k, c)" (Lean `window_iff`) — must reproduce every exactness window. Rival from STRUCT-NGEN: 3-3-1 (`STRUCTNGen.rival331_window`, CITED there) also gives exactly 3; recorded, not recomputed.

## 4. Rule (fixed; in checker docstring)
WELL-POSED iff all planted OK (else ILL-DEFINED). W_K = core ∩ W_QG (∩ 3ℤ if not torus_blind). FORCED-K iff W_K ⊊ core, 3 ∈ W_K and 5·P3 < 0.01. NOT-FORCED / TAUTOLOGICAL-CONDITION (NO-GO) iff W_K = core and TAUT and BREAK and torus_blind and ORDER reproduces all and T2 equal. NOT-FORCED / OTHER iff W_K = core otherwise. Otherwise → UNCLASSIFIED.

## 5. Foregone (declared; Lean `PositiveGeometryEmergentSpaceTime.TrialityWhy`, compiled BEFORE this prereg with Mathlib only, no data)
`sphaleron_eq_wwx`/`exact_iff_wwx` (T1 TAUT), `ccx_zero`, `grav_nuc_zero`, `grav_no_nuc`, `doublet_charge_Y_shift`, `window_iff` (ORDER), `b3_exact_iff`, `z9_exact_iff`, `b3_eq_neg_BminusTwoY`, `qqql_gauge_invariant`, `qqql_deltaB`, `qqql_breaks_b3` (BREAK), `qg_window`, `real_cube_root_one`, `torus_z3_trivial` (torus_blind), `cyclic_z3_not_family_constant`, `null_card`, `null_count_d3`, `null_count_singleton`, `triality_why_summary`. Expected verdict NOT-FORCED / TAUTOLOGICAL-CONDITION (NO-GO): FOREGONE, declared. Content of the rung: the formal statement that the Ibáñez–Ross linear condition for B3 IS the condition that B3 be an exact (sphaleron-invariant) symmetry, so "3 ∣ N" is the price of B3 being a symmetry at all, not a further consistency demand; and that the no-global-symmetries argument is satisfied by breaking B3 for every N.

## 6. Planted and broken
Planted (inline; `planted_cases.json` lists them): P1 Z₉(3B) window = multiples of 3 (`STRUCTNGen.triality_iff`); P2 B3 = −(B − 2Y) mod 3; P3 sphaleron N = 3: Δ(3B) = 9; P4 SU(3)² sum 0; P5 B − L exact for all N; P6 QQQL invariant, ΔB = 1, B3-odd; P7 detector: QUL not invariant.
Broken: "the gauged-triality window within the AF-SU(3) range {1..8} is {3}" — already false by Lean `PositiveGeometryEmergentSpaceTime.STRUCTNGen.triality_su3_only_not_forced` (N = 6 passes); must be REJECTED.

## 7. Prediction
NOT-FORCED / TAUTOLOGICAL-CONDITION ≈ 95%. Proposed credit 0 (proposal only).

## 8. Guard and locks
Hardened guard: `guard` in every scoring/live function (charges, sphaleron_charge, wwx_sum, ccx_sum, grav_sum, window_*, trial_T1..T4, b3_charge, op_invariants, null_rate, rival_order, classify, guard_banner); no pass flag; per-call re-verification of the checker sha256 against this file and of this prereg's add-commit as an ancestor of origin/main; caches keyed by origin/main sha; fetch once per process. Heavy trials do their arithmetic inline inside one guarded call. Import test: 2 direct calls must refuse before the push.

Locked:
- `sims/triwhy/triwhy_checker.py` sha256 `a7be9f5ab7f7b20d7db63104f11d535776e33f521f2ebd8f82384d2c924d32fb`
- `sims/triwhy/planted_cases.json` sha256 `20a7683a86034f5df1b969e915fc2329bf16aa72a168096bd19efe0dcaebe07a`
- `sims/triwhy/import_guard_test.py` sha256 `14b53f0f663ac91acee433952890ce5e5675da6c4ac3461e0c7acc3d72d9b662`
- (foregone-theorem file, not a scoring input; committed with the result) `lean/PositiveGeometryEmergentSpaceTime/TrialityWhy.lean` sha256 `776e8fb230f59a9242e084eedb9bcbfc849733f55239bd12e5f428b16c0073bb`
Run id: TRIALITY-WHY-2026-10-23-r1.
