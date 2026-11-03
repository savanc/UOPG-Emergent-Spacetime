# BR-6 prereg — Spinor (massless) ↔ MassiveSpinor bridge (2026-10-14), pushed alone before any Lean
Source of candidate: graph/analysis.json bridge_candidates (top score 13.0: Spinor cluster ↔ MassiveSpinor).
Claim to formalise (classical): for a 2×2 complex momentum matrix p, det p = 0 (massless) ⇔ p has rank ≤ 1 ⇔ p = λ λ̃ᵀ
(a single spinor pair), the m → 0 counterpart of MassiveSpinor's rank-2 decomposition; and massive p (det ≠ 0) is never
of the single-pair form. Lean will reuse existing Spinor / MassiveSpinor statements where their types match; if the
massless rank-1 decomposition already exists in Spinor, the bridge is the statement "det = 0 ⇔ not massive" linking them.
Verdicts (exhaustive): PASS = Lean theorem(s) importing both modules and using ≥1 lemma from each, plus witness,
checklist + alignment ALIGNED; PARTIAL = statement proved but uses only one module; FAIL = types prevent a joint
statement; otherwise UNCLASSIFIED. Credit 0 (classical).
