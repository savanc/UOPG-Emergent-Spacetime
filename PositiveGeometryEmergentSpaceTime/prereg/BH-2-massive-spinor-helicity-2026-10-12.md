# BH-2 pre-registration: massive spinor helicity, SU(2) little group, x-factor, minimal-coupling power counting

Date 2026-10-12 (Europe/London). Written and committed BEFORE `lean/PositiveGeometryEmergentSpaceTime/MassiveSpinor.lean` and
`scripts/bh2_massive_spinor_check.py` exist. Builds on BH-1 (`PositiveGeometryEmergentSpaceTime.KerrMinimal`) and M1 (`PositiveGeometryEmergentSpaceTime.Spinor`).

## 0. Prior art (read today unless marked)
- Arkani-Hamed–Huang–Huang 1709.04891 (AHH), fetched: p_{αα̇} = λ^I_α λ̃_{α̇I}, det λ · det λ̃ = m² (eq. 13–14),
  SL(2)/SU(2) little group λ→Wλ, λ̃→W⁻¹λ̃; equal-mass x-factor x λ3 = p1 λ̃3 / m (eq. 61), ζ-independence (eq. 62),
  x has +1 little-group weight; 2S+1 structures g_i x^{h} ... (eq. 63); minimal coupling = pure x·ε structure
  (eq. 66–67, §4.3), defined by best high-energy behaviour.
- Ochirov 1802.06730, fetched: conventions, det λ = det λ̃ = m (eq. 12), ⟨p^a p^b⟩ = −m ε^{ab} (eq. 15), explicit
  helicity parametrisation (eq. 16).
- Chung–Huang–Kim–Lee 1812.08752 (CHKL), fetched: general 3-pt (mx)^h Σ_a g_a ε^{2s−a}(x λ3λ3/m)^a (eq. 18, 23);
  subleading g_a carry extra 1/m^a and match higher-derivative couplings in the UV; minimal = g_0 only (eq. 42).
- Tooby-Smith 2411.07667 (HepLean/Physlib index notation), fetched: Weyl reps of SL(2,C) formalised; spinor-helicity
  listed as future work. Physlib repo front page checked; no massive spinor-helicity module found by one search
  (not exhaustive). Physlib not importable here (different Lean/Mathlib pin; same as OP-1/BH-1).

## 1. Well-posedness / method fitness (gate)
Everything below is finite-dimensional 2×2 complex linear algebra: formalisable on a CPU with Mathlib in hours.
Faithfulness caveat fixed in advance: we encode spinors as 2×2 matrices Λ (row α, column I) and use one explicit
ε = !![0,1;−1,0]; index heights/sign conventions are ours (consistent with Ochirov up to overall signs) — results are
stated convention-independently where possible (covariance, determinants, existence, weights).
Target (d) is NOT the full tensor-structure uniqueness of AHH/CHKL (which needs symmetric SL(2) tensor reps).
It is posed as a scalarised power-counting statement: the CHKL basis term a carries m^{-a}; the amplitude
Σ_a g_a c_a m^{-a} (c_a ≠ 0 fixed kinematic factors) stays bounded as m→0 iff g_a = 0 for all a ≥ 1.
This is a faithful model of the "best high-energy behaviour" criterion, not of the tensor algebra.

## 2. Lean targets (fixed now)
 (a) For any complex 2×2 p with det p = m² (m ≠ 0) there exist Λ, Λ̃ with p = Λ Λ̃ᵀ, det Λ = det Λ̃ = m; p has rank 2.
     Real case: p Hermitian with p00 > 0 and det p = m², m > 0 (positive-definite / future timelike) ⇒ explicit
     Λ (lower-triangular) with p = Λ Λᴴ, det Λ = m.
 (b) Little group: (Λ, Λ̃) ↦ (Λ W, Λ̃ W⁻ᵀ), W ∈ SL(2,C) preserves p and both determinants; for W ∈ SU(2) the reality
     condition Λ̃ = conj Λ is preserved. Brackets ⟨1 2⟩ := Λ1ᵀ ε Λ2 transform covariantly W1ᵀ ⟨12⟩ W2;
     ⟨1 1⟩ = det Λ1 · ε (the AHH/Ochirov ⟨p^I p^J⟩ ∝ m ε^{IJ}); SL(2,C) Lorentz action on α is an invariance.
 (c) x-factor: for det p1 = m² ≠ 0 and null k = λ3 λ̃3ᵀ, the equal-mass condition det(p1+k) = det p1 is equivalent to
     ⟨3|p1|3] = 0; under it there is a unique x with p1 ε λ̃3 = m x λ3 (λ3 ≠ 0); ζ-formula
     x = ⟨ζ| p1 ε λ̃3⟩ / (m ⟨ζ 3⟩) for every ζ with ⟨ζ 3⟩ ≠ 0; weight: (λ3, λ̃3) ↦ (tλ3, t⁻¹λ̃3) gives x ↦ t⁻² x
     (so x^h carries helicity weight h in BH-1's convention).
 (d) OPTIONAL: scalarised minimal-coupling uniqueness as in §1. If not cheap, OPEN (no sorry counted).
Script (SIMULATED, exact sympy, non-blind): random rational/Gaussian-rational kinematics: decomposition, SL(2)
covariance, x existence/ζ-independence/weight, and power counting of the CHKL basis.
PASS: (a)–(c) build, standard axioms only, 0 sorry, and script exact agreement. FAIL: any of (a)–(c) not faithfully
statable or unprovable within the session. (d) status reported separately.
Blindness: none (textbook kinematics). Novelty claimed: only the Lean formalisation, if no prior Lean version found.
