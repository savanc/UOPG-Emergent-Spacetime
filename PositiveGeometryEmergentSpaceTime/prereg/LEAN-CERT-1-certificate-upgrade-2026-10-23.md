# PREREG LEAN-CERT-1: can an exact sketch-and-verify certificate checker move a SIMULATED rung result to PROVED in Lean?
Written 2026-10-23 by Grok. This is a **The author-directed manual frontier rung**, not AutoResearch (AutoResearch is paused and is not touched). The author said "Ok go" at on 2026-10-23, relayed by the parent: run LEAN-CERT-1, then CASCADE-1, and not NL9c.
Source: `notes/LIT-REVIEW-2026-10-22-cosmic-nine-loops-ai-physics.md` (commit 5017263), lesson 4: "certificate-checked linear algebra, sketch mod p and verify exactly, Lean checks the certificate".
Pushed ALONE, ff-only, together with the locked checker, planted spec and import test, before any checker computation (precedents: INT-1 32cec63, FL-1Z 99863fe). No physical datum enters.

## 1. Hypothesis
**H (LEAN-CERT-1).** Take a SIMULATED repo result that rests on an exact linear-algebra fact. An integer split certificate makes it PROVED. The certificate is computed outside Lean (exact rref, after a randomised mod-p rank sketch), checked inside Lean by `decide` (kernel reduction, no `native_decide`), and turned into the result by a once-proved soundness theorem. This happens:
- within the box budget: < 1 h wall time and < 15 GB RSS for the Lean module;
- with standard axioms only;
- with a planted wrong certificate rejected by the same checker.

**Upgrade target (T1).** GRADED-POSITROID N_ACC = 2. Run GPOS-2026-10-22-r1, `sims/gpos/gpos_checker.py` `count_full_acc`, currently SIMULATED (exact). The statement: on the domain R = {p/q : −10 ≤ p ≤ 10, 1 ≤ q ≤ 10} with yQ = 1, the set of (yu, yd, yL, ye) ∈ R⁴ satisfying the four ACCs (§2) is exactly {(−4, 2, −3, 6), (2, −4, −3, 6)}, so the count is 2.

**Known-result reproduction (T0), same run.** ABHY 1711.09102 (CITED, fetched 2026-10-23 at arxiv.org/abs/1711.09102):
- eq. (5): n independent momentum-conservation constraints Σ_{j≠i} s_ij = 0;
- eq. (6): dim K_n = n(n−3)/2;
- eq. (10): s_ij = X_{i,j+1} + X_{i+1,j} − X_{i,j} − X_{i+1,j+1}, and the planar X form a basis.

Reproduced as "ker C = image A and A is injective", where C is eq. (5) and A is eq. (10), for n = 5 and n = 6. The finrank form is dim ker C = 5 and 9.

**Opposing view (steelman, recorded now).** T1 has 4 unknowns. `linarith`/`nlinarith` with hand-picked multipliers, or plain `decide` over a 129⁴ product, would prove or refute it without any certificate machinery. A certificate checker earns its keep only where kernel `decide` over the full statement is infeasible. So a T1 PASS shows the *workflow* works, not that it was *needed*. Cosmic9's mod-p sketching matters at large size; here the sketch is decorative. The steelman is answered only by the size scaling (T0 n = 5 → 6 → 7) and by the resource figures, not by T1.

## 2. Exact definitions
- **Certificate.** Integer matrices M (m×n) and K (n×k), plus P (n×m), Q (k×n), d ∈ ℤ, with:
  - checkZero: M·K = 0;
  - checkSplit: P·M + K·Q = d·I_n;
  - checkInj: Q·K = d·I_k;
  - d ≠ 0.

  The Lean checkers are Bool-valued functions over `Matrix (Fin _) (Fin _) ℤ` (`!![…]` literals), computed with structurally recursive `sumFin`/`allFin` (so kernel `decide` reduces them). They are proved equal to the Mathlib `∑`/`∀` forms.
