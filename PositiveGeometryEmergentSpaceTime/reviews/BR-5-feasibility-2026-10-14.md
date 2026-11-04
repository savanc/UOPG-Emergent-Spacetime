# BR-5 feasibility gate result (2026-10-14)
Prereg: prereg/BR-5-feasibility-gate-2026-10-14.md (09062c5, pushed alone first). EW-Z1 files read only, not edited.
Read: lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean (header, N, Q1, Q2, N_decomp, zero_of_gauge), sims/ewz1b/mklean.py (lines 1–36),
lean/PositiveGeometryEmergentSpaceTime/MassiveSpinor.lean (declaration list).

- **G1 inputs:** N takes abstract Lorentz invariants (εi·εj, εi·pj), vev differences k1..k3, s, couplings a, lam3, lam4.
  It is produced by a sympy Berends–Giele build of the colour-ordered amplitude (s- and t-channel currents, contact term),
  then restricted to the hidden-zero locus (ε1·ε3 = ε1·p3 = ε3·p1 = 0, t eliminated). Positive (clear, script-defined).
- **G2 path via MassiveSpinor:** NEGATIVE. MassiveSpinor provides massive momentum decomposition (`exists_massive_decomp`,
  rank 2), little-group covariance (`br_covariant`, `br_lorentz`) and spinor brackets (`ang`, `u`), but no massive
  polarisation vectors, no ε·p/ε·ε dictionary and no vertex/current algebra. N is not written in spinor variables at all,
  so MassiveSpinor is not the natural source of N.
- **G3 cost:** a Lean derivation of N needs formal VVV, VVS, VVVV vertices and a 4-point current recursion over abstract
  dot products (a ring identity of the size of N plus the build) — new infrastructure; > 1 session.

## Verdict: **NOT-FEASIBLE** (per prereg: G2 negative)
Alternative route recorded (not run): BR-5′ — formalise the Feynman-rule build over abstract invariants (no spinors),
reproducing N by `ring`; addresses audit A-4 (script-trusted N); cost > 1 session (FEASIBLE-LONG class); it would sit
next to PositiveGeometryEmergentSpaceTime's EW-Z1 files, so it needs PositiveGeometryEmergentSpaceTime's agreement before starting.
Blocker: FRONTIER-THEORY (missing infrastructure). Reopen: massive polarisation vectors from spinors in Lean, or PositiveGeometryEmergentSpaceTime
requests BR-5′.
## Proposed credit: 0.
## Lesson: check that the target object is even expressed in the variables of the proposed bridge before scoring a graph-suggested bridge.
