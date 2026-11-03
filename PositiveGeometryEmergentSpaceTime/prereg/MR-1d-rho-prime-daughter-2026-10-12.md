# MR-1d pre-registration: LS I=1 spin-1 daughter at m^2 = 3 m_rho^2 vs rho(1450) (2026-10-12)

Written and committed BEFORE any rho(1450)/rho(1700) numerical listing was opened in this rung.

## Prediction (PROVED)
`lean/PositiveGeometryEmergentSpaceTime/LSResidue.lean`: `f2_level_I1_vector` (I=1 part of the level-1 residue has a P1 term) and
`rho_daughter_ratio`: single-channel P1 coefficient of the level-1 residue F_f2 is 3/4 (checked by hand: F_f2 = 9/8 x^2 + 3/4 x - 3/8),
divided by m^2 = 3, over the rho value (1/2)/1 -> **R_pred = 1/2**. This is exactly the MR-1b convention (residue coefficient / m^2,
normalised to the rho). Same isospin and J as the rho, so kappa_rho' / kappa_rho = 1 (no extra factor).
Width conversion (MR-1b prereg, J=1): Gamma(rho'->pipi) = R * Gamma_rho * (m'/m_rho) * sigma'^3/sigma_rho^3.
Numerically (SIMULATED, back-of-envelope): Gamma_pred(pipi) ~ 162 MeV at m' = 1465 MeV, ~159 MeV at the LS mass sqrt(3) m_rho = 1343 MeV.

## Prior art (CITED; sweep 2026-10-12)
- Bianchi-Consoli-Di Vecchia, arXiv:2002.05419: same LS residue decomposition (eq. 36), identify LS states with physical mesons.
- Szczepaniak et al., arXiv:1403.5782: Veneziano Dalitz fits explicitly identify the first rho daughter with rho(1450).
- PDG review "rho(1450) and rho(1700)" (Eidelman, Hanhart, Venanzoni): two overlapping states, widths widely scattered.
- Not re-read this rung (from memory, disclosed): AHRV / Albert-Rastelli / FPRS bootstrap papers treat leading-trajectory couplings, not this daughter, as far as we recall. Lovelace 1968 / Shapiro 1969 originals.
New here only: the Lean-checked 1/2 and a blind confrontation, if posed.

## What we already know (honest, from memory)
- m'^2/m_rho^2 ~ 3.5-3.6 (seen before). LS gives 3. Mass mismatch handled as in MR-1b: V1 data mass (primary), V4 LS mass (convention spread).
- We vaguely recall rho(1450) is "weak in pipi" relative to omega-pi / 4pi, and total widths 300-550 MeV. This is a prior that tilts against PASS. We do NOT recall any Gamma_pipi number.
- PDG likely lists BR(pipi) as "seen" only.

## Well-posedness gate (decided on source STRUCTURE only, before numbers)
Observable O1 (primary): Gamma(rho(1450) -> pipi) = Gamma_tot * BR(pipi), needing a numerical BR (or partial width) in a source with its own mass and width.
Requirement: >= 2 independent sources with a numerical pipi BR or Gamma_pipi. If PDG gives only "seen" and fewer than 2 such sources exist: **FAIL (not posed)**, stop like MR-1c.
O2 (form-factor coefficients beta from tau->pipinu / e+e- -> pipi, Belle 2008, BaBar 2012, CMD-3...): product f_rho' x g_rho'pipi, NOT a pure coupling. NOT scored; any comparison is SPECULATION.
Products Gamma_ee x BR(pipi) without an independent Gamma_ee: NOT scored.
Contamination: rho(1450)-rho(1700) interference makes any BR model-dependent -> extra 50% data-model band added in quadrature.

## Pass rule (if posed)
R_data = Gamma*BR/Gamma_rho / [(m'/m_rho) sigma'^3/sigma_rho^3], MC over quoted errors, conventions V1 (data mass), V2 (sigma^1), V4 (LS mass) half-spread.
Theory band: sqrt(0.30^2 + 0.20^2) = 36% (level-1 LS allowance 0.20, as MR-1b level 2) x 1/2. Plus 50% contamination band.
|z| <= 2 PASS per source, |z| > 3 FAIL, else INCONCLUSIVE. Rung PASS needs both sources PASS; FAIL if any source FAIL.

## Method fitness
Python/numpy MC reused from scripts/mr1b_data_check.py; Lean value already proved; sources read via WebFetch (PDG live / review PDF).
