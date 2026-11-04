# PREREG STRUCT-3 / R3 — N_gen from consistency or a discrete geometric invariant
Written 2026-10-15. Pushed ALONE, together with its locked checker and planted pair, before the live run.

**SM ledger line moved:** N_gen (number of generations). EV 0.038 (see the log ranking).

**Prior art / well-posedness.**
- QCD asymptotic freedom needs n_f ≤ 16 (Gross–Wilczek, Politzer 1973), i.e. N_gen ≤ 8.
- SU(2) one-loop b₀ = 19/6 in the SM.
- Kobayashi–Maskawa (1973): (N−1)(N−2)/2 physical CP phases, so CP violation needs N_gen ≥ 3. This is CITED, and it needs observed CP violation as an *empirical structural input*. That is not a hadron gate and has no numeric fit.
- χ(Gr≥0(k,n)) = 1 (Galashin–Karp–Lam, arXiv:1707.02010: closed ball).
- Per-generation anomaly cancellation is additive, so ACC and Witten are blind to N_gen. Well-posed as: which N_gen survive the consistency stack, and does any fixed-family invariant of a trunk positive geometry *force* 3?

**Claims.**
- G1: the total anomaly of N_gen copies = N_gen × the one-generation anomaly. So the ACC hold for every N_gen, and so does Witten for odd N_c.
- G2: AF(SU(3)) ⇔ N_gen ≤ 8; AF(SU(2), one Higgs doublet) ⇔ N_gen ≤ 5.
- G3: KM phase count > 0 ⇔ N_gen ≥ 3.
- G4: window AF ∧ KM = {3, 4, 5}; 3 and 4 both pass, so N_gen = 3 is not selected.
- G5: none of the fixed invariant families in the checker (χ(Gr≥0), Catalan vertex count, facet count n(n−3)/2, positroid cells of Gr≥0(1,n) = 2ⁿ−1, dim Gr(k,n), helicity-sector count) is constantly 3. Values of 3 occur only at tuned parameters. In Lean: 2ⁿ − 1 = 3 ⇔ n = 2, and Catalan never equals 3.

**Verdict rules.**
- G1–G5 ⇒ **NO-GO-FOR-N_gen=3** (exclusion PASS), recording "N_gen ∈ {3,4,5} given AF+KM".
- A forced invariant = 3 ⇒ **SELECTS-3**.
- Window = {3} ⇒ **SELECTS-3 (consistency)**.
- Otherwise UNCLASSIFIED.
- A geometry→STRUCT LINK requires a geometry-module theorem implying an N_gen statement. A tuned-parameter hit does not count.

**Fixed basis.** Integers and rationals with |p|,|q| ≤ 50. The b₀ coefficients are CITED group theory (11/3, 2/3, 1/3). No fitted constants.

**Planted pair.** sims/struct3/struct3_planted.txt. Planted (N_gen ≤ 8, b_su2(3) = 19/6, km(3) = 1, km(2) = 0) recovered: exit 0. Broken (sign-flipped gauge term) rejected: exit 1. The first planted attempt caught a Higgs-coefficient error (1/12), which I fixed before locking.

**Locked checker.** `sims/struct3/struct3_ngen.py` sha256 `98bc1b1f7d91570edc579a8dc35808418f9d8355b476865e41a2112c8ec45db4` (committed in this prereg commit).
