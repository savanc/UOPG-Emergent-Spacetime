# HG-DIM-2 (PERMUTO) result: do the permutohedron's hexagons break the Ollivier–Forman link? (Grok, 2026-10-31; the author)

## Provenance
- Request: The author's ("Ok let's do this proof too 'The permutohedron is a natural next test, because its hexagonal faces should break the simple Ollivier–Forman link.'"). PositiveGeometryEmergentSpaceTime's steering at required a literature check before finalising; that check is done (prereg §1).
- AUTORESEARCH-STOP stayed in place.
- Base: cb7b0bc.
- Prereg **5935f37**, pushed alone and first. sha256 of the prereg file: `32d22ddf…6c202`.
- Checker, guard, import test and refusals: c26bd89. The guard refused on the unpushed prereg (CLI exit 1; import test 2/2 REFUSED, exit 2).
- Live run: **5dc0b7e**.
- Lean: 3e6bac4.
- Locked files, unchanged:
  - checker `sims/hgdim2/hgdim2_checker.py`, sha256 `0c153533…f02d`;
  - guard `c4186051…f62e`.
- Run manifest `sims/hgdim2/run_manifest.txt`:
  - run id **HGDIM2-20261031T104614**;
  - Python 3.13.5, numpy 2.5.4, scipy 1.18.1;
  - LP sample seed 20261031 + n;
  - 31.4 s wall, 319 764 kB peak RSS, CPU only.
- Output sha256 (`sims/hgdim2/result_sha256.txt`): planted ed3e863d…, broken 7256e4c6…, live 77cc2f1b….

## Verdict (locked, as is; no hand adjudication)
**LINK-HOLDS**, which was my predicted branch. SIMULATED (HGDIM2-20261031T104614).

On P_n for n = 3..8 (N = 6..40 320; **158 322 edges, all computed exactly**), every edge satisfies all of the following:
- **κ = (2 − 2h)/n**, with Forman **κ_F = 2 − 2h**;
- **κ = κ_F/(D+1)**, with **link gap max = 0** at every n;
- h is the number of hexagons, taken from the explicit coset 2-faces. h = 1 on the two end labels and h = 2 on the interior labels.

The quoted hypothesis (hexagons break the link) is **refuted on the permutohedron**. A hexagon costs 3 in both pictures: a transport distance of 3, and 6 − 3 = 3 Forman parallel edges.

| n | D | N | edges | κ end / interior | κ_F end / interior | mean κ | mean κ_F |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 6 | 6 | 0 / — | 0 / — | 0 | 0 |
| 4 | 3 | 24 | 36 | 0 / −1/2 | 0 / −2 | −1/6 | −2/3 |
| 5 | 4 | 120 | 240 | 0 / −2/5 | 0 / −2 | −1/5 | −1 |
| 6 | 5 | 720 | 1800 | 0 / −1/3 | 0 / −2 | −1/5 | −6/5 |
| 7 | 6 | 5040 | 15120 | 0 / −2/7 | 0 / −2 | −4/21 | −4/3 |
| 8 | 7 | 40320 | 141120 | 0 / −1/4 | 0 / −2 | −5/28 | −10/7 |

Gate and control results:
- **Gates.** Formula, link and conv gates pass at every n.
- **LP cross-check.** HiGHS agrees with the assignment at idleness 1/(D+1), 1/2 and 0. It ran on all edges for n ≤ 5, and on 100 seeded edges plus the identity representatives for n = 6..8.
- **Symmetry.** Left-multiplication symmetry holds for all g (n ≤ 6) or 50 seeded g (n = 7, 8). The w0 mirror holds.
- **Planted controls: ALL OK (PL1–PL10).** The octagonal prism control confirms that the link gate *can* fail: κ = 0 vs κ_F/4 = −1/2.
- **Broken variants: ALL_REJECTED.**
  - open_nbhd fails PL1/3/4/5/8/10.
  - dist_cap2 fails PL2/4/5/6/7/8.
  - no_shared fails PL1/3/5/7/8/10.
  - hex_as_square fails PL2/5/8.
  - empty gives ILL-DEFINED.
- **Conventions: CONVENTION-ROBUST.**
  - κ_{1/2} = (1 − h)/(n − 1).
  - κ_0 = κ_LLY = (2 − 2h)/(n − 1).
  - 2310.15953 Thm 1.2 is reproduced on every LP edge.

