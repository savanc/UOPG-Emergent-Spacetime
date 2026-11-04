# SC-3 step 0 review — λ normalisation gate (2026-10-14)
**Verdict: NOT-WELL-POSED** (prereg 94eb88a). Rung complete at the well-posedness gate. Proposed credit **0**.

## Result
- Cell A: EWZ1b docstring labels `lam4` as **(VVVV)**, the four-gauge-boson contact; `a` is VVS (Higgs/Goldstone–W–W per unit mass).
- Cell B: `N` has no Higgs self-quartic argument. The 4-vector amplitude does not contain the Higgs quartic λ at tree level.
- So the credited relation "λ₄ = g²" (lam4 = lam3²) is the gauge-contact = (gauge cubic)² identity that gauge invariance forces at every scale. It is **not** a Higgs-quartic boundary condition. SC-3's premise (compare λ(μ*) = 0 from MPC/AS with an EW-Z1b λ = g²) is void.

## Consequences
- NO-GO for "μ* defined by λ_H(μ*) = g²(μ*) from EW-Z1b". SC-3 as written is CLOSED. Reopen trigger: a hidden-zero amplitude in which the Higgs self-quartic actually appears (e.g. a 4-scalar or 2V2H zero) and gets fixed.
- Trade-space: correct the SCALE-SWEEP wording "EW-Z1b forces λ₄ = g²" → "forces lam4 (VVVV) = lam3²".

## Method compliance
Prereg pushed alone ✔ · planted pair (good → WELL-POSED; broken → REJECT) sims/sc3/sc3_planted.txt ✔ · constant basis N/A (declared) ✔ · locked checker + planted inputs hashed, unedited ✔ · Lean: none (nothing PROVED) ✔ · exposure of EWZ1b line 8 before the prereg was disclosed in the prereg ✔ · EWZ1b file read only, not edited ✔.

## Lesson
Before preregistering a rung that reuses a credited coupling, check what the symbol denotes in the Lean source (docstring and argument list). "λ₄" here was a gauge contact, not a Higgs quartic.
