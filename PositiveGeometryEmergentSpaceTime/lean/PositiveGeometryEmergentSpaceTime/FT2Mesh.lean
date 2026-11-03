/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib
import PositiveGeometryEmergentSpaceTime.DecayZeroNoGo

/-!
FT-2. Quark-line (U(3), SU(3)-broken) mesh variables. Planar X_{a,b} = (p_a+…+p_{b-1})² −
(μ_{f a} + μ_{f b}), where meson (f a, f (a+1)) has mass² μ_{f a} + μ_{f (a+1)}. The massive
mesh variable c̃_{a,b} = X_{a,b} + X_{a+1,b+1} − X_{a,b+1} − X_{a+1,b} equals the massless one:
all unequal quark-mass shifts cancel identically. Hence the CGW zero loci are p_a·p_b = 0
(c = −2 p_a·p_b) for any quark masses. Plus: such a locus is never in a physical region
(massive, positive energies): same-side pairs have p·p ≥ m m, crossed pairs p·p ≤ −m m.
-/

namespace PositiveGeometryEmergentSpaceTime.FT2Mesh

/-- Mass shifts cancel in the mesh combination, for arbitrary (unequal) quark-mass spurions. -/
theorem mesh_shift_cancels (Y11 Y22 Y12 Y21 μa μa1 μb μb1 : ℝ) :
    ((Y11 - (μa + μb)) + (Y22 - (μa1 + μb1)) - (Y12 - (μa + μb1)) - (Y21 - (μa1 + μb)))
      = Y11 + Y22 - Y12 - Y21 := by ring

/-- The massless mesh combination of planar invariants is −2 p_a·p_b (scalar form):
with S = sum of momenta strictly between, X_{a,b}=(a+S)², X_{a+1,b+1}=(S+b)²,
X_{a,b+1}=(a+S+b)², X_{a+1,b}=S². Written in Gram entries. -/
theorem mesh_is_dot (aa bb SS aS bS ab : ℝ) :
    (aa + 2*aS + SS) + (SS + 2*bS + bb) - (aa + bb + SS + 2*aS + 2*bS + 2*ab) - SS = -2*ab := by
  ring

/-- No CGW zero locus p·p = 0 is physical for 6-meson (3→3, 2→4, 1→5) kinematics: every pair is
same-side (p·p ≥ m m > 0) or crossed (all-incoming p·p ≤ −m m < 0). Reuses MR-6's `no_zero`. -/
theorem zero_unphysical (m1 m2 a1 a2 E1 E2 d : ℝ) (hm1 : 0 < m1) (hm2 : 0 < m2) (ha1 : 0 ≤ a1)
    (ha2 : 0 ≤ a2) (hE1 : 0 ≤ E1) (hE2 : 0 ≤ E2) (h1 : E1^2 = m1^2 + a1^2) (h2 : E2^2 = m2^2 + a2^2)
    (hd : d ≤ a1*a2) : E1*E2 - d ≠ 0 ∧ -(E1*E2 - d) ≠ 0 := by
  have h := PositiveGeometryEmergentSpaceTime.DecayZeroNoGo.no_zero m1 m2 a1 a2 E1 E2 d hm1 hm2 ha1 ha2 hE1 hE2 h1 h2 hd
  exact ⟨h, neg_ne_zero.mpr h⟩

end PositiveGeometryEmergentSpaceTime.FT2Mesh
