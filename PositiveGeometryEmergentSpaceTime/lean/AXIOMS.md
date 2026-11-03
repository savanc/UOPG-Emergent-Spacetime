# Axiom check (M1)

> **R4-DM forward note (2026-10-20).** `lake build` (9077 jobs) and `lake env lean AxiomsAll.lean` re-run on the R4-DM worktree: output byte-identical to `lean/AxiomsAll_output.txt` (TOTAL theorems=850 defs=381 nonstandard=0, sorry_dependent=0). R4-DM added no library Lean; its planted file `sims/r4dm/planted/R4DMPlanted.lean` (not imported by `PositiveGeometryEmergentSpaceTime.lean`) has 8 theorems, all [propext, Classical.choice, Quot.sound], 0 sorry.

> **Current audit (PositiveGeometryEmergentSpaceTime review 2026-10-20, forward note; nothing below is edited).** Fresh isolated `lake build` of origin/main 87a7a1f (9077 jobs, success, 97 `PositiveGeometryEmergentSpaceTime.*` modules) and fresh `lake env lean AxiomsAll.lean`, byte-identical to `lean/AxiomsAll_output.txt`: **`TOTAL theorems=850 defs=381 nonstandard=0`**, `sorry_dependent=0`. No `sorry`, `native_decide` or `axiom` in `lean/PositiveGeometryEmergentSpaceTime/`. The `TOTAL` lines further down (181/53 at the ladder review, 199/53 at M3w, 347/121, 554/189, …) are **historical snapshots** of the date in their section heading. One theorem is not counted: `PositiveGeometryEmergentSpaceTime.SplitZeroGate.chiral_match_iff` (`SplitZeroGate.lean:29`) is dropped by the auxiliary-name filter, which matches the substring `match_` rather than compiler-generated `match_<n>`; `#print axioms` on it gives standard axioms only (propext, Classical.choice, Quot.sound), so the true theorem count is 851, still all standard. A filter fix is proposed in notes/REVIEW-2026-10-20/REVIEW.md (not applied, so the 850 baseline stays comparable).

Run on 2026-10-10 with Lean v4.34.1, Mathlib v4.34.1 (d13f23b), Physlib a4ef461:

```
cd lean && lake build && lake env lean Axioms.lean
```

Output:

