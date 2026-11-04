# SC-2b prereg — are SC-2's weights canonical cell volumes in the 2309.15913 curve-integral fan? (2026-10-15)
Pushed alone, before any sympy/Lean for this rung. author approved.

**Source (read-only, theory, no data cells):** Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas, arXiv 2309.15913.
**Disclosure:** the abs-page fetch at returned the full introduction and §§2–6, including eq. 22 (cone measure = |⟨g…⟩|, all cones unimodular) and eq. 101 (planar bubble g-vectors). So the I1 outcome is partly anticipated; this is a structure check, not blind.

**What "matching cell volume" means (fixed now, three candidates):**
- I1: cone Jacobian |det(g_{C1}…g_{CE})| of the diagram's top cone (eq. 22 measure).
- I2: Lebesgue volume of the projective slice {ρ ≥ 0, Σρ = 1} of that cone in ρ-coordinates (ρ_1…ρ_{E−1}) = 1/(E−1)!.
- I3 (not a volume, control): bubble F/U moment ∫₀¹ x(1−x) dx.
Cones: bubble = {S1, S2}, g = (0,−1), (−1,0) (eq. 101); triangle = triangulation T, g = e₁, e₂, e₃ (eq. 78).
**Compared quantities (SC-2 geometric factors, Γ-residues and symmetry factors stripped):** triangle 1/2 (simplex area), bubble 1/6 (∫x(1−x)). These are what SC-2's weights 1/2 and 1/12 reduce to once dimension-dependent Γ factors (1/Γ(3)·2!, Γ(−1+ε) residue) and the bubble symmetry factor 1/2 are removed.

**Fixed constant basis:** rationals p/q, |p|,|q| ≤ 100. Nothing else.
**Locked checker:** `2a20bef910ff148e7406cce9ab78436bd2749dfa7fb1f676c6d1617ea5d27d3e  sims/sc2b/sc2b_cells.py`
**Planted-answer test:** planted = 2309.15913 eq. 81 five-point tree fan, all five cones must come out unimodular; broken = cone {(1,0),(1,2)} must be REJECTED (|det| = 2). Either failing ⇒ STOP. Log → sims/sc2b/sc2b_planted.txt.

**Verdicts (exhaustive):**
- PASS: both factors equal a pure cell volume (I1 or I2) of the matching cone.
- PARTIAL: exactly one does (the other needs a non-volume insertion such as I3).
- FAIL: neither does.
- Otherwise (checker error, value outside basis, planted test fails, cone identification not expressible) → UNCLASSIFIED (closest category and why).

**Lean plan (real proofs, no simulated inputs for the identities):** Matrix.det of both cones; MeasureTheory.volume of the 2-simplex slice (regionBetween) = 1/2 and of the 1-simplex slice = 1; reuse SC2.bubble_param_integral for I3; link to SC2 (and to the Associahedron chain only if a genuine statement connects them, otherwise reported as unlinked). Non-vacuity witnesses.
**Proposed credit:** 0.
