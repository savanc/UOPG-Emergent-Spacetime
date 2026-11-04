# PREREG RP-TN-1: does total nonnegativity (Gr≥0) of an OS correlator window carry anything beyond transfer positivity? (locked)

Authorisation: author approved (2026-10-30). Exactly 1 rung, then AUTORESEARCH-STOP.

Re-read before picking (2026-10-30, after `git pull --ff-only` to 5653ec2): `notes/AUTORESEARCH-METHOD.md` in full at **METHOD commit 5653ec2** (`git log -1 --format=%h -- notes/AUTORESEARCH-METHOD.md`), incl. the convention-invariance rule, its 30 Oct amendment, the CHIRAL v2 lesson and the new SUPERSEDED label; and Paper I at **4b3abda** (`papers/human-agentic-methods-2026-10/tex/main.tex`, read only) with the Fig. 2 rung statechart and `formal/statechart/ResearchLoop.tla`. This rung follows those states: StartRung → PushPrereg (this file, alone) → planted/broken → (PlantedFail ⇒ ILL-DEFINED, no live) → LiveRun → locked → convention screen if NO-GO/ILL-DEFINED → Lean → review → credit proposal → closed → STOP.

## 0. Why this rung (re-rank, METHOD exploration rules 1–9)
Excluded: gated M5, MC-1, TS-1 hand entries, EW-Z1, CASCADE-2, pilot-wave; PositiveGeometryEmergentSpaceTime-owned CASCADE-1b, INT-1, FL-1Z, paper; CHIRAL-LATTICE-1 itself.

| Rung | P_naive | P_used=0.3·P | V | EV | EMC | IV_min | d vs last 3 (RG-IR-1, CHIRAL v1, CHIRAL v2) | Foregone? |
|---|---|---|---|---|---|---|---|---|
| **RP-TN-1 (this)** | 0.15 (M⁺ = TN-EXTRA) | 0.045 | 0.1 (no ledger line; cap 0.03) | 0.0045 | 0.045·3 + 0.955·2 = **2.05** | 2 | 4 / 3 / 3 | no (prior TN-TAUT ≈ 0.8) |
| HURWITZ-TP-1 (B6) | 0.07 | 0.02 | 0.3 | **0.006** | ≈ 2 | 1 | 2 (B6 TP line repeats RG-IR-1 area) | FM-TAUT predictable |
| RP-BRIDGE-0 (2D toy Gram PSD) | 0.95 (known) | — | 0 | 0 | — | 0 | — | yes (PSD is the definition) |
| CDT-RIVAL | reading node, not a rung | | | | | | | |
| TP-1BR / EW-POS | killed at rule 7 earlier | | | | | | | |

- d axes (basin, SM ledger line, method class, declared failure tag): vs RG-IR-1 = 4 (RG-IR vs RP-BRIDGE frontier node; y_t vs none; ODE closed form vs exact matrix-minor enumeration; FM-FREE vs FM-TAUT). vs CHIRAL v1 = 3 and vs v2 = 3 (cross-basin text audit vs RP-BRIDGE node; ledger none = none; text classifier vs exact minors; SPEC/QNBLIND vs TAUT).
- Exploration slot: CHIRAL v1 filled it within {RG-IR-1, CHIRAL v1, this}, so the slot is satisfied either way. RP-TN-1 is nevertheless exploration-eligible (d ≥ 3 to all three, no frozen basin, not foregone, IV_min = 2) and is ranked by **EMC: 2.05 > HURWITZ-TP-1 ≈ 2** (HURWITZ is not exploration-eligible, d = 2). **Rule-9 flag: under P_used × V, HURWITZ-TP-1 (0.006) ranks above RP-TN-1 (0.0045); EMC and EV disagree**. I take RP-TN-1 because HURWITZ-TP-1's FM-TAUT is predictable on paper and it repeats the RG/TP area of the last pick; RP-BRIDGE-0 is foregone (credit 0).
- M⁺ (TN-EXTRA): RP-BRIDGE node gets a live edge (Gr≥0 content beyond OS positivity); RP→U1 edge SPECULATION → live; BACKLOG item "which Gr≥0 cell". M⁻ (TN-TAUT/WEAKER/NO-BRIDGE): RP-BRIDGE node → blocker row FM-TAUT (the positroid reading restates transfer positivity in a finite window), RP→U1 edge refuted-as-independent, reopen trigger named.
- Failure-mode tally / trigger state (basin_tally.py at 5653ec2): B1 basin form FIRED (FM-MODEL ×3), B5 FIRED (FM-FREE ×5); this rung is outside both. Mode form over last 5 on main (SURF-1′ FM-RANGE, JORD-1 FM-SPEC, RG-IR-1 FM-FREE, CHIRAL v1 FM-SPEC+FM-QNBLIND, CHIRAL v2 FM-QNBLIND): no tag ≥ 3 → not fired.
- Feasibility (rule 7): 2000 instances × (69 minors of a 4×4 + 15 + 7 principal minors + 52 Toeplitz ≤2×2 minors), exact Fractions, cofactor determinants of size ≤ 4: < 1 min CPU, < 200 MB. Kill: > 30 min CPU or > 2 GB → PARTIAL-LIMIT, no verdict.
- Well-posedness / fitness: every label is a finite exact sign test on rational matrices; the verdict is a fixed map of integer counts. Exact arithmetic means no tolerance choice.

