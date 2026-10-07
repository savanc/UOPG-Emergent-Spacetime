# Lemma — a null edge is an outer product

Not an MVP. The ladder does not gain a green rung here.

`det m = 0` if and only if `m = u vᵀ`. For `t ≠ 0`, sending `u` to `t u` and `v` to `v / t` does not change `m`. On the rational polygon from MVP-0, the four edges are the factors in the shadow, and `t = 2` is the rescaling drawn on the MVP-4 card.

That card stays amber. The lemma is the linear algebra under the picture. A helicity would be a weight on a wavefunction, and there is no wavefunction here. MVP-3 is untouched: no ratio, no GeV.

Read [DICTIONARY.md](DICTIONARY.md). The proofs are `mvp0/lean/UOPG0/RankOne.lean`.

```bash
cd mvp0/lean
lake build rankone
lake exe rankone
cd ../..
./lemma/check.sh
```

`lake exe rankone` prints the four factors and that the rescaling agrees. It does not print a helicity or a mass.
