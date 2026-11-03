# Trade-space addendum: pilot-wave (de Broglie–Bohm) foundations rungs (2026-10-28)

*Written 2026-10-28 by Grok. Docs only. No prereg, no rung, no locked checker ran.*
*Source of the request: The author (pilot-wave question) and: "Add to the trade space sure and plan for the future."*

This note **adds** to notes/TRADE-SPACE-2026-10-28.md and notes/TRADE-SPACE-EXPANSION-2026-10-28.md. It edits neither file, and
nothing earlier is superseded. Base commit: origin/main 14a922c.

Tags: **PROVED** (Lean in repo, or "by hand" for a one-line fact); **SIMULATED** (script + run id); **CITED** (source
fetched this session, link below); **CONJECTURE**; **SPECULATION**; **DRAFT** (proposal text, *not* a prereg).

## 0. Status and gating

| Node | Status | Gate |
|---|---|---|
| PW-3 CANON-BORN | PLANNED / PROPOSED, **NOT RUN** | The author's go; scheduled **after** AutoResearch's 3-rung run and CASCADE-1b r2 grade + push |
| PW-1 BELL-EQ | PLANNED / PROPOSED, **NOT RUN** | same; uses the 1-in-3 known-outcome slot |
| PW-2 BELL-RELAX | PLANNED / PROPOSED, **NOT RUN** | same; companion to PW-1 |

Rank: **PW-3 > PW-1 > PW-2.** Each needs its own prereg, pushed alone with the guard refusing before the push, under
MISSION frontier mode. Nothing below is a prediction on record until that happens.

**Basin label.** the author's request called this basin "B6 foundations". The labels B6–B10 are already *proposed* by
AutoResearch in notes/TRADE-SPACE-EXPANSION-2026-10-28.md (B6 = Lie-type total positivity). To avoid a collision this note
uses **B11 foundations (quantum foundations / pilot-wave)**. Renumbering is the author's call. B11 is not yet in
`scripts/blocker_tags.py` BASIN, because it has no run rungs.

## 1. Analysis summary (from the 2026-10-28 pilot-wave analysis)

**What "carrier" means here.** It is the invariant dlog measure on a cell (Ising or conductance variables), with the kinematic
push-forward as the "modulation". It was never a wave.
- The origin note (notes/carrier-bundles-weinstein-2026-10-11.md, c4d9863) says the analogy has no time, frequency or
  signal, and that Y–Δ invariance is a redundancy, closer to gauge than to stability [SPECULATION, recorded then].
- **H-T3** (e584206): ABJM 4-point measure = Ising carrier exactly; the 6-point measure needs the loop factor J [SIMULATED].
  `IsingOG.ratio_eq_inv_sinh` and `kw_inverts` [PROVED].
- **H-T5f** (prereg 448fa71, review ac62e8d): pure carrier = tile form FAILED at n = 8, 10 [SIMULATED, prereg verdict].
- **H-T5g** (b67a6c2): Ω_tile = 2^{n−5} · carrier · J_V at n = 8, 10, to ≥ 20 digits [SIMULATED].

**Structural comparison.**
- **Wave.** Bohm's ψ is on configuration space and evolves in time. Ours is a canonical form on kinematic space, with no time
  and no Hilbert space.
- **Particle.** Bohm has a definite position. We have none: a point Y in the amplituhedron is external kinematic data, not a
  hidden state.
- **Guide.** Bohm's v = ∇S/m is dynamical. Our analogue, the kinematic map Z, is fixed [SPECULATION].
- **Invariant measure.** Both have one, of different kinds. Bohm's |ψ|² is carried along by the dynamics (equivariance). Our
  carrier is unchanged under re-description (Y–Δ, square moves) [SPECULATION].
- **Positivity ≠ Born positivity.** The segment's canonical function (b−a)/((x−a)(b−x)) is positive on (a,b) but its integral
  diverges logarithmically at both ends [PROVED by hand]. This is the seed of PW-3.
- **No trajectories in the amplituhedron.** The bridge runs the other way: Bohmian scattering theory derives cross-sections
  and S-matrix statistics from trajectories at large distance [CITED: S6, S7]. So a pilot wave would sit underneath an
  amplitude, not inside it [SPECULATION].
- **Lorentz tension.** Relativistic Bohmian theories need a preferred foliation, or one determined by ψ [CITED: S5]. Bohm and
  Hiley say only the statistics are Lorentz invariant for many particles [CITED: S9, ch. 12 preview]. Amplitudes are
  manifestly Lorentz invariant.
- **Best hook: Bell-type QFT.** It is a |Ψ|²-distributed Markov jump process on a discrete configuration space [CITED: S4].
  H-T1 put Markov / trace data onto positive Grassmannian points [PROVED, repo]. Markov processes are the shared
  language [SPECULATION].
