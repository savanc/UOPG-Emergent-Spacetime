# MR-1 pre-registration: the f2/ρ ππ coupling ratio from the Lovelace–Shapiro amplitude (2026-10-12)

Committed and pushed **before** opening any PDG or other data entry for ρ(770) or f2(1270).

**Data-rung standards applied** (MISSION, after the M3 audit):
- well-posedness first;
- a convention, 1/N_c and higher-order budget;
- ≥ 2 independent sources;
- a scale-independent observable.

**Environment:** `<local path>` + `requirements-lock.txt`. sympy/mpmath only; runtime is seconds.

## 0. Disclosure (read before anything else): this test is NOT blind

1. **General knowledge.** I roughly know Γ_ρ ≈ 150 MeV, Γ_f2 ≈ 185 MeV, BR(f2 → ππ) ≈ 85 %, and
   m_f2²/m_ρ² ≈ 2.7.
2. **M3w exposure.** It quoted g̃ρ² = 0.51 ± 0.01 (FPRS §3.4).
3. **Exposure during today's prior-art sweep.** While locating AHRV's normalisation (arXiv:2312.15013) I read their
   eq. (4.4) real-world values: g̃ρ² ≃ 0.504(9) and g̃f2² ≃ 0.329(+13/−7). That is a real-world coupling ratio
   ≈ 0.65, in their normalisation.
4. **Consequence.** The LS prediction below is R_g = 1/2 (AHRV normalisation, before reconciliation). From (3) I
   expect the primary test to PASS. **MR-1 is therefore a REPRODUCTION + NON-BLIND data check.** A PASS will be
   reported as non-blind and will not count as a prediction.

What the pre-registration still fixes before data: the observable, the conventions, the band, the rules and the
sources.

## 1. Prior art (sweep 2026-10-12)

- **Lovelace 1968** (PLB 28, 264); **Shapiro 1969** (PR 179, 1345): the LS ππ amplitude; α₀ = 1/2 from the Adler
  zero. **Ademollo–Rubinstein–Veneziano–Virasoro / AVW** (1968–69): the dual-resonance ρ–f2 relations. [CITED]
- **FPRS arXiv:2211.12488, App. D:** LS with α₀ = 1/2 and α′ = 1/(2m_ρ²); spectrum m_n² = (2n + 1) m_ρ², so
  **m_f2² = 3 m_ρ²** (published). [CITED]
- **AHRV arXiv:2312.15013:**
  - eq. (2.12) defines on-shell couplings via Res_s M = −g_X² m_X² P_J(1 + 2u/m_X²);
  - eq. (2.16): g̃_X² = g_X²/(g1,0 m_ρ²);
  - App. C (C.7): the LS (scalar-subtracted) values **g̃ρ² = 0.52748, g̃f2² = 0.27790** (ratio 0.5268);
  - App. A extracts real-world couplings from widths;
  - they state that their bootstrap kink's g_ππf2/g_ππρ agrees with the real world.

  **So the LS coupling ratio is published (AHRV C.7), as is the data extraction (AHRV App. A).** [CITED]
- Polyakov–Vereshagin 1996 and Kampf (talks): LS phenomenology at O(p⁴); no f2/ρ width ratio found in the parts
  read. [CITED]

**Reconciliation item.** My exact computation (§2) gives g_f2²/g_ρ² = 1/2 exactly. AHRV's C.7 numbers give 0.5268.
That is a 5 % difference, unexplained so far. It is carried as a theory systematic (§4) and investigated in the review.

## 2. Prediction (computed before data; `scripts/mr1_ls_prediction.py`)

**Amplitude:** M(s,u) = Γ(½ − α′s)Γ(½ − α′u)/Γ(−α′(s+u)), with α′ = 1/(2m_ρ²) and m_ρ the one unit.

**Isospin:** Pauli traces give A(s,t,u) ∝ M(s,u) + M(s,t) − M(t,u). Then T⁰ = 3A(s,t,u) + A(t,s,u) + A(u,t,s) and
T¹ = A(t,s,u) − A(u,t,s).

**Partial waves:** t^I_J = (1/64π) ∫ P_J T^I dz, with BW normalisation t ≈ (1/σ) mΓ/(m² − s − imΓ), so
Γ = −σ(m) Res_s t / m.

**Exact results [PROVED in Lean, §6; sympy]:**
- Res at s = m_ρ²: M(s,u) → (residue) ∝ (1 + 2u/m_ρ²)·½·…, so g_ρ² ∝ 1/2.
- At s = 3m_ρ²: Res ∝ (3/4)(P2 + P1) in x = 1 + 2u/m², **J = 0 coefficient = 0**.
- **R_g ≡ g_ππf2²/g_ππρ² = 1/2** (AHRV normalisation).
- Partial-wave residue ratio Res t⁰₂ / Res t¹₁ = (9/320π)/(1/48π) = 27/20.
- **LS-native width ratio (massless pions, LS masses):** R_Γ = (27/20)/√3 = 0.7794.

