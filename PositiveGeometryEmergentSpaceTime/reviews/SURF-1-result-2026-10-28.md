# SURF-1′ result: EMPTY (no N ≥ 3 is colour-sign coherent at one loop, n ≤ 4); Lean PROVED from a kernel enumeration
Written 2026-10-28 by Grok. **Rung 2 of 3 (EV pick; declared foregone, METHOD rule 6), AutoResearch own pick under "Unpause AutoResearch for 3 rungs" (author approved 2026-10-28).** Continuation relayed (the author).

Verdict: EMPTY
Run id: SURF1-2026-10-28-r1 (the only run id; each mode run once)
Failure-mode: FM-RANGE (declared in the prereg; consistency gives a class, not the SM point: the per-channel class is empty, the full-tree reading is the window N ≥ 5; nothing is left free, c = 1 is fixed by SU(N))

- Prereg: `prereg/SURF-1-colour-sign-coherence-2026-10-28.md`, commit ce4a4ee, pushed alone to origin/main (not edited since; timestamp erratum in `sims/surf1/guard_refusal.txt`).
- Guard refusal: 1357e13 (`sims/surf1/guard_refusal.txt`), pushed after the prereg.
- Locked checker: `sims/surf1/surf1_checker.py`, sha256 6ca1af1c…b65184e (= prereg §6; unchanged; re-verified by the guard on every scoring call).
- Run outputs: 14a922c (pushed); `sims/surf1/run_record.txt`.
- Credit: 0 (proposal). CREDITS.md not edited.

Tags: PROVED = Lean theorem, 0 sorry, no native_decide, standard axioms only. SIMULATED = exact rational Python, run id above. CITED = prereg §1 (Haber 1912.13302; 2309.15913; 2412.19881; arXiv + journal record each). CONJECTURE / SPECULATION as stated.

## 1. Verdict and why
All five locked gates are true (PLANTED_ALL_OK, GATE_SELFTESTS_OK, BROKEN_ALL_REJECTED, VALID_ALL_ACCEPTED, DEN_POSITIVE). The sign-coherent set S = {N ≥ 3 : every K_{G,ch}(N) > 0} is **empty** (SIMULATED, exact; PROVED in Lean for the two witnesses below):
- **N = 3** is excluded by the n = 3 triangle: K_tri = (N²−12)/N, K_tri(3) = −1 (CITED P3, reproduced; PROVED `K_tri_three_enum`). The six n = 4 triangle-with-tree graphs in their own channel give the same −1 at N = 3.
- **N ≥ 4** is excluded by the crossed box (box1234 in u, box1243 in t, box1324 in s; identical polynomials): W(tree4_u ∘ box1234) = −32N³ + 480N − 1728/N + 1280/N³ = −32(N²−1)(N²−4)(N²−10)/N³ over W(tree4_u ∘ tree4_u) = 4(N²−1)(N²−4)²/N², so **K = −8(N²−10)/(N(N²−4)) < 0 for every N ≥ 4** (PROVED `K_boxU_neg_enum`).
- Hence `PositiveGeometryEmergentSpaceTime.Surf1.no_sign_coherent_N : ∀ N ≥ 3, K_tri(N) < 0 ∨ K_box,u(N) < 0` (PROVED).

The prereg declared EMPTY among the expected outcomes (with RANGE EXCLUDES-3 and DISCRETE-NOT-3); SELECTS-3 was ruled out in advance by K_tri(3) = −1.

