# PREREG R4 (unify inputs) → R5 fallback (geometry_struct_separation)
Written 2026-10-15. Pushed ALONE with its locked checker and planted pair, in one commit.

**SM ledger line moved:** hypercharges / isospin (EW quantum numbers of quarks), via `ew_from_pion_geometry`; secondarily N_c.
**EV:** P_naive 0.1 → 0.03; V 0.5 → 0.015 (R4). R5 fallback: method/exclusion, capped at 0.03.

## Prior art and well-posedness (done before this prereg)
- **NLSM ⊂ Tr φ³** (Arkani-Hamed, Cao, Dong, Figueiredo, He; arXiv:2401.05483), the δ-shift, hidden zeros and the associahedral grid (arXiv:2508.20161) all produce **flavour-ordered (colour-stripped) partial amplitudes**. Flavour/charge data enter only through trace factors Tr(Tᵃ…), i.e. through the choice of the gauged subgroup Q = T₃ + Y of the chiral symmetry. That choice is not an output of the geometry. The δ-shift fixes a breaking pattern U(N) → U(N−k)×U(k) but no U(1)_Y embedding.
- **The one pion-sector object that knows quark charges is the WZW term** (π⁰→γγ, ABJ / anomaly matching; Witten 1983). It is parity-odd and topological. No positive-geometry or surfaceology construction of it exists (search 2026-10-15; the WZW bordism literature, e.g. SciPost Phys. 10, 061, is not geometric in our sense). The trunk has no WZW declaration (repo grep).
- **Bär–Wiese** (hep-ph/0105258): with anomaly-consistent charges, A(π⁰→γγ) ∝ N_c(Q_u² − Q_d²) is N_c-independent.
- **Well-posedness outcome: R4 has no concrete, non-metaphorical candidate.** The rung executes as **R5**. R4 is kept open only behind the reopen trigger below.

## Claims (R5)
- S1 (dependency): no declaration of STRUCT1/1b/2/3/X6 uses a geometry or hadron module declaration, and none uses theirs (Lean dependency scan of graph/raw_decls.jsonl, type and value uses).
- S2 (Lean): with ACC (STRUCT-2 `ACCN`) and the lepton-doublet normalisation yL = −1/2, the π⁰→γγ coefficient N_c(Q_u² − Q_d²) = 1 for every N_c ≠ 0. The single pion↔charge link is therefore blind to N_c (in the anomaly-consistent class).
- S3 (Lean bundle `geometry_struct_separation`): the conjunction of the existing no-gos (STRUCT1.not_unique_with_nu, STRUCT1b.dirac_not_unique, STRUCT2.three_not_selected, X6.positivity_orientation_blind, X6.vectorlike_acc_vanish, STRUCT3.three_not_selected_ngen) and S2.

## Verdict rules
- S1 holds and S2, S3 are proved ⇒ **R5-SEPARATION** (exclusion PASS): geometry and the EW/STRUCT inputs are separate in the current trunk.
- S1 fails (a cross edge exists) ⇒ inspect it. A substantive edge ⇒ **R4-CANDIDATE**.
- Anything else is UNCLASSIFIED.
- No MISSION.md edit. Only a claim-update proposal, in `proposals/`.

## Basis / no hadron gates
Rationals with |p|,|q| ≤ 10. No data comparison and no cited numerical hadron inputs (π⁰ width not used).

## Planted pair
sims/r4/r4_planted.txt. An injected fake STRUCT2→NLSM edge must be detected, and the N_c = 3 charges must be 2/3 and −1/3 (exit 0). An empty STRUCT set (vacuous scan) must be rejected (exit 1).

## Protocol deviation (disclosed)
While testing the checker I executed `live` once before this prereg. Seen: 0 cross edges, A = 1. Neither is a fitted or numeric target, and the verdict rules above are structural and do not depend on choosing a threshold. The deviation is logged in the AUTORESEARCH-LOG and the review.

## Locked checker
`sims/r4/r4_separation.py` sha256 `78cb891b33ec7abce2cc8d26e3f1a8388ed3a79d32132ab0a94b3c8d10b47583`.
