/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE C (2026-11-03) — JORD-1: the full Jordan identity for the 27-dimensional table.
Not part of `import PositiveGeometryEmergentSpaceTime`.
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Bridge
import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1JordanCheck

/-!
# JORD-1: full Jordan identity for J₃(𝕆)

`jm x y = Σᵢⱼ xᵢ yⱼ bc i j` is the dense product `2 x∘y` of the integer table `T1s` used by `PositiveGeometryEmergentSpaceTime.Jord1`.
We prove, for all `x y : ℚ²⁷`, `(x∘y)∘(x∘x) = x∘(y∘(x∘x))` (stated for `jm`; the factor 2 is homogeneous).

Route: expand both sides in the basis, reduce to the fully linearised defect `tD i j k l`, symmetrise over
`(i, j, k)` (the cyclic sum `cD` is fully symmetric because `tD` is symmetric in `j k`), so only sorted
triples need checking; these are `Jord1JordanCheck.allChunks` (378 kernel theorems, `decide +kernel`),
transported by the sparse–dense bridge `jm_sv`.
-/

set_option autoImplicit false
set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Jordan
open PositiveGeometryEmergentSpaceTime.Jord1 PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Sanity
open PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Bridge PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1JordanCheck

abbrev V := Fin 27 → ℚ

/-- Dense `2 x∘y`. -/
def jm (x y : V) : V := fun l => ∑ i : Fin 27, ∑ j : Fin 27, x i * y j * (bc i j l : ℚ)

theorem jm_comm (x y : V) : jm x y = jm y x := by
  funext l; unfold jm; rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [bc_comm]; ring

