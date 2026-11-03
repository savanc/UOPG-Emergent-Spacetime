# PREREG CHIRAL-LATTICE-1: does the Nielsen–Ninomiya no-doubling constraint bite any basin record? (mechanical audit)

Authorisation: author approved (2026-10-30). Rung 2 of 2.

## 0. Why this rung (re-rank; exploration slot)
| Rung | P_naive | P_used | V | EV | EMC | IV_min | d vs last 3 (SURF-1′c, LEAN-CERT-2c, RG-IR-1) | Foregone? |
|---|---|---|---|---|---|---|---|---|
| **CHIRAL-LATTICE-1 (this)** | 0.3 (BITES) | 0.09 | 0.15 | 0.014 | 0.09·3 + 0.91·2 = **2.1** | 2 | 4 (new node lattice; ledger line fermion chirality; method class mechanical text audit; FM expected FM-QNBLIND) | no (mechanical BITES ≈ 0.3–0.4 from claim lines) |
| HURWITZ-TP-1 (B6) | 0.07 | 0.02 | 0.3 | 0.006 | ≈2 | 1 | 2 | FM-TAUT predictable |
| RP-BRIDGE-0 | known | — | 0 | 0 | — | 0 | — | yes, credit 0 |
| CDT-RIVAL | reading node, not a rung | | | | | | | |
| TP-1BR / EW-POS | killed at rule 7 earlier | | | | | | | |
Rung 1 (RG-IR-1) was the EV/V pick; this is the exploration (EMC) pick, d ≥ 3, IV_min ≥ 1, not declared foregone. M+: VACUOUS recorded (the constraint is vacuous for the whole programme, a map fact); M−: BITES gives a list of open obligations with line citations.
Well-posedness: the corpus, the line rule and the verdict are mechanical and fixed here; human reading is report-only. CPU-only, seconds, < 100 MB.

## 1. Prior art (arXiv abs pages read 2026-10-30)
- Kaplan, "A Method for Simulating Chiral Fermions on the Lattice", hep-lat/9206013. CITED: domain-wall zero modes evade doublers.
- Neuberger, "Exactly massless quarks on the lattice", hep-lat/9707022. CITED: overlap operator.
- Lüscher, "Exact chiral symmetry on the lattice and the Ginsparg-Wilson relation", hep-lat/9802011. CITED.
- Nielsen–Ninomiya, NPB 185 (1981) 20; NPB 193 (1981) 173; PLB 105 (1981) 219; Ginsparg–Wilson PRD 25 (1982) 2649 (not on arXiv; CITED from memory, MEMORISED).

## 2. Corpus, rule, verdict (locked; implemented in the checker)
- Corpus: every record path (5th field) of `scripts/blocker_tags.py` B **at this prereg's commit**, read with `git show <prereg>:path`. Basins from BASIN; JORD-1 → B7, SURF-1′ → B8, RG-IR-1 → RG-IR; others "pre-basin". B6, B9, B10, B11 have no run records → NO-RECORD (not read, pilot-wave stays gated).
- Regexes HIT / MECH / PROD / NEG exactly as in the checker. Line: HIT ∧ MECH → (b); HIT ∧ PROD ∧ ¬NEG → (c); other HIT → (a). Record: (c) ≻ (b) ≻ (a).
- Verdict: VACUOUS (all (a)); BITES (any (c)); EVADES (no (c), ≥ 1 (b)); UNCLASSIFIED otherwise; ILL-DEFINED (empty corpus / unreadable record).
- Report-only, not verdict-bearing: my reading of every (c) line as TRUE-CLAIM or FALSE-POSITIVE. If every (c) line reads FALSE-POSITIVE the mechanical verdict stands and is annotated [MECH-FP], FM-SPEC for the keyword method.

## 3. Planted / broken / null / rival / conventions
- Planted (must recover): T1 claim → (c); T2 domain-wall → (b); T3 "taken as input" → (a); T4 negated "cannot produce chirality" → (a); T5 no hit → (a); verdict map; gate self-tests (each regex true once, false once).
- Broken (must reject): non-fermion line labelled (c); claim line labelled (a); empty corpus → ILL-DEFINED.
- Null: records of control basins B1 (LS-pion) and B4 (Lean certification), non-fermion by construction; report their (c) rate as the false-positive rate.
- Rival: FM-QNBLIND prior "every record is (a)"; report whether it matches.
- Convention screening: CONV-NA (classification of record text; no physics normalisation enters).
- Memory audit: regex vocabulary from memory of the lattice literature; no target number. No tuning: rule fixed before any record is scored.

## 4. Lean plan (PositiveGeometryEmergentSpaceTime.ChiralLat1) and kill
Discrete 1D doubling lemma: for any cyclic Boolean sign sequence, #up-crossings = #down-crossings (general proof by telescoping, no decide over large spaces). Reading: a periodic lattice dispersion has as many right- as left-moving zeros. 0 sorry, no native_decide. Kill: > 8 GB anon RSS or > 20 min → LIMIT.

## 5. Tags
Verdict SIMULATED (mechanical) + PROVED (lemma) + CITED. Expected FM-QNBLIND (VACUOUS). Credit: proposal only (expected 0).

## 6. Lock
`chirallat1_checker.py` sha256 `18515a97898b0aa8eff35ad15e56daa2c6c2de172d4793ec5afae17ff729bd52`
`guard.py` sha256 `4d8f44803388e2c12d318b33b0d7f570d11229bc62807c35cdee05e18ecdbeca`
Guard: re-read prereg, re-hash checker + guard, re-check prereg-commit ancestry of origin/main on every call; no pass flag. Import test and CLI must refuse before push (sims/chirallat1/guard_refusal.txt).
