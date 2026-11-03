# PREREG FL-1Z: does a modular fixed point (τ = i or ω) give a fit-free neutrino prediction?
Written 2026-10-22 (Grok). The author-directed manual frontier rung (the author: "keep frontier research … formal lean maths and simulations"). It is not an AutoResearch run.
AUTORESEARCH-STOP: the stop file was added in 87a7a1f and removed in 343ae42 ("author approved",). This rung does not depend on that file. The conflict with "AutoResearch stays paused" is flagged for the author in the INT-1 and FL-1Z reports.
Immutable after push. Any change goes into a new dated amendment file.

## 0. Up-front well-posedness declaration (required by the rung instruction)
The instruction says: "if the model can't be chosen without effectively fitting, or no correlation is independent of the free distance, record FL-1Z as NOT-WELL-POSED".
At prereg-writing time I declare **FL-1Z = NOT-WELL-POSED as a TS-1 prediction**, for three reasons. All of them come from reading 2502.12662 (fetched this run), not from any output of this rung.
1. **Fitting.** The one published minimal model (Zee–Babu + non-holomorphic modular A4, 2502.12662) fixes the weights and representations by hand (Tab. I). It then fits 4 real parameters (τ, b̃_k ∈ ℂ) to 5 oscillation observables, and (a_e, b_e, c_e) to the 3 charged-lepton masses. Best Δχ²_min ≈ 16, and s12² lies outside 3σ (Tab. II).
2. **Exact fixed point excluded.** At τ = ω the model has b̃_k = 0 (Y1^(−2)(ω) = 0), and m_ν is rank 1 with two massless neutrinos (App. D). Every viable point sits at |τ − ω| ≈ 0.006, which is a free distance.
3. **The ε-independent outputs are not fixed-point outputs.** m1 = 0 and the normal ordering come from the antisymmetric Zee–Babu coupling f (rank 2), which holds for every τ. They do not come from the fixed point.
What the rung still does: it reproduces the published exclusion as a planted test, proves the structural facts in Lean, and tests reason 3 and the "free distance" claim numerically. A kill criterion is attached to the declaration (§6).

## 1. Hypothesis (H, the thing that would make FL-1Z well-posed)
Some neutrino observable O ∈ {ρ, s12², s13², s23², |m_ee|/m3} is independent of the free distance δ = τ − ω and of b̃_k near the fixed point. Such an O is a fixed-point prediction, and it would be the TS-1 entry.

## 2. Exact definitions (model fixed now, before any output)
- Forms: Y3^(0) = (y1, y2, y3) and Y3^(−2) = (y1′, y2′, y3′) from the q-expansions in 2502.12662 App. A, eqs. (A.1)–(A.6), truncated at order n ≤ 4.
- Mass matrices (dropping the overall v/√2 and κ):
  - M_ℓ = a_e P + b_e S(Y0) + c_e A(Y0)
  - f = A(Y0)
  - g = S(Y−2) + b̃_k P
  - m_ν = f · conj(M_ℓ) · g · conj(M_ℓ)ᵀ · fᵀ
  - Here P is the permutation matrix (1)(23), S is the symmetric triplet matrix and A the antisymmetric one, as in eqs. (III.2) and (III.16).
- Charged-lepton fit: (β, γ) = (b_e/a_e, c_e/a_e) are solved so that the eigenvalue ratios of M_ℓ M_ℓ† equal (m_e/m_τ)² and (m_μ/m_τ)². Every branch found from 40 seeded starts is kept.
- PMNS: U = V_L† V_ν, with V_L the eigenvectors of M_ℓ M_ℓ† and V_ν the eigenvectors of m_ν† m_ν, both in ascending order. Angles are taken from eq. (III.25).
- **Dimensionless target:** ρ ≡ (m2/m3)² = Δm²_sol/Δm²_atm (NH, m1 = 0). The experimental band is [0.02655, 0.03268], from the 3σ columns of 2502.12662 Tab. II.

## 3. Theorem statements (Lean 4 + Mathlib; new module `lean/PositiveGeometryEmergentSpaceTime/FL1Z.lean`, namespace `PositiveGeometryEmergentSpaceTime.FL1Z`; 0 sorry; standard axioms only; no FRONTIER-AXIOM)
- `valence_lt12`: if 12n + 6a + 4b = k (the SL(2,ℤ) valence formula, given as a declared hypothesis, not a Mathlib theorem) and k < 12, then n = 0. So the zeros of a nonzero form of weight below 12 sit only at τ = i or ω. Companions: `valence_k2_empty`, `valence_k4`, `valence_k6`, and `valence_k12_free` (n = 1 is allowed, which is the Δ case).
- `antisymm3_det_zero`: det of [[0,c,−b],[−c,0,a],[b,−a,0]] = 0 over any commutative ring. `antisymm3_kernel`: the vector (a,b,c) is in its kernel. Together these give m1 = 0 for every τ.
- `D3_rank_one`: for ω³ = 1 in a commutative ring, the eq. (D.3) matrix equals w wᵀ with w = (2, −ω², 2ω). `D3_det_zero` is a companion.
- `hierarchy_ratio_surj`: every ρ > 0 is D2²/D3² for some D2, D3 > 0. So ρ alone carries no structural integer.

## 4. Foregone / contamination (declared)
- L2 and L3 are foregone. They are the published result (App. D) and linear algebra.
- I read 2502.12662 Tab. II (the near-ω fit box) before writing this. D3 is therefore report-only.
- The verdict NOT-WELL-POSED is declared in §0 before running. The live run can only overturn it through §6 K1.

