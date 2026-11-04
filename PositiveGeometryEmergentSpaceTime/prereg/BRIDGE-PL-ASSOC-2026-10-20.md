# PREREG BRIDGE-PL-ASSOC (mission rung): can the Plücker → torus orbit → hypersimplex → associahedron chain constrain a U(1) charge (hypercharge)?
Written 2026-10-20 by Grok. Continuous mode; approved by author approved. STOP absent on origin/main at rung start.
Pushed ALONE (with its locked checker, planted spec and import test) before any checker computation. No physical datum enters this rung.

## 0. Re-read (done first)
- STRUCT-1 (reviews/STRUCT-1-result-2026-10-15.md): `hypercharge_unique` — ACC + no νᶜ + yQ ≠ 0 ⇒ SM hypercharges up to normalisation and uᶜ↔dᶜ; geometry NO-LINK; reopen trigger: "a Lean theorem in a geometry module whose conclusion is one of the ACC equations".
- STRUCT-1b: with νᶜ, Majorana restores uniqueness; Dirac Yukawas do not (B−L); geometry NO-LINK.
- notes/GEOMETRY-STRUCT-SEPARATION-2026-10-15.md: 0 Lean cross edges geometry↔STRUCT; "charges enter only through the choice of gauged subgroup … which is an input"; reopen: "a canonical form or residue that depends on a charge matrix Q, with a Lean identity to ACC".
- Queue: BACKLOG (STRUCT-1 line) "BRIDGE-PL-ASSOC via XD-2 moment-map route (pl → torus orbit → hypersimplex → Assoc planar X_ij, n=4,5)"; notes/BRIDGE-PL-ASSOC-2026-10-15.md (XD-1, PARTIAL: `moment_in_hypersimplex24/25`, `planar_three_channel`, `pl_assoc_bridge`; graph unification only, "moves no SM ledger line", EV capped 0.03).

## 1. Standard maps (CITED; verified on arXiv abstract pages where on arXiv)
1. Gr(2,n) ⊃ Gr₊(2,n), Plücker coordinates; column torus T = (ℂ*)ⁿ acts by P ↦ P·diag(t). Moment map of the closure of a generic T-orbit has image the hypersimplex Δ(2,n); torus orbits ↔ matroid polytopes (Gelfand–Goresky–MacPherson–Serganova, Adv. Math. 63 (1987); restated in Lukowski–Parisi–Williams 2002.06164 abstract).
2. Positroid dissections of Δ(k+1,n) ↔ images of positroid cells (LPW 2002.06164).
3. Trop⁺Gr(2,n) is the Stanley–Pitman fan, "combinatorially the fan dual to the (type A_{n−3}) associahedron" (Speyer–Williams math/0312297).
4. Gr₊(2,n)/T = M₀,ₙ⁺; its compactification/u-variables give the associahedron as a positive geometry with canonical form (Arkani-Hamed–Bai–Lam 1703.04541; Arkani-Hamed–He–Lam 1912.08707); kinematic associahedron with planar X_ij (Arkani-Hamed–Bai–He–Yan 1711.09102).
Already in Lean (XD-1): moment map into Δ(2,4), Δ(2,5); planar three-channel identity; Assoc chart skeleton.

## 2. The bridge claim and the SM object (new, mission-relevant)
- **SM object:** the hypercharge vector Y of one generation and the four perturbative ACC of STRUCT-1 (`STRUCT1.ACC`), field content ASSUMED (STRUCT-1 hypotheses).
- **How a charge can enter the chain:** only as a cocharacter of the column torus (columns = SM multiplets, n = 5, or Weyl states, n = 15): t = exp(τλ). Two declared maps, no others:
  - **M1 (quotient level, where the associahedron/planar X live):** λ ↦ all cross-ratios / u-variables of t_λ·P.
  - **M2 (equivariant level, before the quotient):** λ ↦ moments m_d(λ) = E[⟨λ, μ⟩^d] of the uniform measure on Δ(2,15); conditions m₁ = 0 (⇔ Tr Y = 0, the gravitational ACC) and, on m₁ = 0, m₃ = κ·Tr Y³ (Lean `sym_cubic_reduction`, `triple_sum_five`), so m₃ = 0 ⇔ the U(1)³ ACC when κ ≠ 0.
