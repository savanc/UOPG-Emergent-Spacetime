# M3w pre-registration: is the O(p⁴) data test well-posed?

Date: 2026-10-11 (Europe/London). Written and pushed **before** any M3w script, Lean or number below the "Rules"
section is computed. Rung protocol step 0 (well-posedness), added in the ladder review (`reviews/LADDER-REVIEW-2026-10-10.md` §6).

## Question (fixed)

Is each measured O(p⁴) value inside the region reachable by
- (i) **any unitary large-N tree theory** (region R_full), and
- (ii) **the planned M3b family** (region R_fam; family defined below and in `prereg/M3b-spin-family-2026-10-11.md`)?

The answer is used **only** to decide whether the M3b data test is meaningful, and which dataset M3b may use. It
does not change the M3 verdict (FAIL, recorded).

## Disclosure (post-hoc risk)

I already know from M3 and the ladder review that the BE14 NNLO central value L3/L2 = −307/81 lies below −3
(`LECRatio.be14_outside_wedge`) and that the BE14 p⁴ fit (−2.38) sits inside. So the BE14-NNLO part of this rung
is largely a formal confirmation. What is not yet computed: error-aware pulls, the 1/N_c band treatment, the SU(2)
and AR-Table-1 points, the FPRS mapping that keeps L1, the scale window, and all Lean statements for the family.

## Prior art (sweep done before writing; all [CITED])

- **Albert–Rastelli, arXiv:2203.11950 (AR).** Large-N positivity with all null constraints. Linear bounds
  g̃2′ ≥ 0 and g̃2′ ≤ 4g̃2 (ℓ2 ≥ 0, ℓ1 + ℓ2 ≥ 0; eq. 78); g̃2 ≤ 1, g̃2′ ≤ 3.2589 (eq. 52). The lower-right edge
  is the Skyrme line g̃2′ = 4g̃2 up to a kink (eq. 59, numerically g̃2 ≈ 0.494 at n = 15, extrapolated ≈ 0.42).
  §4.4.3, Table 1: four real-world ℓ_i^r(m_ρ) sets [GL84; Bijnens–Colangelo–Gasser 1994; Girlanda–Knecht–Moussallam–Stern
  1997; Amoros–Bijnens–Talavera 2000] "all show some overlap with our allowed region to within uncertainty" and gather
  near the Skyrme line. Eq. 79: the large-N bound ℓ1 + ℓ2 ≥ 0 at μ = m_ρ is ℓ̄1 + 2ℓ̄2 ≥ 3 ln(m_ρ²/m_π²) ≈ 10.3.
  LS sits at g̃2 = ln 2, g̃2′ = 2 ln 2 (eq. 75).
- **Fernandez–Pomarol–Riva–Sciotti, arXiv:2211.12488 (FPRS).** Proves the kink is the single-ρ theory
  (g̃2,1, g̃2,0) = (4/3, 1/3) in their normalisation (App. B, eq. 45; their g2,1 = 2× AR's). Eq. 31: the ratio is
  fixed by the odd/even split of ⟨1/m⁴⟩ (our `hidden_zero_iff_balance`). Builds scalar-less LS (eq. 113, 115:
  g̃2,1/g̃2,0 ≈ 2.05/0.55) and Coon deformations near the boundary. Eq. 54–55: g̃2,0 = 4(2L1+3L2+L3)M²/F²,
  g̃2,1 = 16L2 M²/F²; with 2L1 = L2, ratio set by Δ_L = 3L2 + L3 ≥ 0, which **vanishes for spin-1-only theories**;
  combined large-N_c lattice [Bali et al. 1304.4437; Hernández–Pena–Romero-López 1907.11511; Baeza-Ballesteros et al.
  2202.02291] quoted as Δ_L = (−0.12 ± 0.22)·10⁻³. With a gap M′/m_ρ = 1.65 (f2/ρ) the allowed strip hugs the
  spin-1 line (VMD from positivity). QCD g̃ρ² = 0.51(1), g̃f2² = 0.18(1) from PDG widths (§3.4).
- **Li, arXiv:2310.09698.** Primal/dual convergence for large-N χPT; reproduces AR's region, g̃2′ ≤ 3.2589, the
  Skyrme bound (primal 3.939 g̃2), and an O(p⁶) region (g̃3, g̃3′) with g̃3′ ≤ 4g̃3; holographic QCD (Sakai–Sugimoto)
  sits on the Skyrme line below the kink.
- **2024–26 updates found:** none that change the O(p⁴) large-N region (the 1/N, loop-level bootstraps
  Guerrieri–Penedones–Vieira 2011.02802 and Alvarez–Bijnens–Sjö 2112.04253 are finite-N and different problems).
  Search was not exhaustive.
- **Finite-N positivity (M2)** is a different region (Manohar–Mateu, ℓ̄-space) and is satisfied by the data (M2).

## Regions (definitions; the Lean statements will be exactly these)

Variables. AR normalisation: M(s,u) ⊃ g20(s²+u²) + 2 g21 su. Large-N maps (AR 4.21, 4.26, 4.27; `LECRatio.su3_rename`,
`su2_iff`): g20 ∝ 2(L3 + 4L2), g21 ∝ 4L2 (SU(3) with 2L1 = L2); g20 ∝ (2ℓ1 + 3ℓ2)/2, g21 ∝ ℓ2 (SU(2)).
Ratio ρ ≡ g21/g20; r ≡ L3/L2; q ≡ ℓ1/ℓ2; ε ≡ 1 − ρ = ⟨(−1)^J/m⁴⟩/⟨1/m⁴⟩.

- **R_full (projective, O(p⁴)).** 0 ≤ g21 ≤ 2 g20 ⇔ L2 ≥ 0 ∧ L3 + 3L2 ≥ 0 ⇔ ℓ2 ≥ 0 ∧ ℓ1 + ℓ2 ≥ 0 ⇔ ρ ∈ [0, 2]
  ⇔ r ∈ [−3, ∞) (L2 > 0) ⇔ q ∈ [−1, ∞) (ℓ2 > 0). This is the exact ratio projection of AR's region (both edges are
  attained: scalar, ρ-only), so the nonlinear null constraints do not shrink it.
