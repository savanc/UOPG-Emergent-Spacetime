# BRIDGE-PL-ASSOC result — mission rung (2026-10-20, Grok; continuous-mode own pick (author approved 2026-10-20))
**Verdict: NO-LINK (NO-GO), foregone and declared in the prereg.** Credit 0 (proposal). Prereg 65cf592 (pushed alone); housekeeping 18211ad; result commit follows.

## Question
The queued chain Plücker → torus orbit → hypersimplex → associahedron planar X (XD-1 PARTIAL, graph-only) is standard math (CITED: GGMS 1987; Speyer–Williams math/0312297 "Trop⁺Gr(2,n) … combinatorially the fan dual to the associahedron"; Arkani-Hamed–Bai–Lam 1703.04541; Arkani-Hamed–He–Lam 1912.08707; ABHY 1711.09102; Lukowski–Parisi–Williams 2002.06164). Mission question: does it connect to an SM-structure object — the hypercharge vector and STRUCT-1's four ACC (content assumed)? LINK = a chain property that holds iff ACC (fixing Y as in STRUCT-1), not reproduced by rival polytopes; or a charge-sensitive associahedron.

## Re-read
STRUCT-1/1b (anomaly-fixed hypercharges, geometry NO-LINK, reopen = geometry theorem concluding an ACC); Separation note (charges enter only via the gauged subgroup; 0 cross edges); XD-1 note (graph bridge, "moves no SM ledger line").

## Results
- **M1 (associahedron level): CHARGE-BLIND.** A charge enters Gr(2,n) only as a column-torus cocharacter t = exp(τλ). Lean `uCR_torus_invariant` / `uCR_charge_blind` / `uCR_rival_indistinguishable`: every Plücker cross-ratio (u-variable of M₀,ₙ⁺ = Gr₊/T) is invariant for every λ. Numerics: max |Δu| ≤ 5·10⁻⁶¹ for SM Y, B−L and a non-ACC rival at n = 5 and 15. `pos_torus`: positivity constrains nothing. The associahedron is built after the torus is quotiented out, so this is true by construction.
- **M2 (equivariant moments on Δ(2,15), columns = 15 Weyl states):** m₁ = 0 ⇔ Tr Y = 0; on that hyperplane m₃ = κ Tr Y³ (Lean `sym_cubic_reduction`, `triple_sum_five`), κ(Δ(2,15)) = 129017/33392760 ≈ 3.86·10⁻³ > 0 (exact; prediction "negative ~60%" was wrong). So the hypersimplex reproduces the gravitational and U(1)³ ACC — but:
  - **unearned:** the simplex rival Δ(1,15) gives κ = 1/2040 > 0, the same constraint set (Lean `simplex_kappa_pos`); any Sₙ-symmetric non-centrally-symmetric measure does. The cube gives κ = 0 (`cube_kappa_zero`).
  - **non-discriminating:** at yQ = 1 in the STRUCT-1 basis the two trace conditions admit 35 vectors vs 2 under the full ACC; e.g. (yu,yd,yL,ye) = (−7,0,8,−1) (Lean `trace_conditions_not_acc`). SU(3)²U(1) and SU(2)²U(1) are invisible to an Sₙ-symmetric object.
  - report-only: with multiplets as columns (n = 5, unit multiplicity) the SM itself violates M2 (Tr Y = 1/3).
- Planted all OK (Dirichlet κ for n = 5, 8, 15 exact; octahedron κ = 0; centroid 2/15; full-ACC count = the two SM branches; M1 toy; 4 classifier toys). Broken "SM Y and B−L give different u-variables" REJECTED.

## Lean `PositiveGeometryEmergentSpaceTime.BridgePLCharge` (12 theorems + 2 defs; 0 sorry; no native_decide; #lint clean; standard axioms; no FRONTIER-AXIOM)
`pl5_torus`, `uCR_torus_invariant`, `uCR_charge_blind`, `uCR_rival_indistinguishable`, `pos_torus`, `X13mono_torus`, `sym_cubic_reduction`, `triple_sum_five`, `cube_kappa_zero`, `simplex_kappa_pos`, `trace_conditions_not_acc`, bundle `bridge_charge_nolink`.

## Reading for the mission
The kinematic positive geometry is charge-blind at the quotient level and only S_n-generic (trace) at the equivariant level. This sharpens the Separation statement: within this chain, no theorem can conclude a non-abelian ACC. A link requires a new object that breaks Sₙ to the multiplet structure (colour/isospin grading) or a torus-non-invariant canonical form — i.e. new construction (FRONTIER), not more of the same chain.

## Caveats and compliance
Field content and column = Weyl-state assignment are assumptions (STRUCT-1). Only two maps were declared; others are not excluded. Prereg header time 15:20 vs commit 15:18:53 (disclosed in notes/PROVENANCE-CORRECTION-2026-10-20.md). Per the author's 15:22 change, the trade-space figure and the Lean naming map were NOT edited; deltas are in notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-20.md. CREDITS.md, EW-Z1 paths, R4Indep blueprint block, XResearch untouched; STOP not created; nobody contacted.

## Reopen triggers
An Sₙ-breaking (colour/isospin-graded) positroid or canonical form whose invariants reproduce SU(3)²U(1) and SU(2)²U(1); a torus-non-invariant residue with a Lean identity to ACC; an amplitude-specific measure on Δ(2,n) reproducing all four ACC.