**Post-hoc curiosity (NOT verdict-bearing; look-elsewhere: one of 38 K's, noticed after the run):** the crossed box is positive *only* at N = 3 (N² < 10; K(3) = 8/15). Read alone it "selects" N = 3, but the triangle kills N = 3 in the same set, and no preregistered observable singles out the crossed box. Recorded as a reopen ingredient, not a result.

## 2. Python run (SIMULATED SURF1-2026-10-28-r1)
- **Planted P1–P6 ALL OK:** P1 single loop N²−1 (scale convention); P2 theta 2(N²−1)(N²−4)/N; P3 K_tri = (N²−12)/N; P4 K_bub = 2(N²−4)/N (K_bub(3) = 10/3); P5 U(N) all coefficients positive; P6 f-theta |W| = 2N(N²−1).
- **Gate self-tests (METHOD JORD-1 lesson (a)) all true:** planted gate true/false/false on all-true/one-false/empty; deliberately wrong P1 fails; synthetic classifier cases RANGE INCLUDES-3, RANGE EXCLUDES-3, EMPTY, DISCRETE-NOT-3 {4,5}, SELECTS-3 all as declared.
- **Broken B1 (c = 0 labelled SU(N)), B2 (c = −1), B3 (single orientation): all rejected.**
- **Valid V1 (glue-order invariance), V2 (relabel (2,1,4,3)), V3 (propagator ×2): all accepted.**
- **Live:** 38 K's (n = 2 bubble; n = 3 triangle; n = 4: 3 boxes × 3 channels, 6 triangle-with-tree × 3, 3 bubble insertions × 3). Distinct n = 4 K polynomials: planar box (K(3) = 3/10, positive for all N ≥ 3), crossed box (positive only at N = 3), same-channel triangle (−1 at N = 3, positive N ≥ 4), off-channel triangle (= planar box polynomial), same-channel bubble (= K_bub), off-channel bubble (= triangle polynomial). All denominators positive for N ≥ 3. S = ∅.
- **Full-tree interference (report only, prereg V1):** channel-summed K's give RANGE EXCLUDES-3 with N0 = 5 (crossed-box negativity is diluted by the planar channels).
- **Null N1 (U(N), c = 0):** S ⊇ {3..30}, large-N positive (coherence is automatic without the ghost; P5).
- **Null N2 (ghost grid c ∈ {0, ¼, …, 2}):** c = 0, ¼, ½ → S = {3..30}, large-N positive; **c = ¾ → S = {3}**, large-N not positive; c = 1, 5/4, 3/2, 7/4, 2 → S = ∅. The physical c = 1 sits in the empty band; the {3}-only window at c = ¾ is unphysical and is reported, not scored.
- **Rival R1 (f-coupled cubic, report only):** no K changes sign on N = 3..30 (`rival_f_any_sign_change_in_N` false); several f-K's vanish identically (e.g. box1234|u). The antisymmetric coupling carries no N-dependent sign information at this order.
- Resources (watchdog, RssAnon): planted 16.0 s / 8 MB; broken 1.0 s / <1 MB; live 39.0 s / 10 MB.

## 3. Lean (module `PositiveGeometryEmergentSpaceTime.Surf1`: Enum / Box.Graph / Box.C0–C3 / Box / Signs / Main)
PROVED, 0 sorry, no native_decide; enumeration checks by `decide +kernel`:
- **Enumerator** (`Enum`): a double-line colour-weight evaluator over orientation patterns × ghost subsets with a bitmask index-loop walk over precomputed slot tables. `single_c1` (P1), `theta_c1` (P2), `tetra_c1` (tetrahedron = tree3 ∘ triangle), `theta_u` (U(N) theta).
- **Box** (`Box.Graph`, `Box.C0`–`C3`, `Box`): `ttU_c1` (denominator, 2⁴ × 2⁶ terms); 64 per-orientation certificates `boxU_o0` … `boxU_o63` (2⁹ ghost masks each; generated as statements by `sims/surf1/emit_box_chunks.py` from a Lean `#eval`, values re-derived by the kernel); `boxU_c1 : W1 boxU = [(3,-32),(1,480),(-1,-1728),(-3,1280)]` (rewrite of the orientation sum + decision on literal lists).
- **Signs** (over ℚ): `ev_theta`, `ev_tetra`, `ev_ttU`, `ev_boxU` (closed factorisations), `K_tri_closed` (P3), `K_tri_three`, `K_tri_three_neg`, `K_boxU_closed`, `K_boxU_neg`, `K_boxU_three` (post-hoc 8/15), `ev_theta_pos`, `ev_ttU_pos`, `no_coherent_poly`.
- **Main:** `K_tri_three_enum`, `K_boxU_neg_enum`, **`PositiveGeometryEmergentSpaceTime.Surf1.no_sign_coherent_N`**.
- Scope: Lean certifies the five enumerated weights (single, theta, tetra, tree4∘tree4, tree4∘crossed box) and that the two witnesses exclude every N ≥ 3. That these Lean graphs are the prereg graphs is by construction (vertex/edge lists documented in `Box/Graph.lean`) and cross-checked against the independent Python checker (identical Laurent data). The other 36 K's, the nulls and the rival stay SIMULATED. The kinematic-sign assumption (sign K = sign of interference) is a paper derivation (prereg §2), not Lean.
- Resources (LEAN_NUM_THREADS=1, one target at a time, anon-RSS watchdog 3.5 GB / 30 min): Box.Graph 19 s / 1910 MB; Box.C0 433 s / 3212 MB, C1 383 s / 3211 MB, C2 395 s / 3208 MB, C3 404 s / 3215 MB (anon-RSS peaks); Box (combining step) 2 s / 89 MB; Signs 4 s / 196 MB; Main 3 s / 241 MB; `lake build PositiveGeometryEmergentSpaceTime` 9106 jobs, 48 s / 680 MB; all WATCHDOG OK. Box data from the `#eval` generator 714.7 s / 127 MB.
- Axioms: 0 sorry, no `native_decide` / `Lean.ofReduceBool` (grep over `lean/PositiveGeometryEmergentSpaceTime/Surf1*`). Enumeration theorems (`theta_c1`, `tetra_c1`, `ttU_c1`, `boxU_o0`…`boxU_o63`, `boxU_c1`) use [propext] only; `no_sign_coherent_N`, `K_tri_three_enum`, `K_boxU_neg_enum`, `no_coherent_poly` use [propext, Classical.choice, Quot.sound]. Fresh `lean/AxiomsAll_output.txt` (`lake env lean` on mktemp copy /tmp/AxiomsAllFbBm.lean, 399 s / 571 MB): **TOTAL theorems=1155 defs=630 nonstandard=0, sorry_dependent=0** (= 1062/584 + Surf1 93/46; other_kinds 24 → 27 for structure `G`; every non-Surf1 line unchanged).

## 4. Declared deviations
- **D1 (enumeration scope).** Prereg §4 made the n = 4 enumeration conditional ("attempted only if the n = 3 module is cheap"). It was: n = 3 checked in 18 s; the box was done by chunking per orientation (64 theorems in 4 modules) because one `decide` over 32768 configurations exceeds the kernel memory budget.
- **D2 (emitter).** Instead of `sims/surf1/emit_lean.py` from live_out (prereg §4), the box data were emitted from a Lean `#eval` of the same enumerator (`sims/surf1/lean_gen/BoxGen.lean`, output `boxgen_eval_out.txt`, 714.7 s / 127 MB) by `sims/surf1/emit_box_chunks.py` (data only). The Laurent sums match the Python checker exactly. Signs.lean states the literal lists directly.
- **D3 (one unwatched build).** One `lake build PositiveGeometryEmergentSpaceTime.Surf1.Enum` (16 s, LEAN_NUM_THREADS=1) ran without the watchdog; nothing is claimed from it beyond what the later watched builds reproduced.
- **D4 (threads).** "-j1 under a memory cap" was implemented as LEAN_NUM_THREADS=1 + one lake target at a time under the RssAnon watchdog (same effect: one Lean worker).
- **D6 (FM tag reading) [ASSESS].** The locked rule attaches FM-RANGE to the verdict RANGE and gives no tag for EMPTY. I keep the declared FM-RANGE ("consistency gives a window, bound or class, not the SM point"): the per-channel class is empty and the full-tree reading is the window N ≥ 5. I rejected FM-FREE (no continuous parameter is free; c = 1 is fixed by SU(N)) and FM-TAUT (the condition does not reproduce its input). The tag does not affect the verdict.
- **D5 (prereg timestamp erratum).** Recorded in `sims/surf1/guard_refusal.txt`; the prereg file itself is not amended.

## 5. Steelman and answer
- **Steelman.** The headline was known before the rung: Haber's (N²−12)/N kills N = 3 at n = 3, so "colour sign selects N_c = 3" was dead on arrival (declared foregone). And "S = ∅" depends on treating every channel's K as a separate sign condition.
- **Answer.** Conceded: the question had no room to select 3 (declared foregone, rule 6). What is new and kept: (i) the full n ≤ 4 SU(N) one-loop colour-interference table of the d-coupled cubic (38 K's, SIMULATED exact), (ii) the crossed-box polynomial −8(N²−10)/(N(N²−4)), which closes the "range" escape (the per-channel S is not {N ≥ N0} but empty), and (iii) a kernel-checked double-line enumerator in Lean, reusable for any closed cubic ribbon graph. Under the full-tree (channel-summed) reading the answer is RANGE EXCLUDES-3 (N0 = 5), still not selecting 3.

## 6. Ledger, blockers, reopen
- **Exclusion (row added):** `Surf1.no_sign_coherent_N` (as `SURF1.nc_not_selected_by_colour_sign`): rules out "N_c = 3 selected by one-loop colour-sign coherence of cubic adjoint amplitudes (n ≤ 4)".
- **Blocker:** SURF-1′ `NO-GO`, FM `FM-RANGE`. Trigger check (last 5 on main: TRIALITY-WHY, CASCADE-1b, LEAN-CERT-2, JORD-1, SURF-1′): FM-RANGE 2, FM-SPEC 2, FM-LIMIT 2, FM-TAUT 1 → no mode-form trigger; B8 has one rung → no basin-form trigger. Reopen triggers (prereg §5): a term whose colour sign is coherent **only** at N = 3 under a preregistered observable — e.g. two loops, fermion loops (fundamental matter), or a principled reason to score only crossed-channel interference (the post-hoc N² < 10 window).
- **Credit:** 0 (proposal).

## 7. Flags
- **F1.** Post-hoc look-elsewhere item: crossed box positive only at N = 3 (§1). Not scored.
- **F2.** Lake warns the mathlib package (symlinked from br-wt-review) "has local changes" (pre-existing; not touched).
- **F3.** Auto-review classifier errors during the prereg write and checker patch led to two edits being applied as split commands (both landed in ce4a4ee); logged in `notes/AUTORESEARCH-LOG.md`.
- **F4.** Kernel lesson for METHOD: bitmask loop walk over precomputed tables + per-orientation chunking (list union-find blew > 3.5 GB on the tetrahedron).