/-- `jm` as a bilinear map. -/
def JB : V →ₗ[ℚ] V →ₗ[ℚ] V :=
  LinearMap.mk₂ ℚ jm
    (by intro a b c; funext l; simp only [jm, Pi.add_apply, add_mul, Finset.sum_add_distrib])
    (by intro r a b; funext l; simp only [jm, Pi.smul_apply, smul_eq_mul, Finset.mul_sum, mul_assoc])
    (by intro a b c; funext l; simp only [jm, Pi.add_apply, mul_add, add_mul, Finset.sum_add_distrib])
    (by intro r a b; funext l
        simp only [jm, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_; ring)

theorem JB_apply (x y : V) : JB x y = jm x y := rfl

/-! ## Sparse–dense bridge -/

def sv (u : List (ℕ × ℤ)) : V := fun l => (coefS u l : ℚ)

theorem jm_sv (u v : List (ℕ × ℤ)) (hu : idxOK u = true) (hv : idxOK v = true) :
    jm (sv u) (sv v) = sv (prodS u v) := by
  funext l
  simp only [jm, sv, coefS_prodS]
  have e1 : ∀ a : Fin 27, ∑ b : Fin 27, (coefS u a : ℚ) * (coefS v b : ℚ) * (bc a b l : ℚ) =
      (coefS u a : ℚ) * (v.map fun q => (q.2 : ℚ) * (bc a q.1 l : ℚ)).sum := by
    intro a
    rw [← sum_coefS v hv (fun b => (bc a b l : ℚ)), Finset.mul_sum]
    exact Finset.sum_congr rfl fun b _ => by ring
  simp only [e1]
  rw [sum_coefS u hu (fun a => (v.map fun q => (q.2 : ℚ) * (bc a q.1 l : ℚ)).sum)]
  simp only [Int.cast_list_sum, List.map_map]
  congr 1; apply List.map_congr_left; intro p _
  simp only [Function.comp_apply, Int.cast_list_sum, List.map_map, ← List.sum_map_mul_left]
  congr 1; apply List.map_congr_left; intro q _
  simp only [Function.comp_apply]; push_cast; ring

theorem sv_append (u v : List (ℕ × ℤ)) : sv (u ++ v) = sv u + sv v := by
  funext l; simp [sv, coefS_append]

theorem sv_neg (u : List (ℕ × ℤ)) : sv (smulS (-1) u) = - sv u := by
  funext l; simp only [sv, smulS, Pi.neg_apply]; rw [coefS_scale]; push_cast; ring

theorem sv_eB (i : Fin 27) : sv (eB i) = Pi.single i 1 := by
  funext l
  simp only [sv, eB, coefS, add_zero, Pi.single_apply]
  by_cases h : l = i
  · subst h; simp
  · have : (i : ℕ) ≠ l := fun he => h (Fin.ext he.symm)
    simp [this, h]

theorem idx_eB (i : Fin 27) : idxOK (eB i) = true := by simp [idxOK, eB]

/-- Dense defect on basis vectors. -/
def tD (i j k l : Fin 27) : V :=
  JB (JB (Pi.single i 1) (Pi.single l 1)) (JB (Pi.single j 1) (Pi.single k 1)) -
    JB (Pi.single i 1) (JB (Pi.single l 1) (JB (Pi.single j 1) (Pi.single k 1)))

theorem tD_eq (i j k l : Fin 27) : tD i j k l = sv (tS i j k l) := by
  have hi := idx_eB i; have hj := idx_eB j; have hk := idx_eB k; have hl := idx_eB l
  simp only [tD, JB_apply, ← sv_eB, tS, sv_append, sv_neg,
    jm_sv _ _ hi hl, jm_sv _ _ hj hk, jm_sv _ _ hl (idxOK_prodS _ _ hj hk),
    jm_sv _ _ (idxOK_prodS _ _ hi hl) (idxOK_prodS _ _ hj hk),
    jm_sv _ _ hi (idxOK_prodS _ _ hl (idxOK_prodS _ _ hj hk))]
  abel

theorem tD_swap (i j k l : Fin 27) : tD i j k l = tD i k j l := by
  simp only [tD, JB_apply, jm_comm (Pi.single j 1) (Pi.single k 1)]

theorem sv_zero_of (u : List (ℕ × ℤ)) (h : zS u = true) : sv u = 0 := by
  funext m
  simp only [zS, List.all_eq_true, List.mem_range, beq_iff_eq] at h
  simp [sv, h m m.isLt]

/-- Cyclic sum on basis vectors. -/
def cD (i j k l : Fin 27) : V := tD i j k l + tD j k i l + tD k i j l

theorem cD_sorted (hc : ∀ i j : Fin 27, (i : ℕ) ≤ j → chunk2 i j = true)
    (i j k l : Fin 27) (hij : i ≤ j) (hjk : j ≤ k) : cD i j k l = 0 := by
  have h := hc i j hij
  simp only [chunk2, List.all_eq_true, List.mem_range] at h
  have h2 := h k k.isLt
  simp only [show decide ((j : ℕ) ≤ k) = true from decide_eq_true hjk, Bool.not_true,
    Bool.false_or, List.all_eq_true, List.mem_range] at h2
  have h3 := sv_zero_of _ (h2 l l.isLt)
  simp only [cS, sv_append, ← tD_eq] at h3
  exact h3

theorem cD_swap12 (i j k l : Fin 27) : cD j i k l = cD i j k l := by
  simp only [cD]; rw [tD_swap j i k, tD_swap i k j, tD_swap k j i]; abel

theorem cD_cyc (i j k l : Fin 27) : cD j k i l = cD i j k l := by
  simp only [cD]; abel

theorem cD_perms (a b c l : Fin 27) : cD a c b l = cD a b c l ∧ cD b a c l = cD a b c l ∧
    cD b c a l = cD a b c l ∧ cD c a b l = cD a b c l ∧ cD c b a l = cD a b c l := by
  refine ⟨?_, cD_swap12 a b c l, cD_cyc a b c l, ?_, ?_⟩
  · rw [cD_swap12 c a b, cD_cyc b c a, cD_cyc a b c]
  · rw [cD_cyc b c a, cD_cyc a b c]
  · rw [cD_swap12 b c a, cD_cyc a b c]

theorem cD_zero (hc : ∀ i j : Fin 27, (i : ℕ) ≤ j → chunk2 i j = true)
    (i j k l : Fin 27) : cD i j k l = 0 := by
  have P : ∀ a b c : Fin 27, a ≤ b → b ≤ c → cD a b c l = 0 ∧ cD a c b l = 0 ∧ cD b a c l = 0 ∧
      cD b c a l = 0 ∧ cD c a b l = 0 ∧ cD c b a l = 0 := by
    intro a b c h1 h2
    have z := cD_sorted hc a b c l h1 h2
    obtain ⟨e1, e2, e3, e4, e5⟩ := cD_perms a b c l
    exact ⟨z, e1 ▸ z, e2 ▸ z, e3 ▸ z, e4 ▸ z, e5 ▸ z⟩
  rcases le_total i j with h1 | h1 <;> rcases le_total j k with h2 | h2 <;>
    rcases le_total i k with h3 | h3
  all_goals first
    | exact (P i j k (by assumption) (by assumption)).1
    | exact (P i k j (by assumption) (by assumption)).2.1
    | exact (P j i k (by assumption) (by assumption)).2.2.1
    | exact (P j k i (by assumption) (by assumption)).2.2.2.2.1
    | exact (P k i j (by assumption) (by assumption)).2.2.2.1
    | exact (P k j i (by assumption) (by assumption)).2.2.2.2.2

theorem vec_eq_sum (x : V) : x = ∑ i : Fin 27, x i • (Pi.single i 1 : V) := by
  funext m; simp [Pi.single_apply, Finset.sum_apply]

theorem expand (x y : V) :
    JB (JB x y) (JB x x) - JB x (JB y (JB x x)) =
      ∑ a : Fin 27, ∑ b : Fin 27, ∑ c : Fin 27, ∑ d : Fin 27, (x d * y c * x b * x a) • tD d b a c := by
  simp only [tD, smul_sub, Finset.sum_sub_distrib]
  congr 1
  · conv_lhs => rw [vec_eq_sum x, vec_eq_sum y]
    simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply, Finset.smul_sum, smul_smul]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun l _ =>
      Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun k _ => ?_
    congr 1; ring
  · conv_lhs => rw [vec_eq_sum x, vec_eq_sum y]
    simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply, Finset.smul_sum, smul_smul]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun l _ =>
      Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun k _ => ?_
    congr 1; ring

