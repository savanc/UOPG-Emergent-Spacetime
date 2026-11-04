/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.EWZ1b
/-!
# BR-5′: Feynman-rule construction of `EWZ1b.N` (closes audit A-4 for `EWZ1b.N`)

Lean transcription of the rules in `sims/ewz1b/ewz1b.py` (CGW 2601.16860 §VI.2 setup), over abstract invariants.
A vector is its coefficients on the basis `p1 p2 p3 e1 e2 e3 e4` (indices 0–6) plus a 5th (Higgs-direction)
component. The Gram matrix is on the hidden-zero locus (`ee13 = e1p3 = e3p1 = 0`), with `t` eliminated through
`u − m₁² − m₃² = 2 k1 k3`. Vertices:
- VVV (`lam3`) and VVS (`a`) in the cyclic three-vertex current `J`;
- VSS (`gs`), kept for fidelity;
- VVVV contact (`lam4`; `b` for VVSS).

The amplitude is assembled from the s- and t-channel currents plus the contact term, times both propagators.
`built_eq_N` proves that this equals the script-generated `EWZ1b.N`. Lean checks the algebra from the transcribed
rules, not that the rules are CGW's 5D-YM reduction (CITED).
-/
namespace PositiveGeometryEmergentSpaceTime.BR5p

/-- Abstract invariants (couplings, masses = vev differences, `s`, polarisation products). -/
structure Inv where
  /-- VVS coupling (Higgs/Goldstone–W–W per unit mass) -/
  a : ℚ
  /-- ε1·p2 -/
  e1p2 : ℚ
  /-- ε2·p1 -/
  e2p1 : ℚ
  /-- ε2·p3 -/
  e2p3 : ℚ
  /-- ε3·p2 -/
  e3p2 : ℚ
  /-- ε4·p1 -/
  e4p1 : ℚ
  /-- ε4·p2 -/
  e4p2 : ℚ
  /-- ε1·ε2 -/
  ee12 : ℚ
  /-- ε1·ε4 -/
  ee14 : ℚ
  /-- ε2·ε3 -/
  ee23 : ℚ
  /-- ε2·ε4 -/
  ee24 : ℚ
  /-- ε3·ε4 -/
  ee34 : ℚ
  /-- vev difference (mass) of leg 1 -/
  k1 : ℚ
  /-- vev difference (mass) of leg 2 -/
  k2 : ℚ
  /-- vev difference (mass) of leg 3 -/
  k3 : ℚ
  /-- VVV coupling -/
  lam3 : ℚ
  /-- VVVV coupling -/
  lam4 : ℚ
  /-- s-channel invariant -/
  s : ℚ
  /-- VSS coupling -/
  gs : ℚ
  /-- VVSS coupling -/
  b : ℚ

/-- A vector: basis coefficients (p1 p2 p3 e1 e2 e3 e4) and 5th component. -/
structure Vec where
  /-- coefficients on p1 p2 p3 e1 e2 e3 e4 -/
  c : Fin 7 → ℚ
  /-- 5th (Higgs-direction) component -/
  f : ℚ

namespace Vec
/-- Sum. -/
def add (X Y : Vec) : Vec := ⟨fun i => X.c i + Y.c i, X.f + Y.f⟩
/-- Scalar multiple. -/
def smul (r : ℚ) (X : Vec) : Vec := ⟨fun i => r * X.c i, r * X.f⟩
/-- Negation. -/
def neg (X : Vec) : Vec := smul (-1) X
/-- 4D part only. -/
def d4 (X : Vec) : Vec := ⟨X.c, 0⟩
/-- 5th part only. -/
def d5 (X : Vec) : Vec := ⟨fun _ => 0, X.f⟩
end Vec

/-- `t` on the hidden-zero locus: from `u = k1² + k3² + 2 k1 k3`. -/
def tz (x : Inv) : ℚ :=
  x.k1^2 + x.k2^2 + x.k3^2 + (x.k1 + x.k2 + x.k3)^2 - x.s - (x.k1^2 + x.k3^2 + 2*x.k1*x.k3)

