# SC-1 prereg — Regge slope → string tension: m_ρ/√σ = √π at large N (2026-10-15)
Pushed alone, before any target value is read. author approved. Source: notes/SCALE-SWEEP-2026-10-14.md §SC-1.

## Prior-art sweep
- σ = 1/(2πα′) is the classical Nambu–Goto open-string relation (textbook). The comparison "meson Regge slope vs lattice string tension" is long known in phenomenology, so the relation itself is **not new**. Our only addition is the chain from the credited LS/RG model (MassiveLS: chiral-limit α′ = 1/(2m_ρ²), `ap 0 = 1/2`) to a sharp number √π, compared with large-N lattice data.
- Sources (identified from arXiv meta tags only: title, authors, date): A = Bali, Bursa, Castagnini, Collins, … arXiv:1304.4437 "Mesons in large-N QCD" (2013). B = García Pérez, González-Arroyo, Okawa arXiv:2011.13061 "Meson spectrum in the large N limit" (2020; twisted reduction, no shared authors with A → independent). C = Del Debbio, Lucini, Patella, Pica 0712.3036: excluded (no √σ units; shares an author with A).

## Method-fitness gate
- Well-posed: both A and B give m_ρ in units of the Wilson-loop/static string tension √σ, in the large-N chiral limit, i.e. the same quenched/large-N setting as the LS model. ✔
- **Memory audit (CONTAMINATED):** I have a rough memory that large-N lattice m_ρ/√σ is "around 1.5–1.7", most likely from A. That is not exact, but it means the rung is **not blind**: cap ≤ 0.25, proposed credit 0.
- **Exposure so far:** a masked structure dump of the LaTeX sources (every digit replaced by '#') was used to find the table labels and row labels. A presence check printed only "cell numeric = True/False". No target digit has been seen.
- Fit for purpose: yes, as a non-blind consistency test (a gate check, not credit-bearing).

## Cells (exact; extracted only by the locked script)
- A: table `tab:largeNsummary`, row label `$\rho$`, column index 2 (header "$m_q = 0$" under ${m_\infty}/{\sqrt{\sigma}}$, chiral limit, N = ∞). Error = statistical (quadrature of the parentheses) ⊕ the caption's stated percentage systematic (continuum).
- B: table `t:finaltable`, row label `$\frac{m_X^{(0)}}{\sqrt{\sigma}}$`, column index 1 (header $\rho$). Error = statistical ⊕ max(asymmetric systematic).
- Both were checked to be numeric before this prereg (presence mode).

## Prediction, rivals, null, constant basis
- Prediction (no tuning, no free parameter): m_ρ/√σ = √π ≈ 1.7725.
- Strong rivals (equally principled slope conventions): R1 = √(2π) (α′ = 1/m_ρ², intercept 0); R2 = √(π/2) (closed-string slope α′/2).
- Fixed constant basis: B = {√((p/q)·π^k) : 1 ≤ p, q ≤ 6, k ∈ {0,1,2}} ∩ [1,3] (n = 39). Null rate = fraction of B at least as close to the measured value as √π (look-elsewhere).
- Tolerance per source: max(3σ_tot, 5% of √π).

## Verdicts (exhaustive)
- PASS: both A and B within tolerance of √π, √π closer than both rivals for each, and null rate ≤ 0.2 for each.
- PARTIAL: at least one source within tolerance, but the PASS conditions are not all met.
- FAIL: neither source within tolerance ⇒ the LS-slope → σ chain does not give the large-N ρ mass.
- Otherwise (extraction reject/ambiguity) → UNCLASSIFIED.

## Locked checker + planted inputs (sha256, paths under sims/sc1/)
```
69c59df716cc5b9f3d3f7e8555216c2fbde4a226cd723289cf7d1da9d26eca0e  sc1_score.py
661f3f80a8211579102ab1a85d1800dee6f1dd2222e5b358db3bf272737ed88d  planted/good/1304.4437/a.tex
2f1b19bf02ea8ecbe6b049ec6422824c730a5162833c2305401412e5190c8812  planted/good/2011.13061/b.tex
02b2439bda0bc50a6060071fb5576c8b154aaca4acc868a763b47e778758e852  planted/broken/1304.4437/a.tex
2f1b19bf02ea8ecbe6b049ec6422824c730a5162833c2305401412e5190c8812  planted/broken/2011.13061/b.tex
```
Planted test (run after this push, before live): planted/good (synthetic tables with √π-like values in both exact formats) must give PASS with recovered values; planted/broken (duplicated ρ row) must be REJECTED. Either failing ⇒ STOP.

## Lean plan
Theorem: with MassiveLS's chiral-limit slope `ap 0 = 1/2` (m_ρ = 1) and σ := 1/(2π·α′), m_ρ²/σ = π and m_ρ/√σ = √π. This is a genuine edge to MassiveLS (and the KSRF π-gap). Pure algebra, PROVED only if 0 sorry and AxiomsAll is clean.
**Proposed credit:** 0 (non-blind; classic relation).