- **Implicate / explicate vs geometry-first.** M1b's no-go (positivity lives on continued kinematics, not real (1,3)
  spacetime) is the one concrete sense in which our structure is "enfolded" [SPECULATION].
- **Valentini non-equilibrium.** This is the only pilot-wave variant that predicts beyond QM: a CMB large-scale power
  deficit [CITED: S3]. It goes beyond established QM, so it is **context, never a gate** (MISSION frontier rule).

**Candid view.** Pilot-wave theory reproduces QM statistics by construction, so it supplies no SM quantum numbers,
couplings or ratios. A Bohmian layer under the amplituhedron would also need a preferred foliation that amplitudes do not
have. B11 is therefore **foundations / method value, not a mission route**. Expected SM map change is ≈ 0 [CONJECTURE]. The
one framework-relevant output is PW-3: it separates amplitude positivity from probability positivity.

## 2. Exploratory toy checks: run PWX-2026-10-28-r1 [SIMULATED, exploratory, not a rung]

- Script: `sims/pw-explore/pw_explore.py`; output `sims/pw-explore/pw_explore_output.json`.
- Seeds: A = 1, B = 7. numpy 2.5.4, Python 3.13.5. Under 3 s CPU, negligible memory. No prereg, no verdict.

**A. Bell equivariance.** Bell's rates σ_ij = max(0, 2 Im(ψ̄_i H_ij ψ_j))/|ψ_j|² reproduce d|ψ|²/dt. The largest residual over
200 random Hermitian systems (n = 2..7) is **4.4·10⁻¹⁶** [SIMULATED PWX-2026-10-28-r1].

**B. Relaxation.** n = 12, uniform ρ₀, random superposition. D(ρ‖|ψ|²) falls from 0.761 to about 5·10⁻⁷ by t = 4, then sits at
a floor of about 10⁻⁶ that is not monotone [SIMULATED PWX-2026-10-28-r1].
- At dt/4 the floor drops by about 16× (to roughly 3–10·10⁻⁸). That is consistent with an explicit-Euler artefact
  (D quadratic in an O(dt) error), not with physics [CONJECTURE].
- Lesson for PW-2: use an exact per-step propagator for ρ, e.g. expm of the generator, or RK4 with a planted dt check.

## 3. DRAFT rung cards (DRAFT, not a prereg; numbers are proposals)

### PW-3 CANON-BORN (Lean + exact). Rank 1. Basin B11 (Lean side also B4).
- **Statement (DRAFT).** For a segment, and for the 2-simplex, the canonical function is positive on the interior and
  **not integrable** there. Hence no normalised probability density on a positive geometry equals its own canonical function.
- **Prediction.** PROVED in Lean with 0 sorry and standard axioms.
- **Refutation / kill.** A Lean counter-proof (integrability) would refute it, which would be very surprising: the 1/(x−a)
  divergence is elementary [PROVED by hand, segment].
- **Fallback.** If the 2-simplex measure-theory plumbing exceeds the budget, record LIMIT with the segment only.
- **Planted.** The integrable control (x−a)(b−x) must be accepted; 1/(x−a) on (a,b) must be rejected.
- **Feasibility.** 2–4 theorems, about 1 session. Mathlib has interval-integrability lemmas for 1/(x−a) (exact names
  unchecked) [CONJECTURE]. Build in minutes.
- **One target.** A clean structural no-go; no dimensionless number.
- **Diversity.** Distance about 3 from JORD-1 / SURF-1' / CASCADE (it shares only "canonical form"). Known outcome: **yes**
  (elementary).
- **EXCLUSION.** Placeholder `PW3.canon_not_born` (see the ledger).

### PW-1 BELL-EQ (Lean). Rank 2. Basin B11 (Lean side also B4). Uses the 1-in-3 known-outcome slot.
- **Statement (DRAFT).** For finite n, Hermitian H and ψ with all ψ_j ≠ 0, Bell's generator satisfies
  Σ_j (σ_ij|ψ_j|² − σ_ji|ψ_i|²) = d|ψ_i|²/dt (equivariance).
- **Corollary.** For any column-stochastic K, D(Kρ‖Kp) ≤ D(ρ‖p) (data processing: a fine-grained, discrete subquantum
  H-theorem).
- **No-go.** If Hψ = Eψ, every current J_ij = 0, so ρ ≠ |ψ|² never relaxes.
- **Prediction.** All three PROVED, 0 sorry.
- **Refutation.** Any counterexample (A/B above make one very unlikely).
- **Planted.** Real ψ (currents vanish); a 2-level analytic case.
- **Feasibility.** Finset sums over ℂ: about 6–10 theorems, 1–2 sessions. Whether Mathlib's KL-divergence API fits is
  [CONJECTURE]; the fallback is to prove the log-sum inequality directly. Build in minutes, CPU only.