/-- Gram matrix of the basis on the hidden-zero locus. -/
def gram (x : Inv) : Fin 7 → Fin 7 → ℚ := fun i j =>
  let M : Fin 7 → Fin 7 → ℚ := ![
    ![x.k1^2, (x.s - x.k1^2 - x.k2^2)/2, x.k1*x.k3, 0, x.e2p1, 0, x.e4p1],
    ![(x.s - x.k1^2 - x.k2^2)/2, x.k2^2, (tz x - x.k2^2 - x.k3^2)/2, x.e1p2, 0, x.e3p2, x.e4p2],
    ![x.k1*x.k3, (tz x - x.k2^2 - x.k3^2)/2, x.k3^2, 0, x.e2p3, 0, -x.e4p1 - x.e4p2],
    ![0, x.e1p2, 0, 0, x.ee12, 0, x.ee14],
    ![x.e2p1, 0, x.e2p3, x.ee12, 0, x.ee23, x.ee24],
    ![0, x.e3p2, 0, 0, x.ee23, 0, x.ee34],
    ![x.e4p1, x.e4p2, -x.e4p1 - x.e4p2, x.ee14, x.ee24, x.ee34, 0]]
  M i j

/-- 4D dot product. -/
def dot4 (x : Inv) (X Y : Vec) : ℚ := ∑ i, ∑ j, X.c i * Y.c j * gram x i j
/-- Explicit bilinear form of `dot4` (49 Gram entries, zeros dropped). -/
theorem dot4_explicit (x : Inv) (X Y : Vec) : dot4 x X Y =
    X.c 0 * Y.c 0 * (x.k1^2)
    + X.c 0 * Y.c 1 * ((x.s - x.k1^2 - x.k2^2)/2)
    + X.c 0 * Y.c 2 * (x.k1*x.k3)
    + X.c 0 * Y.c 4 * (x.e2p1)
    + X.c 0 * Y.c 6 * (x.e4p1)
    + X.c 1 * Y.c 0 * ((x.s - x.k1^2 - x.k2^2)/2)
    + X.c 1 * Y.c 1 * (x.k2^2)
    + X.c 1 * Y.c 2 * ((tz x - x.k2^2 - x.k3^2)/2)
    + X.c 1 * Y.c 3 * (x.e1p2)
    + X.c 1 * Y.c 5 * (x.e3p2)
    + X.c 1 * Y.c 6 * (x.e4p2)
    + X.c 2 * Y.c 0 * (x.k1*x.k3)
    + X.c 2 * Y.c 1 * ((tz x - x.k2^2 - x.k3^2)/2)
    + X.c 2 * Y.c 2 * (x.k3^2)
    + X.c 2 * Y.c 4 * (x.e2p3)
    + X.c 2 * Y.c 6 * ((-x.e4p1 - x.e4p2))
    + X.c 3 * Y.c 1 * (x.e1p2)
    + X.c 3 * Y.c 4 * (x.ee12)
    + X.c 3 * Y.c 6 * (x.ee14)
    + X.c 4 * Y.c 0 * (x.e2p1)
    + X.c 4 * Y.c 2 * (x.e2p3)
    + X.c 4 * Y.c 3 * (x.ee12)
    + X.c 4 * Y.c 5 * (x.ee23)
    + X.c 4 * Y.c 6 * (x.ee24)
    + X.c 5 * Y.c 1 * (x.e3p2)
    + X.c 5 * Y.c 4 * (x.ee23)
    + X.c 5 * Y.c 6 * (x.ee34)
    + X.c 6 * Y.c 0 * (x.e4p1)
    + X.c 6 * Y.c 1 * (x.e4p2)
    + X.c 6 * Y.c 2 * ((-x.e4p1 - x.e4p2))
    + X.c 6 * Y.c 3 * (x.ee14)
    + X.c 6 * Y.c 4 * (x.ee24)
    + X.c 6 * Y.c 5 * (x.ee34) := by
  simp only [dot4, gram, Fin.sum_univ_succ, Fin.sum_univ_zero]
  simp
  ring

/-- 5th-component product (mostly-minus in the extra dimension). -/
def dot5 (X Y : Vec) : ℚ := -(X.f * Y.f)

/-- External momenta `P1..P4` (5th component = vev difference).

Also known as: BR5p.P, external momenta P₁..P₄ (5th = vev difference).
-/
def extMomenta (x : Inv) : Fin 4 → Vec := ![
  ⟨![1,0,0,0,0,0,0], x.k1⟩, ⟨![0,1,0,0,0,0,0], x.k2⟩, ⟨![0,0,1,0,0,0,0], x.k3⟩,
  ⟨![-1,-1,-1,0,0,0,0], -(x.k1 + x.k2 + x.k3)⟩]
