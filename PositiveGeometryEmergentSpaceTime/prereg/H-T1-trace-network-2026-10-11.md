# H-T1 pre-registration: trace entropy, Kac factor, and the electrical-network route to Gr≥0

Date: 2026-10-11 (Europe/London). Written and pushed before any H-T1 Lean or new script. Context:
a private reading note, `notes/trade-space-minimum-assumptions.md` (P-Net),
`reviews/M1b-result-2026-10-11.md` (geometric vs unitarity positivity).

## Prior art (sweep; sources read this session unless marked)

- **The conjecture, verified verbatim.** the trace-order preprint (doi:10.20944/preprints202410.1305.v1) (PDF "Version
  September 5, 2025 submitted to Entropy", traceinstitute.org), §3, just after the trace-logic paragraph: "We also
  conjecture that if P ≤t Q then the entropy rate of P is less than or equal to the entropy rate of Q." Here
  "P ≤t Q iff P is a trace of Q", and the entropy rate is −Σ μᵢ Pᵢⱼ log₂ Pᵢⱼ (their eq. 47, §6).
- **Trace / censored chain = stochastic complement.** The formula is A + B(I − D)⁻¹C (Meyer's stochastic complement;
  "censored chain", e.g. Grassmann–Taksar–Heyman; summarised in Ben Mamoun–Busic–Fourneau, CDC 2012). The
  stationary law is π|_S/π(S) **[CITED, standard]**. Kac's lemma: the mean return time to S is 1/π(S) (Kac 1947,
  *Bull. AMS* 53:1002) **[CITED]**.
- **Abramov.** h(T_A) = h(T)/μ(A) for the induced transformation (Abramov 1959, *Dokl. Akad. Nauk SSSR* 128;
  pages 873–875 per the Nagoya Math. J. reference list, while our note had "647". **To fix in the note.**) The
  entropy of absorbed or killed chains via Abramov–Rokhlin: arXiv:1910.00990 (read in summary).
- **Networks.**
  - Doyle–Snell, *Random walks and electric networks* (1984; math/0001057): reversible chain ⇔ network,
    c_xy = π_x P_xy.
  - Kron reduction = Schur complement of the Laplacian: Dörfler–Bullo 1102.2950.
  - Curtis–Ingerman–Morrow (LAA 283, 1998): response matrices of circular planar networks.
  - Kenyon–Wilson math/0608422: grove probabilities from the response matrix.
  - Lam–Pylyavskyy 1103.3475: electrical Lie groups.
  - **Lam 1402.6261** (read): ι(E_n) = X ∩ Gr(n−1, 2n)≥0, with Plücker coordinates Δ_I = Σ_{σ concordant with I}
    L_σ (grove measurements; §5.2). Example 5.1 gives the Y-network's 15 Plücker coordinates.
- **Not found:** the observation "the trace-order preprint's trace = Kron reduction = Lam's input", any refutation of the *Traces*
  conjecture, or any Lean formalisation of trace chains, Kac or Lam's map. (Mathlib has `rowStochastic`,
  `Real.negMulLog`, Schur-complement block lemmas, and no Markov-chain entropy rate.)

## Definitions (fixed now)

- Finite chain P on S ⊔ B, blocks A = P_SS, B = P_SB, C = P_BS, D = P_BB, with I − D invertible and N = (I − D)⁻¹
  ≥ 0. **Trace** Tr = A + B N C. Stationary π = (π_S, π_B).
- **Entropy rate** (nats in Lean; bits = nats / log 2): h(P, π) = Σᵢ πᵢ Σⱼ negMulLog(Pᵢⱼ). For the trace,
  h(Tr) uses π_S/π(S), so **π(S)·h(Tr) = Σ_{i∈S} πᵢ H(Tr_i)**.
