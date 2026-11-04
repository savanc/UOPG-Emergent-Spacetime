/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# H-T3b: the Ising star–triangle move and the ABJM loop factor (n = 3)

Prereg: `prereg/H-T3b-loop-factor-2026-10-12.md`. Exact counterpart of HWX 1402.1479 eq. (2.55) in Galashin–Pylyavskyy
Ising variables (`s = sech 2J`, `c = tanh 2J`), with `u = tanh K` the triangle couplings.

* `hasDerivAt_mobius`: derivative of `(a + b x)/(1 + c x)` — every boundary correlation of the triangle is of this
  form in each single coupling.
* `jac_triangle`: the 3×3 Jacobian determinant `det(∂m/∂u) = Π(1 − u²)/(1 + u₁u₂u₃)⁴`.
* `star_triangle_loop`: with the equivalent star determined by `t_i² = m_ij m_ik / m_jk`,
  `det(∂ log sinh 2K/∂ log sinh 2L)` (in its implicit-function form) equals `−J_Y/J_Δ`, where
  `J_Y = 1 + Π sech 2L_i` and `J_Δ = 1 + Π tanh 2K_ij`.
No `sorry`, no `native_decide`, no custom axioms. The derivation of `J_Y`, `J_Δ` from Lee's measure is exact in sympy
(`scripts/ht3b_symbolic_n3.py`), not in Lean.
-/

namespace PositiveGeometryEmergentSpaceTime.IsingLoop

/-- Derivative of the Möbius map `y ↦ (a + b y)/(1 + c y)` at `x` (where `1 + c x ≠ 0`) is `(b − a
  c)/(1 + c x)²`. -/
theorem hasDerivAt_mobius (a b c x : ℝ) (h : 1 + c * x ≠ 0) :
    HasDerivAt (fun y => (a + b * y) / (1 + c * y)) ((b - a * c) / (1 + c * x) ^ 2) x := by
  have h1 : HasDerivAt (fun y => a + b * y) b x := by
    simpa using ((hasDerivAt_id x).const_mul b).const_add a
  have h2 : HasDerivAt (fun y => 1 + c * y) c x := by
    simpa using ((hasDerivAt_id x).const_mul c).const_add 1
  convert h1.div h2 h using 1
  field_simp
  ring

/-- Triangle (Δ network) boundary correlations, `u = (u₁₂, u₁₃, u₂₃) = tanh K` (high-temperature
  expansion). -/
noncomputable def m12 (u₁ u₂ u₃ : ℝ) : ℝ := (u₁ + u₂ * u₃) / (1 + u₁ * u₂ * u₃)
/-- Loop-corrected correlator `m₁₃ = (u₂ + u₁u₃)/(1 + u₁u₂u₃)` of the three-edge Ising loop. -/
noncomputable def m13 (u₁ u₂ u₃ : ℝ) : ℝ := (u₂ + u₁ * u₃) / (1 + u₁ * u₂ * u₃)
/-- Loop-corrected correlator `m₂₃ = (u₃ + u₁u₂)/(1 + u₁u₂u₃)` of the three-edge Ising loop. -/
noncomputable def m23 (u₁ u₂ u₃ : ℝ) : ℝ := (u₃ + u₁ * u₂) / (1 + u₁ * u₂ * u₃)

/-- 3×3 determinant (rule of Sarrus), rows `(a b c) (d e f) (g h i)`. -/
def det3 (a b c d e f g h i : ℝ) : ℝ := a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

/-- Scaling all nine entries of a 3×3 determinant by `1/w` divides it by `w³`. -/
theorem det3_div (a b c d e f g h i w : ℝ) (hw : w ≠ 0) :
    det3 (a / w) (b / w) (c / w) (d / w) (e / w) (f / w) (g / w) (h / w) (i / w) = det3 a b c d e f g h i / w ^ 3 := by
  simp only [det3]; field_simp

/-- The Jacobian rows are `∂m₁₂, ∂m₁₃, ∂m₂₃` w.r.t. `(u₁, u₂, u₃)`; the three `m₁₂` partials are proved here (the
others follow by the symmetry `m₁₃(u₁,u₂,u₃) = m₁₂(u₂,u₁,u₃)`, `m₂₃(u₁,u₂,u₃) = m₁₂(u₃,u₁,u₂)`). The determinant: -/
theorem jac_symm (u₁ u₂ u₃ : ℝ) : m13 u₁ u₂ u₃ = m12 u₂ u₁ u₃ ∧ m23 u₁ u₂ u₃ = m12 u₃ u₁ u₂ := by
  simp only [m12, m13, m23]; constructor <;> congr 1 <;> try ring

