# PREREG HG-DIM-2 (PERMUTO): do the hexagonal 2-faces of the permutohedron break the Ollivier–Forman link? (locked)

Authorisation: author approved (2026-10-31). CPU only, modest. AUTORESEARCH-STOP stays in place. The excluded worktrees (`<local path>`, `<local path>`) are not touched.

## 0. Why this test
HG-DIM-1 (verdict LOCAL-COUNT, review `reviews/HG-DIM-1-result-2026-10-31.md`) found that on the associahedron K_n, edge Ollivier curvature equals Forman curvature divided by D+1, edge by edge (the "Ollivier–Forman link"). My report said hexagons should break that link. This test checks that statement on the permutohedron P_n, the simplest simple polytope whose 2-faces are squares and hexagons. It is a method test (an exact, Lean-certifiable statement about a classical polytope), not a physics rung. EMC is not computed: the question was set by the author, so this is not a re-ranked rung pick.

## 1. First principles and prior art (literature check done BEFORE this lock; CITED = fetched this session)
**Object.** P_n = Cay(S_n, {s_1, …, s_{n−1}}) with s_i = (i i+1), right multiplication; N = n!, D = n − 1. Its 2-faces are the cosets w⟨s_i, s_j⟩: squares when |i − j| ≥ 2 and hexagons when |i − j| = 1. That this coset structure gives the 2-faces is a standard polytope fact; it was not fetched this session, so it is used as the definition of "2-face" here. An edge labelled i lies in n − 2 faces: h hexagons (h = 1 for the end generators s_1, s_{n−1}; h = 2 for interior generators) and c = n − 2 − h squares. Left multiplication by g ∈ S_n is a graph automorphism that preserves labels, so curvature depends only on the label. Conjugation by w0 maps label i to n − i.

**Local transport (paper derivation, not yet computed on P_n).** Take x ~ y with label i and uniform measures on closed neighbourhoods (mass 1/n). The x and y masses cancel at cost 0. For each square, its x-neighbour and y-neighbour are adjacent (cost 1). For each hexagon, the x-neighbour and y-neighbour are at distance 3: P_n is bipartite, they are not adjacent, and the only short cycles are the commuting squares. So W1 ≤ (c + 3h)/n. A matching lower bound comes from the potential f: 0 on hexagon x-neighbours, 1 on x and on square x-neighbours, 2 on y and on square y-neighbours, 3 on hexagon y-neighbours. It is 1-Lipschitz on the support and extends by McShane. Predictions:
- **P1** κ(e) = 1 − (c + 3h)/n = (2 − 2h)/n: end edges 0, interior edges −2/n.
- **P2** Forman (De Loera et al. 2510.11894 Def 1.1/1.2): P_n is simple, so there are no type-(i) parallel edges, and a k-gon contributes k − 3 type-(ii) edges. κ_F = (n − 2) + 2 − (c + 3h) = 2 − 2h: end edges 0, interior edges −2.
- **P3 (main) LINK HOLDS:** κ = κ_F/(D+1) on every edge, because a hexagon costs 3 in both pictures (transport distance 3, and 6 − 3 = 3 parallel edges). Faces with k ≥ 7 would break the link, since transport is capped at 3 while Forman charges k − 3. That claim is SPECULATION for polytopes in general. It is tested here only on the planted octagonal prism (PL5/PL8).
- **P4** Conventions: κ_{1/2} = (1 − h)/(n − 1); κ_0 = (2 − 2h)/(n − 1); κ_LLY = ((D+1)/D)·κ = (2 − 2h)/(n − 1).
- **P5** Means over edges (n!/2 edges per label): mean κ = −2(n − 3)/(n(n − 1)); mean κ_F = −2(n − 3)/(n − 1).
- **P6** Every edge has exactly h hexagons and c squares as stated, constant per label. Left-multiplication symmetry and w0-symmetry hold.

So my prediction contradicts the quoted sentence. Both outcomes are pre-registered (§3).

