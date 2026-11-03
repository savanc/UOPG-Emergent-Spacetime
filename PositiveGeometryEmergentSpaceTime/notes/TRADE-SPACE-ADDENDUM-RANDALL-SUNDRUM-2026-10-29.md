# Trade-space addendum: Randall–Sundrum warped extra dimension (2026-10-29)

*Written 2026-10-29 by Grok. Docs only. No prereg, no rung, no locked checker ran, no Lean build, no web fetch.*
*Source of the request: The author (RS analysis) and (2026-10-29): "Yes add them".*

This note **adds** to notes/TRADE-SPACE-2026-10-28.md, notes/TRADE-SPACE-EXPANSION-2026-10-28.md and
notes/TRADE-SPACE-ADDENDUM-PILOT-WAVE-2026-10-28.md. It edits none of them; nothing is superseded. Base commit: origin/main 433cc73.

Tags: **PROVED**; **SIMULATED**; **CITED** (fetched, link below); **CONJECTURE**; **SPECULATION**; **DRAFT** (proposal text, *not* a prereg);
**BACKGROUND** (standard textbook content, not fetched this session; becomes CITED only after the papers are fetched).

## 0. Status and gating

| Node | Status | Gate |
|---|---|---|
| RS-1 WARP-LEDGER | PLANNED / PROPOSED, **NOT RUN**, DRAFT | The author's go; after CASCADE-1b r2 grade + push; usage permitting |
| RS-2 GEOM-KRC | PLANNED / PROPOSED, **NOT RUN**, SPECULATION | The author's go; only after RS-1 |

Each needs its own prereg, pushed alone with the guard refusing before the push, under MISSION frontier mode.
Nothing below is a prediction on record.

**Basin label.** No numbered basin (B1–B5 in TRADE-SPACE-2026-10-28; proposed B6–B10 in TRADE-SPACE-EXPANSION; B11 in the
pilot-wave addendum) is an emergent-spacetime basin. The existing emergent-spacetime home is the trade-space figure's
**ST "Spacetime layer"** (M1 Minkowski from Hermitian 2×2; M1b real-positivity NO-GO). RS-1/RS-2 are placed there.
**No new basin is created**; promoting ST to a numbered basin is the author's call.

## 1. Context [BACKGROUND, not fetched; TODO-cite]

- RS1 (Randall & Sundrum 1999) [TODO-cite]: a slice of AdS5 between two 3-branes. The warp factor exp(−k·π·r_c) maps the
  Planck scale to the weak scale on the visible ("IR"/TeV) brane: M_weak ≈ M_Pl · exp(−k·π·r_c).
- Getting ~10^16 needs k·r_c ≈ 11–12 [BACKGROUND, by hand: ln(10^16)/π ≈ 11.7].
- Goldberger–Wise stabilisation [TODO-cite] makes k·r_c ~ 11–12 natural from O(1)–O(10) bulk inputs; it is still an input.
- RS2 (Randall & Sundrum 1999, second paper) [TODO-cite] is the single-brane variant (localised gravity, infinite extra dimension); it does not address the hierarchy the same way.
- RS1 predicts Kaluza–Klein gravitons; none seen at the LHC. Current exclusion masses: [TODO-cite, exact ATLAS/CMS bounds not fetched].

## 2. Assessment [CONJECTURE]

Under the zero-fitted-parameter and anti-numerology rules, RS **relocates** the hierarchy into one declared input, k·r_c,
rather than predicting it. Turning a 10^16 mystery into an O(10) number is real progress in naturalness terms, but it scores
as one fitted input in our ledger. The milestone-relevant version is one where a geometric construction outputs k·r_c.

## 3. RS-1 WARP-LEDGER (PLANNED, NOT RUN, DRAFT)

- **What.** A Lean ledger card (proposed module `PositiveGeometryEmergentSpaceTime.RS1`) that formalises M_weak = M_Pl · exp(−k·π·r_c), with k·r_c as a
  declared FRONTIER-AXIOM-style hypothesis (input, not derived), and states the target "derive k·r_c geometrically" as an open item.
- **Proposed lemmas (DRAFT).** monotonicity of the warp in k·r_c; the inverse map k·r_c = ln(M_Pl/M_weak)/π; a statement that the
  ratio is free in the hypothesis (any positive ratio is reachable), so RS alone fixes nothing.
- **Outcome class.** Known-outcome / method card (no SM line predicted). Credit 0 by construction.
- **Basin.** ST Spacetime layer (see §0).

## 4. RS-2 GEOM-KRC (SPECULATION, PLANNED, NOT RUN)

- **Question.** Can a UOPG geometric invariant (e.g. from the Gr₊(2,4) / positive-geometry constructions) fix k·r_c with zero fitting?
- **Pre-stated refutation criterion.** FAIL if the construction needs a continuous free parameter tuned to 11–12, or a discrete
  choice selected post hoc from more than ~3 options.
- **Pre-stated success criterion.** k·r_c within 5% of the value implied by the target ratio, with zero fitted inputs, plus the
  usual anti-numerology test at p < 0.01 and planted-answer tests.
- **Prior.** Low [SPECULATION]. An O(10) number is easy to hit numerologically; the p < 0.01 gate is load-bearing here.

## 5. exclusion ledger

Placeholder row added to notes/EXCLUSION-LEDGER.md: `RS1.krc_declared_input` — hierarchy problem relocated, not solved, by RS (one input k·r_c).

## 6. Figure

RS-1 and RS-2 added as planned nodes in figures/trade-space-traffic-light.mmd under ST ; png re-rendered with mmdc (system Chrome, -w 3000 -s 2).
