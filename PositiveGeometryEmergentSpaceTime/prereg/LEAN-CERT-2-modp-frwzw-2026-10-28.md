# PREREG LEAN-CERT-2: mod-p certificates with rational reconstruction for the FR-WZW exact rank counts
Written 2026-10-28 by Grok. **one-rung own pick (author approved 2026-10-27).** STOP removed in d390b13 (pushed 2026-10-27, "one rung only"); AUTORESEARCH-STOP is re-committed after this rung. Run id **LEANCERT2-2026-10-28-r1**.
Overlap check: PositiveGeometryEmergentSpaceTime runs CASCADE-1b / CASCADE-2 in its own worktree (`sims/cascade*`, `Cascade*`); INT-1, FL-1Z, M5, MC-1, TS-1 hand entries, EW-Z1 and SG-1 (held) untouched. This rung touches only `sims/leancert2/`, `lean/PositiveGeometryEmergentSpaceTime/LeanCert2.lean` and bookkeeping rows. Own worktree `<local path>`; all other worktrees untouched.
Pushed ALONE (with the locked checker, planted spec and import test) before any checker computation; before the push only `py_compile` was run, then the CLI and the import test (which must refuse; refusal recorded in a later commit).

## 0. Ranking (logged before start; METHOD: EV = P_used × V, P_used = 0.3 × P_naive; no ledger line moved ⇒ EV cap 0.03)
Sources re-read 2026-10-28: MISSION, BACKLOG, notes/TRADE-SPACE-2026-10-23.md, scripts/blocker_tags.py index, notes/AUTORESEARCH-METHOD.md, notes/FRONTIER-RANKING-POSITIVEGEOMETRYEMERGENTSPACETIME-2026-10-16.md, notes/FRONTIER-RANKING-AR-2026-10-16.md, notes/BIG-PICTURE-2026-10-15.md §3, notes/LIT-REVIEW-2026-10-22-cosmic-nine-loops-ai-physics.md §6.
| Candidate | Gate / exclusion | P_naive | V | EV |
|---|---|---|---|---|
| **LEAN-CERT-2 on FR-WZW (pick)** | well-posed (8 integers, exact); method-fit (exact linear algebra) | 0.6 | ≤0.03 (method; FR-WZW is the N_c row of EXCLUSION-LEDGER, no ledger value moves) | 0.18 × 0.03 ≈ 0.005 |
| FR-WZW n=8 odd×odd | fails well-posedness (outcome forced by EFT consistency for any c) | – | – | 0 |
| W g=2 | duplicates EW-Z1b / FZ-1 (excluded family) | – | – | excluded |
| q_e/q_p = −1 | duplicates STRUCT-1/2 | – | – | 0 |
| NL9c | multi-day, not one rung | – | – | infeasible |
| XD-3 | textbook, no falsifiable target | – | – | 0 |
| F-REGGE | fails anti-numerology (p ≥ 0.1 on one integer) | – | – | 0 |
| Reopens (F-DIM′, F-COULOMB, F-POSGEOM-DAUGHTER, LS, FR-WZW) | no named reopen ingredient found in the source sweep | – | – | 0 |
| SG-1 | held | – | – | excluded |
| FL-1Zb | FL-1Z family | – | – | excluded |
| TW-1 | REDUNDANT | – | – | 0 |
| GL-LEC / GL-g | graph-only | – | – | 0 |
| CASCADE-1b, CASCADE-2, INT-1, FL-1Z, M5, MC-1, TS-1 hand entries, EW-Z1 | excluded by instruction | – | – | excluded |
LEAN-CERT-2 is the only candidate that clears the method-fitness and well-posedness gate with nonzero value; its value is small (method rung). Trade-space / BACKLOG line 169 listed it PROPOSED, "needs go and a prereg"; the go is the one-rung instruction, the prereg is this file.

## 1. Prior art (each verified on arXiv 2026-10-28, abstract page / full text)
- von Manteuffel, Schabinger, arXiv 1406.4513 ("A novel approach to integration by parts reduction"): row reduction over prime fields, CRT across primes, Wang rational reconstruction, check of the purported rational solution modulo a new prime. CITED.
- Peraro, arXiv 1905.08019 ("FiniteFlow: multivariate functional reconstruction using finite fields and dataflow graphs"): Wang rational reconstruction succeeds iff |a|,|b| < sqrt(n/2); CRT over several primes; result checked against evaluations over unused primes. CITED.
- Arkani-Hamed, Bai, He, Yan, arXiv 1711.09102: eq. (5) momentum-conservation constraints, eq. (6) dim K_n = n(n−3)/2 (planted control PL1). CITED.
Not found in this sweep: a Lean-kernel-checked kernel-dimension certificate built from mod-p reconstruction for a scattering-amplitude constraint matrix. Absence in a sweep is not proof of absence. The arithmetic method is textbook (CITED above); novelty, if any, is only the Lean-kernel closure of an existing SIMULATED count (method).

