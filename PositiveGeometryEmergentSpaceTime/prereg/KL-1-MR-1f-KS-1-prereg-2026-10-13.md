# KL-1 / MR-1f / KS-1 prereg — unequal-mass LS πK amplitude: K*_J masses and Kπ width ratios (VERIFIED-REMEMBERED, rule 6) — 2026-10-13
Committed and pushed **before** any K*_J PDG/LASS value was opened in this session.

## Theory (KL-1 gate)
- Amplitude (CITED prior art: Lovelace 1968; Kawarabayashi–Kitakado–Yabuki PLB 28 (1969) 432 and PR 184 (1969) 1956; Ademollo–Veneziano–Weinberg PRL 22 (1969) 83; recalled, abstracts only re-read):
  A(π⁺K⁺→π⁺K⁺) = β Γ(1−α_ρ(t)) Γ(1−α_K(u)) / Γ(1−α_ρ(t)−α_K(u)).
- New step (ours): the intercepts are fixed by demanding that the dual zero line α_ρ(t)+α_K(u)=1 be exactly the CGW / MR-4 hidden-zero line s = mπ²+mK²: α_ρ(t)=½+α'(t−mπ²), α_K(u)=½+α'(u−mK²). **PROVED** (`PositiveGeometryEmergentSpaceTime.UnequalLS`, 6 thms, 0 sorry, axioms propext/Classical.choice/Quot.sound): `zero_line`, `zero_line_conv`, `mass_formula`, `kstar_relation`, `spacing`, `poch3`.
- Slope universality α'_K = α'_ρ is an ASSUMPTION (KKY require it for signature). α' = 1/(2(mρ²−mπ²)) = 0.8598 GeV⁻².
- Resulting intercepts (α_K(0) ≈ 0.289, α_ρ(0) ≈ 0.483) coincide with the KKY PCAC trajectories (seen in a search snippet while sweeping prior art; theory only, no K*_J target value) → the amplitude is KKY's; our addition is the hidden-zero derivation + Lean.
- SIMULATED (`scripts/kl1_theory.py`): equal/massless limit reproduces MR-1b exactly (5/16, 49/240) — consistency check.
- Gate verdict: **posable** (well-defined, fixed before data, no fitted parameter).

## Input count (strange sector)
- Free unit: mK = 0.4957 GeV (memory, MR-4 value). Extra input: Γ(K*(892)) as width normaliser (MR-1f only) → costs 1.
- Outputs: 4 masses (KS-1) + 3 width ratios (MR-1f) = 7 > 1 extra. Sector credit allowed.

## Memory audit (disclosed; hence rule-6 VR line, not blind)
- Recalled: K*(892) ≈ 892 MeV, Γ ≈ 50 MeV; K2*(1430) ≈ 1430, Γ ≈ 100–110, Kπ BR ≈ 50%; K3*(1780) ≈ 1780, Γ ≈ 160, Kπ BR ≈ 19%; K4*(2045) ≈ 2045, Γ ≈ 200, Kπ BR ≈ 10%. AVW relation mK*² − mK² ≈ mρ² − mπ² is textbook.
- Not computed before this prereg: the LS width ratios; the predictions below were fixed by the theory script alone. No tuning.

## Predictions (fixed)
| Obs | LS prediction |
|---|---|
| m(K*) | 0.9095 GeV (AVW prior art; reported, not scored) |
| m(K2*) | 1.4108 GeV |
| m(K3*) | 1.7758 GeV |
| m(K4*) | 2.0776 GeV |
| R_J = Γ(K_J*→Kπ)/Γ(K*→Kπ) | computed by `kl1_theory.pred` at each source's own masses (V1, primary); at LS masses (V2): R2 = 0.8949, R3 = 0.5776, R4 = 0.3649 |

Width formula: Γ_J ∝ G_J q_J /((2J+1) m_J²), G_J = P_J-Legendre coefficient of the u-pole residue, t = −2q²(1−cosθ). Γ(K*→Kπ) = Γ_tot(K*) (BR ≈ 100%).

## Sources (≥2)
- S1: PDG 2026 averages (pdgLive / listings): mass, Γ_tot, Kπ BR (charged/neutral: use the PDG "K*(J) mass" headline; if separate, the neutral one, stated in advance).
- S2: the single most precise individual Kπ partial-wave measurement listed by PDG with its own mass, width and BR for each state (expected LASS/ASTON 88 or similar). If S2 lacks a BR, use its own m, Γ with PDG BR and flag "partly dependent".
- K*(892) normaliser: PDG 2026 for both.

## Rules
- **KS-1 (masses K2*, K3*, K4*):** σ² = (0.05·m²_pred)² + (2 m σ_m)² on m². PASS per state if |m²_data − m²_pred| ≤ 2σ in both sources; FAIL if >3σ in either; else INCONCLUSIVE. Rung PASS if all three PASS.
  Null: m² uniform in [m²_{J−1,pred}, m²_{J+1,pred}] (K4*: [m²_3, m²_3 + 2/α']); f = fraction within ±2σ. Discriminating if f ≤ 0.3.
- **MR-1f (R3, R4 primary; R2 reported):** σ_th = (30% ⊕ level allowance 10%·(J−1)) × prediction; data error by MC (uncorrelated); systematic sc = |V1−V2|/2. z = (R_data − R_V1)/√(σ_th²+σ_d²+sc²). PASS if |z| ≤ 2 for K3* and K4* in both sources; FAIL if |z| > 3 in either; else INCONCLUSIVE. Well-posed only if Γ/m < 0.25 and BR rel. err ≤ 0.5.
  Null: log-uniform random prediction in [R_data/10, 10 R_data]; f = fraction with |z| ≤ 2. Discriminating if f ≤ 0.3.
- Credit (rule 6, VR line): KS-1 PASS & discriminating → 0.5; MR-1f PASS & discriminating → 0.5; non-discriminating → 0.25 each. No blind credit (memorised).
