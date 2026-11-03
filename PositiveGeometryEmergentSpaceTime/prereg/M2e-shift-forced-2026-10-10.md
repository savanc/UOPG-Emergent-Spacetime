# Pre-registration: M2e, is the δ-shift forced at n = 6?

Date: 2026-10-10 (Europe/London). Committed **before** any M2e computation, Lean or figure.
Rules as before. Builds on M2d (`lean/PositiveGeometryEmergentSpaceTime/NLSM.lean`).

## 0. Prior art (papers and Lean). Read 2026-10-10 before writing this file; extended by amendment A1 below

- **[H] arXiv:2312.16282 §7.1, "Uniqueness of kinematical shift"** already proves (informally, for all n) that
  the shift is the **unique shift preserving every non-planar c_ij**. Their argument: fix the shifts of the
  ray triangulation X_{1,i}; c-preservation forces δ_{1,e} = 0 and all δ_{1,o} equal; that common value is
  nonzero only for even n. The condition there is "keep all hidden zeros/factorisations", **not** the physical
  conditions below. [CITED]
- **[N] arXiv:2401.05483** calls the shift "unique" in its abstract (referring to [H] §7.1). §IV notes that
  for mixed amplitudes, imposing 2m skinny-rectangle zeros "suffices to force all the shifts". [CITED]
- **[AF] arXiv:2403.04826 §3** shows why the *relative minus sign* between (e,e) and (o,o) shifts is needed to
  match the Catalan representation of the NLSM. It does not state a uniqueness theorem for shifts from
  physical conditions. [CITED]
- **Rodina, arXiv:1612.06342**: the NLSM amplitude itself is unique given locality, unitarity-compatible poles
  and the Adler zero. This is a statement about amplitudes, not shifts. [CITED]
- So M2e asks a **different question** from [H] §7.1. Do the physical conditions (finite limit at pion scaling,
  only even-point poles, Adler zero) force the shift? I have not found this statement proved in the literature.
  If it turns out to be there, it gets cited and M2e becomes a re-proof.

## 1. Search space (the ansatz, itself an assumption)

- Hexagon planar variables: the 9 chords X13, X14, X15, X24, X25, X26, X35, X36, X46. The adjacent
  X_{i,i+1} = 0 stay zero (massless on-shell legs; not shifted).
- Shift: **X_ij → X_ij + δ·a_ij**, with constants a ∈ ℝ⁹ (or ℂ⁹ for the algebra), and δ → +∞.
- Symmetry: a ↦ λa with λ > 0 is absorbed by δ ↦ δ/λ, and λ < 0 is δ → −δ. Under δ⁴ scaling, L ↦ λ⁻⁴ L, so
  solutions form lines through 0 (punctured).
- Canonical a*: a_ee = +1 (X24, X26, X46), a_oo = −1 (X13, X15, X35), a_oe = 0 (X14, X25, X36).
  The mirror −a* equals a* rotated by one label (i → i+1 swaps e ↔ o).
- Caveat stated in advance: linear, δ-uniform shifts of planar X's are an ansatz. Non-linear shifts, shifts of
  the adjacent s_{i,i+1}, different δ-powers per chord, or deformations other than shifts are **not** searched.

## 2. Conditions

- **C1(k).** For generic X, δ^k · A6(X + δa) → L(X) as δ → +∞, with L ≢ 0. **Primary k = 4** (= 2n − 2 at
  2n = 6, the [N] eq. 2 scaling, which gives L mass dimension +1 like a 6-pion amplitude). A secondary scan over
  k = 0…6 is reported, not graded.
- **C2 (only even-point poles).** L has no pole at any X_ij with j − i even: X13, X15, X24, X26, X35, X46.
  These are the (e,e)/(o,o) chords, i.e. 2|4 channels whose sub-amplitudes would be 3- and 5-point. Poles
  are allowed only at X14, X25, X36 (3|3 channels). *Correction to the brief: it listed X13 etc. as "j − i
  odd"; they have j − i = 2 or 4, even. The forbidden chords are the ones the brief named, with the parity
  label fixed.*
- **C3 (Adler zero, all 6 legs).** For each leg i, the soft map from M2d (X_{i,j} → X_{i+1,j} for all j,
  X_{i−1,i+1} → 0) sends L to 0 identically. Variant **C3′**: leg 1 only (reported).
- **C4 (cyclic symmetry).** Not imposed. Reported only if needed.

## 3. Method