- **Diversity.** Distance 4 (new basin). Known outcome: **yes** (Bell 1986 via S4).
- **EXCLUSION.** Placeholder `PW1.bell_equivariant`.

### PW-2 BELL-RELAX census (simulation). Rank 3. Basin B11. Companion to PW-1.
- **One dimensionless target.** f = the fraction of N = 1000 random instances (n = 4..16, GUE-like H, random superposition
  with ≥ 2 energies, ρ₀ uniform, fixed seed) with D(ρ_t‖|ψ_t|²) < 10⁻⁸ at t·‖H‖ = 50.
- **Prediction (DRAFT).** f ≥ 0.99 [CONJECTURE].
- **Refutation.** f < 0.99, i.e. more than 1% plateau above 10⁻³, with the integrator check passing.
- **Planted cases.**
  - Eigenstate: D must stay constant.
  - Block-diagonal H: D must plateau at the block-weight mismatch D_block (known in closed form).
  - Real ψ: zero current.
  - **Integrator check:** halving dt must change the final D by < 10⁻¹⁰ (motivated by PWX-r1 B).
- **Feasibility.** About 1000 × 5·10⁴ steps × n² ≤ 256, roughly 20–40 CPU-min, under 100 MB, CPU only. Kill limit per
  instance 60 s; overall 2 h.
- **Gate.** Binds to established QM only (equivariance). Valentini cosmology is context.
- **Diversity.** Distance 4. Known outcome: **partly** (relaxation is expected for a stochastic process; the census
  fraction is not known).
- **Anti-numerology.** Not applicable (no SM number). This is a structural census.

## 4. Schedule and what is *not* done
1. Now: nothing runs. AutoResearch's 3-rung window (; SURF-1' is rung 2/3 at 14a922c) and CASCADE-1b r2 (pid 32017,
   prereg 9b1dca2) finish first.
2. After both, and only on the author's go: PW-3 prereg (pushed alone), then the run, review and Lean. Then PW-1, then PW-2.
3. Not done here: no prereg, no checker, no Lean file, no blocker-index rows. The blocker index records run rungs only;
   planned rungs live in the EXCLUSION "Proposed rows" table, which follows the existing convention.

## 5. Sources fetched this session (2026-10-28; arXiv API / Crossref / publisher page)
- S1. D. Bohm, *A Suggested Interpretation of the Quantum Theory in Terms of "Hidden" Variables. I*, Phys. Rev. 85, 166 (1952), https://doi.org/10.1103/PhysRev.85.166 ; *II*, 85, 180, https://doi.org/10.1103/PhysRev.85.180
- S2. Dürr, Goldstein, Zanghì, *Quantum Equilibrium and the Origin of Absolute Uncertainty*, J. Stat. Phys. 67, 843 (1992), https://arxiv.org/abs/quant-ph/0308039
- S3. Valentini, *Signal-locality, uncertainty, and the subquantum H-theorem I*, Phys. Lett. A 156 (1991), https://doi.org/10.1016/0375-9601(91)90116-P ; Valentini–Westman, *Dynamical Origin of Quantum Probabilities*, https://arxiv.org/abs/quant-ph/0403034 ; Valentini, *Inflationary Cosmology as a Probe of Primordial Quantum Mechanics*, PRD 82, 063513, https://arxiv.org/abs/0805.0163
- S4. Dürr, Goldstein, Tumulka, Zanghì, *Bell-Type Quantum Field Theories*, J. Phys. A 38, R1 (2005), https://arxiv.org/abs/quant-ph/0407116
- S5. Dürr, Goldstein, Norsen, Struyve, Zanghì, *Can Bohmian mechanics be made relativistic?*, Proc. R. Soc. A 470, 20130699 (2014), https://arxiv.org/abs/1307.1714
- S6. Dürr, Goldstein, Teufel, Zanghì, *Scattering theory from microscopic first principles*, Physica A 279 (2000), https://arxiv.org/abs/quant-ph/0001032
- S7. Dürr, Goldstein, Moser, Zanghì, *A microscopic derivation of the quantum mechanical formal scattering cross section*, CMP 266 (2006), https://arxiv.org/abs/quant-ph/0509010
- S8. arXiv search (amplituhedron OR "positive geometry") AND (Bohmian OR pilot-wave OR "hidden variable" OR "de Broglie"): **0 results**. No prior link between pilot-wave theory and positive geometry was found.
- S9. Bohm & Hiley, *The Undivided Universe* (Routledge, 1993), https://doi.org/10.4324/9780203980385 (chapter 12 summary read from the publisher preview).
