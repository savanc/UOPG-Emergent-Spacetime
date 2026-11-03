# Deep review: everything to date against the milestone (2026-10-13)
Tags: PROVED (Lean, 0 sorry, std axioms), SIMULATED, CITED, CONJECTURE, SPECULATION. Written from the repo's own reviews; numbers are quoted from them, not recomputed.

## 0. Milestone
- **Original M6:** one SM particle's dimensionless property within PDG error, zero fitted parameters, full chain checked. **Not met.**
- **Operational OP-2:** from {m_ρ, m_π, f_π}, ≥ 3 independent pre-registered zero-fit dimensionless predictions. **Official 1.5/3**: MR-1b blind = 1, MR-2 non-blind = 0.5. MR-2d/MR-2d1 add nothing independent (same zero; see §2).
- Honest blind count: **1**.

## 1. Lean base (PROVED)
- **450 theorems in 35 modules, 0 `sorry`.**
- Every theorem was checked per module with `#print axioms`, and all depend only on {propext, Classical.choice, Quot.sound} (`lean/AXIOMS-PER-MODULE-2026-10-13.txt`). `lake build` is green.
- The three "sorry" grep hits (IsingLoop, IsingOG, OrderParameter) are comments only.
- Largest modules: LECRatio 40, SliceBridge 36, Associahedron 25, MassiveSpinor 23, NLSM 23, MarkovTrace 22, MassShift 22, KerrMinimal 21.
- **Caveat:** most theorems are finite algebra, kinematics or certificates. The physics bridges (amplitude = data, map LEC → amplitude) are SIMULATED or CITED, not PROVED.

## 2. Results by strength
| Rung | Verdict | Blind? | Null / discrimination | New vs reproduction |
|---|---|---|---|---|
| M0–M1 | PASS | n/a | maths | reproduction (Klein, Hermitian signature) |
| M2 (l̄2 ≥ 27/20) | PASS | no | z = 7.2 but a QFT-axiom bound | reproduction |
| M2b–M2c | PASS | n/a | maths | reproduction formalised (EFT-hedron, associahedron) |
| M2d–M2f | PASS | partial | LO a0⁰ −28% | reproduction (2401.05483, CGW); structure s−M² forced, values input |
| M2e | PASS within ansatz | n/a | – | modest new (forcing within linear δ ansatz) |
| **M3** (L3/L2 = −2) | **FAIL** | yes | 3.8σ vs BE14 NNLO; NLO passes | reproduction ray; a genuine discriminating miss |
| M3w/M3c/M1b | CONDITIONAL / WRONG-SIDE / NO-GO | – | – | M1b no-go is new-ish (PROVED): positivity lives on continued kinematics |
| H-T1 | PASS | – | exact | **new**: *Traces* §3 entropy conjecture refuted exactly |
| H-T2/H-T3/H-T3b/H-T5* | mixed PASS/FAIL | – | certified samples | mostly reproduction (Lam, GP, HWX, Perlstein–Tessler) in Ising language; Lean certificates new as formalisation |
| MR-1 | PASS | no | band ≥14% needed | reproduction (AHRV) |
| **MR-1b** (ρ3, f4 ratios 5/16, 49/240) | **PASS** | **yes (couplings)** | \|z\| ≤ 1.2 in 36–42% 1/N_c bands | prediction from LS (prior art: LS 1969, AHRV); wide bands = weak–moderate |
| MR-1c, MR-1d, MR-2b, NL9, MR-3, MR-2c | WELL-POSEDNESS FAIL | – | – | honest stops |
| MR-3b (KSRF-type) | FAIL ×π | no | – | known |
| **MR-2** (massive zero at P, SU(2) two-loop) | PASS | no | f = 0.35 | new framing; physics is standard ChPT (ℓ3-small) |
| MR-2d (SU(3) tree) | weak PASS | no | f 0.09–0.51 | new combination Z (SIMULATED derivation) |
| MR-2d1 (one-loop, μ-indep.) | PASS | no | f_NDA 0.25 / 0.31; refits 0.06–0.08 | consistency firm-up of MR-2; **not independent** |
| OP-1 | PASS | – | maths | undercut by Percacci 1991 |
| OP-2 | PASS (no-go) | – | maths | new as formal statement (scale no-go) |
| BH-1/BH-2 | PASS | – | formalisation | reproduction (AHH, Guevara–Ochirov–Vines etc.) |
| MG2-0/MG2-1 | sweep / reproduction PASS | – | 3e−14 vs control 0.17 | reproduction (CGW) |
| Anomalies synthesis | survey | – | – | context only, from CITED + [memory] |

