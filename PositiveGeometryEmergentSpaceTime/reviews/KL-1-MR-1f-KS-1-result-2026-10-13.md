# KL-1 theory + MR-1f and KS-1 (verified-remembered, rule 6): **KS-1 PASS (6/6), MR-1f PASS (6/6, weak null)** — 2026-10-13
- Prereg: `prereg/KL-1-MR-1f-KS-1-prereg-2026-10-13.md` (**eb69103, pushed before any K*_J value was opened**).
- Scripts: `scripts/kl1_theory.py`, `scripts/kl1_data_check.py` (+ outputs, json). Lean: `PositiveGeometryEmergentSpaceTime.UnequalLS` (6 thms, 0 sorry, axioms propext/Classical.choice/Quot.sound; `lean/AxUnequalLS_output.txt`).

## KL-1 theory gate: **PASS (posable)**
- **Prior art (CITED):** Lovelace 1968; Kawarabayashi–Kitakado–Yabuki (KKY) PLB 28 (1969) 432 and PR 184 (1969) 1956 (πK Veneziano amplitudes with Adler PCAC condition, universal slope); Ademollo–Veneziano–Weinberg PRL 22 (1969) 83 (soft-meson mass relations). The amplitude used is KKY's ρ–K* term. Our trajectories (α_K(0)=0.289, α_ρ(0)=0.483, α'=0.860 GeV⁻²) coincide with KKY's PCAC values (seen in a prior-art search snippet: theory, not target data).
- **New (ours):** the intercepts follow from requiring that the dual zero line α_ρ(t)+α_K(u)=1 equal the CGW/MR-4 hidden-zero line s = mπ²+mK² — **PROVED** `zero_line`, `zero_line_conv`; the K*_J masses `mass_formula`, `spacing`; the AVW relation `kstar_relation`; Pochhammer residue `poch3`.
- SIMULATED: the massless equal-mass limit reproduces MR-1b's 5/16 and 49/240 exactly (consistency).
- Assumption: slope universality (KKY). Inputs: mπ, mρ (OP-2) + mK (strange free unit) + Γ(K*) (MR-1f normaliser, 1 extra). Outputs 7 > 1 → sector credit allowed.

## Sources (read after the push)
- S1 PDG 2026 (pdgLive): K*0 895.56±0.20, Γ 47.1±0.5; K2*0 1432.4±1.3, Γ 109±5, BR 0.499±0.012; K3* 1779±8, Γ 161±17, BR 0.188±0.010; K4* 2048(+8−9), Γ 199(+27−19), BR 0.099±0.012.
- S2 LASS: ASTON 88 (K*, K2*, K3*: m, Γ, BR), ASTON 86 (K4* m, Γ); K4* BR is the single ASTON 88 value (same as PDG → **S1/S2 not independent for K4* BR**; LASS also dominates several PDG averages: **partly dependent**, disclosed as in MR-1b).

## KS-1 — K*_J masses (SIMULATED) — **PASS**
| State | LS | S1 | z | S2 | z | null f |
|---|---|---|---|---|---|---|
| K2*(1430) | 1.4108 | 1.4324 | +0.62 | 1.4312 | +0.58 | 0.17 |
| K3*(1780) | 1.7758 | 1.7790 | +0.07 | 1.7810 | +0.12 | 0.28 |
| K4*(2045) | 2.0776 | 2.0480 | −0.56 | 2.0620 | −0.28 | 0.38 / 0.40 |
- (K* 0.9095 vs 0.8956: +1.6 %, AVW prior art, not scored.) All |Δm²|/m² ≤ 3.1 %.
- Null: per state 0.17, 0.28, 0.38; joint (all three by chance) ≈ 0.018. K4* alone is not discriminating (f > 0.3).

## MR-1f — Kπ width ratios R_J = Γ(K_J*→Kπ)/Γ(K*→Kπ) (SIMULATED, MC) — **PASS, non-discriminating**
| R | S1 data | LS (V1) | data/LS | z | S2 data | LS | data/LS | z | null f |
|---|---|---|---|---|---|---|---|---|---|
| R2 | 1.156±0.061 | 1.029 | 1.12 | +0.38 | 1.113±0.066 | 1.023 | 1.09 | +0.27 | 0.33 |
| R3 | 0.644±0.076 | 0.626 | 1.03 | +0.07 | 0.740±0.126 | 0.630 | 1.18 | +0.42 | 0.42/0.43 |
| R4 | 0.416±0.077 | 0.348 | 1.20 | +0.41 | 0.424±0.118 | 0.367 | 1.16 | +0.29 | 0.58/0.64 |
- Central agreement is 3–20 % with no parameter; but the pre-registered 30 % ⊕ level band is wide, so the null rate f (0.42–0.64 on the primary R3, R4) exceeds 0.3 → **weak** per prereg.

## Proposed credit (rule 6, VR line; needs the author's OK)
- **KS-1: +0.5** (PASS 6/6; 2 of 3 states discriminating, joint null 0.02). Conservative alternative: 0.25 (if per-state f ≤ 0.3 is required for all three).
- **MR-1f: +0.25** (PASS but non-discriminating, as pre-registered).
- Blind line unchanged (memorised). Caveats: S2 partly dependent; K* masses rest on 1969 prior art (KKY/AVW), our addition being the hidden-zero derivation; slope universality assumed.

## Proposed tally
blind **2.0** (MR-1b, MR-4) | VR **0.5 → 1.25** (MR-2 0.5, KS-1 0.5, MR-1f 0.25) | total **3.25/3** nominal (milestone reached on the combined line only; blind line still 2/3).

## Decision (author approved 2026-10-13): strict option
KS-1 **+0.25** (strict: K4* alone does not beat the null), MR-1f **+0.25** (weak), both on the VR line. Official OP-2: blind 2.0 | VR 1.0 | **3.0/3** — milestone met on the combined line only; blind line 2.0.
