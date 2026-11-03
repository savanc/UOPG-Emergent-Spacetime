# KL-LAT2 result (2026-10-13): K* extended + phi (new observable) — **PASS, NOT DISCRIMINATING**
Prereg prereg/KL-LAT2-prereg-2026-10-13.md + predictions (ed4de3f, pushed before targets were opened; targets sealed by sha256, verified OK before reading). Check sims/kllat2/check.py → check_output.{txt,json}.

## Gates
- Prior art (CITED): AVW/KKY 1969 (K*); quadratic equal spacing m_phi²−m_K*² = m_K*²−m_rho² for an ideally mixed nonet (old quark-line rule); heavy-vector ChPT (linear m_V vs m_P²). No lattice test of the phi version across unphysical masses found in the sweep (not proof none exists).
- Theory/well-posedness: PASS. phi from the KL-1 rule with LO GMOR (Lean PositiveGeometryEmergentSpaceTime.KLPhi PROVED: phi_relation, equal_spacing, phi_from_kstar; 0 sorry; axioms propext, Classical.choice, Quot.sound). Lattice phi = connected ss̄ ⇒ ideal mixing. GMOR input check: phi with lattice eta_ss differs from GMOR version by ≤0.4 % (input-side, not a target).
- Memory audit: no recall of any per-ensemble PACS-CS/CP-PACS/UKQCD vector mass. Disclosed leaks in today's search snippets: physical-point phi (Graz, HPQCD; excluded) and Rendon/Brett K* values (already used in KL-LAT; not rescored).
- HadSpec 283/330: same-ensemble rho FOUND (2303.10701 BW), but no HadSpec K* on these ensembles located → not scored. Blocker: DATA-ABSENT (FRONTIER-DATA). K2*: none on any used ensemble → not scored.

## Results (SIMULATED predictions from PROVED formulas; data CITED)
Groups: Tsukuba (PACS-CS Nf=2+1, 4 pts + CP-PACS Nf=2 PQ, 10 pts; counted as ONE group) and UKQCD (Nf=2 PQ, 3 pts).
| Observable / group | n | KL pass | mean |res| | N1 f | N2 ChPT-linear pass / |res| | N3 phys-fixed pass / |res| | pred high |
|---|---|---|---|---|---|---|---|
| K* / Tsukuba | 14 | 0.93 (1 fail, CP-PACS b1.80) | 0.050 | 0.25 | 1.00 / 0.036 | 0.07 / 0.243 | 93 % |
| K* / UKQCD | 3 | 1.00 | 0.131 | 0.76 | 1.00 / 0.092 | 0.67 / 0.196 | 100 % |
| phi / Tsukuba | 14 | 1.00 | 0.042 | 0.20 | 1.00 / 0.023 | 0.00 / 0.217 | 100 % |
| phi / UKQCD | 3 | 1.00 | 0.124 | 0.40 | 1.00 / 0.106 | 0.67 / 0.169 | 100 % |
Mass residuals: K* +0.0 to +3.1 % (PACS-CS +0.1 to +0.7 %); phi +0.05 to +5.2 % (PACS-CS +0.35 to +0.58 %).

- By the prereg rule both observables PASS (≥80 % per group); strict all-points rule: phi passes all 17, K* fails 1/17.
- **Not DISCRIMINATING**: the stronger null N2 (heavy-vector ChPT linear in m_P², c from physical masses) also passes 100 % and has SMALLER mean residuals in every cell. N1 band null f ≈ 0.20–0.76/point; N3 (δ fixed at physical) is beaten clearly. So the data confirm "vector masses shift ∝ m_K² − m_pi²", but cannot tell KL-1 from the linear chiral rule at these (heavy, near-SU(3)) masses.
- **Offset check (answers KL-LAT caveat):** prediction high in 16/17 K* and 17/17 phi points, all stable ground-state masses (no BW/pole convention). ⇒ the KL-LAT high offset is INTRINSIC to the quadratic relation (CONJECTURE: missing O((m_K²−m_pi²)²) curvature / slope mismatch), not a convention artefact. Not corrected (no tuning).
- UKQCD points have large errors (bands 0.12–0.62) → weak.

## Proposed credit (prereg-fixed)
- phi: PASS, not discriminating → **0** recommended (prereg allowed "+0.25 at most (or 0)"; N2 beats KL-1 on residuals, so I do not recommend +0.25). K* extension: corroboration only, no credit. **OP-2 unchanged: blind 2.5 | VR 1.0 | 3.5/3.**
- Blocker tags: discrimination NOT-DISCRIMINATING (competitor equal); HadSpec 283/330 K* DATA-ABSENT; K2* DATA-ABSENT.

## Reopen trigger / next rung
KL-LAT3: KL-1 and N2 diverge only far from the SU(3) line ((m_K−m_pi)/m_rho ≳ 0.35, light pions, heavy strange). Gate first: compute from inputs where |pred_KL − pred_N2| > band; then look for ensembles there (CLS/RQCD strange-varied trajectories, Mainz/RQCD m_s-heavy ensembles, BMW). Also test the intrinsic offset sign as a pre-registered prediction.
