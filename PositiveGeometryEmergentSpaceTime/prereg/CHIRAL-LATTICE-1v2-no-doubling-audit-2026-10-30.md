# PREREG CHIRAL-LATTICE-1 v2: does Nielsen–Ninomiya no-doubling bite any basin record? (locked, sense-disambiguated re-run)

Authorisation: author approved (2026-10-30). Exactly 1 rung. STOP removed in b4b94a2.
**Supersedes** prereg/CHIRAL-LATTICE-1-no-doubling-audit-2026-10-30.md (v1, prereg 8733135, result d26f3b4). v1 files (prereg, sims/chirallat1/*, v1 review) are not edited.

## 0. Why this rung (beat the alternatives)
Not an EV pick: The author named this rung. Purpose is method integrity: in v1 the locked checker said BITES [MECH-FP] on 9/71 records and the reported reading (VACUOUS) came from hand adjudication after the run, which METHOD does not allow to be verdict-bearing. v2 makes the verdict come from a locked checker. No alternative rung was eligible under this authorisation.

## 1. Memory / contamination disclosure
- The v1 outcome is KNOWN: the 9 v1 (c) records (MR-2b, MR-3, MR-3b, FZ-1, FT-1, MR-7′, STRUCT-1, STRUCT-1b, BRIDGE-PL-ASSOC) and their (c) lines were read by me, and the 9 records' chiral/Weyl/handed lines were read while designing NONF/NEG/MODAL/INPUT (e.g. "chiral zero", "chiral Wilson coefficients", "e.g." clause split). No other live record was read or scored by any v2 code before this push.
- Therefore this rung is **method-integrity only**: a VACUOUS verdict is expected and carries no discovery value. **Credit proposal: 0.**
- Bias disclosure: the INPUT and MODAL lists are broad, so the instrument leans toward NOT-BITES (risk FM-TAUT against the VACUOUS prior). The synthetic true positives S1, S2, S5, S14, S15 are the counterweight.

## 2. Corpus, rule, verdict (locked; implemented in `sims/chirallat1v2/chirallat1v2_checker.py`)
- Corpus: identical to v1: every record path of `scripts/blocker_tags.py` B at **v1 prereg commit 8733135** (71 records), read with `git show 8733135:path`; same basin map as v1. B6/B9/B10/B11 NO-RECORD (not read).
- Unit = clause. Normalise (NFKC; strip `*` and backticks); split lines on `; ! ?`, sentence-final `.` (not after `e.g`/`i.e`) and ` — `.
- (b) **Non-fermion senses removed first** (NONF): ChPT, χPT, chiral perturbation / log(s) / limit / Lagrangian / condensate / symmetry / expansion / EFT / effective / order / counting / coefficient / constant / extrapolation / algebra / ring / primary / boson / scale / regime / point / line / fit / trajectory / LEC / Wilson coefficient / zero (not "zero mode"), and "chiral … breaking".
- A clause is a CHIRAL-HIT if what remains matches FERM (chiral*, chirality, Weyl fermion/spinor/state/field/particle/mode, left-/right-handed).
- A CHIRAL-HIT clause is a **CLAIM** iff it matches OUT (produce, derive, select, emerge, output, predict, force, generate, yield, fixes/fixed, arise, obtain, reproduce, realise, gives rise) and none of:
  (a) NEG: no, not, cannot, can't, never, none, neither, nor, n't, rule(s/d) out, ≠, exclude, nothing, refute, fail, no-go, absent, lack;
  MODAL: if, whether, would, could, might, must, should, reopen, trigger, need(ed), require, obligation, future, planned, conjecture, speculat-, proposal, hypothe-, FRONTIER-THEORY, once;
  (c) INPUT: input(s), label, assum-, given, taken as, by hand, column(s), row(s), index, fed, hand-added, postulat-, impos-, rep/representation(s), encod-.
- ESC (stated doubling escape): domain wall, overlap operator/fermion/Dirac, Ginsparg, Neuberger, Kaplan, Lüscher, mirror fermion, non-local, Wilson term, staggered, not translation-invariant, higher-dimensional bulk, anomaly inflow; counted only in a clause without NEG.
- Record label: `c` = ≥ 1 CLAIM and no ESC clause in the record (BITES); `e` = ≥ 1 CLAIM and ≥ 1 ESC clause (ESCAPED); `a` otherwise (NOT-BITES).
- **Decision rule (fixed now):** ILL-DEFINED if the corpus is empty, a record is unreadable, or the null gate fails (any control record labelled `c`); else **BITES** if any record is `c`; else **ESCAPED** if any `e`; else **VACUOUS**. The live run is executed only if planted ALL_OK and broken ALL_REJECTED; if either fails, the rung is ILL-DEFINED (FM-SPEC) and the live run is not executed.
- **NO hand adjudication of the live output.** The locked verdict is reported as-is. If the live output looks wrong to me, I record it as a checker flaw in a superseding note (new rung needed to change anything); I do not flip or annotate-away the verdict.

## 3. Planted / broken / null / rival / conventions
- Planted (must all recover): the 9 v1 false-positive records (full text at 8733135) → `a`; synthetic S1, S2 (output chiral fermion, no escape) → `c`; S5 (claim + negated escape "No domain wall is used") → `c`; S14 (markdown) and S15 (NFKC ligature "ﬁxes") → `c`; S3 (domain wall) and S4 (overlap / Ginsparg–Wilson) → `e`; S6 cannot, S7 rules out, S8 ≠ → `a`; S9, S10 ChPT / condensate / symmetry breaking → `a`; S11 input labels → `a`; S12 reopen trigger → `a`; S13 mention → `a`. Verdict-map test incl. null-gate failure → ILL-DEFINED. Gate self-tests: every regex and the control predicate true once, false once.
- Broken (must each be rejected by the planted suite): checker with negation handling removed; ChPT exclusion removed; INPUT removed; MODAL removed; ESC removed; normalisation removed; plus empty corpus → ILL-DEFINED.
- Null: control records (basins B1, B4 and the hadron/ChPT/LS-sector pre-basin rungs MR-, FT-, FZ-, LAT-, SC-, NL9, M3, OP-2, DZ-, KS-, KL-, TH-, UL-, SUB-), which by construction claim no chiral fermion output; they share the polysemous words (v1 lesson). Report the `c` rate; gate: must be 0. (Overlap: MR-2b, MR-3, MR-3b, FZ-1, FT-1, MR-7′ are both planted and control.)
- Rivals: (1) the FM-QNBLIND prior "every record NOT-BITES" (VACUOUS); (2) the v1 locked checker (BITES, 9 records). Report which the v2 verdict matches.
- Convention screening: **CONV-NA** (classification of record text; no physics normalisation, sign, basis or unit enters). In-rung text-convention invariance (markdown / NFKC) is planted (S14, S15).

## 4. Lean
None planned (optional for this rung; v1's `PositiveGeometryEmergentSpaceTime.ChiralLat1` stands). AxiomsAll unchanged.

## 5. Tags
Verdict SIMULATED (mechanical). Prior art as v1 (Kaplan hep-lat/9206013; Neuberger hep-lat/9707022; Lüscher hep-lat/9802011; CITED in v1). Expected FM-QNBLIND (if VACUOUS). Credit: proposal 0.

## 6. Lock
`chirallat1v2_checker.py` sha256 `8649f9eb55e47ce3b9a1a525d73df8bb327fb892c367d024109c62aa7238cd95`
`guard.py` sha256 `28d35da59167e4a3877d3905c6e0c4611d27841a2ad7fbac8addca57db8b7afd`
Guard (hardened): called in every scoring/live function (planted, broken, null, rival, live, _suite, _run); on every call re-reads this prereg, re-hashes checker + guard, re-runs `git merge-base --is-ancestor <prereg commit> origin/main`; no pass flag. Import test and CLI must refuse before the push (sims/chirallat1v2/guard_refusal.txt).
