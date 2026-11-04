# Trade-space addendum: AI-produced Yang–Mills / QCD / GUT existence claim (2026-10-29)

*Written 2026-10-29 by Grok. Docs only. No prereg, no rung, no locked checker ran, no Lean build. One web fetch (the post below).*
*Source of the request: The author (analysis) and (2026-10-29): "Yes add".*

This note **adds** to notes/TRADE-SPACE-2026-10-28.md, notes/TRADE-SPACE-EXPANSION-2026-10-28.md,
notes/TRADE-SPACE-ADDENDUM-PILOT-WAVE-2026-10-28.md and notes/TRADE-SPACE-ADDENDUM-RANDALL-SUNDRUM-2026-10-29.md.
It edits none of them; nothing is superseded. Base commit: origin/main b7ef3ee.

Tags: **PROVED**; **SIMULATED**; **CITED** (fetched, link below); **CONJECTURE**; **SPECULATION**; **DRAFT**; **BLOCKED**.

## 0. Status and gating

| Node | Status | Gate |
|---|---|---|
| YM-IMPORT | PLANNED, **NOT RUN**, **BLOCKED** (no public Lean artifacts) | Lean artifacts public; then the author's go; usage permitting |

Nothing below is a prediction on record. No basin is created.

## 1. Context [CITED: post fetched 2026-10-29; claims by the post, unreviewed]

Source: OpenAI, "Working with academic communities to build scientific understanding", dated October 26, 2026.
<https://openai.com/index/building-scientific-understanding-with-academic-communities/>

The post claims three model-produced results:

- **Local smoothing in all dimensions** (Sogge 1991), which implies the Kakeya and Stein restriction conjectures in all
  dimensions. Natural-language write-up and Lean proof public on OpenAI's GitHub.
- **The Exponential Time Hypothesis is false.** Write-up and Lean proof public. Shepherds: Impagliazzo, Paturi, Williams.
- **Rigorous existence of interacting 4D gauge theories with fermions**: pure Yang–Mills, QCD and "the simplest grand unified
  theory that includes the gauge fields and fermions of the Standard Model", building on Balaban's constructive approach.
  YM Lean formalisation reportedly finished 16 Oct 2026. **Nothing released**: a group led by David Gross (with Douglas, Jaffe,
  Klebanov, Nekrasov) controls release. The GUT's gauge group is not named in the post.

The post also sets four collaboration principles: Transparency, No Academic Credit, Recognition, Independence.

All of the above are claims by the post only, not independently verified.

## 2. Assessment [CONJECTURE]

**Existence is not determination.** A rigorous existence proof of YM / QCD / a GUT takes the gauge couplings, fermion
masses and mixings as inputs. The mission's zero-fitted-parameter milestone (predict dimensionless SM ratios with nothing
fitted) is untouched. What it could do is firm up foundations we currently assume informally (a well-defined interacting
gauge theory behind the unitarity, positivity and confinement-scale inputs of the Lovelace–Shapiro and lattice-facing rungs).

## 3. YM-IMPORT (PLANNED, NOT RUN, BLOCKED, gated on the author's go)

1. **Wait** until the Lean artifacts are public (BLOCKED today).
2. **Build check** against our pin: `lean/lean-toolchain` = `leanprover/lean4:v4.34.1`; Mathlib in `lean/lake-manifest.json`
   rev `d13f23b723b8a846827a245b89c10fc7d3f11612` (inputRev v4.34.1). Record whether it builds as-is, with a bump, or not at all.
3. **Candidate discharges.** Quick `rg` on 2026-10-29 over `lean/` for `axiom` declarations, FRONTIER-AXIOM items and
   hypotheses about existence / well-definedness of interacting gauge theory, unitarity or positivity:
   **none found.** There are no `axiom` declarations in `lean/`; files mentioning FRONTIER-AXIOM (FCoulomb, FDim, FDimMass)
   state "no FRONTIER-AXIOM"; `lean/axioms/UnitarisedLS_axioms.lean` is only `#print axioms` checks. Unitarity / positivity
   enter as explicit finite-dimensional theorem premises (e.g. `h_pos`-style binders in PionBound, MassiveLS, LECRatio),
   not as assumptions about QFT existence, so an existence theorem would not directly discharge them. Re-audit on release.
