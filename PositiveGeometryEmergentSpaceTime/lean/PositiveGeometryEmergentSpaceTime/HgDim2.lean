import Mathlib.Data.Rat.Defs
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Group

/-!
# HgDim2 — permutohedron P_n = Cay(S_n, s_1..s_{n−1}): shared lemmas (HG-DIM-2, 2026-10-31)

Paper proof: notes/HG-DIM-2-permutohedron-proof-2026-10-31.md. Prereg: prereg/HG-DIM-2-permutohedron-ollivier-curvature-2026-10-31.md.
An edge of label i lies on h hexagonal 2-faces (h = 1 for an end label, 2 for an interior label) and c = n − 2 − h squares.

* General (all n): `left_mul_aut` (left multiplication is an automorphism of any right Cayley graph on
  `Equiv.Perm (Fin n)`), `label_transitive` (it maps any edge (u, u s) to any other edge (v, v s) of the same label),
  `conj_aut` (conjugation by c is an automorphism when c S c⁻¹ = S; for c = w0 it swaps labels i ↔ n − i).
* Weak duality for walk-realised matchings on any graph: `lip_walk`, `cost_lower`.
* ℚ algebra: matching cost c + 3h = n − 2 + 2h gives κ = (2 − 2h)/n (`kappa_of_cost`); the Ollivier–Forman link
  κ = κ_F/(D + 1) with κ_F = 2 − 2h, D = n − 1 (`link`); agreement with the Cushing et al. 2310.15953 Thm 1.2 + Ex 1.5
  formula (4 + 2c)/D − 2 for κ_LLY (`lly_cushing`); idleness rescaling (`idle_lazy`, `idle_half`); the mean (`mean_kappa`,
  `mean_forman`).
Not formalised: the per-edge formula for general n (paper-proved; Lean certificates for every label at n = 4, 5, 6 in
`PositiveGeometryEmergentSpaceTime.HgDim2P4`–`P6`), Kantorovich duality / Birkhoff reduction (cited), the idleness-linearity theorem (cited).
-/

namespace PositiveGeometryEmergentSpaceTime.HgDim2

/-! ## Automorphisms of right Cayley graphs on S_n (all n) -/

/-- Right Cayley adjacency: v = u s for some generator s ∈ S. -/
def cayAdj {n : ℕ} (S : Set (Equiv.Perm (Fin n))) (u v : Equiv.Perm (Fin n)) : Prop := ∃ s ∈ S, v = u * s

theorem left_mul_aut {n : ℕ} (S : Set (Equiv.Perm (Fin n))) (g u v : Equiv.Perm (Fin n)) :
    cayAdj S (g * u) (g * v) ↔ cayAdj S u v := by
  unfold cayAdj; simp only [mul_assoc, mul_right_inj]

/-- The left translation by v u⁻¹ carries the label-s edge (u, u s) to the label-s edge (v, v s). -/
theorem label_transitive {n : ℕ} (u v s : Equiv.Perm (Fin n)) :
    (v * u⁻¹) * u = v ∧ (v * u⁻¹) * (u * s) = v * s := by
  constructor <;> group

theorem conj_aut {n : ℕ} (S : Set (Equiv.Perm (Fin n))) (c : Equiv.Perm (Fin n))
    (hS : ∀ s, s ∈ S ↔ c * s * c⁻¹ ∈ S) (u v : Equiv.Perm (Fin n)) :
    cayAdj S (c * u * c⁻¹) (c * v * c⁻¹) ↔ cayAdj S u v := by
  constructor
  · rintro ⟨t, ht, h⟩
    refine ⟨c⁻¹ * t * c, (hS _).2 (by simpa [mul_assoc] using ht), ?_⟩
    have : v = c⁻¹ * (c * u * c⁻¹ * t) * c := by rw [← h]; group
    rw [this]; group
  · rintro ⟨s, hs, h⟩
    exact ⟨c * s * c⁻¹, (hS s).1 hs, by rw [h]; group⟩

/-! ## Weak duality for walk-realised matchings (any finite graph) -/

section Walks
variable {V : Type} (adj : V → V → Bool)

def walkOk : List V → Bool
  | [] => false
  | [_] => true
  | a :: b :: t => adj a b && walkOk (b :: t)

def fin (a : V) (t : List V) : V := (a :: t).getLast (List.cons_ne_nil a t)

theorem lip_walk (φ : V → Int) (hφ : ∀ i j : V, adj i j = true → φ i - φ j ≤ 1) :
    ∀ (t : List V) (a : V), walkOk adj (a :: t) = true → φ a - φ (fin a t) ≤ t.length := by
  intro t
  induction t with
  | nil => intro a _; simp [fin]
  | cons b t ih =>
    intro a h
    simp only [walkOk, Bool.and_eq_true] at h
    have h1 := hφ a b h.1
    have h2 := ih b h.2
    have hf : fin a (b :: t) = fin b t := by simp [fin]
    rw [hf]; simp only [List.length_cons, Nat.cast_add, Nat.cast_one]; linarith

