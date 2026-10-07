# MVP-2 dictionary

One chart of `Gr⁺(2,4)`. The orthant coefficient is already proved. This page is the algebraic face of that coefficient. A GeV is not among the outputs.

The proofs are in `mvp0/lean/UOPG0/Boundary.lean`. They use the MVP-1 chart. They do not import `UOPG.lean` or `UOPGv2.lean`.

| Proved | Interpretation | Not claimed |
|---|---|---|
| `adjacentProduct (chart x y z w) = 0` if and only if `x = 0` or `y = 0` or `z = 0` or `w = 0`. | The denominator of `1/(x y z w)` knows only the coordinate walls. | A differential form, or a pole in the sense of a contour integral. |
| The same statement with `P01`, `P12`, `P03`, and `P23` in place of the four coordinates. `P13` is not in that list. | The walls of this chart are the ordered adjacent minors. | That every boundary of `Gr⁺(2,4)` has been listed. |
| On a face, one coordinate satisfies `≥ 0` and the other three are positive, and `P13 = y z + x w` is positive. At the witness face `x = 0`, `P13 = 3/4`. | The non-adjacent minor is not the wall you hit by setting one adjacent minor to zero. | That `P13` never vanishes on a deeper stratum. It does, once two coordinates are zero. |
| At `(1, 1, -1, 1)`, `P13 = 0` and the adjacent product is `-1`. | Vanishing of `P13` is a different condition, and this witness of that fact is outside the positive chamber. | A sign-flip that stays in `Gr⁺`. |
| If `x, y, z, w` are all nonzero, then `x /(x y z w) = 1/(y z w)`, and likewise for `y`, `z`, and `w`. The right-hand side does not contain the cancelled variable. | The orthant coefficient factors onto the opposite 3-orthant. On the witness the values are `8/3`, `8/3`, `8`, and `8/3`. | A residue in de Rham cohomology. A factorization into scattering amplitudes. A cross section. |
| Replacing column 3 by `column 3 + 1 · (column 1 + column 2)` at the positive witness sends `P23` from 1 to 0. The Plücker quadric still vanishes. | One map from the 2026 drafts walks out of the chamber and stays a 2-plane. | That the map is a cluster mutation. That every positive `λ` does this. A definition of mutation. |

Exported theorems use no `sorry`. Their axioms are among `propext`, `Classical.choice`, and `Quot.sound`.