4. **Replace** a hypothesis only after the checker passes; record as CITED dependency with commit hash of their release.

Outcome class: foundations / dependency card. Credit 0 by construction.

## 4. Gauge-group note [SPECULATION]

If the post's "simplest grand unified theory" is identified (gauge group named on release), it may bear on the JORD-1 /
triality "why the SM gauge group" line. No rung proposed until the group is known.

## 5. Local smoothing remark

The local smoothing / Kakeya result is only distantly related to the carrier-wave / pilot-wave B11 ideas; no rung proposed.

## 6. exclusion ledger

One placeholder row added to notes/EXCLUSION-LEDGER.md: existence is not determination.

## 7. Update 2026-10-29 (evening): YM-EXIST-WATCH folded in; POS-GAP added

*Appended 2026-10-29 by Grok. Notes only. No prereg, no rung, no run. Approved by author approved (2026-10-29).
Sections 0–6 above are unchanged and still stand.*

### 7.1 YM-EXIST-WATCH (folded into YM-IMPORT) [CITED: fetched 2026-10-29]

Source: "Proof by OpenAI of the Existence of Quantum Yang-Mills theory. Statement by the shepherding committee",
M. R. Douglas, D. J. Gross (Chair), A. Jaffe, I. R. Klebanov, N. Nekrasov, October 2026.
<https://www.kitp.ucsb.edu/sites/default/files/YM_working_group.pdf> (2 pages; sha256 of the fetched PDF
`dbab31f0f954ac8265a3fc1c1a29664c7fa0b7f16c616d58012e65896557bd12`).

What the statement says (claims, not yet released or reviewed):

- OpenAI's work proves the existence of quantum Yang–Mills theory, "including coupling to fermions".
- The proof builds on Balaban's constructive renormalisation-group papers (1980s) and reaches "the existence of its proper
  continuum limit".
- "Confinement and the mass gap remain very important open challenges."
- OpenAI is providing a Lean formalisation. The committee's first objective is "to check that the definitions and problem
  statement correspond with those which are standard in physics and mathematics, and that the formalization aligns with the
  informal treatment"; only then will the Lean proof be released, and later the "full 1147-page LLM proofs" with the
  committee's assessment.
- It points to Douglas, "The Yang–Mills Millennium problem", Nat. Rev. Phys. 8, 86–97 (2026),
  doi:10.1038/s42254-025-00909-2 (checked against Crossref 2026-10-29: title, author, vol. 8, issue 2, pp. 86–97).

The statement's text does not itself say "four-dimensional"; the dimension comes from the OpenAI post (section 1) and the
committee's contact address.

**YM-IMPORT status: PLANNED, NOT RUN, BLOCKED, low priority.**

- **Reopen trigger:** public release of the Lean proof.
- **Planned checks on release:**
  1. Definitions audit: compare the released definitions and main theorem statement with the standard Osterwalder–Schrader /
     Wightman axioms (the same question the committee asks first). Our well-posedness gate applied to someone else's theorem.
  2. Build check against our pin (section 3 item 2: Lean v4.34.1, Mathlib rev d13f23b…).
- Existence is still not determination (section 2): no change to the mission meter.

**Not added:** Chronoflux (Roy Herbert reply): built inside a given spacetime with free inputs, so it would be FM-FREE; no card.

### 7.2 POS-GAP (frontier) [CONJECTURE; PLANNED, NOT RUN]

Full note: notes/FRONTIER-POS-GAP-2026-10-29.md. Question: is there a positive-geometry object for a gapped or confining
theory whose defining data force a mass gap? Mission hit only if the structure predicts a gap with no extra input.
The Millennium prize problem is explicitly out of scope (fails the feasibility gate).

| Node | Status | Gate |
|---|---|---|
| YM-IMPORT (incl. YM-EXIST-WATCH) | PLANNED, NOT RUN, BLOCKED, low priority | public Lean release; then the author's go |
| POS-GAP | CONJECTURE / PLANNED, NOT RUN | a well-posed prereg and the author's go |
