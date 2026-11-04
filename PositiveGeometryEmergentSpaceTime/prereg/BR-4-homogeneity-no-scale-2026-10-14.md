# BR-4 prereg — one "degree-0 homogeneity ⇒ no scale" lemma, instantiated three times (2026-10-14)
Prior art: Buckingham π theorem (1914); our ScaleNoGo (OP-2), SG1.eigen_scale, ScaleNoGo.LS_scale. Nothing new physically.
Claim: a general Lean lemma: if f : X → Y is invariant under x ↦ c•x for all c ≠ 0 (ScaleBlind) and σ : X → K is
homogeneous of degree k (σ(c•x) = c^k σ(x)) with σ x ≠ 0, then for any c with c^k ≠ 1, f(c•x) = f x but σ(c•x) ≠ σ x
(f cannot determine the scale σ). Instances (as Lean theorems, existing statements unchanged):
 (I1) stabiliser data (ScaleNoGo.stabilizer_smul_eq), (I2) PF eigen-data predicate (SG1.eigen_scale direction + converse),
 (I3) LS amplitude as a function of (s,u,m²).
Plus a non-vacuity witness and a "what MG4 must break" corollary: any f that does fix σ is not ScaleBlind.
Verdicts (exhaustive): PASS = lemma + all 3 instances + witness proved, checklist passes, alignment ALIGNED;
PARTIAL = lemma + ≥1 instance; FAIL = lemma not provable as stated; otherwise UNCLASSIFIED.
Unit: none. Credit: 0 (structural). Memory audit: n/a (no data).
