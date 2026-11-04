# JORD-1 result: ILL-DEFINED (locked F_A consistency check failed on a checker scaling defect); tier-A NO-GO PROVED in Lean independently
Written 2026-10-28 by Grok. **Rung 1 of 3 (exploration slot), AutoResearch own pick under "Unpause AutoResearch for 3 rungs" (author approved 2026-10-28).** STOP removed in 05107da; AUTORESEARCH-STOP is re-committed alone after rung 3.

Verdict: ILL-DEFINED
Run id: JORD1-2026-10-28-r1 (seed 20261028; the only run id; the three modes were re-run once under the same id after a host-restart interruption, outputs identical, see §6)
Failure-mode: FM-SPEC

- Prereg: `prereg/JORD-1-positivity-closure-2026-10-28.md`, commit 719e85d, pushed alone 2026-10-28 (not edited since).
- Guard refusal: commit ec7120f (`sims/jord1/guard_refusal.txt`): CLI rc=1 and import test rc=2 before the push; after the push every scoring call printed "GUARD OK: prereg 719e85d63 on origin/main; checker hash matches".
- Locked checker: `sims/jord1/jord1_checker.py`, sha256 3179e353…602a8 (= prereg §6; unchanged).
- Run outputs + Lean checkpoint: 79a4df2, 6644a04 (pushed 2026-10-28).
- Credit: 0 (proposal). No ledger value moves; the scored verdict is ILL-DEFINED. CREDITS.md not edited.

Tags: PROVED = Lean theorem, 0 sorry, no native_decide, standard axioms only. SIMULATED = exact Python, run id above. CITED = arXiv abstract checked (prereg §1; 2606.15235, 1911.13124, 1912.11282 re-opened on export.arxiv.org 2026-10-28 ≈). CONJECTURE / SPECULATION as stated.

## 1. Verdict and why
Prereg §3: ILL-DEFINED if any planted case fails, any valid alternative is rejected, any broken case is accepted, **or the F_A consistency check fails**. Planted P1–P8 ALL OK, V1–V3 accepted, B1–B3 rejected. F_A failed: `FA_all_idempotent = false`, so the locked rule returns ILL-DEFINED.

**Post-hoc diagnosis (not scoring; `sims/jord1/posthoc_diag_idempotent_scale.py`, written after the live run, imports the locked checker; output `posthoc_diag_out.txt`):** of the 51 declared idempotents, 48 pass and exactly E1, E2, E3 fail. The checker's `idempotents` lists E1–E3 as unit vectors while P_ij(±e_k) are listed at the 2P scale that `is_idempotent2` (which tests 2X∘X = 2X at the 2× product scale) expects; E1–E3 pass when doubled. So the defect is a unit convention inside the checker's consistency gate, not a mathematical inconsistency. Every other F_A number is independent of that flag: 1326 configs, stabiliser-dim histogram {21: 1200, 28: 75, 36: 51}, **SM-type hits 0** (which is what the Galois lemma requires when tier A is NOT-POSITIVITY-CLOSED).

Unscored conditional reading (would be the verdict string had the gate passed; NOT the verdict): NOT-POSITIVITY-CLOSED / CHOICE-UNIQUE / NO-GO.

## 2. Python run (SIMULATED JORD1-2026-10-28-r1)
- **Planted:** P1 Fano table composition + alternativity OK; P2 dim Der h3(O) = 52 (lower = upper = 52); P3 dim stab(E1) = 36; P4 dim stab(E1,E2,E3) = 28; P5 dim setstab(h3(C)) = 16; P6 g_sm subalgebra, invariants (12,4,1,11), type A1+A2+u1; P7 setstab(X) ∩ setstab(B) = g_sm; P8 Der h3(R/C/H) = 3/8/21. V1 (u = e2), V2 (stab(E2+E3) = stab(E1)), V3 (rank seed+1) accepted.
- **Broken:** B1 (e1e2 = e2e1 = e4 table), B2 (dim stab(E1) = 52), B3 (D = E_00) all rejected.
- **Tier A (scored):** Fix(g_sm) = span{E1, E2+E3} (dim 2); closure(g_sm) = stab(Fix) has invariants (36, 4, 0, 36), type candidates B4/C4, and equals stab(E1) as a subspace. 36 > 12 ⇒ NOT-POSITIVITY-CLOSED. Matches the disclosed prior (CONJECTURE ~85–90 %).
- **Tier B (label):** F_B = 18 configs; exactly one is SM-type: X = h2(C) ⊂ B = h3(C) (12, 4, 1, 11; A1+A2+u1). Label CHOICE-UNIQUE. Others e.g. X = h2(R) ⊂ h3(C): 10 (A2+u1²); X = h2(C) ⊂ h3(O): 18; B = h3(C) only: 16 (A2+A2, su3⊕su3); X = h2(O) ⊂ h3(O): 36 (spin(9)); B = h3(O) only: 52 (F4).
- **Null rates (no tuning):** closed fraction 3/18; SM-type fraction 1/18. Within the declared family the SM structure is one choice of 18 and is itself not closed (closure 36).
- **Rival R-J (Krasnov 1912.11282, report only):** the four declared J variants on V_½(E1) give LL, RR, RL = (10, 4, 2, 8) A2+u1² and LR = (22, 4, 1, 21) B3/C3+u1; **none equals g_sm**. This is SIMULATED about our encoding of J (L_e1 / R_e1 per octonion block), not a refutation of Krasnov: his J is a specific complex structure on O² that our four variants evidently do not contain (FLAG F2). The (10, …) value coincides with tier-B config X = h2(R) ⊂ h3(C), a consistency cross-check of the code paths.
- Resources (re-run, watchdog): planted 7.0 s / 90 MB; broken 2.0 s / 22 MB; live 110 s / 45 MB.