- **Kac (excursion form):** E[return time to S | start ~ π_S/π(S)] = Σ_{i∈S} (πᵢ/π(S)) (1 + (B N 𝟙)ᵢ). This uses the
  standard fundamental-matrix identification (Kemeny–Snell) **[CITED]**. We prove the algebra.
- **Network:** a reversible chain has conductances c_xy = π_x P_xy and Laplacian L = diag(π)(I − P). The response
  matrix is Λ = L/L_BB (Schur complement).

## Targets

- **(a)** Exact counterexample: P on {1,2,3}, with 1→3, 2→3 and 3→1, 2 w.p. ½. π = (¼, ¼, ½), Tr on {1,2} =
  [[½,½],[½,½]], h(P) = ½ bit < 1 bit = h(Tr). In Lean: exact rationals, logs via `Real.negMulLog` and
  log 2 > 0, no native_decide.
- **(b)** General (any finite S, B; field-valued block matrices):
  - Tr is row-stochastic (and nonnegative if N ≥ 0).
  - π_S is Tr-stationary, hence so is π_S/π(S).
  - Kac: the excursion formula equals 1/π(S).
  - Commute times: the Traces §7 uniform 3-colour example, exactly (6 → 4, ratio 2/3 = π(S)). The general commute
    rescaling is CITED (commute = R_eff × volume, Chandra et al. 1989; Kron reduction preserves R_eff).
- **(c)** The correct statement, worked out before computing:
  - The sequence of S-states visited is **itself Markov with kernel Tr** (strong Markov property). So "the induced
    process is not Markov" is not the issue.
  - Abramov gives h(induced transformation on path space) = h(P)/π(S). The S-state process is a **factor** of it
    (it forgets the excursions). Hence **π(S)·h(Tr) ≤ h(P)**, with equality iff the excursions carry no extra
    entropy given the S-sequence.
  - Lean target: the **one-state elimination theorem** (|B| = 1, any |S|), proved in general by an elementary
    grouping argument. The general |B| case = iterate, using the quotient property of Schur complements
    (Crabtree–Haynsworth): CITED plus paper proof. The general Abramov route: CITED.
- **(d) stretch:** the general |B| bound in Lean.
- **(e)** Network bridge:
  - (e1) A general Schur identity: diag(π_S)(I − Tr) = L_SS − L_SB L_BB⁻¹ L_BS. This is the trace generator as the
    Kron-reduced Laplacian (response matrix). It is purely algebraic and needs no reversibility.
  - (e2) n = 2 boundary nodes: the path network 1 — 0 — 2 with conductances a, c. **With a = c it is exactly the
    counterexample chain of (a).** Lam's point in Gr(1,4) is [L₁₂ : L₁|₂ : L₁₂ : L₁|₂] = [ac : a+c : ac : a+c]. All
    Plücker coordinates are > 0 for a, c > 0, and L₁₂/L₁|₂ = the effective conductance = −Λ₁₂.
  - (e3) n = 3 (the Y/star network, Lam Ex. 5.1): an explicit 2×6 matrix whose 15 minors equal Lam's Δ's, all > 0
    for a, b, c > 0 (the top cell of X₃). The star chain's trace on the leaves gives Λ = diag(a) − aaᵀ/Σ, up to the
    normalisation 1/(2Σ).
- **Positivity type.** This is real, probability/conductance positivity (the unitarity-type side of the M1b split),
  not the continued-kinematics positivity of Gr⁺ amplitudes.

## Outcomes (fixed now)

- **PASS:** (a), (b) [general algebra; commute example], (e1), (e2), (e3) proved in Lean, and (c) proved in the
  stated scope (|B| = 1 general) with the general case honestly CITED.
- **INCONCLUSIVE:** (c) only on examples.
- **FAIL:** the counterexample does not survive exact arithmetic, or Lam's Δ's are not realisable by a 2×6 matrix
  (that would mean a transcription error on our part).
- **Not tested:** "time is the step count", "mass = entropy rate", and any Lorentz claim. They stay CONJECTURE
  whatever Lean proves.
