# CHIRAL-LATTICE-1 result (rung 2/2, Grok, 2026-10-30; author approved)

Prereg 8733135 (refusals c6e895d). Locked checker `sims/chirallat1/chirallat1_checker.py`, unchanged. Outputs: `sims/chirallat1/chirallat1_{planted,broken,live}.json`.

## Verdict
**Mechanical (locked): BITES [MECH-FP].** SIMULATED. 71 records; (c) records: MR-2b, MR-3, MR-3b, FZ-1, FT-1, MR-7′, STRUCT-1, STRUCT-1b (pre-basin) and BRIDGE-PL-ASSOC (B2). All other basins (a); B6/B9/B10/B11 NO-RECORD.
**Adjudication (report-only, not verdict-bearing): every (c) line is FALSE-POSITIVE**, so the reading is VACUOUS: no record claims to produce chiral fermion content, so Nielsen–Ninomiya has nothing to bite on. Tag FM-QNBLIND (programme) + FM-SPEC (keyword instrument).

| Record | (c) line gist | Reading |
|---|---|---|
| MR-2b, MR-3, MR-3b | "chiral logs", "chiral-limit LS" | FALSE-POSITIVE: ChPT sense of "chiral", not fermion chirality |
| FT-1, MR-7′ | "… already proved ≠ chiral" | FALSE-POSITIVE: chiral-limit line; "≠" not in NEG |
| FZ-1 | "prediction κ = 0 for a hidden-zero fermion" | FALSE-POSITIVE: a property of a given fermion, not producing chirality |
| STRUCT-1 l.19, STRUCT-1b | "rules out hypercharge fixed by …" | FALSE-POSITIVE: negation ("rules out" not in NEG) |
| STRUCT-1 l.22 | reopen trigger "a positive-geometry statement that forces the chiral field content" | FALSE-POSITIVE as a claim; it is a **conditional obligation**: if that reopen ever fires, the construction must say whether it is a local, translation-invariant discretisation (then it must name a doubling evasion: domain wall / overlap / Ginsparg–Wilson) or not (then NN does not apply) |
| BRIDGE-PL-ASSOC | "columns = 15 Weyl states … prediction … was wrong" | FALSE-POSITIVE: Weyl states are input labels |

- Planted T1–T5, verdict map, gate self-tests: ALL OK. Broken B1–B3: ALL REJECTED (empty corpus → ILL-DEFINED).
- Null (control basins B1, B4; 8 records): (c) rate 0.0. The false positives came from pre-basin LS/ChPT records, which the control set did not cover, so the null under-estimated the instrument's polysemy error.
- Rival (all-(a) FM-QNBLIND prior): mechanically does not match (9 (c) records); after adjudication it matches.
- CONV-NA. Memory audit: regex vocabulary from memory; no target number; no contamination path (the corpus is our own records). No tuning: no regex changed after scoring.

## Lean (PROVED, 0 sorry, no native_decide; axioms ⊆ {propext, Classical.choice, Quot.sound})
`PositiveGeometryEmergentSpaceTime.ChiralLat1.ups_sub_dns` (telescoping), `getLast_snoc`, `cyclic_ups_eq_dns` (closed loop: up-crossings = down-crossings, the 1D shadow of no-doubling), `naive_sin8` (naive sin(2πk/8) sign pattern: one right-mover, one left-mover; `decide`). AxiomsAll 1185 thm / 637 defs / 0 nonstandard / 0 sorry-dependent. Peak RSS 0.66 GB, LEAN_NUM_THREADS=1.

## Prior art (CITED)
Kaplan hep-lat/9206013; Neuberger hep-lat/9707022; Lüscher hep-lat/9802011; Nielsen–Ninomiya 1981 and Ginsparg–Wilson 1982 (not on arXiv, MEMORISED).

## Credit
Proposal: 0 (map fact only).

Failure-mode: FM-SPEC (keyword instrument cannot tell ChPT "chiral" from fermion chirality, nor "rules out"/"≠" from assertion; every mechanical bite was a false positive) + FM-QNBLIND (adjudicated: no basin produces chiral content, so the constraint is vacuous for the programme).