Write ε = 1/δ and b_ij = 1/a_ij on the support S = {a_ij ≠ 0}. Each diagram contributes
Π_{unshifted} 1/X · Π_{shifted} ε b (1 − ε b X + …). So A6 = Σ_m ε^m C_m, with C_m homogeneous of degree m in b.
For each of the 2⁹ = 512 supports S: C1(k) ⇔ C_0 = … = C_{k−1} ≡ 0 and C_k ≢ 0. Clearing the unshifted
denominators turns each "≡ 0 in X" into polynomial equations in b. C2 ⇔ for each forbidden unshifted chord f,
the numerator vanishes at X_f = 0. C3 ⇔ the numerator of the soft image vanishes. Solve with Gröbner bases
(sympy, exact rationals), with b ≠ 0 enforced by a Rabinowitsch variable. Enumerate every solution, then
cross-check each one numerically at random rational X with large δ.

## 4. Lean targets

- (L1) **Converse**: a* satisfies C1(4), C2, C3. From M2d: `shift6_limit` + `nlsm6_zero/adler` + the pole
  structure of A6N.
- (L2) **Algebraic uniqueness**: the polynomial conditions the script derives (stated as explicit hypotheses)
  ⇒ a = λ a*. If deriving those conditions from the limit inside Lean is too heavy, I will say plainly that the
  reduction C1–C3 → polynomial system is **script-verified** and only the algebra is Lean-proved.

## 5. Pass / partial / fail

- **PASS**: the full scan finds exactly the line {λa* : λ ≠ 0} for C1(4) + C2 + C3, and (L1) and (L2) are
  proved in Lean with standard axioms.
- **PARTIAL**: uniqueness holds only with extra assumptions (C4, a restricted support, all legs needed vs not,
  etc.; stated which), or the Lean part covers only some supports.
- **FAIL**: other solutions exist. They are exhibited, checked numerically and reported as a finding.
- Also reported: whether C2 or C3 alone suffices, and which conditions do the work.

## 6. What a PASS would mean (in advance)

Within linear shifts, the pion shift is not a free choice. It is forced by "finite at pion scaling, even-point
poles only, Adler zero". That removes one input rule from M2d's chain, but the ansatz remains, and so do the
conditions themselves. The Adler zero is the defining property of Goldstone bosons, so "pions from geometry"
would become "pions = the unique Adler-zero deformation of the associahedron's form within linear shifts".
That is not a derivation from nothing.

## Amendment A1 (2026-10-10,): prior-art sweep extended under the new standing rule

Committed **before any M2e result exists**. A first scan run was interrupted after ~1 min with no output; no
solution set has been seen.

**Papers (physics).**
- **Cheung, Kampf, Novotný, Shen, Trnka, *A Periodic Table of Effective Field Theories*, arXiv:1611.03137**
  (title and authors checked). The soft bootstrap shows that NLSM, DBI and the special Galileon are fixed by
  their soft degree (σ = 1 for NLSM, i.e. the Adler zero), valency and power counting; such EFTs sit on the
  boundary of theory space. [CITED]
- **Rodina, arXiv:1612.06342** (with Arkani-Hamed, Rodina, Trnka, arXiv:1612.02797): tree NLSM amplitudes are
  fixed by locality plus the Adler zero (on n−1 legs). [CITED]
- **ABHY arXiv:1711.09102 §9.1**: the NLSM scattering form is "entirely fixed" by power counting, the Adler
  zero and projectivity. [CITED]
- [H] §7.1, [N], [AF]: see §0.

**Consequence for what is new.** The literature already implies that any L passing C1(4)+C2+C3 with local
cubic-graph pole structure is c·A6^NLSM, because the *amplitude* is unique by the soft bootstrap. That part
is **prior art**, not ours. [H] §7.1 already proves that the shift is unique *among c-preserving shifts*.
**What M2e claims as new** (modest): within the linear-shift ansatz, the *shift vector a* is forced by
C1(4)+C2+C3 alone, without assuming c-preservation, plus a machine-checked classification over all 512
supports at n = 6, and Lean proofs. If a reference is found that already does this, the claim reduces to
"independent re-derivation + formalisation".

**Lean formalisations.** In Mathlib v4.34.1 and Physlib (a4ef461), at our pins, a grep for associahedron,
sigma model, Adler and amplitude finds nothing relevant. A web search found no Lean/Coq/Isabelle
formalisation of the associahedron canonical form, NLSM amplitudes or the δ-shift. Our own M2c/M2d files
are the only Lean base. Reused: `PositiveGeometryEmergentSpaceTime.NLSM.*` (M2d) for the converse direction.
