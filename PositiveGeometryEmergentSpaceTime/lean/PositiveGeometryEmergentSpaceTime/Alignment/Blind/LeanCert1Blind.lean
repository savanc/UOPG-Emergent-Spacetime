/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT BLIND-2 (2026-11-03) — BLIND second formalisation of LEAN-CERT-1.
Written ONLY from Paper II v8 §"LEAN-CERT-1" prose ("the ABHY dimension count for n = 5,6,7 …
dim ker C = n(n−3)/2" and "N_ACC = 2 (the number of hypercharge solutions in the
graded-positroid test)") and Paper I v9, BEFORE opening the original module, the certificate
checker, the blueprint row or generated/lean/nacc_eq_two.lean.

AMBIGUITIES (both readings are the blind author's choice, logged in BLIND-2026-11-03.md):
 (A) "C" is not defined in the prose. Reading: C is the momentum-conservation map on the
     n(n−1)/2 Mandelstams s_ij of n massless particles, (C s)_a = Σ_{b≠a} s_ab, so ker C is the
     (n(n−3)/2)-dimensional kinematic space of ABHY. We prove this for ALL n ≥ 3 (C is onto),
     and instantiate n = 5, 6, 7.
 (B) "N_ACC" is not defined. Reading: the number of rational solutions (Y_u, Y_d, Y_L, Y_e) of
     the four one-generation ACC with Y_Q fixed to 1/6. Result 2 (the SM and its u↔d swap).
     Other natural readings give other numbers: counting projective solutions without fixing
     Y_Q ≠ 0 adds the Y_Q = 0 line (Y_u = −Y_d, Y_L = Y_e = 0), giving 3; identifying u↔d gives 1.
-/
import Mathlib

namespace PositiveGeometryEmergentSpaceTime.Alignment.LeanCert1Blind

open Finset

/-! ### (A) ABHY kinematic-space dimension -/

/-- unordered pairs i < j of particle labels -/
abbrev Pairs (n : ℕ) := {p : Fin n × Fin n // p.1 < p.2}

/-- value of a Mandelstam vector on the unordered pair {a, b} (0 on the diagonal) -/
def sv {n : ℕ} (s : Pairs n → ℚ) (a b : Fin n) : ℚ :=
  if h : a < b then s ⟨(a, b), h⟩ else if h' : b < a then s ⟨(b, a), h'⟩ else 0

/-- momentum conservation: (C s)_a = Σ_{b ≠ a} s_ab -/
def C (n : ℕ) : (Pairs n → ℚ) →ₗ[ℚ] (Fin n → ℚ) where
  toFun s a := ∑ b, sv s a b
  map_add' s t := by
    funext a; simp only [Pi.add_apply, ← sum_add_distrib]
    refine sum_congr rfl fun b _ => ?_
    unfold sv; split_ifs <;> simp
  map_smul' c s := by
    funext a; simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, mul_sum]
    refine sum_congr rfl fun b _ => ?_
    unfold sv; split_ifs <;> simp

lemma sv_symm_fun {n : ℕ} (F : Fin n → Fin n → ℚ) (hF : ∀ a b, F a b = F b a) (a b : Fin n) :
    sv (fun p : Pairs n => F p.1.1 p.1.2) a b = if b = a then 0 else F a b := by
  unfold sv
  split_ifs <;> first | rfl | exact hF _ _ | (exfalso; omega)

/-- C is onto for n ≥ 3 (explicit right inverse). -/
theorem C_surjective (n : ℕ) (hn : 3 ≤ n) : Function.Surjective (C n) := by
  intro v
  set S := ∑ b, v b
  have h1 : ((n : ℚ) - 1) ≠ 0 := by
    have : (3 : ℚ) ≤ n := by exact_mod_cast hn
    linarith
  have h2 : ((n : ℚ) - 2) ≠ 0 := by
    have : (3 : ℚ) ≤ n := by exact_mod_cast hn
    linarith
  let F : Fin n → Fin n → ℚ := fun a b => (v a + v b) / (n - 2) - S / ((n - 1) * (n - 2))
  refine ⟨fun p => F p.1.1 p.1.2, ?_⟩
  funext a
  show ∑ b, sv _ a b = v a
  rw [sum_congr rfl (fun b _ => sv_symm_fun F (fun x y => by simp only [F]; ring) a b)]
  rw [sum_ite, sum_const_zero, zero_add]
  have hfilt : (univ.filter fun b : Fin n => ¬ b = a) = univ.erase a := by
    ext b; simp
  rw [hfilt, sum_erase_eq_sub (mem_univ a)]
  simp only [F, ← sum_div, sum_add_distrib, sum_const, card_univ, Fintype.card_fin, nsmul_eq_mul,
    sum_sub_distrib]
  field_simp
  ring

/-- general count: dim ker C = #pairs − n, for every n ≥ 3. -/
theorem finrank_ker_C (n : ℕ) (hn : 3 ≤ n) :
    Module.finrank ℚ (LinearMap.ker (C n)) = Fintype.card (Pairs n) - n := by
  have hr := LinearMap.finrank_range_add_finrank_ker (C n)
  rw [LinearMap.range_eq_top.mpr (C_surjective n hn), finrank_top,
    Module.finrank_fintype_fun_eq_card, Module.finrank_fintype_fun_eq_card,
    Fintype.card_fin] at hr
  omega

theorem card_pairs5 : Fintype.card (Pairs 5) = 10 := by decide
theorem card_pairs6 : Fintype.card (Pairs 6) = 15 := by decide
theorem card_pairs7 : Fintype.card (Pairs 7) = 21 := by decide

/-- BLIND CLAIM (ABHY count, n = 5, 6, 7): dim ker C = n(n−3)/2. -/
theorem abhy_count_5 : Module.finrank ℚ (LinearMap.ker (C 5)) = 5 * (5 - 3) / 2 := by
  rw [finrank_ker_C 5 (by norm_num), card_pairs5]
theorem abhy_count_6 : Module.finrank ℚ (LinearMap.ker (C 6)) = 6 * (6 - 3) / 2 := by
  rw [finrank_ker_C 6 (by norm_num), card_pairs6]
theorem abhy_count_7 : Module.finrank ℚ (LinearMap.ker (C 7)) = 7 * (7 - 3) / 2 := by
  rw [finrank_ker_C 7 (by norm_num), card_pairs7]

/-! ### (B) N_ACC -/

structure Hyp where
  yQ : ℚ
  yu : ℚ
  yd : ℚ
  yL : ℚ
  ye : ℚ

def ACC (y : Hyp) : Prop :=
  6 * y.yQ + 3 * y.yu + 3 * y.yd + 2 * y.yL + y.ye = 0 ∧
  2 * y.yQ + y.yu + y.yd = 0 ∧
  3 * y.yQ + y.yL = 0 ∧
  6 * y.yQ ^ 3 + 3 * y.yu ^ 3 + 3 * y.yd ^ 3 + 2 * y.yL ^ 3 + y.ye ^ 3 = 0

def solSet : Set Hyp := {y | y.yQ = 1/6 ∧ ACC y}

theorem solSet_eq : solSet = {⟨1/6, -2/3, 1/3, -1/2, 1⟩, ⟨1/6, 1/3, -2/3, -1/2, 1⟩} := by
  ext ⟨q, u, d, l, e⟩
  simp only [solSet, ACC, Set.mem_ofPred_eq, Set.mem_insert_iff, Set.mem_singleton_iff,
    Hyp.mk.injEq]
  constructor
  · rintro ⟨rfl, hg, h3, h2, hc⟩
    have hl : l = -1/2 := by linarith
    have hd : d = -1/3 - u := by linarith
    have he : e = 1 := by subst hl hd; linarith
    subst hl hd he
    have key : (u + 2/3) * (u - 1/3) = 0 := by linear_combination (-1/3 : ℚ) * hc
    rcases mul_eq_zero.mp key with h | h
    · left; refine ⟨rfl, by linarith, by linarith, rfl, rfl⟩
    · right; refine ⟨rfl, by linarith, by linarith, rfl, rfl⟩
  · rintro (⟨rfl, rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl, rfl⟩) <;> norm_num

/-- BLIND CLAIM: N_ACC = 2 (reading B). -/
theorem nacc_eq_two_blind : solSet.ncard = 2 := by
  rw [solSet_eq, Set.ncard_pair]
  simp only [ne_eq, Hyp.mk.injEq]; norm_num

/-- Ambiguity witness: with Y_Q = 0 the ACC have a whole line of solutions. -/
theorem yq_zero_line (u : ℚ) : ACC ⟨0, u, -u, 0, 0⟩ := by
  unfold ACC; refine ⟨by ring, by ring, by ring, by ring⟩

theorem yq_zero_classification (u d l e : ℚ) : ACC ⟨0, u, d, l, e⟩ ↔ (d = -u ∧ l = 0 ∧ e = 0) := by
  unfold ACC
  constructor
  · rintro ⟨hg, h3, h2, _⟩
    refine ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨rfl, rfl, rfl⟩; refine ⟨by ring, by ring, by ring, by ring⟩

end PositiveGeometryEmergentSpaceTime.Alignment.LeanCert1Blind