## 3. Lean (module `PositiveGeometryEmergentSpaceTime.Jord1`: Table / Alg / Data / Gens / NoGo)
PROVED, 0 sorry, no native_decide, all kernel checks by `decide +kernel`:
- `PositiveGeometryEmergentSpaceTime.Jord1.bc_eq_jprod` (the literal table equals the product computed from the Fano lines), `isDer_of_derS` (sparse check ⇒ derivation over ℚ), `presB_of`, `mulVec_E1_of`.
- `gen0_ok` … `gen11_ok`, `gens_ok`, **`gen_mem_gsm`** (each of the 12 integer generators from the live run lies in g_sm = stab(E1) ∩ setstab(h3(C))).
- `W_tpos`, `W_derS`, **`W_isDer`**, **`W_not_presB`** (W is a derivation not preserving h3(C)); `selOK_true`, `Rsel_kills`, `certW_true`, `certW_int` (row-span certificate 2·W = Cm·Rsel), **`W_kills_fix`** (W kills every vector fixed by all 12 generators).
- **`PositiveGeometryEmergentSpaceTime.Jord1.gsm_not_pointwise_stabiliser : ¬ ∃ S : Set (Fin 27 → ℚ), stab S = gsm`** — g_sm is not the pointwise stabiliser (in Der h3(O) over ℚ) of any subset S of h3(O). It needs only gen_k ∈ g_sm, not that they span it, so it does not depend on the checker's F_A flag or on the SIMULATED dimension 12.
- Scope: "positivity-native" is read through the Galois lemma (prereg §2, on paper): any set of cone points/faces is a subset S, so the theorem covers them a fortiori. Lean does not prove dim closure = 36 or closure = spin(9); those stay SIMULATED.
- Resources (LEAN_NUM_THREADS=1, one module at a time, anon-RSS watchdog 3.5 GB): Table 3 s; Alg 42 s / 2682 MB; Gens 76 s / 1264 MB; NoGo 7 s / 765 MB. `lake build PositiveGeometryEmergentSpaceTime.Jord1 PositiveGeometryEmergentSpaceTime` green (9096 jobs).
- Axioms: the key theorems use [propext, Classical.choice, Quot.sound]. Fresh `lean/AxiomsAll_output.txt` (mktemp copy, 378 s, 571 MB anon): **TOTAL theorems=1062 defs=584 nonstandard=0, sorry_dependent=0** (was 1027/538; +35 thm, +46 def, all in Jord1).

## 4. Declared deviations
- **D1 (Lean names).** Prereg §4 sketched `gen_k_isDer`, `W_not_setstab`; the module uses `gen0_ok…gen11_ok` + `gen_mem_gsm` and `W_not_presB` (same statements).
- **D2 (interruption).** The host restarted mid-rung (last file write, later than the ≈20:48 first estimated). All three modes were re-run through the guard 21:53–; outputs identical to the pre-interruption files ('seconds' excluded). `sims/jord1/run_record.txt`.
- **D3 (watchdog field).** The first Lean watchdog measured VmRSS (includes mmapped Mathlib oleans) and killed runs at 3.7–4.2 GB; switched to RssAnon to match the prereg's "anon RSS". Nothing was claimed from killed attempts.
- **D4 (network).** GitHub TLS failed ≈22:05–; local commits waited and were pushed after `git fetch` + `pull --ff-only` succeeded.
- **D5.** `emit_lean.py` (data formatter of the locked live output) and the post-hoc diag are not scoring functions.

## 5. Steelman and answer
- **Steelman.** The rung is ILL-DEFINED by its own rule; the "NO-GO" was the stated prior; and "G_SM is not a pointwise stabiliser" is close to obvious once one notices Fix(g_sm) is just span{E1, E2+E3}.
- **Answer.** Conceded on the score. What is new: a kernel-checked theorem over ℚ that the Todorov/Baez–Schwahn g_sm is not the stabiliser of any set of points of h3(O) (hence of no cone points or faces), and a SIMULATED audit that within the declared 18-config family the SM type appears exactly once and is not closed. The positivity structure of h3(O) alone does not single out G_SM; the h3(C) sub-algebra (equivalently a complex structure) is an input. That is the TAUT edge the trade-space note predicted, now on record, but it earns nothing because the scored gate failed.

## 6. Ledger, blockers, reopen
- **Exclusion (row added):** `Jord1.gsm_not_pointwise_stabiliser` — rules out "the SM gauge algebra as a positivity-native (pointwise-stabiliser) structure of the exceptional Jordan cone"; the h3(C)/complex-structure choice is input.
- **Blocker:** JORD-1 `ILL-DEFINED`, FM `FM-SPEC`. Reopen triggers: (i) a superseding checker v2 (fixed idempotent scale) under a new prereg — PROPOSED, not run in this batch (its outcome is already known from the diag: it would only convert the label); (ii) a positivity-native reason (not a choice) for the complex structure J / h3(C); (iii) a faithful encoding of Krasnov's J (rival fidelity).
- **Credit:** 0 (proposal).

## 7. Flags
- **F1.** Locked-rule ILL-DEFINED from a checker unit convention (second FM-SPEC rung in a row on main after LEAN-CERT-2). METHOD lesson added.
- **F2.** Rival R-J as encoded does not reproduce g_sm; likely an encoding gap, not a Krasnov refutation.
- **F3.** Lake warns the mathlib package (symlinked from br-wt-review) "has local changes" (pre-existing; not touched).
- **F4.** Proposed basin B7 (Jordan-cone positivity) is not yet in `scripts/blocker_tags.py` BASIN (PositiveGeometryEmergentSpaceTime's map); proposed in the handoff deltas.