## Prior art (CITED = fetched this session; full list in prereg §1)
- **KNOWN.** The per-class κ_LLY of P_n is a direct specialisation of Cushing–Kamtue–Kangaslampi–Liu–Münch–Peyerimhoff, arXiv:2310.15953, Thm 1.2 (RACG formula) + Ex 1.5 (Coxeter Cayley graphs reduce to the RACG case). Take deg_H(s_i) = c and D = n − 1. That paper does not write out S_n or the permutohedron.
- The lazy κ then follows from the idleness linearity in Bourne et al., 1704.04398. So P1 and P4 are a **reproduction** (FM-KNOWN).
- Adjacent work, not covering P1:
  - 1606.01496 Thm 10.7 and Siconolfi FPSAC 2020 Thm 5.1 (Bakry–Émery vertex curvature of Coxeter Cayley graphs);
  - Peyerimhoff lecture notes Ex 4.2 / Fig 16 (a drawing only);
  - Fung–Lim 2606.16530 (Γ(S_n, {σ1, σ2}), κ = 0, two generators).
- De Loera et al. 2510.11894 has no permutohedron.
- **Not found in this sweep:**
  - the explicit edge-by-edge Ollivier–Forman comparison on P_n (that hexagons do *not* break it);
  - the mean closed forms;
  - a kernel-checked certificate.

  Once both formulas are known, these are routine. The additional content is the comparison and the Lean certificate, nothing more.

## Proof status (`notes/HG-DIM-2-permutohedron-proof-2026-10-31.md`)
**PROVED (Lean, 0 sorry, no native_decide, kernel `decide` only):**
- Left multiplication and S-preserving conjugation are automorphisms of right Cayley graphs on `Equiv.Perm (Fin n)`, for all n. Label transitivity also holds for all n.
- Weak duality for walk-realised matchings.
- The ℚ algebra for all n: cost → κ; the link; LLY = 2310.15953; idleness; both means.
- For **every label at n = 4, 5, 6**: the closed-neighbourhood minimum matching cost is exactly n − 2 + 2h. That gives κ = (2 − 2h)/n, certified by an explicit matching and the global inversion potential `phiInv`.

  The graph semantics are checked in Lean too: `perms_valid`, `rank_P` (injective, all n! permutations) and `nbr_spec` (neighbour k = swap of positions k, k+1). The Birkhoff and Kantorovich steps are cited, not formalised.

**PAPER-PROVED (all n):**
- the per-class κ: coupling c + 3h, plus a 1-Lipschitz inversion-indicator potential with gap c + 3h;
- Forman κ_F = 2 − 2h, from the coset faces;
- the link, and the means.

**SIMULATED:**
- everything in the table (n ≤ 8);
- κ_0.

**SPECULATION:** faces with k ≥ 7 sides break the link on general simple polytopes. Only the planted octagonal prism supports this.

## Lean counts
- New modules `PositiveGeometryEmergentSpaceTime.HgDim2` (14 thm), `HgDim2P4` (20), `HgDim2P5` (25), `HgDim2P6` (30). Total +89 theorems / +75 defs.
- Every declaration uses at most [propext, Classical.choice, Quot.sound].
- P6 builds in 258 s at about 8 GB RSS. n = 7 was not attempted, because it would need about 7× more vertices.
- AxiomsAll: TOTAL theorems=**1328** defs=**746** nonstandard=0, axiom_decls=0, opaque_decls=0, sorry_dependent=0. Before this rung it was 1239/671.

## Map change
None needed. This is a method test of a statement from my own report, not a trade-space rung, so no trade-space node was added.
- The HG-DIM-1 reading "Ollivier = Forman/(D+1)" now covers two polytope families: associahedra (squares and pentagons) and permutohedra (squares and hexagons).
- The open edge is faces with k ≥ 7 sides (SPECULATION).

## Tags
- Verdict: SIMULATED.
- Per-class κ: KNOWN (CITED 2310.15953) and reproduced. PAPER-PROVED for all n; PROVED for n = 4, 5, 6.
- Link: PAPER-PROVED for all n; SIMULATED for n ≤ 8; PROVED (κ side) for n = 4..6.
- Blocker: `REDUNDANT` (main formula known).
- Failure modes: FM-KNOWN, FM-METHOD.

## Credit
Proposal: 0. This is a reproduction of a known formula plus a routine comparison and a Lean certificate.

Reopen: a simple polytope with a k ≥ 7 face where Ollivier and Forman are both computed. Natural candidates are graph associahedra or cyclohedra with long cycles as 2-faces. Alternatively, a weighted measure on P_n. Reopen flag: not set.
