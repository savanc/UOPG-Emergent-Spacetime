# COS-1e′ result: flat spin-2 exchange wavefunction — outside the pre-registered categories; closest to FAIL (no robust physical zero) (2026-10-13)

Prereg: `prereg/COS-1e-prime-spin2-exchange-gate-2026-10-13.md` (519b20e; data cells: none; one exploratory sympy step before the prereg was disclosed). Script: `sims/cos1e/cos1e_spin2.py` → `_output.txt`. The inflaton-leg version (COS-1e proper) was **not run**: it was judged too costly to do reliably (reason logged).

## Results
- **T1:** the residue-matched instantaneous kernel is
  I = [(Y²−X²)a₀₀b₀₀ + Y²(a₀₀ tr b_⊥ + tr a_⊥ b₀₀) − 4Y² a_{0⊥}·b_{0⊥}]/(2Y⁴).
  It keeps an explicit X², so the residue does **not** fix the off-shell lift. This differs from spin-1, where κ was fixed.
  The full construction (TT exchange plus I) reproduces the Lorentz amplitude N/(Y²−X²) at E = 0. Checked at 200 points with negative-energy null legs: max rel. dev. 2.9e−10.
- **T2:** sampling 10⁵ physical points shows ψ is essentially positive (attractive gravity) for every lift:
  - Symmetric lift −X_L X_R and the c = ±1 family: ψ > 0 at 100 % of points. The symmetric lift's minimum ψ/E is 4.6e−5 > 0.
  - Asymmetric lifts X_L² and X_R²: negative at only 0.01 % and 0.05 % of points.
  - Sign disagreement between lifts is ≤ 0.05 %.

## Verdict
The outcome does not fit any pre-registered category:
- Not PASS, because the lift is not unique.
- Not AMBIGUOUS, because sign disagreement is 0.05 %, below the 0.1 % threshold.
- Not strictly FAIL, because two asymmetric lifts have tiny negative regions.

Recorded as **UNCLASSIFIED, closest to FAIL**. There is no robust physical-region zero. The only zeros are small regions that depend on the lift, i.e. they are boundary-term artefacts. Unlike spin-1 (COS-1c/1d), the spin-2 exchange between scalars is dominated by a positive (attractive) structure.

## Blocker tags
`FRONTIER-THEORY` (the off-shell lift needs a canonical ADM constraint derivation) and, provisionally, `NO-GO` for robust zeros in this channel. Reopen trigger: an ADM-derived instantaneous kernel. If it selects X_L² or X_R², re-examine the small negative regions; if it selects the symmetric lift, close the channel.

## Lessons
The prereg verdict set was not exhaustive. Future preregs will include an explicit "otherwise" rule.

## Proposed credit (NOT awarded): 0.
