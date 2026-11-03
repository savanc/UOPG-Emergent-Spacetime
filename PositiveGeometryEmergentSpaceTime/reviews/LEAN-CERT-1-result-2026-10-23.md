# LEAN-CERT-1 result: UPGRADED. GPOS N_ACC = 2 moves from SIMULATED to PROVED; ABHY dim K_n reproduced as PROVED for n = 5, 6, 7
Written 2026-10-23 by Grok. The author-directed manual frontier rung (author approved 2026-10-23). Not AutoResearch (paused, untouched).

- Prereg: `prereg/LEAN-CERT-1-certificate-upgrade-2026-10-23.md`, commit 689d929, pushed alone and ff-only.
- Guard refusal: commit 3fc8fc1 (`sims/leancert1/guard_refusal.txt`). There were 5/5 import calls REFUSED plus a CLI refusal before the push. After the push the guard reported OK.
- Run: `LEANCERT1-2026-10-23-r1`, seed 20261023. Planted mode ran first (ALL OK), then live mode.
- Credit: 0. This is a method rung. No physical datum enters.

Tags: PROVED means a Lean theorem, 0 sorry, standard axioms. SIMULATED(run id) means exact Python. CITED means fetched this rung. CONJECTURE and SPECULATION are as usual.

## 1. Verdict
**UPGRADED** (prereg §6). All of the following hold:
- `nacc_eq_two` and `nacc_set_eq` compile.
- T0 n = 6 compiles. n = 7 compiles as well.
- All 4 Lean planted theorems compile.
- AxiomsAll: nonstandard = 0, sorry_dependent = 0.
- No kill fired: the module took 10.2 s wall time against a 3600 s limit, peaked at 6.8 GB RSS against 15 GB, and uses no native_decide and no `Lean.ofReduceBool`.

## 2. What was proved (Lean module `PositiveGeometryEmergentSpaceTime.LeanCert`: 40 source theorems and 42 defs/instances; AxiomsAll counts 42 thm because it includes the 2 auxiliary eq lemmas `sumFin.eq_2` and `allFin.eq_2`)
**Checker and soundness (PROVED).** These are proved once and can be reused for any integer certificate.
- `sumFin_eq` and `allFin_iff` show the structural folds equal `∑` and `∀`.
- `mulE_eq`, `checkZero_spec`, `checkSplit_spec`, `checkInj_spec` and `checkEq_spec` show each Bool check is true iff the matrix identity holds over ℤ.
- `cq_mul`, `cq_smul_one` and `cq_add` handle the cast to ℚ.
- `kernel_char`: if MK = 0, PM + KQ = d·1 and d ≠ 0, then Mx = 0 ⇔ x ∈ range K.
- `leftInv_injective`: QK = d·1 and d ≠ 0 imply K is injective.
- `affine_char`: if Mx₀ = b, then Mx = b ⇔ x = x₀ + Kt.
- `ker_eq_range` and `finrank_ker`: finrank ker M = k.

