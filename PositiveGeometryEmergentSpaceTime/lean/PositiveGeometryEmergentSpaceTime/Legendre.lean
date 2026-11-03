/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import Mathlib

/-!
# Shared Legendre polynomials (HANG-1)

Canonical `legendreP1`…`legendreP4` used by LS residue identities (MR-1, credited) and by
massive LS / Adler–ρ placement (MassiveLS). One definition each — no duplicate copies.

Also known as: P₁…P₄, P1…P4 (prior local defs in `LSResidue` / `MassiveLS`).
-/

namespace PositiveGeometryEmergentSpaceTime.Legendre

/-- Legendre polynomial P₁(x) = x.

Also known as: P1, P₁. -/
noncomputable def legendreP1 (x : ℝ) : ℝ := x

/-- Legendre polynomial P₂(x) = (3x² − 1)/2.

Also known as: P2, P₂. -/
noncomputable def legendreP2 (x : ℝ) : ℝ := (3 * x ^ 2 - 1) / 2

/-- Legendre polynomial P₃(x) = (5x³ − 3x)/2.

Also known as: P3, P₃. -/
noncomputable def legendreP3 (x : ℝ) : ℝ := (5 * x ^ 3 - 3 * x) / 2

/-- Legendre polynomial P₄(x) = (35x⁴ − 30x² + 3)/8.

Also known as: P4, P₄. -/
noncomputable def legendreP4 (x : ℝ) : ℝ := (35 * x ^ 4 - 30 * x ^ 2 + 3) / 8

end PositiveGeometryEmergentSpaceTime.Legendre