```
'PositiveGeometryEmergentSpaceTime.hermEquiv' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.coords_sigma' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.sigma_coords' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.det_sigma' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.det_herm_real' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.minkQ_sigPos' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.minkQ_sigNeg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.det_signature_one_three' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.eta_basis' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.eta_lorentzOf' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.lorentzOf_mul' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.lorentzOf_eq_id_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.sl2c_to_restricted_lorentz' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.sigma_eq_pauli' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.herm_det_eq_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.lightlike_iff_rank_one' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.plucker_rel' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.chart_pl' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.chart_klein' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.klein_affine_chart' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Every theorem depends only on the three standard axioms `propext`, `Classical.choice`, `Quot.sound`. A repo-wide search finds no `sorry`, no `native_decide`, and no `axiom` declarations in `PositiveGeometryEmergentSpaceTime/`. The build (`lake build`, 8985 jobs) finishes with linter warnings only.


# Axiom check (M2 / P-EFT)

Run on 2026-10-10 with the same pins (Lean v4.34.1, Mathlib v4.34.1 d13f23b, Physlib a4ef461). Commands: `cd lean && lake build && lake env lean Axioms.lean`. Output for the new M2 theorems:

```
'PositiveGeometryEmergentSpaceTime.Dispersion.secondDeriv_nonneg_of_dispersion' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Dispersion.secondDeriv_nonneg_of_measure' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Dispersion.convexOn_pole_right' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Dispersion.convexOn_pole_left' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Dispersion.convexOn_discrete_dispersion' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Dispersion.deriv2_pole' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.Tpm_poly' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.T00_poly' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.deriv2_Tpm' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.deriv2_T00' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.lbar2_ge' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.lbar1_2lbar2_ge' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.Tpm_curvature_neg_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.PionBound.lbar2_ge_of_dispersion' depends on axioms: [propext, Classical.choice, Quot.sound]
```

As for M1, everything depends only on `propext`, `Classical.choice`, `Quot.sound`. A search finds no `sorry`, no `native_decide` and no `axiom` declarations anywhere in `PositiveGeometryEmergentSpaceTime/`. `lake build` (8987 jobs) finishes, with linter warnings only.

Physics inputs are **hypotheses of the theorems, not axioms**. They appear as explicit arguments:
- `hdisp`: the twice-subtracted dispersion relation;
- `himS`/`himU`: Im T ≥ 0 on the cuts;
- `hmatch`: the true curvature equals the O(p⁴) ChPT curvature.

Each is tagged [CITED] in the docstrings and in `reviews/M2-result-2026-10-10.md`.

# Axiom check (M2b / EFT-hedron)

Run 2026-10-10, same pins. `lake build` (8988 jobs) OK; `lake env lean Axioms.lean`:

```
✔ [8986/8988] Built PositiveGeometryEmergentSpaceTime.Hankel (76s)
'PositiveGeometryEmergentSpaceTime.Hankel.sq_le_mul_of_quad_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.integral_sq_affine' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.moment_sq_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.hankel2_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.moment_succ_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.quadForm_hankel' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.hankel_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.hankel_posSemidef_of_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.moment_sq_le_discrete' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.hankel3_det_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.moment_succ_le_discrete' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.toy_moments' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.toy_checks' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.single_delta_saturates' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.C1_violates' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.C3_violates' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.no_positive_measure' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Hankel.no_finite_measure' depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorry`, `native_decide` or `axiom` in `PositiveGeometryEmergentSpaceTime/`. The physics input (forward coefficients are
moments of a positive measure) is a hypothesis in the form of the theorems' arguments (`μ`, `w ≥ 0`),
tagged [CITED] in `reviews/M2b-result-2026-10-10.md`.

# Axiom check (M2c / associahedron)

Run 2026-10-10, same pins. `lake build` (8989 jobs) OK; `lake env lean Axioms.lean`:

```
✔ [8987/8989] Built PositiveGeometryEmergentSpaceTime.Associahedron (115s)
'PositiveGeometryEmergentSpaceTime.Assoc.region_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.vertex_spec' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.vertex_injective' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.two_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.facet_X13' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.facet_X14' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.facet_X24' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.facet_X25' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.facet_X35' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.omegaFan_eq_m5' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.res_X13' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.res_X14' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.res_X24' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.res_X25' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.res_X35' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.tendsto_res_X13' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.empty_of_c14c24_neg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.empty_of_c13c14_neg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.region_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.X14_pos_of_c13_neg' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.soft_limit' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.Assoc.diags_five' does not depend on any axioms
'PositiveGeometryEmergentSpaceTime.Assoc.diags_six' does not depend on any axioms
'PositiveGeometryEmergentSpaceTime.Assoc.catalan_five' does not depend on any axioms
'PositiveGeometryEmergentSpaceTime.Assoc.catalan_six' does not depend on any axioms
```

The four `decide` counts use no axioms at all. No `sorry`, `native_decide` or `axiom` in `PositiveGeometryEmergentSpaceTime/`. The physical identification (this polygon is the n = 5 kinematic space and m5 is the φ³ amplitude) is [CITED], ABHY arXiv:1711.09102.

# Axiom check (M2d / NLSM)

Same pins and commands. `lake build` (8990 jobs) succeeds. Output for the new theorems:

```
'PositiveGeometryEmergentSpaceTime.NLSM.tendsto_atTop_of_inv' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm4_eq_c13' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.shift4_limit' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5_eq_m5f' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.shift5_limit_one' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.shift5_limit_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.shift5_c' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_zero_0' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_zero_1' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_zero_2' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_zero_3' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_zero_4' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_factor_c14' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.m5f_factor_c13' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.shift6_limit' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_zero_1' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_zero_2' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_zero_3' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_zero_4' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_zero_5' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_zero_6' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.nlsm6_adler' depends on axioms: [propext, Classical.choice, Quot.sound]
'PositiveGeometryEmergentSpaceTime.NLSM.shift6_zero_1' depends on axioms: [propext, Classical.choice, Quot.sound]
```

All 23 depend only on `propext`, `Classical.choice`, `Quot.sound`. No `sorry`, `native_decide` or `axiom` in `PositiveGeometryEmergentSpaceTime/`. Limits are genuine `Filter.Tendsto … atTop`; the physical identification (A6N is the NLSM amplitude, the shift gives pions) is [CITED] (2312.16282 eq. 4.3; 2401.05483 eq. 2).

## M2e: ShiftForced, ShiftForcedConverse (checked 2026-10-10)

All 17 theorems: [propext, Classical.choice, Quot.sound]. No sorry, native_decide or custom axioms.

## M2f: MassShift (checked 2026-10-10)

`lake build` (8993 jobs) succeeds; `lake env lean Axioms.lean`. All 25 declarations in `PositiveGeometryEmergentSpaceTime.MassShift` (22 theorems:
`mshift4_limit`, `mshift4_uniform`, `mshift4_eq_neg_c13`, `dressing_coeff`, `weinberg_iff`, `uniform_c`,
`hidden_zero4_forces`, `msoft4_zero`, `msoft4_naive`, `T0_threshold`, `T2_threshold`, `weinberg_lengths`, `ratio_iff`,
`mshift6_limit`, `mshift6_uniform`, `msoft6_leg1`, `a6n_reparam`, `a4n_reparam`, `offsets_forced6`,
`offsets_forced6_converse`, `hidden_zeros_force6`, `hidden_zeros_force6_opp`; 3 defs: `c13m`, `a00`, `a20`) depend only on
[propext, Classical.choice, Quot.sound]. No `sorry`, `native_decide` or custom axioms. The limits are genuine
`Filter.Tendsto … atTop`, obtained from the M2d limits at shifted arguments. The `hidden_zeros_force6*` certificates
(evaluation points, rational coefficients) come from `scripts/m2f_d2_cert.py` and are re-checked by `linear_combination`.

## M3: LECRatio (checked 2026-10-10)

`lake build` (8994 jobs) succeeds; `#print axioms` on all 23 declarations in `PositiveGeometryEmergentSpaceTime.LECRatio` (20 theorems:
`hidden_zero_iff`, `hidden_zero_form`, `sym_part_of_zero`, `product_split`, `shift4_factor`, `shift4_expansion`,
`su3_iff`, `su3_rename`, `su2_iff`, `linear_bounds`, `hidden_zero_iff_balance`, `hidden_zero_consistent`,
`odd_only_skyrme`, `even_only_zero`, `forward_hankel`, `ls_hankel`, `ls_gt2`, `be14_central`, `be14_fail`, `be14_gap`;
3 defs: `P4`, `g20`, `g21`) gives only [propext, Classical.choice, Quot.sound]. No `sorry`, `native_decide` or custom
axioms. Scope: the algebra (hidden zero ⇔ ratio; LEC maps; positivity consistency; exact data arithmetic) is proved.
The α′-expansion coefficients of the [H] and LS amplitudes (digamma values) are computed in sympy, not Lean; Lean
proves the inequalities for the resulting closed forms using `Real.pi_gt_three` and `Real.log_two_lt_d9`.