- **R_full,2D (normalised).** Additionally g̃2 ≤ 1 (masses ≥ M) and the numerical AR boundary (cited, not proved).
  Needs F and M: AR's inputs fπ = 92 MeV, M = m_ρ = 775 MeV (pre-registered, to compare with AR Table 1 directly).
- **R_fam (planned M3b family).** ε ∈ [−1, 0] ⇔ ρ ∈ [1, 2] ⇔ r ∈ [−3, −2] ⇔ q ∈ [−1, −1/2]. The family is the
  positive (convex) combination of the hidden-zero completion (LS, ε = 0) and the single-ρ kink amplitude (FPRS eq. 25,
  m∞ → ∞; ε = −1). Its reachable ratio interval is what is computed here; nothing else about M3b is computed.

## Data (sources verified; values at μ = 0.77 GeV unless stated)

| id | source | values (10⁻³) | variable |
|---|---|---|---|
| D1 | BE14 NNLO preferred, arXiv:1405.6488 Table 3 | L1 = 0.53(6), L2 = 0.81(4), L3 = −3.07(20) | r; FPRS-ρ with L1 |
| D2 | BE14 p⁴ fit, Table 1 col. 6 (NLO) | L1 = 1.0(1), L2 = 1.6(2), L3 = −3.8(3) | r; FPRS-ρ |
| D3 | BE14 NNLO free fit, Table 3 | L1 = 0.64(6), L2 = 0.59(4), L3 = −2.80(20) | r |
| D4 | GL 1985 (BE14 Table 1 last col.) | L1 = 0.7(3), L2 = 1.3(7), L3 = −4.4(2.5) | r |
| D5 | Pich 1995 / BEG 1994 (hep-ph/9502366 Table 1) | L2 = 1.4(3), L3 = −3.5(1.1) | r |
| D6 | SU(2) CGL 2001 eq. 14.1 | ℓ̄1 = −0.4(6), ℓ̄2 = 4.3(1), Mπ = 139.57 MeV | q, ℓ1+ℓ2, 2ℓ1+3ℓ2 |
| D7 | AR Table 1 (ℓ_i^r(m_ρ)) | GL84 (−6.0(3.9), 5.5(2.7)); BCG94 (−5.4(1.1), 5.7(1.1)); GKMS97 (−4.0(2.1), 1.6(1.0)); ABT00 (−3.2(2.5), 3.1(2.1)) | q, 2D |
| D8 | FPRS quote of large-N_c lattice | Δ_L = 3L2 + L3 = −0.12(22) | Δ_L ≥ 0 (R_full); Δ_L ∈ [0, L2] needs L2 (R_fam) |

Errors uncorrelated (no covariances published); BE14 errors exclude higher orders.

## Rules (fixed now)

1. **Pull.** For a dataset with value x ± σ (linear error propagation; MC check), gap g = distance from x to the
   region (0 if inside). z_exp = g/σ. **Large-N_c band:** σ_N = 0.30·|x| (same 30% convention as M3; data-side support:
   BE14's own L_A/L2 = 0.24/0.81 ≈ 0.30), z_N = g / √(σ² + σ_N²).
2. **Per dataset and region:** INSIDE if z_exp ≤ 1; COMPATIBLE if 1 < z_exp ≤ 2; OUTSIDE if z_exp > 2. Report also
   z_N and the **minimal band fraction f\*** at which z_N = 2 (the "X" for CONDITIONAL).
3. **Well-posedness of a dataset for M3b:** WELL-POSED if z_exp ≤ 2 for R_fam (hence for R_full); ILL-POSED if
   z_N > 2 for R_full (outside every unitary large-N theory even with the 30% band); CONDITIONAL otherwise (state f\*).
4. **Overall M3w verdict** = the status of D1 (the M3 primary, the authors' preferred fit), with D2–D8 reported.
5. **M3b dataset rule (fixed now):** M3b may use for its ε-measurement only datasets that are WELL-POSED here; among
   them the one with the smallest σ on r (or q). If none is WELL-POSED, M3b's LEC-ratio comparison is labelled
   ill-posed and M3b must use a non-LEC observable (stated in its prereg).
6. **Scale (informational, does not change the verdict):** L2 runs (Γ2 = 3/16), L3 does not. Report the μ-window in
   which D1's central r lies in R_fam and in R_full. For SU(2) report the μ at which ℓ1 + ℓ2 = 0 (AR eq. 79 form).
   The pre-registered comparison scale stays 0.77 GeV (m_ρ for D7, as AR).
7. **Lean (exact statements):** family ratio interval [1, 2] (mixture of a hidden-zero and an odd-only spectrum),
   surjectivity onto [1, 2], the maps ρ ↔ r ↔ q for the family and for R_full, R_fam ⊂ R_full, g̃2 ≤ 1 from a gap,
   and the inclusion/exclusion facts as exact ℚ inequalities on the quoted (rounded) numbers. No sorry, no
   native_decide, no custom axioms.

## Expected outcome (stated so it cannot be moved)

D1 OUTSIDE R_fam and outside R_full on experimental errors (≈2.5σ), so not WELL-POSED; whether it is CONDITIONAL or
ILL-POSED depends on the 30% band, which I have not computed. D2 INSIDE. If so, the M3 primary comparison was
ill-posed or conditional against D1, and M3b must use D2-type data or a resonance observable.
