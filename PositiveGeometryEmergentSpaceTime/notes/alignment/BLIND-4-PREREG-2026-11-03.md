# BLIND-4 prereg: blind Lean statement of the MR-1f width formula (2026-11-03)

Authority: author approved (2026-11-03). This is **Phase 1 (prose only)**. It is committed and pushed **before** any of the following is opened: lean/PositiveGeometryEmergentSpaceTime/UnequalLS.lean, lean/PositiveGeometryEmergentSpaceTime/DecayZeroNoGo.lean, lean/AxUnequalLS_output.txt, scripts/kl1_theory.py, scripts/kl1_data_check.py and their outputs/json, and any MR-1f blueprint row. Credit is not touched (MR-1f VR 0.25).

**Prose sources.** The papers have no MR-1f prose: Paper II names it only in a generated ledger row. The statement was therefore written from the rung records:
- prereg/KL-1-MR-1f-KS-1-prereg-2026-10-13.md (Theory, Predictions, "Width formula");
- reviews/KL-1-MR-1f-KS-1-result-2026-10-13.md.

**Disclosed contamination.** `UnequalLS.poch3` was read in BLIND-3 Phase 2; it is not reused here. Earlier summaries said "G_J Legendre residue". No width code was read.

**Module.** `lean/PositiveGeometryEmergentSpaceTime/Alignment/Blind/Mr1fBlind.lean` (8 thm, 11 def; over ℝ). It is not imported by `PositiveGeometryEmergentSpaceTime`, so the main totals stay 1378/798. Compiled with `CAP_ANON_GB=4 memrun2.py lake env lean`: EXIT 0, peak anon 0.54 GB. 0 sorry, 0 native_decide.

| Statement | Content | Reading chosen blind |
|---|---|---|
| `gamma_ratio` | Γ(1−a) = (−1)^J (a)_J Γ(1−a−J) for a ∉ −ℕ | The Gamma-ratio half of the u-pole residue. |
| `res` (def) | residue at α_K = J as a function of a = α_ρ(t): (a)_J/(J−1)! | The pole factor (−1)^J/(J−1)! of Γ(1−α_K) is standard; its limit is **not** formalised. The common 1/α′ and sign drop out of R_J. |
| `alphaRho_tOf` | α_ρ(−2q²(1−x)) = A + Bx with B = 2α′q², A = ½ − α′mπ² − 2α′q² | t = −2q²(1−cos θ) (prose). |
| `Gtop`, `Gtop_vals` | G_J = B^J 2^J (J!)²/((J−1)!(2J)!): B, 2B²/3, B³/5, 4B⁴/105 | G_J = the **top** (P_J) Legendre coefficient of the degree-J residue polynomial. |
| `legendre_J1`…`legendre_J4` | full Legendre decomposition of `res J (A + Bx)` for J = 1..4, with top coefficient `Gtop J B` | P_0..P_4 explicit. |
| `m2J`, `alphaK_m2J` | m_J² = mK² + (J−½)/α′ satisfies α_K(m_J²) = J | pole position |
| `q2`, `width`, `ratio`, `apOf` (defs) | q² = (m²−(mK+mπ)²)(m²−(mK−mπ)²)/(4m²); Γ_J = G_J q_J/((2J+1)m_J²); R_J = Γ_J/Γ_1; α′ = 1/(2(mρ²−mπ²)) | Γ_J up to a J-independent constant (prose "∝"). |

**Blind numeric expectation** (pre-registered here and checked in Phase 2 in Lean). At mπ = 0.13957, mρ = 0.77526 and mK = 0.4957 GeV, the prose values are R2 = 0.8949, R3 = 0.5776 and R4 = 0.3649 (V2, LS masses).
- **SIMULATED: a blind exact-rational Python re-computation.** An inline throwaway, not a repo script; run id BLIND4-PY-2026-11-03-r1. It gives 0.894891, 0.577637 and 0.364884, which reproduce all three prose values to 4 d.p.
- **Planted wrong reading:** the x^J coefficient instead of the P_J coefficient. It gives 1.342, 1.444 and 1.596.

**Phase 2** (after this push) opens the originals. It adds:
- `Blind/Compare/MR1F.lean`, with the comparison and the sanity theorems (known value, planted wrong case, non-vacuity, and Lean interval proofs of the three V2 ratios);
- blueprint rows;
- an axiom audit;
- coverage counts.
