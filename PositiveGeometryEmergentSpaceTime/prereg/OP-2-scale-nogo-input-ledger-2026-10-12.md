# OP-2 pre-registration (2026-10-12): scale no-go + minimal input ledger + operational milestone

Committed BEFORE lean/PositiveGeometryEmergentSpaceTime/ScaleNoGo.lean exists.

## Targets (Lean, PROVED only if lake build passes, 0 sorry, std axioms)
(a) `stabilizer_smul_eq`: for a linear action (DistribMulAction G V over a field K, actions commuting:
    SMulCommClass G K V), c ≠ 0 ⇒ stabilizer G (c•v) = stabilizer G v.
(b) `orbit_smul`: orbit of c•v is c•(orbit of v) (scaling acts on the vacuum manifold bijectively).
(c) `opData_scale_invariant`: any function F of the stabiliser data (F : Subgroup G → α) satisfies
    F(Stab(c•v)) = F(Stab v); hence `no_magnitude`: a function of stabiliser data cannot equal ‖v‖ (or any
    map with f(c•v)=|c|f(v), f(v)≠0) for all c — no dimensionful magnitude is fixed.
(d) `no_cross_ratio`: two independent sectors v₁, v₂ rescaled independently (c₁,c₂): stabiliser data is
    invariant, while a magnitude ratio ‖v₁‖/‖v₂‖ changes ⇒ no function of the data fixes the ratio.
(e) Amplitude side `LS_scale`: the LS amplitude written with dimensionful (s,u,m_ρ²) depends only on
    (s/m_ρ², u/m_ρ²); invariant under (s,u,m²)↦(λs,λu,λm²), λ>0, so the family never selects m_ρ.
PASS = (a)–(e) proved. Partial = (a)–(c). These are expected-true (no-go formalisations; not blind, not a data test).

## Ledger and milestone (decided now, fill in review)
Ledger rows: m_ρ/Λ_QCD; quark-mass input (m_π); f_π normalisation; v; ρ_Λ; M_Pl; SM 19 (PDG GUT review, fetched).
Milestone operational form: "From minimal input set S, predict N independent dimensionless observables with zero
fits; score = #passed blind / #posed". Only pre-registered, data-tested rungs count; non-blind counted separately.

## Prior art (credit)
Buckingham 1914 Phys. Rev. 4, 345 (fetched abstract page); Landau theory scale freedom (memory: the magnitude of the
order parameter is set by potential coefficients, e.g. v²=−μ²/λ, not by the symmetry pattern); PDG RPP 2026 GUT review
(fetched): SM has 19 parameters, +9 for Majorana neutrinos.
