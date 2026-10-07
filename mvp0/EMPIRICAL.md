# MVP-0 empirical check

Pre-registered with the proof, not after a fit. There is no free parameter.

## What the geometry says

For any four twistors whose consecutive angle brackets are nonzero, each edge momentum `pᵢ = xᵢ − xᵢ₊₁` satisfies `det pᵢ = 0` (`edgeMomentum_det_eq_zero`) and the four edges sum to zero (`edgeMomentum_sum_eq_zero`). In the `2 × 2` matrix model of a four-vector, that determinant is the quadratic form `t² − x² − y² − z²`. The mass defined by it is exactly zero. This is an identity, not a calibrated output.

## What is being compared

The massless case is the photon. The comparison is an inequality against published upper bounds, not agreement with a tuned central value.

Source: S. Navas et al. (Particle Data Group), Phys. Rev. D 110, 030001 (2024) and 2025 update, photon listing, `https://pdg.lbl.gov/2025/listings/rpp2025-list-photon.pdf`, page created 30 May 2025.

The limit PDG places at the head of the mass table, and the one it uses rather than the rows marked "we do not use the following data for averages, fits, limits, etc.", is

- Ryutov 2007, magnetohydrodynamics of the solar wind out to Pluto's orbit: `m_γ < 1 × 10⁻¹⁸ eV`.

Rows PDG does not use for that average include, with the assumptions in the listing's notes:

- Yan et al. 2024, JUNO data and the Jovian magnetic field: `< 2.5 × 10⁻¹⁸ eV`.
- Wang et al. 2023, fast radio bursts: `< 2.1 × 10⁻¹⁵ eV`.
- Malta and Zarro 2024, Cassini Shapiro delay: `< 4.9 × 10⁻⁷ eV`.

PDG note 11, quoting Adelberger, Dvali and Gruzinov: if the photon acquired a mass through the Higgs mechanism, the large-scale field can still look Maxwellian. The stronger galactic bound `< 1 × 10⁻²⁶ eV` assumes a Proca equation on every scale. This check does not adopt that stronger number.

## The comparison

Theory: `m = 0`.

Bound used: `m_γ < 1 × 10⁻¹⁸ eV` (Ryutov 2007, as listed by PDG for the quoted limit).

`0` lies under that bound. No parameter was adjusted to put it there. The electroweak scale is about `10¹¹ eV`, so this check says nothing about `m_W`, `m_Z`, or `m_H`. Those are not claims of MVP-0.

Passing this check means the massless identity is not in conflict with the cited bound. It does not mean the photon has been derived as a Standard Model field, and it does not constrain a nonzero mass below the bound.
