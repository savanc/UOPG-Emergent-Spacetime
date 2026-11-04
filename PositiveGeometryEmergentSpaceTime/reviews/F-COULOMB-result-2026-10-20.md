# F-COULOMB result (frontier, 2026-10-20). Verdict: **CONTINUOUS (NO-GO for quantisation by positivity)**
Written 2026-10-20 by Grok (AutoResearch executor). author approved,; STOP removed in 4f51c67.
Prereg: `prereg/F-COULOMB-2026-10-20.md`, commit 19a54a4 (pushed alone). Lean module: `PositiveGeometryEmergentSpaceTime.FCoulomb`.

## Question
Does positivity of the deformed amplituhedron (arXiv:2311.10814, CITED, read-only) quantise dimensionless mass ratios?
SM ledger line: mass ratios.

## Paper content used
- Eq. (1): the 4-pt one-loop inequalities.
- Eqs. (4)–(5): the shifted X̂_i with ρ, ρ̃, η, η̃.
- Eqs. (6)–(8): the deformed region, a product of two wedges, with existence condition ρρ̃ < 1 and ηη̃ < 1.
- Boundary counts (4,6,4,2).
- Eq. (21): u = (1+ρρ̃)²/(4ρρ̃).
- Eq. (22): the masses m₁…m₄ enter as inputs; Sec. IV: n⁽¹⁾ is not fixed.
- Sec. V: the VEV link is conjectural.

## Guard (hard precondition)
`fcoulomb_checker.py` refuses every mode unless, after `git fetch`:
- the commit that added the prereg is an ancestor of origin/main, AND
- the checker's own sha256 equals the hash in the prereg.

Proof that it refused before the push: `sims/fcoulomb/guard_refusal.txt`. At, with the prereg committed locally but not pushed, the run gave `GUARD REFUSED: prereg commit 19a54a45a is not an ancestor of origin/main (not pushed)`, exit 1. Before the push the only other test was `py_compile`.

## Planted pair (after push; `fcoulomb_planted.txt`)
Planted, all recovered:
- the undeformed point is in region (1);
- u(¼) = 1.5625;
- the planted quantising rule gives QUANTISED [1, 1];
- the planted continuous rule gives CONTINUOUS [31, 127].

Broken: ρρ̃ ∈ (1, 2) gives EMPTY [0, 0], so the checker REJECTs it (exit 1, as required).

## Live result (`fcoulomb_output.txt`)
- ρρ̃ ∈ (0, 1): CONTINUOUS [63, 255], i.e. every grid point is allowed.
- Mass-ratio proxy ρ/ρ̃ = e^(8t−4): CONTINUOUS [63, 255].
- Sampled u ∈ [1.000004, 64.5], all > 1.
- Edge: 0.999 is allowed and 1.001 is not, matching the open bound ρρ̃ < 1.

## Lean (`PositiveGeometryEmergentSpaceTime.FCoulomb`, 8 theorems + 3 defs, 0 sorry, no native_decide, standard axioms only, #lint clean)
- `wedge_nonempty_iff`: the eq. (7) wedge is non-empty ⇔ ρρ̃ < 1.
- `crossRatio_gt_one` and `crossRatio_surj`.
- `allowed_u_eq_Ioi`: the allowed set of u is exactly (1, ∞).
- `allowed_u_infinite`.
- `rho_ratio_free`: ρ/ρ̃ can be any q > 0 at any product r.
- `mass_ratio_free`: for every u > 1 and q > 0 there exist (s, m₁, m₃) with m₁/m₃ = q satisfying eq. (22).
- `fcoulomb_continuous`: bundle of the above.

CITED, not formalised: the reduction from the momentum-twistor brackets (1), (4)–(6) to the wedges (7)–(8). It is checked numerically in the checker (`deformed_ok` against Vandermonde twistors).

## Verdict
CONTINUOUS. All prereg conditions hold: both ratios are CONTINUOUS and Lean proves allowed-u = (1, ∞). No refutation criterion (a), (b) or (c) was triggered. Positivity imposes only open inequalities; the face structure is the same on the whole region; nothing discrete appears.

## Gates
N = 4 SYM on the Coulomb branch is not an experimentally established theory, so no GATE-FAIL can arise from it. Measured real-particle mass ratios are non-trivial, which conflicts with neither outcome.

## No-go assumptions changed (Exclusion)
- `BR4.no_scale` (scale-free): the deformation brings in masses. The outcome is consistent with BR-4, because the masses are still inputs.
- `PG1.ratio_not_fixed`: the fixing mechanism tried here is positivity. It does not fix the ratios either.
- New Exclusion row: `FCoulomb.fcoulomb_continuous`.

## Blocker and reopen triggers
NO-GO. Reopen if any of these appears:
- a closed/compact positivity condition (equalities, not inequalities);
- an integrality condition, e.g. requiring integer boundary-face multiplicities or a canonical form with integer residues in ρρ̃;
- a geometry where n⁽¹⁾ or the VEV is fixed and feeds back into the masses;
- higher-loop deformed geometries with non-convex allowed sets.

## Lesson
Positivity regions defined by strict inequalities are open sets. Their parameter images are open, so they cannot quantise unless something adds a discrete (topological or integrality) condition. Screen any future "positivity quantises X" idea for such a condition before running it.

## Credit (proposal only)
0 (a NO-GO that confirms the prediction; adds one Lean no-go row).
