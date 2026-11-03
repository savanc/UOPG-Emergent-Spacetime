# COS-1r result: 2610.01775 does not fix c or give physical wavefunction zeros — FAIL (2026-10-13)

Prereg: `prereg/COS-1r-2610.01775-reopen-check-2026-10-13.md` (594344a; data cells: none). Script: `sims/cos1r/cos1r_check.py` → `_output.txt`. Source: arXiv 2610.01775 (Rodina), read-only.

## Q1: an NLSM cosmological wavefunction? NO
The paper's NLSM results (§4, §6.2) are flat-space *amplitudes* from the δ-shift. Its cosmological objects (§2, §5, §6.3) are kinematically mapped Tr φ³ tree functions ψ_G(s) = Σ_{maximal tubings} Π 1/s_S (eq. 2.14), where tube energies are replaced by Mandelstams. The paper itself says this map "is distinct from taking a total-energy residue". There is no NLSM wavefunction and no boundary term, so c is not fixed.

## Q2: physical zeros? NO
I reimplemented ψ_G from the paper's tubing rule. "Nested or disjoint" reproduces its counts: chain 5, 222 6, 223 18. (A non-adjacency variant gives chain 4, so it is not the paper's rule; the first run used it and was corrected.) Results on each quoted zero, with mapped kinematics s_V = 0:

| Zero | ψ on locus | points with all s_S > 0 | forced sign pairs (examples) |
|---|---|---|---|
| 222 blob c₁₂=c₁₄=0 (5.11) | 0 ✓ | 0/20000 | s₁₃ = −s₂₃₄ |
| 222 non-blob (6.15) | 0 ✓ | 0/20000 | s₂₃ = −s₁₃ |
| 2222 non-blob (6.16) | 0 ✓ | 0/20000 | s₁₃ = −s₃₄, s₁₂₃₄ = −s₁₂₃₅ |
| 223 non-blob (6.17) | 0 ✓ | 0/20000 | s₁₂₃₄ = −s₄₅, s₂₃₄₅ = −s₃₄ |

Every zero locus forces pairs of channels of opposite sign. Since ψ_G is a +1-weighted sum of products of 1/s_S, a zero with all s_S > 0 is impossible (Lean `PositiveGeometryEmergentSpaceTime.COS1.sum_pos_ne_zero`, reused). Under the identification E_S ↔ s_S with E_S > 0, none of these zeros is physical.

As a side check, I independently reproduced the paper's four zero claims (ψ = 0 exactly), its tubing counts, and the regularity of the loci (no channel identically 0).

**Verdict: FAIL** (per prereg). COS-1b's reopen trigger is not met by 2610.01775.

## Blocker tags
`NO-GO` (positive-sum mapped wavefunctions) and `FRONTIER-THEORY`. Restated reopen trigger: a wavefunction formula with *sign-indefinite* coefficients and a fixed boundary term, e.g. spinning or NLSM wavefunctions from a cosmohedron-type canonical form with signed numerators (COS-1c).

## Proposed credit (NOT awarded): 0.