/-- The nine partial derivatives (each from `hasDerivAt_mobius`) and their determinant. -/
theorem jac_triangle {u₁ u₂ u₃ : ℝ} (h : 1 + u₁ * u₂ * u₃ ≠ 0) :
    let Z := 1 + u₁ * u₂ * u₃
    HasDerivAt (fun x => m12 x u₂ u₃) ((1 - u₂ ^ 2 * u₃ ^ 2) / Z ^ 2) u₁ ∧
    HasDerivAt (fun x => m12 u₁ x u₃) ((u₃ - u₁ ^ 2 * u₃) / Z ^ 2) u₂ ∧
    HasDerivAt (fun x => m12 u₁ u₂ x) ((u₂ - u₁ ^ 2 * u₂) / Z ^ 2) u₃ ∧
    det3 ((1 - u₂ ^ 2 * u₃ ^ 2) / Z ^ 2) ((u₃ - u₁ ^ 2 * u₃) / Z ^ 2) ((u₂ - u₁ ^ 2 * u₂) / Z ^ 2)
         ((u₃ - u₂ ^ 2 * u₃) / Z ^ 2) ((1 - u₁ ^ 2 * u₃ ^ 2) / Z ^ 2) ((u₁ - u₂ ^ 2 * u₁) / Z ^ 2)
         ((u₂ - u₃ ^ 2 * u₂) / Z ^ 2) ((u₁ - u₃ ^ 2 * u₁) / Z ^ 2) ((1 - u₁ ^ 2 * u₂ ^ 2) / Z ^ 2)
      = ((1 - u₁ ^ 2) * (1 - u₂ ^ 2) * (1 - u₃ ^ 2)) / Z ^ 4 := by
  intro Z
  refine ⟨?_, ?_, ?_, ?_⟩
  · have := hasDerivAt_mobius (u₂ * u₃) 1 (u₂ * u₃) u₁ (by convert h using 1 <;> ring)
    convert this using 1
    · funext x; simp only [m12] <;> (try congr 1) <;> (try ring)
    · simp only [Z]; congr 1 <;> try ring
  · have := hasDerivAt_mobius u₁ u₃ (u₁ * u₃) u₂ (by convert h using 1 <;> ring)
    convert this using 1
    · funext x; simp only [m12] <;> (try congr 1) <;> (try ring)
    · simp only [Z]; congr 1 <;> try ring
  · have := hasDerivAt_mobius u₁ u₂ (u₁ * u₂) u₃ (by convert h using 1)
    convert this using 1
    · funext x; simp only [m12]
    · simp only [Z]; congr 1 <;> try ring
  · have hZ2 : Z ^ 2 ≠ 0 := pow_ne_zero 2 h
    rw [det3_div _ _ _ _ _ _ _ _ _ _ hZ2]
    have key : det3 (1 - u₂ ^ 2 * u₃ ^ 2) (u₃ - u₁ ^ 2 * u₃) (u₂ - u₁ ^ 2 * u₂) (u₃ - u₂ ^ 2 * u₃)
        (1 - u₁ ^ 2 * u₃ ^ 2) (u₁ - u₂ ^ 2 * u₁) (u₂ - u₃ ^ 2 * u₂) (u₁ - u₃ ^ 2 * u₁) (1 - u₁ ^ 2 * u₂ ^ 2)
        = ((1 - u₁ ^ 2) * (1 - u₂ ^ 2) * (1 - u₃ ^ 2)) * Z ^ 2 := by
      simp only [det3, Z]; ring
    rw [key]
    have hZ : Z ≠ 0 := h
    field_simp

/-- `(1 − T)/(1 + T)` for the star's `T₁ = t₁² = m₁₂ m₁₃ / m₂₃` (i.e. `sech 2L₁`), written over the triangle couplings
(sympy factorisation, checked here by `field_simp; ring` in `star_triangle_loop`). -/
noncomputable def q1 (u₁ u₂ u₃ : ℝ) : ℝ :=
  u₃ * (1 - u₁ ^ 2) * (1 - u₂ ^ 2) /
    (u₁ ^ 2 * u₂ ^ 2 * u₃ + u₁ ^ 2 * u₃ + 2 * u₁ * u₂ * u₃ ^ 2 + 2 * u₁ * u₂ + u₂ ^ 2 * u₃ + u₃)

