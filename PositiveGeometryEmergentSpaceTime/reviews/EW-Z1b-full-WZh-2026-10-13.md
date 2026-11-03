# EW-Z1b — full massive-vector hidden-zero check (2026-10-13)
Status: **CONTROL REPRODUCED; FORCING FOUND = SM/gauge values (no deviation)**. Credit proposed: **0** (cap would be 0.25: SM match + CONTAMINATED). No data read. No deviation → nothing time-stamped.

## Memory audit
Remembered: gauge-theory relations (quartic = cubic², hWW = g·m_W), CLT/Llewellyn Smith unitarity results, Naculich's dimensional-reduction construction. CGW 2601.16860 read this session (§VI). Any SM-match therefore CONTAMINATED.

## Prior art (credited)
- Carrillo González & Ward, arXiv 2601.16860 §VI: Proca YM has no zero (eq. 53–54); U(N)→U(1)^N adjoint-Higgs SSB keeps zeros (via X→X̃).
- Naculich, JHEP 09 (2015) 122 (1506.06134): Coulomb-branch amplitudes = dimensional reduction of massless YM.
- Cornwall–Levin–Tiktopoulos; Llewellyn Smith (1973–74): unitarity forces the same relations.

## Method (SIMULATED, exact symbolic sympy — `sims/ewz1b/`, outputs `output*.txt`)
Colour-ordered 4-pt tree A[1234] from Feynman rules with each vertex term tagged by its number of Higgs-direction indices:
lam3 (VVV), a (VVS: h/Goldstone–W–W per unit mass), gs (VSS), lam4 (VVVV), b (VVSS = hhVV), kap3 (h³). All = 1 ⇔ CGW's SSB theory.
Contact normalisation fixed by massless Ward identity (not tuned). Hidden-zero locus: c̃₁₃ = −2K₁·K₃ = 0, ε₁·ε₃ = ε₁·p₃ = ε₃·p₁ = 0.
Massive spinor-helicity (BH-2 `MassiveSpinor`) not needed: the CGW conditions are polarisation-vector dot products, so the check is done in the general dot-product basis (stronger: all helicities at once).

## Results
| Check | Result |
|---|---|
| Control-0 massless YM | zero ✓ |
| Control-1 Proca, uniform m | residual = m²/(s−m²)[(ε₁ε₂)(ε₃ε₄) − (ε₂ε₃)(ε₁ε₄)] — **exactly CGW eq. 53** ✓ |
| Control-2 SSB (same & generic vevs), 5D Ward identity | zero ✓ (reproduces CGW §VI.2) |
| WW→WW, couplings free (generic vevs, and with physical neutral h in t-channel) | zero ⇔ **a = ±lam3 and lam4 = lam3²** (gauge/SM values; sign = field redefinition) |
| W W γγ (diagonal neutral) | same forcing |
| [W h W h] | identically zero for all a, gs, b → **blind** |
| [W W h h] (hhVV b, h³ kap3) | CGW condition ε₃·p₁ fails in 5D form (E₃·K₁ = −κ₁); amplitude ∝ m_W²(2 + kap3/m_W) — **not posable** (would need a leg-dependent h³) |
| W W → Z Z | **not posable**: CGW setup has no massive neutral vector |
| massive h | breaks the X→X̃ structure; zeros shifted (as in EW-Z1) |

## Lean (PROVED, 0 sorry, axioms propext/Classical.choice/Quot.sound) — `lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean`
`N_decomp` (residual = Q1·(a²−lam3²) + Q2·(lam4−lam3²), generated verbatim from the Feynman rules), `zero_of_gauge`, `forced` (two explicit kinematic points ⇒ a² = lam3², lam4 = lam3²), `forced_iff`, `proca_control`, `proca_nonzero`. Axioms: `lean/axioms/EWZ1b_axioms_output.txt`.

## Conclusion / tags
Contrast with EW-Z1: there the scalar (Goldstone/HEFT) sector was blind to couplings; the full vector amplitude with CGW polarisation conditions **does** force κ_V-type (a = g) and quartic-gauge (lam4 = g²) relations — but only to their gauge-theory/SM values, the same answer as tree unitarity. FORCING: PROVED (toy CGW Coulomb-branch, 4 pt, tree). Deviation: none. κ_2V (b), κ_3: NOT POSED.
Blocker tags: SM-MATCH (cap 0.25), CONTAMINATED, FRONTIER-THEORY (hidden-zero conditions with external scalars / massive neutral Z / SU(2)×U(1) doublet breaking undefined), NO-GO for κ_2V, κ_3 at 4 pt.
Reopen trigger: a definition of hidden zeros for SU(2)_L×U(1)_Y→U(1)_em with a doublet (massive Z, γ mixing) or for external-scalar legs.
Next rung: EW-Z1c — redo for the actual SM breaking pattern (doublet, θ_W), where the zero could relate m_Z/m_W (θ_W) to couplings; gate = can the mesh/X̃ structure be defined there.

## Forward note (2026-10-20; nothing above is edited)
**Retag, approved by author approved (2026-10-20):** derived, conditional (coupling tier, amplitude-sourced, SM match;
Carrillo González–Ward arXiv 2601.16860 CITED — abstract and §VI verified 2026-10-20). The R4-DM derivation meter
(`reviews/R4-DM-result-2026-10-20.md`; v2 `reviews/R4-DM2-result-2026-10-20.md`) finds `PositiveGeometryEmergentSpaceTime.EWZ1b.forced` to be the
only Lean statement in which a geometry/amplitude property (the assumed massive hidden zero) yields SM structure (a² = λ₃²,
λ₄ = λ₃²: cubic coupling ±g, quartic g²). It is conditional (the zero is posited, not produced by a positive geometry) and
reproduces known physics, so credit stays **0** and the SM-MATCH / CONTAMINATED tags stand. Ledger class changed from
PASS to DERIVED-CONDITIONAL in `notes/REVIEW-2026-10-20/CLAIMS-LEDGER-VERIFIED.{md,csv}`.
