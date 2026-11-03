# PREREG RG-IR-1: does the one-loop SM infrared quasi-fixed point remove the top Yukawa as an input? (UV-memory gate W-RG)

Authorisation: author approved (2026-10-30). This is rung 1 of 2. Node: RG-IR FIXED-POINTS (notes/FRONTIER-RG-STABILITY-2026-10-30.md, f6b115b), gate W-RG.

## 0. Why this rung (re-rank, METHOD rules 1–9)
Candidates eligible (excluding gated M5/MC-1/TS-1 hand entries/EW-Z1/CASCADE-2/pilot-wave, and PositiveGeometryEmergentSpaceTime-owned CASCADE-1b/INT-1/FL-1Z/paper):

| Rung | P_naive | P_used=0.3·P | V | EV | EMC (P·\|M+\|+(1−P)·\|M−\|) | IV_min | d vs last 3 (JORD-1c, SURF-1′c, LEAN-CERT-2c) | Foregone? |
|---|---|---|---|---|---|---|---|---|
| **RG-IR-1 (this)** | 0.05 | 0.015 | 0.8 | **0.012** | 3·0.015+3·0.985 = **3.0** | 3 | 4 (new basin RG-IR, ledger line y_t, method ODE closed form, FM-FREE) | no (paper prior PARTIAL ≈ 0.7) |
| CHIRAL-LATTICE-1 | 0.3 | 0.09 | 0.15 | 0.014 | ≈2.1 | 2 | ≥3 | no — taken as rung 2 (exploration slot) |
| HURWITZ-TP-1 (B6) | 0.07 | 0.02 | 0.3 | 0.006 | ≈2 | 1 | 2 (B6 basin repeats TP line) | FM-TAUT predictable |
| RP-BRIDGE-0 | 0.95 (known) | — | 0 | 0 | — | 0 | — | yes, credit 0 |
| CDT-RIVAL | — | — | — | — | — | — | reading node, not a rung | — |
| TP-1BR / EW-POS | killed at rule 7 earlier | | | | | | | |

RG-IR-1 is the only eligible rung that moves a fermion-mass ledger line (y_t); it is taken on V and diversity (d = 4). Its EV is low because P_used is small; the value is in the map decision either way (M+: y_t removed as an input; M−: UV-memory recorded with named reopen trigger "a derived UV boundary condition for y_t").
Well-posedness/method fitness: one-loop SM betas are standard; the question "relative width of y_t(M_Z) over a declared UV prior" is a single number with a declared threshold; CPU-only, < 100 MB; exact closed form exists (u = 1/y² affine), so method fits.

## 1. Prior art (arXiv abs pages read 2026-10-30 via export.arxiv.org)
- Lanzagorta, Ross, "Infra-red fixed points revisited", hep-ph/9501394. CITED: rate of approach to the IR fixed point decides whether Yukawas are fixed by gauge couplings. The analytic u = 1/y² solution used here is standard (this rung claims no novelty for it).
- Froggatt, "The Top Quark and other Fermion Masses", hep-ph/9603432. CITED: review of the top mass at the IR quasi-fixed point (MSSM) and the SM critical-point idea.
- Shaposhnikov, Wetterich, "Asymptotic safety of gravity and the Higgs boson mass", 0912.0208. CITED: UV fixed-point boundary conditions as the way to remove a low-energy input (rival reopen route).
- Eichhorn, Held, "Top mass from asymptotic safety", 1707.01107. CITED: a UV-side (gravity) fixed point for y_t — exactly the named reopen ingredient.
- Luo, Wang, Xiao, "Two-loop RGEs in general gauge field theories", hep-ph/0211440. CITED: general beta formulas; SM one-loop coefficients b=(41/6,−19/6,−7), Yukawa c=(17/12,9/4,8), a=9/2 also memorised (Machacek–Vaughn 1983–85, Pendleton–Ross PLB 98 (1981) 291, Hill PRD 24 (1981) 691; not on arXiv) — recorded in §4 memory audit.
Not found in this sweep: a gate statement "the SM QFP does / does not remove y_t under a declared UV prior with W ≤ 2%". Absence in a sweep is not proof of absence; the expected answer (narrowing, not removal) is folklore → predicted FM-FREE.

