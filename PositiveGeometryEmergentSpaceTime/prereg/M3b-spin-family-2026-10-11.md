# M3b pre-registration: the even/odd spin family ε (hidden zero ↔ ρ dominance)

Date: 2026-10-11 (Europe/London). **Pre-registration only.** No M3b prediction number and no comparison with data has
been computed. The author and the reviewer re-read this before any M3b computation (pacing rule). Well-posedness input:
`reviews/M3w-result-2026-10-11.md` (verdict CONDITIONAL for the NNLO LEC fit; the NLO fit is well-posed; the LEC ratio
has too little discriminating power to measure ε).

## 1. What ε is

In any large-N tree completion with positive spectral weight, the O(p⁴) ratio is set by the even/odd spin balance
(AR 4.35; Lean `hidden_zero_iff_balance`, `family_iff_odd_excess`):

  ε ≡ ⟨(−1)^J / m⁴⟩ / ⟨1/m⁴⟩ = 1 − g2,1/g2,0 (AR normalisation),  L3/L2 = 2/(1 − ε) − 4  (2L1 = L2).

ε = 0 is the hidden zero (L3/L2 = −2, M3). ε = −1 is odd spins only, i.e. vector/ρ dominance on the Skyrme edge
(L3/L2 = −3). ε = +1 is scalars only.

## 2. Options considered (prior-art sweep)

| option | what it is | prior art | can it move ε off 0? | decision |
|---|---|---|---|---|
| (a) deform the stringy/curve-integral δ-shift | α′δ-family of 2312.16282 §7, Z-theory | M3 (this repo): hidden zero holds for **all** α′δ; Arkani-Hamed et al. 2312.16282, 2401.05483 | **No**: every member has ε = 0 | rejected (proved not to move) |
| (b) Lovelace–Shapiro with satellites | LS plus Γ-function satellites | Polyakov–Vereshagin 1996 (hep-ph/9509259): the L3 = −2L2 relation "holds with any type of satellites added to a simple LS amplitude" | **No** (published) | rejected |
| (c) reweight even/odd spins along the LS Regge tower | multiply J-even residues by λ | Null constraints (AR §3; FPRS eq. 18) are linear in the couplings; reweighting one tower generically violates them (no consistent amplitude) | only if the result is a sum of consistent amplitudes, which is (e) | rejected as stated |
| (d) Coon q-deformation of LS | M_q (FPRS eq. 118–121, App. E; Coon–Sukhatme–Tran Thanh Van 1973) | Figueroa–Tourkine 2201.12331; Maldacena–Remmen 2207.06426 (q-strings); Cheung–Remmen 2302.12263; FPRS Fig. 3 (Coon curves) | Probably (the LS zero 1/Γ(−α′(s+u)) is lost at q < 1), but ε(q)'s range is **not known** and it was not the family in the M3w prereg | **held as M3c** (most geometric option; needs its own well-posedness check) |
| (e) **chord of the EFT-hedron**: positive mix of the hidden-zero completion and the ρ-only (kink) theory | M_ε below | AR §4 and FPRS eq. 47 build a *different* interpolation (su-model ↔ spin-1) for the boundary; positive mixtures are the standard "convex hull" geometry of the EFT-hedron (Arkani-Hamed–Huang–Huang 2012.15849) | **Yes**, reaches exactly ε ∈ [−1, 0] (Lean `family_surj`, `family_interval`) | **chosen** |

