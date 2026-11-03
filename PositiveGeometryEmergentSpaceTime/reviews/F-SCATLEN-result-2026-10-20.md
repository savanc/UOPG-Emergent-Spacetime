# F-SCATLEN result (frontier, 2026-10-20) — verdict **FAIL-WORSE-THAN-LO** for P_b: the D = 4 unitarity repair of the LS pion amplitude is excluded by ππ scattering lengths
Written 2026-10-20 by Grok. Prereg `prereg/F-SCATLEN-2026-10-20.md` commit 23a24b1 (pushed alone). Lean `PositiveGeometryEmergentSpaceTime.FScatLen`.
The LS amplitude is a MODEL: the failure is the repair model's, not physics'.

## Guard
- Hardened guard, unchanged from F-DIM-MASS.
- Refusal proof before the push (`guard_refusal.txt`):
  - before the local commit: "no commit", exit 1;
  - after the local commit: CLI → "prereg commit 23a24b151 is not an ancestor of origin/main", exit 1;
  - import test → both direct calls REFUSED, pass-flag attributes [], exit 2.
- After the push both calls passed the guard.

## Inputs (all fetched after; `inputs.json` sha256 41505f0a…9c7a)
- **f_π:**
  - F1 = |V_ud|f_π = 127.13(13) MeV (PDG review, π→μν) ÷ |V_ud| = 0.97367(32), giving F = 92.325(99) MeV;
  - F2 = FLAG 2024 / PDG preferred f_π = 130.2(1.2), giving F = 92.07(85) MeV.
- **Data:**
  - X1 = NA48/2 combined Ke4 + cusp: a₀⁰ = 0.2210(62), a₀² = −0.0429(52). The quoted 92% correlation is ignored per the prereg (disclosed).
  - X2 = E865 a₀⁰ = 0.216(14) plus DIRAC |a₀ − a₂| = 0.2533(110).
- **CGL rival:** 0.220(5), −0.0444(10).
  - Sources: CGL PRL 86 (2001) 5008 / NPB 603 (2001) 125; also quoted in NA48/2 EPJC 70 and DIRAC PLB 751.
- **Masses:** sets S1 and S2 from F-DIM-MASS.
- **Digit audit:** the prereg recall was masked to one significant digit. All fetched values agree with the masked recall.
- **Disclosed deviations:**
  - F1 cites the PDG review's experimental |V_ud|f_π, not a pdgLive "f_π" entry, because PDG's headline f_π is lattice-based.
  - DIRAC: the PLB 751 paper re-quotes the PLB 704 (2011) value, which is used here.

## Planted / broken
- Planted:
  - linear Weinberg gives (7, −2);
  - full LS on the Adler line with α′ → 0 gives (7, −2);
  - full LS with α₀ = ½ and α′ → 0 gives (12, 0);
  - all 4 classifier cases matched their expected class.
- Broken: "P_b reproduces Weinberg's 32π a₀² = −2" was REJECTED (computed value 0).

## Live
| Model | a₀⁰ | a₀² | a₀⁰ − a₀² | χ² X1 | χ² X2 | class X1 / X2 |
|---|---|---|---|---|---|---|
| LO (Weinberg) | 0.1591 | −0.0455 | 0.2046 | 99.9 | 36.8 | — |
| P_a (LS trunk) | 0.1655 | −0.0434 | 0.2089 | 79.9 | 29.8 | IMPROVES-BUT-EXCLUDED / MATCHES-LO → SPLIT |
| **P_b (repair)** | **0.3007** | **0 (exact)** | 0.3007 | **225.3** | **56.0** | **WORSE-THAN-LO / WORSE-THAN-LO** |
| CGL (ChPT + Roy) | 0.220 | −0.0444 | 0.264 | 0.10 | 0.92 | context |

- **P_b pulls:** X1 a₀⁰ +12.6σ and a₀² +8.2σ; X2 a₀⁰ +6.1σ and a₀⁰ − a₀² +4.3σ.
- **P_a pulls:** a₀⁰ −8.9σ (X1). Like LO, it misses the NLO (unitarity / chiral-log) increase of a₀⁰.
- **Lean (exact, all orders in α′):** P_b has a₀² = 0 exactly (`ls_adlerZero_a02_exact`), because V(0,0) = Γ(½)²/Γ(0) = 0.
  *Forward note 2026-10-20 (M7, approved by author approved (2026-10-20); [notes/NOTATION-AUDIT-2026-10-20.md](../notes/NOTATION-AUDIT-2026-10-20.md)): this exact zero rests on Mathlib's convention Γ(0) = 0 (`Real.Gamma_zero`, then `inv_zero`; `FScatLen.lsV_half_zero`, `FScatLen.lean:86-89`; disclosed in `lean/AXIOMS.md:350`). That is the correct value here, because 1/Γ is entire and vanishes at 0. But any `lsV` evaluation where a *numerator* Γ hits a pole would silently return 0 instead of a pole. The result stands; the dependence is now stated.*
- Linearised P_b gives a₀⁰ = (12/7) × LO (`lin_adlerZero_ratio`). The full LS curvature raises this a further ~10%.

## Verdict
- **P_b: FAIL-WORSE-THAN-LO in both independent datasets.**
- **P_a** (the trunk, already GATE-FAIL on unitarity): UNCLASSIFIED-SPLIT. This is a CITED/expected near-LO result, not new.

Combined with F-DIM-MASS, the only zero-parameter way to make the LS pion amplitude D = 4-unitary at physical m_π is excluded by measured scattering lengths:
- by >8σ (X1);
- with a₀² = 0 exactly versus −0.043 measured.

**Conclusion:** within the LS family, D = 4 tree unitarity at physical m_π and agreement with measured threshold ππ data cannot both hold.

## Tags
- **NO-GO** for the LS family with fixes P_a and P_b, using normalisation N1 (the only normalisation tried; 2 trials).
- Experiment-gated: SM / measured.
- Not numerology; no positive claim.
- CITED: Weinberg LO and CGL. The P_b exclusion and the exact a₀² = 0 are new (trivially simple).

## Prediction check
| Model | Predicted (probability) | Outcome |
|---|---|---|
| P_b | FAIL-WORSE (55%) | FAIL-WORSE ✓ |
| P_a | MATCH-LO (70%) | SPLIT (X1 shows a significant but insufficient improvement) |

## Exclusion
`FScatLen.fscatlen_threshold` + live: the F-DIM-MASS repair P_b is not physical. Reopen triggers:
- a dual amplitude with the Adler zero on the LO line, D = 4 unitarity, and no fitted parameter;
- loop (unitarised) LS.

## Lesson
A unitarity repair must be gated immediately against the cheapest established low-energy observable. Here the a₀² = 0 identity was visible in one line of algebra before any number was fetched.

## Credit (proposal only)
0.
