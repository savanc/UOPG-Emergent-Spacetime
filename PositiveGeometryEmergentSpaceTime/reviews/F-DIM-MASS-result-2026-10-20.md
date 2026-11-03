# F-DIM-MASS result (frontier gate check, 2026-10-20). Verdict: **GATE-FAIL-REPAIRED-AT-COST (P_b)**: the trunk LS model fails D = 4 unitarity at the physical pion mass; the only zero-parameter repair moves the Adler zero off the LO current-algebra line.
Written 2026-10-20 by Grok.
- Prereg: `prereg/F-DIM-MASS-2026-10-20.md`, commit 063378f (pushed alone).
- Lean: `PositiveGeometryEmergentSpaceTime.FDimMass`.
- The LS amplitude is a **model**. GATE-FAIL here means the trunk model fails at physical m_π, not that physics does.

## Guard (hardened)
- There is no pass flag. `guard` runs inside every scoring function and, on every call, re-checks:
  - the checker's sha256 against the prereg;
  - that the prereg commit is an ancestor of origin/main.
- The only caches are keyed by the origin/main commit sha; `git fetch` runs once per process.
- **Before the push** (`guard_refusal.txt`):
  - CLI → `GUARD REFUSED … not an ancestor of origin/main`, exit 1.
  - The import-and-call test made two direct calls. Both were REFUSED (the second re-verified rather than reading a stored success). Pass-flag attributes present: none. Exit 2.
- After the push, both direct calls passed the guard.

## Inputs (fetched after the push; `masses.json` sha256 f94cd13b…0616a)
| Set | m_π | m_ρ | m_f2 |
|---|---|---|---|
| **S1** (PDG 2026) | π± 139.57039 MeV | ρ(770) 775.26 MeV (neutral, e⁺e⁻) | f₂(1270) 1275.4 MeV |
| **S2** | 139.57077 MeV (Trassinelli 2016, pionic N₂ X-ray) | 763.7 MeV (García-Martín et al. 2011 GKPY pole, Re √s) | 1267.5 MeV (Peláez–Rodas–Ruiz de Elvira dispersive pole, as quoted in arXiv:2512.09033) |

- **Digit audit:** before the prereg the values were recalled to 2 significant figures only. No value entered any file before the push.
- **Deviation (disclosed):** the prereg named Daum 2019 as its pionic-atom example, but Daum 2019 is a π→μν kinematics measurement. The actual pionic-atom X-ray value (Trassinelli 2016) was used instead. The shift is 4·10⁻⁴ MeV and has no effect on any verdict.

## Planted pair
- **Planted, recovered:**
  - massless trunk → D ≤ 4, with D = 4 positive for N ≤ 40 (reproduces F-DIM′);
  - NS model → D ≤ 10, with D = 4 positive.
- **Broken (Lean-excluded):** the massless trunk asked for D ≤ 26 gave D ≤ 4, so it was REJECTED as required.

## Live (`fdimm_output.txt`)
| Model | α₀ (S1 / S2) | level-1 D_c (S1 / S2) | D = 4 positive to N ≤ 40 |
|---|---|---|---|
| P_a baseline (Adler at s = t = m_π²) | 0.48325 / 0.48272 | 3.8675 / 3.8634 | **No / No** → GATE-FAIL (trunk model) |
| P_b Adler at s = t = 0 | 0.5 / 0.5 | 4.0247 / 4.0263 | **Yes / Yes** → PASS |
| P_c Adler at the symmetric point | 0.47742 / 0.47670 | 3.8221 / 3.8165 | No / No → FAIL |
| F5 ρ–f₂ trajectory | 0.41398 / 0.43005 | 3.5366 / 3.5773 | No / No → FAIL |
| F6 daughter shift, F7 Coon | — | — | AUTO-FAIL (fitted parameter) |

The report-only D-scan labels "FORCED-EQUALITY D=3" are artefacts of the scan starting at D = 3. They are not forcing.

## Verdict
**GATE-FAIL-REPAIRED-AT-COST (P_b)**. Every prereg prediction held:
- the baseline fails, with D_c ≈ 3.87;
- P_b passes at all levels N ≤ 40 (levels 2–40 were blind);
- P_c and F5 fail.

**The cost of P_b** (`FDimMass.weinberg_line_iff`): the LS zero line coincides with the LO current-algebra Adler line s + t = 2m_π² *only* for the baseline. P_b puts the zero at s + t = 0, off that line by O(m_π²).

So, within the LS family, Adler consistency at LO plus a physical m_π > 0 plus D = 4 tree unitarity cannot all hold at once. This is proved in Lean at level 1, and the checker confirms the baseline failure in both input sets.

## Tags
- `GATE-FAIL` (trunk model, CITED: Bianchi et al. noted that α₀ < ½ gives D_c < 4).
- Repair: AT-COST, 1 of 5 declared fixes; no significance claim.
- New relative to the cited work:
  - the exact N ≤ 40 test with physical inputs from two sources;
  - the declared fix family;
  - the Weinberg-line uniqueness (Lean).

## Lean (`PositiveGeometryEmergentSpaceTime.FDimMass`, 10 theorems + 2 defs, 0 sorry, standard axioms)
- `weinberg_line_iff`
- `baseline_spin0_D4`: the D = 4 spin-0 coefficient on the Adler line is m²(m²−½)
- `baseline_gate_fail`
- `lsCritDim_lt_four_iff`
- `adlerZero_spin0_D4` (16m⁴/3), `adlerZero_level1_pass`
- `symmetric_spin0_D4`, `symmetric_level1_fail`
- `level1_residue_quadratic`
- bundle `fdimmass_gate`

## Exclusion
- New row: `FDimMass.fdimmass_gate`. The massless trunk cannot be extended to physical m_π inside the LS family without giving up either D = 4 unitarity or the LO Adler line.
- Assumption changed: `FDim.fdim_bound_not_forced` (m_π = 0).

## Blocker / reopen
`GATE-FAIL` (trunk model). Reopen with:
- a non-LS dual-resonance pion amplitude with an O(m_π²) Adler line and no fitted parameter;
- a unitarisation (`UnitarisedLS`-type) that restores positivity without new parameters;
- a positive-geometry derivation that fixes a mass-dependent daughter structure.

## Lesson
A gate check whose headline is analytic (α₀ < ½ ⇒ D_c < 4) is only worth a rung if paired with a declared, finite fix family. Here the open part was whether *any* zero-parameter fix exists, and at what cost.

## Credit (proposal only)
0.
