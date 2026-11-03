# BR-3 prereg — Klein/Spinor Plücker coordinates ↔ Network (H-T) 2×6 minors (2026-10-14)
Prior art: classical (Plücker relations for Gr(2,n)); Lam's electrical networks (H-T rungs). Nothing new physically.
Lean plan: `mn_eq_pl`: for any column map e : Fin 4 → Fin 6, Network.mn M (e i) (e j) = Klein.pl (M.submatrix id e) i j;
`plucker_any4`: the three-term Plücker relation holds for the minors of any 4 columns of a 2×6 real matrix (transfer of
Klein.plucker_rel); instance on Network.MY (Lam's Y-network point); witness.
Verdicts (exhaustive): PASS = all proved, checklist + alignment ALIGNED; PARTIAL = mn_eq_pl only; FAIL = type mismatch
prevents a statement; otherwise UNCLASSIFIED. Credit 0.
