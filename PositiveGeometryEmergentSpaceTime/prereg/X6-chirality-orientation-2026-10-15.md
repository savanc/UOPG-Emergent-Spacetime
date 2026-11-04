# PREREG X6 / XD-6 / R2 — chirality_orientation lemma
Written 2026-10-15. Pushed ALONE before any live run or Lean result.

**Question.** Does the orientation / sign structure of positive geometry (Gr₊, positroids, amplituhedron) force a chiral rather than a vector-like fermion spectrum, and does it constrain the hypercharges or N_c?

**SM ledger line moved:** "hypercharges / chiral content" (structural, BIG-PICTURE §3), with a secondary effect on "gauge group / colour number" through STRUCT-2.
**EV (calibrated):** P_naive 0.3 → P_used 0.09; V 0.3; EV = 0.027.

**Prior art / well-posedness.**
- Galashin–Lam, *Parity duality for the amplituhedron*, arXiv:1805.00600 (Compositio 2020). The twist map gives Gr₊(k,n) ≅ Gr₊(n−k,n) (orthogonal complement with alternating column signs) and preserves canonical forms up to sign. Physically this is parity (k ↔ n−k, i.e. λ ↔ λ̃).
- The positive Grassmannian is also invariant under cyclic shift and reflection.
- Expectation: positivity is parity-symmetric, so it cannot be the source of chirality. Well-posed as: (i) is the Gr₊ structure invariant under the parity and reflection maps; (ii) what does chirality, as an input, buy the STRUCT anomaly island.

**Claims (pre-stated).**
- C1: the twisted complement map sends Gr₊(k,n) to Gr₊(n−k,n). Checked numerically for (k,n) ∈ {(1,3),(1,4),(2,4),(2,5),(3,6),(2,6),(3,7)}; proved in Lean for Gr(2,4) Plücker data, where the map is p_I ↦ p_{Iᶜ}, preserving positivity and the Plücker relation (an involution).
- C2: the reflection i ↦ n+1−i preserves Gr₊ (projectively). Same cases; proved in Lean for Gr(2,4).
- C3: a vector-like spectrum (charges in ± pairs with equal multiplicity) satisfies the linear and cubic ACC sums identically. Proved in Lean for arbitrary finite families.
- C4: the one-generation ACC branch with y_Q = 1 (STRUCT-2) is vector-like iff N_c = 1, over the integers 1–9 (checker). In Lean: for every N_c ∉ {0, 1, −1/2}, the charge −1 is absent (Q unpaired), so the spectrum is chiral; at N_c = 1 the multiset is closed under negation.

**Verdict rules.**
- C1 ∧ C2 hold ⇒ **NO-GO** for "positivity orientation forces chirality". Exclusion PASS, removing positive-geometry orientation as the source of chiral content.
- Additionally C3 ∧ C4 ⇒ **LINK-LEMMA**: chirality is an independent input that makes the ACC non-vacuous; combined with Witten it gives N_c odd and ≥ 3, which still does not select 3.
- If C1 or C2 fails, then **CANDIDATE** (orientation distinguishes parity); escalate.
- Anything else is UNCLASSIFIED.
- Geometry→STRUCT edge counts as LINK only if a Lean theorem in a geometry module implies an ACC statement. Otherwise NO-LINK.

**Fixed basis.** Integers and rationals with |p|,|q| ≤ 20. No fitted constants. No hadron gates, no cited numerical inputs.

**Planted pair.** sims/x6/x6_planted.txt. Planted (twisted map, reflection, vector-like sums, N_c=1) recovered: exit 0. Broken (untwisted complement) rejected: exit 1.

**Locked checker.** `sims/x6/x6_orientation.py` sha256 `360e3a285264c06f8163eedc2172b425930baacd124e6f05d69e7e90caf15cb5`.

**Glossary.** Every new Lean identifier uses canonical ids (`chirality_orientation`, `N_c`, `yQ`…), with aliases in docstrings, and is added to scripts/lean_glossary.py.