**Prior-art check (queries and hits logged in `/tmp/sweep/log.txt`; sources fetched).**
- CITED **Cushing, Kamtue, Kangaslampi, Liu, Münch, Peyerimhoff, arXiv:2310.15953**. Theorem 1.2: for a RACG with defining graph H, κ_LLY(s) = (4 + 2·deg_H(s))/D − 2. Example 1.5: a Coxeter Cayley graph has only even cycles, and "since our curvatures are local concepts, any cycles of length ≥ 6 do not change the curvature values", so the RACG case suffices, with H = the complement of the Coxeter diagram. For S_n, H is the commutation graph, deg_H(s_i) = c and D = n − 1. This gives κ_LLY = (4 + 2c)/(n − 1) − 2 = (2 − 2h)/(n − 1), which is P4. **The per-class LLY curvature of P_n is therefore KNOWN, as a direct specialisation of 2310.15953 (Thm 1.2 + Ex 1.5).** The paper does not write out the permutohedron or S_n (a full-text grep for "permutohedron" and "polytope" returned 0 hits). P1 then follows from Bourne et al. 1704.04398 (κ_α = (1 − α)κ_LLY on [1/(D+1), 1]), also cited in HG-DIM-1. **P1/P4 are therefore a reproduction, not a new result.** The checker includes the 2310.15953 formula as a convention cross-check.
- CITED **Cushing–Liu–Peyerimhoff, "Bakry-Émery curvature functions on graphs", arXiv:1606.01496** (Canad. J. Math. 2020): Theorem 10.7 covers the Bakry-Émery curvature of Coxeter Cayley graphs with standard generators, via the Laplacian of the Coxeter diagram. That is a vertex (Bakry-Émery) notion, not edge Ollivier curvature. Adjacent, not P1.
- CITED **Siconolfi, FPSAC 2020 extended abstract** (mat.univie.ac.at/~slc/wpapers/FPSAC2020/97-Siconolfi.pdf) and arXiv:2102.10134. The weak order graph (= P_n for type A) has Bakry-Émery/Schmuckenschläger curvature Ric = −2cos(π/|S|) for strictly linear Coxeter systems (Thm 5.1). Again a vertex notion. Adjacent.
- CITED **Peyerimhoff lecture notes** (maths.dur.ac.uk/…/peyerimhoff-lecture-notes.pdf): Example 4.2, Fig. 16 draws Cay(S_4, {(12), (23), (34)}) in the Cayley-graph/hyperbolicity section. No Ollivier value is computed for it (grep).
- CITED **Fung–Lim arXiv:2606.16530**: LLY curvature of digraphs. The appendix table for Γ(S_n, {σ1, σ2}) gives κ(e, σ1) = κ(e, σ2) = 0 for n ≥ 3. That covers only the two-generator Cayley graph, which equals P_3 = C_6 at n = 3. It recovers the RAACH formula of 2310.15953. It does not give the full P_n.
- CITED **De Loera et al. 2510.11894**: Forman definition and Lemma 2.1. No mention of the permutohedron (grep "permut": only "permutation matrix").
- arXiv API searches: abs:permutahedron AND abs:curvature → 0; abs:"adjacent transpositions" AND abs:curvature → 0; abs:"symmetric group" AND abs:"Ricci curvature" AND abs:Cayley → 0; abs:Coxeter AND abs:"Ricci curvature" → 5 (all listed above or Bruhat-order papers 2102.11277, 2103.03828).
- **Not found in this sweep:** an explicit edge-by-edge comparison of Ollivier and Forman curvature on the permutohedron (P3), and a Lean certificate. Those are the only possibly additional parts of this test. P2 is a one-line specialisation of De Loera Def 1.2 once the face structure is known, so it is credited as routine.

## 2. Memory / contamination disclosure
P1–P6 were derived on paper before any computation on P_n for n ≥ 4. Before this lock I smoke-ran the checker helpers on planted graphs only (Q_4, hexagonal and octagonal prisms, C_6, K_5, the 3-regular tree) and on the broken variants on those graphs. I also ran `census(3)` once to catch crashes; P_3 = C_6 is itself a planted control with κ = 0. No P_n with n ≥ 4 curvature was computed before the lock. The 2310.15953 formula (§1) was read before the lock and agrees with P4. That is disclosed: P1/P4 are not blind tests of a new claim. Of the gates, only P3 (the link) is the question that 2310.15953 does not state.

## 3. Object, rule, verdict (locked; `sims/hgdim2/hgdim2_checker.py`)
- Live: P_n for n = 3..8 (N = 6..40320; D = 2..7). **All edges** are computed exactly with an integer assignment (uniform closed neighbourhoods, local distance 0/1/2/3, which is exact). Forman is computed from the explicit coset 2-faces with De Loera Def 1.1/1.2 (both parallel types are counted from incidences; no closed formula is used). h and c are counted from the faces, not taken from the label.
- LP (HiGHS) cross-checks: idleness 1/(D+1), 1/2 and 0, on all edges for n ≤ 5, and on a seeded sample of 100 edges (seed 20261031 + n) plus every identity-edge representative for n = 6..8.
- Symmetry: left multiplication by every g ∈ S_n (n ≤ 6), or by 50 seeded g (n = 7, 8), preserves edges and labels. w0-conjugation maps label i to n − i.
- Gates (all edges, every n):
  - **link** = [κ(e) = κ_F(e)/(D+1)];
  - **formula** = [κ(e) = (2 − 2h(e))/n] ∧ [κ_F(e) = 2 − 2h(e)] ∧ [h, c as in P6] ∧ [constant per label] ∧ [means as in P5];
  - **conv** = [κ_{1/2} = ((D+1)/(2D))κ = (1 − h)/(n − 1)] ∧ [κ_0 = (2 − 2h)/(n − 1)] ∧ [2κ_{1/2} = ((D+1)/D)κ = (4 + 2deg_H)/D − 2 (2310.15953 Thm 1.2)] on LP edges, tolerance 1e-9.