**Independence:** MR-2, MR-2d and MR-2d1 test one zero, A(M²,M²,2M²) = 0, through different LEC routes. Together they are at most one non-blind observable (0.5). MR-1b's two couplings come from one LS amplitude and count as one.

## 3. What is genuinely new
- PROVED/SIMULATED claims a referee might count as new:
  - H-T1 entropy-conjecture refutation.
  - M1b no-go.
  - Massive-zero framing of A(P) ≈ 0 in the physical ππ amplitude, with the SU(3) combination Z = 4(2L1+L2+L3)+16(2L6−L4)+8(2L8−L5) and its one-loop μ-independent form.
  - OP-2 scale no-go as a theorem.
  - A large Lean corpus formalising known results.
- **No new zero-parameter physical number** has been confirmed that was not already implicit in LS or ChPT.

## 4. Structural bottlenecks
1. **Scale gap (OP-2, PROVED):** stabiliser and orbit data are scale-invariant, so one dimensionful unit must be input. Fine, and built into OP-2.
2. **Symmetry-breaking input (MR-3, PROVED within minimal LS):** positivity forces m_π = 0. The quark mass, and by extension g′/g and λ in MG2, is an input geometry does not supply. Cross-sector ratios are blocked.
3. **Blindness exhaustion:** the low-energy ππ/LEC sector is thoroughly known from memory (MR-2 family is non-blind by construction). The blind route that worked (MR-1b) used resonance couplings whose values were not memorised.
4. **Data posability:** many targets have only "seen" listings, unevaluable formats (NL9), or are untabulated (MR-2b, MR-2c).
5. **Prior-art density:** most PASSes are reproductions. Novelty needs either new data classes or open theory questions (e.g. CGW's open non-uniform spurion question).

## 5. Ranked next actions (toward ≥ 3 blind)
| # | Action | Well-posedness | Blindness feasibility | Est. P(+1 blind) | Notes |
|---|---|---|---|---|---|
| 1 | **MR-1e**: LS leading-trajectory couplings for spin 5 / 6 (ρ5(2350), f6(2510)) → ππ, ratio to ρ, blind; gate on PDG listing structure first (headers only) | medium: PDG may list BR(ππ) only as "seen", as in MR-1d | **high**: values not memorised | ~0.25 | same LS model as MR-1b; distinct observables. CONJECTURE that bands stay ≤ 45% |
| 2 | **MR-4**: πK massive hidden zero with unequal-mass spurion (CGW open question). Derive the locus at tree level (Lean + sympy), then compare blind with the Roy–Steiner πK amplitude / subthreshold parameters (Büttiker–Descotes-Genon–Moussallam 2004) | low–medium: zero may not exist for non-uniform masses (CGW say open) | high: πK subthreshold values not memorised | ~0.15 | **highest novelty**: new theory plus new data class |
| 3 | MR-1f: LS ratios in other channels (K* trajectory couplings Kπ, SU(3)-flavoured LS) | medium | medium–high | ~0.15 | needs flavoured LS (prior art: AHRV extensions?) |
| 4 | Lattice-blind route: a Z-like condition involving only L4, L5, L6, L8 (e.g. a different zero point or a scalar form factor zero) vs FLAG Table 25 (still unread) | low (MR-2c showed kinematic LECs enter) | high (FLAG values unread) | ~0.08 | keep FLAG unread as a reserve |
| 5 | MG2-2: hidden zeros with a fundamental Higgs | theory only | – | 0 now | no data path until g′/g, λ addressed |
| 6 | H-T/Ising, BH-3, Physlib PR | – | – | 0 | value as formalisation/outreach, not OP-2 |

## 6. Recommendation
**Top action: MR-1e gate (prior-art + PDG listing-structure check, headers only, no values) for ρ5(2350)/f6(2510) → ππ.** It has the highest expected blind credit at low cost, and it reuses `PositiveGeometryEmergentSpaceTime.LSResidue`.
- Stop rule: if the ππ branching fractions are not quantitatively listed by ≥ 2 sources, switch immediately to the MR-4 gate (πK unequal-mass zero, tree-level derivation first). That is the best novelty bet.
- Keep FLAG 2019 Table 25 values unread as a blind reserve.
- Do not count MR-2d1 toward OP-2 beyond MR-2's 0.5.