## 2. Gate
Well-posed: target = 8 integers dim ker M_{k,σ} over ℚ, matrices fixed by sims/frwzw/rank_count.py (seed 20261016, 40 points, rows cyc−id / rev−σ·id / par+id). Method-fit: exact integer arithmetic only, no fitting, no free parameter, no tuning. Gate verdict: WELL-POSED.
**Declared deviation:** the trade-space line asks for "at least 100×100". No existing SIMULATED exact linear claim is that large; the largest is FR-WZW k=3 at 120×56 (6720 entries). This rung uses 120×56 and reports the shortfall.

## 3. Targets, cases, rules (locked checker `sims/leancert2/leancert2_checker.py`)
Live: integer row-primitive versions of the 8 FR-WZW matrices (row scaling does not change the kernel); certificates (M K = 0, P M + K Q = d·1, Q K = d·1, d ≠ 0) built by mod-p elimination + multi-prime CRT + Wang rational reconstruction of B⁻¹ (B = pivot block), verified exactly in Python (mirror of the Lean checker), then checked in Lean.
SIMULATED values under test (FR-WZW 2026-10-16): σ=+1, k=0..3: 1, 2, 5, 10; σ=−1: 0, 0, 0, 2.
Planted: PL1 ABHY eq. (5) n=5,6,7 → 5, 9, 14 (1711.09102 eq. (6)); PL2 synthetic 120×56, rank 46 (dim 10), entries ≥ 25 digits; PL3 synthetic 120×56, rank 54 (dim 2).
Broken (already proved false): B1 "dim ker(ABHY eq5, n=6) = 10", refuted by PROVED `PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_finrank` (= 9): the 10-column forged certificate must be rejected by the mirror checker and, in Lean, `decide` must evaluate the checker to `false` (theorem stating rejection). B2 (supplementary): dim-9 claim on PL2 must be rejected.
Null rates (no tuning): N1 mod-p sketch disagreement over 20 fresh 31-bit primes per live matrix (reported); N2 single-entry ±1 corruptions, 60 per live certificate, acceptance must be 0/480.
Rival baselines: original FR-WZW Fraction elimination (qrank logic) on the unscaled rational rows; sympy `Matrix.rank` on the integer matrix for n ≤ 21. Timing vs the LEAN-CERT-1 extrapolation t ≈ 2.2 s × (n/21)^3.2 is a diagnostic only.
Python verdict: ILL-DEFINED if any planted case fails, B1/B2 accepted, or N2 > 0; CONTRADICTS if any certified dim ≠ SIMULATED dim; else CERTS-OK.

## 4. Lean plan and kill
Module `lean/PositiveGeometryEmergentSpaceTime/LeanCert2.lean` (namespace `PositiveGeometryEmergentSpaceTime.LeanCert2`, imports `PositiveGeometryEmergentSpaceTime.LeanCert`). Matrices as `List (List ℤ)` (rows; K, Q also as rows), dot products by structural recursion; soundness lemma (list checker true ⇒ the Fin-matrix identities) proved once, then `PositiveGeometryEmergentSpaceTime.LeanCert.finrank_ker` gives `Module.finrank ℚ (ker (cq M).mulVecLin) = k`. Certificates checked by `decide +kernel`. Theorems `frwzw_k{0..3}{p,m}_finrank`, planted `abhy{5,6,7}_finrank'`, `planted_pl2_finrank`, broken `broken_abhy6_dim10_rejected`.
PROVED only at 0 sorry, no `native_decide`, fresh AxiomsAll (temp file, committed output) with 0 nonstandard axioms.
Kill: any single certificate whose `lake env lean` check exceeds 1 h wall or 15 GB RSS → that theorem is not claimed (LIMIT). CPU only.
Lean verdict: **UPGRADED** if all 8 FR-WZW finrank theorems are PROVED and equal the SIMULATED values (rank step becomes PROVED; matrix generation from kinematics stays SIMULATED, cross-checked by the rival baselines); **PARTIAL-LIMIT** if some hit the kill; **CONTRADICTS** / **ILL-DEFINED** as in §3.

## 5. Tags and ledger
Tags used: PROVED (Lean, 0 sorry), SIMULATED (Python), CITED (§1), CONJECTURE (priors), SPECULATION (none planned). Ledger line: EXCLUSION-LEDGER row FR-WZW (N_c from the n=5 parity-odd extension); this rung moves no ledger value (it can only upgrade the evidential tag of the rank counts). Proposed credit 0; CREDITS.md not edited.

## 6. Lock
`leancert2_checker.py` sha256 `74ca907f7f644774fd82b8aae56d9407dd17e667148866b94ad2b55435977084`
