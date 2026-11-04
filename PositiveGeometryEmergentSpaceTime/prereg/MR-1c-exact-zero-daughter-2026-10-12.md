# MR-1c prereg: blind exact-zero daughter test (LS ππ) — 2026-10-12

Written and committed **before any data for the candidate states was opened** (no PDG listing, no Roy/GKPY tables read for this rung).

## 1. Which residues are zero [PROVED + SIMULATED]
- LS (α₀ = ½ from Adler zero, m_ρ² = 1, α' = ½), s-channel I=0 ∝ A(s,t)+A(s,u), I=1 ∝ A(s,t)−A(s,u), I=2 = A(t,u) [CITED: Lovelace 1968].
- **Exact zero:** at the f2 level (m² = 3 m_ρ², √3·775 ≈ 1343 MeV) the I=0 residue is pure J=2: **J=0 (scalar) coefficient = 0**.
  Lean: `PositiveGeometryEmergentSpaceTime.LSResidue.f2_level_I0_scalar_zero` (axioms: propext, Classical.choice, Quot.sound).
- Contrast (same file): ρ level has a non-zero I=0 scalar (`rho_level_I0_scalar_nonzero`); f2-level I=1 has a non-zero J=1 daughter, g²/g_ρ² = 1/2 (`f2_level_I1_vector`, `rho_daughter_ratio`).
- Scan levels n=1..6 (`scripts/mr1c_zero_scan.py`, exact sympy) [SIMULATED]: this is the **only** accidental (non-parity) zero. Parity zeros (odd J in I=0, even J in I=1) and the all-level I=2 zero (no exotic resonances) are structural/duality results, not LS-specific.

## 2. Physical state
The only I=0 J^PC=0⁺⁺ state near 1343 MeV is **f0(1370)**. Prediction: g²(f0(1370)→ππ)/g_ρ² = 0 at leading large-N_c.

## 3. Disclosure of prior knowledge (the author + me)
- f0(1370): mass range broad (≈1200–1500 MeV), width ≈200–500 MeV, ππ branching not averaged by PDG to my memory, 4π dominant; its very existence has been disputed (Klempt–Zaitsev 2007; Ochs 2013 vs Bugg 2007); strong mixing expected with glueball candidates f0(1500)/f0(1710).
- f0(500)/f0(980) are messy (known to both of us).
- So the f0(1370) ππ coupling is **not** blind in the sense of "unknown order of magnitude": we already broadly believe it is small/ill-determined.

## 4. Well-posedness / method-fitness gate (decided here, pre-data)
Criteria (all required for a GO): (a) the LS sector in question works at the lower level; (b) target state is established with Γ/m ≲ 0.3; (c) ≥2 independent sources give a ππ coupling with ≤50 % error; (d) mixing with non-q̄q states is subleading (O(1/N_c)); (e) observable is blind.

| Criterion | Status | Reason |
|---|---|---|
| (a) LS scalar sector reliable | **FAIL** | LS's level-1 I=0 scalar is degenerate with ρ (775 MeV, narrow); nature's f0(500) is at ~450–550 MeV with Γ/m ~ 1 and is not a q̄q Regge state at large N_c (Peláez, Phys. Rept. 658 (2016) — CITED). The same model sector already fails one level down. |
| (b) state established, narrow | **FAIL** | f0(1370) Γ/m ≈ 0.15–0.4, existence disputed (§3). |
| (c) ≥2 sources with ≤50 % ππ coupling | **FAIL (expected)** | Roy/GKPY analyses (García-Martín et al. 2011) are reliable only to ~1.4 GeV, i.e. at the f0(1370) edge, and see an inelastic S-wave, not an isolated pole residue; no PDG ππ average. |
| (d) mixing subleading | **FAIL** | glueball–q̄q mixing in the 1.3–1.7 GeV scalar sector is O(1) in practice (three f0's share strength). |
| (e) blind | **PARTIAL** | §3. |

A zero is the *hardest* observable to test: with threshold "R < 0.15" (0.3 × the level-2 J=2 coupling 1/2, i.e. 1/N_c), any upper limit inside a messy scalar sector would PASS trivially, and a large value could be blamed on mixing. Neither outcome is informative.

## 5. Decision (pre-registered)
**MR-1c = WELL-POSEDNESS FAIL. No data check is run.** No numerical pass/fail thresholds are applied because no clean blind observable exists. Not forced.

## 6. Higher-order large-N errors
Would have been 30 % of the natural level-2 coupling (absolute, since the central value is 0) ⊕ level allowance 20 %; recorded only for completeness.

## 7. Follow-ups named now (not run)
- **MR-1d (non-zero daughter):** ρ(1450) as the f2-level I=1 J=1 daughter, predicted g²/g_ρ² = 1/2, m² = 3 (data mass² ratio ≈ 3.6). Needs its own well-posedness check (ρ(1450)/ρ(1700) mixing, ππ BR poorly known).
- **I=2 exotic absence:** clean but generic (duality/Harari–Rosner) and non-blind; could be logged as a CITED consistency check only.

## Prior art (credit)
- **Bianchi–Consoli–Di Vecchia, JHEP 03 (2021) 119, arXiv:2002.05419** explicitly note the absence of a scalar in ππ→ππ at α's = 3/2 for D=4, α₀=½ (eq. 2.8, §4) and explain it as a cancellation between a scalar and a ghost. **This zero is theirs; our new content is only the Lean proof and the isospin-projected scan.**
- Lovelace (PLB 28, 1968) / Shapiro (PR 179, 1969): amplitude and isospin structure. AHRV, Albert–Rastelli (2203.11950), FPRS: positivity/bootstrap of LS-type amplitudes; I did not find them claiming this zero (not exhaustive). Coon: q-deformation, not used here. Whether Lovelace 1968 itself noted the zero: not verified.
