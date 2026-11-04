# H-T5g pre-registration: n = 10 tile-form normalisation audit, then the vertex-chain loop factor (2026-10-12)

Written and pushed before computing. Environment: `<local path>` + `requirements-lock.txt` (unchanged); RAM about
2–3 GB free; 8 CPUs. The gauge convention is G2 as before.

## Prior art and re-read gap disclosure

- **HWX 1402.1479:** the loop factor J for the ABJM measure in OG/Ising variables. Our H-T3b rule C1 is HWX's rule in
  Ising variables.
- **Lee 2010; Huang–Wen 2014:** the measure.
- **Perlstein–Tessler 2501.07576:** BCFW cells = trees.

**Already seen:** H-T5f's post-hoc n = 8 identity (the residue form equals 8 · carrier · J_C1, with the
shared-corner sech omitted) and its n = 10 mismatch (spread 0.52). We have **not** re-read HWX §2.4 for chains yet;
that is Stage 2, after Stage 1.

## Stage 1: normalisation audit (gate)

**Route A — no fiber, no Y-chart.** The tile measure is pulled back to tree coordinates directly. For each tree tile
T, take a **top** network N ⊃ T (T plus 3 extra edges at n = 10, 1 extra edge at n = 8; found by search, with 10 resp.
6 crossings).
- The Lee measure in N's Ising chart is ω_N(J) = ρ_H(m(J)) · |det ∂m/∂J| / Π_{i=1..k} M_i(C′) (Haar on O(k) in gauge
  G2).
- The tile measure is the iterated residue at J_extra → 0, i.e. lim (Π_extra J_e) · ω_N with the extra J_e = ε.
- Hence J_A(J_tree) = lim(Π_extra J_e · ω_N) / Π_tree 2 coth 2J_e.
- This uses no fiber, no det(VᵀV), no Φ, and no Grothendieck formula.

**Route B — same quantity, more precision.** Every derivative is a central difference at mp.dps = 80 with
h = 10⁻³⁵ (truncation ~10⁻⁷⁰, rounding ~10⁻⁴⁵), giving ≥ 30 reliable digits. Each value is cross-checked against
h = 10⁻²⁵: they must agree to ≥ 20 digits. The extra-edge limit uses ε = 10⁻²⁵ and 10⁻³⁰ and must agree to ≥ 20
digits.

**Route C — same code at n = 8.** Route A at n = 8 must reproduce H-T5f's residue ratio (J_A ∝ R_res with the same
constant across both trees) and the post-hoc J_C1 identity.

**Criteria:**
- **Normalisation verified:** R_res(H-T5f route) / (carrier · J_A) is the same constant to ≥ 15 digits at 4 points
  on each of the 5 n = 10 trees, *and* the analogous constant at n = 8 is consistent (both trees).
  In that case the n = 10 mismatch is a real J effect and Stage 2 proceeds.
- **Normalisation wrong:** the ratio varies. Then J_A (route A) replaces the H-T5f residue at n = 10, and we report
  whether the n = 8 rule (C1, shared-corner sech omitted) fits J_A at n = 10. **That test is not blind**, since we
  know the rule.
- **INCONCLUSIVE:** routes disagree with each other (route A for two different N, or h/ε checks fail).

Route A also gives the Stage 2 target directly: J_tile(J) = J_A / constant.

## Stage 2 (only if needed after Stage 1)

Re-read HWX §2.4 for vertex chains and shared corners. Then pre-register one vertex-chain J rule plus one alternative
in a **prereg amendment, committed before evaluating at n = 10**.
- **PASS:** ratio constant to ≥ 20 digits across 5 trees × ≥ 6 points, with a universal 2⁻ᵏ-type constant.
- **FAIL:** otherwise.

Lean: the n = 8 identity symbolically, only if cheap.

## Fitness self-review

- **Methods:** derivatives are high-precision finite differences with stated error budgets (not interval-certified),
  so all results are tagged [SIMULATED, ≥ 20 digits].
- **Route independence:** A shares only ρ_H and Π M with the H-T5f residue, i.e. the definition of the measure.
- **Process and infrastructure:** cheap (minutes).

---
## Amendment S2 (written after Stage 1, BEFORE any Stage-2 evaluation at n = 10)

### Stage-1 outcome (see the review)

The H-T5f residue normalisation is **verified**. R_res / J_A = 1 with:
- spread 6 · 10⁻²¹ at n = 10 (5 trees × 4 points);
- spread 4 · 10⁻²² at n = 8.

The n = 10 mismatch is therefore real, and Stage 2 proceeds.

### HWX §2.4.2 re-read (eqs. 2.23–2.33)

J = 1 + J1 + J2 + J3 + J13 + J23. In this formula:
- **J1** sums over disjoint sets of closed medial loops;
- **J2** covers loops sharing a single medial vertex, as the product of the loops' factors *except* the shared vertex;
- **J3** covers loops sharing two vertices.

In Ising language:
- a medial vertex is an Ising edge e, with factor sech 2J_e (as fitted at n = 8);
- each internal Ising vertex x gives a closed medial loop L_x = Π_{e∋x} sech 2J_e;
- two internal vertices joined by an edge give loops that share exactly that one medial vertex;
- a tree has no bounded Ising faces, so J3 = J13 = J23 = 0.

### New disclosure (gap)

The H-T5f n = 10 "omit" test mixed in H-T5d's *non-tree* network R1b (a star with two triangles, which has
bounded faces and so J3-type loops). It did not use the tree T5 of the Catalan list. Per-tile spreads at n = 10
have **not** been looked at.

### Rule V: vertex-chain (primary)

J_V = Σ_{S ⊆ internal vertices} Π_{e : |e ∩ S| = 1} sech 2J_e.

Every set S is included, connected or not. Edges with both ends in S (the shared corners of a chain) are omitted,
which is HWX J2 extended to chains of any length. This equals H-T5f "omit" applied to genuine trees.

### Rule P: pairwise only (alternative)

The same, but connected subsets of more than 2 vertices (here only the chain {u, v, w}) contribute 0. This is the
literal "pairs sharing a single vertex".

### Test

- **Points:** the 5 trees T1–T5 (T5 = Catalan tree ((45)(12))3 via tree5(5), not R1b) × 8 points each.
- **Measurement:** the verified residue route, at dps 60 with h = 10⁻²⁵ (≥ 20 digits).
- **PASS:** R / J_rule is constant to ≥ 20 digits (spread < 10⁻²⁰) over all 40 points. The constant must be a
  power of 2; the prediction is 2^{k−1} = 16, following n = 8's 8 = 2^{k−1}.
- **PARTIAL:** constant per tile but not universal.
- **FAIL:** otherwise.
- **Diagnostic only:** both rules are also reported on R1b, the non-tree network.
