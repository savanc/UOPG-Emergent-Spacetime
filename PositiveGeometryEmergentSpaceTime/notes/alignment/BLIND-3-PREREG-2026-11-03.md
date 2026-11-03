# BLIND-3 prereg: blind statements for the credited rungs MR-4, KL-LAT (+KL-LAT2, KS-1 masses) and MR-2 (2026-11-03)

Authority: author approved (2026-11-03). This is **Phase 1 (prose only)**. It is committed and pushed **before** any of the following is opened: lean/PositiveGeometryEmergentSpaceTime/PiKZero.lean, UnequalLS.lean, KLPhi.lean, MassiveZero.lean, DecayZeroNoGo.lean, their Ax*_output files, their blueprint rows, blueprint/src/content.tex and graph/theorems.json.

**Prose sources.**
- These rungs have almost no prose in the papers: Paper II mentions them only in generated ledger rows. The blind statements were therefore written from the rung records:
  - reviews/MR-4-result-2026-10-13.md and reviews/MR-4-prereg-2026-10-13.md;
  - prereg/MR-2-massive-hidden-zero-2026-10-12.md and reviews/MR-2-result-2026-10-12.md;
  - prereg/KL-1-MR-1f-KS-1-prereg-2026-10-13.md, prereg/KL-LAT-prereg-2026-10-13.md, reviews/KL-LAT-result-2026-10-13.md, reviews/KL-LAT2-gate-2026-10-13.md (Theory gate) and reviews/KL-1-MR-1f-KS-1-result-2026-10-13.md.
- **Disclosed contamination.** These records name the original theorems (for example `dress_zero_at_P`, `poly_zero_iff`, `zero_line_conv`, `mass_formula`). Some blind names reuse them, but none of the theorem bodies were read.
- Lean modules exist for all three rungs (checked by file name only): PiKZero, UnequalLS, KLPhi, MassiveZero. DecayZeroNoGo exists for MR-1f.

**Modules** (`lean/PositiveGeometryEmergentSpaceTime/Alignment/Blind/`). They are not imported by `PositiveGeometryEmergentSpaceTime`, so the main totals stay 1378/798. Each was compiled with `CAP_ANON_GB=4 memrun2.py lake env lean` (EXIT 0, peak anon about 0.5 GB). 0 sorry, 0 native_decide.

| Rung | Module | Blind statements (over a field K, char 0) | Readings chosen blind |
|---|---|---|---|
| MR-4 | `Mr4Blind` (9 thm, 2 def) | `line_s_sub_u`, `line_nu`: on s = Σ = Mπ²+MK², s − u = t and ν = t/(4mK). `lo_closed`: the LO F^{3/2} equals (Σ − s)/(2F²). `lo_zero_on_line`, plus the converse `lo_ne_zero_off_line`. `line_iff_dot_zero`: for any symmetric bilinear form, s = Σ ⇔ p·q = 0, for **any** masses, not only the equal-mass limit. `line_restriction`: F⁺ − F⁻ at x = κτ equals g0 + g1τ + g2τ² + g3τ³, with the prereg coefficients. `kappa_line`: κ = mπ/(4mK). | Σ, on-shell s+t+u = 2Σ, ν = (s−u)/(4mK). F^{3/2} = F⁺ − F⁻, truncated at τ-degree 3. Not blinded: `bdm_g0/1/2` (the BDM formulas are not in the prose). |
| MR-2 | `Mr2Blind` (8 thm, 2 def) | `dress_zero_P`, and `dress_zero_P_nosym` (symmetry is **not needed**). `fpoly_on_line`. `poly_zero_iff`: for M ≠ 0, zero on s+t = 2M² ⇔ a2 = 2a1 ∧ 4a1+2a3+a4 = 0. `dress_poly_P`: A(P) = M⁴[(a2−2a1) + (4a1+2a3+a4)]. `lo_zero_P` (Weinberg). `lo_dress`: LO ordered f = (s+t−2M²)/(2F²) dresses to Weinberg, off shell too. | Dressing A = f(s,t) + f(s,u) − f(t,u). O(p⁴) basis a1(s²+t²) + a2 st + a3 M²(s+t) + a4 M⁴. Not blinded: G¹/F¹ values at P. |
| KL-LAT / KL-LAT2 / KS-1 (algebra) | `KlLatBlind` (13 thm, 2 def) | `zero_line`: α_ρ(t)+α_K(u) = 1 ⇔ s = mπ²+mK². **`zero_line_conv` (blind finding):** with common slope, "dual zero line = hidden-zero line" fixes only the **sum** a + b = 1 − α'(mπ²+mK²) of the intercepts. The split (½ at each pseudoscalar mass²) is extra input (`split_not_forced`, `stated_sum`). `slope`: α' = 1/(2(mρ²−mπ²)). `mass_formula`: α_K(m²) = J ⇔ m² = mK² + (2J−1)(mρ²−mπ²). `kstar_relation`, `k2star`, `spacing`. `phi_relation`, `equal_spacing`, `phi_from_kstar` (GMOR m_ηs² = 2mK² − mπ² as input). | K*_J is the J-th recurrence on the K trajectory. Not blinded: `poch3`. MR-1f width formula: not blinded (lower priority; see the result note). |

**Phase 2** (after this push) opens the originals. It adds:
- blueprint rows (prose vs literal Lean);
- Sanity modules (known values, a planted wrong case, non-vacuity, ties);
- `Blind/Compare/{MR4,MR2,KLLAT}.lean`;
- a batched axiom audit.

Credit is not touched in either phase; any finding is a proposal only.
