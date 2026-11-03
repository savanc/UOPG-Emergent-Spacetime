# MR-2 pre-registration: the massive hidden zero at the Mandelstam-triangle point P = (M², M², 2M²)

Date 2026-10-12 (Europe/London). Written and committed BEFORE `scripts/mr2_massive_zero.py` exists or is run.

## 0. Claim under test
Massive hidden zero (M2f, PROVED within the shift ansatz; prior art Carrillo González–Ward arXiv:2601.16860 [CGW],
Arkani-Hamed et al. 2312.16282, 2401.05483): the colour-ordered 4-pion amplitude f(s,t) vanishes on s + t = 2M².
Consequence (Lean `MassiveZero.dress_zero_at_P`, PROVED): the full SU(2) amplitude A(s,t,u) vanishes at
P: s = t = M², u = 2M², for ANY symmetric ordered f with the zero, at any order in p², as long as A is single-trace.
Polynomial content (Lean `poly_zero_iff`, PROVED): at O(p⁴) the zero ⇔ a2 = 2a1 (the M3 condition) AND
4a1 + 2a3 + a4 = 0 (NEW: involves the mass terms, i.e. ℓ3/ℓ4 in SU(2); at large N_c L5 = 2L8-type — CONJECTURE, not used).

## 1. Why this differs from M3
M3 tested a scheme-dependent LEC ratio at μ = 0.77 GeV. MR-2 tests an ON-SHELL AMPLITUDE VALUE: A(P) is physical,
μ-independent, includes mass-dependent LECs and loops. LO (Weinberg) vanishes at P identically (`lo_zero_at_P`), so
the content starts at O(p⁴). Overlap disclosed: A(P) contains M3's combination too (`dress_poly_at_P`).

## 2. Well-posedness (gate)
- Kinematics: P lies inside the Mandelstam triangle (0 < s,t,u < 4M²): unphysical, NOT directly measurable, but A is
  real-analytic there and fixed by Roy-equation/ChPT analyses of data [CITED: CGL hep-ph/0103088 §§3–4]. Accessible
  only indirectly → acceptable, tagged as model(dispersive)-dependent.
- Map: two-loop representation of BCEGS (hep-ph/9707291, eqs. 4.14–4.15, read today from the arXiv source) with
  coefficients b1…b6. Sources: (S1) CGL 2001 eq. 16.2 b̄i (Roy + data, errors given); (S2) BCEGS set II, Table 3,
  μ = 1 GeV and μ = 0.5 GeV (Ke4 + resonance r_i; μ spread used as its error). ≥2 sources ✓ (not fully independent:
  same two-loop formula, CGL compare to BCEGS).
- Higher orders: O(p⁶) (two-loop) kept in full; O(p⁸) not available → budgeted as |x2³ term| (size of last kept order).
- Convention budget: A(P) is μ-independent; only conventions are F_π = 92.4 MeV, M_π = 139.57 MeV (CGL).
- Single-trace assumption: SU(2) cannot separate double-trace (OZI) pieces; they are O(1/N_c) → in the band.
- **Disclosure (NOT BLIND):** while reading CGL for the gate I saw b̄1..b̄6 and noticed by eye that b̄1 + b̄2 + b̄3 + b̄4
  ≈ −0.19 is small. M3 data, ℓ̄1 = −0.4(6), ℓ̄2 = 4.3(1) (CGL) were known. So MR-2 is a non-blind check, like MR-1.
- Gate verdict: POSED (indirect, non-blind).

## 3. Observable and rule (fixed now)
R(Q) ≡ A(Q)/x2 − (s − 1), x2 = M²/F², units M² = 1 (the NLO+NNLO remainder; LO removed).
Z ≡ R(P) = A(P)/x2. Natural scale S ≡ RMS of R over the Mandelstam triangle (0 ≤ s,t,u ≤ 4, uniform grid).
r ≡ Z/S. Prediction: r = 0, theory band B = 1/3 (1/N_c: loops + double trace).
σ: S1 Gaussian MC over b̄ errors (independent; correlation scan ±0.8 reported), plus truncation |x2³-term at P|/S
in quadrature. S2: half the μ = 0.5 vs 1 GeV spread.
- PASS: |r| − 2σ ≤ B for S1 AND S2.
- FAIL: |r| − 2σ > B for S1.
- otherwise INCONCLUSIVE.
- **Discrimination check (pre-registered):** f ≡ fraction of grid points Q with |R(Q)|/S ≤ B. If f > 0.5 the test is
  NON-DISCRIMINATING and a PASS is downgraded to "consistent, not informative".
Reported (not graded): r with O(p⁴) truncation only; r normalised to |R(threshold)| and to |R(centre)|.

## 4. What a PASS would and would not mean
Would: the on-shell 4π amplitude respects the massive hidden-zero point within large-N accuracy. Would NOT: any
zero-parameter prediction (M, F inputs), nor test the δ-shift, nor be blind.
