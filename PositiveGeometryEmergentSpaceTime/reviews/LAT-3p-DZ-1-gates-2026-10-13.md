# LAT-3′ and DZ-1 gates — 2026-10-13
**Both NOT POSABLE.** No prereg was written; no target values were read. Structure checks used digit-masked LaTeX source.

## LAT-3′ — MR-2 ππ zero at P vs Roy analyses of lattice data (m_π ≈ 391 MeV)
- **Output, not input: PASS** for 2303.02596 (extended Roy equations with a σ bound-state pole).
  - The authors state that a₀⁰, a₀², s_σ and |g_σππ| "are not taken as external inputs but correspond to the predictions".
  - Subthreshold behaviour is a Roy-equation output: driving terms come from lattice data plus Regge models.
- **Is the needed quantity published? FAIL.** P = (M², M², 2M²) needs I = 0, 1, 2 S/P/D partial waves at s = M², cos θ = 1/3 (`LatticeGate.pipi_cos_at_P`). The paper tabulates only:
  - (i) Schenk-type parameters of the solutions, valid above threshold;
  - (ii) residues;
  - (iii) partial-wave Adler-zero positions in IJ = 00, 20, compared with NNLO ChPT.
  - The subthreshold full amplitude at P appears only implicitly, through the Roy RHS. Reconstructing it needs their lattice+Regge driving terms, which are shown only as figures.
  - The partial-wave Adler zeros are a *different* observable. Their location is a ChPT prediction, not one of ours.
- **Second source:** 2304.03762 (Rodas et al., dispersed HadSpec amplitudes at 239/283 MeV). Contaminated: a search snippet showed rough Adler-zero positions. Its subthreshold section also gives figures only. **Excluded.**
- With fewer than 2 usable non-circular sources, LAT-3′ is not posable. It would become posable only if an analysis tabulated the full amplitude at subthreshold points; TS1-7 already covers that as a bet.

## DZ-1 — zero line in dispersive η→3π (Khuri–Treiman)
**Theory gate: FAIL**, on three counts, all PROVED in `PositiveGeometryEmergentSpaceTime.EtaGate` (0 sorry, standard axioms):
1. **No hidden zero of ours.** The LO isospin-breaking amplitude vanishes on s = 4M²/3. There p₊·p₋ = −M²/3 ≠ 0 (`dot_on_line`, `not_cgw`), so this is the LO Adler/Weinberg zero, **not** a CGW-type p_a·p_b = 0 line. (MR-6 already proved the CGW decay locus unphysical.) Any prediction would be LO ChPT, not our machinery. This is the same pattern as MR-5 Kη.
2. **Cuts.** Along s = 4M²/3, t + u = Mη² + 5M²/3. Since Mη² > 19M²/3, one of t, u always exceeds 4M² (`crosses_cut`), so the line runs onto the t/u-channel cuts and only Re M could vanish. The zero is not reachable cut-free.
3. **Circularity and memory.**
   - Khuri–Treiman analyses (CLLP, Kampf et al., Albaladejo–Moussallam; from memory) fix subtraction constants by matching to ChPT in the Adler-zero region, i.e. partly an input.
   - I also recall the dispersive Adler-zero position roughly (contamination).

## Status
- Credit proposal: 0. OP-2 stays 2.5/3.
- Pattern [ASSESS]: every subthreshold test now fails on publication format (full amplitude not tabulated), circularity, or ChPT overlap.
- The blind passes so far came from tabulated dispersive subthreshold *coefficients* (MR-4: C_ij). The remaining unexplored targets of that type are the ππ **subthreshold parameters** α, β, λ₁, λ₂ (CCL/GKPY tabulate them; MR-2 zero ⇒ a linear relation?). Next: theory check of MR-2 at P in terms of ππ subthreshold parameters, then a memory audit.