# Full check (ladder review, 2026-10-10)

The per-rung lists above were incomplete: M1 helper lemmas and the M2e module names were not listed one by one.
`AxiomsAll.lean` now enumerates **every** theorem and definition in modules `PositiveGeometryEmergentSpaceTime.*` (skipping compiler-generated
`eq_*`, `match_*`, `proof_*` and internal names) and runs Lean's `collectAxioms` on each. Same pins. `lake build`:
**8994 jobs, success** (linter warnings only). Then `lake env lean AxiomsAll.lean > AxiomsAll_output.txt`.

```
TOTAL theorems=181 defs=53 nonstandard=0
```

| Module(s) | Rung | Theorems |
|---|---|---|
| Spinor, Lorentz, Null, LightCone, Klein | M1 | 14 + 7 + 4 + 2 + 5 = 32 |
| Dispersion, PionBound | M2 | 8 + 9 = 17 |
| Hankel | M2b | 18 |
| Associahedron | M2c | 30 |
| NLSM | M2d | 23 |
| ShiftForced, ShiftForcedConverse | M2e | 8 + 9 = 17 |
| MassShift | M2f | 22 |
| LECRatio | M3 (+2 from the ladder review: `l3_ge_neg3_l2`, `be14_outside_wedge`) | 22 |
| **Total** | | **181** |

## M3w: LECRatio §L8 (checked 2026-10-11)

`lake build` (8994 jobs) green. 18 new theorems in `PositiveGeometryEmergentSpaceTime.LECRatio` (§L8: `family_interval`, `family_surj`,
`family_iff_odd_excess`, `family_sub_full`, `family_su3`, `family_su2`, `family_eps_endpoints`, `moment_two_le_gap`,
`d1_outside_2sigma`, `d1_inside_with_band`, `d1_inside_with_7pct`, `d1_deltaL_outside`, `band_wider_than_family`,
`d2_inside_family`, `d3_outside_2sigma`, `d8_within_1sigma`, `cgl_outside_2sigma`, `vmd_edge_passes_m3_rule`).
Re-ran `AxiomsAll.lean`:

```
TOTAL theorems=199 defs=53 nonstandard=0
```

LECRatio now 40 theorems; total 199. No `sorry`, `native_decide` or `axiom`. The data facts are exact ℚ (or ℝ with
Mathlib log bounds) arithmetic on quoted, rounded numbers.


Every declaration depends only on a subset of `propext`, `Classical.choice`, `Quot.sound` (the four `decide`
Catalan counts use none). There is no `sorry`, `native_decide` or `axiom` in `PositiveGeometryEmergentSpaceTime/`. Re-run `AxiomsAll.lean` at
every rung (MISSION, Rung protocol step 4).

## M3c: Coon (checked 2026-10-11)

All 16 theorems in `PositiveGeometryEmergentSpaceTime.Coon` use only [propext, Classical.choice, Quot.sound]. No sorry, native_decide or custom axioms. The full list is in `AxiomsAll_output.txt` (total theorems in the project: 215).

## M1b: SliceBridge (checked 2026-10-11)

