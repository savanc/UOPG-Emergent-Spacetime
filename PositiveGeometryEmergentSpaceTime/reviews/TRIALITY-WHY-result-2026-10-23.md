# TRIALITY-WHY result (2026-10-23, Grok; continuous-mode own pick (author approved 2026-10-23))
Verdict: NOT-FORCED / TAUTOLOGICAL-CONDITION — NO-GO
Run id: TRIALITY-WHY-2026-10-23-r1
**Verdict: NOT-FORCED / TAUTOLOGICAL-CONDITION (NO-GO).** Foregone and declared. Credit 0 (proposal). Prereg 7f98786 + guard-refusal record a494614 (pushed); planted 22:26:31, broken 22:26:33, live.

## Question
STRUCT-NGEN reopen trigger: is there a consistency (not phenomenological) reason to gauge baryon triality B3 (equivalently the Z₉ acting by 3B, whose anomaly cancels iff 3 ∣ N_gen; 1808.00009, CITED)? Gated on a declared mechanism list M1–M5 (prereg §1); anything else stays OPEN.

## Trials and results (sims/triwhy/triwhy_output.txt)
| Trial | Class | Result |
|---|---|---|
| T1 exactness vs Ibáñez–Ross linear | K | 29 240 Yukawa-compatible Z_k assignments (k = 2..18), N = 1..20: 0 mismatches between the SU(2)-instanton exactness window and the SU(2)²–Z_k window; SU(3)² and grav² (with νᶜ) sums identically 0. TAUT = true (PROVED: `sphaleron_eq_wwx`, `ccx_zero`, `grav_nuc_zero`) |
| T2 Dai–Freed Z₉ | C | window {3,6,…,18} = exactness window of Z₉(3B) (CITED 1808.00009 + SIMULATED) |
| T3 no global symmetries | K-conj | QQQL and uᶜuᶜdᶜeᶜ SM-invariant, ΔB = ±1, B3 charge ≠ 0 ⇒ "break" branch always available; W_QG = {1..5} (PROVED: `qqql_breaks_b3`, `qg_window`) |
| T4 geometry | geometry | x³ = 1 has 1 real root ⇒ no Z₃ through the real column torus (PROVED `torus_z3_trivial`); cyclic Z_n of Gr⁺(k,n) has Z₃ for 5/17 of n = 4..20, not family-constant |
| T5 proton stability | E | reported only; phenomenological, cannot force |
| null rate | — | 12/170 Z_k choices single out N = 3 (P3 = 6/85 ≈ 0.071; ×5 = 0.35 ≫ 0.01); 32/170 single out some N ∈ {3,4,5} (PROVED `null_count_d3`, `null_count_singleton`) |
| Rival ORDER | — | "window = multiples of k/gcd(k,c)" reproduces every exactness window (PROVED `window_iff`; SIMULATED scan) |
W_K = {1,…,5} (unchanged SM core window). Planted P1–P7 all OK; broken "gauged-triality window in AF-SU(3) range is {3}" REJECTED (window {3,6}; already false by the STRUCT-NGEN Lean theorem triality_su3_only_not_forced).

## Lean `PositiveGeometryEmergentSpaceTime.TrialityWhy` (22 theorems + 7 defs; 0 sorry; no native_decide; #lint clean; standard axioms; Mathlib only)
`sphaleron_eq_wwx`, `exact_iff_wwx`, `ccx_zero`, `grav_no_nuc`, `grav_nuc_zero`, `doublet_charge_Y_shift`, `window_iff`, `b3_exact_iff`, `z9_exact_iff`, `bminusl_doublet_zero`, `b3_eq_neg_BminusTwoY`, `qqql_gauge_invariant`, `qqql_deltaB`, `qqql_breaks_b3`, `qg_window`, `real_cube_root_one`, `torus_z3_trivial`, `cyclic_z3_not_family_constant`, `null_card`, `null_count_d3`, `null_count_singleton`, bundle `triality_why_summary`. Defs: `doubletCharge`, `sphaleronCharge`, `wwxSum`, `ccxSum`, `gravSum`, `qgOK`, `nullFamily`.

## Reading
- The linear anomaly condition that singles out 3 ∣ N for B3 is the same integer as the condition that B3 be an exact symmetry of the SM with sphalerons (PROVED, `sphaleron_eq_wwx`). "Gauged B3 needs 3 ∣ N" therefore says only "B3 exists as a symmetry needs 3 ∣ N". If 3 ∤ N, B3 is not a symmetry; nothing inconsistent happens (1808.00009 itself: a global anomaly obstructs gauging, it is not an inconsistency).
- No-global-symmetries (1011.5120, 1810.05337; CONJECTURE-level for our purposes) demands gauge OR break. Breaking by QQQL-type operators is always available, so the dichotomy constrains no N. Choosing "gauge" is motivated in hep-ph/0512163 by proton stability, i.e. phenomenology (class E).
- B3 = −(B − 2Y) mod 3 (PROVED), so B3 ≅ Z₉(3B) up to a U(1)_Y rotation: the "3" comes from picking order 9 for 3B. Picking order 12 or 15 singles out 4 or 5 the same way (null 12/170 for 3).
- Geometry side: the real column torus of positive geometry carries no Z₃ (PROVED); the cyclic symmetry of Gr⁺(k,n) has Z₃ only for 3 ∣ n, which is not a family-constant structure. Triality-blind.

## Caveats
Generation-universal Z_k only; one Higgs doublet; dim-6 operator list declared (4 operators, 2 invariant); cubic Z_k³ and Dai–Freed terms taken as CITED (UV/heavy-sector dependent per hep-ph/0512163 and 1808.02881, can be trivialised by symmetry extension), not recomputed. The QG dichotomy is a conjecture; the rung only shows it does not constrain N. Non-torus (complex/Galois) Z₃ actions on the geometry side and mechanisms outside M1–M5 are OPEN, not excluded. Prereg header time 22:27 is wrong (real: written 22:25:59, committed); erratum in sims/triwhy/guard_refusal.txt. Not touched: CREDITS.md, EW-Z1 paths, R4Indep blueprint block, XResearch, CASCADE-1b/2, INT-1, FL-1Z, M5, MC-1, TS-1, trade-space figure, Lean naming map (deltas in notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-23.md).

## Reopen triggers
A consistency principle that demands B3 (or another Z_n with N_gen-dependent anomaly) be EXACT, not merely non-anomalous (e.g. a derivation that dim-6 baryon violation is inconsistent, not just small); a geometry-side Z₃ that is not torus-valued (complex or Galois action) and is family-constant; any mechanism outside M1–M5 with a stated K-class argument.