**T0, the known-result reproduction (PROVED, in this repo's encoding).** It follows ABHY 1711.09102 eqs. (5), (6) and (10) (CITED, fetched 2026-10-23).
- `abhy5_matrices`, `abhy6_matrices` and `abhy7_matrices`: the pasted literals equal the Lean-side generators `eq5` and `eq10`. This is checked by `checkEq` and `decide +kernel`, so the literals cannot be transcription errors.
- `abhy{5,6,7}_cert` hold by `decide +kernel`.
- `abhy6_kernel_eq_range`: ker C₆ = range A₆.
- `abhy6_injective`.
- `abhy6_conservation`.
- **`abhy5_finrank` = 5, `abhy6_finrank` = 9 and `abhy7_finrank` = 14.** These equal n(n−3)/2, which is ABHY eq. (6).

**T1, the upgrade (PROVED).**
- `gpos_cert`.
- `gpos_linear_iff`: the three linear ACC hold ⇔ ∃ t, (yu, yd, yL, ye) = (−2 − t, t, −3, 6). This goes through `affine_char`.
- `gpos_cubic_on_line`: the cubic on the line equals −18(t + 4)(t − 2).
- `acc_iff`, over **all of ℚ⁴**: ACC ⇔ (2, −4, −3, 6) or (−4, 2, −3, 6).
- `nacc_set_eq`: (R⁴).filter ACC = {(−4, 2, −3, 6), (2, −4, −3, 6)}.
- **`nacc_eq_two`: card = 2.**
- The Lean result is stronger than the SIMULATED statement. The restriction to the finite domain R⁴ is not needed: there are exactly 2 rational solutions at yQ = 1.

**Planted (PROVED REJECTED).**
- `planted_flip_rejected`: a K entry flipped gives checkZero = false.
- `planted_split_rejected`: a corrupted P gives checkSplit = false.
- `planted_abhy_flip_rejected`: the same for A₆.
- `planted_tuple_rejected`: (−4, 2, −3, 7) ∉ accSet.

**Axioms** (`lean/axioms/LeanCert_output.txt`). Every theorem uses a subset of {propext, Classical.choice, Quot.sound}.
- The `decide +kernel` certificate theorems use [propext, Quot.sound] only.
- `allFin_iff` uses [propext].
- AxiomsAll (`lean/AxiomsAll_output.txt`, fresh): **TOTAL theorems=937 defs=443 nonstandard=0, sorry_dependent=0**. That is 895/401 + LeanCert 42/42. Lines for other modules are byte-identical to before.
- There is no `sorry`, `native_decide`, `axiom` or `ofReduceBool` in the module.

## 3. Python run (SIMULATED LEANCERT1-2026-10-23-r1)
- **Planted:** PL1–PL8 ALL OK (`sims/leancert1/leancert1_planted.txt`). PL8 shows detector power: dropping the cubic gives a count of 63.
- **T0 for n = 5/6/7:**
  - **Held-out C·A = 0: true at all three n.**
  - Exact dim ker C = 5/9/14.
  - The sketch ranks are C = 5/6/7 and A = 5/9/14 at all 3 primes, so sketch = exact.
  - Certificates verify with **d = 2**. Each takes < 0.06 s.
- **T1:**
  - x₀ = (−2, 0, −3, 6) and kernel (−1, 1, 0, 0), with d = 1.
  - The cubic on the line has coefficients (144, −36, −18, 0) and roots {−4, 2}.
  - |R| = 127.
  - **Independent recount: N_ACC = 2**, with solutions (−4, 2, −3, 6) and (2, −4, −3, 6).
- Python verdict: CERTS-VERIFIED.

## 4. Resources (SIMULATED; `sims/leancert1/lean_build_time.txt`, `per_n_probe.json`; figure `figures/leancert1-2026-10-23.png`)
- **Whole module:** `lake env lean PositiveGeometryEmergentSpaceTime/LeanCert.lean` took 10.2 s wall time at 6.82 GB peak RSS. The ~4 s Mathlib import dominates the wall time and most of the RSS.
- **`lake build PositiveGeometryEmergentSpaceTime.LeanCert`:** 20.1 s, 6.84 GB.
- **Per-certificate kernel type-check** of the `decide +kernel` re-check, median of 3:

| Certificate | Kernel type-check (s) |
|---|---|
| gpos (3×4) | 0.015 |
| n = 5 (C 5×10, A 10×5) | 0.20 |
| n = 6 (6×15, 15×9) | 0.69 |
| n = 7 (7×21, 21×14) | 2.16 |

- The log–log slope against N = C(n, 2) is **3.22**, fitted from 3 points.
- **CONJECTURE:** extrapolating N^3.2 reaches the 1 h kill near N ≈ 215 Mandelstams (n ≈ 21). Memory has not yet been seen to grow beyond the import baseline.

## 5. Predictions vs outcome
| Prediction | p | Outcome |
|---|---|---|
| Python planted ALL OK | 97% | yes |
| T0 d = 1 / some d > 1 | 60% / 35% | **d = 2** (the 35% branch) |
| held-out C·A = 0 | 97% | yes |
| dim ker C = 5, 9, 14 | 97% | yes |
| sketch = exact | 99% | yes |
| T1 recount 2, roots {−4, 2} | 99% | yes |
| module compiles, 0 sorry, std axioms | 80% | yes |
| n = 6 decide < 10 min | 85% | yes (0.7 s) |
| n = 7 < 1 h, < 15 GB | 65% | yes (2.2 s) |
| `abhy6_finrank` as planned | 70% | yes (plus n = 5 and n = 7) |
| `gpos_linear_iff` via `affine_char` | 85% | yes (see deviation D3) |
| whole module < 1 h, < 15 GB | 85% | yes |
| verdict UPGRADED | 75% | **UPGRADED** |

## 6. Declared deviations
- **D1 (meter).** `/usr/bin/time` is not installed on the box. `sims/leancert1/timed_build.py` uses `resource.getrusage(RUSAGE_CHILDREN).ru_maxrss` for the peak RSS of the waited-for subprocess tree, plus wall clock, with a 3600 s timeout. The 15 GB and 1 h thresholds were applied unchanged.
- **D2 (line parametrisation).** Prereg §3.5 wrote the line as (t, −2 − t, −3, 6). The certificate's kernel is (−1, 1, 0, 0) with x₀ = (−2, 0, −3, 6), so Lean states (−2 − t, t, −3, 6). The two are the same set under t ↦ −2 − t. The prereg's planning x₀ = (0, −2, −3, 6) (§4) is a different particular solution on the same line. This falls under the §3 re-wording allowance and is declared here.
- **D3 (rearrangement).** In `gpos_linear_iff`, `linear_combination` is used only to rewrite each ACC equation into the `M *ᵥ x = b` row form (one equation at a time, no elimination). The solution set comes from `affine_char` with the certificate. I do not count this as the "non-certificate shortcut" of §6 PARTIAL. A stricter reader could, and that reader would score PARTIAL, not UPGRADED.
- **D4.** The cubic step is `ring` on a hand factorisation, as the prereg §12 already declared.
- **D5.** `per_n_probe.py` and `make_figure.py` are post-run additions. They read run outputs and re-time the existing certificates. They are not scoring functions and are not guarded.
- **D6.** Three `unnecessarySeqFocus` linter warnings remain (lines 298, 301, 324). They are cosmetic.

## 7. Steelman (opposing view) and answer
- **Steelman.** T1 never needed the machinery. `nlinarith` or a hand elimination proves the 4-variable linear system, and the PROVED N_ACC = 2 is a textbook SM fact. The sketch is decorative at these sizes, since exact rref takes < 0.06 s. T0 is reproduced only for n ≤ 7 and only for *this repo's encoding* of eqs. (5)/(10). The "= ABHY" link is the CITED reading of those equations, which is not formalised. A general-n theorem dim K_n = n(n−3)/2 is not proved. So the rung shows a workflow on toy sizes, not a capability.
- **Answer.** Mostly conceded.
  - The gain is the reusable, proved-once soundness layer plus a measured cost curve (slope ≈ 3.2, 2 s at 21×14).
  - The rung also shows that the kernel-`decide` route (no `native_decide`) stays seconds-scale through n = 7.
  - Upgrading T1 removes one SIMULATED dependency from the GRADED-POSITROID NO-GO.
  - The steelman's point stands that no repo result yet *requires* certificates. That would need a SIMULATED linear-algebra fact at N in the hundreds.

## 8. Status moves
- **SIMULATED → PROVED:** GRADED-POSITROID N_ACC = 2 (GPOS-2026-10-22-r1 `count_full_acc`) → `PositiveGeometryEmergentSpaceTime.LeanCert.nacc_eq_two` / `nacc_set_eq`, strengthened to all of ℚ⁴ by `acc_iff`.
- **CITED → PROVED (repo encoding):** ABHY dim K_n = n(n−3)/2 for n = 5, 6, 7, together with ker(eq. 5) = range(eq. 10) at n = 6.
- **Unchanged:**
  - INT-1 n = 6 chamber data (SIMULATED; not linear algebra of this kind);
  - FL-1Z observables (SIMULATED, numerical);
  - all credit.

## 9. What it means for the mission gaps
- **P1–P5 physics gaps: no change.** This rung adds no physical number and moves no credit.
- **Method gap (the SIMULATED → PROVED backlog):** there is now a reusable integer-certificate path for exact linear-algebra facts. Candidates must be ranks or kernels of integer or rational matrices. Measured budget: seconds up to ~21×21, and an N^3.2 extrapolation (CONJECTURE) gives roughly N ≈ 200 before the 1 h kill.
- **The GRADED-POSITROID NO-GO now rests on PROVED counts.** Before, it combined a Lean equivalence (`graded_cubic_iff_acc`) with a SIMULATED count. Its simplex-rival κ values remain SIMULATED.
- **SPECULATION:** the same path could certify CASCADE-1's constraint-count ranks, which are integer linear systems, if those are small.

## 10. What remains untested
- Certificates for non-linear facts. The cubic is still `ring` on a hand factorisation.
- Mod-p certificates with rational reconstruction (Cosmic9's actual pipeline). The exact certificate here was computed directly.
- Any matrix larger than 21×21. The scaling beyond n = 7 is CONJECTURE, from 3 points.
- A general-n Lean theorem for dim K_n.
- Whether other SIMULATED repo results admit the same upgrade (INT-1 n = 6, the GPOS κ values).
- Whether larger certificates stress memory (here RSS ≈ the import baseline).

## 11. Manifest
- `sims/leancert1/{leancert1_checker.py (locked), planted_cases.json (locked), import_guard_test.py (locked), guard_refusal.txt, leancert1_planted.txt, leancert1_output.txt, leancert1_live.json, certs_lean.txt, timed_build.py, lean_build_time.txt, per_n_probe.py, per_n_probe.json, make_figure.py}`
- `lean/PositiveGeometryEmergentSpaceTime/LeanCert.lean`, `lean/PositiveGeometryEmergentSpaceTime.lean` (import), `lean/axioms/LeanCert_axioms.lean`, `lean/axioms/LeanCert_output.txt`, `lean/AxiomsAll_output.txt`
- `figures/leancert1-2026-10-23.png`
- Environment: Lean v4.34.1, Mathlib d13f23b7; Python 3.13.5 (`<local path>`); figure via `<local path>`. CPU only, 8 CPU / 15 GB box.