theorem cost_lower (φ : V → Int) (hφ : ∀ i j : V, adj i j = true → φ i - φ j ≤ 1) :
    ∀ ws : List (V × List V), (∀ p ∈ ws, walkOk adj (p.1 :: p.2) = true) →
      ((ws.map Prod.fst).map φ).sum - ((ws.map fun p => fin p.1 p.2).map φ).sum ≤ (ws.map fun p => (p.2.length : Int)).sum := by
  intro ws
  induction ws with
  | nil => intro _; simp
  | cons p ws ih =>
    intro hw
    have h1 := lip_walk adj φ hφ p.2 p.1 (hw p (List.mem_cons_self))
    have h2 := ih (fun q hq => hw q (List.mem_cons_of_mem p hq))
    simp only [List.map_cons, List.sum_cons]; linarith
end Walks

/-! ## Computable helpers for the certificates -/

/-- Position of value a in a one-line permutation. -/
def pos : List Nat → Nat → Nat
  | [], _ => 0
  | x :: t, a => if x = a then 0 else pos t a + 1
/-- Inversion indicator of the value pair a < b (b written before a). -/
def iv (p : List Nat) (a b : Nat) : Int := if pos p b < pos p a then 1 else 0
/-- Lehmer rank (lexicographic index) of a one-line permutation. -/
def lehmer : List Nat → Nat
  | [] => 0
  | a :: t => (t.filter (· < a)).length * Nat.factorial t.length + lehmer t
/-- Swap positions k, k + 1 (right multiplication by s_k). -/
def swapAt (p : List Nat) (k : Nat) : List Nat := (p.set k (p.getD (k + 1) 0)).set (k + 1) (p.getD k 0)
/-- Number of hexagons on a label-k edge of P_n (0-based labels k = 0..n−2). -/
def hexCount (n k : Nat) : Nat := (if 0 < k then 1 else 0) + (if k + 2 < n then 1 else 0)
/-- The inversion potential for the edge (e, s_k): −[k,k+1] + ([k+1,k+2] − [k,k+2]) + ([k−1,k] − [k−1,k+1]),
hexagon terms present only when the neighbouring label exists. Each edge toggles exactly one inversion, so this
integer function is 1-Lipschitz (checked per instance by `decide`; paper-proved for all n). -/
def phiInv (n k : Nat) (p : List Nat) : Int :=
  -iv p k (k + 1)
  + (if k + 2 < n then iv p (k + 1) (k + 2) - iv p k (k + 2) else 0)
  + (if 0 < k then iv p (k - 1) k - iv p (k - 1) (k + 1) else 0)

/-! ## ℚ algebra (all n) -/

/-- Lazy (idleness 1/(D+1)) curvature from a perfect-matching cost on closed neighbourhoods of size n. -/
theorem kappa_of_cost (n h : ℚ) (hn : n ≠ 0) : 1 - ((n - 2 - h) + 3 * h) / n = (2 - 2 * h) / n := by
  field_simp; ring

/-- Ollivier–Forman link: κ = κ_F/(D + 1) with κ_F = 2 − 2h, D = n − 1. -/
theorem link (n h : ℚ) : (2 - 2 * h) / n = (2 - 2 * h) / ((n - 1) + 1) := by ring_nf

/-- κ_LLY = (2 − 2h)/(n − 1) equals 2310.15953 Thm 1.2 with deg_H = c = n − 2 − h and D = n − 1. -/
theorem lly_cushing (n h : ℚ) (hn : n - 1 ≠ 0) : (4 + 2 * (n - 2 - h)) / (n - 1) - 2 = (2 - 2 * h) / (n - 1) := by
  field_simp; ring

/-- κ_α = (1 − α) κ_LLY at α = 1/n (lazy) and α = 1/2. -/
theorem idle_lazy (n h : ℚ) (hn : n ≠ 0) (hn1 : n - 1 ≠ 0) : (1 - 1 / n) * ((2 - 2 * h) / (n - 1)) = (2 - 2 * h) / n := by
  field_simp
theorem idle_half (n h : ℚ) : (1 - 1 / 2) * ((2 - 2 * h) / (n - 1)) = (1 - h) / (n - 1) := by ring

/-- Mean over labels (each label carries n!/2 edges): 2 end labels (h = 1), n − 3 interior (h = 2), n − 1 labels. -/
theorem mean_kappa (n : ℚ) (hn : n ≠ 0) (hn1 : n - 1 ≠ 0) :
    (2 * ((2 - 2 * 1) / n) + (n - 3) * ((2 - 2 * 2) / n)) / (n - 1) = -2 * (n - 3) / (n * (n - 1)) := by
  field_simp; ring
theorem mean_forman (n : ℚ) (hn1 : n - 1 ≠ 0) :
    (2 * (2 - 2 * 1) + (n - 3) * (2 - 2 * 2)) / (n - 1) = -2 * (n - 3) / (n - 1) := by
  field_simp; ring

end PositiveGeometryEmergentSpaceTime.HgDim2