All 36 theorems and 14 definitions in `PositiveGeometryEmergentSpaceTime.SliceBridge` use only a subset of [propext, Classical.choice,
Quot.sound]. There is no sorry, native_decide or custom axiom. Proved mathematics: `herm_not_pos`, `tau_chart_herm`,
`tau_fixed_not_pos`, `herm_nonneg_iff`, `herm_nonneg_null`, `herm_real_minors_y0`, `herm_real_minors_no_open`,
`det_Xw`, `Xw_real_herm`, `det_Xw_split`, `Xw_pos_forces_split`, `Xw_real_forces_split`, `herm_slice_excluded`,
`null_dot_nonneg`, `null_zero_energy`, `neg_dot_opposite`, `pos_dot_same`, `s_eq_two_dot`, `no_euclid5`, `no_pos5`,
`planar5_eq`, `no_pos4`, `det_two_spinor`. Exact arithmetic on explicit points: `split_point_pos`,
`twisted_example`, `cfg4_*`, `cfg6_*`, `splitPos_*`, `splitNeg_*`. Project total: **251 theorems, 67 definitions,
nonstandard = 0** (`AxiomsAll_output.txt`).

## H-T1: MarkovTrace + Network (checked 2026-10-11)

All 32 theorems (22 in `PositiveGeometryEmergentSpaceTime.MarkovTrace`, 10 in `PositiveGeometryEmergentSpaceTime.Network`) and 10 definitions use only [propext,
Classical.choice, Quot.sound]. There is no sorry, native_decide or custom axiom.
- General mathematics: `trace_rowsum`, `trace_nonneg`, `trace_mem_rowStochastic`, `piB_eq`, `trace_stationary(_normalised)`,
  `kac_sum`, `kac`, `negMulLog_add_le`, `sum_negMulLog_mul`, `one_state_elimination`, `schur_trace`, plus the
  symbolic network results `path_*`, `lam2_*`, `Y_pluecker`, `Y_pos`, `star_response` (for all positive conductances).
- Exact examples: `P3_*`, `pi3_stationary`, `Tr3_eq`, `entRate_*`, `bits`, `conjecture_false`, `corrected_equality`,
  `commute_*`.

Project total: **283 theorems, 77 definitions, nonstandard = 0**.

## H-T2: PositroidCells (checked 2026-10-11)

All 17 theorems and 15 definitions in `PositiveGeometryEmergentSpaceTime.PositroidCells` use only [propext, Classical.choice, Quot.sound]. There
is no sorry, native_decide or custom axiom; the combinatorics uses `decide` (kernel reduction).
- Symbolic, for all positive conductances: `F_pluecker`, `F_pattern`, `dy_yd`, `yd_dy`, `yd_bijOn`,
  `hasDerivAt_lin_div`, `hasDerivAt_const_div`, `logJac_entry00`, `logJac_entry20`, `star_triangle_dlog`,
  `grove_quadric`, `terminal_minors`.
- Finite combinatorics (`decide`): `dim_formula_n3`, `crossing_census_n3`, `facet_cell`, `top_cell`,
  `fusions_matches_projection`.

Project total: **300 theorems, 92 definitions, nonstandard = 0** (`AxiomsAll_output.txt`); `lake build` green.

## H-T3: IsingOG (checked 2026-10-11)

All 10 theorems and 4 definitions in `PositiveGeometryEmergentSpaceTime.IsingOG` use only [propext, Classical.choice, Quot.sound] (`gp2_cells`
uses only [propext]). There is no sorry, native_decide or custom axiom.
- Symbolic: `gp2_minors`, `gp2_orthogonal`, `gp2_pos`, `gp2_inverse` (all σ), `ratio_eq_inv_sinh` (all J > 0),
  `medial_weights`, `kw_inverts`, `gpY_orthogonal` (all t₁, t₂, t₃).
- Exact sample: `gpY_pos_sample`.
- Finite combinatorics (`decide`): `gp2_cells`.

Project total: **310 theorems, 96 definitions, nonstandard = 0** (`AxiomsAll_output.txt`); `lake build` green.

## H-T3b: IsingLoop (checked 2026-10-12)

All 7 theorems and 5 definitions in `PositiveGeometryEmergentSpaceTime.IsingLoop` use only [propext, Classical.choice, Quot.sound]. There is no
sorry, native_decide or custom axiom.
- `hasDerivAt_mobius`, `jac_symm`, `jac_triangle`, `det3_div`, `q1_den_pos`, `sech_star_eq`, `star_triangle_loop`.

Project total: **317 theorems, 101 definitions, nonstandard = 0**; `lake build` green.

## H-T5: IsingTiling (checked 2026-10-12)

All 5 theorems and 5 definitions in `PositiveGeometryEmergentSpaceTime.IsingTiling` use only standard axioms. There is no sorry, native_decide or custom axiom.
- `Y_eq`, `C_orth`, `adjacent_brackets`, `first_row_brackets`, `sign_flip_certificate`.

Project total: **322 theorems, 106 definitions, nonstandard = 0**; `lake build` green (9002 jobs).