## 2. Hypothesis, metric, rule (fixed now)
Metric W = relative width (y_max − y_min)/mean of y_t(M_Z) when y_t(Λ) ranges over the primary UV prior [1, √(4π)], one-loop SM, Λ = 1.22e19 GeV (Planck). 
- ILL-DEFINED if the closed-form/RK4 consistency gate fails (> 1e-6) or any α_i ≥ 1 / Landau pole in range or non-physical inputs.
- PASS (REMOVES-INPUT) if W ≤ 0.02; PARTIAL (QFP-NARROWING: input relocated to the UV prior) if 0.02 < W ≤ 0.2; FAIL (UV-MEMORY) if W > 0.2; anything else UNCLASSIFIED.
- Robustness box 3×3×3 (α_em⁻¹ ∈ {126, 127.95, 130}, sin²θ ∈ {0.225, 0.23122, 0.237}, α_s ∈ {0.110, 0.118, 0.126}): if box verdicts differ from central, append [BOX-STRADDLE]. 
- Report-only, not verdict-bearing: GUT-range W (Λ=1e16), alternative priors [0.5, √4π] and [0.1, √4π], and the IR window — any comparison with measured m_t is CONTAMINATED (memorised) and not a gate.
- Predicted (paper estimate S ≈ 0.08): PARTIAL, W ≈ 0.05, FM-FREE (result sets a prior-relocated input, not a prediction).

## 3. Conventions and convention-invariance screening
Declared: t = ln(μ/M_Z), g1 = g′ (SM normalisation), m_t = y v/√2. Screened equivalences (physics-preserving, must give identical W to 1e-9, checked as planted P4): E1 GUT normalisation g1² = (5/3)g′² (b1, c1 × 3/5); E2 s = ln μ² (all coefficients halve, range doubles). E3 (y ↦ √2 y normalisation) maps the prior interval too, so W is invariant by construction; not run. Lean: `exp_ratio_invariant` (c·k)/(b·k) = c/b.

## 4. Planted / broken / null / rival / memory audit
- Planted (must recover): P1 QCD-only S equals (α3(Λ)/α3(0))^{8/7} to 1e-9 and RK4 agrees; P2 toy c3 = 80 ⇒ PASS; P3 no gauge (c = 0) ⇒ FAIL; P4 E1/E2 give same W; G self-tests: consistency gate true on SM / false with S×1.5; perturbative gate true on SM / false with b1 = 200; verdict map on W = 0.01/0.1/0.5/ill.
- Broken (must reject): B1 b3 = +7 (IR-free QCD) ⇒ not PASS; B2 α_s < 0 ⇒ ILL-DEFINED; B3 reversed UV interval ⇒ ILL-DEFINED.
- Null: 2000 random one-loop flows, seed 20261030, b1∈U[0.5,10], b2∈U[−7,1] (|b2|≥0.1), b3∈U[−11,−1], c1∈U[0,3], c2∈U[0,5], c3∈U[0,12], a∈U[1.5,9]; report PASS rate and PARTIAL-or-better rate. If SM is PARTIAL and the null PARTIAL-or-better rate ≥ 0.5, narrowing is generic (recorded as FM-QNBLIND-adjacent: not SM-specific).
- Rivals: QCD-only Pendleton–Ross flow; no-running identity (W of the prior itself).
- Memory audit: α inputs, b, c, a are memorised (MEMORISED-INPUT); none is the target. No tuning: thresholds, prior, box and seed fixed here. Digit masking: the checker never reads a measured m_t or y_t.

## 5. Lean plan (PositiveGeometryEmergentSpaceTime.RgIr1) and kill
Targets: u_flow_affine (field_simp/ring); qcd_ratio_fixed (R>0 ∧ R(9R−2)=0 ↔ R=2/9); qcd_sensitivity_exponent (−8/(−7) − 1 = 1/7 > 0); exp_ratio_invariant; affine_width; sm_exponent_signs (−c3/b3=8/7, −c2/b2=27/38, −c1/b1=−17/82). PROVED only at 0 sorry, no native_decide, axioms checked. Kill: if a target needs > 8 GB anon RSS or > 20 min, record LIMIT.

## 6. Tags and ledger
Verdict tagged SIMULATED (numerics) + PROVED (algebra) + CITED. FM tag expected FM-FREE. Blocker row in BLOCKER-INDEX with reopen trigger "derived UV boundary condition for y_t (e.g. 1707.01107-type fixed point) or a basin producing y_UV". Credit: proposal only (expected 0).

## 7. Lock
`rgir1_checker.py` sha256 `59a965b873a17228a1b7102fd58b8afbbdb70c24741f424c3f09fb6214ba7482`
`guard.py` sha256 `e1bff0e236144d7a8ae18d32f9241963c884a0ce7b46dfa5c7cc630b3a15345c`
Guard: re-read prereg, re-hash checker + guard, re-check prereg-commit ancestry of origin/main on every call; no pass flag. Import test and CLI must refuse before this prereg is pushed (record in sims/rgir1/guard_refusal.txt).
Lean: LEAN_NUM_THREADS=1, anon-RSS watchdog 8 GB; fresh AxiomsAll; commit lean/AxiomsAll_output.txt.