- **LINK (theorem with falsifiable alternative):** the chain's property P(M(λ)) holds iff λ satisfies ACC, so that with STRUCT-1 it fixes Y up to normalisation (N_M2 = N_ACC), AND the link is earned: rival non-amplitude polytopes do not reproduce it (κ = 0 for both rivals Δ(1,n) simplex and [0,1]ⁿ cube). Or M1 is charge-sensitive.
- **NO-LINK:** M1 charge-blind and M2 not earned (a rival reproduces it, or it does not discriminate SM from non-SM charges).
- **Null / rival structures:** charge rivals B−L and a non-anomaly-free vector (1,…,5)/7 for M1; polytope rivals Δ(1,n), [0,1]ⁿ for M2.
- **Well-posedness:** both maps and the rule are explicit theorems/computations with a falsifiable alternative ⇒ well-posed (not ILL-DEFINED).

## 3. Foregone check (declared; Lean `PositiveGeometryEmergentSpaceTime.BridgePLCharge`, compiled BEFORE this prereg, no physical input)
- M1 is FOREGONE CHARGE-BLIND: `uCR_torus_invariant`, `uCR_charge_blind`, `uCR_rival_indistinguishable` (every cross-ratio is invariant under every torus element; the associahedron is built on Gr₊/T, so a charge is quotiented out by construction). `pos_torus`: positivity imposes nothing on λ. `X13mono_torus`: chart monomials only pick up a common weight.
- M2 cannot be EARNED: `simplex_kappa_pos` (κ = 2/(n(n+1)(n+2)) > 0 for the simplex rival, Dirichlet moments CITED). Whatever κ(Δ(2,15)) is, the rival simplex yields the same constraint set (Tr Y = 0, Tr Y³ = 0) — a symmetric-function fact true of every Sₙ-symmetric, non-centrally-symmetric measure (`sym_cubic_reduction`). `cube_kappa_zero`: centrally symmetric rivals give no cubic constraint.
- **Hence the overall verdict NO-LINK is FOREGONE.** Not foregone, and recorded: κ(Δ(2,15)) (sign, nonzero?), and N_M2 (how many non-SM hypercharge vectors the two trace conditions admit). Also expected: M2 at multiplet level (n = 5, unit multiplicity) is violated by SM Y (Tr Y ≠ 0) — report-only.

## 4. Planted and broken
- Planted: slice-integral κ(Δ(1,n)) equals Dirichlet 2/(n(n+1)(n+2)) for n = 5, 8, 15 (exact); κ(Δ(2,4)) = 0 (octahedron); centroid 2/15 on Δ(2,15); full-ACC count at yQ = 1 = exactly the two SM branches (−4,2,−3,6), (2,−4,−3,6); M1 invariance on an n = 6 toy; four classifier toys. Any planted failure ⇒ ILL-DEFINED.
- Broken (already proved false, `BridgePLCharge.uCR_rival_indistinguishable`): "SM hypercharge and B−L give different u-variables". Must be REJECTED.

## 5. Anti-numerology and contamination
No numbers are fitted; one declared trial (single rule, M1 ∨ M2). Basis fixed as in STRUCT-1 (p/q, |p|,|q| ≤ 10). Memorised: SM hypercharges, ACC, Dirichlet moments; nothing to mask (no data). The κ(Δ(2,15)) value is unknown to me before the run.

## 6. Prediction
NO-LINK ~99% (foregone). κ(Δ(2,15)) ≠ 0 ~85% (sign negative ~60%). N_M2 > 2 ~95%.

## 7. Guard and locks
Hardened guard as in F-POSGEOM-DAUGHTER: `guard` inside pos_matrix, plk, cross_ratios, torus, state_vector, m1_maxdiff, slice_moment, kappa_*, basis_ints, count_solutions, classify; no pass flag; per-call hash + ancestry re-verification; caches keyed by origin/main sha; fetch once per process. Import test: 2 direct calls must refuse before the push; before the push only `py_compile` was run.

Locked:
- `sims/bplc/bplc_checker.py` sha256 `ecf1cea66f24e9fce07df9dd4db8f3d947cd296b98207a55eee8acdea3d8ca29`
- `sims/bplc/planted_cases.json` sha256 `8649cedb2785fe5484a66b02cbb83238972bd16001c345700cae8dca9fff09cc`
- `sims/bplc/import_guard_test.py` sha256 `b5ece36fea28840fec10ba4e493b8e3f0e625d2f821a037fd2b1bd1f86b9616e`
