# F-RHOWIDTH result (frontier, 2026-10-20) — verdict **FAIL-WORSE-THAN-KSRF** (P_a; also P_b): with the Adler/Weinberg normalisation, the LS ρ coupling is (2/π)(1 − m_π²/m_ρ²) × KSRF, so Γ_ρ comes out ~38% too low
Written 2026-10-20 by Grok.
- Prereg: `prereg/F-RHOWIDTH-2026-10-20.md`, commit 63138a6 (pushed alone).
- Lean module: `PositiveGeometryEmergentSpaceTime.FRhoWidth`.
- The LS amplitude is a MODEL. A failure here is the model's, not physics'.

## Analytic pre-check (Lean, before the prereg; the main content)
- **Result:** g²_LS/g²_KSRF = (2/π)(1 − m_π²/m_ρ²) (`ls_ksrf_ratio`).
- **Strict bound:** the ratio is below 2/π, which is below 1 (`ls_below_ksrf`, `ls_ne_ksrf`). The LS residue does NOT reproduce KSRF.
- **Why:** normalising the LS amplitude to Weinberg's LO amplitude (N1) fixes λ, and λ then fixes the ρ residue. The ratio between the two is set by Γ(½)² = π, not by the factor 2 that KSRF needs.
- **P_b:** the ratio is exactly 2/π (`ls_ksrf_ratio_Pb`).
- **Cross-check:** the numerical residue taken from the full amplitude agrees with the Lean formula to 8+ digits in every dataset, and to 10⁻¹⁵ in the planted toy cases.
- **Caveat:** the step from the pole-stripped value to the limit at the pole is CITED (continuity), not proved in Lean.

## Guard
- **Refusal before the push** (`guard_refusal.txt`):
  - before the local commit: no commit, exit 1;
  - after the local commit: not an ancestor of origin/main, exit 1;
  - import test: both direct calls REFUSED, pass-flag attributes [], exit 2.
- **After the push:** both calls passed the guard. The planted cases were recovered and the broken case (LS residue equals KSRF) was REJECTED, giving 0.3056 against 0.5.

## Inputs (fetched after; `inputs.json` sha256 22a2497d…5c)
- **D1, verdict:** GKPY 2011 pole (763.7 − i73.2), so Γ = 146.4(2.1).
- **D2, verdict:** Hoferichter 2024 pole (762.5 − i73.2), so Γ = 146.4(2.2).
  - **Disclosed:** a PDG footnote says D2 updates D1, so the two are not fully independent.
- **Report-only:**
  - BW: PDG 775.26 / 147.4;
  - CGL 2001 pole. This was added as an extra report-only line that is not in the prereg; it does not affect the verdict.
- **Other inputs:** m_π = PDG; F1 and F2 from F-SCATLEN.
- **Contamination:** the pole values were already seen in this session (disclosed in the prereg). The masked recall agreed.

## Live
| Set | data r = Γ/m | KSRF r (Γ) | z_KSRF | P_a r (Γ) | z_Pa | P_b r (Γ) |
|---|---|---|---|---|---|---|
| D1 | 0.1917(28) | 0.1830 (139.7 MeV) | −3.1 | 0.1126 (86.0 MeV) | −28.2 | 0.1165 (89.0 MeV) |
| D2 | 0.1920(29) | 0.1823 (139.0 MeV) | −3.3 | 0.1121 (85.5 MeV) | −27.1 | 0.1160 (88.5 MeV) |
| BW (report) | 0.1901(10) | 0.1898 (147.2 MeV) | −0.24 | 0.1169 (90.7 MeV) | −65.7 | 0.1209 |
| CGL01 (report) | 0.1905(37) | 0.1822 | −2.2 | 0.1121 | −21.1 | 0.1160 |

**Verdict:** P_a is **FAIL-WORSE-THAN-KSRF** in D1 and D2; P_b is the same.

KSRF itself sits about 3σ low against the pole definition and about 0.2σ against BW. That is the definitional sensitivity, and it was fixed in advance in favour of the pole. It does not affect the LS verdict.

## Tags
- **NO-GO:** the LS family with N1 normalisation cannot match the ρ width.
- The outcome was FOREGONE analytically, as declared in the prereg. The Lean ratio is the content.
- **CITED:** KSRF. The LS/KSRF = 2/π statement is probably classical (Lovelace/Shapiro-era); this is not verified, so the novelty claim is unverified.
- **Not numerology.**
- **Combined with F-DIM-MASS and F-SCATLEN:** with Weinberg normalisation, the LS pion amplitude fails D = 4 unitarity (P_a), threshold data (P_b) and the ρ width (both).
  - Fixing the normalisation to the ρ instead (KSRF) would break the Adler/Weinberg LO matching by the factor π/2.

## Exclusion
- New row: `FRhoWidth.frhowidth_ratio`.
- Reopen trigger: a dual amplitude in which LO Adler matching and the ρ residue are independent (e.g. non-Γ(½)² soft constant), with no fitted parameter.

## Lesson
Check normalisation consistency between two low-energy theorems analytically first. If a single constant (here λ) fixes both, the rung reduces to a ratio of pure numbers (2/π against 1), and the data step is only significance bookkeeping.

## Credit (proposal only)
0.
