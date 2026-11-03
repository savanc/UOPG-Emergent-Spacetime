# KL-LAT pre-registration (2026-10-13) — committed and pushed BEFORE any lattice K* value is opened

## Prediction (from PositiveGeometryEmergentSpaceTime.UnequalLS, PROVED: mass_formula, kstar_relation)
Per lattice ensemble with inputs (m_pi, m_K, m_rho) in any common units (lattice units fine; ratios only, no scale setting):
- J=1: m_K*^2 = m_K^2 + (m_rho^2 - m_pi^2)
- J=2 (only if a lattice K2* exists in that ensemble): m_K2*^2 = m_K^2 + 3 (m_rho^2 - m_pi^2)
No parameter is fitted. Slope from the rho of the SAME ensemble; intercept from the hidden-zero line.

## Statistic, pass rule, null (fixed now)
- delta = (m_K* - m_rho)/(m_K - m_pi). Prediction delta_pred from the inputs. Only ensembles with (m_K - m_pi)/m_rho >= 0.10 (away from SU(3) point, where any guess works).
- Point PASS: |delta_obs - delta_pred| <= max(2 sigma_delta, 0.10); sigma_delta from quoted m_K*, m_rho errors (stat+sys in quadrature, uncorrelated; input m_pi, m_K errors added).
- Null: delta ~ Uniform[0,1] (span between "K* = rho" and linear equal spacing m_K*-m_rho = m_K-m_pi). Point null rate f = |band ∩ [0,1]|. A point is discriminating iff f <= 0.3.
- Mass used: the group's quoted K*/rho mass (pole real part if quoted, else BW/bound-state mass); same convention for rho and K* within a group where possible; disclosed.
- Rung PASS: >= 2 independent groups, every scored point PASS, >= 1 discriminating point per group. FAIL if any scored point fails. INCONCLUSIVE if < 2 groups usable.
- J=2 points reported separately, scored only if 2 groups have them.

## Sources (selection rule fixed now)
Lattice Lüscher/finite-volume studies of the K* (Kpi P-wave) at m_pi >= 200 MeV whose group also determined the rho on the same ensemble. Candidates identified from memory of arXiv ids (not values):
- G1 HadSpec: 391 MeV (K* 1406.4158; rho 1212.0830); 239/284 MeV (K* 1904.03188; rho 1507.02599 and same-ensemble rho papers)
- G2 Alexandrou/Leskovec/Meinel/Rendon et al. (~317 MeV; K* 2006.14035; rho 1710.01557)
- G3 Graz Lang/Prelovsek (~266 MeV; K* 1307.0736; rho 1105.5636)
- G4 CLS Bulava/Brett et al. (~200 MeV D200; K* 1802.03100; rho 1808.05007)
Excluded: m_pi < 200 MeV (physical-point K*/rho memorised; RBC/UKQCD physical-point values seen in a prior-art snippet today); any ensemble whose strange mass is tuned using m_K* (circular).

## Memory audit (written before reading)
- Recalled: G3 K* mass ≈ 891 ± 14 MeV (Prelovsek et al. 2013) → G3 tagged CONTAMINATED, reported, NOT counted for blind.
- Seen today in snippets: K* is a bound state at m_pi=391 (qualitative, no number); RBC/UKQCD physical-point M_K*=893, M_rho=796 (excluded range).
- Vague: HadSpec 391 K* somewhere ~0.9 GeV (no digits trusted) → G1-391 flagged PARTIAL; blind count requires a second group from G2/G4 or HadSpec 239/284.
- No recall of G2, G4 or HadSpec 239/284 K* values.

## Counting (gate)
- Inputs m_pi, m_rho = OP-2 units; m_K = strange-sector free unit (as KS-1). Extra inputs: 0. Outputs: 1 function m_K*/m_rho(m_pi/m_rho, m_K/m_rho) tested at N ensembles → counts as ONE observable.
- Prior art: AVW 1969 relation (CITED); Weinberg "Stringy mass squared splittings reexamined" (chiral-algebra derivation, CITED). A lattice test of it at unphysical masses was not found in the sweep (not proof none exists). Our addition: derivation from the hidden-zero intercept.
- Tags: prediction SIMULATED from a PROVED formula. No tuning.
