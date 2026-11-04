# FRONTIER-1: frontier fermion/strange ranking + MR-1f-η gate — 2026-10-13
No target values were read. No prereg was written because the gate failed before any data step.

## Prior-art sweep (2025–26)
- CITED Zhang–Zhu 2609.06552: fermionic hidden zeros for **massless adjoint** fermions + gluons (D = 4, 6, 10), plus gravitino/EYM extensions. There are no hadronic (πN, baryon) loci.
- CITED 2610.01775 (Oct 2026): exact splittings and five new zero families for Tr φ³ and NLSM. Bosonic only.
- CITED Wan–Zhou 2605.11084: analytic dual bootstrap that uniquely fixes Veneziano. Bosonic four-point only.
- CITED 2011.07944 (ππ S-matrix bootstrap with Adler zeros): ππ only.
- Old prior art: πN dual/Veneziano duality classes (late 1960s–70s); Pasupathy–Singh (Adler zero ⇔ trajectory splitting in dual pion models).
- **No 2025–26 baryon dual amplitude with an Adler zero was found, and no πN hidden-zero locus.**

## Ranking (how posable it is × how plausible a blind target is)
1. **MR-1f-η** (K*_J → Kη via UnequalLS). Theory almost exists. Targets (K*_J → Kη BRs) are partly remembered, with about 1–2 sources (LASS, PDG). Ranked best, so we ran it.
2. **MR-7′** (Born-subtracted πN zero, ν = 0 / Cheng–Dashen). Posable, but it is standard current algebra, and the σ-term/subthreshold values are remembered. Capped at 0.25 under the SM rule.
3. **MR-5** (η-channel zeros). Its theory already failed (πη constant at LO; Kη not of CGW form). Nothing new found in the 2025–26 literature.
4. **MR-8** (baryon dual amplitude). No theory exists, even in 2025–26.
5. **FZ line** (FZ-2). The theorems are for massless adjoint fermions only; no hadronic target.

## MR-1f-η gate: FAIL (theory/well-posedness)
- **PROVED** (`PositiveGeometryEmergentSpaceTime.KEtaGate`, 3 thms, 0 sorry, standard axioms only):
  - `su_zero_line`: the K* su-dual zero of Kη→Kη sits at t = 2m_η².
  - `dual_ne_chiral`: this zero never coincides with the LO ChPT zero t₀ = (6m_η² + 2m_π²)/9.
  - `chiral_on_dual`: on the dual line, the LO amplitude is 12m_η² − 2m_π² > 0.
- **SIMULATED** (`sims/mr1feta/gate.py`, masses only): t_dual = 0.600 GeV² vs t₀ = 0.205 GeV². On the dual line, the LO amplitude is −1.94 × its t = 0 value.
- **Reading:** the unequal-LS amplitude that worked for πK (where the dual zero is the MR-4 line) has **no Adler-consistent zero in the η channel**.
  - Repairing it needs a t-channel ηη → f/f′ term with a free coupling and the η–η′ mixing angle. Both are fitted inputs, so the rung is not zero-fit.
  - The targets would also be remembered (K₃* → Kη sizeable) and have fewer than 2 independent sources.
- **Blocker tags:** `FRONTIER-THEORY` `CONTAMINATED`. **Reopen when** a dual Kη amplitude exists whose Adler zero is fixed by geometry (e.g. a 2610.01775-type splitting zero for unequal masses).

## Credit
**None proposed.** OP-2 stays at 3.5/3 (2.5 blind + 1.0 remembered-but-verified).

## Next rung
Every frontier rung is now theory-blocked. The cheapest theory step is **FT-1**: look for an unequal-mass NLSM splitting zero (the 2610.01775 mechanism) whose locus lands on a Kη or πη line. It is pure theory plus Lean, and if it succeeds it reopens MR-5 and MR-1f-η. Alternative: MR-7′, as a capped 0.25 confirmation.
