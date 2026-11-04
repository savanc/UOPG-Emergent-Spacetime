# FR-MU result (frontier rung 1): μ_n/μ_p — 2026-10-16
Prereg + locked checker (sha256 69852d5b…) + planted pair: 95f9a83, pushed before the measured value was fetched.

## Verdict: **NUMEROLOGY** (in band; not significant after trials). Credit proposed 0.

| | value |
|---|---|
| Construction prediction (N_c = 3, anomaly-fixed charges) | **−2/3 = −0.666667** |
| Measured: CODATA 2022, https://physics.nist.gov/cgi-bin/cuu/Value?munsmup (fetched 2026-10-16 after the prereg) | **−0.684 979 35(16)** |
| Relative deviation | 2.673 % (band 1/N_c² = 11.11 %) → in band |
| p_single (null uniform on [−1, 1]) | 0.0761 |
| p_corr (Šidák, TRIALS = 13) | **0.643** (bar 0.01) |

## Construction (FRONTIER-CONSTRUCTION)
- N_c quarks, colour antisymmetric ⇒ spin×flavour totally symmetric.
- Nucleon = the unique S = I = ½ state.
- μ_z = Σ Q_f (n_{f↑} − n_{f↓}), with a common quark magneton (isospin symmetry).
- Charges from the STRUCT-2 anomaly branch with y_L = −½: Q_u = (1 + 1/N_c)/2, Q_d = (−1 + 1/N_c)/2.
- Brute-force check (live): N_c = 1, 3, 5, 7 give 0, −2/3, −16/19, −10/11, all equal to the closed form R(N_c) = (3 − N_c(N_c+2))/(3 + N_c(N_c+2)).

## What is new / re-derivation
- The N_c = 3 value −2/3 is the 1964 SU(6) result (Beg–Lee–Pais). This is a **re-derivation**, fully non-blind: the value was known from memory.
- Possibly new, modest and unverified against the full literature:
  - the explicit finite-N_c closed form with anomaly-consistent charges (prior art uses these charges, e.g. hep-ph/9905334, and states R → −1 at large N_c);
  - the Lean fact that it coincides with the fixed-charge form −(N_c+1)/(N_c+3) **only at N_c = 3** (`acc_fixed_agree_iff`).
- The N_c = 1 value 0 reproduces the Bär–Wiese observation that at N_c = 1 the "quarks" are p and n (neutron neutral and pointlike in this model).

## Gates (experimentally established only)
- Nucleon spin ½ and isospin doublet: consistent.
- Quark charges at N_c = 3 equal the measured 2/3, −1/3 (DIS/R-ratio; the PDG quark-model review): consistent.
- The ratio is within the a-priori band of the CODATA measurement: no GATE-FAIL.
- Not addressed: the absolute moments, which need the quark magneton (BR-4: no scale).

## No-go assumptions changed (Exclusion)
- Sidesteps `R4Indep.mesonCharge_shift`: in baryons the individual Q_u and Q_d enter (via Q_u + Q_d = 1/N_c), not only differences.
- Uses `STRUCT2.accN_solution` charges.
- Does not touch `Separation.geometry_struct_separation`: the spin-flavour structure is not a positive-geometry object, so geometry↔STRUCT stays NO-LINK.
- New Exclusion row added.

## Anti-numerology
- Family: 1 formula.
- TRIALS = 13 (the ranked targets; selected knowing −2/3 ≈ data).
- As preregistered, NUMEROLOGY was certain once the value fell in band: an O(10 %) band inside an O(1) null cannot give p < 0.01. Even TRIALS = 1 gives 0.076.

## Lean
`PositiveGeometryEmergentSpaceTime.FRMU`: 6 theorems, 4 defs, 0 sorry, no native_decide, lint clean. No FRONTIER-AXIOM; the construction hypothesis is explicit (`SymIrrepME.Valid`), and the dependent results are conditional on it (lean/AXIOMS.md).

## Protocol deviation (disclosed in the prereg)
While testing, the checker's `live` mode ran once before the prereg. Its output was filtered out of my terminal and not seen. It contains only theory values; `score` first ran after the prereg and the CODATA fetch.

## Blocker
`NUMEROLOGY`. Reopen trigger: a zero-parameter computation of the correction terms (1/N_c², quark-mass/relativistic) that shrinks the band below ~0.1 %, or a blind dimensionless target.

## Lesson
Compute the best achievable p (band/null)^trials before choosing a frontier target. With current constructions, only targets whose zero-parameter theory band is ≪ 1 % can ever PASS.

## Credit
Proposal only: 0. CREDITS.md untouched.