## 1. Prior art (read 2026-10-30)
- Hankel total positivity ⇔ Stieltjes moment sequence (infinite case): Fallat–Johnson–Sokal arXiv:1612.02210 Thm 2.8 (citing Gantmacher–Krein p. 460 Thm 9; Pinkus Thm 4.4); also arXiv:1506.07449, arXiv:2007.14924, PAMS doi:10.1090/proc/14599 (abstracts/statements read via search).
- RP on the lattice ⇒ positive spectral (Källén–Lehmann-type) representation of two-point functions: arXiv:1201.3415 (abstract read). Euclidean lattice correlator matrices as a truncated Hamburger moment problem: arXiv:2508.01377 (abstract/intro read).
- Osterwalder–Seiler 1978 (positive self-adjoint transfer matrix for lattice gauge theory) and Wilson 1974, as cited in notes/FRONTIER-LATTICE-2026-10-30.md §2.
- **Not read:** any finite-matrix version of the FJS characterisation. I recall (memory, unverified) that one exists; if true, TN-TAUT is expected. This is why the prior is ≈ 0.8 and not 1.
- Not found: any paper stating the OS Gram/Hankel window as a point of the totally nonnegative Grassmannian. Novelty of the question is the reading, not the mathematics.

## 2. Memory / contamination disclosure
On paper before this push (no code run on any ensemble instance): (i) for f(t) = Σ w_k x_k^t with w, x > 0, H = [f(i+j)] = Vᵀ W V with V a generalized Vandermonde, so H is TN by Cauchy–Binet; (ii) two-state Hankel 2×2 minor = w₁w₂(x₁x₂)^{a+c}(x₂^k − x₁^k)(x₂^l − x₁^l) ≥ 0; (iii) two-state Toeplitz f(a)f(b) − f(0)f(a+b) = −w₁w₂(x₁^a − x₂^a)(x₁^b − x₂^b) < 0 for distinct nodes, a, b ≥ 1 (so the unreflected Toeplitz window is never TN2); (iv) a negative node keeps H0 PSD (Gram) but makes f(1) < 0 possible; (v) the planted values below. The checker was only `py_compile`d before the push.

## 3. Object, rule, verdict (locked; `sims/rptn1/rptn1_checker.py`)
- Correlator window f(t) = Σ_k w_k λ_k^t, t = 0..6. H0 = [f(i+j)]_{i,j=0..3} (OS Gram/Hankel), H1 = [f(i+j+1)]_{i,j=0..2}, Tz = [f(|i−j|)]_{i,j=0..3} (unreflected).
- Labels: **TN** = all 69 minors of H0 ≥ 0. **RP2** (strong rival: transfer positivity seen in the window) = H0 PSD and H1 PSD (PSD = all principal minors ≥ 0). H0PSD; TzTN2 = all 1×1 and 2×2 minors of Tz ≥ 0.
- Ensemble (seed 20261030, `random.Random`): class P: 1000 instances, K ∈ {2,3,4}, distinct nodes from {k/12: k = 1..11}, weights j/6 with j ∈ {1..6} (positive transfer matrix); class R: 1000 instances, same but nodes from {k/12: k = ±1..±11}, resampled until ≥ 1 node < 0 (self-adjoint transfer matrix with a negative eigenvalue: not RP at unit step, e.g. staggered-type oscillating states).
- Counts: E = #(TN false ∧ RP2 true) (TN strictly stronger); W = #(TN true ∧ RP2 false); P_TN = TN rate on class P.
- **Decision rule (fixed now):** ILL-DEFINED if planted not ALL_OK or broken not ALL_REJECTED (live not run), or the vacuity null gate fails (TN-true count < 50 or TN-false count < 50); else **NO-BRIDGE** if P_TN < 1; else **TN-WEAKER** if W > 0; else **TN-EXTRA** if E > 0; else **TN-TAUT** (E = W = 0: on every instance TN ⇔ RP2); UNCLASSIFIED is unreachable and stated for exhaustiveness.
- Report-only: agree count, null agreement of an independent predictor with the same marginals, R_det (class-R TN failures), class-R RP2 failures, P_Tz_fail (class P, prediction 1000/1000), H0PSD on all instances (prediction all true).
- Verdict class for the statechart: NO-BRIDGE is the NO-GO class; TN-TAUT, TN-EXTRA, TN-WEAKER are PASS-OR-FAIL class (FinaliseDirect).
- **NO hand adjudication.** The locked verdict is reported as-is; if it looks wrong I record a checker flaw in a superseding note and do not flip it.