theorem sym_zero (hc : ∀ i j : Fin 27, (i : ℕ) ≤ j → chunk2 i j = true) (w : Fin 27 → ℚ) (l : Fin 27) :
    ∑ i : Fin 27, ∑ j : Fin 27, ∑ k : Fin 27, (w i * w j * w k) • tD i j k l = 0 := by
  set S := ∑ i : Fin 27, ∑ j : Fin 27, ∑ k : Fin 27, (w i * w j * w k) • tD i j k l with hS
  have h1 : ∑ i : Fin 27, ∑ j : Fin 27, ∑ k : Fin 27, (w i * w j * w k) • tD j k i l = S := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun k _ => Finset.sum_congr rfl fun i _ => ?_
    congr 1; ring
  have h2 : ∑ i : Fin 27, ∑ j : Fin 27, ∑ k : Fin 27, (w i * w j * w k) • tD k i j l = S := by
    have : ∀ i : Fin 27, ∑ j : Fin 27, ∑ k : Fin 27, (w i * w j * w k) • tD k i j l =
        ∑ k : Fin 27, ∑ j : Fin 27, (w i * w j * w k) • tD k i j l := fun i => Finset.sum_comm
    simp only [this]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun k _ => Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    congr 1; ring
  have h3 : ∑ i : Fin 27, ∑ j : Fin 27, ∑ k : Fin 27, (w i * w j * w k) • cD i j k l = 0 := by
    simp [cD_zero hc]
  simp only [cD, smul_add, Finset.sum_add_distrib, h1, h2] at h3
  have : (3 : ℚ) • S = 0 := by rw [← h3]; module
  exact (smul_eq_zero.mp this).resolve_left (by norm_num)

theorem jordanJB (hc : ∀ i j : Fin 27, (i : ℕ) ≤ j → chunk2 i j = true) (x y : V) :
    JB (JB x y) (JB x x) = JB x (JB y (JB x x)) := by
  rw [← sub_eq_zero, expand]
  have r1 : ∀ a : Fin 27, ∑ b : Fin 27, ∑ c : Fin 27, ∑ d : Fin 27, (x d * y c * x b * x a) • tD d b a c =
      ∑ c : Fin 27, ∑ b : Fin 27, ∑ d : Fin 27, (x d * y c * x b * x a) • tD d b a c :=
    fun a => Finset.sum_comm
  simp only [r1]
  rw [Finset.sum_comm]
  refine Finset.sum_eq_zero fun c _ => ?_
  have r2 : ∀ a : Fin 27, ∑ b : Fin 27, ∑ d : Fin 27, (x d * y c * x b * x a) • tD d b a c =
      ∑ d : Fin 27, ∑ b : Fin 27, (x d * y c * x b * x a) • tD d b a c := fun a => Finset.sum_comm
  simp only [r2]
  rw [Finset.sum_comm]
  have r3 : ∀ d : Fin 27, ∑ a : Fin 27, ∑ b : Fin 27, (x d * y c * x b * x a) • tD d b a c =
      ∑ b : Fin 27, ∑ a : Fin 27, y c • ((x d * x b * x a) • tD d b a c) := by
    intro d; rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun b _ => Finset.sum_congr rfl fun a _ => ?_
    rw [smul_smul]; congr 1; ring
  simp only [r3, ← Finset.smul_sum, sym_zero hc x c, smul_zero]

/-- **JORD-1 (full Jordan identity).** For the 27-dimensional table, `(x∘y)∘(x∘x) = x∘(y∘(x∘x))`. -/
theorem jordan (x y : V) : jm (jm x y) (jm x x) = jm x (jm y (jm x x)) := jordanJB allChunks x y

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.Jord1Jordan
