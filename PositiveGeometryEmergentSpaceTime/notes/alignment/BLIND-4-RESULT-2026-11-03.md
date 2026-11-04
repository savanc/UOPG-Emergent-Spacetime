# BLIND-4 result: MR-1f width formula in Lean (2026-11-03)

Authority: author approved (2026-11-03).
Prereg: notes/alignment/BLIND-4-PREREG-2026-11-03.md (commit d8004bd, pushed before the originals were opened).
Modules (alignment layer, NOT imported by `PositiveGeometryEmergentSpaceTime`): `PositiveGeometryEmergentSpaceTime.Alignment.Blind.Mr1fBlind` (8 thm, 11 defs),
`PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.MR1F` (19 thm, 5 defs). Axiom audit: lean/AlignmentBlind4Axioms.lean,
output lean/AlignmentBlind4Axioms_output.txt: 37/37 declarations depend only on [propext, Classical.choice, Quot.sound].
All runs via <local path> (CAP_ANON_GB=4), peak anon ≤ 0.75 GB; no sorry, no native_decide.

## Originals opened after the prereg
- lean/PositiveGeometryEmergentSpaceTime/UnequalLS.lean: the only width-related theorem is `poch3` (J = 3 Gamma ratio). No width theorem.
- scripts/kl1_theory.py (`resid`, `width`, `pred`) and scripts/kl1_theory_output.txt (SIMULATED V2 ratios 0.89489 / 0.57764 / 0.36488).

## Compare (blind vs original)
| Item | Class | Lean |
|---|---|---|
| Gamma ratio Γ(1−a) = (−1)^J (a)_J Γ(1−a−J) | BLIND-STRONGER (all J vs J = 3); EQUIV at J = 3 | gamma_ratio_min, blind_of_min, orig_poch3_of_blind, blind3_of_orig |
| Residue (script `resid`) | EQUIV up to a uniform sign | script_residue_eq |
| Legendre projection G_J, J = 1..4 | MISSING-LEAN in original → PROVED (blind) | Mr1fBlind.legendre_J1..J4, Gtop_vals |
| Kinematics q², t(x), pole m_J² | MISSING-LEAN → PROVED | Mr1fBlind.alphaRho_tOf, alphaK_m2J; Compare.q2_pos, pole_J1 |
| Ratios R2, R3, R4 at V2 inputs | SIMULATED → PROVED intervals | R2_val (0.89485, 0.89495), R3_val (0.57755, 0.57765), R4_val (0.36485, 0.36495) |

## Sanity
- Known value / tie to SIMULATED numbers: R2_val, R3_val, R4_val bracket the script output (kl1_theory_output.txt) and the blind Python run BLIND4-PY-2026-11-03-r1 (0.894891 / 0.577637 / 0.364884).
- Planted wrong cases: planted_xJ_R2 (x^J-coefficient reading gives R2 > 1.3, rejected); planted_nofact_R3 (dropping 1/(J−1)! doubles R3, rejected by the band).
- Non-vacuity: q2_pos (all four poles above Kπ threshold), gamma_hyp_nonvacuous (a = ½), ratio_pos, width_pos.

## Findings
1. The prose width formula (prereg:30) is consistent with the script: the blind reading reproduces the V2 ratios to 6 digits. (PROVED intervals + SIMULATED BLIND4-PY-2026-11-03-r1.)
2. Minor: the script's G_J print as negative (−0.154, −0.272, −0.292, −0.271) beside "(sign must be >0)". The script takes the coefficient of 1/(J − α_K); the sign is uniform in J (script_residue_eq), so every ratio is unaffected. The residue in (u − m_J²) is positive. Bookkeeping only; no number changes.
3. The original record lists `poch3` as proved (MATCH) but the width formula itself had no Lean (MISSING-LEAN). It is now PROVED as algebra in the alignment layer.

## What stays outside Lean
- CITED: the pole factor of Γ(1 − α_K) at α_K = J (standard), and the proportionality convention Γ_J ∝ G_J q_J /((2J+1) m_J²).
- SIMULATED: V1 ratios at each source's own masses, the data comparison, z-scores and MC null rate f (kl1_data_check). PASS stays non-discriminating.

No status, tag or credit change (credit stays 3.5/3). Blueprint rows C16–C18 in notes/alignment/blueprint-credited-2026-11-03.tsv.
Coverage (figures/make_lean_map_2026_11_03.py): alignment 75 modules (BLIND 17, BLINDCMP 14, PILOT 12, SANITY 32);
77 index rungs: with_blueprint 22, with_sanity 11, with_blind 13, with_any_alignment 22.
