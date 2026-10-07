# MVP atlas

One object: the positive Grassmannian `Gr⁺(2,4)`. Spacetime is the Klein correspondence of that object. Particles, if they come out at all, come out of the same field. A rung below is green only when Lean has checked it. An amber rung is the job, not a result.

![The five rungs. Green is proved. Amber is a contract.](figures/mvp-ladder.png)

Regenerate every picture, and recompute the rational numbers on them, with

```bash
python3 mvp0/viz/geometry.py --write   # rewrite docs/figures
python3 mvp0/viz/geometry.py --check   # identities only; fails if shadow.txt is stale
```

The arithmetic is exact (`fractions.Fraction`). There is no Monte Carlo and no fitted scale. `docs/figures/shadow.txt` is the numerical record. If an identity fails, the script does not draw.

The old notebooks simulated a Hessian, a column update, and a calibration to a W mass. Those are not redrawn here. They are not simulations of the proved object.

## MVP-0 — proved

The 2-plane is the massless boson. Theorems and the line they do not cross are in [mvp0/DICTIONARY.md](../mvp0/DICTIONARY.md). The only experiment is [mvp0/EMPIRICAL.md](../mvp0/EMPIRICAL.md): the mass defined by `det` is 0, compared with the PDG photon bound, not fitted to it.

![One witness, three pictures: the plane, its Plücker coordinates, the affine event.](figures/mvp0-klein.png)

![Four twistor events. Every edge has det = 0 and the edges sum to 0.](figures/mvp0-polygon.png)

![Six positive minors, and the same plane in the orthant chart.](figures/mvp0-positive.png)

![GL(2) multiplies every minor by det g. SL(2) fixes them. Thirty-six plus one hundred fifty-four exact samples.](figures/mvp0-gl2.png)

The polygon is not a sketch that was then checked. `regionMatrix` in [mvp0/viz/geometry.py](../mvp0/viz/geometry.py) is the same formula as `UOPG0.regionMatrix`. The four events, the six minors, and the GL(2) ensemble are computed, then the picture is drawn. The light-cone labels `u = t+x`, `v = t−x` are a reading of those diagonal matrices, so that `det = t² − x²`. They are not an extra assumption.

## MVP-1 — contract

![The positive chamber as an orthant, and the Parke–Taylor factor it has not yet been identified with.](figures/mvp1-canonical.png)

In the gauge used on the witness, the positive chamber is the orthant `x, y, z, w > 0`. The canonical form of an orthant is the dlog form. That is the easy half. The milestone is the change of coordinates that identifies it with the 4-point Parke–Taylor factor, as in Arkani-Hamed–Bourjaily–Cachazo–Goncharov–Postnikov–Trnka (arXiv:1212.5605) and Arkani-Hamed–Bai–Lam (arXiv:1703.04541). N=4 super Yang–Mills is the method to copy, not the target. No residue has been computed in Lean.

## MVP-2 — contract

![The Plücker exchange, which stays positive, against the column shift, which walks onto a wall.](figures/mvp2-cluster.png)

The identity `<13><24> = <12><34> + <14><23>` is `plucker_relation`, rearranged. On `Gr(2,4)` that exchange is the A₁ mutation; the four adjacent brackets are frozen. The column update in the 2026 drafts is a different map. At the Lean witness and `λ = 1` it sends `P23` from 1 to 0: still on the quadric, no longer in the chamber. That is one rational illustration, not a theorem about every shift.

Locality — that the poles of the canonical form are exactly those walls, the factorisation channels — is the milestone. It is not claimed.

## MVP-3 — contract

![A GeV may enter only as one named external mass. The ratio R is blank.](figures/mvp3-scale.png)

`Gr⁺(2,4)` is conformal. It does not contain a GeV. The only contract that can produce a mass is: one measured mass, declared before the comparison, and a dimensionless ratio R that a proof computes with no remaining freedom. R is not in this repository. A regulator, a Planck suppression, or a second measured mass ends the milestone. Nothing on this page is a prediction of an electroweak mass.

## MVP-4 — contract

![A null edge factors as a pair of spinors. Helicity would be the little-group weight. The weight is unknown.](figures/mvp4-helicity.png)

`det p = 0` is proved, and so is the existence of a kernel vector. Rank at most one means the matrix is an outer product `u vᵀ`; the script exhibits that factor for the four edges and checks that `u → t u`, `v → v/t` leaves `p` fixed. That rescaling is ordinary linear algebra on a proved null matrix. It is not yet a Lean theorem, and it is not a helicity. A massless boson would be a weight the geometry forces. MVP-4 has to derive the weight.

## What is not in the atlas

- a Hessian of `Σ log|det|`, or that scalar as a metric
- the λ column update, promoted to a mutation
- a W, Z, or Higgs mass, or `sin²θ_W`
- a GeV produced by the geometry
- a cross section, a wave equation, or a Monte Carlo calibration
