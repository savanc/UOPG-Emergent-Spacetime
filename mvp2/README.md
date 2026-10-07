# MVP-2 — the orthant factors onto a face

`Gr⁺(2,4)` in the MVP-1 gauge is the orthant `x, y, z, w > 0`. The coefficient is `1/(x y z w)`. This rung says where that denominator vanishes, and what remains after one coordinate is cancelled.

Read [DICTIONARY.md](DICTIONARY.md) before the Lean file. The picture is in [docs/ROADMAP.md](../docs/ROADMAP.md).

## What is proved

Over a field:

- `x y z w = 0` if and only if one of those four is zero
- those four are the ordered adjacent minors `P01`, `P12`, `P03`, `P23`
- if none is zero, `x / (x y z w) = 1/(y z w)`, and the same for `y`, `z`, and `w`
- at `(1, 1, -1, 1)`, which is outside the chamber, `P13 = 0` while the product is `-1`

Over an ordered field:

- on each codimension-1 face, one coordinate is at least zero and the other three are positive, and `P13 = y z + x w` stays positive

At the witness chart `(1/2, 1/2, 3/2, 1/2)`:

- dropping `x`, `y`, or `w` gives `8/3`; dropping `z` gives `8`
- the face `x = 0` has `P13 = 3/4`
- the column update with `λ = 1` sends `P23` from 1 to 0 and stays on the quadric

## What is not proved

A de Rham residue, a factorization of an amplitude, a cross section, a general cluster mutation, or a mass. `8/3` and `8` are not GeV. `Gr⁺(2,4)` still does not contain a gluon, a W, a Z, or a fermion.

## Check

```bash
cd mvp2
./check.sh
```

The Lake project is `mvp0/lean`. `lake exe uopg2` prints the face numbers. It does not print a W mass.
