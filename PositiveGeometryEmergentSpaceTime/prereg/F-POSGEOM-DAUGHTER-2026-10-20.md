# PREREG F-POSGEOM-DAUGHTER: well-posedness gate for a geometry-native dual pion amplitude (δ-shifted stringy Tr(Φ³))
Written 2026-10-20 by Grok. Continuous mode; approved by author approved. STOP absent on origin/main at rung start (re-checked).
This file is pushed ALONE (with its locked checker, planted spec and import test) before any checker computation. No physical datum is fetched in this rung unless gate W passes.

## 1. Prior-art sweep (done BEFORE this prereg; every item verified against its arXiv text/abstract page)
| arXiv | Authors | What the text says (verified) | Role here |
|---|---|---|---|
| 2312.16282 | Arkani-Hamed, Cao, Dong, Figueiredo, He ("Hidden zeros…") | §7: δ-shift X_ee→X_ee+δ, X_oo→X_oo−δ (unique c-preserving shift); 4-pt I₄^δ = Γ[α′(X₁₃−δ)]Γ[α′(X₂₄+δ)]/Γ[α′(X₁₃+X₂₄)] (eq. 7.10); low energy → NLSM with λ² = α′Γ[−α′δ]Γ[α′δ] (7.11); "α′δ ∈ (0,1) … we claim … NLSM"; α′δ→1: a light spin-1 (ρ-like) state descends; UV completion has "colored massive scalars … mass² = δ or tachyons with mass² = −δ", "not cyclically invariant" | **Candidate F_A (the geometry-native one)** |
| 2401.05483 | Arkani-Hamed, Cao, Dong, Figueiredo, He ("NLSM ⊂ Tr(φ³)") | field-theory δ→∞ limit gives NLSM with f_π² ∝ δ; cubic Lagrangian U(N)→U(N−k)×U(k); full non-linear U(N) needs m_φ² = −m_φ̃² ("physically problematic"); general shifts give masses m_χ² | massive extension of F_A |
| 2403.04826 | Arkani-Hamed, Figueiredo ("Circles and Triangles, the NLSM and Tr(Φ³)") | elementary proof of NLSM⊂Tr(Φ³), field theory | no new parameter fixing |
| 2403.08855 | Cao, Dong, He, Shi ("A universal splitting…") | splits of Koba–Nielsen factor; "via a simple deformation to unified stringy amplitudes", splitting of NLSM | no parameter fixing |
| 2405.09608 | Arkani-Hamed, Figueiredo ("All-order splits and multi-soft limits") | splits from binary geometry of curve integrals | no parameter fixing |
| 1608.02569 | Carrasco, Mafra, Schlotterer ("Abelian Z-theory") | NLSM = α′→0 of abelian disk integrals; 4-pt eq. 4.1/4.4 (massless, cyclic) | **Candidate F_B** (stringy NLSM, massless only) |
| 2002.05419 | Bianchi, Consoli, Di Vecchia ("N-pion extension of the Lovelace–Shapiro model") | N-point LS; 4-pt reduces to LS | = LS line, closed by F-DIM-MASS/F-SCATLEN/F-RHOWIDTH |
(Correction: the summary's "1609.07078" for abelian Z-theory was wrong; the verified id is 1608.02569, ref. [32] of 2312.16282. Ref. [37] is 2002.05419.)

## 2. Gate W (well-posedness), fixed rule
A family passes W iff (i) it is uniquely specified as a physical π⁺π⁰π⁻ amplitude with massive pions (needed by the locked gates: D=4 positivity at physical m_π; a₀⁰, a₀² at threshold 4m_π²; Γ_ρ/m_ρ pole), and (ii) every continuous parameter other than overall scales fixed by declared inputs (α′ by a mass, normalisation by F) is fixed by a declared geometric or consistency condition from the verified literature. Fitting to data is forbidden (no family invented to fit).
- **F_A:** parameter α′δ ∈ (0,1). Literature reading: no text fixes it (2312.16282 only discusses regimes "near 0", "∼½", "→1"). Checker test (no physical input): the dimensionless ρ-type ratio RV(d) = (1−d)|Γ(−d)Γ(d)| (first spin-1 mass² × λ²) is evaluated on the declared grid d = 0.1…0.9; if max/min − 1 > 1% the parameter changes dimensionless predictions ⇒ **ILL-DEFINED**. Massive pions (2401.05483) need extra independent shifts ⇒ (i) also fails.
- **F_B:** no continuous parameter beyond α′ and normalisation, but massless pions only; no unique massive deformation is given in the verified text ⇒ (i) fails ⇒ **ILL-DEFINED for the locked gates** (a₀ ∝ m_π² cannot be predicted by a chiral-limit amplitude; using chiral-limit gate definitions would change locked definitions).
- **Overall:** ILL-DEFINED unless one family passes W. If W passes (not expected), a NEW prereg with the locked F-DIM-MASS/F-SCATLEN/F-RHOWIDTH definitions is required before any data comparison.

## 3. Foregone check (declared)
- The W outcome for F_A is FOREGONE from the paper text (α′δ is left free) — this rung's content is the formal record plus the analytic obstruction below.
- **Analytic obstruction (Lean `PositiveGeometryEmergentSpaceTime.FDeltaNLSM`, compiled before this prereg, no physical inputs):** `shift_preserves_c_iff` (4-pt uniqueness of the c-preserving shift), `deltaAmp4_stripped`, `deltaAmp4_tachyon_residue` (pole at X₁₃ = δ, pole-stripped value exactly 1 for every δ ⇒ state of mass² −δ, CITED convention 1/(X+m²)), `nlsm_mass_condition_tachyon` / `delta_family_tachyon` (m_φ²+m_φ̃² = 0, m_φ² ≠ 0 ⇒ a tachyon). Consequence: even if α′δ were fixed, every NLSM member of F_A has a tachyonic exchange and would fail the D=4 positivity/unitarity gate (CITED QM: no tachyonic poles in a unitary Lorentz-invariant S-matrix). FOREGONE-FAIL of gate 1, independent of δ.

## 4. Contamination audit
Memorised: Γ(x)Γ(−x) = −π/(x sin πx), so RV varies strongly in d (known before running). No physical numbers are used; no digit masking needed. Abstracts/§7 text of all papers above were read before this prereg (disclosed).

## 5. Planted and broken
- Planted: eq. 7.11 low-energy limit I₄/(L2·(X+Y)) → 1 at d = 0.1, 0.5, 0.9 (tol 1e−9); numerical residue = 1 at d = 0.25, 0.75 (tol 1e−20); classifier cases constant → not free, varying → free. Any planted failure ⇒ checker defective, rung ILL-DEFINED for that reason instead.
- Broken (already proved false, `FDeltaNLSM.deltaAmp4_tachyon_residue`): "the α′δ = ½ member has no pole at X₁₃ = δ". Must be REJECTED.

## 6. Prediction
F_A: ILL-DEFINED (free α′δ) ~97%; F_B: ILL-DEFINED (no massive extension) ~95%; overall ILL-DEFINED ~95%. Tachyon obstruction confirmed numerically ~99%.

## 7. Guard and locks
Hardened guard as in F-RHOWIDTH: `guard` inside I4, residue, L2, lowenergy_ratio, RV, gate_w; no pass flag; per-call hash + ancestry re-verification; caches keyed by origin/main sha; fetch once per process. The import test makes 2 direct calls that must both refuse before the push; before the push only `py_compile` was run.

Locked:
- `sims/fpgd/fpgd_checker.py` sha256 `6f1e171c97b91cbbae0696e04ad17352cb7623f50ba31a127f1aecc1abd1238f`
- `sims/fpgd/planted_cases.json` sha256 `210c79032eed96eb4d05976b1ff4d1c2529094139ed1b6ec3da3bf4f7845a8ee`
- `sims/fpgd/import_guard_test.py` sha256 `a183d2e9fd9c0e9184ad4d0ae8f4b7d4fee6a704d18a0fad6b85ebd01db2a0fc`