**Justification for (e).** It is the only option that (i) is guaranteed consistent: a positive sum of amplitudes that
each satisfy positivity, crossing, the null constraints and k_min = 1 Regge behaviour satisfies all of them, since all
are linear in the spectral density; (ii) has a reachable region already computed and proved (M3w: R_fam = ε ∈ [−1, 0],
the whole odd-heavy half of AR's wedge); and (iii) contains both pre-registered endpoints exactly. **Honest geometric
status:** the family is a straight segment (a chord) inside the convex EFT-hedron, between an interior point produced
by our geometry chain (LS, hidden zero) and the kink vertex (ρ only, FPRS App. B). The ε = −1 endpoint is a field-theory
vector exchange. It is **not** produced by the associahedron, the curve integral or the δ-shift. Geometric only in
the EFT-hedron (convex-hull) sense.

## 3. The family (exact definition)

Units m_ρ = 1. Components (both with their lightest J ≥ 1 state at s = m_ρ²):

- **A_HZ = Lovelace–Shapiro**, AR (2.22) / FPRS (106): M_LS(s,u) = −Γ(1/2 − α′s)Γ(1/2 − α′u)/Γ(−α′(s+u)),
  α′ = 1/(2m_ρ²), intercept 1/2 (first pole at s = m_ρ², levels s_n = (2n + 1) m_ρ²). With scalars, as in M3.
- **A_V = ρ-only theory**, FPRS (25) in the limit m∞/m_ρ → ∞, whose Wilson coefficients are FPRS (26):
  g1,0 = 3g²_ρππ/m_ρ², g̃ρ² = 1/3, and the even/odd content of a single J = 1 state.
- **M_ε = (1 + ε) · M_LS / g2,0[LS] + (−ε) · M̂_ρ / g2,0[ρ]**, for ε ∈ [−1, 0].

Every Wilson coefficient is linear in M, so g2,0[M_ε] = 1 and g2,1[M_ε] = 1 − ε exactly (AR normalisation).

## 4. Is ε fixed by the geometry? **No. ε is a FREE dial.**

Our chain (associahedron → δ-shift → pions, M2c–M2f) fixes ε = 0 (M3). Nothing in it produces ε ≠ 0. Positivity
only bounds ε ∈ [−1, 0] on this chord (ε ∈ [−1, 1] in R_full). **So M3b is a MEASUREMENT of ε, not a prediction.**
The only test is the secondary observable in §6, predicted by the fitted ε with no further freedom.

## 5. Primary: measure ε (not a test)

- **Observable:** the normalised ρ coupling g̃ρ² ≡ g²_ρππ / (g1,0 m_ρ²) (FPRS eq. 52/60). In M_ε,
  g̃ρ²(ε) = [ (1+ε) G_ρ^LS + (−ε) G_ρ^V ] / [ (1+ε) G_10^LS + (−ε) G_10^V ], with G_X^C the component's J = 1 coupling at
  s = m_ρ² (resp. its g1,0), each divided by its g2,0. This is a Möbius map of ε, so it inverts in closed form.
  G^V values are FPRS (26) (g̃ρ²[V] = 1/3). G^LS values come from LS residues (to compute; exact in Γ-functions).
- **Data:** g̃ρ² = 0.51 ± 0.01 (FPRS §3.4, from Γ(ρ → ππ), PDG 2022). Large-N_c band ±30 % (σ_N = 0.15), the same
  convention as M3/M3w. Why not the LEC ratio: M3w showed that, with the band, L3/L2 cannot separate ε = 0 from −1
  (`band_wider_than_family`), and the NNLO preferred fit is only CONDITIONALLY well-posed.
- **Step 0 (well-posedness, run first next time):** compute g̃ρ²(0) and g̃ρ²(−1) = 1/3. If 0.51 lies outside
  [min, max] by more than 2σ_tot (σ_tot² = 0.01² + 0.15²), M3b is **ILL-POSED**: record it and stop, with no tests and no
  switch of family.
- **Output:** ε̂ with an error from the data and the band (linear and MC). Labelled MEASUREMENT.

## 6. Secondary: the real test (f2 coupling)

- **Observable:** g̃²_f2 ≡ g²_f2ππ / (g1,0 m²_f2) (FPRS eq. 60), J = 2 meson. In M_ε only LS contributes: its
  first J = 2 state is at s = 3m_ρ² (n = 1), so m_f2 = √3 m_ρ in the theory's own normalisation. A_V has no J = 2 state at
  finite mass.
  Prediction: g̃²_f2(ε̂), no free parameter left.
- **Data:** g̃²_f2 = 0.18 ± 0.01 (FPRS §3.4, from Γ(f2 → ππ), PDG 2022). I₁ = [0.17, 0.19], I₂ = [0.16, 0.20].
- **Theory band:** ±30 % (1/N_c), plus the ε̂ error propagated, plus ±11 % for the mass mismatch (LS J = 2 at
  √3·0.775 = 1.342 GeV vs m_f2 = 1.2754 GeV, 5.2 %, entering squared), combined in quadrature.
- **Rule (M3 style):** PASS if the theory band meets I₁; **FAIL (kill)** if it misses I₂, recorded as a miss with the
  target not moved; INCONCLUSIVE otherwise.
  **NON-DISCRIMINATING flag:** if the pure-LS value g̃²_f2(ε = 0), with the same band, also PASSES, the result is
  reported as "consistent but not a test of the deformation".
- **Prior art (so a PASS is not over-claimed):** LS's spin-2 couplings date from 1969. FPRS Fig. 6 plots scalar-less LS.
  Albert–Henriksson–Rastelli–Vichi 2312.15013 (JHEP 09 (2024) 172) reproduce the real-world g_ππf2/g_ππρ from the f2
  bootstrap kink. New here would be only the specific chord's prediction.

## 7. Tertiary (reported, never verdict inputs)

- T1: L3/L2 = 2/(1 − ε̂) − 4 against D2 (BE14 p⁴ fit, −2.38 ± 0.35; the smallest-σ WELL-POSED LEC set, per M3w rule 5).
  D1 (NNLO) only with the 30 % band, labelled CONDITIONAL.
- T2: Δ_L/L2 = (1 + ε̂)/(1 − ε̂) against the large-N_c lattice Δ_L = (−0.12 ± 0.22)·10⁻³ (FPRS quote), using the fitted
  family's L2 in units of F²/m_ρ² (needs F/m_ρ as input, stated).
- T3: O(p⁶) ratio g̃3,1/g̃3,0 of M_ε(ε̂) and its position in Li's (2310.09698) O(p⁶) region (consistency only; the
  O(p⁶) C_i data are prior-driven, BE14 §4, so no data comparison).

## 8. Kill criteria and anti-post-hoc rules

- Kill (family): Step 0 ILL-POSED, or ε̂ outside [−1, 0] by more than 2σ. Then the chord is excluded as a model of
  O(p⁴) + ρ data.
- Kill (prediction): §6 FAIL.
- No switching to Coon (M3c) or another chord after seeing M3b numbers without a new, separately labelled prereg.
  The components, the normalisation (m_ρ = 1, LS with scalars), the observables, the data and the bands above are frozen.
- Lean (planned): the Möbius inversion ε̂(g̃ρ²) as an exact identity, and the endpoint values as exact facts.

## 9. Open questions for the re-read

1. LS **with** scalars (as in M3) vs **scalar-less** LS (FPRS eq. 113, ε ≈ −0.86, already near the ρ edge): which
   endpoint should "the hidden-zero completion" be? With scalars is frozen here, because it is the M3 object and has
   ε = 0 exactly. Scalar-less LS is not a hidden-zero amplitude.
2. Is g̃ρ² clean enough in 1/N_c to measure ε? ±30 % is a convention.
3. Should M3c (Coon, geometric q) run before M3b? It is the closer answer to "is ε geometric?", but its reachable range
   is unknown.
