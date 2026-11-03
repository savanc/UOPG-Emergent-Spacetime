# Candidate sweep for the last OP-2 blind prediction (0.5) — 2026-10-13
- Scope: (a) the fermion/boson boundary, (b) giant scales, (c) electroweak and above.
- No target values were read. This is analysis plus memory, disclosed per row.
- Tags: CONJECTURE, SPECULATION, CITED (from memory unless noted).
- MR-2e credit stays 0.

## Input-ledger proposal (honest counting across sectors)
OP-2's scale no-go (PROVED) means every sector needs one dimensionful unit. The proposed rules:
1. **One declared unit per sector** in the ledger (m_ρ for mesons, m_N for baryons, M_BH for Kerr, v for EW). It costs nothing, but it must be declared in the prereg.
2. **Every further input** (m_s / MK, g′/g, λ, BH spin a) counts as one dimensionless input.
   - A sector contributes credit only if its number of independent pre-registered predictions exceeds its number of extra dimensionless inputs.
   - In each new sector, the first prediction pays for the first extra input. So the sector shows net predictive power or earns nothing.
3. **Standard-theory reproductions earn ≤ 0.25.** These are predictions any SM/GR calculation makes without our geometry, e.g. Kerr κ = 1 or ρ_EW = 1. Full credit needs geometry-specific content: a hidden-zero line, an LS ratio, or a positivity cell not implied by standard symmetry alone.
4. **Blindness discount.** Partial memory of the target caps credit at 0.25. Score on combinations not memorised.

## Ranked table
| # | Candidate | Theory readiness | Well-posed / ≥2 quantitative sources | Blindness (memory disclosed) | Null discrimination | Novelty | Cost | P(+0.5) |
|---|---|---|---|---|---|---|---|---|
| 1 | **MR-7: πN hidden-zero line** s = m_N² + Mπ² (p_N·p_π = 0, MR-4's structure with K → N), tested on the isospin-even/odd subthreshold expansion (D = A + νB) | medium-low: needs a fermion extension of the CGW zero (CONJECTURE). The tree gate needs Weinberg–Tomozawa + pseudovector Born in relativistic ChPT, and the nucleon pole near s = m_N² may spoil a clean line. | **likely yes**: πN Roy–Steiner subthreshold parameters (Hoferichter–Ruiz de Elvira–Kubis–Meißner 2015/16), Karlsruhe–Helsinki KH80 (Höhler), GWU/SAID | **medium**: I vaguely recall d⁺00 ≈ −1.4 Mπ⁻¹ and σ_πN ≈ 45–60 MeV; I don't recall the other d_ij / b_ij. Score on the slope/residual combination along the line, not d⁺00. | expected good (the random-line null, as in MR-4) | **high**: hidden zeros with fermions are open (CGW, scalars/gluons only) | medium (theory gate ~1 rung) | **~0.25** |
| 2 | MR-8: baryon LS/Regge coupling ratios on the Δ trajectory: Δ(1232) → Δ(1950) 7/2⁺ → Δ(2420) 11/2⁺ Nπ couplings | low: fermionic dual amplitudes (Neveu–Schwarz-type, πN Veneziano) exist but are not in our LS code | PDG lists Nπ fractions with several analyses (likely) | **low–medium**: I recall Δ(1950) Nπ ≈ 40% roughly, Δ(2420) only vaguely | moderate (wide 1/N_c bands) | medium (prior art: dual πN amplitudes) | high | ~0.1 |
| 3 | BH-4: Kerr spin-induced quadrupole κ = 1 (BH-1 minimal coupling) vs LVK GW constraints, or BH tidal Love number = 0 | **ready** (BH-1/BH-2 PROVED structure) | yes: LVK GWTC tests-of-GR papers, independent analyses | high (I don't know the κ posteriors) | poor: bounds are O(1–10) wide, and NS-like κ is also allowed | **none**: it is GR (rule 3, ≤ 0.25) | low | ~0.05 effective |
| 4 | EW-1: SMEFT dimension-8 positivity (aQGC signs, f_T/f_M combinations) as positive-geometry cells, vs CMS/ATLAS aQGC limits | medium: positivity cones are prior art (Remmen–Rodd, Zhang–Zhou); our EFT-hedron Lean (M2b) covers moments | yes (ATLAS, CMS) | high | **poor**: limits contain 0, so a half-space test is weakly discriminating | low (prior art) | medium | ~0.05 |
| 5 | EW-2: ρ_EW = 1 / custodial symmetry from the OP-1 stabiliser | ready-ish | yes | **no**: values known | – | none (SM) | low | 0 |
| 6 | EW-3: Higgs self-coupling λ, or m_H/v | not posable: λ is unfixed by on-shell consistency (MG2-0, PRD 2026) | κ_λ bounds wide | – | – | – | – | 0 |
| 7 | Longitudinal WW scattering / unitarity sum rules (κ_V = 1) | partial: CGW zeros cover only adjoint SSB; the doublet is open (MG2-2) | yes | known (κ_V ≈ 1) | weak | low | high | ~0 |
| 8 | HQET/heavy-quark spectra (D, B, Υ) ratios | not in our framework: needs heavy-quark symmetry input; ratios like hyperfine splittings are prior art | yes | values partly known | – | low | high | ~0 |
| 9 | Neutron-star EoS / supernova ν | no framework link | – | – | – | – | – | 0 |
| 10 | SUSY-like Bose–Fermi relations | SPECULATION; no data | – | – | – | – | – | 0 |

## Recommendation
**Top: MR-7 gate (πN hidden-zero line).**
- **Step 1, theory:** derive the tree amplitude (Weinberg–Tomozawa + pseudovector Born + c_i at O(p²)) with sympy, and check whether D^{3/2} (π⁺p) vanishes on s = m_N² + Mπ² at LO.
- **Step 2, Lean:** formalise the line algebra, reusing `PositiveGeometryEmergentSpaceTime.PiKZero`.
- **Step 3:** digit-masked structure check of the subthreshold tables in Hoferichter et al. 2015 and KH80.
- **Step 4:** prereg the r/r0/r1 + random-line null exactly as in MR-4, scoring on non-memorised combinations.
- Stop if the LO amplitude has no zero line (as with πη in MR-5), or if the nucleon pole makes the line ill-defined.

**Fallback: MR-8 gate** (dual πN amplitude prior-art sweep plus a digit-masked PDG Δ-trajectory structure check).

**Not recommended for credit:** BH-4 and EW-1 (reproductions of GR/SMEFT; rule 3). They are still worth doing cheaply as consistency checks.
