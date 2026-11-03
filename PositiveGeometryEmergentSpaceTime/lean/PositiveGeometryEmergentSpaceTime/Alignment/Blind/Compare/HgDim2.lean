/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara
-/
import PositiveGeometryEmergentSpaceTime.HgDim2
import PositiveGeometryEmergentSpaceTime.HgDim2P4
import PositiveGeometryEmergentSpaceTime.HgDim2P5
import PositiveGeometryEmergentSpaceTime.HgDim2P6
import PositiveGeometryEmergentSpaceTime.Alignment.Blind.HgDim2Blind

/-!
# ALIGNMENT BLIND-2 (2026-11-03) — Compare: HG-DIM-2 (permutahedron per-label κ)

Blind: `labelCost n i` = minimum over bijections of the Kendall-τ assignment cost between the closed
balls of `id` and `id·s_i` in Perm_n (n = 4, 5, 6), so `κ = 1 − cost/n = (2 − 2h)/n`.
Original: per-edge LP-dual certificates (`edgeN_i`: explicit walk matching + Lipschitz potential)
for the same edges, `hexCount` h, and the algebra `kappa_of_cost`, `mean_kappa`.

VERDICT: **EQUIV on every certified number; ORIG-STRONGER on certificate rigour.**
Both certify the same 12 (n, label) values. The blind's minimum is exact over assignments with
Kendall-τ distance, which equals the Cayley-graph (adjacent-transposition) distance — a CITED fact
not formalised in the blind module; the original's walk/dual pair proves optimality directly in the
graph. GAP: the two cost functionals are not proved equal as functions.
-/

namespace PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.HgDim2

open PositiveGeometryEmergentSpaceTime.Alignment.HgDim2Blind
open PositiveGeometryEmergentSpaceTime.HgDim2 (hexCount)

/-- Same edge: the original's `swapAt` (List.set-based) and the blind's (recursive) agree on the
identity for every label used. -/
theorem swapAt_agree :
    (∀ k : Fin 3, PositiveGeometryEmergentSpaceTime.HgDim2.swapAt (List.range 4) k = swapAt k (List.range 4)) ∧
    (∀ k : Fin 4, PositiveGeometryEmergentSpaceTime.HgDim2.swapAt (List.range 5) k = swapAt k (List.range 5)) ∧
    (∀ k : Fin 5, PositiveGeometryEmergentSpaceTime.HgDim2.swapAt (List.range 6) k = swapAt k (List.range 6)) := by
  decide +kernel

/-- Blind costs = original certified integers = `(n − 2 − h) + 3h` with the original's `hexCount`. -/
theorem costs_eq_hex :
    labelCost 4 0 = (4 - 2 - hexCount 4 0) + 3 * hexCount 4 0 ∧
    labelCost 4 1 = (4 - 2 - hexCount 4 1) + 3 * hexCount 4 1 ∧
    labelCost 4 2 = (4 - 2 - hexCount 4 2) + 3 * hexCount 4 2 ∧
    labelCost 5 0 = (5 - 2 - hexCount 5 0) + 3 * hexCount 5 0 ∧
    labelCost 5 1 = (5 - 2 - hexCount 5 1) + 3 * hexCount 5 1 ∧
    labelCost 5 2 = (5 - 2 - hexCount 5 2) + 3 * hexCount 5 2 ∧
    labelCost 5 3 = (5 - 2 - hexCount 5 3) + 3 * hexCount 5 3 ∧
    labelCost 6 0 = (6 - 2 - hexCount 6 0) + 3 * hexCount 6 0 ∧
    labelCost 6 1 = (6 - 2 - hexCount 6 1) + 3 * hexCount 6 1 ∧
    labelCost 6 2 = (6 - 2 - hexCount 6 2) + 3 * hexCount 6 2 ∧
    labelCost 6 3 = (6 - 2 - hexCount 6 3) + 3 * hexCount 6 3 ∧
    labelCost 6 4 = (6 - 2 - hexCount 6 4) + 3 * hexCount 6 4 := by
  obtain ⟨a0, a1, a2⟩ := p4_costs
  obtain ⟨b0, b1, b2, b3⟩ := p5_costs
  obtain ⟨c0, c1, c2, c3, c4⟩ := p6_costs
  simp only [a0, a1, a2, b0, b1, b2, b3, c0, c1, c2, c3, c4, hexCount]
  decide

/-- Blind κ equals the original's closed form `(2 − 2h)/n` with the original's `hexCount`. -/
theorem kappa_eq_orig_form :
    kappa 4 0 = (2 - 2 * (hexCount 4 0 : ℚ)) / 4 ∧ kappa 4 1 = (2 - 2 * (hexCount 4 1 : ℚ)) / 4 ∧
    kappa 4 2 = (2 - 2 * (hexCount 4 2 : ℚ)) / 4 ∧
    kappa 5 0 = (2 - 2 * (hexCount 5 0 : ℚ)) / 5 ∧ kappa 5 1 = (2 - 2 * (hexCount 5 1 : ℚ)) / 5 ∧
    kappa 5 2 = (2 - 2 * (hexCount 5 2 : ℚ)) / 5 ∧ kappa 5 3 = (2 - 2 * (hexCount 5 3 : ℚ)) / 5 ∧
    kappa 6 0 = (2 - 2 * (hexCount 6 0 : ℚ)) / 6 ∧ kappa 6 1 = (2 - 2 * (hexCount 6 1 : ℚ)) / 6 ∧
    kappa 6 2 = (2 - 2 * (hexCount 6 2 : ℚ)) / 6 ∧ kappa 6 3 = (2 - 2 * (hexCount 6 3 : ℚ)) / 6 ∧
    kappa 6 4 = (2 - 2 * (hexCount 6 4 : ℚ)) / 6 := by
  obtain ⟨a0, a1, a2⟩ := p4_costs
  obtain ⟨b0, b1, b2, b3⟩ := p5_costs
  obtain ⟨c0, c1, c2, c3, c4⟩ := p6_costs
  simp only [kappa, a0, a1, a2, b0, b1, b2, b3, c0, c1, c2, c3, c4, hexCount]
  norm_num

/-- Mean-κ formulas coincide (original's per-label form specialised with h = 1, 2). -/
theorem mean_agree (n : ℚ) (hn : 4 ≤ n) :
    (2 * ((2 - 2 * 1) / n) + (n - 3) * ((2 - 2 * 2) / n)) / (n - 1) =
      (2 * 0 + (n - 3) * (-2 / n)) / (n - 1) := by
  have h1 : n ≠ 0 := by linarith
  have h2 : n - 1 ≠ 0 := by linarith
  rw [PositiveGeometryEmergentSpaceTime.HgDim2.mean_kappa n h1 h2, mean_kappa n hn]

end PositiveGeometryEmergentSpaceTime.Alignment.Blind.Compare.HgDim2
