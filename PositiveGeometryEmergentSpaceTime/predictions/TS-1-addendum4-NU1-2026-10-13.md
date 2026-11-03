# TS-1 addendum 4 — NU-1 neutrino mixing entries (registered 2026-10-13)

Separate file so existing TS-1 hashes are unchanged. TS-1 rules and **TS-1 cap** apply (per-entry credit ≤ 0.25 as REMEMBERED/PATTERN-GIVEN unless the author grants up to 0.5 for a pattern that beats the rival; total NU-1 ≤ 0.5). SHA256 in `TS-1-addendum4-NU1-2026-10-13.sha256`.

## Disclosure (contamination)
- JUNO 207-day result arXiv:2609.37895 (Sept 2026: sin²θ₁₂ = 0.3036 ± 0.0064, Δm²₂₁ = 7.388e-5 eV²) and JUNO 2511.14593 **were seen** during the out-of-box scan. They do **not** score. Global-fit, DESI DR2 and KATRIN values are remembered from training.
- **Only results whose first public version (arXiv v1 / collaboration release) postdates this commit score.**
- The patterns (TM1, TM2, GR1, GR2) are textbook [CITED, memory]; they are not derived from our geometry. Claim tag: **PATTERN-GIVEN / PRE-REGISTERED**, not DERIVED.

## Inputs (fixed now)
s₁₃² ≡ sin²θ₁₃ is taken from the **same future release** if it quotes it, else 0.0222 (band 0.0215–0.0229). φ = (1+√5)/2. Tree level, no RG running.

## Entries
| ID | Pattern | Formula | Prediction | Pass band |
|---|---|---|---|---|
| TS1-NU1a | TM1 (TBM 1st column kept) | sin²θ₁₂ = (1−3s₁₃²)/(3(1−s₁₃²)); cos δ = −(1−5s₁₃²)cot2θ₂₃ / (2√2 s₁₃ √(1−3s₁₃²)) | sin²θ₁₂ = 0.318 (0.3177–0.3187); δ ≈ ±90° if θ₂₃ maximal | sin²θ₁₂ within 2σ_exp of 0.318 |
| TS1-NU1b | TM2 (2nd column kept) | sin²θ₁₂ = 1/(3(1−s₁₃²)) | 0.341 (0.3407–0.3411) | within 2σ_exp |
| TS1-NU1c | GR1 golden ratio | tan θ₁₂ = 1/φ ⇒ sin²θ₁₂ = 1/(1+φ²) | 0.2764 | within 2σ_exp |
| TS1-NU1d | GR2 golden ratio | cos θ₁₂ = φ/2 ⇒ sin²θ₁₂ = 1 − φ²/4 | 0.3455 | within 2σ_exp |
| TS1-NU1e | Positive-geometry motivated (μ–τ reflection, real-positive residual symmetry) | θ₂₃ = 45°, δ_CP = ±90° | sin²θ₂₃ = 0.500; \|sin δ\| = 1 | sin²θ₂₃ within 2σ of 0.5 **and** δ within 2σ of 270° (or 90°) in next NOvA/T2K/JUNO+global release |
| TS1-NU1f | Scale no-go consequence (geometry fixes no scale) | Normal ordering, lightest m ≈ 0 ⇒ Σm_ν = √Δm²₂₁ + √Δm²₃₁ | Σm_ν ≈ 0.059 eV; NO | next DESI / KATRIN: 95% bound not below 0.059 eV *and* no KATRIN detection (m_β > 0.3 eV); fails if IO preferred > 3σ |

σ_exp = total uncertainty quoted by the scoring release.

## Rival baseline (pre-registered)
Global-fit central values (NuFIT-6.x class, remembered): sin²θ₁₂ = 0.307, sin²θ₂₃ ≈ 0.47–0.56 (octant open), sin²θ₁₃ = 0.0222, δ_CP ≈ 180–230° (NO), Σm_ν ≥ 0.059 eV. A pattern scores only if it passes its band **and** its |pull| is ≤ the rival's |pull| on the same quantity; otherwise PASS-NO-CREDIT.

## Scoring rule
1. First qualifying release after this commit per entry; no shopping among releases.
2. PASS (band + beats rival) → up to cap; PASS-NO-CREDIT; FAIL (>2σ) → 0 and pattern marked REFUTED-PREREG. Expected: TM2, GR1, GR2 likely fail given seen data (stated now).
3. Credit decision is the author's.
