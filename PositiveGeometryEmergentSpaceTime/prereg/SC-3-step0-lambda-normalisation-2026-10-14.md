# SC-3 step 0 prereg — is "λ₄ = g²" in EW-Z1b the Higgs quartic? (2026-10-14)
Pushed alone before any work on this rung. Source: notes/SCALE-SWEEP-2026-10-14.md §SC-3 step 0.
Well-posedness gate only; no running, no data, no numbers matched.

**Question:** SC-3 assumes EW-Z1b forces the Higgs self-coupling λ to equal g² at tree level. Does the coupling `lam4` in `lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean` (READ ONLY; not edited) denote the Higgs quartic, or something else?
**Cells (exact):** (A) the sentence(s) of the EWZ1b module docstring that name `lam4`; (B) the argument list of `def N`. Extracted only by the locked script.
**Disclosure:** while locating SC-3 inputs at I saw EWZ1b.lean line 8 (the docstring line naming lam3/a/lam4) in a grep. No numeric target is involved; disclosed, not CONTAMINATED in the numeric sense.

**Fixed constant basis:** N/A (no number matching; declared to satisfy METHOD).
**Locked checker + planted inputs (sha256):**
```
630c1bd1e76c9dafd4416f4d09142fd1f4aeb2484d7289ededb741ba3e7310da  sims/sc3/sc3_step0_check.py
9f11d27a6530df0cc9ac83726388a1eda58ab79e02086d6faec0cf8ada6b55c3  sims/sc3/planted/good.lean
d9a66c76be5c20225daefe248149246305f39a4cad89802e8851ee054300a751  sims/sc3/planted/broken.lean
```
**Planted-answer test (before live):** good.lean (lam4 labelled Higgs quartic) must give WELL-POSED; broken.lean (no `def N`) must be REJECTED. Either failing ⇒ STOP. Log → sims/sc3/sc3_planted.txt.

**Verdicts (exhaustive):**
- WELL-POSED: lam4 is labelled a Higgs/scalar quartic, or N has a separate Higgs-quartic argument ⇒ proceed to SC-3 step 1 (new prereg).
- NOT-WELL-POSED: lam4 is labelled the VVVV (four-gauge) contact and N has no Higgs-quartic argument ⇒ SC-3 premise void; record NO-GO for "λ(μ*) = g²" from EW-Z1b; rung complete at the gate.
- Otherwise (script reject on live file, ambiguous label) → UNCLASSIFIED (report closest and why).

**Lean:** none planned (nothing claimed PROVED). **Proposed credit:** 0.
