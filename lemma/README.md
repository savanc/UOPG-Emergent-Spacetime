# Lemma — a null edge is an outer product

Not an MVP. The ladder does not gain a green rung here.

`det m = 0` if and only if `m = u vᵀ`. For `t ≠ 0`, sending `u` to `t u` and `v` to `v / t` does not change `m`. On the rational polygon from MVP-0, the four edges are the factors in the shadow, and `t = 2` is the rescaling drawn on the MVP-4 card.

That card stays amber, and the ladder is frozen. There is no further rung on `Gr⁺(2,4)`. For `t ≠ 1` the factor `u` moves, and every function of the momentum stays fixed, so the momentum does not determine `t`. On edge 0, `t = 2` sends `u` from `(−2, 0)` to `(−4, 0)` while `p` stays put. A helicity would be a weight in `t` on a function this geometry has not supplied. MVP-3 is untouched: no ratio, no GeV.

Read [DICTIONARY.md](DICTIONARY.md). The proofs are `mvp0/lean/UOPG0/RankOne.lean`.

```bash
cd mvp0/lean
lake build rankone
lake exe rankone
cd ../..
./lemma/check.sh
```

`lake exe rankone` prints the four factors, that the rescaling agrees, and that `t = 2` moves edge 0 from `(−2, 0)` to `(−4, 0)`. It does not print a helicity or a mass.
