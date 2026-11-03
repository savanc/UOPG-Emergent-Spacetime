# Direction review — the last OP-2 0.5 (score 2.5/3) — 2026-10-13
Tags: [ASSESS] judgement, [PROVED]/[CITED] as before, [MEMORY] recalled. No target values were read.

## 1. Lessons [ASSESS]
| Dead end | Rungs | Structural cause |
|---|---|---|
| Memory contamination | MR-1 f2, MR-2e, FZ-1 (LET), BH-4, EW-1 | Famous physical-point numbers, or textbook overlap |
| Single / no source | MR-1c–1f, MR-5, MR-8 | High-spin and exotic states have one analysis |
| Circular lattice fits | LAT-2, LAT-3 | Lattice fits impose Adler zeros, or cannot locate them |
| Kinematic-only zeros | FZ-0, MR-7 | The bridge or pole structure makes the zero trivial or ill-defined |
| Subthreshold weakness | LAT-2/3, MR-2 family | Our zeros sit where data constrain least |
| Scale no-go | OP-2 | Geometry fixes ratios, never the unit, so one dimensionful input per sector |

**What succeeded (MR-1b, MR-4):**
- Blind targets.
- **Dispersive (Roy / Roy–Steiner) data**, which are model-independent and come with ≥2 independent analyses.
- Physical or near-threshold region.
- A quantity **fixed by geometry with no free parameter**: an LS residue ratio, or a zero line.
- Quantities nobody memorises: subthreshold C_ij, high-spin couplings.

The winning recipe is a geometry-fixed number, compared against dispersive analyses, in a channel or parameter that is rarely quoted.

## 2. Attack the premise: is OP-2 the right milestone? [ASSESS]
- OP-2 asks for ≥3 *independent* observables. MR-2 (0.5) and MR-4 (1) are both hidden zeros, so their evidence is correlated in theory (the M3 combination is shared).
- A further zero would add a count without adding independence.
- **Proposal (the author decides):** the final 0.5 should come from a **third observable class**, neither LS couplings nor hidden zeros. The milestone would then read: "3 classes, each with ≥1 blind pass". That is stricter and more meaningful.
- Observables our proved machinery fixes with zero fits, beyond zeros and couplings:
  - (i) Threshold parameters of higher partial waves (LS amplitude, Regge/ρ-exchange dominated, so loop corrections are small).
  - (ii) Strange-sector LS couplings (K* ladder).
  - (iii) Positivity inequalities.
  - (iv) Kerr/g=2 multipoles.
  - (v) Adler-zero positions in Roy solutions.

## 3. Ranked directions
| # | Direction | Class | Theory readiness | Blindness | ≥2 sources | Null discrimination | Novelty | Cost | P(+0.5) |
|---|---|---|---|---|---|---|---|---|---|
| **1** | **TH-1: LS threshold-parameter ratios in high ππ waves.** F-wave a₃^1, D-wave slopes b₂^0, b₂^2, P-wave slope b₁ as dimensionless ratios (e.g. M_π⁴ a₃/M_π² a₁ type) from the LS amplitude with m_ρ, f_π, m_π, vs Roy analyses | new: threshold params | High: MR-1b LS amplitude; threshold expansion is exact algebra (Lean-able). High waves are dominated by t/u-channel Regge exchange, where LS is most reliable. | Medium-high. [MEMORY] S-wave a₀ and roughly the D-wave a₂ magnitudes are known, so **score only on F-wave and slope parameters**, which are not memorised (disclosed). | CCL 2001 (Roy), GKPRY 2011 (Madrid GKPY), Kamiński et al. (structure check) | Good if ratios span decades (log-uniform null) | Moderate (resonance saturation of higher waves is old; the exact LS/dual version + Lean is new) | Low | **~0.35** |
| 2 | KS-1: dual πK amplitude (K* trajectory) predicting K₂*, K₃*, K₄* → Kπ coupling ratios (MR-1b strange analogue) | LS couplings, new sector | Medium: needs an Adler-consistent unequal-mass dual amplitude. Extra input (m_K* or common slope) costs 1 under the counting rule. | Medium. [MEMORY] K₂* Kπ BR roughly known, so score on K₃*, K₄*. | LASS/Aston 1988, Estabrooks 1978, Dalitz analyses (LHCb/BESIII) | Medium | Moderate-high | Medium | ~0.25 |
| 3 | πK threshold parameters (P/D/F waves) from the KS-1 amplitude vs BDM / Peláez–Rodas Roy–Steiner | threshold params, πK | Depends on KS-1 | **High** (never memorised) | BDM 2004, Peláez–Rodas 2020 | Good | Moderate | Medium (after KS-1) | ~0.25 (conditional on KS-1) |
| 4 | Positivity: LS-implied LEC inequalities with discrimination (narrow allowed wedge vs data) | inequality | High (M2 EFT-hedron) | Low-medium | many | **Poor:** QCD satisfies them trivially; the M2 history shows this | Low | Low | ~0.05 |
| 5 | Kerr multipoles / GW ringdown (BH-4) | Kerr/g=2 | High | Low (GR textbook) | LVK | – | Low | Medium | cap 0.25 |

## 4. Recommendation and gate plan
**Top: TH-1.** Gates, in order:
1. **Theory:**
   - Expand the MR-1b LS amplitude around threshold to get closed-form a_ℓ^I and b_ℓ^I for ℓ = 1, 2, 3 (sympy, exact).
   - Prove the projection algebra in Lean (Legendre projection of a polynomial in t at threshold).
   - Fix inputs exactly as in MR-1b: no new inputs.
2. **Method fitness (non-blind control, disclosed):** check the LS P-wave a₁^1 against KSRF expectations (known physics) to confirm normalisation. A mismatch > 30 % stops the rung.
3. **Digit-masked structure check:** confirm that ≥2 Roy-type sources tabulate a₃^1, b₂^0, b₂^2, b₁^1 with errors.
4. **Prereg (committed and pushed before reading):**
   - Targets: 3 ratios R₁ = b₁^1/a₁^1, R₂ = b₂^0/b₂^2, R₃ = a₃^1/a₁^1 (exact list fixed in prereg).
   - Band: LS 1/N_c ⊕ level band as in TS-1 (~30 %).
   - Null: log-uniform over 2 decades, discriminating if f ≤ 0.3.
   - PASS: ≥2 of 3 ratios within band on ≥2 sources.
5. Read the values and give the verdict.

**Fallback: KS-1 → πK thresholds (3).** The strange-sector LS amplitude unlocks two blind targets at once.

**Milestone note:** if the author adopts the "third class" reading, TH-1 qualifies (threshold parameters). Further zeros (TS1-6/7/8) would remain corroboration only.