## 3. Observable (primary): R_g = g_ππf2²/g_ππρ², on-shell couplings in AHRV (2.12) normalisation

This is dimensionless and has no renormalisation scale.

**Data → R_g** (massive pions, physical masses, the same partial-wave normalisation for both):

Γ_X(ππ) = κ_IJ · g_X² · m_X · σ_X^{2J+1},  σ = √(1 − 4m_π²/m²).

With κ₀₂/κ₁₁ = 1.8 (from the massless limit: 0.7794 = 1.8 · ½ · √3):

**R_g^data = [Γ(f2→ππ)/Γ(ρ→ππ)] / [1.8 · (m_f2/m_ρ) · σ_f2⁵ / σ_ρ³]**

- m_π = 139.57 MeV.
- The factor 1.8 is fixed by the isospin/partial-wave algebra above and is not data.
- Γ(f2 → ππ) = Γ_tot(f2) · BR(f2 → ππ). Γ(ρ → ππ) = Γ_tot(ρ), with BR ≈ 100 % to be confirmed from the source.

**Secondary (non-blind, no verdict):**
- m_f2²/m_ρ², predicted 3, with the same band;
- R_Γ itself.

## 4. Error budget (theory and conventions), fixed now

- **1/N_c:** ±30 % on R_g. Couplings receive O(1/N_c) corrections; Γ/m ≈ 0.15–0.2 for both states sets their size.
- **LS-specific:** ±10 %. This covers LS's known non-unitary features (the scalar sector; AHRV/FPRS place full LS
  outside their allowed region) and the 5 % AHRV reconciliation item.
- **Total theory σ_th = 0.32 · R_g^pred = 0.16.**

**Data-side conventions:** each enters as a separate R_g^data variant. σ_conv is half the max−min spread over the
variants.
- **V1 primary:** S1 Breit–Wigner masses and widths with the formula above.
- **V2:** no barrier factor (σ¹ instead of σ^{2J+1}).
- **V3:** Blatt–Weisskopf barrier with R = 1 fm (5 GeV⁻¹) applied to the extraction.
- **V4:** LS-predicted masses (m_f2 = √3 m_ρ) in the kinematic factors.
- **V5:** pole masses and widths (S2) in place of the BW values.

Higher orders are covered by the 1/N_c item; there is no extra band.

## 5. Sources (≥ 2), well-posedness first, and rules

**Sources:**
- **S1:** PDG Review of Particle Physics, current online edition: ρ(770) and f2(1270) BW mass and width averages,
  and BR(f2 → ππ).
- **S2:** an independent determination of ρ and f2 pole parameters / couplings: dispersive/Roy-type analyses as
  listed in the PDG pole entries, e.g. García-Martín et al. 2011 for ρ, plus a dispersive f2 determination. If no
  separate f2 pole coupling is available, the PDG pole-position entries are used for both.
- **S3 (cross-check, no verdict):** AHRV App. A values, already seen.

**Step 0, well-posedness (per source).** All of:
- (i) both states are narrow (Γ/m < 0.25);
- (ii) R_g^data > 0;
- (iii) the data point is inside the large-N allowed region, using AHRV's placement of the real-world point
  (Fig. 5) as cited.

If any of these fails, the source is CONDITIONAL and cannot give PASS or FAIL.

**Per source:**

z = (R_g^data − 0.5) / √(σ_th² + σ_data² + σ_conv²)

- **PASS** if |z| ≤ 2.
- **FAIL** if |z| > 3.
- **INCONCLUSIVE** otherwise.

**Overall:**
- **PASS** only if all well-posed sources PASS.
- **FAIL** only if all well-posed sources FAIL.
- Otherwise INCONCLUSIVE.
- A PASS is labelled **"PASS (non-blind reproduction)"**.

**Kill criterion** (from the trade-space review): an overall FAIL records a second miss for the LS hidden-zero class
and moves the mass route to (b).

## 6. Lean (cheap)

- **The Gamma recursion:** Γ(a) = (a−1)(a−2)Γ(a−2) via Mathlib.
- **The residue polynomials and their Legendre decompositions** (by `ring`):
  - ρ: residue (1 + x)/2 → J = 1 coefficient ½;
  - f2: (3/8)(3x² + 2x − 1) = (3/4)(P2 + P1), J = 0 coefficient 0;
  - hence R_g = 1/2.
- **R_g^data and the z-arithmetic** in ℚ, if the numbers are rational.
