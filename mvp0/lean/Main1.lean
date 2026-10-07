import UOPG0.Canonical

/-!
Executable witness for the orthant coefficient. The rationals are the ones
proved in `UOPG0.Canonical`. This program does not print a mass.
-/

open UOPG0

def main : IO Unit := do
  let C := positiveExample
  let x := chartX C
  let y := chartY C
  let z := chartZ C
  let w := chartW C
  IO.println "UOPG MVP-1 — orthant coefficient of Gr+(2,4)"
  IO.println s!"x = {x}"
  IO.println s!"y = {y}"
  IO.println s!"z = {z}"
  IO.println s!"w = {w}"
  IO.println s!"orthant coefficient = {orthantCoeff x y z w}"
  IO.println s!"Parke-Taylor coefficient = {parkeTaylorCoeff x y z w}"
  IO.println "The cyclic product is the negative of the ordered adjacent product."
  IO.println "Helicity weight and a cross section are not theorems of MVP-1."
