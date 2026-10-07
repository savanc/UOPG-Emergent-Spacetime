# Rank-one dictionary

One object, still: `Gr⁺(2,4)`. This page is a lemma about a singular `2 × 2` matrix. It is not MVP-4.

The proofs are in `mvp0/lean/UOPG0/RankOne.lean`. They use the MVP-0 edge momenta. They do not import `UOPG.lean` or `UOPGv2.lean`.

| Proved | Interpretation | Not claimed |
|---|---|---|
| `det(u vᵀ) = 0`. | An outer product of two vectors in `k²` is singular. | That the two vectors are a unique factorisation. The next row is the ambiguity. |
| `det m = 0` if and only if `m = u vᵀ` for some `u` and `v`. | Rank at most one. This is the factorisation the atlas draws for a null edge. | A preferred spinor frame. A polarisation sum. |
| For `t ≠ 0`, ` (t u) (v / t)ᵀ = u vᵀ `. | The opposite rescaling. The matrix, which is the edge momentum, stays fixed. | A preferred value of `t`. The next row says the momentum cannot choose one. |
| If `t ≠ 1` and `u ≠ 0`, then `t u ≠ u`. Every function of the outer product is unchanged. On edge 0, `t = 2` sends `u` from `(−2, 0)` to `(−4, 0)` and leaves `p` fixed. | The momentum does not determine `t`. A weight in `t` is not a function of `p`. This is why MVP-4 does not turn green. | A wavefunction. A value of the helicity. The two Lorentz `SL(2)` actions. A gluon, a W, a Z, or a fermion. |
| Each of the four polygon edges equals the factor exhibited in the shadow. At `t = 2` the rescaled factors give the same edge. | The picture on the MVP-4 card, for this one rational polygon. | That the card is a theorem. The Lorentz actions of the two `SL(2)`s are not proved. MVP-4 stays a contract. |

The factors are `u = (−2, 0)`, `(0, −2)`, `(2, 0)`, `(0, 2)` and `v = (1, 0)`, `(0, 1)`, `(1, 0)`, `(0, 1)`.

Exported theorems use no `sorry`. Their axioms are among `propext`, `Classical.choice`, and `Quot.sound`.
