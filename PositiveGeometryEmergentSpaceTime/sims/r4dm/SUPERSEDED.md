# sims/r4dm (R4-DM v1) — SUPERSEDED 2026-10-20 (forward note; the locked v1 files are NOT edited)
Superseded by **R4-DM v2**: prereg `prereg/R4-DM2-2026-10-20.md` (af4430e), checker `sims/r4dm2/r4dm2_checker.py`,
result `reviews/R4-DM2-result-2026-10-20.md`. v2 fixes the three v1 defects found by hand reading
(D1 bound field reads, D2 Lean-generated constructor lemmas, D3 suffixed role overrides). v1 outputs
(`r4dm_live.txt` 6/87, planted/broken/history) stay as historical records; v1's B3 history scan is not repeated in v2
and stands. `R4DMExport.lean` remains in use: v2 hash-locks it and requires its export block to be byte-identical.
