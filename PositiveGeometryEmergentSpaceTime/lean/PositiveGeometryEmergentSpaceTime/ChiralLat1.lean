import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# ChiralLat1 — discrete 1D doubling lemma (CHIRAL-LATTICE-1, 2026-10-30)

Sample the sign of a periodic lattice dispersion around the Brillouin zone as a cyclic Boolean list.
An up-crossing (`false → true`) is a zero with positive slope (a right-mover), a down-crossing a left-mover.
`cyclic_ups_eq_dns`: around any closed loop the two counts are equal — the 1D shadow of Nielsen–Ninomiya
(chiral zeros come in opposite-chirality pairs). `naive_sin8`: the naive sin(2πk/8) sign pattern has one of each.
-/

namespace PositiveGeometryEmergentSpaceTime.ChiralLat1

/-- 0/1 value of a sign bit. -/
def b2i (b : Bool) : ℤ := if b then 1 else 0

/-- Up-crossings along a list (false followed by true). -/
def ups : List Bool → ℕ
  | a :: b :: t => (if (!a && b) then 1 else 0) + ups (b :: t)
  | _ => 0

/-- Down-crossings along a list (true followed by false). -/
def dns : List Bool → ℕ
  | a :: b :: t => (if (a && !b) then 1 else 0) + dns (b :: t)
  | _ => 0

/-- Telescoping: along an open list, ups − downs = last − first. -/
theorem ups_sub_dns (a : Bool) (t : List Bool) :
    (ups (a :: t) : ℤ) - dns (a :: t) = b2i ((a :: t).getLast (by simp)) - b2i a := by
  induction t generalizing a with
  | nil => simp [ups, dns]
  | cons b t ih =>
    have h := ih b
    simp only [ups, dns, List.getLast_cons_cons] at h ⊢
    push_cast
    cases a <;> cases b <;> simp [b2i] at h ⊢ <;> linarith

/-- Last element of `b :: t ++ [a]` is `a`. -/
theorem getLast_snoc (b a : Bool) (t : List Bool) : (b :: (t ++ [a])).getLast (by simp) = a := by
  induction t generalizing b with
  | nil => rfl
  | cons c t ih => simp only [List.cons_append, List.getLast_cons_cons]; exact ih c

/-- Closed loop (first sample repeated at the end): as many up- as down-crossings. -/
theorem cyclic_ups_eq_dns (a : Bool) (t : List Bool) : ups (a :: t ++ [a]) = dns (a :: t ++ [a]) := by
  have h := ups_sub_dns a (t ++ [a])
  simp only [List.cons_append] at h ⊢
  rw [getLast_snoc] at h
  omega

/-- Naive sin(2πk/8), k = 0..7, sign bit `> 0` with k = 0, 4 at the zeros read as `false`; closed loop. -/
theorem naive_sin8 : ups [false, true, true, true, false, false, false, false, false] = 1 ∧
    dns [false, true, true, true, false, false, false, false, false] = 1 := by
  decide

end PositiveGeometryEmergentSpaceTime.ChiralLat1
