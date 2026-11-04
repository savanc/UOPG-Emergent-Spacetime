# PREREG F-RHOWIDTH: zero-parameter ρ width ratio Γ_ρ/m_ρ of the LS amplitude (N1 normalisation) vs KSRF and dispersive pole data
Written 2026-10-20 by Grok. Continuous mode; approved by author approved. STOP absent on origin/main at rung start.
This file is pushed ALONE, before any ρ pole, BW width or other new datum is fetched and before any checker computation.

## 1. Target and inputs (fixed)
- **Target:** the dimensionless ratio r = Γ_ρ/m_ρ.
- **POLE definition (fixed; this is the verdict definition):** m = Re √s_pole and Γ = −2 Im √s_pole.
  - Breit–Wigner (BW) values are REPORT-ONLY. A BW result never changes the verdict; it is reported as a definitional-sensitivity line.
- **Inputs that enter:** exactly x = m_π/m and f = F/m.
  - m_π = PDG π± 139.57039 MeV (`sims/fdimm/masses.json` S1).
  - F = f_π/√2 from `sims/fscat/inputs.json`: F1 (π→μν) is central; the F1/F2 spread and F1's error give the model error.
  - m is the pole mass of the dataset being compared. It sets α′ (P_a: α′ = 1/(2(m² − m_π²)); P_b: α′ = 1/(2m²)) and the phase space.
- **Width formula:** Γ = g²p³/(6πm²), with p = √(m²/4 − m_π²). So r = g²(¼ − x²)^{3/2}/(6π).
  - Convention: L = g ε ρ·π×∂π, so T¹ ≈ 2g²(t−u)/(m² − s).

## 2. Models and rival
- **LS P_a** (verdict model) and **LS P_b** (second trial, report). Amplitude A = λ[V(s,t)+V(s,u)−V(t,u)] with the F-SCATLEN normalisation N1, λ = −1/(2πα′F²); no fit.
  - g² is extracted NUMERICALLY from the full amplitude by the checker: (m² − s)T¹/(2(t−u)) at s = m²(1−10⁻²⁵).
- **Rival: KSRF**, g² = m²/(2F²), so r_KSRF = (¼ − x²)^{3/2}/(12πf²).
  - Kawarabayashi–Suzuki 1966; Riazuddin–Fayyazuddin 1966. Cited from 2 sources: the original papers, plus a modern review quoting KSRF (e.g. PDG / Ecker et al. resonance saturation).

## 3. Analytic pre-check (asked for; Lean `PositiveGeometryEmergentSpaceTime.FRhoWidth`, compiled BEFORE this prereg, no physical inputs)
- `dual_T1`: T¹ = 2λ(V(s,t) − V(s,u)).
- `stripped_block` and `stripped_at_pole`: the pole-stripped residue is −α_t. The limit step is CITED.
- `T1_pole_form`: g² = −λ.
- `gLS2_Pa`: g²_LS = (m² − m_π²)/(πF²).
- **`ls_ksrf_ratio`: g²_LS/g²_KSRF = (2/π)(1 − m_π²/m²).**
- `ls_below_ksrf` and `ls_ne_ksrf`: the ratio is below 2/π, which is below 1.
- `ls_ksrf_ratio_Pb`: for P_b the ratio is exactly 2/π.

**Conclusion, stated up front:** the LS residue with Weinberg/Adler normalisation does NOT reproduce KSRF. It is KSRF times a FIXED analytic factor (2/π)(1 − x²) ≈ 0.6 (masked).

Every outcome is therefore implied analytically by KSRF plus that factor:
- if KSRF fits the data, P_a must be low by ~40%;
- P_a can only beat KSRF if KSRF itself is ~40% high.

The rung is near-FOREGONE. Its content is the Lean theorem. The live run only quantifies the significance.

## 4. Contamination audit (masked)
**Memorised:**
- Γ_ρ ≈ 1.5×10² MeV;
- m_ρ ≈ 7.7×10² MeV;
- pole ≈ 7.6×10² − i 7×10¹ MeV;
- KSRF known to hold to ~10%.