- **Soundness (to prove once).** Over ℚ (entries cast), if checkZero ∧ checkSplit ∧ d ≠ 0, then M.mulVec x = 0 ↔ ∃ t, x = K.mulVec t. If checkInj ∧ d ≠ 0, then K.mulVec is injective. Affine version: if M·x0 = b, then M x = b ↔ ∃ t, x = x0 + K t.
- **T1 ACC** (yQ = 1):
  - grav: 6 + 3yu + 3yd + 2yL + ye = 0
  - SU(2)²U(1): 3 + yL = 0
  - SU(3)²U(1): 2 + yu + yd = 0
  - cubic: 6 + 3yu³ + 3yd³ + 2yL³ + ye³ = 0

  Linear block M = [[3,3,2,1],[0,0,1,0],[1,1,0,0]], b = (−6, −3, −2).
- **T0 matrices.**
  - Planar variables X_ab with 1 ≤ a < b ≤ n, b ≥ a + 2, (a, b) ≠ (1, n), in lexicographic order.
  - Mandelstams s_ij with 1 ≤ i < j ≤ n, in lexicographic order.
  - A (C(n,2) × n(n−3)/2) from eq. (10), using cyclic indices and X_{a,a+1} = X_{1,n} = X_{a,a} = 0.
  - C (n × C(n,2)) from eq. (5).
  - A and C are built **independently**; C·A = 0 is a **held-out** consequence (§5).
- **Sketch.** Rank of S·M·T mod p for p ∈ {1000003, 998244353, 2147483647}, with S, T uniform random from `random.Random(SEED)`. The sketch is a randomised rank estimate, never a proof. The exact verify is the proof (in Python, and again in Lean).
- **Deviation from the lit-review wording, declared.** Certificates are over ℤ, which is sound over ℚ. Mod-p is used only for the Python sketch. Mod-p certificates alone do not prove rank over ℚ, so they are not used as proofs.

## 3. Theorem statements (Lean 4 + Mathlib; new module `lean/PositiveGeometryEmergentSpaceTime/LeanCert.lean`, namespace `PositiveGeometryEmergentSpaceTime.LeanCert`; 0 sorry; no native_decide; standard axioms only)
1. `sumFin_eq`, `allFin_iff`: the computable folds equal `∑ i : Fin n` / `∀ i : Fin n`.
2. `checkZero_spec`, `checkSplit_spec`, `checkInj_spec`: Bool check = true ↔ the matrix identity (over ℤ).
3. `kernel_char`: soundness over ℚ as in §2. `leftInv_injective`. `affine_char`.
4. T0: `abhy5_cert`, `abhy6_cert` (all three checks hold, by `decide`), `abhy6_kernel_eq_range`: ker C₆ = range A₆ (as ℚ-submodules / sets), `abhy6_injective`. `abhy6_finrank`: finrank ℚ (ker C₆) = 9 (and `abhy5_finrank` = 5). If the finrank statements resist, they may be dropped to the set/injective form (declared in the result). n = 7 (dim 14) is attempted in Lean as a size-scaling probe only. It is not a pass condition.
5. T1:
   - `gpos_cert` (by decide);
   - `gpos_linear_iff`: the three linear ACC ↔ ∃ t, (yu, yd, yL, ye) = (t, −2 − t, −3, 6), proved **through `affine_char`**, not through linarith;
   - `gpos_cubic_on_line`: the cubic at the line = −18 (t + 4)(t − 2);
   - `nacc_set_eq`: (R⁴).filter ACC = {(−4, 2, −3, 6), (2, −4, −3, 6)};
   - `nacc_eq_two`: card = 2.
6. Planted (Lean):
   - `planted_flip_rejected`: checkZero M (K with one entry flipped) = false, by decide;
   - `planted_split_rejected`: a corrupted P is rejected;
   - `planted_abhy_flip_rejected`: the same for A₆;
   - `planted_tuple_rejected`: (−4, 2, −3, 7) ∉ the ACC set.

If a statement needs re-wording to compile, the change is declared in the result, never hidden. If no correct re-wording exists, the statement is reported FAILED, and the verdict follows §6.