## 5. Predictions (written before running)
| # | Prediction | P |
|---|---|---|
| L1 | b0 = −0.2623 and b−2 = 0.4166, each to within 5e-4; residual < 1e-3. My hand estimate from (A.1) and (A.4) is y1(ω) ≈ 0.0874 and y1′(ω) ≈ 0.2778. | 85% |
| L2 | At τ = ω with b̃_k = 0, m_ν is rank 1 and ∝ (D.3) | 90% |
| L3 | m1/m3 < 1e-10 everywhere | 98% |
| L4 | The broken f gives m1 ≠ 0 | 99% |
| D1 | With b̃_k = 0, ρ → 0 as \|δ\| → 0, and ρ varies by more than ×10 across \|δ\| ∈ [1e-3, 3e-2] | 85% |
| D2 | At τ = ω with b̃_k ≠ 0, ρ > 0 and it varies by more than ×10 across \|b̃_k\| ∈ [0.1, 1] | 80% |
| D4 | No observable in {ρ, s12², s13², s23², \|m_ee\|/m3} has relative spread below 1% over D1 ∪ D2 ∪ D4, so NOT-WELL-POSED is confirmed | 95% |
| Br | More than one charged-lepton branch exists at a generic point, which is a further discrete choice | 70% |
| D3 | Report only: the s_ij² sit near the Tab. II box at the box midpoint. No pass/fail. | — |
| D5 | Report only: at τ = i, ρ > 0 | — |

## 6. Pass / fail / kill criteria
- **PLANTED PASS** requires all of L1–L4. If L1 fails, my transcription of the forms is wrong: D1, D4 and D5 are reported as INVALID, and only the exact-eigenvector L2 stands. If L2 fails, my m_ν convention does not reproduce the published exclusion, and that is reported plainly.
- **K1 (kill of the NOT-WELL-POSED declaration):** some observable has relative spread below 1% over D1 ∪ D2 ∪ D4. That observable then becomes a WELL-POSED-CANDIDATE TS-1 entry, and it needs a fresh prereg before any claim.
- **Confirm:** D4 shows no constant observable, and D1 or D2 show that ρ depends on δ or b̃_k. FL-1Z is then recorded as NOT-WELL-POSED, with the reason.
- ε-independent outputs (m1 = 0, NH-preference) get credit 0. They are Zee–Babu-generic, not fixed-point outputs.

## 7. Planted-answer test (inline; list in `sims/fl1z/planted_cases.json`)
- L1: the fixed-point eigenvector reproduction (D.1)–(D.2).
- L2: the published τ = ω exclusion (D.3), with rank 1 and two massless states.
- L3: the Zee–Babu m1 = 0.
- L4: the broken detector.

## 8. Simulation plan
`python sims/fl1z/fl1z_checker.py planted` writes `sims/fl1z/fl1z_planted.txt`. `python sims/fl1z/fl1z_checker.py live` writes `fl1z_output.txt` and `fl1z_live.json`. The scans are:
- D1: |δ| ∈ {1e-3, 3e-3, 6e-3, 1e-2, 3e-2} × 8 phases in [0, π), b̃_k = 0.
- D2: τ = ω, |b̃_k| ∈ {0.1, 0.3, 0.5, 0.7, 1} × 8 phases.
- D3: τ = −0.4958 + 0.8709i, b̃_k = 0.511 e^{±2.07i}.
- D5: τ = i, b̃_k = 0.
- D4: 300 random points with |δ| ≤ 0.03 (Im δ ≥ 0) and |b̃_k| ≤ 1.
- A figure script draws ρ vs |δ| and vs |b̃_k| from the json. The figure is drawn after the run and is not used for any verdict.

## 9. Data sources and tiers
- 2502.12662 v2 (fetched this run, arXiv PDF). It supplies the model, App. A forms, App. D and Tab. II. Tier: primary paper.
- 2506.23343 was fetched earlier in this session and is context only.
- Charged-lepton masses are PDG values used as inputs, not fetched this run; only ratios enter.
- The oscillation bands are NuFit 6.0 as quoted in 2502.12662 Tab. II (secondary).

## 10. Pinned environment
- Python 3.13.5 (<local path>), numpy 2.5.4 (the checker uses numpy and the stdlib only).
- Lean v4.34.1, Mathlib rev d13f23b723b8a846827a245b89c10fc7d3f11612.
- CPU only.

## 11. Guard and run manifest
- `sims/fl1z/fl1z_checker.py` sha256 `54a72162d550bd4b1f34fb54beff00feff7d290ad7aa44b179bfa6c71c5e6665`
- `sims/fl1z/planted_cases.json` sha256 `ea203ece91c1cf53e30404432d65b66aa77106c229f4e5374a68edcec1fcff2c`
- `sims/fl1z/import_guard_test.py` sha256 `d719ad1382a8595cb76d7fb9c97cd27a5d5f76c29e6027dc8fad8cd82cb67fd2`
- Run id FL1Z-2026-10-22-r1. Seed 20261022; the planted test uses seed +1.
- guard refuses every scoring call unless this file's adding commit is an ancestor of origin/main and the checker hash matches. The refusal is recorded in `sims/fl1z/guard_refusal.txt` before the push.
- Manifest: the planted run, then the live run, then the Lean build, the axioms file `lean/axioms/FL1Z_output.txt`, and the review `reviews/FL-1Z-result-2026-10-22.md`.
