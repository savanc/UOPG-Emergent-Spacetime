# Plan update 2026-10-13: review of the author's external mass-gap analysis

Input: The author's analysis (chat, 2026-10-13), reviewed against the repo state at 0f82db5. Planning document, no rung run.

## Adopted
- **M6 is blocked by the mass-scale gap; pure positive geometry is dimensionless.** Agrees with OP-2 (PROVED, `PositiveGeometryEmergentSpaceTime.ScaleNoGo`: stabiliser data and the LS family are scale-blind) and MR-3.
- **New trade-space entry: "Mass-generating dictionary (one unit + geometric ratios)"**, sub-branches in the author's order:
  1. Spurion NLSM / massive hidden-zero LEC relations (yellow).
  2. Spontaneously broken gauge theories → W/Z/Higgs (yellow, promising bridge). CGW arXiv:2601.16860: hidden zeros survive uniform-mass Trφ³, spurion NLSM and SSB gauge theories, fail for naive massive YM (CITED). Connects to OP-1 (H = U(1)em, PROVED) and BH-2 (AHH massive spinor helicity, PROVED). Needs a pre-registered geometric vev dictionary (K3) before any data.
  3. One external unit + zero extra parameters (yellow) — integrated with OP-2, not duplicated.
  4. Geometric origin of the unit (red). Candidates — dimensional transmutation, compactification, dynamical vev, a period/residue/cell-volume invariant — all SPECULATION.
- Rule "continue MR only on unseen quantities; 1/N_c-band passes count as weak evidence" adopted into MISSION.

## Already done (the analysis is out of date here)
- **MR-2 already ran:** PASS, non-blind, indirect. Zero at P = (M², M², 2M²) ⇔ a2 = 2a1 ∧ 4a1+2a3+a4 = 0 (PROVED); r ≈ −0.0002 (CGL), −0.04 (BCEGS) vs band 1/3, null pass fraction f ≈ 0.35 (SIMULATED). Moderate evidence only.
- **MR-2b failed well-posedness:** ℓ̄1+ℓ̄2 is not lattice-determined (FLAG lists ℓ̄1−ℓ̄2), FLAG 2024 dropped the LEC section (CITED).
- So sub-branch (1) is done for SU(2); its open part is the SU(3) L5/L8 route (MR-2c).
- **Sub-branch (3) = OP-2's restated milestone:** S = {m_ρ, m_π, f_π} → N ≥ 3 zero-fit pre-registered dimensionless predictions; score 1.5/3 (MR-1b blind + MR-2 non-blind).
- Constraints recorded under (3)/(4): MR-3 — positivity forces m_π = 0 in the minimal massive LS (PROVED, `PositiveGeometryEmergentSpaceTime.MassiveLS`), so m_π enters as a quark-mass input; MR-3b — LS g²f_π²/m_ρ² = 1/(2π) vs ≈ 0.50 (KSRF), FAIL ×π (non-blind).

## Corrected
- **MR-1b was BLIND on the couplings** (resonance masses seen), not "partially blind". MR-1 was the non-blind one.
- The analysis treats MR-2 as the next rung; it is the last rung done. The next rung is its SU(3) blind extension, MR-2c.
- "Network branch closed" and "M3 failed", "M1b NO-GO": confirmed, no change.

## MR-2c posability check (FLAG 2019, headings only)
FLAG 2019 (arXiv:1902.08191) §5.3 "Extraction of SU(3) low-energy constants"; Table 25 "Low-energy constants of the SU(3) Lagrangian at NLO with running scale μ = 770 MeV" has columns for L4, L6, L5, L8 and 2L6−L4, 2L8−L5; Table 26 holds further SU(3) NLO LECs (L9, L10). The text notes three Nf = 2+1 SU(3) papers plus one Nf = 2+1+1, and that it is "an open issue" whether m_s ≈ m_s^phys data allow unambiguous SU(3) LECs (CITED). **No values were read**, so blindness holds.

**Verdict: CONDITIONALLY POSABLE.** Gate items, to be cleared before a prereg is frozen:
1. Derive (Lean, as in `MassiveZero`) the SU(3) single-trace massive hidden-zero condition in terms of L-basis LECs. Expected (CONJECTURE): single-trace mass operators are L5, L8 (L4, L6 double-trace, large-N_c suppressed); the condition may also need L1–L3, which are not in Table 25.
2. RG check: L5 and L8 run differently, so a relation like L8 = c·L5 is μ-dependent unless its combination is scale-invariant. Pre-register μ = 770 MeV and a band covering the scale ambiguity, or find a μ-independent form (M3 lesson).
3. Need ≥ 2 independent lattice collaborations for the target combination; report the null pass fraction f.
4. If the map needs a combination FLAG doesn't tabulate → stop, as MR-2b did.

## Rung queue (in order)
1. **MR-2c** — SU(3) massive hidden zero → L5/L8 relation, blind against FLAG 2019 lattice table; well-posedness gate above first. (MG1)
2. **MG2-0** — prior-art sweep + well-posedness: CGW SSB gauge-theory hidden zeros in BH-2 massive spinor language; pre-register the vev dictionary (K3) before any W/Z/H number.
3. **MR series on unseen quantities** toward N = 3 (MG3), e.g. cleaner LS ratios or blind MR-2 if new lattice data appear; 1/N_c-band passes = weak evidence.
4. **MG4** — literature watch only (SPECULATION), until a candidate links to the associahedron/surfaceology chain.
Parked separately: BH-3 (Newman–Janis shift), Physlib PR series (backlog, awaiting the author).
