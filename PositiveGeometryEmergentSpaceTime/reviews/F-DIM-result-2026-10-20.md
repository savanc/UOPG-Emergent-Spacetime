# F-DIM result (frontier, 2026-10-20). Verdict: **ILL-DEFINED** (planted pair failed: the broken case was mis-specified). Live NOT run.
Written 2026-10-20 by Grok (AutoResearch executor).
Prereg: `prereg/F-DIM-2026-10-20.md`, commit e97e8ec (pushed alone). Lean: `PositiveGeometryEmergentSpaceTime.FDim`.

## Question
Is the trunk forced into a spacetime dimension by its consistency conditions, and which integers come with it?
- Trunk objects: Gr₊, ABHY associahedron, amplituhedron, and the LS pion amplitude.
- Conditions: positivity, factorisation, unitarity, anomalies.
- Candidates: 4, 8, 10, 11, 16, 24, 26.
- Look-elsewhere set: 38 dimensions (D = 3..40).

## Guard proof
At, with the prereg committed locally but not pushed: `GUARD REFUSED: prereg commit e97e8ec9e is not an ancestor of origin/main (not pushed)`, exit 1 (`sims/fdim/guard_refusal.txt`). Before the push the only test was `py_compile`.

## Planted pair (`fdim_planted.txt`)
- **Planted, recovered:**
  - bosonic Veneziano (m² = −1) → BOUND-ONLY D ≤ 26 ✓ (cited 26);
  - LS α₀ = 1 (NS model) → BOUND-ONLY D ≤ 10 ✓ (cited 10).
- **Broken, NOT rejected:** bosonic Veneziano with m² = 0 also gave BOUND-ONLY D ≤ 26 (levels ≤ 12).
- Per the prereg verdict set ("planted pair fails → ILL-DEFINED"), the rung is **ILL-DEFINED**. The live mode was deliberately **not run**, to keep a corrected rerun blind.

## Diagnosis (post-prereg, exploratory; `broken_diagnosis.py/.txt`)
**What the diagnosis shows**
- The diagnosis evaluated only the bosonic m² = 0 and m² = −1 models, never the trunk LS model.
- **The checker is right and the broken spec was wrong.** With m² = 0, levels 0–7 stay positive at D = 27. The first violation is at N = 8, spin 0, coefficient ≈ +1.2·10⁻⁵ against σ = −1. So the m² = 0 model also has the bound D ≤ 26, at least for N ≤ 12.
- My pre-registration expectation that it would not give 26 was a hand check of level 2 only. That check was inadequate.
- **The real string differs in where it fails:** with m² = −1, the first violation at D = 27 comes at level N = 2 (spin 0).
- Whether the m² = 0 bound at 26 holds at higher levels is not established. This is a side observation (UNVERIFIED), not a claim.

**How it was run**
- The diagnosis imports the locked checker's functions directly, so it bypasses `main` and therefore the guard.
- The prereg was already on origin/main, so the guard would have passed.

## Lean (`PositiveGeometryEmergentSpaceTime.FDim`, analytic; independent of the checker; 0 sorry, standard axioms only)
- `quadratic_gegenbauer`: exact spin decomposition. The spin-0 part of a x² + b x + c is a/(D−1) + c.
- `lsLevel1_eq`: the level-1 LS residue is (α₀/4)(9α₀x² + (6−6α₀)x − (2−α₀)).
- `ls_spin0_nonneg_iff`: spin-0 positivity holds ⇔ D ≤ D_c(α₀) = 2(1+4α₀)/(2−α₀). This reproduces Bianchi–Consoli–Di Vecchia 2021 (CITED-REPRODUCED).
  *Forward note 2026-10-20 (M6, approved by author approved (2026-10-20); [notes/NOTATION-AUDIT-2026-10-20.md](../notes/NOTATION-AUDIT-2026-10-20.md)): the Lean theorem states this for `lsSpin0`, the spin-0 coefficient *divided by α₀/4*, under `alpha0 < 2` and `1 < D` only. As a statement about the physical spin-0 coefficient it needs **α₀ > 0** (for α₀ ≤ 0 the division flips or kills the sign). Every use here has 0 < α₀ < 2 (α₀ = ½; `lsCritDim_surj`), so no result changes. The text stays as written; read it with α₀ > 0.*
- `lsCritDim_half` (= 4), `lsCritDim_one` (= 10), `bos_spin0_nonneg_iff` (D ≤ 26).
- `lsCritDim_surj`: every real bound > 1 occurs for some intercept. The integer 4 is inherited from the Adler-zero value α₀ = ½.
- `trunk_bound_not_forced`: at α₀ = ½, D = 3 and D = 4 both pass level 1, and 8, 10, 11, 16, 24, 26 all fail.
- `fdim_bound_not_forced`: bundles the above.

## What stands, and what does not
**Stands (Lean, analytic, level 1):**
- Trunk positivity *bounds* D ≤ 4.
- It does not force D = 4, since D = 3 passes as well.
- None of the author's candidate integers is allowed at the trunk intercept.
- M1 (geometry positivity) forces no dimension (CITED: Postnikov, ABHY, AHTT). It carries only an even/odd-m distinction.

**Open:** the blind high-level test, i.e. whether D = 4 survives every level N ≤ 40. This is deferred to a rerun with a corrected broken case.

## Tags
- Rung verdict: `ILL-DEFINED` (protocol).
- Lean content: NO-GO for *forcing* (level 1).
- Significance of "trunk explains D = 4": the best achievable p is 1/38 ≈ 0.026, so it is NUMEROLOGY by construction. It is also CITED prior art.

## Changed no-go assumptions (Exclusion)
- `Separation.geometry_struct_separation`: now extended to spacetime dimension.
- `X6.positivity_orientation_blind`: positivity is parity-blind but D-sensitive through the Gegenbauer weight.
- New row: `FDim.fdim_bound_not_forced`.

## Gates
D = 4 is established. Level-1 positivity allows D = 4, so there is no GATE-FAIL at level 1.

## Reopen / next
F-DIM′ is the same question with a new prereg and a checker whose guard points to the new prereg. Its broken case should be the trunk model asked to give D ≤ 26. That is analytically impossible by `trunk_bound_not_forced`, since level 1 already caps D at 4.

## Lesson
A broken case must be *provably* wrong, by a theorem or a single exact evaluation that is already established. It must not be a hand-guessed expectation from one level.

## Credit (proposal only)
0.
