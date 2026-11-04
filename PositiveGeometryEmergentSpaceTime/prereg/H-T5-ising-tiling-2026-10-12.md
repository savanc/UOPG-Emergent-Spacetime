# H-T5 pre-registration: do Ising (OG≥0) cells tile the ABJM orthogonal momentum amplituhedron?

Date: 2026-10-12 (Europe/London). Pushed before any H-T5 computation.
Parents: H-T3 (Ising → OG≥0), H-T3b (J rule C1).

## Prior art (sweep done first; read this session)

- **Huang–Kojima–Wen–Zhang 2111.03037 (HKWZ), §§1–4.**
  - O_k := {Y = C·Λ : C ∈ OG+(k, 2k) positive branch (M_I/M_Ī = +1), Λ 2k points on the (k+2)-dim moment curve}.
  - dim O_k = n − 3. Codim-1 boundaries: the odd-particle planar Mandelstams. Sign-flip characterisation (3.14) plus
    orthogonality.
  - n = 4, 6: the amplitude is the *top cell*, so the tiling is trivial (one cell, because dim OG(3,6) = 3 = n − 3).
  - n = 8: two BCFW cells tile O₄; this was checked numerically by HKWZ.
  - Canonical form via the N=4 formalism (dlog); the N=6 version needs J.
- **Huang–Wen 1309.3252 §4.** The 8-pt BCFW cells are σ₁ = (15)(27)(36)(48) (on M₃ = 0) and σ₂ = (14)(26)(37)(58)
  (on M₁ = 0), for shift (1,2). The cyclically shifted pair (M₂ = 0, M₄ = 0) is the other contour, related by the
  residue theorem.
- **Łukowski–Moerman–Stalknecht 2112.03294.**
  - Full boundary stratification of O_k (OG forests).
  - f-vector of O₄ = (14, 28, 28, 20, 8, 1), so χ = 1 (ball-like).
- **He–Kuo–Zhang 2111.02576:** momentum amplituhedra of SYM/ABJM from twistor-string maps (abstract only).
- **Lipstein–Mason** (ABJM Grassmannian/twistor; not re-read).
- **Galashin–Pylyavskyy:** every cell of OG≥0(n, 2n) is the image of a reduced planar Ising network with
  xing(τ) edges. So *every* BCFW cell is trivially an "Ising cell".

Proved or established already (credit, not re-claimed): the n = 6 trivial tiling; the n = 8 BCFW tiling (numerical,
HKWZ); the boundary structure (LMS).

## Re-read gap

- Known before writing: everything above. In particular, the n = 8 BCFW cells are known and tile, and the label
  "Ising cell" is automatic.
- Not computed: which Ising networks give σ₁ and σ₂; whether any other pairs of 5-dim cells tile; injectivity at
  n = 6 in Ising charts; any canonical-form check.

## Setup

- Λ: moment curve, x_i = i, (k+2)-dim.
- Cells are parametrised by reduced Ising networks with GP's map, couplings J > 0.
- Membership of Y in a cell's image: multi-start least squares on C(J)·Λ·Y⊥ = 0 with J > 0. "Contained" means
  residual < 1e-10 with all couplings in (1e-4, 20).
- Only the positive branch: GP's OG = {Δ_I = Δ_Ī} is HKWZ's positive branch. The negative branch is not used, and a
  sign check is reported.

## Targets and criteria

**(a) n = 6 (k = 3).** Over 40 sampled Y from Y-network points:
- (i) the sign-flip conditions hold (⟨Y i i+1⟩ > 0 with the twisted last bracket as in HKWZ, and 3 flips of ⟨Y 1 j⟩);
- (ii) injectivity: exactly one positive Ising preimage, from 30 starts each;
- (iii) the Y and Δ networks give the same image (the same top cell).

Coverage is tautological, because O₃ is defined as the image of the top cell. This is stated, not tested.
**PASS:** (i)–(iii) hold on all samples.

**(b) n = 8 (k = 4).**
- Enumerate all 5-crossing matchings of [8] (5-dim cells) and realise each by an Ising network obtained from the
  H-T3b top networks N1, N2, N3 by one deletion (J → 0) or one contraction (J → ∞, at a non-boundary–boundary edge).
- Check that each image is 5-dim (Jacobian rank).
- Test **every pair** for tiling: each of 200 top-cell sample points lies in exactly one cell of the pair.
- **PASS:** at least one pair tiles, and the tiling pairs include HW's {σ₁, σ₂} or its cyclic shift.
- **FAIL:** no pair tiles. That would contradict HKWZ, so it would be treated as a method problem: **INCONCLUSIVE**.

**(c) Canonical form (spurious-pole check, n = 8).** The tile form is carrier × J_C1, pushed forward to a fixed
5-coordinate chart of Y-space, signed so it is positive inside its own tile and continued through the unique real
preimage. Along a path crossing the internal wall of the tiling pair, as the path approaches the wall:
- **PASS:** |Ω_A + Ω_B| stays bounded while |Ω_A|, |Ω_B| grow like 1/d.
- **FAIL:** the sum diverges like the parts.
- **INCONCLUSIVE:** the preimage continuation fails (degree > 1 or a complex preimage).

Not attempted: comparison with the full 6- and 8-pt superamplitudes. At 6-pt the form is the top-cell pushforward
already covered by H-T3/H-T3b and HKWZ (CITED).

**(d) The mission question: is the tiling Ising-natural?** Hypothesis H_KW, fixed now: every tiling pair is
{G with J_e → 0, G with J_e → ∞} for a single edge e of a single reduced top network G. These are the high- and
low-temperature (Kramers–Wannier-dual) limits of one coupling.
- **PASS** ("Ising-natural selection rule"): H_KW holds for every tiling pair found.
- **FAIL** ("BCFW imported"): some tiling pair has no such realisation, or the pairs selected by H_KW include
  non-tiling ones. The second clause matters because H_KW must *select* tilings, not just be compatible with them.
- Report the fraction of H_KW pairs that tile.
