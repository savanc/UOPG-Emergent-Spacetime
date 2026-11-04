# H-T2 pre-registration: electrical networks → positroid cells → canonical forms

Date: 2026-10-11 (Europe/London). Pushed before any H-T2 computation. Prior art: `notes/H-T2-prior-art-2026-10-11.md`.
Builds on H-T1 (`lean/PositiveGeometryEmergentSpaceTime/Network.lean`, `MarkovTrace.lean`).

## Re-read gap (what was known before writing)

Known from H-T1 and the prior-art read:
- Lam's map and our n = 2, 3 points (top cells, all Plücker coordinates > 0).
- Lam's f_τ formula and Thm 4.16.
- Lam's open conjecture that E_n is a positive geometry.
- *Fusions* Def. 2 discards probabilities.

Derived by hand before computing, and **therefore not blind**:
- (i) dim Π_{f_τ} = n − 1 + 2c(τ) (prior-art note).
- (ii) The face counts of E_3 from matchings of 6 points (crossing numbers 0:5, 1:6, 2:3, 3:1), i.e. 1 top cell, 3
  facets, 6 codim-2, 5 vertices. So E_3's face poset is **not** that of the 3-dim associahedron (9 facets).
- (iii) The n = 3 grove quadric L₁₂₃ L₁|₂|₃ = L₁₂|₃L₁₃|₂ + L₁₂|₃L₂₃|₁ + L₁₃|₂L₂₃|₁. This suggests a candidate form
  Ω₃ = Res_Q ⟨L d⁴L⟩ / (Q · L₁₂|₃ L₁₃|₂ L₂₃|₁), which in the chart L₁|₂|₃ = 1 is dlog x₁₂ ∧ dlog x₁₃ ∧ dlog x₂₃ in the
  response (Δ-network) conductances.
- (iv) For a connected network, the terminal-column (odd-column) minors all equal L_{1…n}, so the terminal
  projection is the top cell of Gr(n−1, n), the same as *Fusions*' σ for an irreducible chain.

The computations below test these; they are not discoveries made after the fact.

## Targets and criteria

**(a) Cells for n = 3, 4 families.**
- Families: all edge subsets of two planar supergraphs, with terminals on the outer face:
  - n = 3: triangle + centre with 3 spokes (6 edges, 64 subgraphs).
  - n = 4: 4-cycle + centre with 4 spokes (8 edges, 256 subgraphs).
- Method: random positive rational conductances, exact arithmetic.
  - Grove sums L_σ by forest enumeration.
  - Δ_I by Lam's concordance rule (H-T1 script).
  - Grassmann necklace → bounded affine permutation f.
  - Checks: (1) g = f + 1 mod 2n is a fixed-point-free involution τ (an electrical permutation, Lam §4.6); (2)
    c(τ) (chord crossings) = electroid dimension = the Jacobian rank of the response matrix w.r.t. conductances;
    (3) dim Π_f = k(2n−k) − ℓ(f) = n − 1 + 2c.
- **PASS** if all three checks hold for every subgraph (connected or not; cactus strata outside the families are not
  tested). **FAIL** on any exact mismatch, which would mean either our reading of Lam or our code is wrong.
  **PARTIAL** if a check fails only on degenerate inputs (e.g. Jacobian rank on special conductances; then re-run
  with fresh random values).

**(b) Lean.**
- At least one cell identification beyond the top cell: the n = 3 facet network (terminal 1 joined to 2 and 3),
  with exact minors, its zero pattern, Grassmann necklace and decorated permutation, matched to Lam's f_τ.
- The top-cell dimension count: the Y ↔ response map is a bijection ℝ³_{>0} → ℝ³_{>0} (dim = 3 = number of edges).
- The combinatorial identity dim = n − 1 + 2c for all 15 matchings of n = 3 (by `decide` if feasible, otherwise
  SIMULATED).
- **PASS** if the facet identification and the bijection are proved. The `decide` part is optional.

**(c) Canonical form, the falsifiable question.**
- n = 2: the segment, exact.
- n = 3: check the candidate Ω₃.
  - Its poles lie exactly on the 3 facets.
  - Residues reproduce the facets' forms (dlog x ∧ dlog y).
  - The pull-back to Y (star) conductances differs from dlog a ∧ dlog b ∧ dlog c (whose pole a = 0 is codim 2, not a
    facet).
- n = 4: face counts from matchings.
- **PASS (amplitude-like):** the face poset or form of E_3 or E_4 matches a known amplitude geometry after a change
  of variables. Candidates: the associahedron/Tr(φ³) m_n of the same dimension; an N=4 on-shell or amplituhedron
  form with poles on factorisation channels.
- **FAIL (only combinatorial):** face posets differ from every associahedron of the same dimension, and the
  (candidate) form is a single dlog monomial in natural network coordinates, with poles where an effective
  conductance vanishes and no sum over channels.
- **INCONCLUSIVE:** the form cannot be determined at n = 3.
- Whatever the outcome, a proof that E_n is a positive geometry is out of scope. Ω₃ stays CONJECTURE unless all
  axioms are checked.

**(d) *Fusions* vs network cell.**
- Compare Fusions σ (Def. 2) of (i) the trace chain on the terminals and (ii) the full chain on all nodes with
  (iii) Lam's f_τ and (iv) the positroid cell of the terminal-column projection.
- Prediction (iv) = (i) for connected networks, and (i) ≠ (iii) in general (different ambient Gr; Fusions forgets τ).
- **PASS** = the prediction verified on the families (and in Lean for the Y network). **FAIL** = a counterexample.

## Not tested

Any physics of networks; "observer ↔ particles". All CONJECTURE/SPECULATION tags stay.
