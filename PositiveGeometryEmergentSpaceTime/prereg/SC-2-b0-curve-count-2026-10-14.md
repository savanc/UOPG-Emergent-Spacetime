# SC-2 prereg — is b₀ of φ³₆ a pure curve count? (2026-10-14)
Pushed alone, before any sympy/Lean for this rung. Source: notes/SCALE-SWEEP-2026-10-14.md §2.

**Scope (fixed):** single real scalar, L = ½(∂φ)² + (g/3!)φ³, D = 6−2ε, MS, one loop, massless. The one-loop UV-divergent "curves" (diagram types on the one-loop surface) are exactly: triangle (vertex) and bubble (self-energy p² log). Colour-ordered Tr φ³ is out of scope (colour normalisation would add a free choice); reopen as SC-2b if PASS/PARTIAL.

**Target cells (all computed by the locked script, no external data opened):** (C1) b in β = b·g³/(4π)³; (C2) per-curve pole weights w_T, w_S and symmetry factors; (C3) flag universal_weight.
**Reference cell (CITED, remembered → capped ≤0.25):** Srednicki QFT ch. 28: β(g) = −3g³/(4(4π)³), i.e. b_ref = −3/4 (a number; checked present in memory/text, not looked up now).

**Fixed constant basis:** rationals p/q with |p|,|q| ≤ 100, times the fixed loop factor (4π)^{−3}. No π, ζ, √ beyond that. A match outside the basis does not count.

**Locked checker:** `0884314014f2244300792d886d25fe0cc696a9f13a28b2399142880776618a5d  sims/sc2/sc2_uvcount.py`. Not to be edited during the rung.

**Planted-answer test (must run before live mode; results → sims/sc2/sc2_planted.txt):** planted: φ⁴ in D=4 must give b = 3 (β = 3λ²/(4π)² = 3λ²/16π²); broken: φ³ in D=5 must be REJECTED (no pole). Either failing ⇒ STOP.

**Verdicts (exhaustive):**
- PASS: C1 = −3/4 AND universal_weight = True (b₀ = single universal weight × signed curve count).
- PARTIAL: C1 = −3/4 but universal_weight = False (b₀ is a weighted count with ≥2 distinct rational per-type weights in the basis).
- FAIL: C1 ≠ −3/4 (any rational mismatch) ⇒ NO-GO for "b₀ is a count" in this formalism.
- Otherwise (script error, value outside basis, planted test fails) → UNCLASSIFIED (report closest category and why).

**Lean plan:** finite model (curve types, counts, weights as ℚ); prove b = −3/4 from the weights and prove the weights are not universal (or are); non-vacuity witness. Pole weights from sympy are tagged SIMULATED unless formalised.
**Proposed credit:** 0 (consistency, remembered reference).