## 4. Foregone / contamination (declared)
- T1 is **FOREGONE as a fact**. GPOS-2026-10-22-r1 already lists the two solutions. The hand algebra was done during planning, before this prereg:
  - particular solution x0 = (0, −2, −3, 6);
  - kernel (1, −1, 0, 0);
  - cubic on the line = −18(t² + 2t − 8).
  
  The rung tests the *upgrade path* (certificate → PROVED within budget), not the fact.
- T0 dimensions are CITED (ABHY eq. 6), so they are foregone.
- **Smoke test, declared.** Before locking, `run_planted` was executed once in /tmp from a guard-stubbed copy, to catch crashes (all PL1–PL8 OK; PL8 linear-only count printed). After that, the guard was removed from the pure predicate `acc_ok`, for speed only, since it is called about 2·10⁶ times inside guarded functions. No live-mode function was run.
- **Not foregone:**
  - whether kernel `decide` on the n = 6 / n = 7 certificates fits the budget;
  - the sketch = exact agreement;
  - the held-out C·A = 0 check at n = 7;
  - whether the soundness theorem plus `decide` reaches the R⁴ statement without native_decide or new axioms.

## 5. Predictions (written before running)
Python:
- Planted all OK: 97%.
- T0 certificates verify with d = 1 at n = 5, 6, 7: 60%; with some d > 1: 35%.
- Held-out C·A = 0 at n = 5, 6, 7: 97% (eq. 10 is built to solve eq. 5; failure would mean my index convention is wrong, which is ILL-DEFINED, not a kill).
- dim ker C = n(n−3)/2 (5, 9, 14): 97%.
- Sketch rank = exact rank at all three primes: 99%.
- T1 recount = 2 and the line roots are exactly {−4, 2}: 99%.

Lean:
- Module compiles with 0 sorry and standard axioms: 80%.
- n = 6 `decide` within 10 min: 85%.
- n = 7 within 1 h and < 15 GB: 65%.
- `abhy6_finrank` stated as planned: 70%.
- `gpos_linear_iff` through `affine_char` (no linarith shortcut for the linear part): 85%.
- Whole module < 1 h and < 15 GB: 85%.

Verdict: **UPGRADED (T1 PROVED, T0 reproduced PROVED): 75%**; PARTIAL: 17%; LIMIT: 6%; FAIL: 2%.

## 6. Pass / fail / kill criteria
- **ILL-DEFINED:** any Python planted case fails, or held-out C·A ≠ 0 at n = 5 or 6. Then live is not scored and the index convention is audited.
- **KILL → LIMIT (result stays SIMULATED):** the Lean module needs > 1 h wall time, > 15 GB peak RSS, `native_decide`, `Lean.ofReduceBool`, or any non-standard axiom for T1 or T0 n ≤ 6. Measured with `/usr/bin/time -v` on `lake env lean PositiveGeometryEmergentSpaceTime/LeanCert.lean`. An n = 7 overrun alone is recorded as LIMIT-at-n=7 and is not a kill.
- **FAIL:**
  - Lean proves T1 false (N_ACC ≠ 2 on R⁴); this would also falsify GPOS-r1;
  - a planted wrong certificate or tuple is ACCEPTED by the Lean or Python checker;
  - Python T1 recount ≠ 2.
- **UPGRADED:** `nacc_eq_two` and `nacc_set_eq` compile; T0 n = 6 compiles; all Lean planted theorems compile; AxiomsAll nonstandard = 0, sorry_dependent = 0. GPOS N_ACC moves SIMULATED → PROVED.
- **PARTIAL:** T1 compiles but some T0 or planted statement is dropped or re-worded beyond §3's allowance, or `gpos_linear_iff` needed a non-certificate shortcut (declared).

## 7. Planted-answer test (list in `sims/leancert1/planted_cases.json`)
Python:
- PL1: known kernel and certificate.
- PL2: a flipped kernel entry is REJECTED.
- PL3: a corrupted P is REJECTED.
- PL4: a fake extra kernel vector is REJECTED.
- PL5: ABHY n = 4 eq. (10): s12 = X13, s23 = X24, s13 = −X13 − X24.
- PL6: the sketch detects a rank-2 3×3 matrix.
- PL7: wrong tuple (−4, 2, −3, 7) rejected; SM tuple accepted.
- PL8: dropping the cubic gives count > 2 (detector power).

