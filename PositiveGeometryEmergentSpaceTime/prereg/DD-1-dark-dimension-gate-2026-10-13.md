# DD-1 prereg — dark-dimension R↔Λ chain vs sub-mm gravity (2026-10-13)
Written before reading any target content. Pre-check (sims/dd1/dd1_numcheck.py, prints counts only): both abstracts contain numbers
(2205.12293: 23 numeric tokens; 2002.11761: 10), with length/energy units.

## Question (OUT-OF-BOX gate #9)
Does the dark-dimension chain fix the extra-dimension size R from Λ with no free O(1) factor, and is the resulting R allowed by the
Eöt-Wash inverse-square test? An observable outcome = an R window that sub-mm gravity can probe.

## Cells (only these; pulled by sims/dd1/dd1_cells.py)
- D1: sentences of the 2205.12293 abstract (Montero–Vafa–Valenzuela) that contain a digit.
- D2: sentences of the 2002.11761 abstract (Lee et al., Eöt-Wash) that contain a digit.
Contamination: I recall R ~ μm scale and an O(1)–O(10^-1..10^-4) λ factor; recall not used for scoring.

## Verdicts (exhaustive)
- PASS: D1 gives R as a function of Λ with no free parameter, and that R is not excluded by D2.
- FAIL-OBS: no free parameter, and that R is excluded by D2.
- PARTIAL: R carries a free factor but the implied R range spans ≤ 1 decade, and at least part of it is allowed by D2.
- FAIL (gate): R carries a free factor spanning > 1 decade in R (no sharp prediction).
- otherwise → UNCLASSIFIED (incl. cells lacking the needed numbers).
Credit cap 0.25 (OUT-OF-BOX table); proposal only.
