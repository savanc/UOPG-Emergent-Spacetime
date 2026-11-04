import PositiveGeometryEmergentSpaceTime.HgDim1Mean

/-!
# HgDim1Mean9 — the n = 9 instance of `PositiveGeometryEmergentSpaceTime.HgDim1Mean` (split off for kernel memory)

429 enumerated triangulations of the 9-gon: valid (`check_9`), duplicate-free (`nodup_9`), of Catalan size
C₇ = 429 (`catalan_vals`), hence all of them (Catalan count CITED). Per-triangulation identity, ear sum
9·C₆ = 1188 and Σ_{(T,d)} p = 4950 = (2·9 − 12)C₇ + 2·9·C₆.
-/

namespace PositiveGeometryEmergentSpaceTime.HgDim1Mean

theorem check_9 : checkAll 9 = true := by decide +kernel
theorem nodup_9 : (tris 9).Nodup := List.Nodup.of_map (key 9) (by decide +kernel)
theorem counts_9 : (tris 9).length = 429 ∧ ((tris 9).map (ears 9)).sum = 9 * 132 ∧
    ((tris 9).map (sumPT 9)).sum = 4950 := by
  decide +kernel
theorem enum_eq_sumP_9 : ((((tris 9).map (sumPT 9)).sum : ℕ) : ℤ) = sumP 5 := by
  rw [counts_9.2.2, sumP_instances.2.2.2.2]; norm_num

/-- Witness (nonvacuity): the fan from vertex 0 is in the enumerated nonagon list and has exactly 2 ears. -/
theorem witness_fan_9 : ∃ s ∈ tris 9, ears 9 s = 2 :=
  ⟨[(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], by decide +kernel, by decide +kernel⟩

end PositiveGeometryEmergentSpaceTime.HgDim1Mean
