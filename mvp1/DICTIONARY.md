# MVP-1 dictionary

One object: `Gr⁺(2,4)`. One gauge: columns 0 and 2 set to the identity, which needs `P₀₂ ≠ 0`. The four remaining entries are the orthant coordinates. A GeV is not among them.

The proofs are in `mvp0/lean/UOPG0/Canonical.lean`. They use the MVP-0 Plücker lemmas. They do not import `UOPG.lean` or `UOPGv2.lean`.

| Proved | Interpretation | Not claimed |
|---|---|---|
| On the chart, `P₀₁ = x`, `P₀₂ = 1`, `P₀₃ = z`, `P₁₂ = y`, `P₂₃ = w`, and `P₁₃ = y z + x w`. | These are the Plücker coordinates after the gauge, not a new field. | That the chart is defined when `P₀₂ = 0`. |
| The ordered adjacent product equals `x y z w`. `⟨4 1⟩ = −P₀₃`, so the cyclic product `⟨1 2⟩⟨2 3⟩⟨3 4⟩⟨4 1⟩` equals `−(x y z w)`. | The sign is the order of columns in `⟨4 1⟩`. It is not a convention that can be dropped. | A helicity numerator such as `⟨1 2⟩⁴`. |
| Left `GL(2)` multiplies the adjacent product by `(det g)⁴`. The Plücker relation determines `P₁₃` from the other five. | After the gauge `P₀₂ = 1`, the independent positive data are the four orthant coordinates. That is the dimension `k(n−k) = 4`. | That this counting is a scattering amplitude. |
| If `P₀₂ ≠ 0`, one left `GL(2)` matrix sends columns 0 and 2 to the identity, and it is the only matrix that does. The product is the chart of `(P₀₁, P₁₂, P₀₃, P₂₃)/P₀₂`. | A positive 2-plane, off the wall `P₀₂ = 0`, is one point of the orthant. | A cell decomposition of the whole positive Grassmannian, or a mutation. |
| If those five minors are positive, the four chart coordinates are positive, and every ordered minor of the chart is positive. | The gauge stays inside the positive chamber. | That every boundary of the chamber has been classified. That is MVP-2. |
| The orthant coefficient `1/(x y z w)` equals `1` over the adjacent product. Where the product is nonzero, multiplying back by `x y z w` returns `1`. | This is the rational coefficient of `dlog x ∧ dlog y ∧ dlog z ∧ dlog w` in the physics literature. | A de Rham 4-form in Mathlib. Uniqueness of the canonical form for a general positive geometry. |
| The Parke–Taylor coefficient `−1/(x y z w)` equals `1` over the cyclic product. | Same rational function, written with the cyclic order and the sign from `⟨4 1⟩`. | A momentum delta, a cross section, or an identification with an N=4 amplitude. N=4 is the method that was copied, not the target. |
| On the witness with rows `(1 1 1 1)` and `(0 1 2 3)`, the chart is `(1/2, 1/2, 3/2, 1/2)`, the orthant coefficient is `16/3`, and the Parke–Taylor coefficient is `−16/3`. | The same point as MVP-0, moved by the gauge. `det g = 1/2`, so the adjacent product moves from `3` to `3/16` by the weight `(det g)⁴`. | A fitted scale. `16/3` is not a mass and not a GeV. |

Exported theorems use no `sorry`. Their axioms are among `propext`, `Classical.choice`, and `Quot.sound`.
