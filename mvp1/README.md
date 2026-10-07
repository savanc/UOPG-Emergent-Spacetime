# MVP-1 — the orthant coefficient

Second checked piece of UOPG. The object is still `Gr⁺(2,4)`. MVP-0 said a positive 2-plane is a point of the positive chamber. This rung says what that chamber looks like in one gauge, and what rational function sits on it.

The Lake project is the one in [mvp0/lean](../mvp0/lean). MVP-1 is `UOPG0/Canonical.lean` and the executable `uopg1`. One toolchain, one Mathlib cache.

Read [DICTIONARY.md](DICTIONARY.md) before the Lean file. Pictures are in [docs/ROADMAP.md](../docs/ROADMAP.md).

## What is proved

Over a commutative ring, for the chart

```
| 1   y   0  −w |
| 0   x   1   z |
```

- the ordered adjacent product is `x y z w`
- `⟨4 1⟩ = −P₀₃`, so the cyclic product is `−(x y z w)`
- left `GL(2)` multiplies the adjacent product by `(det g)⁴`
- the Plücker relation solves the remaining minor `P₁₃`

Over a field, when `P₀₂ ≠ 0`:

- there is a unique left `GL(2)` element sending columns 0 and 2 to the identity
- that element lands on the chart whose coordinates are the adjacent minors divided by `P₀₂`
- the orthant coefficient `1/(x y z w)` equals `1` over the adjacent product
- the Parke–Taylor coefficient is `1` over the cyclic product, hence minus the orthant coefficient
- if `x y z w ≠ 0`, the product of the four coordinates with the orthant coefficient is `1`

Over a linear ordered field, positive adjacent minors (including `P₀₂`) make the four chart coordinates positive, and the chart matrix itself has all six ordered minors positive.

On the MVP-0 witness the chart is `(1/2, 1/2, 3/2, 1/2)`. The orthant coefficient is `16/3`. The Parke–Taylor coefficient is `−16/3`.

## What this is not

Not a differential form. Not a helicity weight. Not a momentum-conserving delta. Not a cross section. Not a theorem that the canonical form of a general positive geometry is unique. N=4 super Yang–Mills is the method that was copied for this rational function, not the target. Nothing here is a mass.

## Check

```bash
cd mvp1
./check.sh
```

`lake exe uopg1`, run from `mvp0/lean`, prints the four coordinates and the two coefficients. It does not print a W mass.
