# RP-TN-1 result (1 rung, own pick by EMC, Grok, 2026-10-30; author approved)

Provenance: The author's authorisation ("One more rung to run and than pause"); the rung is my own pick (prereg §0: EMC 2.05 vs HURWITZ-TP-1 ≈ 2; EV disagreed, flagged). STOP removed b8af495; prereg 7ad25ac (pushed alone, first); checker + guard + refusals f055924; live locked beff89d. METHOD read at 5653ec2; Paper I at 4b3abda with Fig. 2 / `formal/statechart/ResearchLoop.tla` followed (PushPrereg → planted pass → LiveRun → locked → Lean → review → STOP).
Locked checker `sims/rptn1/rptn1_checker.py` (sha256 dc1339a0…73f5), guard (d938bc57…00b8), unchanged after the push. Outputs `sims/rptn1/rptn1_{planted,broken,live}.json`.

## Verdict (locked, as-is; no hand adjudication)
**TN-TAUT.** SIMULATED. 2000 exact-rational correlator windows (1000 positive transfer spectra, 1000 with ≥ 1 negative eigenvalue; K ∈ {2,3,4}, t ≤ 6). TN(H0) ⇔ RP2 (H0 PSD ∧ H1 PSD) on **2000/2000**; E = 0 (TN never stricter), W = 0 (TN never weaker); P_TN = 1000/1000. On a finite OS window, total nonnegativity of the Gram/Hankel matrix says exactly what transfer positivity in that window says, nothing more.

- Planted: ALL OK (P1–P10 incl. P5 normalisation alternative accepted, P6 time reversal, P7 gate self-tests, P8 every verdict branch).
- Broken: all rejected: principal-only TN (P3, P4), Hankel-as-Toeplitz (P2, P9, P10), rival H0-only (P3, P4), strict > 0 (P1, P2, P7, P9, P10), wrong H1 window (P3, P4), empty ensemble → ILL-DEFINED.
- Null: vacuity gate passed (1001 TN-true / 999 TN-false); an independent predictor with the same marginals agrees 0.50 of the time vs observed 1.00.
- Rival: RP2 (strong rival) matches TN on every instance; the weak rival "H0 PSD only" is wrong on 999/1000 negative-node windows (H0 PSD on all 2000).
- Report-only: 999/1000 negative-node windows fail both TN and RP2; 1 negative-node window passes both (the 7-moment window is representable by a positive measure, so neither test can see that eigenvalue). The unreflected Toeplitz window [f(|i−j|)] fails TN2 on 1000/1000 positive spectra (Lean, two-state: `toeplitz2_minor_neg`).
- Convention screen: CONV-NA (pre-declared; operator normalisation and time reversal planted P5/P6). Statechart: TN-TAUT is PASS-OR-FAIL class (FinaliseDirect).

## Observations (report-only; none changes the verdict; no checker flaw recorded)
- Retrospectively near-foregone: E = W = 0 is what a finite-matrix version of Fallat–Johnson–Sokal (arXiv:1612.02210) would predict. I did not read that finite statement before the push (prereg §1); prior 0.8 TN-TAUT. If it is a theorem, this rung's map value is the recorded FM-TAUT, not discovery.
- The vacuity gate is balanced by ensemble design (class R mostly fails), so passing it is weak evidence; the strong evidence is the agreement count against a 0.50 null.
- Scope: one operator, one time direction, 4×4 window. A multi-operator or multi-direction Gr≥0 array is outside this rung (reopen trigger).
- Bookkeeping choice not fixed in the prereg: blocker tag `NO-GO` (+FM-TAUT) for a TAUTOLOGICAL bridge, following the GRADED-POSITROID precedent. A proposal for PositiveGeometryEmergentSpaceTime/the author if another label is preferred.
- Pre-push design fix (disclosed, before lock): the variant list was renamed BROKEN → VARIANTS because the import test's pass-flag scan matches "ok" inside "broken".

## Map change (M⁻ branch)
RP-BRIDGE node (notes/FRONTIER-LATTICE-2026-10-30.md §2): the Gr≥0 reading of a single-operator OS window is **refuted as an independent bridge** (FM-TAUT); RP→U1 edge stays SPECULATION with this record attached. New items: blocker row RP-TN-1, EXCLUSION row. The trade-space figure, FRONTIER note and CHIRAL rows are not edited (PositiveGeometryEmergentSpaceTime's files; node/edge status change is a proposal).

## Lean
`PositiveGeometryEmergentSpaceTime.RpTn1` 8 theorems + 1 def, all [propext, Classical.choice, Quot.sound], 0 sorry, no native_decide (LEAN_NUM_THREADS=1, RssAnon watchdog 8 GB, peak 0.59 GB): `hankel2_minor_identity`, `pow_diff_mul_nonneg`, `hankel2_minor_nonneg` (two-state reflected 2×2 minor ≥ 0), `toeplitz2_minor_identity`, `toeplitz2_minor_neg` (unreflected minor < 0, distinct nonnegative nodes), `toeplitz1_minor_zero`, `neg_node_witness` (f(1) < 0 while the rank-one H0 minor is 0), `toeplitz2_witness` (non-vacuity). Fresh AxiomsAll: **TOTAL theorems=1193 defs=638 nonstandard=0, sorry_dependent=0** (was 1185/637). PROVED covers the two-state statements only; the 2000-instance verdict is SIMULATED.

## Tags
Verdict SIMULATED; two-state identities PROVED; Hankel TN ⇔ Stieltjes CITED (1612.02210 Thm 2.8); RP ⇒ positive spectral representation CITED (1201.3415). Blocker `NO-GO`, CONV-NA.

## Credit
Proposal: 0.

Failure-mode: FM-TAUT (TN of the OS Hankel window is equivalent to transfer positivity in the same window; the positroid language restates RP).
Reopen: a Gr≥0 object attached to an RP theory that is not a Hankel/Krylov window of one transfer matrix (multi-operator or multi-time-direction arrays) whose TN is not implied by T ≥ 0; or any finite-window TN failure on a positive spectrum. Reopen flag: not set.
