# MVP-0 — the 2-plane is the massless boson

First checked piece of UOPG. The object is `Gr⁺(2,4)`. Spacetime enters as the Klein correspondence, not as a Hessian and not as a fitted scale.

Read [DICTIONARY.md](DICTIONARY.md) before the Lean files. Read [EMPIRICAL.md](EMPIRICAL.md) for the only experimental comparison. The root files `UOPG.lean` and `UOPGv2.lean` are earlier drafts and are not imported here.

## What is proved

Over any commutative ring:

- the Plücker relation on every `2 × 4` matrix
- the `GL(2)` weight `P(gC) = (det g) P(C)`, and `SL(2)` invariance
- one rational point with all six ordered minors positive

Over a field:

- Plücker bilinear of two affine events `= det(x − y)`
- that vanishes if and only if the two events share a direction
- four twistor events give four edge momenta with `det pᵢ = 0` and `Σ pᵢ = 0`

## Check

The proofs were checked with Lean `v4.34.1` and Mathlib `v4.34.1`. Exported theorems have no `sorry`. Their axioms are only `propext`, `Classical.choice`, and `Quot.sound`. `mvp0/check.sh` rebuilds, runs the witness, and prints the axiom list.

```bash
cd mvp0/lean
lake exe cache get
lake build
lake exe uopg0
cd ..
./check.sh
```

`lake exe uopg0` prints the six positive minors. It does not print a W mass.

## Layout

```
mvp0/lean/UOPG0/Basic.lean      definitions
mvp0/lean/UOPG0/Plucker.lean    relation and GL(2) weight
mvp0/lean/UOPG0/Positive.lean   rational witness
mvp0/lean/UOPG0/Klein.lean      null separation
mvp0/lean/UOPG0/Momenta.lean    four null, conserved edges
```

A separate comparator challenge file is not included. `leanprover/comparator` checks that a solution module discharges names declared in a challenge module; wiring that split on top of a development that already builds is a follow-up. The kernel check that this MVP actually runs is `lake build`, plus the axiom audit in `check.sh`.