/-- External W polarisations. -/
def E : Fin 4 → Vec := ![
  ⟨![0,0,0,1,0,0,0], 0⟩, ⟨![0,0,0,0,1,0,0], 0⟩, ⟨![0,0,0,0,0,1,0], 0⟩, ⟨![0,0,0,0,0,0,1], 0⟩]

open Vec in
/-- Off-shell current from the cyclic three-vertex V3(1,2,−(1+2)), with VVV `lam3`, VVS `a` and VSS
  `gs` parts. -/
def J (x : Inv) (E1 K1 E2 K2 : Vec) : Vec :=
  let K3 := neg (add K1 K2)
  let D := add K1 (neg K2)
  let e4 := dot4 x E1 E2
  let e5 := dot5 E1 E2
  let t1 := add (smul (x.lam3 * e4 + x.gs * e5) (d4 D)) (smul (x.a * e4) (d5 D))
  let term := fun (Ea Kx Ky Eb : Vec) =>
    let Q := add Kx (neg Ky)
    let q4 := dot4 x Q Eb
    let q5 := dot5 Q Eb
    add (smul (x.lam3 * q4 + x.a * q5) (d4 Ea)) (smul (x.gs * q4) (d5 Ea))
  add t1 (add (term E2 K2 K3 E1) (term E1 K3 K1 E2))

/-- Exchange numerator J_a·J_b: 4D part minus the product of 5th components (Goldstone/Higgs
  exchange). -/
def exch (x : Inv) (Ja Jb : Vec) : ℚ := dot4 x Ja Jb - Ja.f * Jb.f

/-- s-channel numerator (12)(34). -/
def ns (x : Inv) : ℚ := exch x (J x (E 0) (extMomenta x 0) (E 1) (extMomenta x 1)) (J x (E 2) (extMomenta x 2) (E 3) (extMomenta x 3))
/-- t-channel numerator (23)(41). -/
def nt (x : Inv) : ℚ := exch x (J x (E 1) (extMomenta x 1) (E 2) (extMomenta x 2)) (J x (E 3) (extMomenta x 3) (E 0) (extMomenta x 0))

/-- Contact pairing with VVVV `lam4`, VVSS `b`, SSSS 1. -/
def pr (x : Inv) (X Y Z W : Vec) : ℚ :=
  x.lam4 * dot4 x X Y * dot4 x Z W + x.b * (dot4 x X Y * dot5 Z W + dot5 X Y * dot4 x Z W)
    + dot5 X Y * dot5 Z W
/-- Four-vector contact term 2(13)(24) − (12)(34) − (14)(23). -/
def ct (x : Inv) : ℚ :=
  2 * pr x (E 0) (E 2) (E 1) (E 3) - pr x (E 0) (E 1) (E 2) (E 3) - pr x (E 0) (E 3) (E 1) (E 2)

/-- Masses² of the s- and t-channel internal lines. -/
def Ms (x : Inv) : ℚ := (x.k1 + x.k2)^2
/-- t-channel internal mass². -/
def Mt (x : Inv) : ℚ := (x.k2 + x.k3)^2

/-- Amplitude × both propagators, assembled from the Feynman rules on the hidden-zero locus. -/
def Nbuilt (x : Inv) : ℚ :=
  ns x * (tz x - Mt x) + nt x * (x.s - Ms x) + ct x * (x.s - Ms x) * (tz x - Mt x)

/-- Contact term on the locus (VVSS `b` and SSSS drop out for external W). -/
theorem ct_eq (x : Inv) : ct x = -x.ee12*x.ee34*x.lam4 - x.ee14*x.ee23*x.lam4 := by
  simp [ct, pr, dot4_explicit, dot5, E]
  ring

/-- s-channel numerator on the hidden-zero locus (VSS `gs` drops out). -/
theorem ns_eq (x : Inv) : ns x = -x.a^2*x.ee12*x.ee34*x.k1^2 - 2*x.a^2*x.ee12*x.ee34*x.k1*x.k3 + x.a^2*x.ee12*x.ee34*x.k2^2 + 2*x.a^2*x.ee12*x.ee34*x.k2*x.k3 + 4*x.e1p2*x.e2p3*x.ee34*x.lam3^2 - 4*x.e1p2*x.e3p2*x.ee24*x.lam3^2 + 4*x.e1p2*x.e4p1*x.ee23*x.lam3^2 + 4*x.e1p2*x.e4p2*x.ee23*x.lam3^2 + 4*x.e2p1*x.e3p2*x.ee14*x.lam3^2 - 4*x.e3p2*x.e4p1*x.ee12*x.lam3^2 + x.ee12*x.ee34*x.lam3^2*x.s - 2*x.ee12*x.ee34*x.lam3^2*x.k1*x.k2 + 2*x.ee12*x.ee34*x.lam3^2*x.k1*x.k3 - 2*x.ee12*x.ee34*x.lam3^2*x.k2^2 - 2*x.ee12*x.ee34*x.lam3^2*x.k2*x.k3 := by
  simp [ns, exch, J, dot4_explicit, dot5, tz, extMomenta, E, Vec.add, Vec.smul, Vec.neg, Vec.d4,
      Vec.d5]
  ring

