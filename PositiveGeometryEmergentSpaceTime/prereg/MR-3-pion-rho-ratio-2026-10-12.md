# MR-3 pre-registration (2026-10-12): m_π/m_ρ window, and fallback MR-3b (KSRF-type ratio)

Written and committed BEFORE the data script exists and before any PDG/FLAG page is opened for this rung.

## Part A — the original question (m_π/m_ρ) — WELL-POSEDNESS FAIL, decided pre-data
Minimal massive Lovelace–Shapiro family (α(x)=α₀+α'x; Adler zero at s=u=m_π²; ρ on the leading trajectory)
is a one-parameter family in r=m_π²/m_ρ² (PROVED, `PositiveGeometryEmergentSpaceTime.MassiveLS.adler_condition`, `rho_condition`).
Positivity: level 1 needs only r<1/4 (threshold; PROVED `level1_positive`), but the f₂-level J=0 coefficient
is r(2r−1)/(4(r−1)²) < 0 for 0<r<1/2 (PROVED `level2_decomp`, `level2_scalar_negative`), so positivity forces
r=0 (PROVED `positivity_forces_chiral`). Exact scan r∈[0,0.2475] step 1/400, levels ≤8: only r=0 survives
(SIMULATED, `scripts/mr3_massive_ls_scan.py`).
So the ingredients give either "r=0" (minimal family) or — once the family is deformed (satellite terms,
non-linear trajectories, as in the S-matrix bootstrap of massive pions, where m_π is an input) — no bound
(CONJECTURE). Neither is a testable window. m_π/m_ρ ≈ 0.18 was known to us (memory) throughout. Not scored.

## Part B — MR-3b: KSRF-type cross-sector ratio (posed instead)
Observable: g̃ρ² ≡ g_ρππ² f_π² / m_ρ² (Albert–Rastelli 2203.11950 eqs. 68, 92; L = −g f_abc π^a ∂π^b ρ^c,
A(s|t,u) = s/f_π² + …, f_π ≈ 92 MeV convention).
Prediction (chiral-limit LS with Adler zero, large N): g̃ρ² = 1/(2π) = 0.1592 (PROVED algebra `ksrf_ratio`;
normalisation cross-checked against AR eq. 75 g̃₂ = ln 2, SIMULATED). KSRF corresponds to 1/2 (`ksrf_gap`: factor π).
Extraction: g² = 6π m_ρ² Γ_ρ / p³, p = sqrt(m_ρ²/4 − m_π±²) (tree-level width formula, from memory).
Sources (≥2): PDG for m_ρ, Γ_ρ(770), f_π± (f_π = F_π/√2); FLAG for f_π (physical) and, as a large-N/chiral
variant, the chiral-limit F.
Error budget: ±36% (as MR-1b: large-N + conventions), plus input errors in quadrature.
PASS: measured g̃ρ² within [0.102, 0.217] for the PDG central set. FAIL otherwise.
Blindness: NOT blind. I know from memory that KSRF (g̃ρ² ≈ 1/2) holds to ~10% in nature, so I expect FAIL
(≈ factor 3). The test is pre-stated and the band fixed, but its outcome is anticipated. Discrimination: n/a.
