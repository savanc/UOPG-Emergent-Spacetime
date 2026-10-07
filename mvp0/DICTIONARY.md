# MVP-0 dictionary

One object: the positive Grassmannian `Gr⁺(2,4)`. One chart: the Klein correspondence. Nothing in the proved column was fitted, and nothing in that column outputs a GeV. Pictures of this table, and of the later rungs that are not theorems, are in [docs/ROADMAP.md](../docs/ROADMAP.md).

The draft files `UOPG.lean` and `UOPGv2.lean` at the repository root are not part of this project. They contain `sorry` and, in the earlier file, `opaque` stand-ins for the real operations. They were left where they are. They are not proofs.

| Statement | Status |
|---|---|
| For every `2 × 4` matrix, `P₀₁ P₂₃ − P₀₂ P₁₃ + P₀₃ P₁₂ = 0`. | Proved. `plucker_relation`. |
| Left `GL(2)` multiplies every Plücker coordinate by `det g`. | Proved. `plucker_gl_weight`, `plucker_gl_weight_det`. |
| Left `SL(2)` (`det g = 1`) fixes every Plücker coordinate. | Proved. `plucker_sl_invariant`, `plucker_specialLinear_invariant`. |
| The rational matrix with rows `(1 1 1 1)` and `(0 1 2 3)` has all six ordered minors positive: `1, 2, 3, 1, 2, 1`. | Proved. `positiveExample_minors_pos`. |
| In the affine chart, the Plücker bilinear of the graphs of `x` and `y` equals `det(x − y)`. | Proved. `pairing_graph`. |
| That bilinear vanishes if and only if `x − y` has a nonzero kernel vector. | Proved. `nullSeparation_iff` and `singular_iff_exists_kernel`. |
| Four twistors with independent consecutive `λ` spinors determine four events `xᵢ`. The edges `pᵢ = xᵢ − xᵢ₊₁` each have `det pᵢ = 0`, and `Σ pᵢ = 0`. | Proved. `edgeMomentum_det_eq_zero`, `edgeMomentum_sum_eq_zero`. |
| Each such edge is a null separation of two points of `Gr(2,4)`. | Proved. `edge_nullSeparation`. |
| A point of `Gr(2,4)` is a spacetime event, and a null edge is a massless boson. | Interpretation. The proved content is the Klein incidence and `det = 0`. The word "photon" is the comparison in `EMPIRICAL.md`, not a theorem. |
| The gauge with `P₀₂ ≠ 0` puts the matrix in the orthant chart, and `1/(x y z w)` is `1` over the ordered adjacent product. The cyclic product is the negative of that product. | Proved in [MVP-1](../mvp1/DICTIONARY.md). |
| That rational function is a differential form, a helicity weight, a momentum delta, or a cross section. | Not claimed. |
| The canonical form is unique for a general positive geometry. | Not claimed. |
| A Hessian of `Σ log\|det\|` is a spacetime metric, and it is positive definite. | Not claimed. The published numerical point has negative Hessian eigenvalues. |
| The update `C[:,−1] ← C[:,−1] + λ(C[:,−2] + C[:,−3])` is a positivity-preserving Plücker mutation. | Not claimed. It is not a cluster exchange. |
| `m_W = 80.4 GeV`, `sin²θ_W`, `m_Z`, `m_H`, or a vacuum expectation value, read off from eigenvalues. | Not claimed. Those numbers were fitted, and MVP-0 has no scale to fit. |
| `UOPG.lean` and `UOPGv2.lean` formalize the paper. | Not claimed. |

The `GL(2)` weight is the corrected form of the old invariance sentence. The scalar `Σ log|det|` is not `GL(2)`-invariant: it shifts by `binom(4,2) log|det g|`. MVP-0 does not use that scalar.