/-- t-channel numerator on the hidden-zero locus. -/
theorem nt_eq (x : Inv) : nt x = 2*x.a^2*x.ee14*x.ee23*x.k1*x.k2 - 2*x.a^2*x.ee14*x.ee23*x.k1*x.k3 + x.a^2*x.ee14*x.ee23*x.k2^2 - x.a^2*x.ee14*x.ee23*x.k3^2 + 4*x.e1p2*x.e2p3*x.ee34*x.lam3^2 - 4*x.e1p2*x.e3p2*x.ee24*x.lam3^2 + 4*x.e1p2*x.e4p1*x.ee23*x.lam3^2 + 4*x.e1p2*x.e4p2*x.ee23*x.lam3^2 + 4*x.e2p1*x.e3p2*x.ee14*x.lam3^2 - 4*x.e3p2*x.e4p1*x.ee12*x.lam3^2 - x.ee14*x.ee23*x.lam3^2*x.s + x.ee14*x.ee23*x.lam3^2*x.k1^2 + 2*x.ee14*x.ee23*x.lam3^2*x.k1*x.k3 + x.ee14*x.ee23*x.lam3^2*x.k3^2 := by
  simp [nt, exch, J, dot4_explicit, dot5, tz, extMomenta, E, Vec.add, Vec.smul, Vec.neg, Vec.d4,
      Vec.d5]
  ring

/-- **A-4 closed for `EWZ1b.N`:** the Feynman-rule construction equals the script-generated
  polynomial. -/
theorem built_eq_N (x : Inv) :
    Nbuilt x = PositiveGeometryEmergentSpaceTime.EWZ1b.N x.a x.e1p2 x.e2p1 x.e2p3 x.e3p2 x.e4p1 x.e4p2 x.ee12 x.ee14 x.ee23 x.ee24
      x.ee34 x.k1 x.k2 x.k3 x.lam3 x.lam4 x.s := by
  rw [Nbuilt, ns_eq, nt_eq, ct_eq]
  unfold PositiveGeometryEmergentSpaceTime.EWZ1b.N tz Ms Mt
  ring

/-- Consequence: the CGW zero holds for the *constructed* amplitude at SM couplings. -/
theorem built_zero_of_gauge (x : Inv) (ha : x.a ^ 2 = x.lam3 ^ 2) (h4 : x.lam4 = x.lam3 ^ 2) :
    Nbuilt x = 0 := by
  rw [built_eq_N]; exact PositiveGeometryEmergentSpaceTime.EWZ1b.zero_of_gauge _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ha h4

/-- Non-vacuity witness: the construction is not identically zero (lam4 defect alone, explicit
  point). -/
theorem br5p_witness :
    Nbuilt ⟨0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0⟩ ≠ 0 := by
  rw [built_eq_N]; unfold PositiveGeometryEmergentSpaceTime.EWZ1b.N; norm_num

/-- Review (2026-10-14) non-vacuity of `built_zero_of_gauge`: the gauge hypotheses are satisfiable at a point
where the s-channel numerator alone is nonzero, so the zero is a genuine cancellation between diagrams. -/
theorem br5p_gauge_witness_nontrivial :
    let x : Inv := ⟨1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0⟩
    x.a ^ 2 = x.lam3 ^ 2 ∧ x.lam4 = x.lam3 ^ 2 ∧ ns x ≠ 0 ∧ Nbuilt x = 0 := by
  intro x
  refine ⟨by norm_num [x], by norm_num [x], ?_,
      built_zero_of_gauge x (by norm_num [x]) (by norm_num [x])⟩
  rw [ns_eq]; norm_num [x]

end PositiveGeometryEmergentSpaceTime.BR5p