## H-T5b: IsingTiling8 (checked 2026-10-12)

All 4 theorems and 4 definitions in `PositiveGeometryEmergentSpaceTime.IsingTiling8` use only standard axioms. There is no sorry, native_decide or custom axiom.
- `C0_orth`, `C2_orth`, `C0_minors`, `C2_minors`.

Project total: **326 theorems, 110 definitions, nonstandard = 0**; `lake build` green (9003 jobs).

## H-T5d: IsingTiling10 (checked 2026-10-12)

All 10 theorems and 7 definitions in `PositiveGeometryEmergentSpaceTime.IsingTiling10` use only standard axioms. There is no sorry, native_decide or custom axiom.
- `C1_orth` … `C5_orth`, `C1_minors` … `C5_minors`.

Project total: **336 theorems, 117 definitions, nonstandard = 0**; `lake build` green (9004 jobs).

## H-T5f (2026-10-12)

No new Lean modules. Totals unchanged: **336 theorems, 117 definitions, nonstandard = 0**.

## MR-1 (2026-10-12)

`PositiveGeometryEmergentSpaceTime.LSResidue`: 5 theorems and 2 definitions, standard axioms only. Project total: **341 theorems, 119 definitions, nonstandard = 0**; `lake build` green.

## MR-1b (2026-10-12)

`PositiveGeometryEmergentSpaceTime.LSResidue` extended to 11 theorems and 4 definitions. Project total: **347 theorems, 121 definitions, nonstandard = 0**.

### 2026-10-13 (AutoResearch): SG1 + SG1b wired in
Added `import PositiveGeometryEmergentSpaceTime.SG1`, `import PositiveGeometryEmergentSpaceTime.SG1b` to `PositiveGeometryEmergentSpaceTime.lean` (EWZ1b kept). `lake build`: 9038 jobs, success. `AxiomsAll.lean` (unchanged; it enumerates all `PositiveGeometryEmergentSpaceTime.*`) re-run: **TOTAL theorems=554 defs=189 nonstandard=0**. SG1/SG1b: 8 theorems + 1 def, standard axioms only.

## FR-MU (2026-10-16)
No FRONTIER-AXIOM introduced. The construction's symmetric-irrep matrix elements are an explicit hypothesis (`PositiveGeometryEmergentSpaceTime.FRMU.SymIrrepME.Valid`, a theorem argument). Results depending on it (`planted_sm`, `ratio_acc`, `ratio_fixed_charges`) are conditional on that hypothesis, which `sims/frmu/frmu_checker.py` verifies by brute force for N_c = 1, 3, 5, 7.

## FR-WZW (2026-10-16, Grok)
No FRONTIER-AXIOM. `PositiveGeometryEmergentSpaceTime.FRWZW`: 8 theorems + 5 defs, standard axioms only (propext, Classical.choice, Quot.sound).

## F-COULOMB (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FCoulomb`: 8 theorems + 3 defs, standard axioms only (propext, Classical.choice, Quot.sound). The reduction of the momentum-twistor inequalities (arXiv:2311.10814 eqs. (1), (4)–(6)) to the wedges (7)–(8) is CITED and checked numerically in `sims/fcoulomb`; it is not formalised. Fresh AxiomsAll: **TOTAL theorems=771 defs=359 nonstandard=0**, sorry_dependent=0.

## F-DIM (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FDim`: 9 theorems + 5 defs, standard axioms only. The LS amplitude and the SO(D−1) Gegenbauer partial-wave criterion are CITED (Bianchi–Consoli–Di Vecchia 2021; AEHM arXiv:2201.11575); the Gegenbauer `C₁`, `C₂` are defined explicitly.

## F-DIM′ (2026-10-20, Grok)
No FRONTIER-AXIOM. `PositiveGeometryEmergentSpaceTime.FDim` extended with `lsLevel2Half` (def) and `lsLevel2Half_legendre` (now 10 theorems + 6 defs), standard axioms only; imports `PositiveGeometryEmergentSpaceTime.Legendre`.

## F-DIM-MASS (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FDimMass`: 10 theorems + 2 defs, standard axioms only; imports `PositiveGeometryEmergentSpaceTime.FDim`. LS amplitude with massive external pions CITED (Bianchi–Consoli–Di Vecchia 2021); physical masses CITED in `sims/fdimm/masses.json` and never enter Lean.

## F-SCATLEN (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FScatLen`: 17 theorems + 5 defs, standard axioms only. `lsV_half_zero` uses Mathlib's `Real.Gamma_zero` (Γ(0) = 0 by convention) with `inv_zero`; this coincides with the true value 1/Γ(0) = 0 of the entire function 1/Γ (disclosed). Weinberg/Lovelace amplitudes and all data CITED.