- **Verdict** (applied by the checker only):
  - ILL-DEFINED if a planted control fails, no sizes ran, the LP disagrees with the assignment, or symmetry or regularity fails;
  - else **LINK-BREAKS** if the link gate fails anywhere (the checker reports max |κ − κ_F/(D+1)|);
  - else **LINK-HOLDS** if the formula gate passes;
  - else **LINK-HOLDS-OFF-FORM**;
  - the suffix **+CONV-MISMATCH** is added if the conv gate fails.
- Predicted: **LINK-HOLDS**. The author's quoted hypothesis corresponds to LINK-BREAKS. **Refutation of my derivation:** any edge with κ ≠ (2 − 2h)/n, κ_F ≠ 2 − 2h, or a link failure. Negative results are kept as they come.

## 4. Planted / broken / conventions
- **Planted (must pass):**
  - PL1: K_5, κ = 1.
  - PL2: C_8, κ = 0; the C_6 polygon has κ_F = 0 and the link holds.
  - PL3: Q_4, κ = 2/5 and κ_F = 2; the link holds.
  - PL4: 3-regular tree root edge, −1/2.
  - PL5: hexagonal prism: hexagon edge κ = 0, κ_F = 0; rung edge κ = 1/2, κ_F = 2. Octagonal prism: octagon edge κ = 0, κ_F = −2 (link FAILS by 1/2); rung edge 1/2, 2.
  - PL6: valid alternatives that must be accepted on P_4 and P_5: reversed edge orientation, the left-Cayley convention (same κ multiset per label), the w0 mirror i ↔ n − i, and P_3 = C_6 with κ = 0.
  - PL7: LP checks: Q_4 lazy 2/5, κ_{1/2} 1/4; K_5 κ_0 = 3/4; tree −1/2.
  - PL8: the link gate is true on the hexagonal prism and FALSE on the octagonal prism; the formula gate rejects the wrong form (2 − h)/n on P_4.
  - PL9: every verdict branch is reachable.
  - PL10: the 2310.15953 formula on Q_4 (H = K_4) gives 1/2 = κ_LLY.
- **Broken (each must fail at least one planted check):**
  - open_nbhd (supports without the centre);
  - dist_cap2 (distance 3 counted as 2);
  - no_shared (shared point costs 1);
  - hex_as_square (Forman counts every face as contributing 1 parallel edge);
  - empty (no sizes, so ILL-DEFINED).
- **Conventions:** the same as HG-DIM-1: lazy idleness 1/(D+1) uniform on closed neighbourhoods (primary); LLY = ((D+1)/D)κ (Bourne et al.); idleness-1/2 and idleness-0 LP cross-checks; and the 2310.15953 Thm 1.2 normalisation (non-normalised in their paper; for regular graphs κ_LLY is the same).
- No random-graph null: the question is an exact identity, not a separation.

## 5. Lean plan (post-live; PROVED only for Lean-checked claims)
- `lean/PositiveGeometryEmergentSpaceTime/HgDim2.lean`, Mathlib, `decide +kernel` only, 0 sorry, no native_decide, no nonstandard axioms:
  - (a) General: on `Equiv.Perm (Fin n)` with adjacency v = u * swap i (i+1), left multiplication preserves adjacency and label, for all n (vertex-transitivity per class).
  - (b) General ℚ algebra for all n ≥ 4: 1 − (c + 3h)/n = (2 − 2h)/n with c = n − 2 − h; Forman (n − 2) + 2 − (c + 3h) = 2 − 2h; the ratio identity κ = κ_F/(D+1); the LLY, κ_{1/2} and mean identities.
  - (c) decide-checked certificates (coupling walks plus a global integer 1-Lipschitz potential) for the end and interior classes at n = 4 and n = 5 (and n = 6 if memory allows), in the HG-DIM-1 style.
- The general per-class κ theorem for all n (the coupling plus potential argument) is **paper-proved** in `notes/HG-DIM-2-permutohedron-proof-2026-10-31.md`, not Lean, unless formalised.

## 6. Tags and failure modes (declared)
- Expected credit: reproduction of a KNOWN formula (2310.15953), plus the Ollivier–Forman link statement for P_n, which was not found in this sweep. The link statement is routine once both formulas are known. Failure-mode tag: FM-KNOWN (main formula known) and FM-METHOD (value is the method and Lean certificate).
- Kill: more than 45 min CPU or more than 4 GB gives PARTIAL-LIMIT and no verdict.
- Run: pinned environment (python 3.13.5, numpy 2.5.4, scipy 1.18.1), fixed seeds, manifest in `sims/hgdim2/run_manifest.txt`.

## 7. Lock
`hgdim2_checker.py` sha256 `0c1535339d9f735a1fbdc3fa2eabfc8efa2f86ab9b9a3dda09fc766f4f70f02d`
`guard.py` sha256 `c41860513c33477555ee45f7863f093737cdb4b30924d743fb4dd6cb2726f62e`
