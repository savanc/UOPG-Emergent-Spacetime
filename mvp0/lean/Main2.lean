import UOPG0.Boundary

/-!
Executable witness for the algebraic face. The rationals are the ones proved in
`UOPG0.Boundary`. This program does not print a mass.
-/

open UOPG0

def main : IO Unit := do
  let x : ℚ := 1 / 2
  let y : ℚ := 1 / 2
  let z : ℚ := 3 / 2
  let w : ℚ := 1 / 2
  IO.println "UOPG MVP-2 — algebraic face of Gr+(2,4)"
  IO.println s!"drop x = {x * orthantCoeff x y z w}"
  IO.println s!"drop y = {y * orthantCoeff x y z w}"
  IO.println s!"drop z = {z * orthantCoeff x y z w}"
  IO.println s!"drop w = {w * orthantCoeff x y z w}"
  IO.println s!"P13 on the x = 0 face = {plucker (chart 0 y z w) 1 3}"
  IO.println s!"column shift P23 = {plucker (columnShift 1 positiveExample) 2 3}"
  IO.println "The face factor is not a cross section. The column shift is not a mutation."