**Already seen in this session:** an earlier rung's search output (F-DIM-MASS, ~13:2x BST) displayed the PDG ρ pole entries (García-Martín 2011 and Hoferichter 2024) and the PDG BW mass. These are therefore CONTAMINATED.

**Hand estimate made mentally before writing this prereg, using memorised inputs (disclosed):** Γ_KSRF ≈ 1.5×10² MeV, so the LS prediction is ≈ 0.6 × that.

**The bar is raised accordingly:**
- PASS requires BEATING KSRF in BOTH pole datasets, by the Bonferroni margin and with |z| ≤ 3;
- MATCH-KSRF is CITED/expected (implied by KSRF);
- there are no free choices left: definition, inputs, normalisation and formula are all fixed above.

## 5. Data sources (fetched AFTER the push)
- **D1 (verdict):** García-Martín, Kamiński, Peláez, Ruiz de Elvira 2011 (GKPY dispersive) ρ pole, as listed in PDG ρ(770) pole entries.
- **D2 (verdict):** Hoferichter et al. 2024 dispersive ρ pole (PDG "HOFERICHTER 24"); fallback Colangelo–Hoferichter–Stoffer 2019.
- Asymmetric errors are symmetrised (mean). σ_data(r) = r·√((δΓ/Γ)² + (δm/m)²).
- **BW (report-only):** PDG 2026 ρ(770) neutral (e⁺e⁻) mass and width.

## 6. Rule (fixed)
- **Trials:** 2 (P_a, P_b) vs KSRF. Bonferroni p < 0.01 gives Δχ² > 7.879.
- **Pull:** z = (pred − r_data)/√(σ_data² + σ_model²), where σ_model = √((2r·δF₁/F₁)² + (half F1/F2 spread)²).
- **Per dataset:**
  - BEATS-KSRF: z_K² − z_M² > 7.879 and |z_M| ≤ 3;
  - IMPROVES-BUT-EXCLUDED: same margin, but |z_M| > 3;
  - MATCHES-KSRF: |Δ| ≤ 7.879;
  - WORSE-THAN-KSRF: z_M² − z_K² > 7.879.
- **Overall** (D1 and D2 must agree, else UNCLASSIFIED-SPLIT):
  - PASS-BEATS-KSRF;
  - MATCH-KSRF (CITED/expected);
  - FAIL-WORSE-THAN-KSRF;
  - FAIL-EXCLUDED.
- **Verdict = P_a.** The planted cases below failing → ILL-DEFINED.
- **Planted:**
  - numerical residue equals the Lean formula (P_a toy; P_b toy) to 10⁻¹⁵;
  - KSRF width on a toy input equals 1/(96π);
  - 4 classifier cases.
- **Broken (already proved false, `FRhoWidth.ls_ne_ksrf`):** "the P_a residue equals KSRF". It must be REJECTED.

## 7. Prediction
- P_a: FAIL-WORSE-THAN-KSRF (~90%); FAIL-EXCLUDED (~5%); other (~5%).
- P_b: same.
- KSRF fits within ~2σ (~60%).

## 8. Guard and locks
- Hardened guard, as in F-DIM-MASS / F-SCATLEN: `guard` runs inside V, A, g2_ls, models, ratio_from_g2, predict, z, classify and overall.
- No pass flag; per-call hash and ancestry re-verification; caches keyed by sha only.
- The import test makes 2 direct calls, which must both refuse before the push. Before the push only `py_compile` was run.

Locked:
- `sims/frho/frho_checker.py` sha256 `13fc2ea35e545cf02e0b6999f3d70bb1911e4d7250897f3061b1507b5c62530b`
- `sims/frho/planted_cases.json` sha256 `d1f4b4aef59c654e038ff05a1215faaad208e5d13aa19fdeec18fc8a68e01b61`
- `sims/frho/import_guard_test.py` sha256 `6970041a275513c7a030d9fb049562dc6828f4058f5003463a7995c31eae3148`
