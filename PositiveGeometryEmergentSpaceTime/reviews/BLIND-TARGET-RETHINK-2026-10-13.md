# Blind-target rethink for the last OP-2 0.5 — 2026-10-13
Tags: [CITED] = read today; [MEMORY] = recalled; [ASSESS] = judgement. No target values were read.
Contamination disclosure: two search snippets displayed physical-point lattice ρ and K*(892) pole values and the phrase "g_ρππ weakly m_π-dependent" (Yu et al. 2311.03903). No heavy-mass numbers were seen.

## 1. Why the candidates failed (diagnosis) [ASSESS]
| Failure mode | Rungs | Root cause |
|---|---|---|
| Memory contamination | MR-1 (f2), MR-2e (large-N_c), FZ-1 (LET), BH-4/EW-1 (GR/SM) | Physical-point PDG quantities of famous sectors are memorised. The prediction overlaps a textbook result. |
| < 2 quantitative sources | MR-1c/1d/1e/1f, MR-5 (Kη), MR-8 | High-spin/obscure states have one model-dependent analysis, or none. |
| Theory not ready | MR-6, MR-8, FZ-2, πη | No zero/LS structure, or no fermionic dual amplitude. |
| Kinematic-only zero | FZ-0, MR-7 | The zero carries no dynamics (bridge ⇒ trivial), or it is crossed by a pole. |
| Shared data / same zero | MR-2/2d/2d1 | One zero tested several times. |

**Structural lesson:**
- At the physical point, everything our machinery can say is either memorised or has a single source.
- The **quark-mass axis** escapes both problems. Our predictions (LS ladder, MR-2/MR-4 zeros) are functions of (m_π, m_K, f_π, m_ρ) at *any* quark mass.
- Lattice collaborations publish amplitudes at several unphysical masses, from independent groups. Nobody, including us, memorises those amplitudes or subthreshold numbers.
- Each ensemble's inputs (m_π, m_K, f_π, m_ρ on that ensemble) are declared per-ensemble inputs, a units/scale ledger with no fit.

## 2. Candidate classes
Sources are [CITED] from today's search unless marked [MEMORY].

| # | Target | Class | Theory readiness | Blindness | ≥2 sources | Null discrimination | Cost |
|---|---|---|---|---|---|---|---|
| **1** | **LAT-2: MR-4 πK zero line at unphysical m_π.** Evaluate the lattice-fitted πK amplitude (K-matrix/ERE in s, p, d waves) analytically continued to the subthreshold line s = M_π² + M_K², per ensemble. Score r = \|A_line\|/\|A_ref\| vs the MR-4 band. | (c)+(a) | High: MR-4 code + PiKZero Lean reused; masses become per-ensemble variables. **Gate item:** confirm which isospin combination the line constrains. I=3/2-only is ideal; if I=1/2 is needed, K* ensembles are required. | **High.** Subthreshold values of lattice K-matrices are never quoted; we have no memory of them. | I=3/2: Dawid et al. 2502.17976 (CLS, 4 ensembles incl. near-physical, s/p/d K-matrices); Fu et al. 2601.01205 (staggered, physical, a/r/P); [MEMORY] HadSpec πK 2014/2019 (m_π ≈ 391, 239). I=1/2 p-wave: 2603.16266 (8 ensembles, 135–320 MeV). | Good: the zero must hold at *every* mass, so the null rate compounds across ensembles. | Medium (continuation systematics) |
| 2 | LAT-1: LS/KSRF ρ coupling vs m_π (g_ρππ or Γ_ρ/m_ρ from the LS residue, per-ensemble m_ρ, f_π) | (c) | High (MR-1b LSResidue) | **Medium-low.** "g weakly m_π-dependent" was just read, and the KSRF value is memorised. | JHEP08(2025)064 (9 ensembles); HEFT 2311.03903; [MEMORY] HadSpec, ETMC, CLS | Medium | Low |
| 3 | LAT-3: MR-2 massive ππ zero at P with lattice I=2 + I=1 + I=0 amplitudes at heavy m_π | (c) | Medium: needs all isospins at the same ensemble (I=0 σ is hard) | High | HadSpec (I=0/1/2 at 391/239) [MEMORY], Dawid (I=2 only) | Good | Medium-high |
| 4 | TS-1: time-stamped predictions (register now, score on release): LS ρ₃/f₄ couplings and the MR-4 line at HadSpec/CLS forthcoming ensembles; BESIII/LHCb high-spin branching fractions | (b) | High | **Perfect by construction** | Depends on future releases | Good | Low now, payoff delayed (months to years) |
| 5 | Fresh experimental BFs (BESIII/LHCb 2025-26 new resonances) | (a) | Low: no LS prediction for exotic/charm states | High | Often 1 | – | High |
| 6 | KK I=1, ηπ a₀(980) couplings | (c) | Low (MR-5: no CGW-form zero) | High | 1 | – | – |
| 7 | Positive geometry on lattice: EFT-hedron positivity of lattice LECs/amplitudes vs m_π | (d) | High | Medium | many | **Poor:** bounds are inequalities that QCD satisfies trivially | Low |

## 3. Recommendation
- **Top: LAT-2**, gated. Steps:
  1. Theory gate (no data): derive which isospin amplitude the MR-4 line constrains (Lean, reusing PiKZero). Show that the line value is computable from s/p/d K-matrix parametrisations (continuation below threshold, distance 2M_πM_K, no left-hand cut crossing; check the u-channel cut position per ensemble).
  2. Structure check (digit-masked): confirm that ≥2 sources publish parametrisation coefficients plus per-ensemble masses.
  3. Prereg (per-ensemble scoring, band = MR-4 band, null = MR-4 null compounded over ensembles), committed and pushed.
  4. Then read and compute.
- **Counting:** per-ensemble masses are declared inputs. One blind dimensionless prediction counts once (+0.5 if it passes on ≥2 sources, under the approved cross-sector rule), not once per ensemble.
- **Fallback: LAT-3**, if the line needs I=1/2 data with too few sources.
- **Parallel, cheap: TS-1.** Register predictions now in `reviews/TS-1-...`, timestamped by git commit and push, scored only after release. This creates the first truly unforgeable blind targets. It earns no credit until scored.
- Deprioritise LAT-1 (contaminated) and class (d) (non-discriminating).