Lean: the four `planted_*` theorems of §3.6.

## 8. Simulation plan
Run id `LEANCERT1-2026-10-23-r1`, seed `20261023` (PL6 uses seed+6). Modes: `planted`, then `live` (live only if planted is ALL OK).
- Live T0: n = 5, 6, 7. Sketch, then exact rref, the certificate and the verify. Then emit `sims/leancert1/certs_lean.txt` (the Lean literals pasted verbatim into `LeanCert.lean`).
- Live T1: x0, kernel, certificate, the cubic on the line and its rational roots, and the independent brute-force recount over R⁴ (iterating (yu, yd, yL) ∈ R³, deriving ye from grav, testing ye ∈ R and all four ACCs).
- Lean build: `/usr/bin/time -v lake env lean PositiveGeometryEmergentSpaceTime/LeanCert.lean`, with wall time and max RSS recorded in `sims/leancert1/lean_build_time.txt`. Then the axioms file and AxiomsAll.
- **Figure** (post-run, reads JSON + time file only): Lean check time and RSS against matrix size (n = 5, 6, 7) and the T1 line cubic with its roots.
- Negative results are kept.

## 9. Data tiers
- Tier 0 (mathematics): ABHY 1711.09102 (CITED, fetched); repo GPOS run (SIMULATED).
- No experimental data. No data-credit moves.

## 10. Pinned environment
- Python 3.13.5 (`<local path>`; the checker uses stdlib only: fractions, random, math).
- Lean `leanprover/lean4:v4.34.1`, Mathlib rev `d13f23b723b8a846827a245b89c10fc7d3f11612`.
- Box: 8 CPU, 15 GB, no GPU. CPU only.
- Figure: `<local path>`.

## 11. Guard and run manifest
- Hardened guard, copied from `sims/int1`. git fetch once per process. The prereg add-commit must be an ancestor of origin/main. The checker sha256 must match the line below. `guard` is called in every scoring function (`matmul`, `rref`, `kernel_basis`, `solve_left`, `split_cert`, `verify_cert`, `rank_mod_p`, `sketch_rank`, `abhy_matrices`, `gpos_domain`, `gpos_recount`, `gpos_line`, `cubic_on_line`, `run_planted`, `run_live`). There is no pass flag.
- The import test must REFUSE before the push; its output is saved to `sims/leancert1/guard_refusal.txt` (own commit).
- Run manifest (result commit):
  - `sims/leancert1/{leancert1_planted.txt, leancert1_output.txt, leancert1_live.json, certs_lean.txt, lean_build_time.txt}`
  - `lean/PositiveGeometryEmergentSpaceTime/LeanCert.lean`, `lean/axioms/LeanCert_axioms.lean`, `lean/axioms/LeanCert_output.txt`, `lean/AxiomsAll_output.txt`
  - `figures/leancert1-2026-10-23.png`, `reviews/LEAN-CERT-1-result-2026-10-23.md`
  - ledger/glossary/graph/blueprint/BACKLOG/blocker/AXIOMS updates

## 12. What remains untested (by design)
- Certificates for non-linear facts. The cubic step is a hand factorisation checked by `ring`, not a certificate.
- Mod-p certificates with rational reconstruction (Cosmic9's actual pipeline). Here the exact certificate is computed directly, because the sizes are tiny.
- Any matrix larger than 21×21. The scaling claim beyond n = 7 stays CONJECTURE.
- Whether other SIMULATED repo results (INT-1 n = 6 data, FL-1Z) admit the same upgrade.

Locked:
- `sims/leancert1/leancert1_checker.py` sha256 `013715682a6af2f9a4530f57ba3b089635d0f5c888c5842a25d5cbf2cb80bc7b`
- `sims/leancert1/planted_cases.json` sha256 `beb3c156f4428264e3120928c09372d84dbf19bae193e7be4c7aacd729526e9f`
- `sims/leancert1/import_guard_test.py` sha256 `c574f8d54845a5885a5ce41857a86cfc84caa5b41e5d73cfd39d8b9cea88315b`