## F-RHOWIDTH (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FRhoWidth`: 11 theorems + 3 defs, standard axioms only; imports `PositiveGeometryEmergentSpaceTime.FScatLen`. The residue limit (continuity of the pole-stripped block) is CITED, not formalised; KSRF and data CITED.

## F-POSGEOM-DAUGHTER (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FDeltaNLSM`: 7 theorems + 1 def, standard axioms only. The δ-shifted amplitude (2312.16282 eq. 7.10), the propagator convention 1/(X + m²) and the full-U(N) mass condition m_φ² + m_φ̃² = 0 (2401.05483) are CITED; the pole limit is CITED (pole-stripped value proved).

## BRIDGE-PL-ASSOC mission rung (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.BridgePLCharge`: 12 theorems + 2 defs, standard axioms only; imports `PositiveGeometryEmergentSpaceTime.BridgePLAssoc` (not `PositiveGeometryEmergentSpaceTime.STRUCT1`: the ACC conditions in `trace_conditions_not_acc` are restated inline so that no spurious geometry↔STRUCT dependency edge is created). GGMS/Speyer–Williams/ABL/AHL maps, Dirichlet and cube moments CITED; κ(Δ(2,15)) SIMULATED (exact rationals).

## STRUCT-NGEN sharpen (2026-10-20, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.STRUCTNGen`: 12 theorems + 3 defs, standard axioms only; imports `PositiveGeometryEmergentSpaceTime.STRUCT3`. Baryon-triality residues and the Spin-Z₄ Weyl count (1808.00009), the 3-3-1 content (hep-ph/9206242) and the two-loop QCD coefficient are CITED.

## INT-1 (2026-10-22, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.IntChamber`: 22 theorems + 13 defs, 0 sorry, no native_decide, standard axioms only ([propext, Classical.choice, Quot.sound]; lean/axioms/IntChamber_output.txt and graph/raw_decls.jsonl); imports `PositiveGeometryEmergentSpaceTime.Associahedron`.

## GRADED-POSITROID (2026-10-22, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.GradedPositroid`: 9 theorems + 5 defs, standard axioms only (propext, Classical.choice, Quot.sound); imports `PositiveGeometryEmergentSpaceTime.BridgePLCharge`. Hypercharge assignments are SM inputs; κ values are SIMULATED (exact rational), not formalised.

## FL-1Z (2026-10-22, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.FL1Z`: 10 theorems + 2 defs (`D3`, `w`), 0 sorry, no native_decide, standard axioms only (lean/axioms/FL1Z_output.txt): `valence_lt12`, `valence_k2_empty` [propext, Quot.sound]; `valence_k12_free` [propext]; the rest [propext, Classical.choice, Quot.sound]. The level-1 valence formula 12n + 6a + 4b = k (Serre VII.3, not fetched this run) enters only as an explicit theorem hypothesis `hv`, not an axiom; the level-3 (A4) valence count of the physical model is not formalised. Imports Mathlib only.

## INT-1 count reconciliation (2026-10-22, Grok; per notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-22.md)
The INT-1 section's "22 theorems + 13 defs" counts source declarations and is correct. AxiomsAll_output.txt / graph/raw_decls.jsonl list 26 `thm` for `PositiveGeometryEmergentSpaceTime.IntChamber` because they also include 4 compiler-generated equation lemmas of match-defined defs: `dec.eq_2`, `dec.eq_3`, `val.eq_2`, `val.eq_3`. Those are not user theorems, and GraphExport's `isAux` filters only `.eq_1`/`.eq_def`. 22 + 4 = 26; all are standard axioms. No change to the INT-1 section. `PositiveGeometryEmergentSpaceTime.FL1Z` has no such lemmas: 10 thm + 2 def in both counts.
Fresh lean/AxiomsAll_output.txt after the FL-1Z rebase (onto 51d1342): TOTAL theorems=895 defs=401 nonstandard=0, sorry_dependent=0 (885/399 + FL1Z 10/2).

## LEAN-CERT-1 (2026-10-23, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.LeanCert` has 40 source theorems and 42 defs/instances. It has 0 sorry and no native_decide / `Lean.ofReduceBool`; certificates are checked by `decide +kernel` on structurally recursive Bool folds. Standard axioms only (lean/axioms/LeanCert_output.txt):
- the certificate, matrix-equality and planted `decide` theorems use [propext, Quot.sound];
- `allFin_iff` uses [propext];
- the rest use [propext, Classical.choice, Quot.sound].

It imports Mathlib only. `lake env lean PositiveGeometryEmergentSpaceTime/LeanCert.lean` took 10.2 s at 6.8 GB peak RSS (sims/leancert1/lean_build_time.txt). AxiomsAll lists 42 `thm` for the module: the 40 source theorems plus the compiler eq lemmas `sumFin.eq_2` and `allFin.eq_2`.

Fresh lean/AxiomsAll_output.txt (full `lake build`, 9081 jobs): **TOTAL theorems=937 defs=443 nonstandard=0, sorry_dependent=0**. That is 895/401 + LeanCert 42/42; all other lines are byte-identical.