/-- `sech 2L₁ = (1 − t₁²)/(1 + t₁²)` equals `q1`, where `t₁² = m₁₂ m₁₃ / m₂₃`. -/
theorem sech_star_eq {u₁ u₂ u₃ : ℝ} (h1 : 0 < u₁) (h2 : 0 < u₂) (h3 : 0 < u₃) :
    let T := m12 u₁ u₂ u₃ * m13 u₁ u₂ u₃ / m23 u₁ u₂ u₃
    (1 - T) / (1 + T) = q1 u₁ u₂ u₃ := by
  intro T
  have hZ : 0 < 1 + u₁ * u₂ * u₃ := by positivity
  have hD : 0 < u₁ ^ 2 * u₂ ^ 2 * u₃ + u₁ ^ 2 * u₃ + 2 * u₁ * u₂ * u₃ ^ 2 + 2 * u₁ * u₂ + u₂ ^ 2 * u₃ + u₃ := by
    positivity
  have ha : 0 < u₃ + u₁ * u₂ := by positivity
  have hb : 0 < u₁ + u₂ * u₃ := by positivity
  have hc : 0 < u₂ + u₁ * u₃ := by positivity
  have hT : 0 < 1 + T := by simp only [T, m12, m13, m23]; positivity
  simp only [T, m12, m13, m23, q1] at hT ⊢
  rw [div_eq_div_iff hT.ne' hD.ne']
  field_simp
  ring

/-- The polynomial `a²b²c + a²c + 2abc² + 2ab + b²c + c` is positive for positive `a, b, c`. -/
theorem q1_den_pos (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    0 < a ^ 2 * b ^ 2 * c + a ^ 2 * c + 2 * a * b * c ^ 2 + 2 * a * b + b ^ 2 * c + c := by positivity

/-- **Star–triangle loop identity** (HWX eq. 2.55 in Ising variables), implicit-function form:
`[det(∂m_Y/∂t) Π t(1−t²)/(1+t²)] / [det(∂m_Δ/∂u) Π u(1−u²)/(1+u²)] = −J_Y/J_Δ`, with
`det(∂m_Y/∂t) Π t(1−t²)/(1+t²) = −2 P² Π q_i`, `P² = m₁₂m₁₃m₂₃`, `q_i = sech 2L_i`, `J_Y = 1 + q₁q₂q₃`,
`J_Δ = 1 + Π 2u/(1+u²)` (`= 1 + Π tanh 2K`). -/
theorem star_triangle_loop {u₁ u₂ u₃ : ℝ} (h1 : 0 < u₁) (h2 : 0 < u₂) (h3 : 0 < u₃)
    (h1' : u₁ < 1) (h2' : u₂ < 1) (h3' : u₃ < 1) :
    let Z := 1 + u₁ * u₂ * u₃
    let P2 := m12 u₁ u₂ u₃ * m13 u₁ u₂ u₃ * m23 u₁ u₂ u₃
    let Q := q1 u₁ u₂ u₃ * q1 u₁ u₃ u₂ * q1 u₂ u₃ u₁
    let detD := ((1 - u₁ ^ 2) * (1 - u₂ ^ 2) * (1 - u₃ ^ 2)) / Z ^ 4
    let JD := 1 + (2 * u₁ / (1 + u₁ ^ 2)) * (2 * u₂ / (1 + u₂ ^ 2)) * (2 * u₃ / (1 + u₃ ^ 2))
    (-2 * P2 * Q) / (detD * (u₁ * (1 - u₁ ^ 2) / (1 + u₁ ^ 2)) * (u₂ * (1 - u₂ ^ 2) / (1 + u₂ ^ 2)) *
      (u₃ * (1 - u₃ ^ 2) / (1 + u₃ ^ 2))) = -(1 + Q) / JD := by
  intro Z P2 Q detD JD
  have e1 : 0 < 1 - u₁ ^ 2 := by nlinarith
  have e2 : 0 < 1 - u₂ ^ 2 := by nlinarith
  have e3 : 0 < 1 - u₃ ^ 2 := by nlinarith
  have d1 := (q1_den_pos u₁ u₂ u₃ h1 h2 h3).ne'
  have d2 := (q1_den_pos u₁ u₃ u₂ h1 h3 h2).ne'
  have d3 := (q1_den_pos u₂ u₃ u₁ h2 h3 h1).ne'
  have hZ : 1 + u₁ * u₂ * u₃ ≠ 0 := by positivity
  have na : u₁ + u₂ * u₃ ≠ 0 := by positivity
  have nb : u₂ + u₁ * u₃ ≠ 0 := by positivity
  have nc : u₃ + u₁ * u₂ ≠ 0 := by positivity
  have p1 : 1 + u₁ ^ 2 ≠ 0 := by positivity
  have p2 : 1 + u₂ ^ 2 ≠ 0 := by positivity
  have p3 : 1 + u₃ ^ 2 ≠ 0 := by positivity
  have f1 := e1.ne'
  have f2 := e2.ne'
  have f3 := e3.ne'
  have g1 := h1.ne'
  have g2 := h2.ne'
  have g3 := h3.ne'
  have hJD : (1 + u₁ ^ 2) * (1 + u₂ ^ 2) * (1 + u₃ ^ 2) + 2 * u₁ * (2 * u₂) * (2 * u₃) ≠ 0 := by positivity
  simp only [Z, P2, Q, detD, JD, m12, m13, m23, q1]
  field_simp
  ring

end PositiveGeometryEmergentSpaceTime.IsingLoop
