# F-POSGEOM-DAUGHTER result (2026-10-20, Grok; continuous-mode own pick (author approved 2026-10-20); rung start)
_Provenance corrected 2026-10-20 (forward correction; was "approved by author approved"), see notes/PROVENANCE-CORRECTION-2026-10-20.md._
**Verdict: ILL-DEFINED (gate W) + analytic NO-GO (tachyon in every member). The locked pion gates (D=4 positivity at physical m_π, a₀⁰/a₀², Γ_ρ/m_ρ pole) were NOT run, as the prereg required. Credit 0 (proposal).**

## Question
Does the geometry-native dual pion amplitude, the δ-shifted stringy Tr(Φ³) of Arkani-Hamed–Cao–Dong–Figueiredo–He (curve integrals / associahedron; NLSM ⊂ Tr(Φ³)), give a uniquely specified, zero-fit physical ππ amplitude that can be put through the locked F-DIM-MASS / F-SCATLEN / F-RHOWIDTH gates?

## Prior art (verified against arXiv text / abstract pages; table in the prereg §1)
2312.16282 §7 (eqs. 7.10–7.15, text at "α′δ ∈ (0,1) … we claim", "near ∼ 1/2", "ρ meson plays the dominant role", "tachyons with mass² = −δ", "not cyclically invariant"); 2401.05483 (field-theory δ→∞; U(N)→U(N−k)×U(k) cubic Lagrangian; full U(N) needs m_φ² = −m_φ̃²); 2403.04826; 2403.08855; 2405.09608; 1608.02569 (abelian Z-theory, 4-pt eq. 4.1/4.4, massless, cyclic); 2002.05419 (N-pion LS = LS line). No paper fixes α′δ; none gives a massive-pion extension with the zeros intact.

## Records
- Prereg 40e3ed8 (pushed ALONE): candidates F_A, F_B; rule for gate W; foregone declaration; planted/broken; locked hashes.
- Guard: import test refused both direct calls before the push (`sims/fpgd/guard_refusal.txt`); after the push: GUARD OK.
- Planted (`sims/fpgd/fpgd_planted.txt`): eq. 7.11 low-energy limit recovered to 1e−11 at d = 0.1, 0.5, 0.9; residue = 1 at d = 0.25, 0.75; classifier cases OK. Broken claim ("α′δ = ½ has no pole at X₁₃ = δ") REJECTED (residue 1.0).
- Live (`sims/fpgd/fpgd_output.txt`): RV(d) = (1−d)|Γ(−d)Γ(d)| = π(1−d)/(d sin πd) runs 91.5 → 1.13 over d = 0.1…0.9 (spread ×81 ≫ 1%); unit-residue pole at X = d in every member. GATE W: ILL-DEFINED.

## Lean `PositiveGeometryEmergentSpaceTime.FDeltaNLSM` (7 theorems + 1 def; 0 sorry; no native_decide; #lint clean; standard axioms)
`shift_preserves_c_iff`, `delta_shift_preserves_c`, `deltaAmp4_stripped`, `deltaAmp4_tachyon_residue`, `nlsm_mass_condition_tachyon`, `delta_family_tachyon`, bundle `fdelta_obstruction`. Fresh AxiomsAll (temp copy): TOTAL theorems=826 defs=376 nonstandard=0, sorry_dependent=0.

## Reading
- The geometry fixes the FORM of the deformation (unique c-preserving shift, Lean at 4 pt) but not its SIZE: α′δ is a modulus. Choosing it from m_ρ or Γ_ρ would be a fit; forbidden.
- Independent of α′δ, the NLSM members have a tachyon (mass² = −δ, residue 1); the authors call this an "unfamiliar UV completion". With established QM (no tachyonic poles in a unitary Lorentz-invariant S-matrix), the D=4 positivity gate fails for the whole family: the model fails, not physics.
- Abelian Z-theory is the one stringy NLSM with no extra modulus, but it is massless-only; the locked gates need m_π (a₀ ∝ m_π²), and no unique massive extension exists in the verified text.

## Caveats and compliance
- The W outcome for F_A was foregone from the paper text and declared so; the prior-art reading happened before the prereg (disclosed). No physical data were fetched. 1609.07078 in the working notes was a wrong id (corrected to 1608.02569).
- The "tachyon" reading uses the paper's own statement and convention 1/(X + m²); the pole limit is CITED (pole-stripped value proved).
  *Forward note 2026-10-20 (M8, approved by author approved (2026-10-20); [notes/NOTATION-AUDIT-2026-10-20.md](../notes/NOTATION-AUDIT-2026-10-20.md)): `FDeltaNLSM.delta_family_tachyon` is **algebra only** (it proves `-d < 0 ∨ d < 0`). The identification "mass² = ∓δ, a tachyon" uses the CITED propagator convention 1/(X + m²) (`FDeltaNLSM.lean:11`). Read as **PROVED (algebra) + CITED (mass identification)**. The conclusion holds in either sign convention, because the two channels sit at ±δ.*
- Not touched: CREDITS.md, EW-Z1 paths, the R4Indep blueprint block, XResearch. STOP not recreated. Physlib warning left alone. Nobody contacted.

## Reopen triggers
A geometric/consistency condition from the curve-integral picture fixing α′δ; a tachyon-free, cyclic c-preserving pion deformation with a unique massive-pion extension; a uniquely specified massive abelian Z-theory.
