# BH-1 pre-registration: Kerr black hole as the minimal spinor structure

Date 2026-10-12 (Europe/London). Written and committed BEFORE `lean/PositiveGeometryEmergentSpaceTime/KerrMinimal.lean` and
`scripts/bh1_kerr_multipoles.py` exist.

## 0. Claim and what is NOT claimed
Physics claim (CITED, not ours, not proved here): the massive spin-s three-point amplitude minimally coupled to a
graviton, M3 = x^{±2} <12>^{2s}/m^{2s-2} (Arkani-Hamed–Huang–Huang 1709.04891 §4.3, eq. 67 and graviton analogue),
in the classical limit s→∞, ħ→0, ħs fixed, exponentiates, (1 ± q·s/(2sm))^{2s} → exp(±q·a)
(Arkani-Hamed–Huang–O'Connell 1906.10100 eq. 24; Guevara–Ochirov–Vines 1812.06895 eqs. 39–44), and reproduces the
linearized Kerr stress tensor / multipoles M_ℓ + iS_ℓ = m(ia)^ℓ (Vines 1709.06016 eq. 1; Hansen 1974, Geroch 1970;
Chung–Huang–Kim–Lee 1812.08752 §4: Wilson coefficients C_{S^n}=1 at s≫1; Levi–Steinhoff for the EFT coefficients
— cited from memory, not re-read today). Higher-spin Compton beyond S^4 is NOT fixed by minimal coupling alone
(Bautista–Guevara–Kavanagh–Vines 2212.07965; CHKL §5 contact-term ambiguity for s>2). BH-1 does NOT test GR.

## 1. Well-posedness / method fitness (gate)
Reusable machinery (read today): `PositiveGeometryEmergentSpaceTime.Spinor` (Hermitian 2×2 ≅ R^{1,3}, det = η), `PositiveGeometryEmergentSpaceTime.Lorentz`
(SL(2,C) → restricted Lorentz), `PositiveGeometryEmergentSpaceTime.Null` (det = 0 Hermitian ⇔ ±outer product), `PositiveGeometryEmergentSpaceTime.LightCone`
(lightlike ⇔ rank one). No massive spinor-helicity or little-group objects exist yet; Physlib has Lorentz/Weyl
but no spinor-helicity (Tooby-Smith 2411.07667 lists it as future work).
Lean targets (fixed now):
 (a) massless little group: λλ̃ᵀ invariant under (λ,λ̃)→(tλ,t⁻¹λ̃); for real momenta (λ̃ = λ*) the phase t=e^{iθ}
     leaves outerH invariant; a function homogeneous of weight w in (λ,λ̃) fixes helicity weights — stated as a
     homogeneity lemma for the minimal x^h·(bracket)^{2s} monomial.
 (b) exponentiation: (1 + y/n)^n → exp y (n→∞), complex y; finite-n coefficient C(n,ℓ)/n^ℓ → 1/ℓ!; coefficient is
     0 for ℓ>n (spin-s carries multipoles only up to ℓ = 2s, nilpotency, GOV eq. 41).
 (c) Kerr sequence: ℓ!·[z^ℓ] exp(i a z) = (ia)^ℓ; Re/Im split: M_ℓ = m·Re(ia)^ℓ, S_ℓ = m·Im(ia)^ℓ, odd mass and even
     current multipoles vanish, M_2 = −m a² (sign of Hansen/Thorne quadrupole).
 (d) minimal-coupling uniqueness (lowest x-power / only g0 ≠ 0): OPTIONAL; attempt only if cheap, else OPEN.
Script (SIMULATED, non-blind; textbook result): (i) exact rational coefficients of (1+y/n)^n vs 1/ℓ! for n=2s up to
s=200; (ii) independent check: Ernst potential of Kerr on the symmetry axis, ξ(z) = 1/(z − m − ...)? — use the
known axis form ξ = m/(z + i a) in Fodor–Hoenselaers–Perjés normalisation (ξ̃ = Σ m_ℓ z^{-ℓ-1}), expand in 1/z with
sympy, and compare m_ℓ = m(ia)^ℓ... (the axis data of Kerr is ε(z)=1−2m/(z+ia) [Ernst], ξ=(1−ε)/(1+ε)); FHP says for
leading order the axis coefficients equal the Geroch–Hansen moments only up to ℓ ≤ 3, so the comparison is (ii-a)
directly for the axis coefficients of ξ = m/(z − ... ) and (ii-b) for M_ℓ via FHP up to ℓ = 10 if implementable.
PASS: all Lean targets (a)–(c) build with standard axioms only, 0 sorry; script agreement exact (rational/symbolic).
FAIL: any (a)–(c) target cannot be stated faithfully with Mathlib + M1 machinery, or script disagrees.
Blindness: NONE (textbook). Novelty claimed: only the Lean formalisation, if no prior Lean version is found.
