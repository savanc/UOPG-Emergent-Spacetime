# GB-2s prereg — cell-level scoring of GB-1a against the GB-2 watch source (2026-10-14), pushed alone first
## Source (identified from metadata/abstracts only)
arXiv 2205.06190 (Bonanno, D'Elia, Lucini, Vadacchino, PLB 833 (2022) 137281) = "Ref. [30]" of 2210.07622.
Abstract/metadata (already seen): SU(6) only, ONE lattice spacing a ≃ 0.0938 fm, 20k configurations, masses to 2–5%;
proceedings map cubic irreps A1→0, A2→3, E→2, T1→1, T2→2 (no J = 4 assignment stated).
## Predictions (exactly as registered in prereg/GB-1a-closed-string-glueball-predictions-2026-10-13.md, 17ee8d1)
Model A (Nambu–Goto, D=4): m(2++)/√σ = 4.7998, m(4++)/√σ = 6.9405, ratio 4++/2++ = 1.4460 (√(23/11)).
Model B (rival; LS-anchored closed intercept 1): 3.5449, 6.1400, ratio 1.7321.
## Bands (as registered): PASS |pred − lat| ≤ max(2σ_lat, 5%); PARTIAL ≤ 10%; FAIL otherwise. Registered rule needs a
CONTINUUM value with the paper's own J = 4 spin label for 4++; 2++ rows are CONTAMINATED at N = ∞ (finite N soft-blind).
## Null: m(4++)/m(2++) = 1 (no spin splitting) and, for 2++, the trivial "m(2++)/√σ = m(0++)/√σ" is not used (0++ not opened).
## Usability gate (applied BEFORE opening any table, from the metadata above):
U1 continuum value available? U2 a J = 4 (4++) state labelled by the authors? U3 2++ in units of √σ?
If U1 or U2 fails → STOP: no cells opened, tag FRONTIER-DATA (per steering condition 4).
## Cells (only if U1–U3 pass): the E++ and T2++ ground-state rows and the authors' J=4 row, column "aM" and the √σ row,
SU(6), pulled by sims/gb2s/gb2s_cells.py by exact row label. Nothing else.
## Verdicts (exhaustive): per-model PASS/PARTIAL/FAIL as registered; STOPPED-FRONTIER-DATA if the gate fails;
otherwise UNCLASSIFIED. Credit proposed only; cap 0.5 per model (GB-1 soft-blind cap).