## CASCADE-1 (2026-10-23, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.Cascade1` has 36 theorems and 13 defs. It has 0 sorry and no native_decide / `Lean.ofReduceBool`. The Θ_3 dimension certificates `em4_cert` and `em5_cert` are checked by `decide +kernel` through the LeanCert soundness layer (`finrank_ker`). Standard axioms only (lean/axioms/Cascade1_output.txt):
- `em4_cert` and `em5_cert` use [propext, Quot.sound];
- the other 34 use [propext, Classical.choice, Quot.sound].

It imports Mathlib and PositiveGeometryEmergentSpaceTime.LeanCert. The 20 relation-specific n = 5 statements (`zero5_of_rel_k`, `split5_of_rel_33_k`, `split5_of_rel_35_k`, `zero5_only_if_k`) are generated by sims/cascade1/gen_lean.py from the run CASCADE1-2026-10-23-r1 relations and checked by Lean. `lake env lean PositiveGeometryEmergentSpaceTime/Cascade1.lean` took 5.7 s at 6.5 GB peak RSS (sims/cascade1/lean_build_time.txt). AxiomsAll lists 36 `thm` + 13 `def` for the module, with no compiler eq lemmas.

Fresh lean/AxiomsAll_output.txt (full `lake build`, 9082 jobs): **TOTAL theorems=973 defs=456 nonstandard=0, sorry_dependent=0**. That is 937/443 + Cascade1 36/13.

## TRIALITY-WHY (2026-10-23, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.TrialityWhy`: 22 theorems + 7 defs, standard axioms only (subsets of propext, Classical.choice, Quot.sound); imports Mathlib only. The quantum-gravity dichotomy enters as the definition `qgOK exact gauged broken := exact → gauged ∨ broken`, not as an axiom; `qg_window` instantiates it with gauged = False and broken = (B3 doublet charge not ≡ 0 mod 3), so it is shallow: it records that the break branch excludes no N. Dai–Freed cubic terms are CITED (1808.00009, 1808.02881), not formalised.

## CASCADE-1b (2026-10-24, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.Cascade1b`: 2 theorems + 1 def (`offsetsE0`, `e0_n6_offsets_zero_iff`, `e0_n6_collapse`), standard axioms only; imports Mathlib only; no native_decide. Prereg §7 item 1 only (run r1 NOT-EVALUATED; items 2–5 need run relations). Fresh lean/AxiomsAll_output.txt (full `lake build PositiveGeometryEmergentSpaceTime`, 9084 jobs): **TOTAL theorems=997 defs=464 nonstandard=0, sorry_dependent=0** (995/463 + Cascade1b 2/1).

## LEAN-CERT-2 (2026-10-28, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.LeanCert2` (umbrella) + `PositiveGeometryEmergentSpaceTime.LeanCert2.Core` + `PositiveGeometryEmergentSpaceTime.LeanCert2.{FrwzwK0p, FrwzwK0m, FrwzwK1p, FrwzwK1m}`: 28 source theorems and 74 defs (10 list-checker defs + 8 data defs per certificate for ABHY n = 5/6/7, broken B1 and four FR-WZW cases). 0 sorry and no native_decide / `Lean.ofReduceBool`; certificates are checked by `decide +kernel`. Axioms: subsets of propext, Classical.choice, Quot.sound (the `*_cert` decide theorems use [propext] only). Imports Mathlib and PositiveGeometryEmergentSpaceTime.LeanCert (`finrank_ker`).
Theorems: `dotL_eq`, `getD_len`, `mulL_eq`, `tposL_spec`, `zeroL_spec`, `splitL_spec`, `injL_spec`, `finrank_of_certL`, `abhyL5_matrix`, `abhyL6_matrix`, `abhyL7_matrix`, `abhyL5_cert`, `abhyL6_cert`, `abhyL7_cert`, `abhy5_finrank'`, `abhy6_finrank'`, `abhy7_finrank'`, `broken_abhy6_dim10_rejected`, `no_abhy6_dim10_certL` (Core); `frwzw_k0p_cert`, `frwzw_k0p_finrank`, `frwzw_k0m_cert`, `frwzw_k0m_finrank`, `frwzw_k1p_cert`, `frwzw_k1p_finrank`, `frwzw_k1m_cert`, `frwzw_k1m_finrank` (one submodule each); bundle `frwzw_counts_k01` (umbrella). AxiomsAll lists 30 `thm` for the modules: the 28 source theorems plus the compiler eq lemmas `dotL.eq_2`, `dotL.eq_3`.
Not formalised (LIMIT): FR-WZW k = 2, 3 and planted PL2 (Lean kernel check > 8 GB RSS at 120×21; stay SIMULATED). The FR-WZW matrix literals are emitted from the locked checker (SIMULATED provenance); only ABHY has a Lean generator link (`abhyL*_matrix`).
Fresh lean/AxiomsAll_output.txt (`lake build PositiveGeometryEmergentSpaceTime`, 9090 jobs, one target at a time; then `lake env lean AxiomsAll.lean` to a temp file, 382 s, 6.9 GB peak RSS): **TOTAL theorems=1027 defs=538 nonstandard=0, sorry_dependent=0**. That is 997/464 + LeanCert2 30/74; all other lines are byte-identical (the two Lake 'local changes' warning lines are no longer copied into the file).

