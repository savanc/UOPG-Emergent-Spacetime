# PREREG FR-MU (frontier rung 1): μ_n/μ_p from a spin-flavour-symmetric N_c-quark construction
Written 2026-10-16. Pushed ALONE (with locked checker + planted pair) before the measured value is fetched.

## Target (one real-particle, dimensionless)
Neutron-to-proton magnetic-moment ratio μ_n/μ_p. Source to be fetched AFTER this commit: CODATA 2022 (NIST), https://physics.nist.gov/cgi-bin/cuu/Value?munsmup.
SM ledger line: hadron static properties (a dimensionless baryon observable); secondarily it tests STRUCT-2 charges in the baryon sector.

## Construction (FRONTIER-CONSTRUCTION; precisely defined)
- State space: N_c quarks, each in the 4 spin-flavour modes {u↑, u↓, d↑, d↓}. Colour is totally antisymmetric, so the spin-flavour wavefunction is **totally symmetric** (bosonic occupation basis).
- Nucleon: the unique S = I = ½, S_z = +½ state with n_u = (N_c+1)/2 (proton) or (N_c−1)/2 (neutron).
- Operator: μ_z = Σ_f Q_f (n_{f↑} − n_{f↓}), in units of a common quark magneton (equal u/d constituent masses: isospin symmetry, a structural input).
- **Zero-parameter inputs:**
  - N_c = 3;
  - charges from the STRUCT-2 anomaly branch with lepton doublet y_L = −½: Q_u = (1 + 1/N_c)/2, Q_d = (−1 + 1/N_c)/2 (= 2/3, −1/3 at N_c = 3);
  - the symmetric-irrep structure.
  - Nothing is fitted.
- **Lean:** the construction enters as explicit hypotheses (structure fields, not axioms): the symmetric-irrep matrix elements ⟨Σσ_z⟩ = 1 and ⟨Σσ_zτ_3⟩ = ±(N_c+2)/3. The checker verifies these by brute-force diagonalisation for N_c = 1, 3, 5, 7. The Lean theorems derive the ratio from these hypotheses together with STRUCT2.ACCN.

## Formula family and trials
- Family: the single closed form R(N_c) = (3 − N_c(N_c+2)) / (3 + N_c(N_c+2)) evaluated at N_c = 3, with no alternatives considered.
- Honest look-elsewhere count **TRIALS = 13**: the 13 targets ranked in notes/FRONTIER-RANKING-AR-2026-10-16.md, of which this one was selected *knowing* the textbook −2/3 is close to data.

## Theory band (a priori)
- Relative band **1/N_c² = 1/9 ≈ 11.1 %**.
- Justification: in the large-N_c spin-flavour expansion, ratios of nucleon matrix elements fixed by the contracted SU(4) symmetry receive corrections first at relative O(1/N_c²) (Dashen–Jenkins–Manohar; cf. hep-ph/9905334 for the isovector magnetic moment). The band is not chosen from the data gap.

## Null model and pass bar
- Null: μ_n/μ_p uniform on [−1, 1].
- p_single = (band width around the measured value)/2. p_corr = 1 − (1 − p_single)^13 (Šidák).
- PASS requires p_corr < 0.01.

## Verdict set (exhaustive)
- |pred − meas|/|meas| > 1/9 → **GATE-FAIL** (conflict with a precise measurement).
- In band and p_corr < 0.01 → **PASS** (frontier success candidate).
- In band and p_corr ≥ 0.01 → **NUMEROLOGY** (recorded, not credited).
- The construction cannot be made precise in Lean → **ILL-DEFINED**.
- Otherwise → **UNCLASSIFIED**.

## Expected outcome (stated in advance, honestly)
- With band 1/9 the band width is ≈ 0.15, so p_single ≈ 0.076 and p_corr ≈ 0.64.
- **NUMEROLOGY is expected whatever the measured value**, provided it lies in band. Even with TRIALS = 1, the bar p < 0.01 cannot be met with any O(10 %) theory band and a null of width O(1). This rung therefore tests the protocol and the Lean audit, not a discovery.

## Contamination disclosure
- −2/3 is the famous SU(6) quark-model result (Beg–Lee–Pais 1964), and I know μ_n/μ_p ≈ −0.685 from memory. The rung is a **re-derivation**, not blind.
- What may be new (to check, modest): the closed form at general N_c with anomaly-fixed charges, R(N_c) → −1 as N_c → ∞, and its Lean link to STRUCT-2.

## Protocol deviation (disclosed)
- While testing the checker I accidentally executed its `live` mode once, before this prereg. Its output was filtered out of my terminal by grep and not seen.
- `live` computes only the construction's own predictions (no measured data).
- `score` (the only mode that uses data) has not been run.

## Planted pair
sims/frmu/frmu_planted.txt:
- N_c = 3 with SM charges recovers μ_p = 1 and μ_n = −2/3 (exit 0);
- the S = 3/2 (Δ-like) state is rejected (exit 1).

## Locked checker
`sims/frmu/frmu_checker.py` sha256 `69852d5b92e017a2fe42a0e8ca0f330f2d0dbba0168c84796d05ce9374793fcf`.
