import Mathlib.Data.Matrix.Basic

/-!
# LeanCertConv — certificate-class invariance for LEAN-CERT-2 (2026-10-30, the author)

A split certificate (M, K, P, Q, d) is valid iff M K = 0, P M + K Q = d • 1 and Q K = d • 1.
Validity depends on P only through P M, so (K, P M, Q, d) is the canonical class key.
-/

namespace PositiveGeometryEmergentSpaceTime.LeanCertConv

open Matrix

variable {m n k : Type*} [Fintype m] [Fintype n] [Fintype k] [DecidableEq n] [DecidableEq k]

/-- The certificate predicate (mirror of the LEAN-CERT-2 list checker). -/
def Valid (M : Matrix m n ℤ) (K : Matrix n k ℤ) (P : Matrix n m ℤ) (Q : Matrix k n ℤ) (d : ℤ) : Prop :=
  M * K = 0 ∧ P * M + K * Q = d • (1 : Matrix n n ℤ) ∧ Q * K = d • (1 : Matrix k k ℤ)

/-- The split identity depends on P only through P * M. -/
theorem split_iff_of_PM_eq {M : Matrix m n ℤ} {K : Matrix n k ℤ} {P P' : Matrix n m ℤ}
    {Q : Matrix k n ℤ} {d : ℤ} (h : P * M = P' * M) :
    (P * M + K * Q = d • (1 : Matrix n n ℤ)) ↔ (P' * M + K * Q = d • (1 : Matrix n n ℤ)) := by
  rw [h]

/-- Full certificate validity is invariant within a class (same K, P*M, Q, d). -/
theorem valid_iff_of_PM_eq {M : Matrix m n ℤ} {K : Matrix n k ℤ} {P P' : Matrix n m ℤ}
    {Q : Matrix k n ℤ} {d : ℤ} (h : P * M = P' * M) :
    Valid M K P Q d ↔ Valid M K P' Q d := by
  unfold Valid; rw [h]

end PositiveGeometryEmergentSpaceTime.LeanCertConv