## JORD-1 (2026-10-28, Grok)
No FRONTIER-AXIOM and no hypothesis structure. `PositiveGeometryEmergentSpaceTime.Jord1` (umbrella) + `PositiveGeometryEmergentSpaceTime.Jord1.{Table, Alg, Data, Gens, NoGo}`: 33 source theorems (+2 auto-generated equation lemmas) and 46 defs (octonion/Fano table, h3(O) basis and Jordan product, sparse derivation checker, g_sm / stab definitions, integer generator and witness data). 0 sorry and no native_decide / `Lean.ofReduceBool`; checks by `decide +kernel`. Key theorems (`gsm_not_pointwise_stabiliser`, `W_kills_fix`, `gen_mem_gsm`, `W_isDer`) use [propext, Classical.choice, Quot.sound]. Imports Mathlib and PositiveGeometryEmergentSpaceTime.LeanCert2.Core (list matrices).

Fresh lean/AxiomsAll_output.txt (`lake build PositiveGeometryEmergentSpaceTime`, 9096 jobs, one target at a time, LEAN_NUM_THREADS=1; then `lake env lean` on a mktemp copy of AxiomsAll.lean, 378 s, 571 MB anon peak): **TOTAL theorems=1062 defs=584 nonstandard=0, sorry_dependent=0**. That is 1027/538 + Jord1 35/46; all other lines unchanged.

## SURF-1′ (2026-10-28/29, Grok)
No FRONTIER-AXIOM and no hypothesis structure. Module family: `PositiveGeometryEmergentSpaceTime.Surf1` (umbrella) and `PositiveGeometryEmergentSpaceTime.Surf1.{Enum, Box.Graph, Box.C0, Box.C1, Box.C2, Box.C3, Box, Signs, Main}`. It holds 93 theorems (64 per-orientation box chunks), 46 defs and 1 structure (`G`). 0 sorry, no native_decide / `Lean.ofReduceBool`. Enumeration checks use `decide +kernel` [propext]; rational sign lemmas use field_simp / positivity / nlinarith [propext, Classical.choice, Quot.sound].

Fresh lean/AxiomsAll_output.txt: `lake build PositiveGeometryEmergentSpaceTime`, 9106 jobs, one target at a time with LEAN_NUM_THREADS=1 under the anon-RSS watchdog; then `lake env lean` on a mktemp copy of AxiomsAll.lean, 399 s, 571 MB anon peak. **TOTAL theorems=1155 defs=630 nonstandard=0, sorry_dependent=0**, i.e. 1062/584 plus Surf1 93/46. All other lines are unchanged.

## Convention re-checks: JordConv, SurfConv, LeanCertConv (2026-10-30, Grok)
No FRONTIER-AXIOM and no hypothesis structure. Three small modules from the convention-invariance re-checks (the author; METHOD rule "Convention-invariance check (2026-10-30)"), 8 theorems, 0 sorry, no native_decide:
- `PositiveGeometryEmergentSpaceTime.JordConv` (JORD-1, prereg 32e8a9c, result c6b1f2c): `der_smul_eq_zero_iff`, `stab_smul_eq`, `idem_scale_iff` (3).
- `PositiveGeometryEmergentSpaceTime.SurfConv` (SURF-1′, prereg 422faf1, result 62d1abc): `even_pow_pos`, `pos_iff_scaled`, `ratio_pos_iff` (3).
- `PositiveGeometryEmergentSpaceTime.LeanCertConv` (LEAN-CERT-2, prereg 3131dd6, result a50369a): `split_iff_of_PM_eq`, `valid_iff_of_PM_eq` (2), def `Valid`.

Fresh lean/AxiomsAll_output.txt (PositiveGeometryEmergentSpaceTime, 2026-10-30, main checkout at eb384df: `lake build PositiveGeometryEmergentSpaceTime`, 9110 jobs, LEAN_NUM_THREADS=4; then `lake env lean AxiomsAll.lean`): **TOTAL theorems=1172 defs=634 nonstandard=0, other_kinds=27, sorry_dependent=0**, i.e. 1155 + 17 since the 433cc73 snapshot (8 from these modules, 9 from `PositiveGeometryEmergentSpaceTime.Cascade1bR2`; checked by diffing the theorem lists). All 8 new theorems use only [propext, Classical.choice, Quot.sound] or a subset.
