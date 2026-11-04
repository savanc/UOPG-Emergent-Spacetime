# TS-1 addendum — TS1-8 (registered 2026-10-13)
Separate file, so existing TS-1 hashes are unchanged. Same scoring rules as `TS-1-2026-10-13.md` §rules, unless overridden here.

## TS1-8 — MR-4 πK I=3/2 zero line, Adler zero left FREE
- **Motivation:** LAT-2 gate (`reviews/LAT-2-gate-2026-10-13.md`). Existing lattice I=3/2 πK fits (Dawid et al. 2502.17976) fix the s-wave Adler zero at z² = 1, i.e. *on* our line, so testing them would be circular.
- **Prediction:** a fit that leaves the zero free will place it on, or near, the line, and the full amplitude will be small there.
- **Eligible sources:**
  - Any lattice I=3/2 πK (π⁺K⁺) analysis whose first arXiv version postdates this commit, and which publishes, for at least one ensemble with M_π > 200 MeV or the physical point:
    - an s-wave parametrisation with the Adler-zero position **fitted** (z² free, e.g. "ADLER-z"), or a form with no imposed zero (K-matrix/ERE with ≥ 2 terms, or Chew–Mandelstam);
    - the p-wave if fitted;
    - the ensemble's M_π and M_K.
  - Fits with z² fixed are ineligible.
- **Inputs (declared per ensemble, no fit):** the ensemble's M_π, M_K, and the published fit parameters with their covariance (diagonal if none is given, disclosed).
- **Observables:**
  1. **Primary:** z²_fit vs the prediction z² = 1, i.e. s_A = M_π² + M_K² (LO ChPT and the MR-4 line coincide here; PROVED `PiKZero.lo_zero_on_line`).
  2. **Secondary:** r = RMS_{τ∈[0,4]} |T^{3/2}(s = Σ, t)| / RMS_box |T^{3/2}|.
     - Use the fitted waves (s + p) continued to s = Σ, which lies inside the threshold-expansion disc: `LatticeGate.inside_disc`.
     - Restrict the box to s ≥ M_K² − M_π², the source's validity domain.
- **Bands:**
  - Primary: |z² − 1| ≤ 1/3 within 2σ (i.e. |z² − 1| − 2σ ≤ 1/3).
  - Secondary: r − 2σ_r ≤ 1/3, as in the MR-4 prereg.
- **Null:**
  - Primary: z² ~ U[0, 2] (the range over which an s-wave zero lies between the left-hand circle and threshold, in units of Σ). The null pass fraction is f = 1/3. Across N independent ensembles, f compounds as ∏ f_i, and the result counts as discriminating if ∏ f ≤ 0.3. One ensemble alone is not discriminating.
  - Secondary: the MR-4 random-line null, compounded.
- **Scoring:**
  - PASS = primary and secondary pass on ≥ 2 independent sources (different collaborations or actions), and the compounded null ≤ 0.3.
  - One source = INCONCLUSIVE. A primary fail on ≥ 2 sources = FAIL.
- **Credit:** 0.5 max, shared with TS1-6 (it is the same zero; it is not added to it). The author decides.
- **Blindness:** no free-z² πK lattice value is known to me. Dawid et al. state that "fits with additional parameters do not improve p-values and are not shown" (structure only, digits masked).
