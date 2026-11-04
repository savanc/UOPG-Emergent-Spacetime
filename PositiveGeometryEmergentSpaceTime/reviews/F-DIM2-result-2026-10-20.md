# F-DIM′ (F-DIM2) result (frontier, 2026-10-20). Verdict: **BOUND-ONLY (D ≤ 4)**. No dimension forced; D = 4 survives every level N ≤ 40.
Written 2026-10-20 by Grok. Prereg: `prereg/F-DIM2-2026-10-20.md`, commit e23bbdd (pushed alone). Lean: `PositiveGeometryEmergentSpaceTime.FDim` (extended).

## Guard (tightened, per PositiveGeometryEmergentSpaceTime's review)
- `guard` is called inside every scoring function: `residue_poly`, `geg_coeffs`, `positive_at`, `pass_set` and `classify`. It is also called in `main`, and is memoised after it succeeds.
- **Proof, before the push** (`guard_refusal.txt`):
  - (a) CLI `planted` → `GUARD REFUSED: prereg commit e23bbddee is not an ancestor of origin/main (not pushed)`, exit 1.
  - (b) `import_guard_test.py` (imports the module, then calls `residue_poly`) → `IMPORT-AND-CALL: GUARD REFUSED: …`, exit 2.
- After the push, the import-and-call test passed the guard (`fdim2_planted.txt`).

## Planted pair
- **Planted, both recovered:** bosonic Veneziano (m² = −1) → D ≤ 26 ✓; LS α₀ = 1 → D ≤ 10 ✓.
- **Broken:** the trunk (α₀ = ½) asked for D ≤ 26 → BOUND-ONLY D ≤ 4 → REJECT ✓. This is guaranteed by `FDim.trunk_bound_not_forced`.

## Live (`fdim2_output.txt`)
- **Pass set {3, 4} out of 38 dimensions → BOUND-ONLY D ≤ 4**:
  - D = 5 already fails at level N = 1.
  - The only exact zero at D = 4 is (N = 1, spin 0), i.e. the bound is saturated there.
  - Every coefficient at D = 4 for N ≤ 40 has the single sign σ.
- **Candidates:** 4 is allowed; 8, 10, 11, 16, 24 and 26 are not; none is forced.
- **Diagnostics** (off-Adler α₀, levels ≤ 12, not in the verdict): 0.3 → none allowed; 0.4 → {3}; 0.6 → ≤ 4; 0.7 → ≤ 5. These match the level-1 formula D_c(α₀) = 2(1+4α₀)/(2−α₀) = 2.59, 3.25, 4.86 and 5.85. So the level-1 bound is the binding one at levels ≤ 12. The {3} at α₀ = 0.4 is a scan-floor artefact (the scan starts at D = 3), not forcing.

## Sanity check (post-live, guarded, `sanity_check.txt`)
- At D = 4 the checker's level-2 coefficients ×128·σ are [10, 10, 50, 50]. This equals the Lean identity `lsLevel2Half_legendre`, an independent cross-check. At D = 4 the Gegenbauer basis is the Legendre basis.
- At level 40 at D = 4: 42 non-zero coefficients, all with sign σ, the smallest |c| ≈ 2.3·10⁻⁶ (exact rationals).

## Verdict
**BOUND-ONLY (D ≤ 4)**, as predicted. No refutation criterion fired:
- D = 4 is consistent at every level N ≤ 40 (levels 3–40 were the blind part);
- the pass set is not a singleton;
- the scan does not reach 40.

Tags: `NO-GO` for forcing a dimension; NUMEROLOGY for the significance of "explains D = 4" (best p = 1/38); CITED-REPRODUCED. This extends Bianchi–Consoli–Di Vecchia's numerical check from n ≤ 20 to N ≤ 40 in exact arithmetic, at α₀ = ½ only.

## Lean
`PositiveGeometryEmergentSpaceTime.FDim` now has 10 theorems. New:
- `lsLevel2Half_legendre`: at D = 4 the level-2 trunk residue is 10 + 10P₁ + 50P₂ + 50P₃.

Level 1 is still covered by `ls_spin0_nonneg_iff`, `lsCritDim_half`, `trunk_bound_not_forced` and `lsCritDim_surj`. Levels 3–40 are SIMULATED (exact rational checker), not Lean.
*Forward note 2026-10-20 (M6, approved by author approved (2026-10-20); [notes/NOTATION-AUDIT-2026-10-20.md](../notes/NOTATION-AUDIT-2026-10-20.md)): the Lean theorem states this for `lsSpin0`, the spin-0 coefficient *divided by α₀/4*, under `alpha0 < 2` and `1 < D` only. As a statement about the physical spin-0 coefficient it needs **α₀ > 0** (for α₀ ≤ 0 the division flips or kills the sign). Every use here has 0 < α₀ < 2 (α₀ = ½; `lsCritDim_surj`), so no result changes. The text stays as written; read it with α₀ > 0.*

## Gates
D = 4 is established and allowed, so there is no GATE-FAIL.

## Exclusion
- `FDim.fdim_bound_not_forced` row updated: all levels ≤ 40, not just level 1.
- Assumptions changed: `Separation.geometry_struct_separation` and `X6.positivity_orientation_blind`.

## Blocker / reopen
`NO-GO`. Reopen if any of these appears:
- a positivity or unitarity condition with a *lower* bound on D (e.g. loop-level IR or soft consistency in D ≤ 3);
- a geometry whose canonical form needs a specific m, i.e. a forced m = 4;
- the 1-loop non-planar dual-model pole condition (Lovelace's D = 26 analogue for the LS amplitude).

## Lesson
Guarding inside each scoring function closed the import bypass at negligible cost (a memoised git check). A broken case backed by a Lean theorem worked first time.

## Credit (proposal only)
0. The result is a reproduction-plus-extension of cited work.
