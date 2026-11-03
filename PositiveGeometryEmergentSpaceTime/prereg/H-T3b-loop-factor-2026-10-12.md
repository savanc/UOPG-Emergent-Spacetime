# H-T3b pre-registration: the ABJM loop factor J in Ising variables (exact n = 3, rule test at n = 4)

Date: 2026-10-12 (Europe/London). Pushed before any H-T3b computation. Parent: `reviews/H-T3-result-2026-10-11.md`.

## Prior-art check (done first) and narrowing of H-T3's claim

Sources and what they already contain:
- **HWX 1402.1479 §2.4.2** (re-read 2026-10-12, eqs. 2.22–2.59):
  - a *general combinatorial rule* for the Jacobian J of any medial graph: J = 1 + J1 + J2 + J3 + J13 + J23, with:
    - J1: single closed loops and products of disjoint loops;
    - J2: loops sharing one vertex, the shared vertex's weight omitted;
    - J3: loops sharing two vertices without an edge;
    - each loop's weight is a product of c's (anticlockwise) or s's (clockwise);
  - worked examples: (2.27), (2.28), (2.32);
  - **the triangle-move identity (2.55):**
    (1 + c₁c₂c₃) Π dlog tan θ = (1 + s′₁s′₂s′₃) Π dlog tan θ′, under their map (2.54). They state it was "straightforward
    to show"; no proof is printed.
- **Huang–Kojima–Wen–Zhang 2111.03037:** the 6-pt N=6 Jacobian prefactor is (1 + c₁c₂c₃).
- **Galashin–Pylyavskyy §9** (2018/2020) lists HWX's Jacobian in Ising language as open. Their medial weights are
  s = sech 2J, c = tanh 2J (eq. 5.1).
- Searched without finding a 2019–2026 paper that writes HWX's J in Ising couplings:
  - Henriques–Speyer (cube recurrence), Kenyon–Pemantle (hexahedron recurrence; Ising double-dimers), Lam's surveys;
  - "Ising model ABJM" searches.
  - Absence of evidence only.

**Narrowing H-T3.**
- H-T3's n = 3 factors (J_Y = 1 + Π sech 2L, J_Δ = 1 + Π tanh 2K) and its star–triangle Jacobian identity are
  **HWX's single-loop J and their eq. (2.55)**, rewritten through GP's dictionary. They are **not new as mathematics**.
- What remains ours:
  - (i) the explicit Ising-coupling form;
  - (ii) an independent derivation from Lee's measure (coarea, not HWX's gluing rules);
  - (iii) the KW consistency;
  - (iv) any exact proof (HWX print none).
- The H-T3 review will be corrected accordingly.

## Re-read gap

**Known before writing:**
- the numerical n = 3 results (H-T3);
- HWX's rules and examples;
- the structural guess that vertex-type closed medial faces (around interior Ising vertices) carry s = sech 2J and
  face-type closed medial faces (interior Ising faces) carry c = tanh 2J. This is consistent with the n = 3 data and
  with KW duality swapping them.

**Not yet computed:** anything symbolic at n = 3; anything at n = 4 (k = 4).

## Conventions (same as H-T3)

- GP map, η = diag(+, −, …).
- Lee's measure in gauge **G2** (odd columns = I), minors M_j…M_{j+k−1} for j = 1 and j = 2.
- Carrier ω_I = Π_e dlog sinh 2J_e.
- R := Ω_A/ω_I. J := R · 2^k (normalised so that J = 1 for a network without closed medial faces, as at k = 2).

## Targets

**(a) Symbolic n = 3 (sympy, exact rational functions of t = tanh L).** Lee's measure in G2 is computed via the
Maurer–Cartan form of the O(η) block. This is exact; no coarea square roots. Prove three things exactly:
1. R_Y = ⅛(1 + Π sech 2L_i).
2. R_Δ = ⅛(1 + Π tanh 2K_ij).
3. The star–triangle identity, as a rational identity in the Δ couplings u = tanh K (t_i² = m_ij m_ik / m_jk):
   det(∂ log sinh 2K/∂ log sinh 2L) = −J_Y/J_Δ.
   - Proved via the implicit-function form det(∂m_Y/∂t)/det(∂m_Δ/∂u) × the dlog factors, with odd powers of t
     eliminated through P² = m₁₂m₁₃m₂₃.

PASS: all three simplify to identities. FAIL: any doesn't.

**(b) Lean.** At least the star–triangle identity of (a)3, as a polynomial or rational identity in u after clearing
denominators. If Lee's-measure derivation (1, 2) is too heavy for Lean, say so and prove the cleanly stated
sub-identities instead. No sorry, native_decide or custom axioms.

**(c) General-n rule, fixed now.** Network data:
- **Closed medial faces:** one per interior Ising vertex v (type V, weight w = Π_{e∋v} sech 2J_e) and one per bounded
  Ising face f not touching the boundary circle (type F, weight w = Π_{e∈∂f} tanh 2J_e).
- **Adjacency:** two closed faces are edge-adjacent if they share a medial edge (a V-face and an F-face with a common
  Ising edge-pair). They are vertex-touching if they are opposite at one medial crossing (same type, sharing exactly
  one Ising edge e as a corner).

Candidates:
- **C1 (HWX translated; primary).**
  J = Σ_S Π_{F∈S} Π_{e∈corners(F), e not shared within S} w_e.
  - S runs over collections of closed faces with no two edge-adjacent.
  - Corners shared by two faces of S are omitted.
  - This is HWX's J1 + J2. J3-type configurations (two faces sharing two corners without an edge) are not expected
    at n = 4; if one occurs it is reported.
- **C2 (variant):** the same sum but with plain products, so a shared corner's weight appears squared.
- **C3:** Π_F (1 + w_F).

**(d) Blind test at n = 4 (k = 4, 8-pt).** Top-cell reduced networks (6 edges, 3 closed medial faces):
- **N1** (H-T2 top): 12, 23, 1c, 2c, 3c, 4c. Faces: V_c, F_{12c}, F_{23c}. F_{12c} and F_{23c} touch at 2c.
  - C1: J = 1 + s₁c s₂c s₃c s₄c + c₁₂c₁c c₂c + c₂₃c₂c c₃c + c₁₂c₁c c₂₃c₃c.
- **N2** (Δ→Y of N1 at triangle 12c): 1d, 2d, dc, c3, c4, 23. Faces: V_d, V_c, F_{2dc3}. V_d and V_c touch at dc.
  - C1: J = 1 + s₁d s₂d s_dc + s_dc s_c3 s_c4 + c₂d c_dc c_c3 c₂₃ + s₁d s₂d s_c3 s_c4.
- **N3:** a third reduced network obtained from N2 by Y→Δ at c; its faces are listed by the script before
  evaluation.
- Numerics: 40-digit coarea (H-T3 method), ≥ 4 random coupling points each, j = 1 and j = 2.
- Consistency (convention-independent): N1, N2 and N3 tuned to the same OG point (by matching correlations) must give
  the same Ω_A.

Verdicts:
- **PASS:** C1 matches J on every network and point to ≥ 15 digits. This confirms the HWX rule in Ising variables at
  k = 4; it is *not new* beyond the translation.
- **PASS-variant:** C2 or C3 matches instead of C1. That would flag a discrepancy with HWX's printed rule (or with
  my translation) and is reported as such.
- **FAIL:** none matches. Any post-hoc fit is labelled exploratory.
- **INCONCLUSIVE:** the consistency check fails (numerical or convention problem).