## 4. Planted / broken / null / rival / non-uniqueness / conventions
- Planted (must all recover): P1 one node 1/2 → TN, RP2, TzTN2 true (rank 1; Tz = λ^{|i−j|} kernel is TN). P2 nodes {1/3, 2/3} → TN, RP2 true, TzTN2 false. P3 node −1/2 → TN false, RP2 false, H0PSD true. P4 {1/2, −1/2} equal weights (staggered-type) → TN false, RP2 false, H0PSD true. P9 {1/5, 3/5, 9/10} (off-grid) → TN, RP2 true. P10 {1/5, 4/5} → TN true, TzTN2 false. P5 valid alternative (rule 8; non-uniqueness = normalisation of the operator O): weights ×3 give identical labels — must be ACCEPTED. P6 joint reversal J H0 J preserves TN (P2, P4). P7 gate self-tests: PSD and TN each true once ([[1,1],[1,1]]) and false once ([[1,2],[2,1]]). P8 verdict-map self-test: every branch (two ILL-DEFINED, NO-BRIDGE, TN-WEAKER, TN-EXTRA, TN-TAUT) fired once.
- Broken (each must fail ≥ 1 planted, checked on paper): TN on principal minors only (P3 fails); Hankel built as Toeplitz (P2 fails); rival = H0 PSD only (P3 fails); strict > 0 (P1 fails); H1 with wrong window f(i+j) (P3 fails); empty ensemble → ILL-DEFINED.
- Null: vacuity gate above (both TN outcomes ≥ 50) plus reported independent-predictor agreement.
- Rival: RP2 (transfer positivity in the window) is the strong rival; the verdict is its agreement with TN. Weak rival "RP ⇔ H0 PSD only" is ruled out by P3/P4 by construction.
- Convention screening: **CONV-NA** pre-declared. The physics-preserving equivalences of the object are operator normalisation (weights scale) and time reversal (J H J); both are planted (P5, P6). Exact rationals, no units, sign or basis choice. A time-origin shift f(t) → f(t+1) is a different window and would be a new rung.

## 5. Lean plan
`PositiveGeometryEmergentSpaceTime.RpTn1`: (1) two-state Hankel 2×2 minor ≥ 0 for nonnegative nodes/weights (identity (ii)); (2) two-state Toeplitz 2×2 minor < 0 for distinct nonnegative nodes, positive weights, a, b ≥ 1; (3) one-state Toeplitz minor = 0; (4) witness: node −1/2 gives f(1) < 0 (H1 diagonal) while H0's 2×2 principal minor is 0. 0 sorry, no native_decide, LEAN_NUM_THREADS=1, RssAnon watchdog ~8 GB, fresh AxiomsAll. Lean targets do not depend on checker gates (JORD-1 b).

## 6. Tags (declared)
Verdict SIMULATED (exact enumeration over a declared ensemble). Mathematics (i)–(iii): CITED + PROVED (Lean, two-state). Expected failure mode if TN-TAUT: FM-TAUT. Credit: proposal 0 unless TN-EXTRA (then proposal only, for the author).

## 7. Lock
`rptn1_checker.py` sha256 `dc1339a072c084fc03015fcfa94eb46780db5de56ce4e4795ba5bfea931f73f5`
`guard.py` sha256 `d938bc576d53e07dae2f91678592d4e239017858fd53f47f88cd1756ec4a00b8`
Guard (hardened): called in every scoring/live function (planted, broken, live, _suite, _run) and the CLI; on every call re-reads this prereg, re-hashes checker + guard, re-runs `git merge-base --is-ancestor <prereg commit> origin/main`; no pass flag. Import test (2 calls) and CLI must refuse before the push (sims/rptn1/guard_refusal.txt).
